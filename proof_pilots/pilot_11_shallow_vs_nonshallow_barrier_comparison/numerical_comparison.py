from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

import matplotlib
import numpy as np
from scipy.integrate import solve_bvp


matplotlib.use("Agg")
import matplotlib.pyplot as plt


THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[2]
SRC_ROOT = REPO_ROOT / "src"
PILOT_DIR = THIS_FILE.parent
DEFAULT_OUTPUT_JSON = PILOT_DIR / "comparison_results.json"
DEFAULT_PLOT_DIR = PILOT_DIR / "output"

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


pilot10 = load_module(
    "pilot10_continuation_campaign",
    REPO_ROOT / "proof_pilots" / "pilot_10_high_load_simple_support_continuation" / "continuation_campaign.py",
)

from shell_buckling.supporting import determinant_criterion_comparison as detcomp


MATCHED_LOADS_MPA = (4.3400, 4.3430, 4.3433)
FAILED_TARGET_MPA = 4.3434
COMMON_VARIABLES = ("theta0", "theta0p", "Phi0", "Phi0p")
DISPLAY_NAMES = {
    "theta0": "theta0",
    "theta0p": "theta0'",
    "Phi0": "Phi0",
    "Phi0p": "Phi0'",
}


def float_key(value: float) -> str:
    return f"{value:.4f}"


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


def branch_point_summary(point) -> dict[str, Any]:
    return {
        "q_mpa": float(point.q_mpa),
        "nodes": int(point.nodes),
        "max_rms": float(point.max_rms),
        "max_bc_residual": float(point.max_bc_residual),
        "min_r": float(point.min_r),
        "node_pressure": float(point.node_pressure),
        "right_edge_fraction_0_99": float(point.right_edge_fraction_0_99),
        "right_edge_fraction_0_995": float(point.right_edge_fraction_0_995),
        "right_edge_fraction_0_999": float(point.right_edge_fraction_0_999),
        "min_dx": float(point.min_dx),
        "min_dx_mid": float(point.min_dx_mid),
        "top_gradients": serializable(point.top_gradients),
        "observables": serializable(point.observables),
        "accepted_profile": str(point.accepted_profile),
        "accepted_seed": str(point.accepted_seed),
        "predictor_rel_correction": serializable(point.predictor_rel_correction),
        "predictor_abs_correction": serializable(point.predictor_abs_correction),
        "message": str(point.message),
    }


def attempt_summary(attempt) -> dict[str, Any]:
    return {
        "q_mpa": float(attempt.q_mpa),
        "profile_name": str(attempt.profile_name),
        "seed_label": str(attempt.seed_label),
        "success": bool(attempt.success),
        "attempt_seconds": float(attempt.attempt_seconds),
        "message": str(attempt.message),
        "nodes": int(attempt.nodes),
        "max_nodes": int(attempt.max_nodes),
        "max_rms": serializable(attempt.max_rms),
        "max_bc_residual": serializable(attempt.max_bc_residual),
        "min_r": serializable(attempt.min_r),
        "node_pressure": serializable(attempt.node_pressure),
        "right_edge_fraction_0_99": serializable(attempt.right_edge_fraction_0_99),
        "right_edge_fraction_0_995": serializable(attempt.right_edge_fraction_0_995),
        "right_edge_fraction_0_999": serializable(attempt.right_edge_fraction_0_999),
        "min_dx": serializable(attempt.min_dx),
        "min_dx_mid": serializable(attempt.min_dx_mid),
        "top_gradients": serializable(attempt.top_gradients),
        "observables": serializable(attempt.observables),
        "mesh_pressure_only": bool(attempt.mesh_pressure_only),
        "right_edge_layer_suspicion": bool(attempt.right_edge_layer_suspicion),
        "branch_turning_suspicion": bool(attempt.branch_turning_suspicion),
        "predictor_rel_correction": serializable(attempt.predictor_rel_correction),
        "predictor_abs_correction": serializable(attempt.predictor_abs_correction),
    }


