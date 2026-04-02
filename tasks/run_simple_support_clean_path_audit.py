# -*- coding: utf-8 -*-
# Purpose:
#   Run a narrow clean-path audit for the full simple-support critical layer
#   without changing equations, BC meaning, or solver behavior.
# Typical use:
#   .venv\Scripts\python.exe tasks\run_simple_support_clean_path_audit.py
# Outputs:
#   output/clean_full_simple_support/clean_path_audit_summary.json
#   output/clean_full_simple_support/clean_path_audit_table.csv

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
from shell_buckling.mixed_weak import full_simple_support_critical_search as full_search
from shell_buckling.mixed_weak import simple_support_high_load_background_continuation as high_bg
from shell_buckling.mixed_weak import solver_patched_core as mw


OUTPUT_DIR = REPO_ROOT / "output" / "clean_full_simple_support"
SUMMARY_JSON = OUTPUT_DIR / "clean_path_audit_summary.json"
SUMMARY_CSV = OUTPUT_DIR / "clean_path_audit_table.csv"

SAMPLE_Q_MPA = (17.30, 17.45, 17.60)
SAMPLE_MODES = (7, 8)
BOUNDARY_ROW_LABELS = tuple(full_search.CRITICAL_BOUNDARY_ROW_LABELS)
BOUNDARY_CHANNEL_KEYS = ("u_n", "phi", "T_s", "S", "H")
TARGET_CENTER_BLOCK = np.array(
    [
        [1.0, 0.0],
        [0.0, 1.0],
        [0.0, 0.0],
        [0.0, 0.0],
    ],
    dtype=float,
)
TEST_COMBINATION = np.array([1.25, -0.75], dtype=float)
ALGEBRAIC_TOL = 1.0e-8


def max_abs(A: np.ndarray) -> float:
    return float(np.max(np.abs(np.asarray(A, dtype=float))))


def condition_number(A: np.ndarray) -> float:
    singular_values = np.linalg.svd(np.asarray(A, dtype=float), compute_uv=False)
    if singular_values.size == 0:
        return float("nan")
    if singular_values[-1] <= 0.0:
        return float("inf")
    return float(singular_values[0] / singular_values[-1])


def build_sample_objects(config) -> dict[tuple[int, float], full_search.BoundaryMatrixObjects]:
    q_values = [float(q) for q in SAMPLE_Q_MPA]
    background_results = high_bg.solve_axisymmetric_simple_support_high_load_schedule(
        q_values,
        config=config,
        verbose=False,
    )
    by_q = {round(float(result.q_mpa), 7): result for result in background_results}
    objects: dict[tuple[int, float], full_search.BoundaryMatrixObjects] = {}
    for n in SAMPLE_MODES:
        for q_mpa in SAMPLE_Q_MPA:
            background = by_q[round(float(q_mpa), 7)]
            if not background.success or background.solution is None:
                raise RuntimeError(f"Background solve failed at n={n}, q={q_mpa:.6f} MPa.")
            objects[(int(n), float(q_mpa))] = full_search.build_boundary_matrix_objects(
                n=int(n),
                background_result=background,
                x0=float(config.x0),
            )
    return objects


def manual_boundary_vector(obj: full_search.BoundaryMatrixObjects, coeffs: np.ndarray) -> np.ndarray:
    channels = red.evaluate_mode_channels(
        mw_module=mw,
        space=obj.space,
        base=obj.base,
        coeffs=np.asarray(coeffs, dtype=float),
        x=np.array([1.0], dtype=float),
        B_full=None,
    )
    return np.array([float(channels[key][0]) for key in BOUNDARY_CHANNEL_KEYS], dtype=float)


