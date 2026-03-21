from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np


THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[2]
SRC_ROOT = REPO_ROOT / "src"
PILOT_DIR = THIS_FILE.parent
DEFAULT_OUTPUT_JSON = PILOT_DIR / "comparison_results.json"
DEFAULT_CACHE_NPZ = PILOT_DIR / "comparison_cache.npz"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


pilot12 = load_module(
    "pilot12_high_load_branch_extension",
    REPO_ROOT / "proof_pilots" / "pilot_12_high_load_branch_extension" / "numerical_extension.py",
)
pilot16 = load_module(
    "pilot16_shallow_simple_support_comparator",
    REPO_ROOT / "proof_pilots" / "pilot_16_shallow_simple_support_comparator" / "shallow_simple_support_solver.py",
)

from shell_buckling.mixed_weak.axisymmetric_simple_support_background import (
    AxisymmetricSimpleSupportConfig,
    solve_axisymmetric_simple_support_continuation,
)
from shell_buckling.supporting import determinant_criterion_comparison as detcomp


LOADS_MPA = (0.02, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 4.2, 4.3, 4.3434)
LOW_LOADS_MPA = tuple(load for load in LOADS_MPA if load <= 4.3)
HIGH_LOADS_MPA = tuple(load for load in LOADS_MPA if load > 4.3)
COMMON_VARIABLES = ("theta0", "theta0p", "Phi0", "Phi0p")
DISPLAY_NAMES = {
    "theta0": "theta0",
    "theta0p": "theta0'",
    "Phi0": "Phi0",
    "Phi0p": "Phi0'",
}
CLEAR_THRESHOLD = 0.05


def serializable(value: Any) -> Any:
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (list, tuple)):
        return [serializable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): serializable(item) for key, item in value.items()}
    return str(value)


def save_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(serializable(payload), indent=2), encoding="utf-8")


def float_key(value: float) -> str:
    return f"{value:.4f}"


def elapsed_since(start_time: float) -> float:
    return time.perf_counter() - start_time


def ensure_budget(start_time: float, budget_seconds: float, stage: str) -> None:
    if elapsed_since(start_time) > budget_seconds:
        raise TimeoutError(f"Time budget exceeded during {stage}.")


def shallow_result_summary(result: Any) -> dict[str, Any]:
    return {
        "q_mpa": float(result.q_mpa),
        "success": bool(result.success),
        "message": str(result.message),
        "nodes": int(result.nodes),
        "max_rms": serializable(result.max_rms),
        "max_bc_residual": serializable(result.max_bc_residual),
        "edge_moment_residual": serializable(result.edge_moment_residual),
        "max_abs_theta0": serializable(result.max_abs_theta0),
        "max_abs_Phi0": serializable(result.max_abs_Phi0),
        "max_abs_u_z_recovered": serializable(result.max_abs_u_z_recovered),
    }


def solve_shallow_targets(loads_mpa: tuple[float, ...]) -> tuple[dict[float, Any], list[dict[str, Any]], list[float]]:
    config = pilot16.ShallowSimpleSupportConfig(
        nd_bvp=1500,
        tol=1.0e-5,
        relaxed_tol=5.0e-5,
        max_nodes=80000,
        substep_max_delta_mpa=0.25,
    )
    results = pilot16.solve_shallow_simple_support_continuation(loads_mpa, config=config)
    by_q: dict[float, Any] = {}
    summaries = []
    for item in results:
        summaries.append(shallow_result_summary(item))
        if item.success and item.solution is not None:
            by_q[float(item.q_mpa)] = item.solution
    missing = [float(q) for q in loads_mpa if float(q) not in by_q]
    return by_q, summaries, missing


def nonshallow_result_summary(result: Any) -> dict[str, Any]:
    return {
        "q_mpa": float(result.q_mpa),
        "success": bool(result.success),
        "message": str(result.message),
        "nodes": int(result.nodes),
        "seed_kind": str(result.seed_kind),
        "max_rms": serializable(result.max_rms),
        "max_bc_residual": serializable(result.max_bc_residual),
        "min_r": serializable(result.min_r),
    }


