# -*- coding: utf-8 -*-
# Purpose:
#   Run a focused pair-resolution study for the near-degenerate n=7 / n=8 R2
#   reading on the clean full simple-support path without changing the main
#   solver path.
# Typical use:
#   .venv\Scripts\python.exe tasks\run_simple_support_criterion_pilot_r2_pair_resolution.py
# Outputs:
#   output/clean_full_simple_support/criterion_pilot_r2_pair_resolution_summary.json
#   output/clean_full_simple_support/criterion_pilot_r2_pair_resolution_table.csv
#   output/clean_full_simple_support/criterion_pilot_r2_pair_resolution_curves.csv

from __future__ import annotations

import csv
import json
import time
import warnings
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
SUMMARY_JSON = OUTPUT_DIR / "criterion_pilot_r2_pair_resolution_summary.json"
SUMMARY_CSV = OUTPUT_DIR / "criterion_pilot_r2_pair_resolution_table.csv"
CURVES_CSV = OUTPUT_DIR / "criterion_pilot_r2_pair_resolution_curves.csv"

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
VALLEY_REL_THRESHOLDS = (0.10, 0.25, 0.50)
LOCAL_SHAPE_HALF_SPAN_POINTS = 3
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


def pairwise_count_summary(labels: list[str]) -> dict[str, object]:
    counts = {"n8": 0, "n7": 0, "tie": 0, "unresolved": 0}
    for label in labels:
        if label in counts:
            counts[label] += 1
        else:
            counts["unresolved"] += 1
    if counts["n8"] > counts["n7"]:
        majority = "n8"
    elif counts["n7"] > counts["n8"]:
        majority = "n7"
    elif counts["n8"] == counts["n7"] and counts["n8"] > 0:
        majority = "split"
    else:
        majority = "unresolved"
    return {
        "labels": labels,
        "counts": counts,
        "majority": majority,
    }


def winner_from_signed_value(value: float, *, positive_means_n8: bool = True) -> str:
    if not np.isfinite(value) or abs(value) <= EPS:
        return "tie"
    if positive_means_n8:
        return "n8" if value > 0.0 else "n7"
    return "n7" if value > 0.0 else "n8"


def winner_from_pair(n8_value: float, n7_value: float, *, larger_is_better: bool = True) -> str:
    if not (np.isfinite(n8_value) and np.isfinite(n7_value)):
        return "unresolved"
    if abs(n8_value - n7_value) <= EPS:
        return "tie"
    if larger_is_better:
        return "n8" if n8_value > n7_value else "n7"
    return "n8" if n8_value < n7_value else "n7"


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
                "background_seed_kind": str(background.seed_kind),
            }
        )
    return rows
def window_rows(rows: list[dict[str, object]], *, q_min: float, q_max: float) -> list[dict[str, object]]:
    return [
        row for row in rows
        if float(q_min) - 1.0e-12 <= float(row["q_mpa"]) <= float(q_max) + 1.0e-12
    ]


def arrays_from_rows(rows: list[dict[str, object]], key: str) -> tuple[np.ndarray, np.ndarray]:
    q = np.asarray([float(row["q_mpa"]) for row in rows], dtype=float)
    values = np.asarray([float(row[key]) for row in rows], dtype=float)
    return q, values


def best_row_in_window(
    rows: list[dict[str, object]],
    *,
    q_min: float,
    q_max: float,
) -> dict[str, object]:
    local_rows = window_rows(rows, q_min=q_min, q_max=q_max)
    if not local_rows:
        raise RuntimeError(f"No points found in local window {q_min:.6f} .. {q_max:.6f} MPa.")
    return min(local_rows, key=lambda row: (float(row["rho_R2"]), float(row["q_mpa"])))


def interpolate_crossing(q1: float, y1: float, q2: float, y2: float, target: float) -> float:
    if not (np.isfinite(y1) and np.isfinite(y2)):
        return float(0.5 * (q1 + q2))
    if abs(y2 - y1) <= EPS:
        return float(0.5 * (q1 + q2))
    return float(q1 + (target - y1) * (q2 - q1) / (y2 - y1))


