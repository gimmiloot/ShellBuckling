# -*- coding: utf-8 -*-
# Purpose:
#   Run the clean full simple support / podvizhnyi sharnir criterion pilot A+C
#   on the current competition set without changing the main solver path.
# Typical use:
#   .venv\Scripts\python.exe tasks\run_simple_support_criterion_pilot_ac.py
# Outputs:
#   output/clean_full_simple_support/criterion_pilot_ac_*.{json,csv}

from __future__ import annotations

import csv
import json
import time
from pathlib import Path
import sys

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.mixed_weak import axisymmetric_simple_support_background as simple_bg
from shell_buckling.mixed_weak import full_simple_support_critical_search as full_search
from shell_buckling.mixed_weak import simple_support_high_load_background_continuation as high_bg


OUTPUT_DIR = REPO_ROOT / "output" / "clean_full_simple_support"
SUMMARY_JSON = OUTPUT_DIR / "criterion_pilot_ac_summary.json"
SUMMARY_CSV = OUTPUT_DIR / "criterion_pilot_ac_table.csv"
POINTS_CSV = OUTPUT_DIR / "criterion_pilot_ac_points.csv"

MODE_SPECS: dict[int, dict[str, float | int | str]] = {
    4: {"q_min": 10.95, "q_max": 11.25, "npts": 31, "role_hint": "control mode"},
    6: {"q_min": 17.50, "q_max": 17.80, "npts": 41, "role_hint": "leading supported candidate"},
    7: {"q_min": 17.18, "q_max": 17.43, "npts": 41, "role_hint": "reserve mode"},
    8: {"q_min": 17.72, "q_max": 17.97, "npts": 41, "role_hint": "unstable rival"},
}

SETTING_SPECS = (
    {"label": "baseline", "m_basis": 6, "n_collocation": 120, "nd_base": 4000},
    {"label": "medium_fine", "m_basis": 7, "n_collocation": 140, "nd_base": 5000},
    {"label": "finer", "m_basis": 8, "n_collocation": 160, "nd_base": 6000},
)

LOCAL_WIDTH_FACTORS = (2.0, 3.0)
MAX_BOOTSTRAP_STEP_MPA = 0.5
EPS = 1.0e-30


def make_grid(q_min: float, q_max: float, npts: int) -> np.ndarray:
    return np.linspace(float(q_min), float(q_max), int(npts), dtype=float)


def location_label(best_index: int, size: int) -> str:
    return "interior" if 0 < int(best_index) < int(size) - 1 else "boundary"


def contiguous_width(q_grid: np.ndarray, values: np.ndarray, best_index: int, factor: float) -> float:
    threshold = float(factor) * float(values[best_index])
    left = int(best_index)
    right = int(best_index)
    while left > 0 and values[left - 1] <= threshold:
        left -= 1
    while right + 1 < values.size and values[right + 1] <= threshold:
        right += 1
    return float(q_grid[right] - q_grid[left])


def scaled_block(mat: np.ndarray) -> np.ndarray:
    norm = float(np.linalg.norm(mat, ord="fro"))
    return np.asarray(mat, dtype=float) / max(norm, EPS)


def augmented_solvability_sigma(obj: full_search.BoundaryMatrixObjects) -> float:
    g_matrix = np.array(
        [
            [1.0, 0.0],
            [0.0, 1.0],
            [0.0, 0.0],
            [0.0, 0.0],
        ],
        dtype=float,
    )
    a_block = scaled_block(obj.A_int)
    c_block = scaled_block(obj.C_center)
    b_block = scaled_block(full_search.ROW_SCALE[:, None] * obj.B_full)

    augmented = np.block(
        [
            [a_block, np.zeros((a_block.shape[0], 2), dtype=float)],
            [c_block, -scaled_block(g_matrix)],
            [b_block, np.zeros((b_block.shape[0], 2), dtype=float)],
        ]
    )
    return float(np.linalg.svd(augmented, compute_uv=False)[-1])