def solve_nonshallow_targets(start_time: float, budget_seconds: float) -> tuple[dict[float, Any], dict[str, Any], list[float]]:
    diagnostics: dict[str, Any] = {
        "low_path": [],
        "high_path": {},
    }
    solutions: dict[float, Any] = {}

    ensure_budget(start_time, budget_seconds, "low-load non-shallow continuation")
    low_config = AxisymmetricSimpleSupportConfig(
        nd_bvp=600,
        tol=2.0e-4,
        relaxed_tol=1.0e-3,
        max_nodes=240000,
    )
    low_results = solve_axisymmetric_simple_support_continuation(LOW_LOADS_MPA, config=low_config)
    diagnostics["low_path"] = [nonshallow_result_summary(item) for item in low_results]
    for item in low_results:
        if item.success and item.solution is not None:
            solutions[float(item.q_mpa)] = item.solution

    if HIGH_LOADS_MPA:
        ensure_budget(start_time, budget_seconds, "high-load bootstrap")
        points_by_q, bootstrap_attempts, local_anchor, older_point, previous_point, bootstrap_payload = pilot12.bootstrap_branch(
            start_time,
            budget_seconds,
        )
        diagnostics["high_path"] = {
            "bootstrap": bootstrap_payload,
            "target_steps": {},
        }
        for q_target in HIGH_LOADS_MPA:
            q_target = float(q_target)
            if q_target in points_by_q and getattr(points_by_q[q_target], "solution", None) is not None:
                solutions[q_target] = points_by_q[q_target].solution
                diagnostics["high_path"]["target_steps"][float_key(q_target)] = {
                    "status": "available_from_bootstrap",
                }
                continue

            point, attempts = pilot12.try_extension_step(
                q_target,
                older_point,
                previous_point,
                local_anchor,
                pilot12.PRIMARY_PROFILE,
                start_time,
                budget_seconds,
            )
            diagnostics["high_path"]["target_steps"][float_key(q_target)] = {
                "success": point is not None,
                "attempts": [pilot12.attempt_summary(item) for item in attempts],
            }
            if point is not None and point.solution is not None:
                solutions[q_target] = point.solution
                older_point, previous_point = previous_point, point

    missing = [float(q) for q in LOADS_MPA if float(q) not in solutions]
    return solutions, diagnostics, missing


def mapped_nonshallow_arrays(sol: Any, x_grid: np.ndarray) -> tuple[dict[str, np.ndarray], np.ndarray]:
    theta0, theta0p, Phi0p, Phi0 = detcomp.arrays_nepol_sin(sol, x_grid)
    state = np.asarray(sol.sol(x_grid), dtype=float)
    mapped = {
        "theta0": np.asarray(theta0, dtype=float),
        "theta0p": np.asarray(theta0p, dtype=float),
        "Phi0": np.asarray(Phi0, dtype=float),
        "Phi0p": np.asarray(Phi0p, dtype=float),
    }
    return mapped, state


def shallow_arrays(sol: Any, x_grid: np.ndarray) -> dict[str, np.ndarray]:
    y = np.asarray(sol.sol(x_grid), dtype=float)
    return {
        "theta0": y[1],
        "theta0p": y[0],
        "Phi0": y[3],
        "Phi0p": y[2],
    }


def segment_metrics(x: np.ndarray, candidate: np.ndarray, reference: np.ndarray, mask: np.ndarray) -> dict[str, float]:
    x_seg = x[mask]
    candidate_seg = candidate[mask]
    reference_seg = reference[mask]
    diff_seg = candidate_seg - reference_seg

    max_abs_candidate = float(np.max(np.abs(candidate_seg)))
    max_abs_reference = float(np.max(np.abs(reference_seg)))
    max_abs_diff = float(np.max(np.abs(diff_seg)))
    rel_max = max_abs_diff / max(max_abs_candidate, max_abs_reference, 1.0e-12)

    l2_diff = float(np.sqrt(np.trapezoid(diff_seg**2, x_seg)))
    l2_candidate = float(np.sqrt(np.trapezoid(candidate_seg**2, x_seg)))
    l2_reference = float(np.sqrt(np.trapezoid(reference_seg**2, x_seg)))
    rel_l2 = l2_diff / max(l2_candidate, l2_reference, 1.0e-12)

    return {
        "max_abs_diff": max_abs_diff,
        "rel_max": rel_max,
        "l2_diff": l2_diff,
        "rel_l2": rel_l2,
    }