def valley_width_summary(
    rows: list[dict[str, object]],
    *,
    q_min: float,
    q_max: float,
    rel_threshold: float,
) -> dict[str, object]:
    local_rows = window_rows(rows, q_min=q_min, q_max=q_max)
    if not local_rows:
        raise RuntimeError(f"No points found in local window {q_min:.6f} .. {q_max:.6f} MPa.")
    q, rho = arrays_from_rows(local_rows, "rho_R2")
    idx = int(np.argmin(rho))
    rho_min = float(rho[idx])
    threshold = float(rho_min * (1.0 + rel_threshold))

    left = idx
    while left > 0 and float(rho[left - 1]) <= threshold:
        left -= 1
    right = idx
    while right < len(rho) - 1 and float(rho[right + 1]) <= threshold:
        right += 1

    q_left = float(q[left])
    q_right = float(q[right])
    left_censored = bool(left == 0)
    right_censored = bool(right == len(rho) - 1)

    if left > 0 and float(rho[left - 1]) > threshold and float(rho[left]) < threshold:
        q_left = interpolate_crossing(
            float(q[left - 1]),
            float(rho[left - 1]),
            float(q[left]),
            float(rho[left]),
            threshold,
        )
    if right < len(rho) - 1 and float(rho[right + 1]) > threshold and float(rho[right]) < threshold:
        q_right = interpolate_crossing(
            float(q[right]),
            float(rho[right]),
            float(q[right + 1]),
            float(rho[right + 1]),
            threshold,
        )

    return {
        "rel_threshold": float(rel_threshold),
        "rho_min": rho_min,
        "rho_threshold": threshold,
        "q_minimum_mpa": float(q[idx]),
        "q_left_mpa": q_left,
        "q_right_mpa": q_right,
        "width_mpa": float(max(q_right - q_left, 0.0)),
        "left_censored": left_censored,
        "right_censored": right_censored,
        "censored": bool(left_censored or right_censored),
    }


def collect_sign_segments(q: np.ndarray, values: np.ndarray, *, positive: bool) -> list[dict[str, float]]:
    if q.size < 2:
        return []
    segments: list[dict[str, float]] = []
    current_start: float | None = None

    for idx in range(len(values) - 1):
        v_left = float(values[idx])
        v_right = float(values[idx + 1])
        q_left = float(q[idx])
        q_right = float(q[idx + 1])
        active_left = v_left > 0.0 if positive else v_left < 0.0
        active_right = v_right > 0.0 if positive else v_right < 0.0

        if active_left and current_start is None:
            current_start = q_left
        if active_left and not active_right:
            end = interpolate_crossing(q_left, v_left, q_right, v_right, 0.0)
            if current_start is None:
                current_start = q_left
            segments.append(
                {
                    "q_left_mpa": float(current_start),
                    "q_right_mpa": float(end),
                    "length_mpa": float(max(end - current_start, 0.0)),
                }
            )
            current_start = None
        elif (not active_left) and active_right:
            current_start = interpolate_crossing(q_left, v_left, q_right, v_right, 0.0)

    tail_value = float(values[-1])
    tail_active = tail_value > 0.0 if positive else tail_value < 0.0
    if tail_active:
        if current_start is None:
            current_start = float(q[-1])
        segments.append(
            {
                "q_left_mpa": float(current_start),
                "q_right_mpa": float(q[-1]),
                "length_mpa": float(max(float(q[-1]) - current_start, 0.0)),
            }
        )
    return segments


