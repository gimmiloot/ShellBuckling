# -*- coding: utf-8 -*-
# Purpose:
#   Run a narrow selected-family sensitivity audit for the clean full
#   simple-support path without changing equations, BC meaning, or solver behavior.
# Typical use:
#   .venv\Scripts\python.exe tasks\run_simple_support_selected_family_sensitivity.py
# Outputs:
#   output/clean_full_simple_support/selected_family_sensitivity_summary.json
#   output/clean_full_simple_support/selected_family_sensitivity_table.csv
#   output/clean_full_simple_support/selected_family_sensitivity_curves.csv

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

from shell_buckling.mixed_weak import _core_reduction as red
from shell_buckling.mixed_weak import axisymmetric_simple_support_background as simple_bg
from shell_buckling.mixed_weak import full_simple_support_critical_search as full_search
from shell_buckling.mixed_weak import simple_support_high_load_background_continuation as high_bg


OUTPUT_DIR = REPO_ROOT / "output" / "clean_full_simple_support"
SUMMARY_JSON = OUTPUT_DIR / "selected_family_sensitivity_summary.json"
SUMMARY_CSV = OUTPUT_DIR / "selected_family_sensitivity_table.csv"
CURVES_CSV = OUTPUT_DIR / "selected_family_sensitivity_curves.csv"

PAIR_MODES = (7, 8)
COMMON_WINDOW = {"q_min": 17.20, "q_max": 17.70, "npts": 201}
LOCAL_WINDOWS: dict[int, dict[str, float]] = {
    7: {"q_min": 17.20, "q_max": 17.50},
    8: {"q_min": 17.35, "q_max": 17.70},
}
BASE_SETTING = {"m_basis": 6, "n_collocation": 120, "nd_base": 4000}
AMP_INJECTION = np.array(
    [
        [1.0, 0.0],
        [0.0, 1.0],
        [0.0, 0.0],
        [0.0, 0.0],
    ],
    dtype=float,
)
VARIANTS: tuple[dict[str, object], ...] = (
    {
        "label": "baseline_current",
        "family_group": "baseline",
        "recipe": "current",
        "reg": 1.0e-12,
        "description": "Current normalized-then-orthogonalized two-mode selection.",
        "expected_same_family_as_baseline": True,
    },
    {
        "label": "repr_no_orthog",
        "family_group": "representation",
        "recipe": "no_orthog",
        "reg": 1.0e-12,
        "description": "Same regularized amplitude solves, but without the extra orthogonalization step.",
        "expected_same_family_as_baseline": True,
    },
    {
        "label": "repr_reverse_orthog",
        "family_group": "representation",
        "recipe": "reverse_orthog",
        "reg": 1.0e-12,
        "description": "Same regularized amplitude solves with the orthogonalization order reversed.",
        "expected_same_family_as_baseline": True,
    },
    {
        "label": "repr_kkt_direct",
        "family_group": "representation",
        "recipe": "kkt_direct",
        "reg": 1.0e-12,
        "description": "Direct two-right-hand-side KKT amplitude family before any normalization or orthogonalization.",
        "expected_same_family_as_baseline": True,
    },
    {
        "label": "reg_down_current",
        "family_group": "selection",
        "recipe": "current",
        "reg": 3.0e-13,
        "description": "Current recipe with a smaller KKT regularization.",
        "expected_same_family_as_baseline": False,
    },
    {
        "label": "reg_up_current",
        "family_group": "selection",
        "recipe": "current",
        "reg": 3.0e-12,
        "description": "Current recipe with a larger KKT regularization.",
        "expected_same_family_as_baseline": False,
    },
)
MAX_BOOTSTRAP_STEP_MPA = 0.5
EPS = 1.0e-30
TARGET_CENTER_BLOCK = np.array(
    [
        [1.0, 0.0],
        [0.0, 1.0],
        [0.0, 0.0],
        [0.0, 0.0],
    ],
    dtype=float,
)


def make_grid(q_min: float, q_max: float, npts: int) -> np.ndarray:
    return np.linspace(float(q_min), float(q_max), int(npts), dtype=float)


