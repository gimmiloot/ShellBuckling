# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np
import sympy as sp

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.mixed_weak import full_simple_support_critical_search as full_search
from shell_buckling.mixed_weak import simple_support_high_load_background_continuation as high_bg


SAMPLE_POINTS: tuple[tuple[int, float], ...] = (
    (4, 11.1),
    (6, 17.6),
    (7, 17.3),
    (8, 17.8),
)
BASIS_CHANGE_T = np.array([[2.0, -1.0], [1.0, 3.0]], dtype=float)
AMP_INJECTION = np.array(
    [
        [1.0, 0.0],
        [0.0, 1.0],
        [0.0, 0.0],
        [0.0, 0.0],
    ],
    dtype=float,
)
TARGET_CENTER_BLOCK = np.array(
    [
        [1.0, 0.0],
        [0.0, 1.0],
        [0.0, 0.0],
        [0.0, 0.0],
    ],
    dtype=float,
)
CONSTRAINED_MODE_REG = 1.0e-12


def stacked_full_operator(obj: full_search.BoundaryMatrixObjects) -> np.ndarray:
    return np.vstack([obj.A_int, obj.B_full])


def split_center_matrix(C_center: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return np.asarray(C_center[:2, :], dtype=float), np.asarray(C_center[2:, :], dtype=float)


def canonical_center_basis(obj: full_search.BoundaryMatrixObjects) -> tuple[np.ndarray, np.ndarray]:
    C_amp, _C_reg = split_center_matrix(obj.C_center)
    G_amp = C_amp @ obj.V_reg
    det_g = float(np.linalg.det(G_amp))
    if abs(det_g) <= 1.0e-14:
        raise RuntimeError("Leading center-amplitude block is numerically singular.")
    V_adm = obj.V_reg @ np.linalg.inv(G_amp)
    return V_adm, G_amp


def constrained_amplitude_family(
    obj: full_search.BoundaryMatrixObjects,
    reg: float = CONSTRAINED_MODE_REG,
) -> np.ndarray:
    A = np.asarray(obj.A_int, dtype=float)
    C = np.asarray(obj.C_center, dtype=float)
    n_unknowns = A.shape[1]
    n_constraints = C.shape[0]
    ATA = A.T @ A + float(reg) * np.eye(n_unknowns, dtype=float)
    KKT = np.block(
        [
            [ATA, C.T],
            [C, np.zeros((n_constraints, n_constraints), dtype=float)],
        ]
    )
    rhs = np.vstack([np.zeros((n_unknowns, 2), dtype=float), AMP_INJECTION])
    sol = np.linalg.solve(KKT, rhs)
    return sol[:n_unknowns, :]


def build_sample_objects(
    samples: tuple[tuple[int, float], ...],
    config,
) -> dict[tuple[int, float], full_search.BoundaryMatrixObjects]:
    q_values = sorted({float(q) for _n, q in samples})
    background_results = high_bg.solve_axisymmetric_simple_support_high_load_schedule(
        q_values,
        config=config,
        verbose=False,
    )
    by_q = {round(float(result.q_mpa), 7): result for result in background_results}
    objects: dict[tuple[int, float], full_search.BoundaryMatrixObjects] = {}
    for n, q_mpa in samples:
        background = by_q[round(float(q_mpa), 7)]
        if not background.success or background.solution is None:
            raise RuntimeError(f"Background solve failed at n={n}, q={q_mpa}.")
        objects[(int(n), float(q_mpa))] = full_search.build_boundary_matrix_objects(
            n=int(n),
            background_result=background,
            x0=float(config.x0),
        )
    return objects


def symbolic_checks() -> dict[str, bool]:
    m, k, n, r = sp.symbols("m k n r", integer=True, positive=True)
    lam = sp.symbols("lam")
    A = sp.MatrixSymbol("A", m, n)
    B = sp.MatrixSymbol("B", k, n)
    V = sp.MatrixSymbol("V", n, r)
    T = sp.MatrixSymbol("T", r, r)
    G = sp.MatrixSymbol("G", r, r)
    L = sp.BlockMatrix([[A], [B]])
    stacked_identity = sp.block_collapse(L * V) == sp.BlockMatrix([[A * V], [B * V]])
    gram_identity = sp.block_collapse((L * V).T * (L * V)) == (V.T * A.T * A + V.T * B.T * B) * V
    normal_identity = sp.block_collapse(L.T * L) == A.T * A + B.T * B
    basis_change_identity = sp.block_collapse(L * V * T) == sp.block_collapse((L * V) * T)
    boundary_basis_change_identity = sp.block_collapse(B * V * T) == sp.block_collapse((B * V) * T)
    bred_bmix_coordinate_identity = sp.block_collapse(B * V * sp.Inverse(G) * G) == sp.block_collapse(B * V)

    leading_center = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, lam / n, 0],
            [0, 0, -lam, 1],
        ]
    )
    leading_reg = leading_center[2:, :]
    a_us, a_phi = sp.symbols("a_us a_phi")
    regular_param = sp.Matrix([a_us, -(lam / n) * a_phi, a_phi, lam * a_phi])

    return {
        "stacked_restriction_identity": bool(stacked_identity),
        "reduced_gram_identity": bool(gram_identity),
        "normal_matrix_identity": bool(normal_identity),
        "basis_change_stacked_identity": bool(basis_change_identity),
        "basis_change_boundary_identity": bool(boundary_basis_change_identity),
        "bred_bmix_coordinate_identity": bool(bred_bmix_coordinate_identity),
        "leading_center_block_det_minus_one": bool(sp.simplify(leading_center.det()) == -1),
        "leading_regularity_rank_two": bool(leading_reg.rank() == 2),
        "leading_regularity_nullspace_two_parameter": bool(len(leading_reg.nullspace()) == 2),
        "leading_regular_parameterization_identity": bool(leading_reg * regular_param == sp.zeros(2, 1)),
    }