def sample_report(obj: full_search.BoundaryMatrixObjects) -> dict[str, object]:
    C_amp = np.asarray(obj.C_center[:2, :], dtype=float)
    C_reg = np.asarray(obj.C_center[2:, :], dtype=float)
    L_full = np.vstack([obj.A_int, obj.B_full])
    L_red = L_full @ obj.V_adm

    test_vectors = {
        "V_reg_col1": np.asarray(obj.V_reg[:, 0], dtype=float),
        "V_reg_col2": np.asarray(obj.V_reg[:, 1], dtype=float),
        "V_adm_col1": np.asarray(obj.V_adm[:, 0], dtype=float),
        "V_adm_col2": np.asarray(obj.V_adm[:, 1], dtype=float),
        "V_adm_combo": np.asarray(obj.V_adm @ TEST_COMBINATION, dtype=float),
    }

    boundary_tests: list[dict[str, object]] = []
    rowwise_boundary_max = np.zeros(len(BOUNDARY_ROW_LABELS), dtype=float)
    for label, coeffs in test_vectors.items():
        manual = manual_boundary_vector(obj, coeffs)
        assembled = np.asarray(obj.B_full @ coeffs, dtype=float)
        residual = manual - assembled
        rowwise_boundary_max = np.maximum(rowwise_boundary_max, np.abs(residual))
        boundary_tests.append(
            {
                "label": label,
                "max_abs_residual": max_abs(residual),
                "assembled": assembled.tolist(),
                "manual": manual.tolist(),
                "residual": residual.tolist(),
            }
        )

    center_block = np.asarray(obj.C_center @ obj.V_adm, dtype=float)
    report = {
        "n": int(obj.n),
        "q_mpa": float(obj.q_mpa),
        "trial_space_dimension": int(obj.space.n_unknowns),
        "critical_boundary_row_labels": list(BOUNDARY_ROW_LABELS),
        "row_scale": full_search.ROW_SCALE.tolist(),
        "det_G_amp": float(np.linalg.det(obj.G_amp)),
        "cond_G_amp": condition_number(obj.G_amp),
        "rank_C_amp": int(np.linalg.matrix_rank(C_amp)),
        "rank_C_reg": int(np.linalg.matrix_rank(C_reg)),
        "rank_C_center": int(np.linalg.matrix_rank(obj.C_center)),
        "max_G_amp_minus_C_amp_V_reg": max_abs(obj.G_amp - C_amp @ obj.V_reg),
        "max_C_amp_V_adm_minus_I": max_abs(C_amp @ obj.V_adm - np.eye(2, dtype=float)),
        "max_C_reg_V_adm": max_abs(C_reg @ obj.V_adm),
        "max_C_center_V_adm_minus_target": max_abs(center_block - TARGET_CENTER_BLOCK),
        "max_V_reg_minus_V_adm_G_amp": max_abs(obj.V_reg - obj.V_adm @ obj.G_amp),
        "max_B_red_minus_B_full_V_adm": max_abs(obj.B_red - obj.B_full @ obj.V_adm),
        "max_B_mix_minus_B_red_G_amp": max_abs(obj.B_mix - obj.B_red @ obj.G_amp),
        "max_L_red_minus_stacked_full_V_adm": max_abs(L_red - L_full @ obj.V_adm),
        "max_boundary_manual_vs_assembled": float(np.max(rowwise_boundary_max)),
        "boundary_manual_vs_assembled_by_row": {
            label: float(value) for label, value in zip(BOUNDARY_ROW_LABELS, rowwise_boundary_max)
        },
        "boundary_manual_tests": boundary_tests,
    }
    return report

def aggregate_summary(sample_reports: list[dict[str, object]]) -> dict[str, object]:
    max_center_identity = max(float(item["max_C_center_V_adm_minus_target"]) for item in sample_reports)
    max_boundary_identity = max(float(item["max_boundary_manual_vs_assembled"]) for item in sample_reports)
    max_rebasing_identity = max(
        max(
            float(item["max_G_amp_minus_C_amp_V_reg"]),
            float(item["max_B_red_minus_B_full_V_adm"]),
            float(item["max_B_mix_minus_B_red_G_amp"]),
            float(item["max_V_reg_minus_V_adm_G_amp"]),
        )
        for item in sample_reports
    )
    min_det_g = min(abs(float(item["det_G_amp"])) for item in sample_reports)
    max_cond_g = max(float(item["cond_G_amp"]) for item in sample_reports)

    suspicion_flags: list[str] = []
    if max_center_identity > ALGEBRAIC_TOL:
        suspicion_flags.append("center_identity_residual")
    if max_boundary_identity > ALGEBRAIC_TOL:
        suspicion_flags.append("boundary_row_reconstruction_residual")
    if max_rebasing_identity > ALGEBRAIC_TOL:
        suspicion_flags.append("rebasing_identity_residual")
    if not np.isfinite(min_det_g) or min_det_g <= 1.0e-12:
        suspicion_flags.append("near_singular_G_amp")
    if not np.isfinite(max_cond_g):
        suspicion_flags.append("nonfinite_G_amp_conditioning")

    if suspicion_flags:
        conclusion = (
            "specific clean-path inconsistency or fragility signal detected; review the flagged identities before reading the n=7/n=8 ambiguity as criterion-only"
        )
    else:
        conclusion = (
            "clean path looks internally consistent on the audited representative points; there is no grounded code-level sign/order/rebasing inconsistency here that obviously explains the current n=7/n=8 near-degeneracy"
        )

    return {
        "max_center_identity_residual": max_center_identity,
        "max_boundary_row_reconstruction_residual": max_boundary_identity,
        "max_rebasing_identity_residual": max_rebasing_identity,
        "min_abs_det_G_amp": min_det_g,
        "max_cond_G_amp": max_cond_g,
        "suspicion_flags": suspicion_flags,
        "conclusion": conclusion,
    }


