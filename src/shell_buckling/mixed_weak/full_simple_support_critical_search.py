# -*- coding: utf-8 -*-
"""
Standalone clean critical-load search for the full hinged / simple-support task.

This module reconnects the mixed-weak boundary-matrix search to the honest
6-state axisymmetric simple-support background path instead of the older
hybrid F_min-backed testbench line.
"""
from __future__ import annotations

from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from shell_buckling.mixed_weak import axisymmetric_simple_support_background as simple_bg
from shell_buckling.mixed_weak import simple_support_high_load_background_continuation as high_bg
from shell_buckling.mixed_weak import solver_patched_core as mw


BACKGROUND_BC_LABELS = tuple(simple_bg.BC_LABELS)
CRITICAL_BOUNDARY_ROW_LABELS = ("u_n(1)", "varphi(1)", "T_s(1)", "S(1)", "H(1)")
DEFAULT_SIMPLE_SUPPORT_CRITICAL_MODES = (2, 3, 4, 5, 6)
DEFAULT_P_MIN_MPA = 0.0
DEFAULT_P_MAX_MPA = 15.0
DEFAULT_P_NPTS = 31
ROW_SCALE = np.array([1.0, 1.0, 1.0, 2.0 * (1.0 + mw.nu), mw.C_twist], dtype=float)


@dataclass
class BoundaryMatrixObjects:
    n: int
    q_mpa: float
    space: mw.TrialSpace
    base: mw.BaseInterp
    A_int: np.ndarray
    B_full: np.ndarray
    C_center: np.ndarray
    V_reg: np.ndarray
    B_mix: np.ndarray
    residual_norms: np.ndarray
    sigma_raw: float
    sigma_bal: float
    sigma_bal_noH: float


@dataclass(frozen=True)
class FullSimpleSupportCriticalPoint:
    n: int
    q_mpa: float
    sigma_raw: float
    sigma_bal: float
    sigma_bal_noH: float
    residual_norms: tuple[float, float]
    background_seed_kind: str


@dataclass
class FullSimpleSupportCriticalSearchResult:
    load_grid_mpa: np.ndarray
    modes: tuple[int, ...]
    background_results: list[simple_bg.AxisymmetricBackgroundSolve]
    points_by_mode: dict[int, list[FullSimpleSupportCriticalPoint]]

    def successful_background_results(self) -> list[simple_bg.AxisymmetricBackgroundSolve]:
        return [result for result in self.background_results if result.success and result.solution is not None]

    def first_background_failure(self) -> simple_bg.AxisymmetricBackgroundSolve | None:
        return next((result for result in self.background_results if not result.success), None)

    def best_point_for_mode(self, n: int) -> FullSimpleSupportCriticalPoint | None:
        points = self.points_by_mode.get(int(n), [])
        if not points:
            return None
        return min(points, key=lambda point: point.sigma_bal)

    def best_point_overall(self) -> FullSimpleSupportCriticalPoint | None:
        best: FullSimpleSupportCriticalPoint | None = None
        for n in self.modes:
            candidate = self.best_point_for_mode(n)
            if candidate is None:
                continue
            if best is None or candidate.sigma_bal < best.sigma_bal:
                best = candidate
        return best


def default_load_grid(
    p_min_mpa: float = DEFAULT_P_MIN_MPA,
    p_max_mpa: float = DEFAULT_P_MAX_MPA,
    p_npts: int = DEFAULT_P_NPTS,
) -> np.ndarray:
    if int(p_npts) < 2:
        raise ValueError("p_npts must be at least 2.")
    if float(p_max_mpa) < float(p_min_mpa):
        raise ValueError("p_max_mpa must be greater than or equal to p_min_mpa.")
    return np.linspace(float(p_min_mpa), float(p_max_mpa), int(p_npts), dtype=float)


def balanced_Bmix(B: np.ndarray) -> np.ndarray:
    return ROW_SCALE[:, None] * np.asarray(B, dtype=float)


