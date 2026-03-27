# -*- coding: utf-8 -*-
# Purpose:
#   Run the clean full simple support / podvizhnyi sharnir criterion pilot D
#   on the current competition set without changing the main solver path.
# Typical use:
#   .venv\Scripts\python.exe tasks\run_simple_support_criterion_pilot_d.py
# Outputs:
#   output/clean_full_simple_support/criterion_pilot_d_*.{json,csv}

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
SUMMARY_JSON = OUTPUT_DIR / "criterion_pilot_d_summary.json"
SUMMARY_CSV = OUTPUT_DIR / "criterion_pilot_d_table.csv"
POINTS_CSV = OUTPUT_DIR / "criterion_pilot_d_points.csv"

MODE_SPECS: dict[int, dict[str, object]] = {
    4: {
        "role_hint": "control mode",
        "windows": {
            "broad_local": {"q_min": 10.8, "q_max": 11.4, "npts": 61},
            "focused_local": {"q_min": 10.95, "q_max": 11.25, "npts": 31},
        },
    },
    6: {
        "role_hint": "leading supported candidate",
        "windows": {
            "broad_local": {"q_min": 17.4, "q_max": 18.0, "npts": 81},
            "focused_local": {"q_min": 17.50, "q_max": 17.80, "npts": 41},
        },
    },
    7: {
        "role_hint": "raw unsupported reserve dip",
        "windows": {
            "broad_local": {"q_min": 17.1, "q_max": 17.5, "npts": 65},
            "focused_local": {"q_min": 17.18, "q_max": 17.43, "npts": 41},
        },
    },
    8: {
        "role_hint": "main rival",
        "windows": {
            "broad_local": {"q_min": 17.6, "q_max": 18.0, "npts": 65},
            "focused_local": {"q_min": 17.72, "q_max": 17.97, "npts": 41},
        },
    },
}

SETTING_SPECS = (
    {"label": "baseline", "m_basis": 6, "n_collocation": 120, "nd_base": 4000},
    {"label": "medium_fine", "m_basis": 7, "n_collocation": 140, "nd_base": 5000},
    {"label": "finer", "m_basis": 8, "n_collocation": 160, "nd_base": 6000},
)

FOCUSED_REFINEMENT_MODES = {6, 8}
D_BUNDLE_RADIUS = 1
MAX_BOOTSTRAP_STEP_MPA = 0.5
EPS = 1.0e-30


def make_grid(q_min: float, q_max: float, npts: int) -> np.ndarray:
    return np.linspace(float(q_min), float(q_max), int(npts), dtype=float)


def location_label(best_index: int, size: int) -> str:
    return "interior" if 0 < int(best_index) < int(size) - 1 else "boundary"


def scaled_block(mat: np.ndarray) -> np.ndarray:
    norm = float(np.linalg.norm(mat, ord="fro"))
    return np.asarray(mat, dtype=float) / max(norm, EPS)


def orthonormal_bundle_basis(columns: list[np.ndarray]) -> np.ndarray:
    stacked = np.hstack(columns)
    q, r = np.linalg.qr(stacked)
    keep = [idx for idx in range(min(r.shape)) if abs(r[idx, idx]) > 1.0e-10]
    if not keep:
        return q[:, :1]
    return q[:, keep]


def d_reading_class(boundary_share: float) -> str:
    if float(boundary_share) <= 0.05:
        return "interior-dominated"
    if float(boundary_share) <= 0.50:
        return "mixed interior/boundary"
    return "boundary-dominated"


def stability_class(
    *,
    all_interior: bool,
    q_drift_mpa: float,
    value_ratio: float,
) -> str:
    if all_interior and q_drift_mpa <= 0.08 and value_ratio <= 4.0:
        return "stable"
    if all_interior and q_drift_mpa <= 0.18 and value_ratio <= 12.0:
        return "moderate"
    return "unstable"


def aggregate_reading_class(classes: list[str]) -> str:
    if all(item == "interior-dominated" for item in classes):
        return "interior-dominated"
    if all(item == "boundary-dominated" for item in classes):
        return "boundary-dominated"
    return "mixed"


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