def location_class(x_at_peak: float) -> str:
    if x_at_peak <= 0.15:
        return "center_side"
    if x_at_peak >= 0.95:
        return "right_edge"
    return "interior"


def compare_load(q_mpa: float, shallow_sol: Any, nonshallow_sol: Any, x_grid: np.ndarray) -> tuple[dict[str, Any], np.ndarray, np.ndarray, np.ndarray]:
    mapped_nonshallow, state = mapped_nonshallow_arrays(nonshallow_sol, x_grid)
    shallow_data = shallow_arrays(shallow_sol, x_grid)

    full_mask = np.ones_like(x_grid, dtype=bool)
    center_mask = x_grid <= 0.15
    bulk_mask = x_grid <= 0.95
    edge_mask = x_grid >= 0.95

    per_variable: dict[str, Any] = {}
    bulk_values: list[float] = []
    edge_values: list[float] = []
    center_values: list[float] = []
    clear_variables: list[str] = []
    clear_locations: dict[str, str] = {}
    location_counts = {"center_side": 0, "right_edge": 0, "interior": 0}

    mapped_stack = []
    shallow_stack = []
    for name in COMMON_VARIABLES:
        candidate = mapped_nonshallow[name]
        reference = shallow_data[name]
        diff = candidate - reference
        peak_idx = int(np.argmax(np.abs(diff)))
        peak_x = float(x_grid[peak_idx])
        loc = location_class(peak_x)
        location_counts[loc] += 1

        full = segment_metrics(x_grid, candidate, reference, full_mask)
        center = segment_metrics(x_grid, candidate, reference, center_mask)
        bulk = segment_metrics(x_grid, candidate, reference, bulk_mask)
        edge = segment_metrics(x_grid, candidate, reference, edge_mask)
        per_variable[name] = {
            "display_name": DISPLAY_NAMES[name],
            "x_at_max_abs_diff": peak_x,
            "location_class": loc,
            "full": full,
            "center": center,
            "bulk": bulk,
            "edge": edge,
        }
        bulk_values.append(float(bulk["rel_l2"]))
        edge_values.append(float(edge["rel_l2"]))
        center_values.append(float(center["rel_l2"]))
        if bulk["rel_l2"] >= CLEAR_THRESHOLD:
            clear_variables.append(name)
            clear_locations[name] = loc
        mapped_stack.append(candidate)
        shallow_stack.append(reference)

    distinct_clear_locations = sorted(set(clear_locations.values()))
    if not distinct_clear_locations:
        onset_loc = None
    elif len(distinct_clear_locations) == 1:
        onset_loc = distinct_clear_locations[0]
    else:
        onset_loc = "globally_mixed"

    overall = {
        "mean_bulk_rel_l2": float(np.mean(bulk_values)),
        "mean_edge_rel_l2": float(np.mean(edge_values)),
        "mean_center_rel_l2": float(np.mean(center_values)),
        "max_bulk_rel_l2": float(np.max(bulk_values)),
        "clear_variables_at_threshold": clear_variables,
        "clear_variable_locations": clear_locations,
        "clear_location_summary": onset_loc,
        "dominant_location_class": max(location_counts.items(), key=lambda item: item[1])[0],
    }
    return (
        {
            "q_mpa": float(q_mpa),
            "variables": per_variable,
            "overall": overall,
        },
        state,
        np.asarray(mapped_stack, dtype=float),
        np.asarray(shallow_stack, dtype=float),
    )


def first_clear_load(results: list[dict[str, Any]], *, require_overall: bool) -> float | None:
    for item in results:
        overall = item["overall"]
        if require_overall:
            if overall["mean_bulk_rel_l2"] >= CLEAR_THRESHOLD or len(overall["clear_variables_at_threshold"]) >= 2:
                return float(item["q_mpa"])
        else:
            if overall["clear_variables_at_threshold"]:
                return float(item["q_mpa"])
    return None


