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


def print_check(name: str, ok: bool, detail: str) -> bool:
    print(f"[{name}] {'PASS' if ok else 'FAIL'}")
    print(f"  {detail}")
    return ok


def source_guard(module_name: str, scan_module) -> bool:
    ok_all = True
    build_src = inspect.getsource(scan_module.build_boundary_matrix_test_v2)
    center_src = inspect.getsource(scan_module.make_center_constraint_matrix)

    checks = [
        ("uses make_center_constraint_matrix", "C_center = make_center_constraint_matrix" in build_src),
        ("uses constrained solve for mode 1", "c1 = solve_constrained_mode" in build_src),
        ("uses constrained solve for mode 2", "c2_raw = solve_constrained_mode" in build_src),
        ("orthogonalizes second mode", "c2 = orthogonalize_against(c2_raw, c1)" in build_src),
        (
            "center rows include current regularity relations",
            "u_n / x^n + (lambda_c / n) * phi / x^(n-1)" in center_src
            and "psi / x^(n-1) - lambda_c * phi / x^(n-1)" in center_src,
        ),
    ]

    print(f"Source guard for {module_name}:")
    for label, ok in checks:
        ok_all &= ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    print()
    return ok_all


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


def svd_mode_center_values(obj) -> np.ndarray:
    _u, _s, vh = np.linalg.svd(obj.A_int, full_matrices=False)
    raw = vh[-2:, :].T
    return obj.C_center @ raw


def max_abs(arr: np.ndarray) -> float:
    return float(np.max(np.abs(arr)))


def run_case(module_name: str, scan_module, p_target: float = 3.8, n_mode: int = 13) -> dict[str, object]:
    print(f"=== Numerical V-S4 check: {module_name} ===")
    print(f"objects tested: build_boundary_matrix_test_v2, make_center_constraint_matrix, n={n_mode}, p={p_target:.3f} MPa")
    print(
        "regular-at-center criterion: "
        "[u_s/x^n, phi/x^(n-1), u_n/x^n + (lambda_c/n)phi/x^(n-1), psi/x^(n-1)-lambda_c phi/x^(n-1)]"
    )
    print("stored basis note: the current workflow orthogonalizes the second mode after the constrained solve,")
    print("so the invariant checked here is regularity of the span plus invertibility of the top 2x2 center block.")
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

    target = np.array(
        [
            [1.0, 0.0],
            [0.0, 1.0],
            [0.0, 0.0],
            [0.0, 0.0],
        ],
        dtype=float,
    )
    top_block = obj.center_values[:2, :]
    regularity_block = obj.center_values[2:, :]
    regularity_error = max_abs(regularity_block)
    rank_vreg = int(np.linalg.matrix_rank(obj.V_reg))
    top_rank = int(np.linalg.matrix_rank(top_block))

    if top_rank == 2:
        rebasing = np.linalg.inv(top_block)
        rebased_center = obj.center_values @ rebasing
        rebased_error = max_abs(rebased_center - target)
    else:
        rebasing = None
        rebased_center = None
        rebased_error = float("inf")

    svd_center = svd_mode_center_values(obj)
    svd_regularity_error = max_abs(svd_center[2:, :])

    print("center values of constructed modes:")
    with np.printoptions(precision=6, suppress=True):
        print(obj.center_values)
    print()

    print("top 2x2 center-leading block of constructed modes:")
    with np.printoptions(precision=6, suppress=True):
        print(top_block)
    print()

    print("regularity rows of constructed modes:")
    with np.printoptions(precision=6, suppress=True):
        print(regularity_block)
    print()

    if rebased_center is not None:
        print("center values after re-basing within the constructed two-mode span:")
        with np.printoptions(precision=6, suppress=True):
            print(rebased_center)
        print()

    print("center values of the raw two smallest right-singular vectors of A_int:")
    with np.printoptions(precision=6, suppress=True):
        print(svd_center)
    print()

    checks = [
        print_check(
            "two constructed modes",
            obj.V_reg.shape[1] == 2,
            f"V_reg shape = {obj.V_reg.shape}",
        ),
        print_check(
            "two independent constructed modes",
            rank_vreg == 2,
            f"rank(V_reg) = {rank_vreg}",
        ),
        print_check(
            "constructed modes satisfy current center regularity rows",
            regularity_error < 1.0e-8,
            f"max |regularity rows| = {regularity_error:.3e}",
        ),
        print_check(
            "constructed modes span two independent center-leading directions",
            top_rank == 2,
            f"rank(center_values[:2, :]) = {top_rank}",
        ),
        print_check(
            "constructed span recovers the normalized regular family after re-basing",
            rebased_error < 1.0e-8,
            f"max |rebased_center - target| = {rebased_error:.3e}",
        ),
        print_check(
            "residual norms are finite",
            bool(np.all(np.isfinite(obj.residual_norms))),
            f"residual norms = {obj.residual_norms}",
        ),
        print_check(
            "not merely using raw surrogate-nullspace vectors",
            src_ok and svd_regularity_error > 1.0e-4,
            f"source uses constrained solve; raw SVD max |regularity rows| = {svd_regularity_error:.3e}",
        ),
    ]
    print()

    partial_support = all(checks)
    print(
        "Conclusion: "
        + ("PASS" if partial_support else "FAIL")
        + " for the current workflow check."
    )
    print(
        "Interpretation: this supports the statement that the current implementation "
        "constructs exactly two center-regular directions in the repository sense; "
        "it does not by itself prove an article-level uniqueness theorem for the full differential system."
    )
    print()

    return {
        "module": module_name,
        "source_ok": src_ok,
        "regularity_error": regularity_error,
        "rebased_error": rebased_error,
        "svd_regularity_error": svd_regularity_error,
        "rank_vreg": rank_vreg,
        "top_rank": top_rank,
        "checks_ok": partial_support,
    }


def main() -> int:
    results = [
        run_case("broad simple-support path", broad_scan),
        run_case("targeted patched path", targeted_scan),
    ]

    all_ok = all(result["checks_ok"] for result in results)
    print("Overall summary:")
    for result in results:
        print(
            f"  {result['module']}: "
            f"{'PASS' if result['checks_ok'] else 'FAIL'} | "
            f"regularity_error={result['regularity_error']:.3e} | "
            f"rebased_error={result['rebased_error']:.3e} | "
            f"raw_svd_regularity_error={result['svd_regularity_error']:.3e} | "
            f"rank(V_reg)={result['rank_vreg']} | "
            f"rank(center-top)={result['top_rank']}"
        )
    print()
    print(
        "OVERALL: "
        + ("PASS" if all_ok else "FAIL")
        + "  (for the current surrogate/testbench center-mode workflow)"
    )
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