def tangent_bundle_metric(
    current_obj: full_search.BoundaryMatrixObjects,
    bundle_objects: list[full_search.BoundaryMatrixObjects],
) -> dict[str, float | int | str]:
    bundle_basis = orthonormal_bundle_basis([obj.V_reg for obj in bundle_objects])
    a_block = scaled_block(current_obj.A_int)
    b_block = scaled_block(full_search.ROW_SCALE[:, None] * current_obj.B_full)

    operator = np.vstack([a_block @ bundle_basis, b_block @ bundle_basis])
    _u, singvals, vh = np.linalg.svd(operator, full_matrices=False)
    coeff = vh[-1]
    direction = bundle_basis @ coeff

    interior_norm = float(np.linalg.norm(a_block @ direction))
    boundary_norm = float(np.linalg.norm(b_block @ direction))
    total_sq = interior_norm * interior_norm + boundary_norm * boundary_norm
    boundary_share = float((boundary_norm * boundary_norm) / max(total_sq, EPS))

    return {
        "d_sigma": float(singvals[-1]),
        "d_interior_norm": interior_norm,
        "d_boundary_norm": boundary_norm,
        "d_boundary_share": boundary_share,
        "d_reading_class": d_reading_class(boundary_share),
        "d_bundle_rank": int(bundle_basis.shape[1]),
    }


def summarize_curve(point_rows: list[dict[str, object]], value_key: str) -> dict[str, object]:
    q_grid = np.array([float(row["q_mpa"]) for row in point_rows], dtype=float)
    values = np.array([float(row[value_key]) for row in point_rows], dtype=float)
    best_index = int(np.argmin(values))
    best_row = point_rows[best_index]

    summary: dict[str, object] = {
        "best_q_mpa": float(q_grid[best_index]),
        "best_value": float(values[best_index]),
        "location": location_label(best_index, values.size),
    }

    if value_key == "d_sigma":
        summary["boundary_share"] = float(best_row["d_boundary_share"])
        summary["reading_class"] = str(best_row["d_reading_class"])
        summary["bundle_rank"] = int(best_row["d_bundle_rank"])
        summary["interior_norm"] = float(best_row["d_interior_norm"])
        summary["boundary_norm"] = float(best_row["d_boundary_norm"])

    return summary


def aggregate_metric(summaries: list[dict[str, object]], metric_key: str) -> dict[str, object]:
    best_qs = [float(row[f"{metric_key}_best_q_mpa"]) for row in summaries]
    best_values = [float(row[f"{metric_key}_best_value"]) for row in summaries]
    locations = [str(row[f"{metric_key}_location"]) for row in summaries]
    q_drift_mpa = float(max(best_qs) - min(best_qs))
    value_ratio = float(max(best_values) / max(min(best_values), EPS))
    all_interior = all(location == "interior" for location in locations)

    aggregate: dict[str, object] = {
        "best_qs_mpa": best_qs,
        "best_values": best_values,
        "locations": locations,
        "all_interior": all_interior,
        "q_drift_mpa": q_drift_mpa,
        "value_ratio": value_ratio,
        "stability_class": stability_class(
            all_interior=all_interior,
            q_drift_mpa=q_drift_mpa,
            value_ratio=value_ratio,
        ),
    }

    if metric_key == "d":
        boundary_shares = [float(row["d_boundary_share"]) for row in summaries]
        reading_classes = [str(row["d_reading_class"]) for row in summaries]
        aggregate["boundary_shares"] = boundary_shares
        aggregate["reading_classes"] = reading_classes
        aggregate["reading_class"] = aggregate_reading_class(reading_classes)

    return aggregate


def window_status(raw_summary: dict[str, object], d_summary: dict[str, object]) -> str:
    if str(d_summary["reading_class"]) == "interior-dominated" and str(d_summary["stability_class"]) in {"stable", "moderate"}:
        return "interior tangent-like signal survives the selected local-window check"
    if str(d_summary["reading_class"]) == "interior-dominated":
        return "interior tangent-like signal appears, but it remains sensitivity-limited"
    if str(raw_summary["stability_class"]) == "unstable" and str(d_summary["reading_class"]) != "boundary-dominated":
        return "D is less boundary-led than the raw reading, but not yet stable"
    return "D remains too close to a boundary-led local reading"


def refinement_status(refinement_summary: dict[str, object] | None) -> str:
    if refinement_summary is None:
        return "not requested"
    if str(refinement_summary["stability_class"]) in {"stable", "moderate"}:
        return "selected refinement check is supportive"
    return "selected refinement check remains sensitivity-limited"