def elapsed_since(start_time: float) -> float:
    return time.perf_counter() - start_time


def ensure_budget(start_time: float, budget_seconds: float, stage: str) -> None:
    if elapsed_since(start_time) > budget_seconds:
        raise TimeoutError(f"Time budget exceeded during {stage}.")


def solve_shallow_targets(target_loads_mpa: tuple[float, ...]) -> tuple[dict[float, Any], list[dict[str, Any]]]:
    schedule = sorted(
        {
            0.0,
            0.5,
            1.0,
            1.5,
            2.0,
            3.0,
            4.0,
            4.2,
            4.3,
            *[float(value) for value in target_loads_mpa],
        }
    )

    x_mesh = np.linspace(1.0 / 1500.0, 1.0, 1500)
    y_guess = np.zeros((4, x_mesh.size), dtype=float)
    previous = None
    results: dict[float, Any] = {}
    diagnostics: list[dict[str, Any]] = []

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
        results[float(q_mpa)] = sol
        diagnostics.append(
            {
                "q_mpa": float(q_mpa),
                "success": True,
                "nodes": int(sol.x.size),
                "message": str(sol.message),
                "max_rms": float(np.max(sol.rms_residuals)) if hasattr(sol, "rms_residuals") else None,
            }
        )
    return results, diagnostics


