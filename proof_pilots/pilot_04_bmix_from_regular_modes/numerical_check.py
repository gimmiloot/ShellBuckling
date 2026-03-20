from __future__ import annotations

from pathlib import Path
import inspect
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.mixed_weak import boundary_matrix_scan as broad_scan
from shell_buckling.mixed_weak import boundary_matrix_targeted_scan as targeted_scan


TOL_REG = 1.0e-8
TOL_DIFF = 1.0e-6
RAW_VIOLATION_FLOOR = 1.0e-4


def print_check(name: str, ok: bool, detail: str) -> bool:
    print(f"[{name}] {'PASS' if ok else 'FAIL'}")
    print(f"  {detail}")
    return ok


def max_abs(arr: np.ndarray) -> float:
    return float(np.max(np.abs(np.asarray(arr, dtype=float))))


def matrix_rank(arr: np.ndarray, tol: float = TOL_DIFF) -> int:
    return int(np.linalg.matrix_rank(np.asarray(arr, dtype=float), tol=tol))


def orthonormal_basis(arr: np.ndarray, tol: float = TOL_DIFF) -> np.ndarray:
    q, r = np.linalg.qr(np.asarray(arr, dtype=float), mode="reduced")
    keep = []
    for j in range(r.shape[1]):
        if abs(float(r[j, j])) > tol:
            keep.append(j)
    if not keep:
        return np.zeros((arr.shape[0], 0), dtype=float)
    return q[:, keep]


def projector_distance(a: np.ndarray, b: np.ndarray, tol: float = TOL_DIFF) -> float:
    qa = orthonormal_basis(a, tol=tol)
    qb = orthonormal_basis(b, tol=tol)
    pa = qa @ qa.T
    pb = qb @ qb.T
    return float(np.linalg.norm(pa - pb))


def solve_background(scan_module, p_target: float, nd_bvp: int = 600):
    mw = scan_module.mw
    p_grid = np.linspace(0.0, float(p_target), 5, dtype=float)
    _, sols = mw.solve_axisymmetric_fmin_continuation(
        p_grid,
        nd_bvp=nd_bvp,
        x0=1.0e-3,
        tol=1.0e-4,
        max_nodes=150000,
        verbose=False,
    )
    return sols[-1]


def raw_surrogate_modes(obj) -> np.ndarray:
    _u, _s, vh = np.linalg.svd(obj.A_int, full_matrices=False)
    return vh[-2:, :].T


def normalized_center_block(center_values: np.ndarray) -> tuple[int, np.ndarray | None, float]:
    top = np.asarray(center_values[:2, :], dtype=float)
    rank_top = matrix_rank(top)
    if rank_top != 2:
        return rank_top, None, float("inf")
    rebasing = np.linalg.inv(top)
    rebased = np.asarray(center_values, dtype=float) @ rebasing
    target = np.array(
        [
            [1.0, 0.0],
            [0.0, 1.0],
            [0.0, 0.0],
            [0.0, 0.0],
        ],
        dtype=float,
    )
    return rank_top, rebased, max_abs(rebased - target)


def source_guard(module_name: str, scan_module) -> bool:
    ok_all = True
    module_src = inspect.getsource(scan_module)
    build_src = inspect.getsource(scan_module.build_boundary_matrix_test_v2)

    checks = [
        (
            "module states regular modes are not raw smallest singular vectors",
            "NOT taken as the two smallest right-singular" in module_src,
        ),
        ("uses center constraint matrix", "C_center = make_center_constraint_matrix" in build_src),
        ("uses target d1 for mode 1", "d1 = np.array([1.0, 0.0, 0.0, 0.0]" in build_src),
        ("uses target d2 for mode 2", "d2 = np.array([0.0, 1.0, 0.0, 0.0]" in build_src),
        ("forms V_reg from constrained modes", "V_reg = np.column_stack([c1, c2])" in build_src),
        ("forms B_mix from V_reg", "B_mix = B_full @ V_reg" in build_src),
    ]

    print(f"Source guard for {module_name}:")
    for label, ok in checks:
        ok_all &= ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    print()
    return ok_all