def persistence_summary(q: np.ndarray, advantage_n8: np.ndarray) -> dict[str, object]:
    total_length = float(max(float(q[-1]) - float(q[0]), 0.0)) if q.size else 0.0
    n8_segments = collect_sign_segments(q, advantage_n8, positive=True)
    n7_segments = collect_sign_segments(q, advantage_n8, positive=False)
    n8_total = float(sum(float(item["length_mpa"]) for item in n8_segments))
    n7_total = float(sum(float(item["length_mpa"]) for item in n7_segments))
    n8_longest = max((float(item["length_mpa"]) for item in n8_segments), default=0.0)
    n7_longest = max((float(item["length_mpa"]) for item in n7_segments), default=0.0)

    def longest_interval(segments: list[dict[str, float]]) -> dict[str, float]:
        if not segments:
            return {"q_left_mpa": float("nan"), "q_right_mpa": float("nan"), "length_mpa": 0.0}
        return max(segments, key=lambda item: float(item["length_mpa"]))

    return {
        "window_length_mpa": total_length,
        "n8_ahead_fraction": float(n8_total / max(total_length, EPS)),
        "n7_ahead_fraction": float(n7_total / max(total_length, EPS)),
        "fraction_bias_n8_minus_n7": float((n8_total - n7_total) / max(total_length, EPS)),
        "n8_ahead_segments": n8_segments,
        "n7_ahead_segments": n7_segments,
        "n8_longest_interval": longest_interval(n8_segments),
        "n7_longest_interval": longest_interval(n7_segments),
        "sign_change_count": int(len(n8_segments) + len(n7_segments) - 1) if (n8_segments or n7_segments) else 0,
        "ahead_fraction_winner": winner_from_pair(n8_total, n7_total, larger_is_better=True),
        "longest_interval_winner": winner_from_pair(n8_longest, n7_longest, larger_is_better=True),
    }