def build_full_simple_support_base_interp(
    sol,
    q_mpa: float,
    nd_base: int = 4000,
) -> mw.BaseInterp:
    q_pa = float(q_mpa) * 1.0e6
    qbar = q_pa * mw.a / (mw.E * mw.h)

    xb = np.linspace(float(sol.x[0]), 1.0, int(nd_base), dtype=float)
    yb = sol.sol(xb)

    T_s0 = yb[0]
    T_sn0 = yb[1]
    M_s0 = yb[2]
    u_r0 = yb[3]
    varphi0 = yb[5]

    x_safe = np.maximum(xb, 1.0e-12)
    r0 = np.maximum(xb + u_r0, 1.0e-12)
    e_theta0 = u_r0 / x_safe
    e_s0 = (1.0 - mw.nu**2) * T_s0 - mw.nu * e_theta0
    T_theta0 = mw.nu * T_s0 + e_theta0
    M_theta0 = mw.nu * M_s0 + np.sin(varphi0) / (12.0 * mw.mu**2 * r0)
    varphi0_prime = 12.0 * (1.0 - mw.nu**2) * M_s0 * mw.mu**2 - mw.nu * np.sin(varphi0) / r0

    yprime = simple_bg.axisymmetric_simple_support_ode(xb, yb, q_pa=q_pa)
    r0_prime = 1.0 + yprime[3]
    r0_double_prime = np.gradient(r0_prime, xb, edge_order=2)
    z0_prime = yprime[4] / mw.mu
    z0 = mw.cumulative_trapezoid_from_values(xb, z0_prime)

    return mw.BaseInterp(
        xb=xb,
        r=r0,
        r_prime=r0_prime,
        r_double_prime=r0_double_prime,
        z=z0,
        T_s=T_s0,
        T_sn=T_sn0,
        M_s=M_s0,
        varphi=varphi0,
        varphi_prime=varphi0_prime,
        e_s=e_s0,
        T_theta=T_theta0,
        M_theta=M_theta0,
        q=qbar,
    )


def assemble_interior_and_boundary(
    n: int,
    base: mw.BaseInterp,
    x0: float,
    m_basis: int = 6,
    n_collocation: int = 120,
) -> tuple[mw.TrialSpace, np.ndarray, np.ndarray, np.ndarray]:
    space = mw.TrialSpace(n=int(n), x0=float(x0), m_basis=int(m_basis))
    x_col = np.linspace(float(x0), 1.0, int(n_collocation) + 2, dtype=float)[1:-1]
    n_eq = 8 * x_col.size
    n_unknowns = space.n_unknowns
    A_int = np.zeros((n_eq, n_unknowns), dtype=float)
    B_full = np.zeros((5, n_unknowns), dtype=float)
    for col in range(n_unknowns):
        resid, bvec = mw.assemble_operator_column(x_col, base, space, col)
        A_int[:, col] = resid.reshape(-1, order="F")
        B_full[:, col] = bvec
    return space, x_col, A_int, B_full

def make_center_constraint_matrix(space: mw.TrialSpace, base: mw.BaseInterp) -> np.ndarray:
    x0 = np.array([space.x0], dtype=float)
    b0 = base.at_many(x0)
    lam_c = float(b0["lambda_s0"][0])
    n = space.n
    C = np.zeros((4, space.n_unknowns), dtype=float)
    xpow_us = space.x0 ** n
    xpow_phi = space.x0 ** (n - 1)

    for col in range(space.n_unknowns):
        vals = space.basis_eval(x0, col)
        us = float(vals["u_s"][0]) / xpow_us
        un = float(vals["u_n"][0]) / xpow_us
        phi = float(vals["phi"][0]) / xpow_phi
        psi = float(vals["psi"][0]) / xpow_phi
        C[0, col] = us
        C[1, col] = phi
        C[2, col] = un + (lam_c / n) * phi
        C[3, col] = psi - lam_c * phi
    return C