def evaluate_setting(
    *,
    mode: int,
    window_label: str,
    role_hint: str,
    q_grid: np.ndarray,
    backgrounds: list[simple_bg.AxisymmetricBackgroundSolve],
    x0: float,
    setting: dict[str, object],
) -> tuple[list[dict[str, object]], dict[str, object]]:
    objects = [
        full_search.build_boundary_matrix_objects(
            n=int(mode),
            background_result=background,
            x0=x0,
            m_basis=int(setting["m_basis"]),
            n_collocation=int(setting["n_collocation"]),
            nd_base=int(setting["nd_base"]),
        )
        for background in backgrounds
    ]

    point_rows: list[dict[str, object]] = []
    for idx, (q_mpa, background, obj) in enumerate(zip(q_grid, backgrounds, objects)):
        bundle_indices = range(max(0, idx - D_BUNDLE_RADIUS), min(len(objects), idx + D_BUNDLE_RADIUS + 1))
        bundle_metric = tangent_bundle_metric(obj, [objects[j] for j in bundle_indices])
        point_rows.append(
            {
                "n": int(mode),
                "role_hint": str(role_hint),
                "window": str(window_label),
                "setting": str(setting["label"]),
                "m_basis": int(setting["m_basis"]),
                "n_collocation": int(setting["n_collocation"]),
                "nd_base": int(setting["nd_base"]),
                "q_mpa": float(q_mpa),
                "sigma_raw": float(obj.sigma_raw),
                "sigma_bal": float(obj.sigma_bal),
                "sigma_bal_noH": float(obj.sigma_bal_noH),
                "d_sigma": float(bundle_metric["d_sigma"]),
                "d_interior_norm": float(bundle_metric["d_interior_norm"]),
                "d_boundary_norm": float(bundle_metric["d_boundary_norm"]),
                "d_boundary_share": float(bundle_metric["d_boundary_share"]),
                "d_reading_class": str(bundle_metric["d_reading_class"]),
                "d_bundle_rank": int(bundle_metric["d_bundle_rank"]),
                "residual_norm_1": float(obj.residual_norms[0]),
                "residual_norm_2": float(obj.residual_norms[1]),
                "background_seed_kind": str(background.seed_kind),
            }
        )

    raw_curve = summarize_curve(point_rows, "sigma_bal")
    d_curve = summarize_curve(point_rows, "d_sigma")
    setting_summary = {
        "setting": str(setting["label"]),
        "window": str(window_label),
        "m_basis": int(setting["m_basis"]),
        "n_collocation": int(setting["n_collocation"]),
        "nd_base": int(setting["nd_base"]),
        "raw_best_q_mpa": float(raw_curve["best_q_mpa"]),
        "raw_best_value": float(raw_curve["best_value"]),
        "raw_location": str(raw_curve["location"]),
        "d_best_q_mpa": float(d_curve["best_q_mpa"]),
        "d_best_value": float(d_curve["best_value"]),
        "d_location": str(d_curve["location"]),
        "d_boundary_share": float(d_curve["boundary_share"]),
        "d_reading_class": str(d_curve["reading_class"]),
        "d_bundle_rank": int(d_curve["bundle_rank"]),
        "d_interior_norm": float(d_curve["interior_norm"]),
        "d_boundary_norm": float(d_curve["boundary_norm"]),
    }
    return point_rows, setting_summary