def solve_nonshallow_targets(
    matched_loads_mpa: tuple[float, ...],
    failed_target_mpa: float,
    start_time: float,
    budget_seconds: float,
) -> tuple[dict[float, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    ensure_budget(start_time, budget_seconds, "non-shallow anchor schedule")
    anchor_points = pilot10.solve_anchor_schedule(pilot10.DEFAULT_ANCHOR_LOADS_MPA)
    bootstrap_profile = pilot10.make_profiles("rescue")[0]

    ensure_budget(start_time, budget_seconds, "non-shallow local bootstrap")
    local_points, local_attempts = pilot10.solve_local_bootstrap(
        anchor_points[-1],
        bootstrap_profile,
        pilot10.DEFAULT_LOCAL_BOOTSTRAP_LOADS_MPA,
    )

    points_by_q = {float(point.q_mpa): point for point in anchor_points}
    points_by_q.update({float(point.q_mpa): point for point in local_points})
    all_attempts: list[dict[str, Any]] = [attempt_summary(item) for item in local_attempts]

    anchor_local = local_points[0]
    older = local_points[-2]
    previous = local_points[-1]

    requested_refinement = []
    max_matched = max(float(value) for value in matched_loads_mpa)
    if max_matched > previous.q_mpa + 1.0e-12:
        q_next = previous.q_mpa + 0.0001
        while q_next <= max_matched + 1.0e-12:
            requested_refinement.append(round(q_next, 4))
            q_next += 0.0001

    for q_target in requested_refinement:
        ensure_budget(start_time, budget_seconds, f"non-shallow refinement to {q_target:.4f} MPa")
        point, attempts = pilot10.try_profiles(
            q_target_mpa=q_target,
            older=older,
            previous=previous,
            anchor=anchor_local,
            profiles=[bootstrap_profile],
        )
        all_attempts.extend(attempt_summary(item) for item in attempts)
        if point is None:
            break
        points_by_q[float(point.q_mpa)] = point
        older, previous = previous, point

    ensure_budget(start_time, budget_seconds, f"non-shallow failed-target attempt {failed_target_mpa:.4f} MPa")
    failed_point, failed_attempts = pilot10.try_profiles(
        q_target_mpa=float(failed_target_mpa),
        older=older,
        previous=previous,
        anchor=anchor_local,
        profiles=[bootstrap_profile],
    )
    all_attempts.extend(attempt_summary(item) for item in failed_attempts)
    if failed_point is not None:
        points_by_q[float(failed_point.q_mpa)] = failed_point

    point_summaries = [branch_point_summary(points_by_q[key]) for key in sorted(points_by_q.keys())]
    return points_by_q, point_summaries, all_attempts


def mapped_nonshallow_arrays(sol, x_grid: np.ndarray) -> dict[str, np.ndarray]:
    theta0, theta0p, Phi0p, Phi0 = detcomp.arrays_nepol_sin(sol, x_grid)
    return {
        "theta0": np.asarray(theta0, dtype=float),
        "theta0p": np.asarray(theta0p, dtype=float),
        "Phi0": np.asarray(Phi0, dtype=float),
        "Phi0p": np.asarray(Phi0p, dtype=float),
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

    if x_seg.size >= 2:
        diff_l2 = float(np.sqrt(np.trapezoid(diff**2, x_seg)))
        cand_l2 = float(np.sqrt(np.trapezoid(cand_seg**2, x_seg)))
        ref_l2 = float(np.sqrt(np.trapezoid(ref_seg**2, x_seg)))
    else:
        diff_l2 = float(np.linalg.norm(diff))
        cand_l2 = float(np.linalg.norm(cand_seg))
        ref_l2 = float(np.linalg.norm(ref_seg))
    scale_l2 = max(cand_l2, ref_l2, 1.0e-12)
    rel_l2 = diff_l2 / scale_l2

    return {
        "max_abs_candidate": max_abs_candidate,
        "max_abs_reference": max_abs_reference,
        "max_abs_diff": max_abs_diff,
        "rel_max": rel_max,
        "l2_diff": diff_l2,
        "rel_l2": rel_l2,
    }


def classify_localization(
    x_at_peak: float,
    rel_l2_full: float,
    rel_l2_bulk: float,
    rel_l2_edge: float,
    rel_max_full: float,
) -> str:
    if rel_l2_full < 0.02 and rel_max_full < 0.03:
        return "not_significant"
    if x_at_peak >= 0.97 and rel_l2_edge > 2.0 * max(rel_l2_bulk, 1.0e-12):
        return "right_edge"
    if x_at_peak <= 0.15 and rel_l2_bulk >= 0.8 * rel_l2_edge:
        return "near_center"
    return "global_or_interior"


def summarize_agreement(metrics_by_variable: dict[str, dict[str, Any]]) -> dict[str, Any]:
    good_bulk = 0
    edge_localized = 0
    global_like = 0

    for data in metrics_by_variable.values():
        bulk_rel_l2 = float(data["bulk"]["rel_l2"])
        bulk_rel_max = float(data["bulk"]["rel_max"])
        if bulk_rel_l2 < 0.05 and bulk_rel_max < 0.08:
            good_bulk += 1
        if data["localization"] == "right_edge":
            edge_localized += 1
        if data["localization"] == "global_or_interior" and float(data["full"]["rel_l2"]) >= 0.05:
            global_like += 1

    if good_bulk >= 3 and global_like == 0:
        agreement = "good_bulk_agreement"
    elif global_like >= 2:
        agreement = "global_divergence_visible"
    else:
        agreement = "mixed_or_ambiguous"

    if edge_localized >= 2 and global_like == 0:
        localization = "differences_mainly_localized_near_right_edge"
    elif global_like >= 2:
        localization = "differences_extend_into_the_interior"
    else:
        localization = "localization_ambiguous"

    return {
        "bulk_agreement_label": agreement,
        "localization_label": localization,
        "good_bulk_variable_count": good_bulk,
        "edge_localized_variable_count": edge_localized,
        "global_like_variable_count": global_like,
    }


def compare_case(
    *,
    label: str,
    x_grid: np.ndarray,
    shallow_sol,
    nonshallow_sol,
    shallow_q_mpa: float,
    nonshallow_q_mpa: float,
    precursor_only: bool,
    nonshallow_point_summary: dict[str, Any],
) -> dict[str, Any]:
    shallow_data = shallow_arrays(shallow_sol, x_grid)
    nonshallow_data = mapped_nonshallow_arrays(nonshallow_sol, x_grid)

    full_mask = np.ones_like(x_grid, dtype=bool)
    bulk_mask = x_grid <= 0.95
    edge_mask = x_grid >= 0.95
    tip_mask = x_grid >= 0.99

    metrics_by_variable: dict[str, dict[str, Any]] = {}
    for name in COMMON_VARIABLES:
        candidate = nonshallow_data[name]
        reference = shallow_data[name]
        diff = candidate - reference
        peak_idx = int(np.argmax(np.abs(diff)))
        full = segment_metrics(x_grid, candidate, reference, full_mask)
        bulk = segment_metrics(x_grid, candidate, reference, bulk_mask)
        edge = segment_metrics(x_grid, candidate, reference, edge_mask)
        tip = segment_metrics(x_grid, candidate, reference, tip_mask)
        localization = classify_localization(
            x_at_peak=float(x_grid[peak_idx]),
            rel_l2_full=float(full["rel_l2"]),
            rel_l2_bulk=float(bulk["rel_l2"]),
            rel_l2_edge=float(edge["rel_l2"]),
            rel_max_full=float(full["rel_max"]),
        )
        metrics_by_variable[name] = {
            "x_at_max_abs_diff": float(x_grid[peak_idx]),
            "localization": localization,
            "full": full,
            "bulk": bulk,
            "edge": edge,
            "tip": tip,
        }

    summary = summarize_agreement(metrics_by_variable)
    return {
        "label": label,
        "shallow_q_mpa": float(shallow_q_mpa),
        "nonshallow_q_mpa": float(nonshallow_q_mpa),
        "precursor_only": bool(precursor_only),
        "variables_compared": list(COMMON_VARIABLES),
        "nonshallow_branch_point": nonshallow_point_summary,
        "metrics_by_variable": metrics_by_variable,
        "summary": summary,
    }


def determine_barrier_interpretation(
    cases: list[dict[str, Any]],
    failure_attempts: list[dict[str, Any]],
) -> dict[str, Any]:
    matched_cases = [case for case in cases if not case["precursor_only"]]
    edge_localized = sum(
        case["summary"]["edge_localized_variable_count"] for case in matched_cases
    )
    global_like = sum(
        case["summary"]["global_like_variable_count"] for case in matched_cases
    )
    good_bulk = sum(
        case["summary"]["good_bulk_variable_count"] for case in matched_cases
    )

    mesh_pressure_failures = [
        attempt for attempt in failure_attempts if not attempt["success"] and attempt["mesh_pressure_only"]
    ]
    turning_flags = [
        attempt for attempt in failure_attempts if not attempt["success"] and attempt["branch_turning_suspicion"]
    ]

    if good_bulk >= 7 and global_like == 0 and len(mesh_pressure_failures) == len(failure_attempts):
        emphasis = "numerical_edge_layer_difficulty"
        text = (
            "Across the converged matched loads, the mapped non-shallow and shallow profiles stay close in bulk, "
            "while the non-shallow obstruction still appears as mesh-pressure-dominated failure concentrated near the "
            "right edge. Present evidence therefore points more strongly to a numerical right-edge-layer barrier than "
            "to a demonstrated structural branch end."
        )
    elif global_like >= 3:
        emphasis = "nonshallow_structural_divergence_or_branch_mismatch"
        text = (
            "The comparison shows interior-scale divergence already within the converged range, so the barrier can no "
            "longer be read mainly as a right-edge numerical issue from this evidence alone."
        )
    else:
        emphasis = "unresolved_ambiguity"
        text = (
            "The comparison does not isolate a single interpretation cleanly. Some bulk agreement remains, but the "
            "near-barrier separation is not localized strongly enough to call the obstruction purely numerical."
        )

    return {
        "emphasis": emphasis,
        "matched_case_count": len(matched_cases),
        "good_bulk_variable_total": good_bulk,
        "edge_localized_variable_total": edge_localized,
        "global_like_variable_total": global_like,
        "mesh_pressure_failure_count": len(mesh_pressure_failures),
        "turning_suspicion_count": len(turning_flags),
        "text": text,
    }


def save_case_plots(
    case: dict[str, Any],
    x_grid: np.ndarray,
    shallow_sol,
    nonshallow_sol,
    plot_dir: Path,
) -> list[str]:
    plot_dir.mkdir(parents=True, exist_ok=True)
    shallow_data = shallow_arrays(shallow_sol, x_grid)
    nonshallow_data = mapped_nonshallow_arrays(nonshallow_sol, x_grid)

    saved_paths: list[str] = []
    for suffix, mask, xlim in (
        ("full", np.ones_like(x_grid, dtype=bool), (float(x_grid[0]), 1.0)),
        ("edge", x_grid >= 0.95, (0.95, 1.0)),
    ):
        fig, axes = plt.subplots(2, 2, figsize=(10, 7), constrained_layout=True)
        for ax, name in zip(axes.flat, COMMON_VARIABLES):
            ax.plot(x_grid[mask], shallow_data[name][mask], label="shallow", linewidth=1.5)
            ax.plot(x_grid[mask], nonshallow_data[name][mask], "--", label="mapped non-shallow", linewidth=1.5)
            ax.set_title(DISPLAY_NAMES[name])
            ax.set_xlim(*xlim)
            ax.grid(True, alpha=0.35)
        axes[0, 0].legend(loc="best")
        fig.suptitle(
            f"{case['label']}: shallow {case['shallow_q_mpa']:.4f} MPa vs "
            f"non-shallow {case['nonshallow_q_mpa']:.4f} MPa"
        )
        plot_path = plot_dir / f"{case['label']}_{suffix}.png"
        fig.savefig(plot_path, dpi=150)
        plt.close(fig)
        saved_paths.append(str(plot_path))
    return saved_paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--plot-dir", type=Path, default=DEFAULT_PLOT_DIR)
    parser.add_argument("--n-compare", type=int, default=4000)
    parser.add_argument("--time-budget-seconds", type=float, default=1800.0)
    parser.add_argument("--no-plots", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    start_time = time.perf_counter()

    payload: dict[str, Any] = {
        "metadata": {
            "pilot": "pilot_11_shallow_vs_nonshallow_barrier_comparison",
            "matched_loads_mpa": list(MATCHED_LOADS_MPA),
            "failed_target_mpa": FAILED_TARGET_MPA,
            "n_compare": int(args.n_compare),
            "time_budget_seconds": float(args.time_budget_seconds),
        },
        "status": "started",
    }
    save_json(args.output_json, payload)

    x_grid = np.linspace(1.0 / float(args.n_compare), 1.0, int(args.n_compare))
    target_shallow_loads = tuple(sorted({*MATCHED_LOADS_MPA, FAILED_TARGET_MPA}))

    print("=== Pilot 11 barrier comparison ===")
    print("Solving the repository shallow comparison path...")
    shallow_solutions, shallow_diagnostics = solve_shallow_targets(target_shallow_loads)
    payload["shallow"] = {
        "diagnostics": shallow_diagnostics,
        "loads_solved_mpa": [float(item["q_mpa"]) for item in shallow_diagnostics],
    }
    payload["status"] = "shallow_solved"
    save_json(args.output_json, payload)

    print("Solving the non-shallow pilot-10 branch bootstrap and near-barrier refinement...")
    points_by_q, point_summaries, all_attempts = solve_nonshallow_targets(
        MATCHED_LOADS_MPA,
        FAILED_TARGET_MPA,
        start_time=start_time,
        budget_seconds=float(args.time_budget_seconds),
    )
    payload["nonshallow"] = {
        "point_summaries": point_summaries,
        "attempts": all_attempts,
        "loads_available_mpa": sorted(float(key) for key in points_by_q.keys()),
    }
    payload["status"] = "nonshallow_solved"
    save_json(args.output_json, payload)

    required_nonshallow = [float(load) for load in MATCHED_LOADS_MPA if float(load) not in points_by_q]
    if required_nonshallow:
        raise RuntimeError(f"Missing required non-shallow loads: {required_nonshallow}")

    comparison_cases: list[dict[str, Any]] = []
    for q_mpa in MATCHED_LOADS_MPA:
        shallow_sol = shallow_solutions[float(q_mpa)]
        point = points_by_q[float(q_mpa)]
        case = compare_case(
            label=f"matched_{float_key(q_mpa)}_mpa",
            x_grid=x_grid,
            shallow_sol=shallow_sol,
            nonshallow_sol=point.solution,
            shallow_q_mpa=float(q_mpa),
            nonshallow_q_mpa=float(q_mpa),
            precursor_only=False,
            nonshallow_point_summary=branch_point_summary(point),
        )
        comparison_cases.append(case)

    precursor_q_mpa = max(q for q in points_by_q.keys() if q <= FAILED_TARGET_MPA)
    precursor_point = points_by_q[precursor_q_mpa]
    precursor_only = precursor_q_mpa < FAILED_TARGET_MPA - 1.0e-12
    precursor_label = (
        f"failed_target_precursor_{float_key(FAILED_TARGET_MPA)}_mpa"
        if precursor_only
        else f"matched_barrier_probe_{float_key(FAILED_TARGET_MPA)}_mpa"
    )
    precursor_case = compare_case(
        label=precursor_label,
        x_grid=x_grid,
        shallow_sol=shallow_solutions[FAILED_TARGET_MPA],
        nonshallow_sol=precursor_point.solution,
        shallow_q_mpa=FAILED_TARGET_MPA,
        nonshallow_q_mpa=float(precursor_q_mpa),
        precursor_only=precursor_only,
        nonshallow_point_summary=branch_point_summary(precursor_point),
    )
    comparison_cases.append(precursor_case)

    failure_attempts = [attempt for attempt in all_attempts if abs(attempt["q_mpa"] - FAILED_TARGET_MPA) < 5.0e-5]
    barrier_interpretation = determine_barrier_interpretation(comparison_cases, failure_attempts)
    payload["comparison_cases"] = comparison_cases
    payload["overall_barrier_interpretation"] = barrier_interpretation

    if args.no_plots:
        payload["plots"] = []
    else:
        plot_paths: list[str] = []
        for case in comparison_cases:
            if not case["precursor_only"] or case["label"].endswith("4.3434_mpa"):
                shallow_sol = shallow_solutions[float(case["shallow_q_mpa"])]
                point_q = float(case["nonshallow_q_mpa"])
                plot_paths.extend(
                    save_case_plots(
                        case,
                        x_grid,
                        shallow_sol=shallow_sol,
                        nonshallow_sol=points_by_q[point_q].solution,
                        plot_dir=args.plot_dir,
                    )
                )
        payload["plots"] = plot_paths

    payload["status"] = "completed"
    payload["elapsed_seconds"] = elapsed_since(start_time)
    save_json(args.output_json, payload)

    print(f"Matched loads compared: {', '.join(float_key(load) for load in MATCHED_LOADS_MPA)} MPa")
    if precursor_only:
        print(
            "Failed-target precursor comparison: "
            f"shallow {FAILED_TARGET_MPA:.4f} MPa vs non-shallow precursor {precursor_q_mpa:.4f} MPa"
        )
    else:
        print(
            "Barrier-adjacent matched comparison: "
            f"shallow {FAILED_TARGET_MPA:.4f} MPa vs non-shallow {precursor_q_mpa:.4f} MPa"
        )
    print(f"Barrier interpretation: {barrier_interpretation['emphasis']}")
    print(f"Results written to: {args.output_json}")


if __name__ == "__main__":
    main()