def condition_number(A: np.ndarray) -> float:
    singular_values = np.linalg.svd(np.asarray(A, dtype=float), compute_uv=False)
    if singular_values.size == 0:
        return float("nan")
    if singular_values[-1] <= EPS:
        return float("inf")
    return float(singular_values[0] / singular_values[-1])


def smallest_singular_value(A: np.ndarray) -> float:
    return float(np.linalg.svd(np.asarray(A, dtype=float), compute_uv=False)[-1])


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

def solve_constrained_family(A: np.ndarray, C: np.ndarray, D: np.ndarray, reg: float) -> np.ndarray:
    n_unknowns = A.shape[1]
    n_constraints = C.shape[0]
    ATA = A.T @ A + float(reg) * np.eye(n_unknowns, dtype=float)
    KKT = np.block(
        [
            [ATA, C.T],
            [C, np.zeros((n_constraints, n_constraints), dtype=float)],
        ]
    )
    rhs = np.vstack([np.zeros((n_unknowns, D.shape[1]), dtype=float), np.asarray(D, dtype=float)])
    sol = np.linalg.solve(KKT, rhs)
    return np.asarray(sol[:n_unknowns, :], dtype=float)


def build_vreg(A_int: np.ndarray, C_center: np.ndarray, variant: dict[str, object]) -> np.ndarray:
    reg = float(variant["reg"])
    recipe = str(variant["recipe"])
    d1 = AMP_INJECTION[:, 0]
    d2 = AMP_INJECTION[:, 1]

    if recipe == "current":
        c1 = red.solve_constrained_mode(A_int, C_center, d1, reg=reg)
        c2_raw = red.solve_constrained_mode(A_int, C_center, d2, reg=reg)
        c2 = red.orthogonalize_against(c2_raw, c1)
        return np.column_stack([c1, c2])
    if recipe == "no_orthog":
        c1 = red.solve_constrained_mode(A_int, C_center, d1, reg=reg)
        c2 = red.solve_constrained_mode(A_int, C_center, d2, reg=reg)
        return np.column_stack([c1, c2])
    if recipe == "reverse_orthog":
        c2 = red.solve_constrained_mode(A_int, C_center, d2, reg=reg)
        c1_raw = red.solve_constrained_mode(A_int, C_center, d1, reg=reg)
        c1 = red.orthogonalize_against(c1_raw, c2)
        return np.column_stack([c1, c2])
    if recipe == "kkt_direct":
        return solve_constrained_family(A_int, C_center, AMP_INJECTION, reg=reg)
    raise ValueError(f"Unknown selected-family recipe: {recipe}")


def best_row_in_window(rows: list[dict[str, object]], *, q_min: float, q_max: float) -> dict[str, object]:
    window_rows = [
        row for row in rows
        if float(q_min) - 1.0e-12 <= float(row["q_mpa"]) <= float(q_max) + 1.0e-12
    ]
    if not window_rows:
        raise RuntimeError(f"No points found in local window {q_min:.6f} .. {q_max:.6f} MPa.")
    return min(window_rows, key=lambda row: (float(row["rho_R2"]), float(row["q_mpa"])))


def winner_from_advantage(value: float) -> str:
    if not np.isfinite(value) or abs(value) <= EPS:
        return "tie"
    return "n8" if value > 0.0 else "n7"


def collect_sign_segments(q: np.ndarray, values: np.ndarray, *, positive: bool) -> list[tuple[float, float, float]]:
    if q.size < 2:
        return []
    segments: list[tuple[float, float, float]] = []
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
            if abs(v_right - v_left) <= EPS:
                crossing = 0.5 * (q_left + q_right)
            else:
                crossing = q_left + (0.0 - v_left) * (q_right - q_left) / (v_right - v_left)
            if current_start is None:
                current_start = q_left
            segments.append((float(current_start), float(crossing), float(max(crossing - current_start, 0.0))))
            current_start = None
        elif (not active_left) and active_right:
            if abs(v_right - v_left) <= EPS:
                current_start = 0.5 * (q_left + q_right)
            else:
                current_start = q_left + (0.0 - v_left) * (q_right - q_left) / (v_right - v_left)

    tail = float(values[-1])
    tail_active = tail > 0.0 if positive else tail < 0.0
    if tail_active:
        if current_start is None:
            current_start = float(q[-1])
        segments.append((float(current_start), float(q[-1]), float(max(float(q[-1]) - current_start, 0.0))))
    return segments


