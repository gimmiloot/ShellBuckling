# -*- coding: utf-8 -*-
# Purpose:
#   Run the clean full simple support / podvizhnyi sharnir criterion pilot E
#   on the current competition set without changing the main solver path.
# Typical use:
#   .venv\Scripts\python.exe tasks\run_simple_support_criterion_pilot_e.py
# Outputs:
#   output/clean_full_simple_support/criterion_pilot_e_*.{json,csv}

from __future__ import annotations

import csv
import json
import time
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import cholesky, solve_triangular


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.mixed_weak import axisymmetric_simple_support_background as simple_bg
from shell_buckling.mixed_weak import full_simple_support_critical_search as full_search
from shell_buckling.mixed_weak import simple_support_high_load_background_continuation as high_bg
from shell_buckling.mixed_weak import solver_patched_core as mw


OUTPUT_DIR = REPO_ROOT / "output" / "clean_full_simple_support"
SUMMARY_JSON = OUTPUT_DIR / "criterion_pilot_e_summary.json"
SUMMARY_CSV = OUTPUT_DIR / "criterion_pilot_e_table.csv"
POINTS_CSV = OUTPUT_DIR / "criterion_pilot_e_points.csv"

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
E_BUNDLE_RADIUS = 1
EVAL_NX = 161
EDGE_X_MIN = 0.85
MAX_BOOTSTRAP_STEP_MPA = 0.5
EPS = 1.0e-30

CHANNEL_SPECS: tuple[tuple[str, float], ...] = (
    ("e_s", 1.0),
    ("e_theta", 1.0),
    ("gamma_theta", 1.0),
    ("S", 2.0 * (1.0 + mw.nu)),
    ("phi_x", 1.0),
    ("kappa_theta_new", 1.0),
    ("H", float(np.sqrt(mw.C_twist))),
)


def make_grid(q_min: float, q_max: float, npts: int) -> np.ndarray:
    return np.linspace(float(q_min), float(q_max), int(npts), dtype=float)


def integrate_curve(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.trapezoid(np.asarray(y, dtype=float), np.asarray(x, dtype=float)))


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


def residual_reading_class(boundary_share: float) -> str:
    if float(boundary_share) <= 0.05:
        return "interior-dominated"
    if float(boundary_share) <= 0.50:
        return "mixed interior/boundary"
    return "boundary-dominated"


def concentration_class(edge_share: float) -> str:
    if float(edge_share) <= 0.15:
        return "interior-distributed"
    if float(edge_share) <= 0.35:
        return "mixed interior/edge"
    return "edge-concentrated"


def peak_class(peak_x: float) -> str:
    if float(peak_x) >= 0.90:
        return "edge-peaked"
    if float(peak_x) <= 0.75:
        return "interior-peaked"
    return "transition-peaked"


def stability_class(*, all_interior: bool, q_drift_mpa: float, value_ratio: float) -> str:
    if all_interior and q_drift_mpa <= 0.08 and value_ratio <= 4.0:
        return "stable"
    if all_interior and q_drift_mpa <= 0.18 and value_ratio <= 12.0:
        return "moderate"
    return "unstable"


def aggregate_residual_class(classes: list[str]) -> str:
    if all(item == "interior-dominated" for item in classes):
        return "interior-dominated"
    if all(item == "boundary-dominated" for item in classes):
        return "boundary-dominated"
    return "mixed"


def aggregate_concentration_class(classes: list[str]) -> str:
    if all(item == "interior-distributed" for item in classes):
        return "interior-distributed"
    if all(item == "edge-concentrated" for item in classes):
        return "edge-concentrated"
    return "mixed"


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

def extra_channel(name: str, vals: dict[str, np.ndarray]) -> np.ndarray:
    if name == "gamma_theta":
        return vals["b_m"] * vals["u_n"] + vals["lambda_theta0"] * vals["psi"] - vals["kappa_theta0"] * vals["v"]
    raise KeyError(name)


def trapezoid_row_weights(x_eval: np.ndarray) -> np.ndarray:
    dx = np.diff(x_eval)
    weights = np.empty(x_eval.size, dtype=float)
    weights[0] = dx[0] / 2.0
    weights[-1] = dx[-1] / 2.0
    weights[1:-1] = 0.5 * (dx[:-1] + dx[1:])
    return weights