def barrier_relevance(results: list[dict[str, Any]]) -> dict[str, Any]:
    high = [item for item in results if item["q_mpa"] >= 4.0]
    if len(high) < 2:
        return {
            "label": "insufficient_high_load_data",
            "loads_considered_mpa": [item["q_mpa"] for item in high],
        }

    means = np.array([item["overall"]["mean_bulk_rel_l2"] for item in high], dtype=float)
    diffs = np.diff(means)
    reference = float(np.median(np.abs(diffs[:-1]))) if diffs.size > 1 else float(abs(diffs[-1]))
    reference = max(reference, 1.0e-12)
    last_jump_ratio = float(abs(diffs[-1]) / reference)
    last_two_locations = [item["overall"]["dominant_location_class"] for item in high[-2:]]

    label = "smooth_through_available_high_load_range"
    if last_jump_ratio > 3.0 and len(set(last_two_locations)) > 1:
        label = "possible_qualitative_change_near_ceiling"

    return {
        "label": label,
        "loads_considered_mpa": [item["q_mpa"] for item in high],
        "mean_bulk_rel_l2": means.tolist(),
        "last_jump_ratio": last_jump_ratio,
        "dominant_locations": [item["overall"]["dominant_location_class"] for item in high],
    }


def summarize_sweep(results: list[dict[str, Any]]) -> dict[str, Any]:
    loads = np.array([item["q_mpa"] for item in results], dtype=float)
    overall_bulk = np.array([item["overall"]["mean_bulk_rel_l2"] for item in results], dtype=float)
    overall_edge = np.array([item["overall"]["mean_edge_rel_l2"] for item in results], dtype=float)
    overall_center = np.array([item["overall"]["mean_center_rel_l2"] for item in results], dtype=float)

    if loads.size >= 2 and float(np.std(overall_bulk)) > 0.0:
        bulk_pearson = float(np.corrcoef(loads, overall_bulk)[0, 1])
    else:
        bulk_pearson = None

    growth_ratio = float(overall_bulk[-1] / max(overall_bulk[0], 1.0e-12))
    if bulk_pearson is not None and bulk_pearson <= -0.5:
        growth_label = "decreases_with_load"
    elif growth_ratio >= 1.5 and bulk_pearson is not None and bulk_pearson >= 0.7:
        growth_label = "grows_with_load"
    elif growth_ratio <= 1.2:
        growth_label = "roughly_load_invariant"
    else:
        growth_label = "mild_or_mixed_growth"

    per_variable = {}
    for name in COMMON_VARIABLES:
        bulk_series = np.array([item["variables"][name]["bulk"]["rel_l2"] for item in results], dtype=float)
        first_clear = next((float(item["q_mpa"]) for item in results if item["variables"][name]["bulk"]["rel_l2"] >= CLEAR_THRESHOLD), None)
        per_variable[name] = {
            "first_clear_load_mpa": first_clear,
            "high_load_bulk_rel_l2": float(bulk_series[-1]),
            "growth_ratio": float(bulk_series[-1] / max(bulk_series[0], 1.0e-12)),
        }

    first_any = first_clear_load(results, require_overall=False)
    first_overall = first_clear_load(results, require_overall=True)
    onset_load = first_overall if first_overall is not None else first_any
    onset_summary = None
    if onset_load is not None:
        onset_result = next(item for item in results if abs(item["q_mpa"] - onset_load) < 1.0e-12)
        onset_summary = {
            "q_mpa": onset_load,
            "clear_variables_at_threshold": onset_result["overall"]["clear_variables_at_threshold"],
            "clear_location_summary": onset_result["overall"]["clear_location_summary"],
            "dominant_location_class": onset_result["overall"]["dominant_location_class"],
            "peak_x_by_clear_variable": {
                name: onset_result["variables"][name]["x_at_max_abs_diff"]
                for name in onset_result["overall"]["clear_variables_at_threshold"]
            },
        }

    edge_vs_center_ratio = float(overall_edge[-1] / max(overall_center[-1], 1.0e-12))
    return {
        "clear_threshold_bulk_rel_l2": CLEAR_THRESHOLD,
        "first_any_variable_clear_load_mpa": first_any,
        "first_overall_clear_load_mpa": first_overall,
        "onset_summary": onset_summary,
        "growth_label": growth_label,
        "overall_bulk_growth_ratio": growth_ratio,
        "overall_bulk_pearson_vs_load": bulk_pearson,
        "high_load_edge_to_center_ratio": edge_vs_center_ratio,
        "per_variable": per_variable,
        "barrier_relevance": barrier_relevance(results),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--cache-npz", type=Path, default=DEFAULT_CACHE_NPZ)
    parser.add_argument("--time-budget-seconds", type=float, default=1500.0)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    start_time = time.perf_counter()
    payload: dict[str, Any] = {
        "metadata": {
            "pilot": "pilot_17_shallow_vs_nonshallow_simple_support_divergence",
            "loads_mpa_requested": list(LOADS_MPA),
            "clear_threshold_bulk_rel_l2": CLEAR_THRESHOLD,
            "output_cache_npz": str(args.cache_npz),
            "time_budget_seconds": float(args.time_budget_seconds),
            "nonshallow_path": "active 6-state simple-support background + pilot-12 high-load anchor",
            "shallow_path": "pilot-16 shallow simple-support comparator",
        },
        "status": "started",
    }
    save_json(args.output_json, payload)

    print("=== Pilot 17 shallow vs non-shallow simple-support divergence ===")
    print("Solving the new shallow simple-support comparator...")
    shallow_solutions, shallow_diagnostics, shallow_missing = solve_shallow_targets(LOADS_MPA)
    payload["shallow"] = {
        "diagnostics": shallow_diagnostics,
        "missing_loads_mpa": shallow_missing,
    }
    payload["status"] = "shallow_completed"
    save_json(args.output_json, payload)

    print("Solving the active non-shallow simple-support branch...")
    ensure_budget(start_time, float(args.time_budget_seconds), "before non-shallow solve")
    nonshallow_solutions, nonshallow_diagnostics, nonshallow_missing = solve_nonshallow_targets(
        start_time,
        float(args.time_budget_seconds),
    )
    payload["nonshallow"] = {
        "diagnostics": nonshallow_diagnostics,
        "missing_loads_mpa": nonshallow_missing,
    }
    payload["status"] = "nonshallow_completed"
    save_json(args.output_json, payload)

    compared_loads = [load for load in LOADS_MPA if load in shallow_solutions and load in nonshallow_solutions]
    if not compared_loads:
        raise RuntimeError("No common loads were available for the corrected simple-support comparison.")

    x_grid = pilot12.build_comparison_grid(pilot12.PRIMARY_PROFILE.config, n_left=1400, n_right=1000)
    results = []
    state_stack = []
    mapped_stack = []
    shallow_stack = []

    print("Computing mismatch metrics on the corrected simple-support pair...")
    for q_mpa in compared_loads:
        result, state_y, mapped_y, shallow_y = compare_load(
            q_mpa,
            shallow_solutions[q_mpa],
            nonshallow_solutions[q_mpa],
            x_grid,
        )
        results.append(result)
        state_stack.append(state_y)
        mapped_stack.append(mapped_y)
        shallow_stack.append(shallow_y)
        payload["results"] = results
        payload["status"] = f"metrics_completed_{float_key(q_mpa)}"
        save_json(args.output_json, payload)

    summary = summarize_sweep(results)
    payload["compared_loads_mpa"] = compared_loads
    payload["results"] = results
    payload["summary"] = summary
    payload["status"] = "completed"
    payload["elapsed_seconds"] = elapsed_since(start_time)
    save_json(args.output_json, payload)

    np.savez_compressed(
        args.cache_npz,
        loads_mpa=np.asarray(compared_loads, dtype=float),
        x_grid=np.asarray(x_grid, dtype=float),
        nonshallow_states=np.asarray(state_stack, dtype=float),
        mapped_nonshallow=np.asarray(mapped_stack, dtype=float),
        shallow_fields=np.asarray(shallow_stack, dtype=float),
    )

    print(f"Compared loads: {', '.join(float_key(load) for load in compared_loads)} MPa")
    print(f"First any-variable clear load: {summary['first_any_variable_clear_load_mpa']}")
    print(f"First overall clear load: {summary['first_overall_clear_load_mpa']}")
    print(f"Growth label: {summary['growth_label']}")
    print(f"Barrier relevance: {summary['barrier_relevance']['label']}")
    print(f"Results written to: {args.output_json}")
    print(f"Cache written to: {args.cache_npz}")


if __name__ == "__main__":
    main()
