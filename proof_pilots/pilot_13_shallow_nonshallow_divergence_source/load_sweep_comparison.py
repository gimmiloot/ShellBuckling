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
from scipy.integrate import solve_bvp


THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[2]
SRC_ROOT = REPO_ROOT / "src"
PILOT_DIR = THIS_FILE.parent
DEFAULT_OUTPUT_JSON = PILOT_DIR / "load_sweep_results.json"
DEFAULT_CACHE_NPZ = PILOT_DIR / "load_sweep_cache.npz"

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

from shell_buckling.mixed_weak.axisymmetric_simple_support_background import (
    AxisymmetricSimpleSupportConfig,
    solve_axisymmetric_simple_support_continuation,
)
from shell_buckling.supporting import determinant_criterion_comparison as detcomp


LOW_LOADS_MPA = (0.02, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 4.2, 4.3)
HIGH_LOADS_MPA = (4.325, 4.3275, 4.329, 4.330, 4.332, 4.335, 4.340, 4.343, 4.3434)
ALL_LOADS_MPA = tuple(sorted({*LOW_LOADS_MPA, *HIGH_LOADS_MPA}))
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


def elapsed_since(start_time: float) -> float:
    return time.perf_counter() - start_time


def ensure_budget(start_time: float, budget_seconds: float, stage: str) -> None:
    if elapsed_since(start_time) > budget_seconds:
        raise TimeoutError(f"Time budget exceeded during {stage}.")


def float_key(value: float) -> str:
    return f"{value:.4f}"


def solve_shallow_targets(loads_mpa: tuple[float, ...]) -> dict[float, Any]:
    schedule = sorted(
        {
            0.0,
            0.05,
            0.1,
            0.25,
            0.5,
            0.75,
            1.0,
            1.5,
            2.0,
            3.0,
            4.0,
            4.2,
            4.3,
            *[float(value) for value in loads_mpa],
        }
    )
    x_mesh = np.linspace(1.0 / 1500.0, 1.0, 1500)
    y_guess = np.zeros((4, x_mesh.size), dtype=float)
    previous = None
    results: dict[float, Any] = {}

    for q_mpa in schedule:
        if previous is not None:
            y_guess = previous.sol(x_mesh)
        detcomp.q = float(q_mpa) * 1.0e6
        sol = solve_bvp(
            detcomp.fun_shallow,
            detcomp.bc_sh,
            x_mesh,
            y_guess,
            tol=1.0e-5,
            max_nodes=80000,
            verbose=0,
        )
        if not sol.success:
            sol = solve_bvp(
                detcomp.fun_shallow,
                detcomp.bc_sh,
                x_mesh,
                y_guess,
                tol=5.0e-5,
                max_nodes=80000,
                verbose=0,
            )
        if not sol.success:
            raise RuntimeError(f"Shallow continuation failed at q={q_mpa:.4f} MPa: {sol.message}")
        previous = sol
        if float(q_mpa) in loads_mpa:
            results[float(q_mpa)] = sol
    return results


def solve_nonshallow_targets(start_time: float, budget_seconds: float) -> dict[float, Any]:
    low_config = AxisymmetricSimpleSupportConfig(
        nd_bvp=600,
        tol=2.0e-4,
        relaxed_tol=1.0e-3,
        max_nodes=240000,
    )
    ensure_budget(start_time, budget_seconds, "low-load non-shallow continuation")
    low_results = solve_axisymmetric_simple_support_continuation(LOW_LOADS_MPA, config=low_config)
    low_points = {float(result.q_mpa): result.solution for result in low_results if result.success and result.solution is not None}
    missing_low = [float(q) for q in LOW_LOADS_MPA if float(q) not in low_points]
    if missing_low:
        raise RuntimeError(f"Low-load non-shallow continuation did not reach: {missing_low}")

    ensure_budget(start_time, budget_seconds, "high-load bootstrap to 4.3433")
    points_by_q, _, local_anchor, older_point, previous_point, _ = pilot12.bootstrap_branch(
        start_time,
        budget_seconds,
    )
    high_points = {float(q): point.solution for q, point in points_by_q.items() if q in HIGH_LOADS_MPA and point.solution is not None}

    if 4.3434 not in high_points:
        ensure_budget(start_time, budget_seconds, "high-load 4.3434 solve")
        point_43434, attempts_43434 = pilot12.try_extension_step(
            pilot12.REPRO_TEST_LOAD_MPA,
            older_point,
            previous_point,
            local_anchor,
            pilot12.PRIMARY_PROFILE,
            start_time,
            budget_seconds,
        )
        if point_43434 is None:
            messages = [item.message for item in attempts_43434]
            raise RuntimeError(f"High-load non-shallow branch did not reach 4.3434 MPa: {messages}")
        high_points[4.3434] = point_43434.solution

    combined = {}
    combined.update(low_points)
    combined.update(high_points)
    missing = [float(q) for q in ALL_LOADS_MPA if float(q) not in combined]
    if missing:
        raise RuntimeError(f"Missing non-shallow solutions at loads: {missing}")
    return combined