def solve_constrained_mode(A: np.ndarray, C: np.ndarray, d: np.ndarray, reg: float = 1.0e-12) -> np.ndarray:
    n_unknowns = A.shape[1]
    n_constraints = C.shape[0]
    ATA = A.T @ A + reg * np.eye(n_unknowns)
    KKT = np.block(
        [
            [ATA, C.T],
            [C, np.zeros((n_constraints, n_constraints), dtype=float)],
        ]
    )
    rhs = np.concatenate([np.zeros(n_unknowns, dtype=float), d.astype(float)])
    sol = np.linalg.solve(KKT, rhs)
    coeffs = sol[:n_unknowns]
    norm = np.linalg.norm(coeffs)
    if norm > 0.0:
        coeffs = coeffs / norm
    return coeffs


def orthogonalize_against(c: np.ndarray, ref: np.ndarray) -> np.ndarray:
    c = c - ref * np.dot(ref, c)
    norm = np.linalg.norm(c)
    if norm > 0.0:
        c = c / norm
    return c


def build_boundary_matrix_objects(
    n: int,
    background_result: simple_bg.AxisymmetricBackgroundSolve,
    x0: float,
    m_basis: int = 6,
    n_collocation: int = 120,
    nd_base: int = 4000,
) -> BoundaryMatrixObjects:
    if not background_result.success or background_result.solution is None:
        raise ValueError("Boundary-matrix assembly requires a converged background result.")

    base = build_full_simple_support_base_interp(
        background_result.solution,
        q_mpa=background_result.q_mpa,
        nd_base=nd_base,
    )
    space, _x_col, A_int, B_full = assemble_interior_and_boundary(
        n=n,
        base=base,
        x0=x0,
        m_basis=m_basis,
        n_collocation=n_collocation,
    )
    C_center = make_center_constraint_matrix(space, base)

    c1 = solve_constrained_mode(A_int, C_center, np.array([1.0, 0.0, 0.0, 0.0], dtype=float))
    c2_raw = solve_constrained_mode(A_int, C_center, np.array([0.0, 1.0, 0.0, 0.0], dtype=float))
    c2 = orthogonalize_against(c2_raw, c1)

    V_reg = np.column_stack([c1, c2])
    B_mix = B_full @ V_reg
    residual_norms = np.array([np.linalg.norm(A_int @ c1), np.linalg.norm(A_int @ c2)], dtype=float)
    sigma_raw = float(np.linalg.svd(B_mix, compute_uv=False)[-1])
    B_bal = balanced_Bmix(B_mix)
    sigma_bal = float(np.linalg.svd(B_bal, compute_uv=False)[-1])
    sigma_bal_noH = float(np.linalg.svd(B_bal[:4, :], compute_uv=False)[-1])

    return BoundaryMatrixObjects(
        n=int(n),
        q_mpa=float(background_result.q_mpa),
        space=space,
        base=base,
        A_int=A_int,
        B_full=B_full,
        C_center=C_center,
        V_reg=V_reg,
        B_mix=B_mix,
        residual_norms=residual_norms,
        sigma_raw=sigma_raw,
        sigma_bal=sigma_bal,
        sigma_bal_noH=sigma_bal_noH,
    )


