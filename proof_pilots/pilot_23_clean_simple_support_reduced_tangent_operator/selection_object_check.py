# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

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
LOCAL_ROW_FRACTIONS: tuple[float, ...] = (0.05, 0.10, 0.20, 0.50)
CONSTRAINED_MODE_REG = 1.0e-12
FULL_CENTER_TARGET = np.eye(4, dtype=float)
AMP_TARGET = np.array(
    [
        [1.0, 0.0],
        [0.0, 1.0],
        [0.0, 0.0],
        [0.0, 0.0],
    ],
    dtype=float,
)
TRACE_BASIS_CHANGE_T = np.array([[2.0, -1.0], [1.0, 3.0]], dtype=float)


def solve_kkt_section(
    A_int: np.ndarray,
    C_center: np.ndarray,
    target: np.ndarray,
    reg: float = CONSTRAINED_MODE_REG,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    A = np.asarray(A_int, dtype=float)
    C = np.asarray(C_center, dtype=float)
    D = np.asarray(target, dtype=float)
    n_unknowns = A.shape[1]
    n_constraints = C.shape[0]
    H = A.T @ A + float(reg) * np.eye(n_unknowns, dtype=float)
    KKT = np.block(
        [
            [H, C.T],
            [C, np.zeros((n_constraints, n_constraints), dtype=float)],
        ]
    )
    rhs = np.vstack([np.zeros((n_unknowns, D.shape[1]), dtype=float), D])
    sol = np.linalg.solve(KKT, rhs)
    return sol[:n_unknowns, :], sol[n_unknowns:, :], H


def solve_amplitude_map(
    A_int: np.ndarray,
    C_center: np.ndarray,
    reg: float = CONSTRAINED_MODE_REG,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return solve_kkt_section(A_int, C_center, AMP_TARGET, reg=reg)


def selected_center_lift_formula(H: np.ndarray, C: np.ndarray) -> np.ndarray:
    H_inv_CT = np.linalg.solve(np.asarray(H, dtype=float), np.asarray(C, dtype=float).T)
    schur = np.asarray(C, dtype=float) @ H_inv_CT
    return H_inv_CT @ np.linalg.solve(schur, FULL_CENTER_TARGET)


def nullspace_basis(C: np.ndarray, tol: float = 1.0e-10) -> tuple[np.ndarray, int, list[float]]:
    _u, svals, vt = np.linalg.svd(np.asarray(C, dtype=float), full_matrices=True)
    rank = int(np.sum(svals > float(tol)))
    return vt[rank:].T, rank, [float(value) for value in svals]


def feasible_reference(C: np.ndarray) -> np.ndarray:
    C_arr = np.asarray(C, dtype=float)
    return C_arr.T @ np.linalg.solve(C_arr @ C_arr.T, AMP_TARGET)


def projected_h_minimizer(H: np.ndarray, N_fiber: np.ndarray, M_ref: np.ndarray) -> np.ndarray:
    reduced_h = N_fiber.T @ np.asarray(H, dtype=float) @ N_fiber
    correction = N_fiber @ np.linalg.solve(reduced_h, N_fiber.T @ np.asarray(H, dtype=float) @ M_ref)
    return M_ref - correction


def quadratic_objectives(H: np.ndarray, M: np.ndarray) -> list[float]:
    return [float(M[:, col].T @ H @ M[:, col]) for col in range(M.shape[1])]


def local_row_subset(A_int: np.ndarray, collocation_points: int) -> np.ndarray:
    n_keep = max(1, int(collocation_points))
    return np.asarray(A_int[: 8 * n_keep, :], dtype=float)


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
            raise RuntimeError(f"Background solve failed at n={n}, q={q_mpa} MPa.")
        objects[(int(n), float(q_mpa))] = full_search.build_boundary_matrix_objects(
            n=int(n),
            background_result=background,
            x0=float(config.x0),
        )
    return objects


def exact_center_trace_block_report(obj: full_search.BoundaryMatrixObjects) -> dict[str, object]:
    C_center = np.asarray(obj.C_center, dtype=float)
    active_cols = [col for col in range(C_center.shape[1]) if np.max(np.abs(C_center[:, col])) > 1.0e-14]
    block = C_center[:, active_cols]
    return {
        "active_columns": [int(col) for col in active_cols],
        "active_column_labels": [
            {"field": str(obj.space.decode_column(col)[0]), "basis_index": int(obj.space.decode_column(col)[1])}
            for col in active_cols
        ],
        "leading_center_block": [[float(value) for value in row] for row in block.tolist()],
        "leading_center_block_det": float(np.linalg.det(block)),
        "max_outside_block_entry": float(
            np.max(np.abs(np.delete(C_center, active_cols, axis=1))) if len(active_cols) < C_center.shape[1] else 0.0
        ),
    }


def per_sample_report(
    mode: int,
    q_mpa: float,
    obj: full_search.BoundaryMatrixObjects,
) -> dict[str, object]:
    A_int = np.asarray(obj.A_int, dtype=float)
    B_full = np.asarray(obj.B_full, dtype=float)
    C_center = np.asarray(obj.C_center, dtype=float)
    C_amp = C_center[:2, :]
    C_reg = C_center[2:, :]

    P_sel_kkt, multipliers_full_lift, H_full = solve_kkt_section(A_int, C_center, FULL_CENTER_TARGET)
    M_full, multipliers_full, _H_full_amp = solve_amplitude_map(A_int, C_center)
    P_sel_formula = selected_center_lift_formula(H_full, C_center)
    M_formula = P_sel_formula @ AMP_TARGET
    N_fiber, rank_C_center, singular_values = nullspace_basis(C_center)
    fiber_gram = N_fiber.T @ H_full @ N_fiber
    fiber_gram_sym = 0.5 * (fiber_gram + fiber_gram.T)
    fiber_eigs = np.linalg.eigvalsh(fiber_gram_sym)
    M_ref = feasible_reference(C_center)
    M_proj = projected_h_minimizer(H_full, N_fiber, M_ref)

    H_inv_CT = np.linalg.solve(H_full, C_center.T)
    schur = C_center @ H_inv_CT

    full_objectives = quadratic_objectives(H_full, M_full)
    ref_objectives = quadratic_objectives(H_full, M_ref)

    trace_basis = C_center @ M_full
    trace_basis_changed = C_center @ (M_full @ TRACE_BASIS_CHANGE_T)
    reconstructed_from_trace = P_sel_kkt @ trace_basis
    reconstructed_from_changed_trace = P_sel_kkt @ trace_basis_changed

    n_collocation = int(A_int.shape[0] // 8)
    subset_reports: list[dict[str, object]] = []
    for fraction in LOCAL_ROW_FRACTIONS:
        n_keep = max(1, int(round(float(fraction) * n_collocation)))
        M_local, _multipliers_local, _H_local = solve_amplitude_map(
            local_row_subset(A_int, n_keep),
            C_center,
        )
        local_objectives = quadratic_objectives(H_full, M_local)
        subset_reports.append(
            {
                "fraction_of_collocation_rows": float(fraction),
                "collocation_points_used": int(n_keep),
                "max_center_residual": float(np.max(np.abs(C_center @ M_local - AMP_TARGET))),
                "fro_coeff_diff_vs_full": float(np.linalg.norm(M_local - M_full)),
                "max_coeff_diff_vs_full": float(np.max(np.abs(M_local - M_full))),
                "full_objective_ratio_vs_selected": [
                    float(local_objectives[idx] / full_objectives[idx]) for idx in range(2)
                ],
                "max_boundary_image_diff_vs_full": float(
                    np.max(np.abs(B_full @ (M_local - M_full)))
                ),
                "full_boundary_diff_norm": float(np.linalg.norm(B_full @ (M_local - M_full))),
                "full_interior_diff_norm": float(np.linalg.norm(A_int @ (M_local - M_full))),
            }
        )

    return {
        "n": int(mode),
        "q_mpa": float(q_mpa),
        "trial_dimension": int(C_center.shape[1]),
        "rank_C_center": int(rank_C_center),
        "fiber_dimension": int(N_fiber.shape[1]),
        "rank_C_amp": int(np.linalg.matrix_rank(C_amp)),
        "rank_C_reg": int(np.linalg.matrix_rank(C_reg)),
        "center_constraint_singular_values": singular_values,
        "center_trace_block": exact_center_trace_block_report(obj),
        "selected_full_lift_rank": int(np.linalg.matrix_rank(P_sel_kkt)),
        "max_center_residual_selected_full_lift": float(
            np.max(np.abs(C_center @ P_sel_kkt - FULL_CENTER_TARGET))
        ),
        "max_stationarity_residual_selected_full_lift": float(
            np.max(np.abs(H_full @ P_sel_kkt + C_center.T @ multipliers_full_lift))
        ),
        "max_fiber_orthogonality_residual_selected_full_lift": float(
            np.max(np.abs(N_fiber.T @ H_full @ P_sel_kkt))
        ),
        "schur_condition_number": float(np.linalg.cond(schur)),
        "max_center_residual_closed_form_lift": float(
            np.max(np.abs(C_center @ P_sel_formula - FULL_CENTER_TARGET))
        ),
        "max_fiber_orthogonality_residual_closed_form_lift": float(
            np.max(np.abs(N_fiber.T @ H_full @ P_sel_formula))
        ),
        "max_amplitude_slice_from_lift_residual": float(np.max(np.abs(P_sel_kkt[:, :2] - M_full))),
        "max_center_residual_closed_form_amplitude": float(
            np.max(np.abs(C_center @ M_formula - AMP_TARGET))
        ),
        "max_fiber_orthogonality_residual_closed_form_amplitude": float(
            np.max(np.abs(N_fiber.T @ H_full @ M_formula))
        ),
        "max_center_residual_selected": float(np.max(np.abs(C_center @ M_full - AMP_TARGET))),
        "max_stationarity_residual_selected": float(
            np.max(np.abs(H_full @ M_full + C_center.T @ multipliers_full))
        ),
        "max_fiber_orthogonality_residual_selected": float(
            np.max(np.abs(N_fiber.T @ H_full @ M_full))
        ),
        "trace_plane_rank": int(np.linalg.matrix_rank(trace_basis)),
        "max_trace_plane_residual": float(np.max(np.abs(trace_basis - AMP_TARGET))),
        "max_trace_reconstruction_residual": float(np.max(np.abs(reconstructed_from_trace - M_full))),
        "trace_plane_rank_after_basis_change": int(np.linalg.matrix_rank(trace_basis_changed)),
        "max_trace_basis_change_residual": float(
            np.max(np.abs(trace_basis_changed - AMP_TARGET @ TRACE_BASIS_CHANGE_T))
        ),
        "max_trace_basis_change_reconstruction_residual": float(
            np.max(np.abs(reconstructed_from_changed_trace - (M_full @ TRACE_BASIS_CHANGE_T)))
        ),
        "max_center_residual_projection_candidate": float(
            np.max(np.abs(C_center @ M_proj - AMP_TARGET))
        ),
        "max_fiber_orthogonality_residual_projection_candidate": float(
            np.max(np.abs(N_fiber.T @ H_full @ M_proj))
        ),
        "max_selected_regularity_residual": float(np.max(np.abs(C_reg @ M_full))),
        "max_selected_amplitude_residual": float(np.max(np.abs(C_amp @ M_full - np.eye(2, dtype=float)))),
        "fiber_min_curvature": float(np.min(fiber_eigs)),
        "fiber_max_curvature": float(np.max(fiber_eigs)),
        "fiber_condition_number": float(np.linalg.cond(fiber_gram_sym)),
        "selected_full_objective": full_objectives,
        "constraint_only_reference_full_objective": ref_objectives,
        "reference_to_selected_objective_ratio": [
            float(ref_objectives[idx] / full_objectives[idx]) for idx in range(2)
        ],
        "local_row_surrogate_comparison": subset_reports,
    }


def main() -> None:
    config = high_bg.default_high_load_background_config()
    sample_objects = build_sample_objects(SAMPLE_POINTS, config=config)

    report = {
        "structural_reading": {
            "best_current_trace_map": (
                "The sharpest current repository-level trace candidate is the finite leading-center-jet map "
                "J_0(c) = C_center c. It records amplitudes together with the two leading regularity-defect rows."
            ),
            "compressed_amplitude_trace": (
                "The smaller map J_amp(c) = C_amp c keeps only the two amplitudes. On A_ls it becomes equivalent to J_0, "
                "but off A_ls it forgets the regularity-defect information."
            ),
            "higher_order_germ_warning": (
                "A higher-order local germ/jet extraction is not yet canonical on the current repository boundary, because the full intrinsic local selected family is still open."
            ),
            "amplitude_fiber": (
                "For fixed amplitudes a=(a1,a2), the current weighted ansatz defines the affine fiber "
                "F(a) = {c : C_center c = [a1, a2, 0, 0]}."
            ),
            "selected_full_center_lift": (
                "With H = A_int^T A_int + reg I and C = C_center, the KKT-selected full center-data lift is "
                "P_sel = H^(-1) C^T (C H^(-1) C^T)^(-1), characterized by C P_sel = I_4 and "
                "im(P_sel) being H-orthogonal to ker(C)."
            ),
            "selected_family": "The current repository family A_ls = im(M_amp) is the image of the KKT-selected map a -> c*(a).",
            "kkt_objective": "c*(a) minimizes ||A_int c||^2 + reg ||c||^2 subject to C_center c = [a1, a2, 0, 0].",
            "selected_family_as_slice": (
                "Equivalently, A_ls is the regularity-zero amplitude slice of the 4D selected center-data lift: "
                "A_ls = im(P_sel D_amp) = {c in im(P_sel) : C_reg c = 0}, with D_amp = [[I_2], [0]]."
            ),
            "trace_theorem_reading": (
                "At the current weighted-ansatz boundary, J_0(A_ls) is exactly the 2D plane im(D_amp) in the 4D center-data space, "
                "and J_0 restricted to A_ls is reconstructed uniquely by the inverse lift P_sel on that plane."
            ),
            "fiber_stationarity": "With H = A_int^T A_int + reg I, the KKT equations give H c*(a) + C_center^T lambda(a) = 0, so every feasible fiber direction z in ker(C_center) satisfies z^T H c*(a) = 0.",
            "projection_reading": (
                "If one first picks any feasible section c_ref(a) of the amplitude fiber, the selected representative is "
                "the H-orthogonal projection of c_ref(a) off the fiber directions ker(C_center)."
            ),
            "consequence": (
                "A_ls is therefore not merely a coordinate chart for center regularity; it is a globally interior-selected, H-minimal section of a much larger amplitude fiber."
            ),
            "locality_warning": (
                "Because H is built from the full collocation matrix A_int, the current selection rule is global in x. The repository does not yet exhibit a purely local center-only KKT law that reproduces the same selected family."
            ),
        },
        "samples": [
            per_sample_report(mode, q_mpa, sample_objects[(int(mode), float(q_mpa))])
            for mode, q_mpa in SAMPLE_POINTS
        ],
        "conclusion": {
            "what_is_closed_now": (
                "On representative clean points the current A_ls is confirmed to be the unique H-minimal KKT-selected family inside a 44-dimensional amplitude fiber of the weighted trial space, and its finite leading-center trace J_0(A_ls) is the 2D amplitude plane im(D_amp)."
            ),
            "what_is_not_closed": (
                "The current repository still does not provide a purely local intrinsic theorem-facing selector whose higher-order center-germ selection reproduces that same family."
            ),
            "most_plausible_reading": (
                "The best current theorem-facing trace object is the finite leading-center jet J_0 = C_center; the right next comparison partner is its selected image J_0(A_ls), not the full unrestricted local center-regular family."
            ),
        },
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