def main() -> None:
    start_time = time.time()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    background_config = high_bg.default_high_load_background_config()
    x0 = float(background_config.x0)

    summary: dict[str, object] = {
        "method_note": (
            "Criterion pilot D for the clean full simple support / podvizhnyi sharnir path. "
            "The main standalone clean solver code path is unchanged. "
            "The raw reference is the current balanced boundary-only metric sigma_bal from B_mix. "
            "The D diagnostic is the smallest singular value of the scaled current-operator "
            "[A_int(q); B_bal(q)] restricted to the local three-load tangent-bundle subspace "
            "span(V_reg(q-Delta), V_reg(q), V_reg(q+Delta)), where V_reg is the current two-mode "
            "center-regular family used by the clean solver. This keeps the clean equations and BC meaning unchanged, "
            "stays on the clean full simple-support architecture, and moves the reading closer to a local tangent/operator "
            "interpretation than the boundary-only B_mix minimum."
        ),
        "d_object_definition": {
            "bundle_radius_in_load_steps": D_BUNDLE_RADIUS,
            "operator_blocks": "[scaled A_int(q); scaled balanced B_full(q)]",
            "subspace": "span of neighboring current regular-family bases V_reg",
            "diagnostic": "smallest singular value of the restricted local tangent-bundle operator",
        },
        "background_config": dict(background_config.__dict__),
        "mode_windows": MODE_SPECS,
        "settings": list(SETTING_SPECS),
        "modes": {},
    }

    point_rows_all: list[dict[str, object]] = []
    table_rows: list[dict[str, object]] = []

    for mode, mode_spec in MODE_SPECS.items():
        role_hint = str(mode_spec["role_hint"])
        mode_summary: dict[str, object] = {
            "role_hint": role_hint,
            "windows": {},
        }

        baseline_window_summaries: list[dict[str, object]] = []
        focused_refinement_summaries: list[dict[str, object]] = []

        for window_label, window_spec in dict(mode_spec["windows"]).items():
            q_grid = make_grid(
                float(window_spec["q_min"]),
                float(window_spec["q_max"]),
                int(window_spec["npts"]),
            )
            backgrounds, background_method = solve_window_backgrounds(q_grid, config=background_config)

            if int(mode) in FOCUSED_REFINEMENT_MODES and window_label == "focused_local":
                settings_to_run = SETTING_SPECS
            else:
                settings_to_run = (SETTING_SPECS[0],)

            setting_summaries: list[dict[str, object]] = []
            for setting in settings_to_run:
                point_rows, setting_summary = evaluate_setting(
                    mode=int(mode),
                    window_label=str(window_label),
                    role_hint=role_hint,
                    q_grid=q_grid,
                    backgrounds=backgrounds,
                    x0=x0,
                    setting=setting,
                )
                point_rows_all.extend(point_rows)
                setting_summaries.append(setting_summary)

            baseline_summary = next(row for row in setting_summaries if str(row["setting"]) == "baseline")
            baseline_window_summaries.append(baseline_summary)
            if int(mode) in FOCUSED_REFINEMENT_MODES and window_label == "focused_local":
                focused_refinement_summaries.extend(setting_summaries)

            mode_summary["windows"][str(window_label)] = {
                "window_q_min_mpa": float(q_grid[0]),
                "window_q_max_mpa": float(q_grid[-1]),
                "n_points": int(q_grid.size),
                "background_method": background_method,
                "setting_summaries": setting_summaries,
            }

        raw_window_aggregate = aggregate_metric(baseline_window_summaries, "raw")
        d_window_aggregate = aggregate_metric(baseline_window_summaries, "d")
        mode_summary["raw_window_summary"] = raw_window_aggregate
        mode_summary["d_window_summary"] = d_window_aggregate
        mode_summary["window_status"] = window_status(raw_window_aggregate, d_window_aggregate)

        refinement_summary = None
        if int(mode) in FOCUSED_REFINEMENT_MODES:
            refinement_summary = aggregate_metric(focused_refinement_summaries, "d")
            mode_summary["focused_refinement_d_summary"] = refinement_summary
            mode_summary["focused_refinement_status"] = refinement_status(refinement_summary)

        summary["modes"][str(mode)] = mode_summary

        broad_summary = mode_summary["windows"]["broad_local"]["setting_summaries"][0]
        focused_summary = mode_summary["windows"]["focused_local"]["setting_summaries"][0]
        table_rows.append(
            {
                "n": int(mode),
                "role_hint": role_hint,
                "broad_window_mpa": f"{MODE_SPECS[int(mode)]['windows']['broad_local']['q_min']}..{MODE_SPECS[int(mode)]['windows']['broad_local']['q_max']}",
                "focused_window_mpa": f"{MODE_SPECS[int(mode)]['windows']['focused_local']['q_min']}..{MODE_SPECS[int(mode)]['windows']['focused_local']['q_max']}",
                "raw_broad_best_q_mpa": float(broad_summary["raw_best_q_mpa"]),
                "raw_broad_best_value": float(broad_summary["raw_best_value"]),
                "raw_broad_location": str(broad_summary["raw_location"]),
                "d_broad_best_q_mpa": float(broad_summary["d_best_q_mpa"]),
                "d_broad_best_value": float(broad_summary["d_best_value"]),
                "d_broad_location": str(broad_summary["d_location"]),
                "d_broad_reading_class": str(broad_summary["d_reading_class"]),
                "d_broad_boundary_share": float(broad_summary["d_boundary_share"]),
                "raw_focused_best_q_mpa": float(focused_summary["raw_best_q_mpa"]),
                "raw_focused_best_value": float(focused_summary["raw_best_value"]),
                "raw_focused_location": str(focused_summary["raw_location"]),
                "d_focused_best_q_mpa": float(focused_summary["d_best_q_mpa"]),
                "d_focused_best_value": float(focused_summary["d_best_value"]),
                "d_focused_location": str(focused_summary["d_location"]),
                "d_focused_reading_class": str(focused_summary["d_reading_class"]),
                "d_focused_boundary_share": float(focused_summary["d_boundary_share"]),
                "raw_window_q_drift_mpa": float(raw_window_aggregate["q_drift_mpa"]),
                "raw_window_value_ratio": float(raw_window_aggregate["value_ratio"]),
                "raw_window_stability": str(raw_window_aggregate["stability_class"]),
                "d_window_q_drift_mpa": float(d_window_aggregate["q_drift_mpa"]),
                "d_window_value_ratio": float(d_window_aggregate["value_ratio"]),
                "d_window_stability": str(d_window_aggregate["stability_class"]),
                "d_window_reading_class": str(d_window_aggregate["reading_class"]),
                "window_status": str(mode_summary["window_status"]),
                "focused_refinement_q_drift_mpa": float(refinement_summary["q_drift_mpa"]) if refinement_summary else float("nan"),
                "focused_refinement_value_ratio": float(refinement_summary["value_ratio"]) if refinement_summary else float("nan"),
                "focused_refinement_stability": str(refinement_summary["stability_class"]) if refinement_summary else "not_requested",
                "focused_refinement_status": str(mode_summary.get("focused_refinement_status", "not requested")),
            }
        )

    focused_baseline_rows = sorted(table_rows, key=lambda row: float(row["d_focused_best_value"]))
    summary["focused_baseline_d_ranking"] = [
        {
            "n": int(row["n"]),
            "role_hint": str(row["role_hint"]),
            "d_focused_best_q_mpa": float(row["d_focused_best_q_mpa"]),
            "d_focused_best_value": float(row["d_focused_best_value"]),
        }
        for row in focused_baseline_rows
    ]
    summary["runtime_seconds"] = float(time.time() - start_time)

    with SUMMARY_JSON.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False, allow_nan=True)
        fh.write("\n")

    csv_columns = [
        "n",
        "role_hint",
        "broad_window_mpa",
        "focused_window_mpa",
        "raw_broad_best_q_mpa",
        "raw_broad_best_value",
        "raw_broad_location",
        "d_broad_best_q_mpa",
        "d_broad_best_value",
        "d_broad_location",
        "d_broad_reading_class",
        "d_broad_boundary_share",
        "raw_focused_best_q_mpa",
        "raw_focused_best_value",
        "raw_focused_location",
        "d_focused_best_q_mpa",
        "d_focused_best_value",
        "d_focused_location",
        "d_focused_reading_class",
        "d_focused_boundary_share",
        "raw_window_q_drift_mpa",
        "raw_window_value_ratio",
        "raw_window_stability",
        "d_window_q_drift_mpa",
        "d_window_value_ratio",
        "d_window_stability",
        "d_window_reading_class",
        "window_status",
        "focused_refinement_q_drift_mpa",
        "focused_refinement_value_ratio",
        "focused_refinement_stability",
        "focused_refinement_status",
    ]
    with SUMMARY_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(table_rows)

    point_columns = [
        "n",
        "role_hint",
        "window",
        "setting",
        "m_basis",
        "n_collocation",
        "nd_base",
        "q_mpa",
        "sigma_raw",
        "sigma_bal",
        "sigma_bal_noH",
        "d_sigma",
        "d_interior_norm",
        "d_boundary_norm",
        "d_boundary_share",
        "d_reading_class",
        "d_bundle_rank",
        "residual_norm_1",
        "residual_norm_2",
        "background_seed_kind",
    ]
    with POINTS_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=point_columns)
        writer.writeheader()
        writer.writerows(point_rows_all)

    print("=== Criterion pilot D complete ===")
    print(f"summary json: {SUMMARY_JSON}")
    print(f"summary csv:  {SUMMARY_CSV}")
    print(f"points csv:   {POINTS_CSV}")
    print(f"runtime:      {summary['runtime_seconds']:.2f} s")


if __name__ == "__main__":
    main()