def summarize_curve(point_rows: list[dict[str, float | str]], value_key: str) -> dict[str, float | str | bool]:
    q_grid = np.array([float(row["q_mpa"]) for row in point_rows], dtype=float)
    values = np.array([float(row[value_key]) for row in point_rows], dtype=float)
    best_index = int(np.argmin(values))
    best_value = float(values[best_index])
    best_q = float(q_grid[best_index])
    location = location_label(best_index, values.size)

    summary: dict[str, float | str | bool] = {
        "best_q_mpa": best_q,
        "best_value": best_value,
        "location": location,
        "median_ratio": float(np.median(values) / max(best_value, EPS)),
        "edge_touched": location == "boundary",
    }

    if location == "interior":
        neighbor_mean = 0.5 * (values[best_index - 1] + values[best_index + 1])
        summary["neighbor_ratio"] = float(neighbor_mean / max(best_value, EPS))
    else:
        summary["neighbor_ratio"] = float("nan")

    for factor in LOCAL_WIDTH_FACTORS:
        summary[f"width_le_{int(factor)}x_mpa"] = contiguous_width(q_grid, values, best_index, factor)

    return summary


def stability_class(
    *,
    all_interior: bool,
    q_drift_mpa: float,
    sigma_ratio: float,
    baseline_width_2x_mpa: float,
) -> str:
    if all_interior and q_drift_mpa <= 0.08 and sigma_ratio <= 4.0 and baseline_width_2x_mpa >= 0.03:
        return "stable"
    if all_interior and q_drift_mpa <= 0.12 and sigma_ratio <= 10.0 and baseline_width_2x_mpa >= 0.015:
        return "moderate"
    return "unstable"


def aggregate_metric_across_settings(setting_rows: list[dict[str, object]], metric_key: str) -> dict[str, object]:
    best_qs = [float(row[f"{metric_key}_best_q_mpa"]) for row in setting_rows]
    best_values = [float(row[f"{metric_key}_best_value"]) for row in setting_rows]
    locations = [str(row[f"{metric_key}_location"]) for row in setting_rows]
    baseline = next(row for row in setting_rows if str(row["setting"]) == "baseline")
    q_drift_mpa = float(max(best_qs) - min(best_qs))
    sigma_ratio = float(max(best_values) / max(min(best_values), EPS))
    all_interior = all(location == "interior" for location in locations)
    baseline_width_2x_mpa = float(baseline[f"{metric_key}_width_le_2x_mpa"])

    return {
        "best_qs_mpa": best_qs,
        "best_values": best_values,
        "locations": locations,
        "all_interior": all_interior,
        "q_drift_mpa": q_drift_mpa,
        "sigma_ratio": sigma_ratio,
        "baseline_width_le_2x_mpa": baseline_width_2x_mpa,
        "baseline_width_le_3x_mpa": float(baseline[f"{metric_key}_width_le_3x_mpa"]),
        "baseline_neighbor_ratio": float(baseline[f"{metric_key}_neighbor_ratio"]),
        "baseline_median_ratio": float(baseline[f"{metric_key}_median_ratio"]),
        "stability_class": stability_class(
            all_interior=all_interior,
            q_drift_mpa=q_drift_mpa,
            sigma_ratio=sigma_ratio,
            baseline_width_2x_mpa=baseline_width_2x_mpa,
        ),
    }


def provisional_branch_status(raw_summary: dict[str, object]) -> str:
    if str(raw_summary["stability_class"]) == "stable":
        return "interior valley survives selected refinement/discretization checks"
    if str(raw_summary["stability_class"]) == "moderate":
        return "interior valley survives only moderately"
    if bool(raw_summary["all_interior"]):
        return "interior but window-sensitive local valley"
    return "boundary-sensitive local minimum"


def provisional_bordered_status(raw_summary: dict[str, object], aug_summary: dict[str, object]) -> str:
    raw_class = str(raw_summary["stability_class"])
    aug_class = str(aug_summary["stability_class"])
    if aug_class == "stable":
        return "augmented solvability minimum is stable on the selected checks"
    if raw_class != "stable" and aug_class in {"stable", "moderate"}:
        return "augmented solvability looks more supportive than the raw boundary-only reading"
    if raw_class == "stable" and aug_class == "unstable":
        return "augmented solvability weakens the raw boundary-only support"
    if aug_class == "moderate":
        return "augmented solvability remains only moderately supportive"
    return "augmented solvability remains unstable / window-sensitive"