def main() -> None:
    start_time = time.time()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    config = high_bg.default_high_load_background_config()
    objects = build_sample_objects(config=config)
    reports = [sample_report(objects[(int(n), float(q))]) for n in SAMPLE_MODES for q in SAMPLE_Q_MPA]
    aggregate = aggregate_summary(reports)

    summary = {
        "method_note": (
            "Narrow clean-path audit for the full simple-support critical layer. "
            "This pass checks boundary-row consistency, center-constraint identities, and reduced-family rebasing identities "
            "on representative n=7/n=8 clean points without changing equations, BC meaning, or solver behavior."
        ),
        "inspected_modules": {
            "clean_critical_search": "src/shell_buckling/mixed_weak/full_simple_support_critical_search.py",
            "core_reduction": "src/shell_buckling/mixed_weak/_core_reduction.py",
            "solver_wrapper": "src/shell_buckling/mixed_weak/solver_patched_core.py",
            "solver_shared_core": "src/shell_buckling/mixed_weak/_core_solver_common.py",
            "status_note": "docs/theory/current_simple_support_status.md",
            "pilot_note": "proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md",
        },
        "sample_q_mpa": list(SAMPLE_Q_MPA),
        "sample_modes": list(SAMPLE_MODES),
        "critical_boundary_row_labels": list(BOUNDARY_ROW_LABELS),
        "row_scale": full_search.ROW_SCALE.tolist(),
        "background_config": dict(config.__dict__),
        "sample_reports": reports,
        "aggregate": aggregate,
        "runtime_seconds": float(time.time() - start_time),
    }

    with SUMMARY_JSON.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False, allow_nan=True)
        fh.write("\n")

    columns = [
        "n",
        "q_mpa",
        "det_G_amp",
        "cond_G_amp",
        "rank_C_amp",
        "rank_C_reg",
        "rank_C_center",
        "max_G_amp_minus_C_amp_V_reg",
        "max_C_amp_V_adm_minus_I",
        "max_C_reg_V_adm",
        "max_C_center_V_adm_minus_target",
        "max_V_reg_minus_V_adm_G_amp",
        "max_B_red_minus_B_full_V_adm",
        "max_B_mix_minus_B_red_G_amp",
        "max_L_red_minus_stacked_full_V_adm",
        "max_boundary_manual_vs_assembled",
    ]
    with SUMMARY_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns)
        writer.writeheader()
        writer.writerows({key: item[key] for key in columns} for item in reports)

    print("=== Clean-path audit complete ===")
    print("critical boundary rows: [" + ", ".join(BOUNDARY_ROW_LABELS) + "]")
    for item in reports:
        print(
            f"n={item['n']} q={item['q_mpa']:.2f} MPa | "
            f"det(G_amp)={item['det_G_amp']:.6e} cond(G_amp)={item['cond_G_amp']:.6e} | "
            f"center={item['max_C_center_V_adm_minus_target']:.3e} "
            f"boundary={item['max_boundary_manual_vs_assembled']:.3e} "
            f"rebasing={max(item['max_B_red_minus_B_full_V_adm'], item['max_B_mix_minus_B_red_G_amp'], item['max_G_amp_minus_C_amp_V_reg']):.3e}"
        )
    print("aggregate conclusion: " + str(aggregate["conclusion"]))
    print(f"summary json: {SUMMARY_JSON}")
    print(f"summary csv:  {SUMMARY_CSV}")
    print(f"runtime:      {summary['runtime_seconds']:.2f} s")


if __name__ == "__main__":
    main()
