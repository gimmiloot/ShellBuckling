# -*- coding: utf-8 -*-
"""
solver_patched_core.py

Public wrapper preserving the historical entry-point path for the patched
mixed-weak simple-support prototype. The shared implementation now lives in
``_core_solver_common.py``.
"""
from __future__ import annotations

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
build_base_interp = _shared.build_base_interp
FIELD_ORDER = _shared.FIELD_ORDER
field_exponent = _shared.field_exponent
poly_basis_triplet = _shared.poly_basis_triplet
TrialSpace = _shared.TrialSpace
evaluate_all_channels_for_basis = _shared.evaluate_all_channels_for_basis
basis_eval_full = _shared.basis_eval_full
evaluate_basis_channels_full = _shared.evaluate_basis_channels_full
compute_resultant_channels = _shared.compute_resultant_channels
postprocess_channels = _shared.postprocess_channels
assemble_operator_column = _shared.assemble_operator_column
MixedWeakObjects = _shared.MixedWeakObjects
build_mixed_weak_objects = _shared.build_mixed_weak_objects
sigma_metrics_mixed_weak = _shared.sigma_metrics_mixed_weak
scan_p_for_n_mixed_weak = _shared.scan_p_for_n_mixed_weak
summarize_cross_mode = _shared.summarize_cross_mode
plot_sigma_curves = _shared.plot_sigma_curves
main = _shared.main


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


if __name__ == "__main__":
    main()