def build_energy_channel_matrices(
    obj: full_search.BoundaryMatrixObjects,
    x_eval: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    n_unknowns = obj.space.n_unknowns
    channel_blocks: list[np.ndarray] = []

    for col in range(n_unknowns):
        vals = obj.space.basis_eval_full(x_eval, col, obj.base)
        stacked_channels = []
        for name, scale in CHANNEL_SPECS:
            arr = vals[name] if name in vals else extra_channel(name, vals)
            stacked_channels.append(float(scale) * np.asarray(arr, dtype=float))
        channel_blocks.append(np.concatenate(stacked_channels))

    field_matrix = np.column_stack(channel_blocks)
    row_weights = np.tile(trapezoid_row_weights(x_eval), len(CHANNEL_SPECS))
    weighted_field_matrix = field_matrix * np.sqrt(row_weights)[:, None]
    return field_matrix, weighted_field_matrix


def amplitude_normalized_energy_metric(
    current_obj: full_search.BoundaryMatrixObjects,
    bundle_objects: list[full_search.BoundaryMatrixObjects],
) -> dict[str, float | int | str]:
    bundle_basis = orthonormal_bundle_basis([obj.V_reg for obj in bundle_objects])

    a_block = scaled_block(current_obj.A_int)
    b_block = scaled_block(full_search.ROW_SCALE[:, None] * current_obj.B_full)
    operator = np.vstack([a_block, b_block])

    x_eval = np.linspace(current_obj.space.x0, 1.0, EVAL_NX)
    field_matrix, weighted_field_matrix = build_energy_channel_matrices(current_obj, x_eval)

    operator_reduced = operator @ bundle_basis
    gram_reduced = weighted_field_matrix @ bundle_basis
    mass_matrix = gram_reduced.T @ gram_reduced
    mass_matrix = 0.5 * (mass_matrix + mass_matrix.T)

    reg_scale = max(float(np.trace(mass_matrix)) / max(mass_matrix.shape[0], 1), 1.0)
    mass_matrix = mass_matrix + (1.0e-12 * reg_scale) * np.eye(mass_matrix.shape[0], dtype=float)

    chol = cholesky(mass_matrix, lower=True, check_finite=False)
    chol_inv_t = solve_triangular(chol.T, np.eye(chol.shape[0], dtype=float), lower=False, check_finite=False)
    normalized_operator = operator_reduced @ chol_inv_t

    _u, singular_values, vh = np.linalg.svd(normalized_operator, full_matrices=False)
    reduced_coeff = chol_inv_t @ vh[-1]
    direction = bundle_basis @ reduced_coeff

    amplitude_norm = float(np.linalg.norm(weighted_field_matrix @ direction))
    if amplitude_norm > 0.0:
        direction = direction / amplitude_norm

    interior_resid_norm = float(np.linalg.norm(a_block @ direction))
    boundary_resid_norm = float(np.linalg.norm(b_block @ direction))
    total_resid_sq = interior_resid_norm * interior_resid_norm + boundary_resid_norm * boundary_resid_norm
    boundary_resid_share = float((boundary_resid_norm * boundary_resid_norm) / max(total_resid_sq, EPS))

    weighted_state = field_matrix @ direction
    density = np.zeros_like(x_eval)
    for channel_index in range(len(CHANNEL_SPECS)):
        start = channel_index * x_eval.size
        stop = start + x_eval.size
        block = weighted_state[start:stop]
        density += block * block

    total_density = integrate_curve(x_eval, density)
    edge_mask = x_eval >= EDGE_X_MIN
    edge_share = integrate_curve(x_eval[edge_mask], density[edge_mask]) / max(total_density, EPS)
    peak_x = float(x_eval[int(np.argmax(density))])

    e_sigma = float(singular_values[-1])
    return {
        "e_sigma": e_sigma,
        "e_lambda": float(e_sigma * e_sigma),
        "e_interior_resid_norm": interior_resid_norm,
        "e_boundary_resid_norm": boundary_resid_norm,
        "e_boundary_resid_share": boundary_resid_share,
        "e_residual_class": residual_reading_class(boundary_resid_share),
        "e_edge_share": float(edge_share),
        "e_concentration_class": concentration_class(edge_share),
        "e_peak_x": peak_x,
        "e_peak_class": peak_class(peak_x),
        "e_bundle_rank": int(bundle_basis.shape[1]),
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

    if value_key == "e_sigma":
        summary["lambda"] = float(best_row["e_lambda"])
        summary["boundary_share"] = float(best_row["e_boundary_resid_share"])
        summary["residual_class"] = str(best_row["e_residual_class"])
        summary["edge_share"] = float(best_row["e_edge_share"])
        summary["concentration_class"] = str(best_row["e_concentration_class"])
        summary["peak_x"] = float(best_row["e_peak_x"])
        summary["peak_class"] = str(best_row["e_peak_class"])
        summary["bundle_rank"] = int(best_row["e_bundle_rank"])
        summary["interior_resid_norm"] = float(best_row["e_interior_resid_norm"])
        summary["boundary_resid_norm"] = float(best_row["e_boundary_resid_norm"])

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

    if metric_key == "e":
        boundary_shares = [float(row["e_boundary_share"]) for row in summaries]
        residual_classes = [str(row["e_residual_class"]) for row in summaries]
        edge_shares = [float(row["e_edge_share"]) for row in summaries]
        concentration_classes = [str(row["e_concentration_class"]) for row in summaries]
        aggregate["boundary_shares"] = boundary_shares
        aggregate["residual_class"] = aggregate_residual_class(residual_classes)
        aggregate["edge_shares"] = edge_shares
        aggregate["concentration_class"] = aggregate_concentration_class(concentration_classes)

    return aggregate


def window_status(raw_summary: dict[str, object], e_summary: dict[str, object]) -> str:
    if (
        str(e_summary["residual_class"]) == "interior-dominated"
        and str(e_summary["concentration_class"]) != "edge-concentrated"
        and str(e_summary["stability_class"]) in {"stable", "moderate"}
    ):
        return "energy-like reduced-coercivity signal survives the selected local-window check"
    if str(raw_summary["stability_class"]) == "unstable" and str(e_summary["stability_class"]) in {"stable", "moderate"}:
        return "E is more stable than the raw boundary-only reading on the selected local windows"
    if str(e_summary["residual_class"]) != "boundary-dominated" and str(e_summary["concentration_class"]) != "edge-concentrated":
        return "E gives an interior-distributed surrogate signal, but the competition remains sensitivity-limited"
    return "E remains sensitivity-limited or edge-affected on the selected checks"


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
        bundle_indices = range(max(0, idx - E_BUNDLE_RADIUS), min(len(objects), idx + E_BUNDLE_RADIUS + 1))
        e_metric = amplitude_normalized_energy_metric(obj, [objects[j] for j in bundle_indices])
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
                "e_sigma": float(e_metric["e_sigma"]),
                "e_lambda": float(e_metric["e_lambda"]),
                "e_interior_resid_norm": float(e_metric["e_interior_resid_norm"]),
                "e_boundary_resid_norm": float(e_metric["e_boundary_resid_norm"]),
                "e_boundary_resid_share": float(e_metric["e_boundary_resid_share"]),
                "e_residual_class": str(e_metric["e_residual_class"]),
                "e_edge_share": float(e_metric["e_edge_share"]),
                "e_concentration_class": str(e_metric["e_concentration_class"]),
                "e_peak_x": float(e_metric["e_peak_x"]),
                "e_peak_class": str(e_metric["e_peak_class"]),
                "e_bundle_rank": int(e_metric["e_bundle_rank"]),
                "residual_norm_1": float(obj.residual_norms[0]),
                "residual_norm_2": float(obj.residual_norms[1]),
                "background_seed_kind": str(background.seed_kind),
            }
        )

    raw_curve = summarize_curve(point_rows, "sigma_bal")
    e_curve = summarize_curve(point_rows, "e_sigma")
    setting_summary = {
        "setting": str(setting["label"]),
        "window": str(window_label),
        "m_basis": int(setting["m_basis"]),
        "n_collocation": int(setting["n_collocation"]),
        "nd_base": int(setting["nd_base"]),
        "raw_best_q_mpa": float(raw_curve["best_q_mpa"]),
        "raw_best_value": float(raw_curve["best_value"]),
        "raw_location": str(raw_curve["location"]),
        "e_best_q_mpa": float(e_curve["best_q_mpa"]),
        "e_best_value": float(e_curve["best_value"]),
        "e_best_lambda": float(e_curve["lambda"]),
        "e_location": str(e_curve["location"]),
        "e_boundary_share": float(e_curve["boundary_share"]),
        "e_residual_class": str(e_curve["residual_class"]),
        "e_edge_share": float(e_curve["edge_share"]),
        "e_concentration_class": str(e_curve["concentration_class"]),
        "e_peak_x": float(e_curve["peak_x"]),
        "e_peak_class": str(e_curve["peak_class"]),
        "e_bundle_rank": int(e_curve["bundle_rank"]),
        "e_interior_resid_norm": float(e_curve["interior_resid_norm"]),
        "e_boundary_resid_norm": float(e_curve["boundary_resid_norm"]),
    }
    return point_rows, setting_summary


