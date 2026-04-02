# -*- coding: utf-8 -*-
# Purpose:
#   Run a focused pairwise gap study for the near-degenerate n=7 / n=8 R2
#   reading on the clean full simple-support path without changing the main
#   solver path.
# Typical use:
#   .venv\Scripts\python.exe tasks\run_simple_support_criterion_pilot_r2_pair_gap.py
# Outputs:
#   output/clean_full_simple_support/criterion_pilot_r2_pair_gap_summary.json
#   output/clean_full_simple_support/criterion_pilot_r2_pair_gap_table.csv
#   output/clean_full_simple_support/criterion_pilot_r2_pair_gap_curves.csv

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
SUMMARY_JSON = OUTPUT_DIR / "criterion_pilot_r2_pair_gap_summary.json"
SUMMARY_CSV = OUTPUT_DIR / "criterion_pilot_r2_pair_gap_table.csv"
CURVES_CSV = OUTPUT_DIR / "criterion_pilot_r2_pair_gap_curves.csv"

PAIR_MODES = (7, 8)
COMMON_WINDOW = {"q_min": 17.20, "q_max": 17.70, "npts": 201}
LOCAL_WINDOWS: dict[int, dict[str, float]] = {
    7: {"q_min": 17.20, "q_max": 17.50},
    8: {"q_min": 17.35, "q_max": 17.70},
}

SETTING_SPECS: tuple[dict[str, object], ...] = (
    {"label": "baseline", "m_basis": 6, "n_collocation": 120, "nd_base": 4000},
    {"label": "basis_down", "m_basis": 5, "n_collocation": 120, "nd_base": 4000},
    {"label": "basis_up", "m_basis": 7, "n_collocation": 120, "nd_base": 4000},
    {"label": "collocation_down", "m_basis": 6, "n_collocation": 100, "nd_base": 4000},
    {"label": "collocation_up", "m_basis": 6, "n_collocation": 140, "nd_base": 4000},
    {"label": "paired_fine", "m_basis": 7, "n_collocation": 140, "nd_base": 4000},
)

MAX_BOOTSTRAP_STEP_MPA = 0.5
EPS = 1.0e-30


def make_grid(q_min: float, q_max: float, npts: int) -> np.ndarray:
    return np.linspace(float(q_min), float(q_max), int(npts), dtype=float)


def condition_number(A: np.ndarray) -> float:
    singular_values = np.linalg.svd(np.asarray(A, dtype=float), compute_uv=False)
    if singular_values.size == 0:
        return float("nan")
    if singular_values[-1] <= EPS:
        return float("inf")
    return float(singular_values[0] / singular_values[-1])


def value_summary(values: list[float]) -> dict[str, float]:
    arr = np.asarray(values, dtype=float)
    finite = arr[np.isfinite(arr)]
    if finite.size == 0:
        return {"min": float("nan"), "median": float("nan"), "max": float("nan"), "spread": float("nan")}
    return {
        "min": float(np.min(finite)),
        "median": float(np.median(finite)),
        "max": float(np.max(finite)),
        "spread": float(np.max(finite) - np.min(finite)),
    }


def nearest_lower_retained_background(q_target_mpa: float) -> simple_bg.AxisymmetricBackgroundSolve:
    progress = high_bg.load_fast_progress(high_bg.DEFAULT_HISTORY_RUN_DIR)
    if progress is None:
        raise RuntimeError("Missing retained fast progress for the clean high-load background path.")
    start_index = high_bg.nearest_lower_retained_step_index(
        progress,
        high_bg.DEFAULT_HISTORY_RUN_DIR,
        float(q_target_mpa),
    )
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