def run_full_simple_support_critical_search(
    load_grid_mpa: Sequence[float],
    modes: Sequence[int] = DEFAULT_SIMPLE_SUPPORT_CRITICAL_MODES,
    background_config: simple_bg.AxisymmetricSimpleSupportConfig | None = None,
    x0: float | None = None,
    m_basis: int = 6,
    n_collocation: int = 120,
    nd_base: int = 4000,
    verbose: bool = True,
) -> FullSimpleSupportCriticalSearchResult:
    load_grid = np.asarray(load_grid_mpa, dtype=float)
    modes_tuple = tuple(int(mode) for mode in modes)
    if not modes_tuple:
        raise ValueError("At least one circumferential mode must be requested.")
    if background_config is None:
        background_config = high_bg.default_high_load_background_config()
    if x0 is None:
        x0 = float(background_config.x0)

    background_results = high_bg.solve_axisymmetric_simple_support_high_load_schedule(
        load_grid.tolist(),
        config=background_config,
        verbose=verbose,
    )
    points_by_mode: dict[int, list[FullSimpleSupportCriticalPoint]] = {mode: [] for mode in modes_tuple}

    for i, background_result in enumerate(background_results):
        if not background_result.success:
            if verbose:
                print(
                    "[full-simple-support-bg-fail] "
                    f"i={i:03d} q={background_result.q_mpa:.6f} MPa "
                    f"seed={background_result.seed_kind} message={background_result.message}"
                )
            break

        mode_logs: list[str] = []
        for mode in modes_tuple:
            obj = build_boundary_matrix_objects(
                n=mode,
                background_result=background_result,
                x0=x0,
                m_basis=m_basis,
                n_collocation=n_collocation,
                nd_base=nd_base,
            )
            point = FullSimpleSupportCriticalPoint(
                n=mode,
                q_mpa=float(background_result.q_mpa),
                sigma_raw=obj.sigma_raw,
                sigma_bal=obj.sigma_bal,
                sigma_bal_noH=obj.sigma_bal_noH,
                residual_norms=(float(obj.residual_norms[0]), float(obj.residual_norms[1])),
                background_seed_kind=background_result.seed_kind,
            )
            points_by_mode[mode].append(point)
            mode_logs.append(f"n={mode}: sigma_bal={obj.sigma_bal:.6e}")

        if verbose and (i % 5 == 0 or i == len(background_results) - 1):
            print(
                "[full-simple-support-critical] "
                f"i={i:03d} q={background_result.q_mpa:.6f} MPa "
                f"seed={background_result.seed_kind} | "
                + " | ".join(mode_logs)
            )

    return FullSimpleSupportCriticalSearchResult(
        load_grid_mpa=load_grid,
        modes=modes_tuple,
        background_results=background_results,
        points_by_mode=points_by_mode,
    )

def print_search_header(
    load_grid_mpa: Sequence[float],
    modes: Sequence[int],
    background_config: simple_bg.AxisymmetricSimpleSupportConfig,
    m_basis: int,
    n_collocation: int,
    nd_base: int,
) -> None:
    print("=== Full simple-support critical-load search ===")
    print("background source: src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py")
    print("background continuation: src/shell_buckling/mixed_weak/simple_support_high_load_background_continuation.py")
    print("background BCs: " + "; ".join(BACKGROUND_BC_LABELS[:3]) + "; " + "; ".join(BACKGROUND_BC_LABELS[3:]))
    print("critical boundary rows: [" + ", ".join(CRITICAL_BOUNDARY_ROW_LABELS) + "]")
    print("modes: " + ", ".join(str(int(mode)) for mode in modes))
    print(
        "load grid: "
        f"{float(load_grid_mpa[0]):.6f} .. {float(load_grid_mpa[-1]):.6f} MPa "
        f"({len(load_grid_mpa)} points)"
    )
    print(
        "discretization: "
        f"nd_bvp={background_config.nd_bvp}, m_basis={int(m_basis)}, "
        f"n_collocation={int(n_collocation)}, nd_base={int(nd_base)}"
    )
    print("legacy targeted windows: disabled in this standalone runner")
    print("hybrid F_min background reuse: disabled in this standalone runner")


def print_search_summary(result: FullSimpleSupportCriticalSearchResult) -> None:
    success_backgrounds = result.successful_background_results()
    print("\n=== Background summary ===")
    print(f"successful background solves: {len(success_backgrounds)} / {len(result.load_grid_mpa)}")
    failure = result.first_background_failure()
    if failure is None:
        print("first background failure: not reached in the scheduled load grid")
    else:
        print(
            "first background failure: "
            f"q={failure.q_mpa:.6f} MPa seed={failure.seed_kind} message={failure.message}"
        )

    print("\n=== Critical-search summary (balanced boundary metric) ===")
    for mode in result.modes:
        best_point = result.best_point_for_mode(mode)
        if best_point is None:
            print(f"n={mode:02d}: no successful boundary-matrix points")
            continue
        print(
            f"n={mode:02d}: best q={best_point.q_mpa:.6f} MPa  "
            f"sigma_bal={best_point.sigma_bal:.6e}  sigma_raw={best_point.sigma_raw:.6e}  "
            f"sigma_bal_noH={best_point.sigma_bal_noH:.6e}  seed={best_point.background_seed_kind}"
        )

    best_overall = result.best_point_overall()
    if best_overall is not None:
        print("\n=== Cross-mode best point ===")
        print(
            f"n={best_overall.n:02d} at q={best_overall.q_mpa:.6f} MPa  "
            f"sigma_bal={best_overall.sigma_bal:.6e}"
        )


