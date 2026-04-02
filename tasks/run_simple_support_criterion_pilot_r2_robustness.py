# -*- coding: utf-8 -*-
# Purpose:
#   Run the focused robustness pass for the first practical R2 diagnostic on
#   the clean full simple-support path without changing the main solver path.
# Typical use:
#   .venv\Scripts\python.exe tasks\run_simple_support_criterion_pilot_r2_robustness.py
# Outputs:
#   output/clean_full_simple_support/criterion_pilot_r2_robustness_summary.json
#   output/clean_full_simple_support/criterion_pilot_r2_robustness_table.csv
#   output/clean_full_simple_support/criterion_pilot_r2_robustness_points.csv

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
SUMMARY_JSON = OUTPUT_DIR / "criterion_pilot_r2_robustness_summary.json"
SUMMARY_CSV = OUTPUT_DIR / "criterion_pilot_r2_robustness_table.csv"
POINTS_CSV = OUTPUT_DIR / "criterion_pilot_r2_robustness_points.csv"

MODE_SPECS: dict[int, dict[str, object]] = {
    6: {
        "role_hint": "comparison control",
        "window": {"q_min": 17.5, "q_max": 17.9, "npts": 61},
    },
    7: {
        "role_hint": "competitive second candidate",
        "window": {"q_min": 17.2, "q_max": 17.5, "npts": 61},
    },
    8: {
        "role_hint": "current R2 winner candidate",
        "window": {"q_min": 17.4, "q_max": 17.7, "npts": 61},
    },
}

SETTING_SPECS: tuple[dict[str, object], ...] = (
    {"label": "baseline", "m_basis": 6, "n_collocation": 120, "nd_base": 4000},
    {"label": "basis_down", "m_basis": 5, "n_collocation": 120, "nd_base": 4000},
    {"label": "basis_up", "m_basis": 7, "n_collocation": 120, "nd_base": 4000},
    {"label": "collocation_down", "m_basis": 6, "n_collocation": 100, "nd_base": 4000},
    {"label": "collocation_up", "m_basis": 6, "n_collocation": 140, "nd_base": 4000},
    {"label": "paired_fine", "m_basis": 7, "n_collocation": 140, "nd_base": 4000},
)

METRIC_SPECS: tuple[tuple[str, str], ...] = (
    ("sigma_bal", "sigma_bal(B_mix)"),
    ("sigma_Bred_bal", "sigma_Bred_bal"),
    ("rho_R2", "rho_R2"),
)

MAX_BOOTSTRAP_STEP_MPA = 0.5
EPS = 1.0e-30


def make_grid(q_min: float, q_max: float, npts: int) -> np.ndarray:
    return np.linspace(float(q_min), float(q_max), int(npts), dtype=float)


def location_label(best_index: int, size: int) -> str:
    return "interior" if 0 < int(best_index) < int(size) - 1 else "boundary"


def condition_number(A: np.ndarray) -> float:
    singular_values = np.linalg.svd(np.asarray(A, dtype=float), compute_uv=False)
    if singular_values.size == 0:
        return float("nan")
    if singular_values[-1] <= EPS:
        return float("inf")
    return float(singular_values[0] / singular_values[-1])


def finite_min(values: np.ndarray) -> float:
    finite = values[np.isfinite(values)]
    return float(np.min(finite)) if finite.size else float("nan")


def finite_median(values: np.ndarray) -> float:
    finite = values[np.isfinite(values)]
    return float(np.median(finite)) if finite.size else float("nan")


def finite_max(values: np.ndarray) -> float:
    finite = values[np.isfinite(values)]
    return float(np.max(finite)) if finite.size else float("nan")


def cond_percentile(conds: np.ndarray, value: float) -> float:
    finite = conds[np.isfinite(conds)]
    if finite.size == 0 or not np.isfinite(value):
        return float("nan")
    return float(np.mean(finite <= float(value) + 1.0e-15))


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