def numerical_checks() -> dict[str, object]:
    config = high_bg.default_high_load_background_config()
    objects = build_sample_objects(SAMPLE_POINTS, config=config)
    samples_report: list[dict[str, object]] = []

    for n, q_mpa in SAMPLE_POINTS:
        obj = objects[(int(n), float(q_mpa))]
        V_adm, G_amp = canonical_center_basis(obj)
        V_kkt = constrained_amplitude_family(obj)
        C_amp, C_reg = split_center_matrix(obj.C_center)
        L_full = stacked_full_operator(obj)
        L_red = L_full @ V_adm
        B_red = obj.B_full @ V_adm
        V_basis_changed = V_adm @ BASIS_CHANGE_T
        L_red_basis_changed = L_full @ V_basis_changed
        B_red_basis_changed = obj.B_full @ V_basis_changed
        C_full_canon = obj.C_center @ V_adm
        C_full_kkt = obj.C_center @ V_kkt
        gram_left = L_red.T @ L_red
        gram_right = V_adm.T @ (obj.A_int.T @ obj.A_int + obj.B_full.T @ obj.B_full) @ V_adm

        samples_report.append(
            {
                "n": int(n),
                "q_mpa": float(q_mpa),
                "shapes": {
                    "A_int": list(obj.A_int.shape),
                    "B_full": list(obj.B_full.shape),
                    "C_center": list(obj.C_center.shape),
                    "V_reg": list(obj.V_reg.shape),
                    "L_full": list(L_full.shape),
                    "L_red": list(L_red.shape),
                    "B_red": list(B_red.shape),
                },
                "det_G_amp": float(np.linalg.det(G_amp)),
                "cond_G_amp": float(np.linalg.cond(G_amp)),
                "rank_C_amp": int(np.linalg.matrix_rank(C_amp)),
                "rank_C_reg": int(np.linalg.matrix_rank(C_reg)),
                "rank_C_center": int(np.linalg.matrix_rank(obj.C_center)),
                "dim_trial_space": int(obj.C_center.shape[1]),
                "dim_ker_C_reg": int(obj.C_center.shape[1] - np.linalg.matrix_rank(C_reg)),
                "dim_ker_C_center": int(obj.C_center.shape[1] - np.linalg.matrix_rank(obj.C_center)),
                "rank_V_reg": int(np.linalg.matrix_rank(obj.V_reg)),
                "rank_V_adm": int(np.linalg.matrix_rank(V_adm)),
                "rank_V_kkt": int(np.linalg.matrix_rank(V_kkt)),
                "max_center_regularity_violation_raw": float(np.max(np.abs(C_reg @ obj.V_reg))),
                "max_center_amplitude_row_residual_canon": float(
                    np.max(np.abs(C_amp @ V_adm - np.eye(2, dtype=float)))
                ),
                "max_center_full_residual_canon": float(
                    np.max(np.abs(C_full_canon - TARGET_CENTER_BLOCK))
                ),
                "max_center_full_residual_kkt": float(
                    np.max(np.abs(C_full_kkt - TARGET_CENTER_BLOCK))
                ),
                "max_vreg_reconstruction_residual": float(
                    np.max(np.abs(obj.V_reg - V_adm @ G_amp))
                ),
                "max_vadm_minus_vkkt": float(np.max(np.abs(V_adm - V_kkt))),
                "max_gram_identity_residual": float(np.max(np.abs(gram_left - gram_right))),
                "max_full_coordinate_reconstruction_residual": float(
                    np.max(np.abs(L_full @ obj.V_reg - L_red @ G_amp))
                ),
                "max_kkt_full_residual": float(np.max(np.abs(L_full @ V_kkt - L_red))),
                "max_bmix_reconstruction_residual": float(
                    np.max(np.abs(obj.B_mix - B_red @ G_amp))
                ),
                "max_kkt_boundary_residual": float(
                    np.max(np.abs(obj.B_full @ V_kkt - B_red))
                ),
                "max_basis_change_full_residual": float(
                    np.max(np.abs(L_red_basis_changed - L_red @ BASIS_CHANGE_T))
                ),
                "max_basis_change_boundary_residual": float(
                    np.max(np.abs(B_red_basis_changed - B_red @ BASIS_CHANGE_T))
                ),
                "interior_column_norms_canon": [
                    float(np.linalg.norm(obj.A_int @ V_adm[:, col])) for col in range(V_adm.shape[1])
                ],
                "sigma_min_L_red": float(np.linalg.svd(L_red, compute_uv=False)[-1]),
                "boundary_sigma_min_canon": float(np.linalg.svd(B_red, compute_uv=False)[-1]),
            }
        )

    return {
        "background_config": dict(config.__dict__),
        "basis_change_T": BASIS_CHANGE_T.tolist(),
        "sample_points": samples_report,
    }


def main() -> None:
    report = {
        "symbolic_checks": symbolic_checks(),
        "numerical_checks": numerical_checks(),
        "conclusion": {
            "c3_exact_restricted_statement": "On the current reduced family A_repo = im(V_adm), the map a -> c = V_adm a identifies ker(L_red) exactly with A_repo intersect ker(L_full).",
            "c3b_ansatz_level_statement": "Inside the current weighted trial ansatz, the four leading center coefficients are reduced by the two regularity relations to a two-parameter leading family, but C_reg = 0 alone still leaves a high-dimensional trial-coefficient space. The current A_repo is exactly the KKT-selected two-dimensional constrained-least-squares family for those amplitudes.",
            "remaining_open_gap": "What is still open is whether that KKT-selected family is already the full admissible clean center-regular tangent space of the continuous linearized problem, and therefore whether the reduction is theorem-level lossless beyond the current repository ansatz.",
        },
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