def nearest_lower_retained_background(q_target_mpa: float) -> simple_bg.AxisymmetricBackgroundSolve:
    progress = high_bg.load_fast_progress(high_bg.DEFAULT_HISTORY_RUN_DIR)
    if progress is None:
        raise RuntimeError("Missing retained fast progress for the clean high-load background path.")
    start_index = high_bg.nearest_lower_retained_step_index(progress, high_bg.DEFAULT_HISTORY_RUN_DIR, float(q_target_mpa))
    if start_index is None:
        raise RuntimeError(f"Could not find a retained checkpoint below {q_target_mpa:.4f} MPa.")
    point = high_bg.load_retained_point(progress, high_bg.DEFAULT_HISTORY_RUN_DIR, start_index)
    return high_bg.axisymmetric_result_from_point(point, seed_kind=f"retained::{point.accepted_seed}")


def seeded_bootstrap_window(
    q_values_mpa: np.ndarray,
    config: simple_bg.AxisymmetricSimpleSupportConfig,
) -> list[simple_bg.AxisymmetricBackgroundSolve]:
    q_values = [float(q) for q in q_values_mpa]
    start = nearest_lower_retained_background(min(q_values))
    previous = start
    x_mesh = simple_bg.default_x_mesh(config)
    results_by_q: dict[float, simple_bg.AxisymmetricBackgroundSolve] = {}

    for q_target in q_values:
        if q_target <= previous.q_mpa + 1.0e-12:
            results_by_q[round(q_target, 7)] = previous
            continue
        while previous.q_mpa < q_target - 1.0e-12:
            q_trial = min(float(previous.q_mpa + MAX_BOOTSTRAP_STEP_MPA), float(q_target))
            guess = previous.solution.sol(x_mesh)
            trial = simple_bg.solve_axisymmetric_simple_support_fixed_load(
                q_trial,
                config=config,
                initial_guess=guess,
            )
            if not trial.success or trial.solution is None:
                raise RuntimeError(
                    f"Seeded clean bootstrap failed at q={q_trial:.6f} MPa while targeting {q_target:.6f} MPa."
                )
            previous = trial
        results_by_q[round(q_target, 7)] = previous

    return [results_by_q[round(q, 7)] for q in q_values]


def solve_window_backgrounds(
    q_values_mpa: np.ndarray,
    config: simple_bg.AxisymmetricSimpleSupportConfig,
) -> tuple[list[simple_bg.AxisymmetricBackgroundSolve], str]:
    try:
        results = high_bg.solve_axisymmetric_simple_support_high_load_schedule(
            q_values_mpa.tolist(),
            config=config,
            verbose=False,
        )
        if any((not result.success) or (result.solution is None) for result in results):
            raise RuntimeError("Reusable high-load bridge did not converge at all requested local-window points.")
        return results, "clean_high_load_bridge"
    except Exception:
        results = seeded_bootstrap_window(q_values_mpa, config=config)
        return results, "retained_checkpoint_seeded_fixed_load_bootstrap"