def run_case(module_name: str, scan_module, p_target: float = 3.8, n_mode: int = 13) -> dict[str, object]:
    print(f"=== Numerical V-S5 check: {module_name} ===")
    print(f"objects tested: build_boundary_matrix_test_v2, n={n_mode}, p={p_target:.3f} MPa")
    print("Expected result in the current repository:")
    print("  the live workflow should build B_mix from constrained center-regular modes;")
    print("  raw surrogate directions should violate the active center regularity rows;")
    print("  replacing the regular pair by raw surrogate directions should change the construction in the current repository sense.")
    print()

    src_ok = source_guard(module_name, scan_module)
    sol = solve_background(scan_module, p_target=p_target)
    obj = scan_module.build_boundary_matrix_test_v2(
        n=n_mode,
        sol=sol,
        p_mpa=float(p_target),
        x0=1.0e-3,
        m_basis=6,
        n_collocation=120,
        nd_base=2000,
    )

    v_reg = np.asarray(obj.V_reg, dtype=float)
    center_reg = np.asarray(obj.center_values, dtype=float)
    b_reg = np.asarray(obj.B_mix, dtype=float)

    v_raw = raw_surrogate_modes(obj)
    center_raw = np.asarray(obj.C_center @ v_raw, dtype=float)
    b_raw = np.asarray(obj.B_full @ v_raw, dtype=float)

    reg_regularity = center_reg[2:, :]
    raw_regularity = center_raw[2:, :]
    reg_regularity_error = max_abs(reg_regularity)
    raw_regularity_error = max_abs(raw_regularity)

    reg_top = center_reg[:2, :]
    raw_top = center_raw[:2, :]
    reg_top_rank, reg_rebased, reg_rebased_error = normalized_center_block(center_reg)
    raw_top_rank, raw_rebased, raw_rebased_error = normalized_center_block(center_raw)

    coeff_space_distance = projector_distance(v_reg, v_raw)
    boundary_space_distance = projector_distance(b_reg, b_raw)
    b_matrix_difference = float(np.linalg.norm(b_reg - b_raw))
    sigma_reg = np.linalg.svd(b_reg, compute_uv=False)
    sigma_raw = np.linalg.svd(b_raw, compute_uv=False)

    print("A. Current workflow check")
    print("center values of the actual regular-mode pair:")
    with np.printoptions(precision=6, suppress=True):
        print(center_reg)
    print()

    print("regularity rows of the actual regular-mode pair:")
    with np.printoptions(precision=6, suppress=True):
        print(reg_regularity)
    print()

    if reg_rebased is not None:
        print("actual regular-mode pair after re-basing to the normalized center targets:")
        with np.printoptions(precision=6, suppress=True):
            print(reg_rebased)
        print()

    print("B. Raw surrogate-direction comparison")
    print("center values of the raw two smallest right-singular vectors of A_int:")
    with np.printoptions(precision=6, suppress=True):
        print(center_raw)
    print()

    print("regularity rows of the raw surrogate pair:")
    with np.printoptions(precision=6, suppress=True):
        print(raw_regularity)
    print()

    if raw_rebased is not None:
        print("raw surrogate pair after top-block normalization:")
        with np.printoptions(precision=6, suppress=True):
            print(raw_rebased)
        print()

    print("C. Boundary matrix comparison")
    print("B_mix from the actual regular-mode pair:")
    with np.printoptions(precision=6, suppress=True):
        print(b_reg)
    print()

    print("comparison boundary matrix from the raw surrogate pair:")
    with np.printoptions(precision=6, suppress=True):
        print(b_raw)
    print()

    print("singular values of B_mix from actual regular modes:")
    with np.printoptions(precision=6, suppress=True):
        print(sigma_reg)
    print()

    print("singular values of comparison matrix from raw surrogate directions:")
    with np.printoptions(precision=6, suppress=True):
        print(sigma_raw)
    print()

    checks = [
        print_check(
            "actual build path uses constrained regular modes",
            src_ok,
            "source guards confirm B_mix is formed as B_full @ V_reg with V_reg built from constrained center targets",
        ),
        print_check(
            "actual regular-mode pair has two columns",
            v_reg.shape[1] == 2,
            f"V_reg shape = {v_reg.shape}",
        ),
        print_check(
            "actual regular-mode pair satisfies active center regularity rows",
            reg_regularity_error < TOL_REG,
            f"max |regularity rows on V_reg| = {reg_regularity_error:.3e}",
        ),
        print_check(
            "actual regular-mode pair has rank-2 center-leading block",
            reg_top_rank == 2,
            f"rank(center_reg[:2, :]) = {reg_top_rank}",
        ),
        print_check(
            "actual regular-mode span recovers the normalized center pair",
            reg_rebased_error < TOL_REG,
            f"max |rebased_center_reg - target| = {reg_rebased_error:.3e}",
        ),
        print_check(
            "raw surrogate pair violates active center regularity rows",
            raw_regularity_error > RAW_VIOLATION_FLOOR,
            f"max |regularity rows on V_raw| = {raw_regularity_error:.3e}",
        ),
        print_check(
            "raw surrogate span differs from the regular coefficient-space span",
            coeff_space_distance > TOL_DIFF,
            f"projector distance in coefficient space = {coeff_space_distance:.3e}",
        ),
        print_check(
            "boundary construction differs numerically from the raw surrogate comparison",
            b_matrix_difference > TOL_DIFF or boundary_space_distance > TOL_DIFF,
            f"||B_mix_reg - B_mix_raw|| = {b_matrix_difference:.3e}, boundary-space projector distance = {boundary_space_distance:.3e}",
        ),
    ]
    print()

    actual_uses_regular = bool(src_ok and reg_regularity_error < TOL_REG and reg_top_rank == 2)
    raw_is_not_regular = bool(raw_regularity_error > RAW_VIOLATION_FLOOR)
    replacement_changes_meaningfully = bool(
        raw_is_not_regular and (coeff_space_distance > TOL_DIFF or boundary_space_distance > TOL_DIFF or b_matrix_difference > TOL_DIFF)
    )
    case_pass = all(checks)

    print("D. Final explicit conclusion")
    print(f"  Current repository uses center-regular modes for B_mix: {'YES' if actual_uses_regular else 'NO'}")
    print(f"  Raw surrogate directions satisfy the active center constraints: {'YES' if not raw_is_not_regular else 'NO'}")
    print(f"  Replacing V_reg by raw surrogate directions changes the construction meaningfully: {'YES' if replacement_changes_meaningfully else 'NO'}")
    print(f"  PASS/FAIL for this case: {'PASS' if case_pass else 'FAIL'}")
    print()

    return {
        "module": module_name,
        "src_ok": src_ok,
        "actual_uses_regular": actual_uses_regular,
        "raw_is_not_regular": raw_is_not_regular,
        "replacement_changes_meaningfully": replacement_changes_meaningfully,
        "reg_regularity_error": reg_regularity_error,
        "raw_regularity_error": raw_regularity_error,
        "reg_top_rank": reg_top_rank,
        "raw_top_rank": raw_top_rank,
        "coeff_space_distance": coeff_space_distance,
        "boundary_space_distance": boundary_space_distance,
        "b_matrix_difference": b_matrix_difference,
        "sigma_reg_min": float(sigma_reg[-1]),
        "sigma_raw_min": float(sigma_raw[-1]),
        "case_pass": case_pass,
    }