def summarize_metric_curve(point_rows: list[dict[str, object]], metric_key: str) -> dict[str, object]:
    q_grid = np.array([float(row["q_mpa"]) for row in point_rows], dtype=float)
    values = np.array([float(row[metric_key]) for row in point_rows], dtype=float)
    conds = np.array([float(row["cond_G_amp"]) for row in point_rows], dtype=float)

    best_index = int(np.argmin(values))
    best_row = point_rows[best_index]
    max_cond = finite_max(conds)
    best_cond = float(best_row["cond_G_amp"])

    summary: dict[str, object] = {
        "best_q_mpa": float(best_row["q_mpa"]),
        "best_value": float(best_row[metric_key]),
        "best_location": location_label(best_index, values.size),
        "best_cond_G_amp": best_cond,
        "best_cond_percentile": cond_percentile(conds, best_cond),
        "best_cond_ratio_to_window_max": float(best_cond / max(max_cond, EPS)) if np.isfinite(max_cond) else float("nan"),
        "cond_window_min": finite_min(conds),
        "cond_window_median": finite_median(conds),
        "cond_window_max": max_cond,
    }
    if metric_key == "rho_R2":
        summary["best_rho_R2_raw"] = float(best_row["rho_R2_raw"])
    return summary


def build_metric_ranking(
    summary: dict[str, object],
    setting_label: str,
    metric_key: str,
    metric_label: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for mode, mode_spec in MODE_SPECS.items():
        mode_summary = summary["modes"][str(mode)]
        setting_summary = mode_summary["settings"][setting_label]["metric_summaries"][metric_key]
        row = {
            "n": int(mode),
            "role_hint": str(mode_spec["role_hint"]),
            "q_mpa": float(setting_summary["best_q_mpa"]),
            "value": float(setting_summary["best_value"]),
            "metric_key": metric_key,
            "metric_label": metric_label,
            "best_cond_G_amp": float(setting_summary["best_cond_G_amp"]),
            "best_cond_percentile": float(setting_summary["best_cond_percentile"]),
            "best_cond_ratio_to_window_max": float(setting_summary["best_cond_ratio_to_window_max"]),
        }
        if metric_key == "rho_R2":
            row["rho_R2_raw"] = float(setting_summary["best_rho_R2_raw"])
        rows.append(row)

    rows.sort(key=lambda row: (float(row["value"]), float(row["q_mpa"]), int(row["n"])))
    for rank, row in enumerate(rows, start=1):
        row["rank"] = int(rank)
    return rows


def range_summary(values: list[float]) -> dict[str, float]:
    arr = np.asarray(values, dtype=float)
    finite = arr[np.isfinite(arr)]
    if finite.size == 0:
        return {"min": float("nan"), "median": float("nan"), "max": float("nan")}
    return {
        "min": float(np.min(finite)),
        "median": float(np.median(finite)),
        "max": float(np.max(finite)),
    }


def main() -> None:
    start_time = time.time()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    background_config = high_bg.default_high_load_background_config()
    x0 = float(background_config.x0)

    summary: dict[str, object] = {
        "method_note": (
            "Focused robustness pass for the first practical R2 diagnostic on the clean full simple-support path. "
            "The clean solver path, equations, and BC meaning are unchanged. "
            "The pass keeps sigma_bal(B_mix) and sigma_Bred_bal as auxiliary boundary diagnostics while "
            "testing rho_R2 on dense local windows for n=6,7,8 under small m_basis / n_collocation variations. "
            "Each point also records rho_R2_raw and cond(G_amp) so the R2 winner can be checked against "
            "conditioning changes rather than only raw ranking."
        ),
        "background_config": dict(background_config.__dict__),
        "mode_specs": MODE_SPECS,
        "settings": list(SETTING_SPECS),
        "modes": {},
    }

    point_rows_all: list[dict[str, object]] = []

    for mode, mode_spec in MODE_SPECS.items():
        role_hint = str(mode_spec["role_hint"])
        window = dict(mode_spec["window"])
        q_grid = make_grid(float(window["q_min"]), float(window["q_max"]), int(window["npts"]))
        backgrounds, background_method = solve_window_backgrounds(q_grid, config=background_config)

        mode_summary: dict[str, object] = {
            "role_hint": role_hint,
            "window": {
                "q_min_mpa": float(q_grid[0]),
                "q_max_mpa": float(q_grid[-1]),
                "npts": int(q_grid.size),
            },
            "background_method": background_method,
            "successful_background_solves": int(len(backgrounds)),
            "first_background_failure": None,
            "settings": {},
        }

        for setting in SETTING_SPECS:
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
                row = {
                    "n": int(mode),
                    "role_hint": role_hint,
                    "setting": str(setting["label"]),
                    "m_basis": int(setting["m_basis"]),
                    "n_collocation": int(setting["n_collocation"]),
                    "nd_base": int(setting["nd_base"]),
                    "q_mpa": float(q_mpa),
                    "sigma_bal": float(obj.sigma_bal),
                    "sigma_Bred_bal": float(obj.sigma_Bred_bal),
                    "rho_R2": float(obj.rho_R2),
                    "rho_R2_raw": float(obj.rho_R2_raw),
                    "cond_G_amp": condition_number(obj.G_amp),
                    "sigma_raw": float(obj.sigma_raw),
                    "sigma_bal_noH": float(obj.sigma_bal_noH),
                    "residual_norm_1": float(obj.residual_norms[0]),
                    "residual_norm_2": float(obj.residual_norms[1]),
                    "background_seed_kind": str(background.seed_kind),
                }
                point_rows.append(row)
                point_rows_all.append(row)

            metric_summaries = {
                metric_key: summarize_metric_curve(point_rows, metric_key)
                for metric_key, _metric_label in METRIC_SPECS
            }
            mode_summary["settings"][str(setting["label"])] = {
                "m_basis": int(setting["m_basis"]),
                "n_collocation": int(setting["n_collocation"]),
                "nd_base": int(setting["nd_base"]),
                "metric_summaries": metric_summaries,
            }

        summary["modes"][str(mode)] = mode_summary

    rankings_by_setting: dict[str, dict[str, list[dict[str, object]]]] = {}
    rank_lookup: dict[tuple[str, str, int], int] = {}
    for setting in SETTING_SPECS:
        setting_label = str(setting["label"])
        rankings_by_setting[setting_label] = {}
        for metric_key, metric_label in METRIC_SPECS:
            ranking = build_metric_ranking(summary, setting_label, metric_key, metric_label)
            rankings_by_setting[setting_label][metric_key] = ranking
            for row in ranking:
                rank_lookup[(setting_label, metric_key, int(row["n"]))] = int(row["rank"])

    summary["rankings_by_setting"] = rankings_by_setting

    table_rows: list[dict[str, object]] = []
    for mode in MODE_SPECS:
        for setting in SETTING_SPECS:
            setting_label = str(setting["label"])
            setting_summary = summary["modes"][str(mode)]["settings"][setting_label]
            sigma_bal_summary = setting_summary["metric_summaries"]["sigma_bal"]
            sigma_bred_summary = setting_summary["metric_summaries"]["sigma_Bred_bal"]
            rho_r2_summary = setting_summary["metric_summaries"]["rho_R2"]
            window = summary["modes"][str(mode)]["window"]
            table_rows.append(
                {
                    "n": int(mode),
                    "role_hint": str(MODE_SPECS[int(mode)]["role_hint"]),
                    "setting": setting_label,
                    "m_basis": int(setting["m_basis"]),
                    "n_collocation": int(setting["n_collocation"]),
                    "nd_base": int(setting["nd_base"]),
                    "window_q_min_mpa": float(window["q_min_mpa"]),
                    "window_q_max_mpa": float(window["q_max_mpa"]),
                    "window_npts": int(window["npts"]),
                    "sigma_bal_best_q_mpa": float(sigma_bal_summary["best_q_mpa"]),
                    "sigma_bal_best_value": float(sigma_bal_summary["best_value"]),
                    "sigma_bal_best_cond_G_amp": float(sigma_bal_summary["best_cond_G_amp"]),
                    "sigma_Bred_bal_best_q_mpa": float(sigma_bred_summary["best_q_mpa"]),
                    "sigma_Bred_bal_best_value": float(sigma_bred_summary["best_value"]),
                    "sigma_Bred_bal_best_cond_G_amp": float(sigma_bred_summary["best_cond_G_amp"]),
                    "rho_R2_best_q_mpa": float(rho_r2_summary["best_q_mpa"]),
                    "rho_R2_best_value": float(rho_r2_summary["best_value"]),
                    "rho_R2_best_raw": float(rho_r2_summary["best_rho_R2_raw"]),
                    "rho_R2_best_cond_G_amp": float(rho_r2_summary["best_cond_G_amp"]),
                    "rho_R2_best_cond_percentile": float(rho_r2_summary["best_cond_percentile"]),
                    "rho_R2_best_cond_ratio_to_window_max": float(rho_r2_summary["best_cond_ratio_to_window_max"]),
                    "cond_G_amp_window_min": float(rho_r2_summary["cond_window_min"]),
                    "cond_G_amp_window_median": float(rho_r2_summary["cond_window_median"]),
                    "cond_G_amp_window_max": float(rho_r2_summary["cond_window_max"]),
                    "sigma_bal_rank": rank_lookup[(setting_label, "sigma_bal", int(mode))],
                    "sigma_Bred_bal_rank": rank_lookup[(setting_label, "sigma_Bred_bal", int(mode))],
                    "rho_R2_rank": rank_lookup[(setting_label, "rho_R2", int(mode))],
                }
            )

    r2_winner_rows: list[dict[str, object]] = []
    for setting in SETTING_SPECS:
        setting_label = str(setting["label"])
        ranking = rankings_by_setting[setting_label]["rho_R2"]
        winner = ranking[0]
        second = ranking[1]
        third = ranking[2]
        n8_row = next(row for row in ranking if int(row["n"]) == 8)
        n7_row = next(row for row in ranking if int(row["n"]) == 7)
        n6_row = next(row for row in ranking if int(row["n"]) == 6)
        r2_winner_rows.append(
            {
                "setting": setting_label,
                "m_basis": int(setting["m_basis"]),
                "n_collocation": int(setting["n_collocation"]),
                "winner_n": int(winner["n"]),
                "winner_q_mpa": float(winner["q_mpa"]),
                "winner_value": float(winner["value"]),
                "winner_cond_G_amp": float(winner["best_cond_G_amp"]),
                "winner_cond_percentile": float(winner["best_cond_percentile"]),
                "second_n": int(second["n"]),
                "second_value": float(second["value"]),
                "third_n": int(third["n"]),
                "third_value": float(third["value"]),
                "n8_value": float(n8_row["value"]),
                "n7_value": float(n7_row["value"]),
                "n6_value": float(n6_row["value"]),
                "n8_cond_G_amp": float(n8_row["best_cond_G_amp"]),
                "n7_cond_G_amp": float(n7_row["best_cond_G_amp"]),
                "n6_cond_G_amp": float(n6_row["best_cond_G_amp"]),
                "n8_cond_percentile": float(n8_row["best_cond_percentile"]),
                "n7_cond_percentile": float(n7_row["best_cond_percentile"]),
                "n6_cond_percentile": float(n6_row["best_cond_percentile"]),
                "n8_minus_n7": float(n7_row["value"] - n8_row["value"]),
                "n7_minus_n6": float(n6_row["value"] - n7_row["value"]),
                "n8_ahead_of_n7": bool(float(n8_row["value"]) < float(n7_row["value"])),
                "n7_ahead_of_n6": bool(float(n7_row["value"]) < float(n6_row["value"])),
            }
        )

    lowest_winner_cond = min(r2_winner_rows, key=lambda row: float(row["winner_cond_G_amp"]))
    highest_winner_cond = max(r2_winner_rows, key=lambda row: float(row["winner_cond_G_amp"]))
    summary["r2_robustness"] = {
        "winner_rows": r2_winner_rows,
        "n8_ahead_of_n7_all_settings": all(bool(row["n8_ahead_of_n7"]) for row in r2_winner_rows),
        "n7_second_all_settings": all(int(row["second_n"]) == 7 for row in r2_winner_rows),
        "n6_third_all_settings": all(int(row["third_n"]) == 6 for row in r2_winner_rows),
        "winner_changes_across_settings": len({int(row["winner_n"]) for row in r2_winner_rows}) > 1,
        "winner_changes_when_conditioning_worsens": int(lowest_winner_cond["winner_n"]) != int(highest_winner_cond["winner_n"]),
        "lowest_winner_conditioning_setting": lowest_winner_cond,
        "highest_winner_conditioning_setting": highest_winner_cond,
        "n8_minus_n7_value_gap": range_summary([float(row["n8_minus_n7"]) for row in r2_winner_rows]),
        "n7_minus_n6_value_gap": range_summary([float(row["n7_minus_n6"]) for row in r2_winner_rows]),
        "n8_best_cond_G_amp": range_summary([float(row["n8_cond_G_amp"]) for row in r2_winner_rows]),
        "n7_best_cond_G_amp": range_summary([float(row["n7_cond_G_amp"]) for row in r2_winner_rows]),
        "n6_best_cond_G_amp": range_summary([float(row["n6_cond_G_amp"]) for row in r2_winner_rows]),
        "n8_best_cond_percentile": range_summary([float(row["n8_cond_percentile"]) for row in r2_winner_rows]),
        "n7_best_cond_percentile": range_summary([float(row["n7_cond_percentile"]) for row in r2_winner_rows]),
        "n6_best_cond_percentile": range_summary([float(row["n6_cond_percentile"]) for row in r2_winner_rows]),
    }

    summary["runtime_seconds"] = float(time.time() - start_time)

    with SUMMARY_JSON.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False, allow_nan=True)
        fh.write("\n")

    table_columns = [
        "n",
        "role_hint",
        "setting",
        "m_basis",
        "n_collocation",
        "nd_base",
        "window_q_min_mpa",
        "window_q_max_mpa",
        "window_npts",
        "sigma_bal_best_q_mpa",
        "sigma_bal_best_value",
        "sigma_bal_best_cond_G_amp",
        "sigma_Bred_bal_best_q_mpa",
        "sigma_Bred_bal_best_value",
        "sigma_Bred_bal_best_cond_G_amp",
        "rho_R2_best_q_mpa",
        "rho_R2_best_value",
        "rho_R2_best_raw",
        "rho_R2_best_cond_G_amp",
        "rho_R2_best_cond_percentile",
        "rho_R2_best_cond_ratio_to_window_max",
        "cond_G_amp_window_min",
        "cond_G_amp_window_median",
        "cond_G_amp_window_max",
        "sigma_bal_rank",
        "sigma_Bred_bal_rank",
        "rho_R2_rank",
    ]
    with SUMMARY_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=table_columns)
        writer.writeheader()
        writer.writerows(table_rows)

    point_columns = [
        "n",
        "role_hint",
        "setting",
        "m_basis",
        "n_collocation",
        "nd_base",
        "q_mpa",
        "sigma_bal",
        "sigma_Bred_bal",
        "rho_R2",
        "rho_R2_raw",
        "cond_G_amp",
        "sigma_raw",
        "sigma_bal_noH",
        "residual_norm_1",
        "residual_norm_2",
        "background_seed_kind",
    ]
    with POINTS_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=point_columns)
        writer.writeheader()
        writer.writerows(point_rows_all)

    print("=== Criterion pilot R2 robustness pass complete ===")
    print("\n=== R2 ranking by setting ===")
    for row in r2_winner_rows:
        print(
            f"{row['setting']}: "
            f"#1 n={row['winner_n']} ({row['winner_value']:.6e})  "
            f"#2 n={row['second_n']} ({row['second_value']:.6e})  "
            f"#3 n={row['third_n']} ({row['third_value']:.6e})  "
            f"winner cond(G_amp)={row['winner_cond_G_amp']:.6e}"
        )

    print("\n=== Robustness summary ===")
    print(f"n8 ahead of n7 in rho_R2 across all settings: {summary['r2_robustness']['n8_ahead_of_n7_all_settings']}")
    print(f"n7 stays second across all settings:       {summary['r2_robustness']['n7_second_all_settings']}")
    print(f"n6 stays third across all settings:        {summary['r2_robustness']['n6_third_all_settings']}")
    print(
        "winner changes when conditioning worsens:   "
        f"{summary['r2_robustness']['winner_changes_when_conditioning_worsens']}"
    )

    print(f"\nsummary json: {SUMMARY_JSON}")
    print(f"summary csv:  {SUMMARY_CSV}")
    print(f"points csv:   {POINTS_CSV}")
    print(f"runtime:      {summary['runtime_seconds']:.2f} s")


if __name__ == "__main__":
    main()