def orthonormal_projector(V: np.ndarray) -> np.ndarray:
    Q, _ = np.linalg.qr(np.asarray(V, dtype=float), mode="reduced")
    return Q @ Q.T


def build_variant_object(
    *,
    mode: int,
    q_mpa: float,
    base,
    space,
    A_int: np.ndarray,
    B_full: np.ndarray,
    C_center: np.ndarray,
    variant: dict[str, object],
    baseline_reference: dict[str, np.ndarray] | None,
) -> dict[str, object]:
    C_amp = np.asarray(C_center[:2, :], dtype=float)
    C_reg = np.asarray(C_center[2:, :], dtype=float)
    V_reg = build_vreg(A_int, C_center, variant)
    G_amp = C_amp @ V_reg
    V_adm = V_reg @ np.linalg.inv(G_amp)
    B_red = B_full @ V_adm
    B_mix = B_red @ G_amp
    B_bal = full_search.balanced_Bmix(B_mix)
    W_B = np.diag(full_search.ROW_SCALE**2)
    G_R2 = V_adm.T @ (A_int.T @ A_int + B_full.T @ W_B @ B_full) @ V_adm
    G_R2 = 0.5 * (G_R2 + G_R2.T)
    rho_R2_raw = float(np.linalg.eigvalsh(G_R2)[0])
    rho_R2 = float(np.sqrt(max(rho_R2_raw, 0.0)))

    projector = orthonormal_projector(V_adm)
    if baseline_reference is None:
        vadm_diff = 0.0
        projector_diff = 0.0
    else:
        vadm_diff = float(np.linalg.norm(V_adm - baseline_reference["V_adm"], ord="fro"))
        projector_diff = float(np.linalg.norm(projector - baseline_reference["projector"], ord="fro"))

    return {
        "n": int(mode),
        "q_mpa": float(q_mpa),
        "base": base,
        "space": space,
        "A_int": A_int,
        "B_full": B_full,
        "C_center": C_center,
        "C_amp": C_amp,
        "C_reg": C_reg,
        "V_reg": V_reg,
        "G_amp": G_amp,
        "V_adm": V_adm,
        "B_red": B_red,
        "B_mix": B_mix,
        "rho_R2": rho_R2,
        "rho_R2_raw": rho_R2_raw,
        "sigma_Bred_bal": smallest_singular_value(full_search.balanced_Bmix(B_red)),
        "cond_G_amp": condition_number(G_amp),
        "center_identity_residual": float(np.max(np.abs(C_center @ V_adm - TARGET_CENTER_BLOCK))),
        "amp_identity_residual": float(np.max(np.abs(C_amp @ V_adm - np.eye(2, dtype=float)))),
        "reg_identity_residual": float(np.max(np.abs(C_reg @ V_adm))),
        "vadm_diff_fro_to_baseline": vadm_diff,
        "projector_diff_fro_to_baseline": projector_diff,
        "projector": projector,
    }