def mapped_nonshallow_arrays(sol, x_grid: np.ndarray) -> dict[str, np.ndarray]:
    theta0, theta0p, Phi0p, Phi0 = detcomp.arrays_nepol_sin(sol, x_grid)
    y = sol.sol(x_grid)
    return {
        "theta0": np.asarray(theta0, dtype=float),
        "theta0p": np.asarray(theta0p, dtype=float),
        "Phi0": np.asarray(Phi0, dtype=float),
        "Phi0p": np.asarray(Phi0p, dtype=float),
        "state": np.asarray(y, dtype=float),
    }


def shallow_arrays(sol, x_grid: np.ndarray) -> dict[str, np.ndarray]:
    theta0, theta0p, Phi0p, Phi0 = detcomp.arrays_shallow(sol, x_grid)
    return {
        "theta0": np.asarray(theta0, dtype=float),
        "theta0p": np.asarray(theta0p, dtype=float),
        "Phi0": np.asarray(Phi0, dtype=float),
        "Phi0p": np.asarray(Phi0p, dtype=float),
    }


def segment_metrics(x: np.ndarray, candidate: np.ndarray, reference: np.ndarray, mask: np.ndarray) -> dict[str, float]:
    x_seg = x[mask]
    cand_seg = candidate[mask]
    ref_seg = reference[mask]
    diff = cand_seg - ref_seg

    max_abs_candidate = float(np.max(np.abs(cand_seg)))
    max_abs_reference = float(np.max(np.abs(ref_seg)))
    max_abs_diff = float(np.max(np.abs(diff)))
    scale_max = max(max_abs_candidate, max_abs_reference, 1.0e-12)
    rel_max = max_abs_diff / scale_max

    l2_diff = float(np.sqrt(np.trapezoid(diff**2, x_seg)))
    l2_cand = float(np.sqrt(np.trapezoid(cand_seg**2, x_seg)))
    l2_ref = float(np.sqrt(np.trapezoid(ref_seg**2, x_seg)))
    rel_l2 = l2_diff / max(l2_cand, l2_ref, 1.0e-12)

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


def compare_load(
    q_mpa: float,
    shallow_sol,
    nonshallow_sol,
    x_grid: np.ndarray,
) -> tuple[dict[str, Any], np.ndarray, np.ndarray, np.ndarray]:
    shallow_data = shallow_arrays(shallow_sol, x_grid)
    nonshallow_data = mapped_nonshallow_arrays(nonshallow_sol, x_grid)

    full_mask = np.ones_like(x_grid, dtype=bool)
    center_mask = x_grid <= 0.15
    bulk_mask = x_grid <= 0.95
    edge_mask = x_grid >= 0.95

    per_variable: dict[str, Any] = {}
    overall_bulk_values = []
    overall_edge_values = []
    overall_center_values = []
    first_clear_variables = []
    location_counts = {"center_side": 0, "right_edge": 0, "interior": 0}

    mapped_nonshallow_stack = []
    shallow_stack = []
    for name in COMMON_VARIABLES:
        candidate = nonshallow_data[name]
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
            "x_at_max_abs_diff": peak_x,
            "location_class": loc,
            "full": full,
            "center": center,
            "bulk": bulk,
            "edge": edge,
        }
        overall_bulk_values.append(float(bulk["rel_l2"]))
        overall_edge_values.append(float(edge["rel_l2"]))
        overall_center_values.append(float(center["rel_l2"]))
        if bulk["rel_l2"] >= CLEAR_THRESHOLD:
            first_clear_variables.append(name)
        mapped_nonshallow_stack.append(candidate)
        shallow_stack.append(reference)

    dominant_location = max(location_counts.items(), key=lambda item: item[1])[0]
    result = {
        "q_mpa": float(q_mpa),
        "variables": per_variable,
        "overall": {
            "mean_bulk_rel_l2": float(np.mean(overall_bulk_values)),
            "mean_edge_rel_l2": float(np.mean(overall_edge_values)),
            "mean_center_rel_l2": float(np.mean(overall_center_values)),
            "max_bulk_rel_l2": float(np.max(overall_bulk_values)),
            "first_clear_variables_at_threshold": first_clear_variables,
            "dominant_location_class": dominant_location,
        },
    }
    return (
        result,
        nonshallow_data["state"],
        np.asarray(mapped_nonshallow_stack, dtype=float),
        np.asarray(shallow_stack, dtype=float),
    )