def evaluate_setting(
    *,
    mode: int,
    q_grid: np.ndarray,
    backgrounds: list[simple_bg.AxisymmetricBackgroundSolve],
    x0: float,
    setting: dict[str, object],
) -> tuple[list[dict[str, object]], dict[str, object]]:
    point_rows: list[dict[str, object]] = []

    for q_mpa, background in zip(q_grid, backgrounds):
        obj = full_search.build_boundary_matrix_objects(
            n=int(mode),
            background_result=background,
            x0=x0,
            m_basis=int(setting["m_basis"]),
            n_collocation=int(setting["n_collocation"]),
            nd_base=int(setting["nd_base"]),
        )
        sigma_aug = augmented_solvability_sigma(obj)
        point_rows.append(
            {
                "n": int(mode),
                "setting": str(setting["label"]),
                "m_basis": int(setting["m_basis"]),
                "n_collocation": int(setting["n_collocation"]),
                "nd_base": int(setting["nd_base"]),
                "q_mpa": float(q_mpa),
                "sigma_raw": float(obj.sigma_raw),
                "sigma_bal": float(obj.sigma_bal),
                "sigma_bal_noH": float(obj.sigma_bal_noH),
                "sigma_aug": float(sigma_aug),
                "residual_norm_1": float(obj.residual_norms[0]),
                "residual_norm_2": float(obj.residual_norms[1]),
                "background_seed_kind": str(background.seed_kind),
            }
        )

    raw_curve = summarize_curve(point_rows, "sigma_bal")
    aug_curve = summarize_curve(point_rows, "sigma_aug")
    setting_summary = {
        "setting": str(setting["label"]),
        "m_basis": int(setting["m_basis"]),
        "n_collocation": int(setting["n_collocation"]),
        "nd_base": int(setting["nd_base"]),
        "raw_best_q_mpa": float(raw_curve["best_q_mpa"]),
        "raw_best_value": float(raw_curve["best_value"]),
        "raw_location": str(raw_curve["location"]),
        "raw_neighbor_ratio": float(raw_curve["neighbor_ratio"]),
        "raw_median_ratio": float(raw_curve["median_ratio"]),
        "raw_width_le_2x_mpa": float(raw_curve["width_le_2x_mpa"]),
        "raw_width_le_3x_mpa": float(raw_curve["width_le_3x_mpa"]),
        "aug_best_q_mpa": float(aug_curve["best_q_mpa"]),
        "aug_best_value": float(aug_curve["best_value"]),
        "aug_location": str(aug_curve["location"]),
        "aug_neighbor_ratio": float(aug_curve["neighbor_ratio"]),
        "aug_median_ratio": float(aug_curve["median_ratio"]),
        "aug_width_le_2x_mpa": float(aug_curve["width_le_2x_mpa"]),
        "aug_width_le_3x_mpa": float(aug_curve["width_le_3x_mpa"]),
    }
    return point_rows, setting_summary