def main() -> None:
    start_time = time.time()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    background_config = high_bg.default_high_load_background_config()
    common_grid = make_grid(
        float(COMMON_WINDOW["q_min"]),
        float(COMMON_WINDOW["q_max"]),
        int(COMMON_WINDOW["npts"]),
    )
    backgrounds, background_method = solve_window_backgrounds(common_grid, config=background_config)

    assembly_cache: dict[tuple[int, float], dict[str, object]] = {}
    for mode in PAIR_MODES:
        for q_mpa, background in zip(common_grid, backgrounds):
            base = full_search.build_full_simple_support_base_interp(
                background.solution,
                q_mpa=float(q_mpa),
                nd_base=int(BASE_SETTING["nd_base"]),
            )
            space, _x_col, A_int, B_full = full_search.assemble_interior_and_boundary(
                n=int(mode),
                base=base,
                x0=float(background_config.x0),
                m_basis=int(BASE_SETTING["m_basis"]),
                n_collocation=int(BASE_SETTING["n_collocation"]),
            )
            C_center = full_search.make_center_constraint_matrix(space, base)
            assembly_cache[(int(mode), float(q_mpa))] = {
                "base": base,
                "space": space,
                "A_int": A_int,
                "B_full": B_full,
                "C_center": C_center,
            }

    baseline_variant = VARIANTS[0]
    baseline_reference: dict[tuple[int, float], dict[str, np.ndarray]] = {}
    baseline_rows_by_mode: dict[int, list[dict[str, object]]] = {int(mode): [] for mode in PAIR_MODES}
    for mode in PAIR_MODES:
        for q_mpa in common_grid:
            assembly = assembly_cache[(int(mode), float(q_mpa))]
            obj = build_variant_object(
                mode=int(mode),
                q_mpa=float(q_mpa),
                base=assembly["base"],
                space=assembly["space"],
                A_int=np.asarray(assembly["A_int"], dtype=float),
                B_full=np.asarray(assembly["B_full"], dtype=float),
                C_center=np.asarray(assembly["C_center"], dtype=float),
                variant=baseline_variant,
                baseline_reference=None,
            )
            baseline_reference[(int(mode), float(q_mpa))] = {
                "V_adm": np.asarray(obj["V_adm"], dtype=float),
                "projector": np.asarray(obj["projector"], dtype=float),
            }
            baseline_rows_by_mode[int(mode)].append(obj)

    summary: dict[str, object] = {
        "method_note": (
            "Selected-family sensitivity audit on the clean full simple-support path. "
            "The equations, BC meaning, and solver behavior are unchanged. "
            "The pass varies only the selected-family construction used before canonical rebasing and compares the resulting n=7/n=8 stacked diagnostics on the same dense local window."
        ),
        "background_config": dict(background_config.__dict__),
        "background_method": background_method,
        "base_setting": dict(BASE_SETTING),
        "common_window": COMMON_WINDOW,
        "local_windows": LOCAL_WINDOWS,
        "pair_modes": list(PAIR_MODES),
        "variants": [dict(item) for item in VARIANTS],
        "variant_summaries": {},
    }

    table_rows: list[dict[str, object]] = []
    curve_rows: list[dict[str, object]] = []

    baseline_summary_row: dict[str, object] | None = None

    for variant in VARIANTS:
        rows_by_mode: dict[int, list[dict[str, object]]] = {int(mode): [] for mode in PAIR_MODES}
        for mode in PAIR_MODES:
            if str(variant["label"]) == "baseline_current":
                rows_by_mode[int(mode)] = list(baseline_rows_by_mode[int(mode)])
            else:
                for q_mpa in common_grid:
                    assembly = assembly_cache[(int(mode), float(q_mpa))]
                    obj = build_variant_object(
                        mode=int(mode),
                        q_mpa=float(q_mpa),
                        base=assembly["base"],
                        space=assembly["space"],
                        A_int=np.asarray(assembly["A_int"], dtype=float),
                        B_full=np.asarray(assembly["B_full"], dtype=float),
                        C_center=np.asarray(assembly["C_center"], dtype=float),
                        variant=variant,
                        baseline_reference=baseline_reference[(int(mode), float(q_mpa))],
                    )
                    rows_by_mode[int(mode)].append(obj)

        rows7 = rows_by_mode[7]
        rows8 = rows_by_mode[8]
        best7 = best_row_in_window(rows7, q_min=float(LOCAL_WINDOWS[7]["q_min"]), q_max=float(LOCAL_WINDOWS[7]["q_max"]))
        best8 = best_row_in_window(rows8, q_min=float(LOCAL_WINDOWS[8]["q_min"]), q_max=float(LOCAL_WINDOWS[8]["q_max"]))

        q = np.asarray([float(row["q_mpa"]) for row in rows7], dtype=float)
        rho7 = np.asarray([float(row["rho_R2"]) for row in rows7], dtype=float)
        rho8 = np.asarray([float(row["rho_R2"]) for row in rows8], dtype=float)
        cond7 = np.asarray([float(row["cond_G_amp"]) for row in rows7], dtype=float)
        cond8 = np.asarray([float(row["cond_G_amp"]) for row in rows8], dtype=float)
        diff7 = np.asarray([float(row["projector_diff_fro_to_baseline"]) for row in rows7], dtype=float)
        diff8 = np.asarray([float(row["projector_diff_fro_to_baseline"]) for row in rows8], dtype=float)
        vadm7 = np.asarray([float(row["vadm_diff_fro_to_baseline"]) for row in rows7], dtype=float)
        vadm8 = np.asarray([float(row["vadm_diff_fro_to_baseline"]) for row in rows8], dtype=float)

        advantage_n8 = rho7 - rho8
        signed_area_n8 = float(np.trapezoid(advantage_n8, q))
        absolute_area = float(np.trapezoid(np.abs(advantage_n8), q))
        n8_segments = collect_sign_segments(q, advantage_n8, positive=True)
        n7_segments = collect_sign_segments(q, advantage_n8, positive=False)
        window_length = float(q[-1] - q[0])
        n8_ahead_fraction = float(sum(item[2] for item in n8_segments) / max(window_length, EPS))
        n7_ahead_fraction = float(sum(item[2] for item in n7_segments) / max(window_length, EPS))
        n8_longest = float(max((item[2] for item in n8_segments), default=0.0))
        n7_longest = float(max((item[2] for item in n7_segments), default=0.0))
        pointwise_gap = float(best8["rho_R2"] - best7["rho_R2"])

        pointwise_winner = winner_from_advantage(-pointwise_gap)
        signed_area_winner = winner_from_advantage(signed_area_n8)
        ahead_fraction_winner = "n8" if n8_ahead_fraction > n7_ahead_fraction else "n7" if n7_ahead_fraction > n8_ahead_fraction else "tie"
        longest_winner = "n8" if n8_longest > n7_longest else "n7" if n7_longest > n8_longest else "tie"

        for idx, q_mpa in enumerate(q):
            curve_rows.append(
                {
                    "variant": str(variant["label"]),
                    "family_group": str(variant["family_group"]),
                    "reg": float(variant["reg"]),
                    "q_mpa": float(q_mpa),
                    "rho_R2_n7": float(rho7[idx]),
                    "rho_R2_n8": float(rho8[idx]),
                    "advantage_n8_minus_n7": float(advantage_n8[idx]),
                    "cond_G_amp_n7": float(cond7[idx]),
                    "cond_G_amp_n8": float(cond8[idx]),
                    "projector_diff_n7": float(diff7[idx]),
                    "projector_diff_n8": float(diff8[idx]),
                    "vadm_diff_n7": float(vadm7[idx]),
                    "vadm_diff_n8": float(vadm8[idx]),
                }
            )
        row = {
            "variant": str(variant["label"]),
            "family_group": str(variant["family_group"]),
            "reg": float(variant["reg"]),
            "expected_same_family_as_baseline": bool(variant["expected_same_family_as_baseline"]),
            "best_n7_q_mpa": float(best7["q_mpa"]),
            "best_n7_rho_R2": float(best7["rho_R2"]),
            "best_n7_cond_G_amp": float(best7["cond_G_amp"]),
            "best_n8_q_mpa": float(best8["q_mpa"]),
            "best_n8_rho_R2": float(best8["rho_R2"]),
            "best_n8_cond_G_amp": float(best8["cond_G_amp"]),
            "pointwise_gap_n8_minus_n7": pointwise_gap,
            "pointwise_winner": pointwise_winner,
            "signed_area_n8_minus_n7": signed_area_n8,
            "absolute_area": absolute_area,
            "signed_area_winner": signed_area_winner,
            "ahead_fraction_n8": n8_ahead_fraction,
            "ahead_fraction_n7": n7_ahead_fraction,
            "ahead_fraction_winner": ahead_fraction_winner,
            "longest_interval_n8_mpa": n8_longest,
            "longest_interval_n7_mpa": n7_longest,
            "longest_interval_winner": longest_winner,
            "mean_projector_diff_n7": float(np.mean(diff7)),
            "max_projector_diff_n7": float(np.max(diff7)),
            "mean_projector_diff_n8": float(np.mean(diff8)),
            "max_projector_diff_n8": float(np.max(diff8)),
            "mean_vadm_diff_n7": float(np.mean(vadm7)),
            "max_vadm_diff_n7": float(np.max(vadm7)),
            "mean_vadm_diff_n8": float(np.mean(vadm8)),
            "max_vadm_diff_n8": float(np.max(vadm8)),
            "max_center_identity_residual": float(max(max(float(r["center_identity_residual"]) for r in rows7), max(float(r["center_identity_residual"]) for r in rows8))),
            "max_reg_identity_residual": float(max(max(float(r["reg_identity_residual"]) for r in rows7), max(float(r["reg_identity_residual"]) for r in rows8))),
            "max_cond_G_amp": float(max(np.max(cond7), np.max(cond8))),
        }
        table_rows.append(row)
        if baseline_summary_row is None:
            baseline_summary_row = row

        summary["variant_summaries"][str(variant["label"])] = {
            "description": str(variant["description"]),
            "family_group": str(variant["family_group"]),
            "reg": float(variant["reg"]),
            "pointwise": {
                "best_n7": {"q_mpa": float(best7["q_mpa"]), "rho_R2": float(best7["rho_R2"]), "cond_G_amp": float(best7["cond_G_amp"])} ,
                "best_n8": {"q_mpa": float(best8["q_mpa"]), "rho_R2": float(best8["rho_R2"]), "cond_G_amp": float(best8["cond_G_amp"])} ,
                "gap_n8_minus_n7": pointwise_gap,
                "winner": pointwise_winner,
            },
            "common_window": {
                "signed_area_n8_minus_n7": signed_area_n8,
                "absolute_area": absolute_area,
                "signed_area_winner": signed_area_winner,
                "ahead_fraction_n8": n8_ahead_fraction,
                "ahead_fraction_n7": n7_ahead_fraction,
                "ahead_fraction_winner": ahead_fraction_winner,
                "longest_interval_n8_mpa": n8_longest,
                "longest_interval_n7_mpa": n7_longest,
                "longest_interval_winner": longest_winner,
            },
            "similarity_to_baseline": {
                "mean_projector_diff_n7": float(np.mean(diff7)),
                "max_projector_diff_n7": float(np.max(diff7)),
                "mean_projector_diff_n8": float(np.mean(diff8)),
                "max_projector_diff_n8": float(np.max(diff8)),
                "mean_vadm_diff_n7": float(np.mean(vadm7)),
                "max_vadm_diff_n7": float(np.max(vadm7)),
                "mean_vadm_diff_n8": float(np.mean(vadm8)),
                "max_vadm_diff_n8": float(np.max(vadm8)),
            },
            "identity_checks": {
                "max_center_identity_residual": row["max_center_identity_residual"],
                "max_reg_identity_residual": row["max_reg_identity_residual"],
            },
        }

    selection_rows = [row for row in table_rows if str(row["family_group"]) in ("baseline", "selection")]
    pointwise_labels = [str(row["pointwise_winner"]) for row in selection_rows]
    area_labels = [str(row["signed_area_winner"]) for row in selection_rows]
    ahead_labels = [str(row["ahead_fraction_winner"]) for row in selection_rows]
    longest_labels = [str(row["longest_interval_winner"]) for row in selection_rows]

    nonbaseline_selection_rows = [row for row in table_rows if str(row["family_group"]) == "selection"]
    selection_flips = [
        str(row["variant"]) for row in nonbaseline_selection_rows
        if str(row["pointwise_winner"]) != str(baseline_summary_row["pointwise_winner"])
        or str(row["signed_area_winner"]) != str(baseline_summary_row["signed_area_winner"])
        or str(row["ahead_fraction_winner"]) != str(baseline_summary_row["ahead_fraction_winner"])
    ]

    if selection_flips:
        decision = "B"
        conclusion = "ambiguity is strongly selection-layer-sensitive and the current selected family is not stable enough for criterion conclusions"
    else:
        aligned_variant = next(
            (
                row for row in nonbaseline_selection_rows
                if len({str(row["pointwise_winner"]), str(row["signed_area_winner"]), str(row["ahead_fraction_winner"]), str(row["longest_interval_winner"])}) == 1
                and str(row["pointwise_winner"]) in ("n7", "n8")
            ),
            None,
        )
        if aligned_variant is not None:
            decision = "C"
            conclusion = (
                "one nearby selected-family construction gives a substantially more coherent stacked reading and deserves follow-up"
            )
        else:
            decision = "A"
            conclusion = (
                "ambiguity persists across nearby selected-family constructions and still looks mostly metric-level rather than tied to one specific selected-family recipe"
            )

    summary["selection_family_comparison"] = {
        "selection_variants": [str(row["variant"]) for row in selection_rows],
        "pointwise_winners": pointwise_labels,
        "signed_area_winners": area_labels,
        "ahead_fraction_winners": ahead_labels,
        "longest_interval_winners": longest_labels,
        "selection_flips_relative_to_baseline": selection_flips,
        "decision": decision,
        "conclusion": conclusion,
    }
    summary["runtime_seconds"] = float(time.time() - start_time)

    with SUMMARY_JSON.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False, allow_nan=True)
        fh.write("\n")

    columns = [
        "variant",
        "family_group",
        "reg",
        "expected_same_family_as_baseline",
        "best_n7_q_mpa",
        "best_n7_rho_R2",
        "best_n7_cond_G_amp",
        "best_n8_q_mpa",
        "best_n8_rho_R2",
        "best_n8_cond_G_amp",
        "pointwise_gap_n8_minus_n7",
        "pointwise_winner",
        "signed_area_n8_minus_n7",
        "absolute_area",
        "signed_area_winner",
        "ahead_fraction_n8",
        "ahead_fraction_n7",
        "ahead_fraction_winner",
        "longest_interval_n8_mpa",
        "longest_interval_n7_mpa",
        "longest_interval_winner",
        "mean_projector_diff_n7",
        "max_projector_diff_n7",
        "mean_projector_diff_n8",
        "max_projector_diff_n8",
        "mean_vadm_diff_n7",
        "max_vadm_diff_n7",
        "mean_vadm_diff_n8",
        "max_vadm_diff_n8",
        "max_center_identity_residual",
        "max_reg_identity_residual",
        "max_cond_G_amp",
    ]
    with SUMMARY_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns)
        writer.writeheader()
        writer.writerows(table_rows)

    curve_columns = [
        "variant",
        "family_group",
        "reg",
        "q_mpa",
        "rho_R2_n7",
        "rho_R2_n8",
        "advantage_n8_minus_n7",
        "cond_G_amp_n7",
        "cond_G_amp_n8",
        "projector_diff_n7",
        "projector_diff_n8",
        "vadm_diff_n7",
        "vadm_diff_n8",
    ]
    with CURVES_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=curve_columns)
        writer.writeheader()
        writer.writerows(curve_rows)

    print("=== Selected-family sensitivity audit complete ===")
    for row in table_rows:
        print(
            f"{row['variant']}: pointwise={row['pointwise_winner']} gap={row['pointwise_gap_n8_minus_n7']:.6e} | "
            f"area={row['signed_area_winner']} {row['signed_area_n8_minus_n7']:.6e} | "
            f"ahead_fraction={row['ahead_fraction_winner']} ({row['ahead_fraction_n8']:.3f}) | "
            f"longest={row['longest_interval_winner']} | maxProjDiff={max(row['max_projector_diff_n7'], row['max_projector_diff_n8']):.3e}"
        )
    print("decision: " + decision)
    print("conclusion: " + conclusion)
    print(f"summary json: {SUMMARY_JSON}")
    print(f"summary csv:  {SUMMARY_CSV}")
    print(f"curves csv:   {CURVES_CSV}")
    print(f"runtime:      {summary['runtime_seconds']:.2f} s")


if __name__ == "__main__":
    main()