def summarize_sweep(results: list[dict[str, Any]]) -> dict[str, Any]:
    first_clear_load = None
    for item in results:
        overall = item["overall"]
        if overall["mean_bulk_rel_l2"] >= CLEAR_THRESHOLD or len(overall["first_clear_variables_at_threshold"]) >= 2:
            first_clear_load = item["q_mpa"]
            break

    variable_firsts = {}
    for name in COMMON_VARIABLES:
        variable_firsts[name] = next(
            (item["q_mpa"] for item in results if item["variables"][name]["bulk"]["rel_l2"] >= CLEAR_THRESHOLD),
            None,
        )

    loads = np.array([item["q_mpa"] for item in results], dtype=float)
    overall_bulk = np.array([item["overall"]["mean_bulk_rel_l2"] for item in results], dtype=float)
    overall_edge = np.array([item["overall"]["mean_edge_rel_l2"] for item in results], dtype=float)
    if loads.size >= 2 and np.std(overall_bulk) > 0.0:
        bulk_pearson = float(np.corrcoef(loads, overall_bulk)[0, 1])
        edge_pearson = float(np.corrcoef(loads, overall_edge)[0, 1])
    else:
        bulk_pearson = None
        edge_pearson = None

    growth_ratio = float(overall_bulk[-1] / max(overall_bulk[0], 1.0e-12))
    if growth_ratio >= 1.5 and (bulk_pearson is not None and bulk_pearson >= 0.7):
        growth_label = "grows_with_load"
    elif growth_ratio <= 1.2:
        growth_label = "roughly_load_invariant"
    else:
        growth_label = "mild_or_mixed_growth"

    first_localized = None
    if first_clear_load is not None:
        item = next(result for result in results if abs(result["q_mpa"] - first_clear_load) < 1.0e-12)
        first_localized = {
            "q_mpa": first_clear_load,
            "dominant_location_class": item["overall"]["dominant_location_class"],
            "first_clear_variables": item["overall"]["first_clear_variables_at_threshold"],
            "x_at_peaks": {
                name: item["variables"][name]["x_at_max_abs_diff"]
                for name in item["overall"]["first_clear_variables_at_threshold"]
            },
        }

    return {
        "clear_threshold_bulk_rel_l2": CLEAR_THRESHOLD,
        "first_clear_load_mpa": first_clear_load,
        "variable_first_clear_loads_mpa": variable_firsts,
        "overall_bulk_growth_ratio": growth_ratio,
        "overall_bulk_pearson_vs_load": bulk_pearson,
        "overall_edge_pearson_vs_load": edge_pearson,
        "growth_label": growth_label,
        "first_localized_summary": first_localized,
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
    output_json = args.output_json
    cache_npz = args.cache_npz

    payload: dict[str, Any] = {
        "metadata": {
            "pilot": "pilot_13_shallow_nonshallow_divergence_source",
            "loads_mpa": list(ALL_LOADS_MPA),
            "clear_threshold_bulk_rel_l2": CLEAR_THRESHOLD,
            "cache_npz": str(cache_npz),
            "time_budget_seconds": float(args.time_budget_seconds),
        },
        "status": "started",
    }
    save_json(output_json, payload)

    print("=== Pilot 13 load sweep comparison ===")
    print("Solving shallow sweep...")
    shallow_solutions = solve_shallow_targets(ALL_LOADS_MPA)
    payload["status"] = "shallow_solved"
    save_json(output_json, payload)

    print("Solving non-shallow sweep and high-load branch anchor...")
    nonshallow_solutions = solve_nonshallow_targets(start_time, float(args.time_budget_seconds))
    payload["status"] = "nonshallow_solved"
    save_json(output_json, payload)

    x_grid = pilot12.build_comparison_grid(pilot12.PRIMARY_PROFILE.config, n_left=1400, n_right=1000)
    results = []
    nonshallow_states = []
    mapped_nonshallow = []
    shallow_fields = []

    print("Computing mismatch metrics across the load sweep...")
    for q_mpa in ALL_LOADS_MPA:
        result, state_y, mapped_stack, shallow_stack = compare_load(
            float(q_mpa),
            shallow_solutions[float(q_mpa)],
            nonshallow_solutions[float(q_mpa)],
            x_grid,
        )
        results.append(result)
        nonshallow_states.append(state_y)
        mapped_nonshallow.append(mapped_stack)
        shallow_fields.append(shallow_stack)
        payload["results"] = results
        payload["status"] = f"metrics_completed_{float_key(float(q_mpa))}"
        save_json(output_json, payload)

    summary = summarize_sweep(results)
    payload["results"] = results
    payload["summary"] = summary
    payload["status"] = "completed"
    payload["elapsed_seconds"] = elapsed_since(start_time)
    save_json(output_json, payload)

    np.savez_compressed(
        cache_npz,
        loads_mpa=np.asarray(ALL_LOADS_MPA, dtype=float),
        x_grid=np.asarray(x_grid, dtype=float),
        nonshallow_states=np.asarray(nonshallow_states, dtype=float),
        mapped_nonshallow=np.asarray(mapped_nonshallow, dtype=float),
        shallow_fields=np.asarray(shallow_fields, dtype=float),
    )

    print(f"Compared loads: {', '.join(float_key(load) for load in ALL_LOADS_MPA)} MPa")
    print(f"First clear load: {summary['first_clear_load_mpa']}")
    print(f"Growth label: {summary['growth_label']}")
    print(f"Results written to: {output_json}")
    print(f"Cache written to: {cache_npz}")


if __name__ == "__main__":
    main()