def local_shape_summary(
    rows: list[dict[str, object]],
    *,
    q_min: float,
    q_max: float,
    half_span_points: int,
) -> dict[str, object]:
    local_rows = window_rows(rows, q_min=q_min, q_max=q_max)
    q, rho = arrays_from_rows(local_rows, "rho_R2")
    idx = int(np.argmin(rho))
    left = max(0, idx - int(half_span_points))
    right = min(len(q), idx + int(half_span_points) + 1)
    x = q[left:right] - float(q[idx])
    y = rho[left:right]
    if x.size < 3:
        return {
            "q_mpa": float(q[idx]),
            "rho_min": float(rho[idx]),
            "fit_point_count": int(x.size),
            "quadratic_curvature": float("nan"),
            "relative_curvature": float("nan"),
            "predicted_width_rel25_mpa": float("nan"),
            "fit_r2": float("nan"),
            "fit_is_convex": False,
        }

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        coeffs = np.polyfit(x, y, deg=2)
    a, b, c = [float(value) for value in coeffs]
    fitted = np.polyval(coeffs, x)
    ss_res = float(np.sum((y - fitted) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    curvature = float(2.0 * a)
    rho_min = float(rho[idx])
    relative_curvature = float(curvature / max(rho_min, EPS))
    predicted_width_rel25 = float(2.0 * np.sqrt(max(0.5 / max(relative_curvature, EPS), 0.0))) if relative_curvature > 0.0 else float("nan")

    return {
        "q_mpa": float(q[idx]),
        "rho_min": rho_min,
        "fit_point_count": int(x.size),
        "quadratic_curvature": curvature,
        "relative_curvature": relative_curvature,
        "predicted_width_rel25_mpa": predicted_width_rel25,
        "fit_r2": float(1.0 - ss_res / ss_tot) if ss_tot > EPS else float("nan"),
        "fit_is_convex": bool(curvature > 0.0),
        "fit_linear_term": b,
        "fit_constant_term": c,
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
            "Pairwise n=7 / n=8 resolution study for the first practical R2 diagnostic on the clean full simple-support path. "
            "The equations, BC meaning, and solver behavior are unchanged. "
            "The study keeps rho_R2 as a comparative stacked diagnostic and asks whether broader valley shape, "
            "signed area, and sign persistence on the shared dense window are more stable than pointwise minima."
        ),
        "background_config": dict(background_config.__dict__),
        "background_method": background_method,
        "common_window": COMMON_WINDOW,
        "local_windows": LOCAL_WINDOWS,
        "settings": list(SETTING_SPECS),
        "pair_modes": list(PAIR_MODES),
        "valley_relative_thresholds": list(VALLEY_REL_THRESHOLDS),
        "local_shape_half_span_points": int(LOCAL_SHAPE_HALF_SPAN_POINTS),
        "settings_summary": {},
    }

    table_rows: list[dict[str, object]] = []
    curve_rows_all: list[dict[str, object]] = []

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

        q = np.asarray([float(row["q_mpa"]) for row in rows7], dtype=float)
        rho7 = np.asarray([float(row["rho_R2"]) for row in rows7], dtype=float)
        rho8 = np.asarray([float(row["rho_R2"]) for row in rows8], dtype=float)
        raw7 = np.asarray([float(row["rho_R2_raw"]) for row in rows7], dtype=float)
        raw8 = np.asarray([float(row["rho_R2_raw"]) for row in rows8], dtype=float)
        cond7 = np.asarray([float(row["cond_G_amp"]) for row in rows7], dtype=float)
        cond8 = np.asarray([float(row["cond_G_amp"]) for row in rows8], dtype=float)

        gap_n8_minus_n7 = rho8 - rho7
        advantage_n8 = rho7 - rho8
        local_scale = 0.5 * (np.abs(rho7) + np.abs(rho8))
        normalized_advantage_n8 = advantage_n8 / np.maximum(local_scale, EPS)

        signed_area_n8 = float(np.trapezoid(advantage_n8, q))
        abs_area = float(np.trapezoid(np.abs(advantage_n8), q))
        normalized_signed_area = float(signed_area_n8 / max(abs_area, EPS))
        normalized_area_integral = float(np.trapezoid(normalized_advantage_n8, q))
        mean_normalized_advantage = float(normalized_area_integral / max(float(q[-1] - q[0]), EPS))

        cumulative_signed_area = [0.0]
        cumulative_abs_area = [0.0]
        for idx in range(1, len(q)):
            dq = float(q[idx] - q[idx - 1])
            cumulative_signed_area.append(
                float(cumulative_signed_area[-1] + 0.5 * dq * (advantage_n8[idx - 1] + advantage_n8[idx]))
            )
            cumulative_abs_area.append(
                float(cumulative_abs_area[-1] + 0.5 * dq * (abs(advantage_n8[idx - 1]) + abs(advantage_n8[idx])))
            )

        persistence = persistence_summary(q, advantage_n8)

        valley_threshold_summaries: dict[str, object] = {}
        for rel in VALLEY_REL_THRESHOLDS:
            key = f"rel_{int(round(100.0 * rel)):02d}"
            valley7 = valley_width_summary(
                rows7,
                q_min=float(LOCAL_WINDOWS[7]["q_min"]),
                q_max=float(LOCAL_WINDOWS[7]["q_max"]),
                rel_threshold=float(rel),
            )
            valley8 = valley_width_summary(
                rows8,
                q_min=float(LOCAL_WINDOWS[8]["q_min"]),
                q_max=float(LOCAL_WINDOWS[8]["q_max"]),
                rel_threshold=float(rel),
            )
            width_bias = float(valley8["width_mpa"] - valley7["width_mpa"])
            valley_threshold_summaries[key] = {
                "n7": valley7,
                "n8": valley8,
                "width_bias_n8_minus_n7_mpa": width_bias,
                "winner": winner_from_signed_value(width_bias, positive_means_n8=True),
            }

        shape7 = local_shape_summary(
            rows7,
            q_min=float(LOCAL_WINDOWS[7]["q_min"]),
            q_max=float(LOCAL_WINDOWS[7]["q_max"]),
            half_span_points=int(LOCAL_SHAPE_HALF_SPAN_POINTS),
        )
        shape8 = local_shape_summary(
            rows8,
            q_min=float(LOCAL_WINDOWS[8]["q_min"]),
            q_max=float(LOCAL_WINDOWS[8]["q_max"]),
            half_span_points=int(LOCAL_SHAPE_HALF_SPAN_POINTS),
        )
        curvature_winner = winner_from_pair(
            float(shape8["relative_curvature"]),
            float(shape7["relative_curvature"]),
            larger_is_better=False,
        ) if bool(shape7["fit_is_convex"]) and bool(shape8["fit_is_convex"]) else "unresolved"

        pointwise_gap = float(best8["rho_R2"] - best7["rho_R2"])
        pointwise_winner = winner_from_signed_value(-pointwise_gap, positive_means_n8=True)
        signed_area_winner = winner_from_signed_value(signed_area_n8, positive_means_n8=True)
        normalized_area_winner = winner_from_signed_value(mean_normalized_advantage, positive_means_n8=True)

        setting_summary = {
            "setting": str(setting["label"]),
            "m_basis": int(setting["m_basis"]),
            "n_collocation": int(setting["n_collocation"]),
            "nd_base": int(setting["nd_base"]),
            "pointwise_minima": {
                "n7": {
                    "q_mpa": float(best7["q_mpa"]),
                    "rho_R2": float(best7["rho_R2"]),
                    "rho_R2_raw": float(best7["rho_R2_raw"]),
                    "cond_G_amp": float(best7["cond_G_amp"]),
                },
                "n8": {
                    "q_mpa": float(best8["q_mpa"]),
                    "rho_R2": float(best8["rho_R2"]),
                    "rho_R2_raw": float(best8["rho_R2_raw"]),
                    "cond_G_amp": float(best8["cond_G_amp"]),
                },
                "gap_n8_minus_n7": pointwise_gap,
                "winner": pointwise_winner,
            },
            "valley_widths": valley_threshold_summaries,
            "integrated_advantage": {
                "definition": "Positive values mean n8 has lower rho_R2 on average over the common window because the integrand is rho_R2(n7) - rho_R2(n8).",
                "signed_area_n8_minus_n7": signed_area_n8,
                "absolute_area": abs_area,
                "normalized_signed_area": normalized_signed_area,
                "mean_normalized_advantage": mean_normalized_advantage,
                "winner": signed_area_winner,
                "normalized_winner": normalized_area_winner,
            },
            "persistence": persistence,
            "local_shape": {
                "n7": shape7,
                "n8": shape8,
                "relative_curvature_winner": curvature_winner,
            },
            "metric_winners": {
                "pointwise_minimum": pointwise_winner,
                "signed_area": signed_area_winner,
                "mean_normalized_advantage": normalized_area_winner,
                "ahead_fraction": str(persistence["ahead_fraction_winner"]),
                "longest_interval": str(persistence["longest_interval_winner"]),
                "valley_width_rel10": str(valley_threshold_summaries["rel_10"]["winner"]),
                "valley_width_rel25": str(valley_threshold_summaries["rel_25"]["winner"]),
                "valley_width_rel50": str(valley_threshold_summaries["rel_50"]["winner"]),
                "relative_curvature": curvature_winner,
            },
        }
        summary["settings_summary"][str(setting["label"])] = setting_summary
        for idx, q_mpa in enumerate(q):
            curve_rows_all.append(
                {
                    "setting": str(setting["label"]),
                    "m_basis": int(setting["m_basis"]),
                    "n_collocation": int(setting["n_collocation"]),
                    "nd_base": int(setting["nd_base"]),
                    "q_mpa": float(q_mpa),
                    "rho_R2_n7": float(rho7[idx]),
                    "rho_R2_raw_n7": float(raw7[idx]),
                    "cond_G_amp_n7": float(cond7[idx]),
                    "rho_R2_n8": float(rho8[idx]),
                    "rho_R2_raw_n8": float(raw8[idx]),
                    "cond_G_amp_n8": float(cond8[idx]),
                    "gap_rho_R2_n8_minus_n7": float(gap_n8_minus_n7[idx]),
                    "advantage_n8_minus_n7": float(advantage_n8[idx]),
                    "normalized_advantage_n8_minus_n7": float(normalized_advantage_n8[idx]),
                    "cumulative_signed_area_n8_minus_n7": float(cumulative_signed_area[idx]),
                    "cumulative_abs_area": float(cumulative_abs_area[idx]),
                    "preferred_mode_on_common_grid": winner_from_signed_value(float(advantage_n8[idx]), positive_means_n8=True),
                }
            )

        table_rows.append(
            {
                "setting": str(setting["label"]),
                "m_basis": int(setting["m_basis"]),
                "n_collocation": int(setting["n_collocation"]),
                "nd_base": int(setting["nd_base"]),
                "best_n7_q_mpa": float(best7["q_mpa"]),
                "best_n7_rho_R2": float(best7["rho_R2"]),
                "best_n8_q_mpa": float(best8["q_mpa"]),
                "best_n8_rho_R2": float(best8["rho_R2"]),
                "pointwise_gap_n8_minus_n7": pointwise_gap,
                "pointwise_winner": pointwise_winner,
                "valley_width_rel10_n7_mpa": float(valley_threshold_summaries["rel_10"]["n7"]["width_mpa"]),
                "valley_width_rel10_n8_mpa": float(valley_threshold_summaries["rel_10"]["n8"]["width_mpa"]),
                "valley_width_rel10_winner": str(valley_threshold_summaries["rel_10"]["winner"]),
                "valley_width_rel25_n7_mpa": float(valley_threshold_summaries["rel_25"]["n7"]["width_mpa"]),
                "valley_width_rel25_n8_mpa": float(valley_threshold_summaries["rel_25"]["n8"]["width_mpa"]),
                "valley_width_rel25_winner": str(valley_threshold_summaries["rel_25"]["winner"]),
                "valley_width_rel50_n7_mpa": float(valley_threshold_summaries["rel_50"]["n7"]["width_mpa"]),
                "valley_width_rel50_n8_mpa": float(valley_threshold_summaries["rel_50"]["n8"]["width_mpa"]),
                "valley_width_rel50_winner": str(valley_threshold_summaries["rel_50"]["winner"]),
                "signed_area_n8_minus_n7": signed_area_n8,
                "absolute_area": abs_area,
                "normalized_signed_area": normalized_signed_area,
                "mean_normalized_advantage": mean_normalized_advantage,
                "signed_area_winner": signed_area_winner,
                "ahead_fraction_n8": float(persistence["n8_ahead_fraction"]),
                "ahead_fraction_n7": float(persistence["n7_ahead_fraction"]),
                "ahead_fraction_winner": str(persistence["ahead_fraction_winner"]),
                "longest_interval_n8_mpa": float(persistence["n8_longest_interval"]["length_mpa"]),
                "longest_interval_n7_mpa": float(persistence["n7_longest_interval"]["length_mpa"]),
                "longest_interval_winner": str(persistence["longest_interval_winner"]),
                "sign_change_count": int(persistence["sign_change_count"]),
                "relative_curvature_n7": float(shape7["relative_curvature"]),
                "relative_curvature_n8": float(shape8["relative_curvature"]),
                "relative_curvature_winner": curvature_winner,
            }
        )
    pointwise_labels = [str(row["pointwise_winner"]) for row in table_rows]
    area_labels = [str(row["signed_area_winner"]) for row in table_rows]
    ahead_fraction_labels = [str(row["ahead_fraction_winner"]) for row in table_rows]
    longest_labels = [str(row["longest_interval_winner"]) for row in table_rows]
    valley25_labels = [str(row["valley_width_rel25_winner"]) for row in table_rows]
    curvature_labels = [str(row["relative_curvature_winner"]) for row in table_rows]

    core_metric_majorities = {
        "signed_area": pairwise_count_summary(area_labels),
        "ahead_fraction": pairwise_count_summary(ahead_fraction_labels),
        "longest_interval": pairwise_count_summary(longest_labels),
        "valley_width_rel25": pairwise_count_summary(valley25_labels),
    }
    majority_set = {str(item["majority"]) for item in core_metric_majorities.values()}
    if majority_set == {"n8"}:
        decision = "A"
    elif majority_set == {"n7"}:
        decision = "B"
    else:
        decision = "C"

    summary["metric_stability_comparison"] = {
        "pointwise_minimum": pairwise_count_summary(pointwise_labels),
        "signed_area": core_metric_majorities["signed_area"],
        "ahead_fraction": core_metric_majorities["ahead_fraction"],
        "longest_interval": core_metric_majorities["longest_interval"],
        "valley_width_rel10": pairwise_count_summary([str(row["valley_width_rel10_winner"]) for row in table_rows]),
        "valley_width_rel25": core_metric_majorities["valley_width_rel25"],
        "valley_width_rel50": pairwise_count_summary([str(row["valley_width_rel50_winner"]) for row in table_rows]),
        "relative_curvature": pairwise_count_summary(curvature_labels),
        "decision_rule_note": (
            "Decision A or B requires the broader/persistent core metrics (signed area, ahead fraction, longest interval, and 25% valley width) "
            "to have aligned cross-setting majorities. Otherwise the pair is treated as unresolved."
        ),
        "decision": decision,
    }

    summary["pair_resolution_summary"] = {
        "signed_area_n8_minus_n7": value_summary([float(row["signed_area_n8_minus_n7"]) for row in table_rows]),
        "absolute_area": value_summary([float(row["absolute_area"]) for row in table_rows]),
        "mean_normalized_advantage": value_summary([float(row["mean_normalized_advantage"]) for row in table_rows]),
        "ahead_fraction_n8": value_summary([float(row["ahead_fraction_n8"]) for row in table_rows]),
        "longest_interval_n8_mpa": value_summary([float(row["longest_interval_n8_mpa"]) for row in table_rows]),
        "longest_interval_n7_mpa": value_summary([float(row["longest_interval_n7_mpa"]) for row in table_rows]),
        "decision": decision,
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
        "best_n8_q_mpa",
        "best_n8_rho_R2",
        "pointwise_gap_n8_minus_n7",
        "pointwise_winner",
        "valley_width_rel10_n7_mpa",
        "valley_width_rel10_n8_mpa",
        "valley_width_rel10_winner",
        "valley_width_rel25_n7_mpa",
        "valley_width_rel25_n8_mpa",
        "valley_width_rel25_winner",
        "valley_width_rel50_n7_mpa",
        "valley_width_rel50_n8_mpa",
        "valley_width_rel50_winner",
        "signed_area_n8_minus_n7",
        "absolute_area",
        "normalized_signed_area",
        "mean_normalized_advantage",
        "signed_area_winner",
        "ahead_fraction_n8",
        "ahead_fraction_n7",
        "ahead_fraction_winner",
        "longest_interval_n8_mpa",
        "longest_interval_n7_mpa",
        "longest_interval_winner",
        "sign_change_count",
        "relative_curvature_n7",
        "relative_curvature_n8",
        "relative_curvature_winner",
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
        "advantage_n8_minus_n7",
        "normalized_advantage_n8_minus_n7",
        "cumulative_signed_area_n8_minus_n7",
        "cumulative_abs_area",
        "preferred_mode_on_common_grid",
    ]
    with CURVES_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=curve_columns)
        writer.writeheader()
        writer.writerows(curve_rows_all)
    print("=== Criterion pilot R2 pair-resolution study complete ===")
    print("\n=== Core metric winners by setting ===")
    for row in table_rows:
        print(
            f"{row['setting']}: "
            f"pointwise={row['pointwise_winner']} | "
            f"area={row['signed_area_winner']} | "
            f"ahead_fraction={row['ahead_fraction_winner']} | "
            f"longest={row['longest_interval_winner']} | "
            f"valley25={row['valley_width_rel25_winner']}"
        )

    print("\n=== Pair-resolution conclusion code ===")
    print(f"decision={summary['metric_stability_comparison']['decision']}")
    print(f"summary json: {SUMMARY_JSON}")
    print(f"summary csv:  {SUMMARY_CSV}")
    print(f"curves csv:   {CURVES_CSV}")
    print(f"runtime:      {summary['runtime_seconds']:.2f} s")


if __name__ == "__main__":
    main()