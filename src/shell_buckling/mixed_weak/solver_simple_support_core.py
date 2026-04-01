# -*- coding: utf-8 -*-
"""
solver_simple_support_core.py

Public wrapper preserving the historical entry-point path for the original
simple-support mixed-weak prototype. The shared implementation now lives in
``_core_solver_common.py``, while this wrapper keeps the original second
boundary row ``M_s(1)`` specialization.
"""
from __future__ import annotations

import numpy as np

from shell_buckling.mixed_weak import _core_solver_common as _shared

nu = _shared.nu
E = _shared.E
h = _shared.h
a = _shared.a
mu = _shared.mu
Lambda = _shared.Lambda
C_twist = _shared.C_twist
plt = _shared.plt
solve_bvp = _shared.solve_bvp

q_pa = 0.0

axisymmetric_fmin_bc = _shared.axisymmetric_fmin_bc
cumulative_trapezoid_from_values = _shared.cumulative_trapezoid_from_values
BaseInterp = _shared.BaseInterp
FIELD_ORDER = _shared.FIELD_ORDER
field_exponent = _shared.field_exponent
poly_basis_triplet = _shared.poly_basis_triplet
TrialSpace = _shared.TrialSpace
evaluate_all_channels_for_basis = _shared.evaluate_all_channels_for_basis
basis_eval_full = _shared.basis_eval_full
evaluate_basis_channels_full = _shared.evaluate_basis_channels_full
compute_resultant_channels = _shared.compute_resultant_channels
postprocess_channels = _shared.postprocess_channels
MixedWeakObjects = _shared.MixedWeakObjects
sigma_metrics_mixed_weak = _shared.sigma_metrics_mixed_weak
summarize_cross_mode = _shared.summarize_cross_mode
plot_sigma_curves = _shared.plot_sigma_curves


def _sync_shared_q_pa() -> None:
    _shared.q_pa = float(globals().get("q_pa", 0.0))


def _pull_shared_q_pa() -> None:
    globals()["q_pa"] = float(_shared.q_pa)


def axisymmetric_fmin_ode(x, y):
    _sync_shared_q_pa()
    return _shared.axisymmetric_fmin_ode(x, y)


def solve_axisymmetric_fmin_continuation(*args, **kwargs):
    _sync_shared_q_pa()
    out = _shared.solve_axisymmetric_fmin_continuation(*args, **kwargs)
    _pull_shared_q_pa()
    return out


def build_base_interp(sol, p_mpa: float, nd_base: int = 4000) -> BaseInterp:
    _sync_shared_q_pa()
    out = _shared.build_base_interp(sol, p_mpa, nd_base=nd_base)
    _pull_shared_q_pa()
    return out


def assemble_operator_column(x: np.ndarray, base: BaseInterp, space: TrialSpace, col: int) -> tuple[np.ndarray, np.ndarray]:
    resid, bvec = _shared.assemble_operator_column(x, base, space, col)
    vals1 = space.basis_eval(np.array([1.0], dtype=float), col)
    out = np.asarray(bvec, dtype=float).copy()
    out[1] = float(vals1["M_s"][0])
    return resid, out


def build_mixed_weak_objects(
    n: int,
    base: BaseInterp,
    x0: float = 1.0e-3,
    m_basis: int = 6,
    n_collocation: int = 120,
) -> MixedWeakObjects:
    obj = _shared.build_mixed_weak_objects(
        n=n,
        base=base,
        x0=x0,
        m_basis=m_basis,
        n_collocation=n_collocation,
    )
    B = np.asarray(obj.B, dtype=float).copy()
    x1 = np.array([1.0], dtype=float)
    for col in range(obj.space.n_unknowns):
        vals1 = obj.space.basis_eval(x1, col)
        B[1, col] = float(vals1["M_s"][0])
    A = np.asarray(obj.A, dtype=float).copy()
    A[-5:, :] = B
    svals = np.linalg.svd(A, compute_uv=False)
    return MixedWeakObjects(
        space=obj.space,
        x_col=obj.x_col,
        A=A,
        B=B,
        sigma_min=float(svals[-1]),
        singvals=svals,
    )


def scan_p_for_n_mixed_weak(
    p_grid,
    sols,
    n: int,
    label: str,
    x0: float = 1.0e-3,
    m_basis: int = 6,
    n_collocation: int = 120,
    verbose: bool = True,
):
    sigmas = []
    objects_by_i = {}

    for i, (p_mpa, sol) in enumerate(zip(p_grid, sols)):
        base = build_base_interp(sol, float(p_mpa), nd_base=4000)
        obj = build_mixed_weak_objects(
            n=n,
            base=base,
            x0=x0,
            m_basis=m_basis,
            n_collocation=n_collocation,
        )
        sigma_min, log_sigma = sigma_metrics_mixed_weak(obj)
        sigmas.append(log_sigma)
        objects_by_i[i] = obj

        if verbose and (i % 10 == 0 or i == len(p_grid) - 1):
            print(
                f"[sig-mixed] n={n:02d} i={i:03d} p={p_mpa:.3f} MPa  "
                f"sigma_min={sigma_min:.6e}  log(sigmin)={log_sigma:.3e}"
            )

    return np.asarray(sigmas, dtype=float), objects_by_i


def main() -> None:
    p_grid = np.linspace(0.0, 6.0, 24)
    modes = [12, 13, 14, 15]
    x0 = 1.0e-3
    m_basis = 6
    n_collocation = 120

    print(f"=== Axisymmetric continuation for F_min background (0..{p_grid[-1]:.1f} MPa) ===")
    _, sols = solve_axisymmetric_fmin_continuation(
        p_grid,
        nd_bvp=1400,
        x0=x0,
        tol=1.0e-4,
        max_nodes=150000,
        verbose=True,
    )

    logsig_by_n: dict[int, np.ndarray] = {}

    for n in modes:
        label = "mixed_weak_v1"
        print(f"\n=== Mixed weak sigma scan for n={n} : {label} ===")
        logsig, _ = scan_p_for_n_mixed_weak(
            p_grid,
            sols,
            n=n,
            label=label,
            x0=x0,
            m_basis=m_basis,
            n_collocation=n_collocation,
            verbose=True,
        )
        logsig_by_n[n] = logsig

    summarize_cross_mode(p_grid, logsig_by_n, label="mixed_weak_v1")
    plot_sigma_curves(p_grid, logsig_by_n, label="mixed_weak_v1")


if __name__ == "__main__":
    main()