def main() -> None:
    start_time = time.time()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    background_config = high_bg.default_high_load_background_config()
    x0 = float(background_config.x0)

    summary: dict[str, object] = {
        "method_note": (
            "Criterion pilot A+C for the clean full simple support / podvizhnyi sharnir path. "
            "A = branch-aware local-valley descriptors around the current competition windows. "
            "C = augmented/bordered solvability sigma built from scaled [A_int; C_center - G; B_full] blocks "
            "without changing equations or BC meaning. The main standalone clean solver code path is unchanged. "
            "The local background source first tries the reusable clean high-load bridge and falls back only, if needed, "
            "to the same-equation retained-checkpoint-seeded fixed-load bootstrap helper."
        ),
        "branch_aware_formulas": {
            "median_ratio": "median(local sigma curve) / sigma_min",
            "neighbor_ratio": "0.5*(left+right neighbor sigma) / sigma_min for an interior minimum",
            "width_le_2x_mpa": "contiguous load span around the best point where sigma <= 2*sigma_min",
            "width_le_3x_mpa": "contiguous load span around the best point where sigma <= 3*sigma_min",
            "q_drift_mpa": "max(best_q across selected discretizations) - min(best_q across selected discretizations)",
            "sigma_ratio": "max(best_sigma across selected discretizations) / min(best_sigma across selected discretizations)",
        },
        "bordered_metric_definition": {
            "unknowns": "[full coefficient vector, two regular-family amplitudes]",
            "blocks": "[scaled A_int; scaled (C_center - G); scaled balanced B_full]",
            "diagnostic": "smallest singular value of the augmented matrix",
            "G": [[1.0, 0.0], [0.0, 1.0], [0.0, 0.0], [0.0, 0.0]],
        },
        "background_config": dict(background_config.__dict__),
        "mode_windows": MODE_SPECS,
        "settings": list(SETTING_SPECS),
        "modes": {},
    }

    point_rows_all: list[dict[str, object]] = []
    table_rows: list[dict[str, object]] = []

    for mode, mode_spec in MODE_SPECS.items():
        q_grid = make_grid(float(mode_spec["q_min"]), float(mode_spec["q_max"]), int(mode_spec["npts"]))
        backgrounds, background_method = solve_window_backgrounds(q_grid, config=background_config)

        setting_summaries: list[dict[str, object]] = []
        for setting in SETTING_SPECS:
            point_rows, setting_summary = evaluate_setting(
                mode=int(mode),
                q_grid=q_grid,
                backgrounds=backgrounds,
                x0=x0,
                setting=setting,
            )
            point_rows_all.extend(point_rows)
            setting_summaries.append(setting_summary)

        raw_aggregate = aggregate_metric_across_settings(setting_summaries, "raw")
        aug_aggregate = aggregate_metric_across_settings(setting_summaries, "aug")
        branch_status = provisional_branch_status(raw_aggregate)
        bordered_status = provisional_bordered_status(raw_aggregate, aug_aggregate)

        summary["modes"][str(mode)] = {
            "role_hint": str(mode_spec["role_hint"]),
            "window_q_min_mpa": float(q_grid[0]),
            "window_q_max_mpa": float(q_grid[-1]),
            "n_points": int(q_grid.size),
            "background_method": background_method,
            "setting_summaries": setting_summaries,
            "raw_branch_aware_summary": raw_aggregate,
            "bordered_solvability_summary": aug_aggregate,
            "provisional_branch_aware_status": branch_status,
            "provisional_bordered_status": bordered_status,
        }

        baseline = next(row for row in setting_summaries if str(row["setting"]) == "baseline")
        table_rows.append(
            {
                "n": int(mode),
                "role_hint": str(mode_spec["role_hint"]),
                "raw_q_min_mpa": float(baseline["raw_best_q_mpa"]),
                "raw_sigma_bal": float(baseline["raw_best_value"]),
                "raw_location": str(baseline["raw_location"]),
                "raw_q_drift_mpa": float(raw_aggregate["q_drift_mpa"]),
                "raw_sigma_ratio": float(raw_aggregate["sigma_ratio"]),
                "raw_width_le_2x_mpa": float(raw_aggregate["baseline_width_le_2x_mpa"]),
                "raw_stability_class": str(raw_aggregate["stability_class"]),
                "aug_q_min_mpa": float(baseline["aug_best_q_mpa"]),
                "aug_sigma": float(baseline["aug_best_value"]),
                "aug_location": str(baseline["aug_location"]),
                "aug_q_drift_mpa": float(aug_aggregate["q_drift_mpa"]),
                "aug_sigma_ratio": float(aug_aggregate["sigma_ratio"]),
                "aug_width_le_2x_mpa": float(aug_aggregate["baseline_width_le_2x_mpa"]),
                "aug_stability_class": str(aug_aggregate["stability_class"]),
                "branch_aware_status": branch_status,
                "bordered_solvability_status": bordered_status,
            }
        )

    summary["runtime_seconds"] = float(time.time() - start_time)

    with SUMMARY_JSON.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False, allow_nan=True)
        fh.write("\n")

    csv_columns = [
        "n",
        "role_hint",
        "raw_q_min_mpa",
        "raw_sigma_bal",
        "raw_location",
        "raw_q_drift_mpa",
        "raw_sigma_ratio",
        "raw_width_le_2x_mpa",
        "raw_stability_class",
        "aug_q_min_mpa",
        "aug_sigma",
        "aug_location",
        "aug_q_drift_mpa",
        "aug_sigma_ratio",
        "aug_width_le_2x_mpa",
        "aug_stability_class",
        "branch_aware_status",
        "bordered_solvability_status",
    ]
    with SUMMARY_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(table_rows)

    point_columns = [
        "n",
        "setting",
        "m_basis",
        "n_collocation",
        "nd_base",
        "q_mpa",
        "sigma_raw",
        "sigma_bal",
        "sigma_bal_noH",
        "sigma_aug",
        "residual_norm_1",
        "residual_norm_2",
        "background_seed_kind",
    ]
    with POINTS_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=point_columns)
        writer.writeheader()
        writer.writerows(point_rows_all)

    print("=== Criterion pilot A+C complete ===")
    print(f"summary json: {SUMMARY_JSON}")
    print(f"summary csv:  {SUMMARY_CSV}")
    print(f"points csv:   {POINTS_CSV}")
    print(f"runtime:      {summary['runtime_seconds']:.2f} s")


if __name__ == "__main__":
    main()