def build_mode_rows(
    *,
    mode: int,
    setting: dict[str, object],
    q_grid: np.ndarray,
    backgrounds: list[simple_bg.AxisymmetricBackgroundSolve],
    x0: float,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for q_mpa, background in zip(q_grid, backgrounds):
        obj = full_search.build_boundary_matrix_objects(
            n=int(mode),
            background_result=background,
            x0=x0,
            m_basis=int(setting["m_basis"]),
            n_collocation=int(setting["n_collocation"]),
            nd_base=int(setting["nd_base"]),
        )
        rows.append(
            {
                "n": int(mode),
                "setting": str(setting["label"]),
                "m_basis": int(setting["m_basis"]),
                "n_collocation": int(setting["n_collocation"]),
                "nd_base": int(setting["nd_base"]),
                "q_mpa": float(q_mpa),
                "rho_R2": float(obj.rho_R2),
                "rho_R2_raw": float(obj.rho_R2_raw),
                "cond_G_amp": condition_number(obj.G_amp),
                "sigma_bal": float(obj.sigma_bal),
                "sigma_Bred_bal": float(obj.sigma_Bred_bal),
                "background_seed_kind": str(background.seed_kind),
            }
        )
    return rows


def best_row_in_window(
    rows: list[dict[str, object]],
    *,
    q_min: float,
    q_max: float,
) -> dict[str, object]:
    window_rows = [
        row for row in rows
        if float(q_min) - 1.0e-12 <= float(row["q_mpa"]) <= float(q_max) + 1.0e-12
    ]
    if not window_rows:
        raise RuntimeError(f"No points found in local window {q_min:.6f} .. {q_max:.6f} MPa.")
    return min(window_rows, key=lambda row: (float(row["rho_R2"]), float(row["q_mpa"])))


def sign_label(gap: float) -> str:
    if gap < 0.0:
        return "n8_ahead"
    if gap > 0.0:
        return "n7_ahead"
    return "exact_tie"


def merge_intervals(intervals: list[tuple[float, float]], merge_tol: float = 0.01) -> list[tuple[float, float]]:
    if not intervals:
        return []
    ordered = sorted(intervals)
    merged: list[list[float]] = [[ordered[0][0], ordered[0][1]]]
    for left, right in ordered[1:]:
        current = merged[-1]
        if left <= current[1] + merge_tol:
            current[1] = max(current[1], right)
        else:
            merged.append([left, right])
    return [(float(left), float(right)) for left, right in merged]


def common_grid_gap_summary(curve_rows: list[dict[str, object]]) -> dict[str, object]:
    gaps = np.array([float(row["gap_rho_R2_n8_minus_n7"]) for row in curve_rows], dtype=float)
    q_grid = np.array([float(row["q_mpa"]) for row in curve_rows], dtype=float)
    abs_gap = np.abs(gaps)
    min_idx = int(np.argmin(abs_gap))

    raw_intervals: list[tuple[float, float]] = []
    for idx in range(len(gaps) - 1):
        if gaps[idx] == 0.0:
            raw_intervals.append((float(q_grid[idx]), float(q_grid[idx])))
        elif gaps[idx] * gaps[idx + 1] < 0.0:
            raw_intervals.append((float(q_grid[idx]), float(q_grid[idx + 1])))
    merged_intervals = merge_intervals(raw_intervals)

    negative_fraction = float(np.mean(gaps < 0.0))
    positive_fraction = float(np.mean(gaps > 0.0))
    near_zero_band = float(max(5.0e-06, 0.10 * np.median(abs_gap)))
    near_zero_qs = q_grid[abs_gap <= near_zero_band]

    return {
        "min_abs_gap_q_mpa": float(q_grid[min_idx]),
        "min_abs_gap_value": float(abs_gap[min_idx]),
        "gap_at_min_abs_q": float(gaps[min_idx]),
        "gap_sign_at_min_abs_q": sign_label(float(gaps[min_idx])),
        "negative_fraction_of_common_grid": negative_fraction,
        "positive_fraction_of_common_grid": positive_fraction,
        "sign_change_intervals_mpa": [
            {"q_left_mpa": float(left), "q_right_mpa": float(right)}
            for left, right in merged_intervals
        ],
        "near_zero_gap_band": near_zero_band,
        "near_zero_gap_q_min_mpa": float(np.min(near_zero_qs)) if near_zero_qs.size else float("nan"),
        "near_zero_gap_q_max_mpa": float(np.max(near_zero_qs)) if near_zero_qs.size else float("nan"),
    }


def main() -> None:
    start_time = time.time()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    background_config = high_bg.default_high_load_background_config()
    x0 = float(background_config.x0)
    common_grid = make_grid(
        float(COMMON_WINDOW["q_min"]),
        float(COMMON_WINDOW["q_max"]),
        int(COMMON_WINDOW["npts"]),
    )
    backgrounds, background_method = solve_window_backgrounds(common_grid, config=background_config)

    summary: dict[str, object] = {
        "method_note": (
            "Pairwise n=7 / n=8 gap study for the first practical R2 diagnostic on the clean full simple-support path. "
            "The equations, BC meaning, and solver behavior are unchanged. "
            "The study keeps rho_R2 as a comparative stacked diagnostic and measures whether the n=7 / n=8 preference "
            "is larger than small discretization drift by combining local-minimum comparisons with a shared common-grid gap curve."
        ),
        "background_config": dict(background_config.__dict__),
        "background_method": background_method,
        "common_window": COMMON_WINDOW,
        "local_windows": LOCAL_WINDOWS,
        "settings": list(SETTING_SPECS),
        "pair_modes": list(PAIR_MODES),
        "settings_summary": {},
    }

    curve_rows_all: list[dict[str, object]] = []
    table_rows: list[dict[str, object]] = []

    for setting in SETTING_SPECS:
        rows_by_mode: dict[int, list[dict[str, object]]] = {}
        for mode in PAIR_MODES:
            rows_by_mode[int(mode)] = build_mode_rows(
                mode=int(mode),
                setting=setting,
                q_grid=common_grid,
                backgrounds=backgrounds,
                x0=x0,
            )

        rows7 = rows_by_mode[7]
        rows8 = rows_by_mode[8]
        best7 = best_row_in_window(rows7, q_min=float(LOCAL_WINDOWS[7]["q_min"]), q_max=float(LOCAL_WINDOWS[7]["q_max"]))
        best8 = best_row_in_window(rows8, q_min=float(LOCAL_WINDOWS[8]["q_min"]), q_max=float(LOCAL_WINDOWS[8]["q_max"]))

        curve_rows: list[dict[str, object]] = []
        for row7, row8 in zip(rows7, rows8):
            gap = float(row8["rho_R2"]) - float(row7["rho_R2"])
            curve_row = {
                "setting": str(setting["label"]),
                "m_basis": int(setting["m_basis"]),
                "n_collocation": int(setting["n_collocation"]),
                "nd_base": int(setting["nd_base"]),
                "q_mpa": float(row7["q_mpa"]),
                "rho_R2_n7": float(row7["rho_R2"]),
                "rho_R2_raw_n7": float(row7["rho_R2_raw"]),
                "cond_G_amp_n7": float(row7["cond_G_amp"]),
                "rho_R2_n8": float(row8["rho_R2"]),
                "rho_R2_raw_n8": float(row8["rho_R2_raw"]),
                "cond_G_amp_n8": float(row8["cond_G_amp"]),
                "gap_rho_R2_n8_minus_n7": gap,
                "preferred_mode_on_common_grid": sign_label(gap),
            }
            curve_rows.append(curve_row)
            curve_rows_all.append(curve_row)

        curve_summary = common_grid_gap_summary(curve_rows)
        best_gap = float(best8["rho_R2"]) - float(best7["rho_R2"])
        preferred_mode = 8 if best_gap < 0.0 else 7 if best_gap > 0.0 else 0
        mean_best_scale = 0.5 * (abs(float(best7["rho_R2"])) + abs(float(best8["rho_R2"])))

        setting_summary = {
            "setting": str(setting["label"]),
            "m_basis": int(setting["m_basis"]),
            "n_collocation": int(setting["n_collocation"]),
            "nd_base": int(setting["nd_base"]),
            "best_n7": {
                "q_mpa": float(best7["q_mpa"]),
                "rho_R2": float(best7["rho_R2"]),
                "rho_R2_raw": float(best7["rho_R2_raw"]),
                "cond_G_amp": float(best7["cond_G_amp"]),
            },
            "best_n8": {
                "q_mpa": float(best8["q_mpa"]),
                "rho_R2": float(best8["rho_R2"]),
                "rho_R2_raw": float(best8["rho_R2_raw"]),
                "cond_G_amp": float(best8["cond_G_amp"]),
            },
            "best_gap_n8_minus_n7": best_gap,
            "best_gap_sign": sign_label(best_gap),
            "best_gap_relative_to_mean_best_scale": float(best_gap / max(mean_best_scale, EPS)),
            "best_load_gap_q8_minus_q7_mpa": float(best8["q_mpa"] - best7["q_mpa"]),
            "best_cond_gap_n8_minus_n7": float(best8["cond_G_amp"] - best7["cond_G_amp"]),
            "best_raw_gap_n8_minus_n7": float(best8["rho_R2_raw"] - best7["rho_R2_raw"]),
            "preferred_mode_from_separate_minima": int(preferred_mode),
            "common_grid_gap_summary": curve_summary,
        }
        summary["settings_summary"][str(setting["label"])] = setting_summary

        table_rows.append(
            {
                "setting": str(setting["label"]),
                "m_basis": int(setting["m_basis"]),
                "n_collocation": int(setting["n_collocation"]),
                "nd_base": int(setting["nd_base"]),
                "best_n7_q_mpa": float(best7["q_mpa"]),
                "best_n7_rho_R2": float(best7["rho_R2"]),
                "best_n7_rho_R2_raw": float(best7["rho_R2_raw"]),
                "best_n7_cond_G_amp": float(best7["cond_G_amp"]),
                "best_n8_q_mpa": float(best8["q_mpa"]),
                "best_n8_rho_R2": float(best8["rho_R2"]),
                "best_n8_rho_R2_raw": float(best8["rho_R2_raw"]),
                "best_n8_cond_G_amp": float(best8["cond_G_amp"]),
                "gap_n8_minus_n7": best_gap,
                "gap_sign": sign_label(best_gap),
                "gap_relative_to_mean_best_scale": float(best_gap / max(mean_best_scale, EPS)),
                "load_gap_q8_minus_q7_mpa": float(best8["q_mpa"] - best7["q_mpa"]),
                "best_cond_gap_n8_minus_n7": float(best8["cond_G_amp"] - best7["cond_G_amp"]),
                "best_raw_gap_n8_minus_n7": float(best8["rho_R2_raw"] - best7["rho_R2_raw"]),
                "common_grid_min_abs_gap_q_mpa": float(curve_summary["min_abs_gap_q_mpa"]),
                "common_grid_min_abs_gap_value": float(curve_summary["min_abs_gap_value"]),
                "common_grid_gap_at_min_abs_q": float(curve_summary["gap_at_min_abs_q"]),
                "common_grid_negative_fraction": float(curve_summary["negative_fraction_of_common_grid"]),
                "common_grid_positive_fraction": float(curve_summary["positive_fraction_of_common_grid"]),
                "common_grid_sign_change_count": int(len(curve_summary["sign_change_intervals_mpa"])),
                "common_grid_sign_change_windows": "; ".join(
                    f"{item['q_left_mpa']:.6f}..{item['q_right_mpa']:.6f}"
                    for item in curve_summary["sign_change_intervals_mpa"]
                ),
            }
        )

    best_gap_values = [float(row["gap_n8_minus_n7"]) for row in table_rows]
    best_gap_abs_values = [abs(value) for value in best_gap_values]
    n7_best_values = [float(row["best_n7_rho_R2"]) for row in table_rows]
    n8_best_values = [float(row["best_n8_rho_R2"]) for row in table_rows]
    n7_best_qs = [float(row["best_n7_q_mpa"]) for row in table_rows]
    n8_best_qs = [float(row["best_n8_q_mpa"]) for row in table_rows]

    if all(value < 0.0 for value in best_gap_values):
        decision = "A"
    elif all(value > 0.0 for value in best_gap_values):
        decision = "C"
    else:
        decision = "B"

    summary["pair_gap_summary"] = {
        "best_gap_n8_minus_n7": value_summary(best_gap_values),
        "best_gap_abs_n7_n8": value_summary(best_gap_abs_values),
        "n7_best_rho_R2": value_summary(n7_best_values),
        "n8_best_rho_R2": value_summary(n8_best_values),
        "n7_best_q_mpa": value_summary(n7_best_qs),
        "n8_best_q_mpa": value_summary(n8_best_qs),
        "separate_minima_signs": [sign_label(value) for value in best_gap_values],
        "settings_with_n8_ahead": int(sum(value < 0.0 for value in best_gap_values)),
        "settings_with_n7_ahead": int(sum(value > 0.0 for value in best_gap_values)),
        "max_mode_value_spread": float(max(value_summary(n7_best_values)["spread"], value_summary(n8_best_values)["spread"])),
        "median_abs_best_gap": float(np.median(np.asarray(best_gap_abs_values, dtype=float))),
        "decision": decision,
    }

    summary["simple_correlation_reading"] = {
        "winner_flip_setting_labels": [
            str(row["setting"]) for row in table_rows if str(row["gap_sign"]) == "n7_ahead"
        ],
        "winner_flip_matches_larger_n8_conditioning_at_best_points": [
            bool(float(row["best_cond_gap_n8_minus_n7"]) > 0.0)
            for row in table_rows if str(row["gap_sign"]) == "n7_ahead"
        ],
        "winner_flip_matches_larger_n8_raw_at_best_points": [
            bool(float(row["best_raw_gap_n8_minus_n7"]) > 0.0)
            for row in table_rows if str(row["gap_sign"]) == "n7_ahead"
        ],
        "note": (
            "If the sign flips without a consistent change in best-point cond(G_amp) or rho_R2_raw ordering, "
            "the pair is better read as near-degenerate rather than conditioning-resolved."
        ),
    }
    summary["runtime_seconds"] = float(time.time() - start_time)

    with SUMMARY_JSON.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False, allow_nan=True)
        fh.write("\n")

    summary_columns = [
        "setting",
        "m_basis",
        "n_collocation",
        "nd_base",
        "best_n7_q_mpa",
        "best_n7_rho_R2",
        "best_n7_rho_R2_raw",
        "best_n7_cond_G_amp",
        "best_n8_q_mpa",
        "best_n8_rho_R2",
        "best_n8_rho_R2_raw",
        "best_n8_cond_G_amp",
        "gap_n8_minus_n7",
        "gap_sign",
        "gap_relative_to_mean_best_scale",
        "load_gap_q8_minus_q7_mpa",
        "best_cond_gap_n8_minus_n7",
        "best_raw_gap_n8_minus_n7",
        "common_grid_min_abs_gap_q_mpa",
        "common_grid_min_abs_gap_value",
        "common_grid_gap_at_min_abs_q",
        "common_grid_negative_fraction",
        "common_grid_positive_fraction",
        "common_grid_sign_change_count",
        "common_grid_sign_change_windows",
    ]
    with SUMMARY_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=summary_columns)
        writer.writeheader()
        writer.writerows(table_rows)

    curve_columns = [
        "setting",
        "m_basis",
        "n_collocation",
        "nd_base",
        "q_mpa",
        "rho_R2_n7",
        "rho_R2_raw_n7",
        "cond_G_amp_n7",
        "rho_R2_n8",
        "rho_R2_raw_n8",
        "cond_G_amp_n8",
        "gap_rho_R2_n8_minus_n7",
        "preferred_mode_on_common_grid",
    ]
    with CURVES_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=curve_columns)
        writer.writeheader()
        writer.writerows(curve_rows_all)

    print("=== Criterion pilot R2 pair-gap study complete ===")
    print("\n=== Separate-minimum gaps ===")
    for row in table_rows:
        print(
            f"{row['setting']}: "
            f"n7 @ {row['best_n7_q_mpa']:.6f} MPa ({row['best_n7_rho_R2']:.6e}) | "
            f"n8 @ {row['best_n8_q_mpa']:.6f} MPa ({row['best_n8_rho_R2']:.6e}) | "
            f"gap(n8-n7)={row['gap_n8_minus_n7']:.6e} [{row['gap_sign']}]"
        )

    print("\n=== Pair conclusion code ===")
    print(f"decision={summary['pair_gap_summary']['decision']}")
    print(f"summary json: {SUMMARY_JSON}")
    print(f"summary csv:  {SUMMARY_CSV}")
    print(f"curves csv:   {CURVES_CSV}")
    print(f"runtime:      {summary['runtime_seconds']:.2f} s")


if __name__ == "__main__":
    main()