def main() -> int:
    results = [
        run_case("broad simple-support path", broad_scan),
        run_case("targeted patched path", targeted_scan),
    ]

    overall_pass = all(result["case_pass"] for result in results)

    print("Overall summary:")
    for result in results:
        print(
            f"  {result['module']}: "
            f"{'PASS' if result['case_pass'] else 'FAIL'} | "
            f"actual_uses_regular={'YES' if result['actual_uses_regular'] else 'NO'} | "
            f"raw_is_not_regular={'YES' if result['raw_is_not_regular'] else 'NO'} | "
            f"replacement_changes_meaningfully={'YES' if result['replacement_changes_meaningfully'] else 'NO'} | "
            f"reg_error={result['reg_regularity_error']:.3e} | "
            f"raw_error={result['raw_regularity_error']:.3e} | "
            f"coeff_space_diff={result['coeff_space_distance']:.3e} | "
            f"boundary_space_diff={result['boundary_space_distance']:.3e} | "
            f"||B_reg-B_raw||={result['b_matrix_difference']:.3e} | "
            f"sigma_min(B_reg)={result['sigma_reg_min']:.3e} | "
            f"sigma_min(B_raw)={result['sigma_raw_min']:.3e}"
        )
    print()
    print(
        "OVERALL: "
        + ("PASS" if overall_pass else "FAIL")
        + "  (for the current surrogate/testbench B_mix construction rule)"
    )
    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