def build_arg_parser() -> ArgumentParser:
    defaults = high_bg.default_high_load_background_config()
    parser = ArgumentParser(
        description=(
            "Standalone clean mixed-weak critical-load search for the full "
            "simple-support task using the honest 6-state axisymmetric background."
        )
    )
    parser.add_argument("--p-min-mpa", type=float, default=DEFAULT_P_MIN_MPA)
    parser.add_argument("--p-max-mpa", type=float, default=DEFAULT_P_MAX_MPA)
    parser.add_argument("--p-npts", type=int, default=DEFAULT_P_NPTS)
    parser.add_argument(
        "--modes",
        nargs="+",
        type=int,
        default=list(DEFAULT_SIMPLE_SUPPORT_CRITICAL_MODES),
        help="Circumferential modes to scan. The default first-pass range is n=2..6.",
    )
    parser.add_argument("--x0", type=float, default=defaults.x0)
    parser.add_argument("--nd-bvp", type=int, default=defaults.nd_bvp)
    parser.add_argument("--tol", type=float, default=defaults.tol)
    parser.add_argument("--relaxed-tol", type=float, default=defaults.relaxed_tol)
    parser.add_argument("--max-nodes", type=int, default=defaults.max_nodes)
    parser.add_argument("--template-q-mpa", type=float, default=defaults.template_q_mpa)
    parser.add_argument("--right-edge-cluster-start", type=float, default=defaults.right_edge_cluster_start)
    parser.add_argument("--right-edge-cluster-fraction", type=float, default=defaults.right_edge_cluster_fraction)
    parser.add_argument("--right-edge-cluster-power", type=float, default=defaults.right_edge_cluster_power)
    parser.add_argument("--m-basis", type=int, default=6)
    parser.add_argument("--n-collocation", type=int, default=120)
    parser.add_argument("--nd-base", type=int, default=4000)
    parser.add_argument("--quiet", action="store_true")
    return parser


def background_config_from_args(args: Namespace) -> simple_bg.AxisymmetricSimpleSupportConfig:
    return simple_bg.AxisymmetricSimpleSupportConfig(
        x0=float(args.x0),
        nd_bvp=int(args.nd_bvp),
        tol=float(args.tol),
        relaxed_tol=float(args.relaxed_tol),
        max_nodes=int(args.max_nodes),
        template_q_mpa=float(args.template_q_mpa),
        right_edge_cluster_start=float(args.right_edge_cluster_start),
        right_edge_cluster_fraction=float(args.right_edge_cluster_fraction),
        right_edge_cluster_power=float(args.right_edge_cluster_power),
    )

def main(argv: Sequence[str] | None = None) -> FullSimpleSupportCriticalSearchResult:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    load_grid = default_load_grid(args.p_min_mpa, args.p_max_mpa, args.p_npts)
    background_config = background_config_from_args(args)
    modes = tuple(int(mode) for mode in args.modes)

    if not args.quiet:
        print_search_header(
            load_grid_mpa=load_grid,
            modes=modes,
            background_config=background_config,
            m_basis=int(args.m_basis),
            n_collocation=int(args.n_collocation),
            nd_base=int(args.nd_base),
        )

    result = run_full_simple_support_critical_search(
        load_grid_mpa=load_grid,
        modes=modes,
        background_config=background_config,
        x0=background_config.x0,
        m_basis=int(args.m_basis),
        n_collocation=int(args.n_collocation),
        nd_base=int(args.nd_base),
        verbose=not args.quiet,
    )

    if not args.quiet:
        print_search_summary(result)
    return result


if __name__ == "__main__":
    main()