def main() -> None:
    start_time = time.time()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    background_config = high_bg.default_high_load_background_config()
    x0 = float(background_config.x0)

    summary: dict[str, object] = {
        "method_note": (
            "Criterion pilot E for the clean full simple support / podvizhnyi sharnir path. "
            "The main standalone clean solver code path is unchanged. "
            "The raw reference is the current balanced boundary-only metric sigma_bal from B_mix. "
            "The E diagnostic is an energy-like reduced-coercivity surrogate, not a theorem-level second variation: "
            "it uses the smallest amplitude-normalized singular value of the scaled residual operator "
            "[A_int(q); B_bal(q)] restricted to the local three-load tangent-bundle subspace "
            "span(V_reg(q-Delta), V_reg(q), V_reg(q+Delta)). "
            "The amplitude norm is built from the current reconstructed strain/curvature channels "
            "e_s, e_theta, gamma_theta, 2(1+nu)S, phi_x, kappa_theta_new, sqrt(C_twist) H. "
            "This keeps the clean equations and BC meaning unchanged and moves the reading closer to a quadratic-form "
            "loss-of-coercivity interpretation than the boundary-only B_mix minimum, while remaining only a surrogate."
        ),
        "e_object_definition": {
            "bundle_radius_in_load_steps": E_BUNDLE_RADIUS,
            "quadratic_form": "Q_E(c)=||scaled A_int c||^2 + ||scaled B_bal c||^2 on the local tangent bundle",
            "amplitude_norm": "M_E(c)=integral[e_s^2 + e_theta^2 + gamma_theta^2 + (2(1+nu)S)^2 + phi_x^2 + kappa_theta_new^2 + (sqrt(C_twist)H)^2] dx",
            "diagnostic": "e_sigma = sqrt(min Q_E / M_E) on the selected reduced subspace",
            "status": "energy-like reduced-coercivity surrogate, not the final second variation",
            "edge_share_x_min": EDGE_X_MIN,
            "eval_grid_points": EVAL_NX,
        },
        "background_config": dict(background_config.__dict__),
        "mode_windows": MODE_SPECS,
        "settings": list(SETTING_SPECS),
        "channels": [{"name": name, "scale": float(scale)} for name, scale in CHANNEL_SPECS],
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
        e_window_aggregate = aggregate_metric(baseline_window_summaries, "e")
        mode_summary["raw_window_summary"] = raw_window_aggregate
        mode_summary["e_window_summary"] = e_window_aggregate
        mode_summary["window_status"] = window_status(raw_window_aggregate, e_window_aggregate)

        refinement_summary = None
        if int(mode) in FOCUSED_REFINEMENT_MODES:
            refinement_summary = aggregate_metric(focused_refinement_summaries, "e")
            mode_summary["focused_refinement_e_summary"] = refinement_summary
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
                "e_broad_best_q_mpa": float(broad_summary["e_best_q_mpa"]),
                "e_broad_best_value": float(broad_summary["e_best_value"]),
                "e_broad_best_lambda": float(broad_summary["e_best_lambda"]),
                "e_broad_location": str(broad_summary["e_location"]),
                "e_broad_residual_class": str(broad_summary["e_residual_class"]),
                "e_broad_boundary_share": float(broad_summary["e_boundary_share"]),
                "e_broad_concentration_class": str(broad_summary["e_concentration_class"]),
                "e_broad_edge_share": float(broad_summary["e_edge_share"]),
                "raw_focused_best_q_mpa": float(focused_summary["raw_best_q_mpa"]),
                "raw_focused_best_value": float(focused_summary["raw_best_value"]),
                "raw_focused_location": str(focused_summary["raw_location"]),
                "e_focused_best_q_mpa": float(focused_summary["e_best_q_mpa"]),
                "e_focused_best_value": float(focused_summary["e_best_value"]),
                "e_focused_best_lambda": float(focused_summary["e_best_lambda"]),
                "e_focused_location": str(focused_summary["e_location"]),
                "e_focused_residual_class": str(focused_summary["e_residual_class"]),
                "e_focused_boundary_share": float(focused_summary["e_boundary_share"]),
                "e_focused_concentration_class": str(focused_summary["e_concentration_class"]),
                "e_focused_edge_share": float(focused_summary["e_edge_share"]),
                "raw_window_q_drift_mpa": float(raw_window_aggregate["q_drift_mpa"]),
                "raw_window_value_ratio": float(raw_window_aggregate["value_ratio"]),
                "raw_window_stability": str(raw_window_aggregate["stability_class"]),
                "e_window_q_drift_mpa": float(e_window_aggregate["q_drift_mpa"]),
                "e_window_value_ratio": float(e_window_aggregate["value_ratio"]),
                "e_window_stability": str(e_window_aggregate["stability_class"]),
                "e_window_residual_class": str(e_window_aggregate["residual_class"]),
                "e_window_concentration_class": str(e_window_aggregate["concentration_class"]),
                "window_status": str(mode_summary["window_status"]),
                "focused_refinement_q_drift_mpa": float(refinement_summary["q_drift_mpa"]) if refinement_summary else float("nan"),
                "focused_refinement_value_ratio": float(refinement_summary["value_ratio"]) if refinement_summary else float("nan"),
                "focused_refinement_stability": str(refinement_summary["stability_class"]) if refinement_summary else "not_requested",
                "focused_refinement_status": str(mode_summary.get("focused_refinement_status", "not requested")),
            }
        )

    focused_baseline_rows = sorted(table_rows, key=lambda row: float(row["e_focused_best_value"]))
    summary["focused_baseline_e_ranking"] = [
        {
            "n": int(row["n"]),
            "role_hint": str(row["role_hint"]),
            "e_focused_best_q_mpa": float(row["e_focused_best_q_mpa"]),
            "e_focused_best_value": float(row["e_focused_best_value"]),
            "e_focused_best_lambda": float(row["e_focused_best_lambda"]),
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
        "e_broad_best_q_mpa",
        "e_broad_best_value",
        "e_broad_best_lambda",
        "e_broad_location",
        "e_broad_residual_class",
        "e_broad_boundary_share",
        "e_broad_concentration_class",
        "e_broad_edge_share",
        "raw_focused_best_q_mpa",
        "raw_focused_best_value",
        "raw_focused_location",
        "e_focused_best_q_mpa",
        "e_focused_best_value",
        "e_focused_best_lambda",
        "e_focused_location",
        "e_focused_residual_class",
        "e_focused_boundary_share",
        "e_focused_concentration_class",
        "e_focused_edge_share",
        "raw_window_q_drift_mpa",
        "raw_window_value_ratio",
        "raw_window_stability",
        "e_window_q_drift_mpa",
        "e_window_value_ratio",
        "e_window_stability",
        "e_window_residual_class",
        "e_window_concentration_class",
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
        "e_sigma",
        "e_lambda",
        "e_interior_resid_norm",
        "e_boundary_resid_norm",
        "e_boundary_resid_share",
        "e_residual_class",
        "e_edge_share",
        "e_concentration_class",
        "e_peak_x",
        "e_peak_class",
        "e_bundle_rank",
        "residual_norm_1",
        "residual_norm_2",
        "background_seed_kind",
    ]
    with POINTS_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=point_columns)
        writer.writeheader()
        writer.writerows(point_rows_all)

    print("=== Criterion pilot E complete ===")
    print(f"summary json: {SUMMARY_JSON}")
    print(f"summary csv:  {SUMMARY_CSV}")
    print(f"points csv:   {POINTS_CSV}")
    print(f"runtime:      {summary['runtime_seconds']:.2f} s")


if __name__ == "__main__":
    main()
