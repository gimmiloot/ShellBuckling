# -*- coding: utf-8 -*-
"""
mixed_weak_boundary_matrix_test_v2_updated.py

Boundary-matrix testbench v2 for the new mixed weak criterion.

Difference from v1:
- the two approximate regular modes are NOT taken as the two smallest right-singular
  vectors of the global interior matrix;
- instead, each mode is built by a constrained least-squares problem:
      minimize ||A_int c||
  subject to center-normalization / center-regular constraints.

Added in this updated version:
- deep diagnostics for the two central-regular modes reconstructed from coefficient space;
- local-in-x inspection of the channels available from TrialSpace.basis_eval(...);
- comparison of sigma_min(B_mix) vs sigma_min(B_mix without H-row) to detect whether H
  actually contributes to the boundary criterion;
- center-constraint diagnostics to verify that the intended two-mode normalization is
  really what is being built numerically.

The purpose is to localize where the new information is lost if B_mix still collapses:
- already at center-normalization,
- inside the surrogate interior operator,
- or only in the right-boundary evaluation of T_s, S, H.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence
import inspect

import numpy as np

THIS_DIR = Path(__file__).resolve().parent
import sys
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

import mixed_weak_solver_v1_simple_support as mw

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
CHECKPOINTS = (0.0, 0.05, 0.20, 0.50, 0.80, 1.0)
DEEP_DEBUG_TARGETS = []
DEEP_DEBUG_VERBOSE = False
PRINT_CENTER_DIAGNOSTICS = False
SHOW_SAMPLE_MATRICES = False
BASELINE_VERBOSE = False

RUN_BASELINE_SCAN = True
RUN_RESOLUTION_STUDY = True
RESOLUTION_CASES = [(6, 120), (8, 180), (10, 240)]
RESOLUTION_WINDOWS = {
    13: (2.8, 4.2),
    14: (4.0, 5.4),
}
RESOLUTION_NPTS = 17

RUN_FINE_SCAN = True
FINE_SCAN_CASES = [(10, 240), (12, 300)]
FINE_SCAN_WINDOWS = {13: (3.85, 4.05), 14: (4.18, 4.32)}
FINE_SCAN_NPTS = 21

RUN_ADAPTIVE_SCAN = True
ADAPTIVE_SCAN_CASES = [(12, 300), (14, 360)]
ADAPTIVE_SCAN_WINDOWS = {13: (3.72, 3.94), 14: (4.28, 4.42)}
ADAPTIVE_SCAN_NPTS = 25
ADAPTIVE_SCAN_MAX_ITERS = 4
ADAPTIVE_EDGE_PAD = 1
PLOT_LINEAR_FULL_RANGE = True
PLOT_LOG_FULL_RANGE = False

# broader production scan used for current search
BASELINE_P_MAX_MPA = 8.0
BASELINE_P_NPTS = 33
BASELINE_MODES = list(range(10, 19))

ROW_SCALE = np.array([1.0, 1.0, 1.0, 2.0 * (1.0 + mw.nu), mw.C_twist], dtype=float)


def balanced_Bmix(B: np.ndarray) -> np.ndarray:
    return ROW_SCALE[:, None] * np.asarray(B, dtype=float)


@dataclass
class BoundaryMatrixObjectsV2:
    n: int
    p_mpa: float
    x0: float
    m_basis: int
    A_int: np.ndarray
    B_full: np.ndarray
    C_center: np.ndarray
    V_reg: np.ndarray
    residual_norms: np.ndarray
    B_mix: np.ndarray
    sigma_Bmix: float
    x_col: np.ndarray
    space: Any
    base: Any
    center_values: np.ndarray


# -----------------------------------------------------------------------------
# Assembly
# -----------------------------------------------------------------------------
def assemble_interior_and_boundary(
    n: int,
    base: mw.BaseInterp,
    x0: float = 1.0e-3,
    m_basis: int = 6,
    n_collocation: int = 120,
):
    space = mw.TrialSpace(n=int(n), x0=float(x0), m_basis=int(m_basis))
    x_col = np.linspace(float(x0), 1.0, int(n_collocation) + 2)[1:-1]
    n_eq = 8 * x_col.size
    n_unknowns = space.n_unknowns
    A_int = np.zeros((n_eq, n_unknowns), dtype=float)
    B_full = np.zeros((5, n_unknowns), dtype=float)
    for col in range(n_unknowns):
        resid, bvec = mw.assemble_operator_column(x_col, base, space, col)
        A_int[:, col] = resid.reshape(-1, order='F')
        B_full[:, col] = bvec
    return space, x_col, A_int, B_full


def make_center_constraint_matrix(space: mw.TrialSpace, base: mw.BaseInterp) -> np.ndarray:
    """
    Build center-leading-amplitude functionals on coefficient space.

    Rows correspond to approximate leading coefficients at x=x0 for:
      0: u_s / x^n
      1: phi / x^(n-1)
      2: u_n / x^n + (lambda_c / n) * phi / x^(n-1)
      3: psi / x^(n-1) - lambda_c * phi / x^(n-1)
    """
    x0 = np.array([space.x0], dtype=float)
    b0 = base.at_many(x0)
    lam_c = float(b0['lambda_s0'][0])
    n = space.n
    N = space.n_unknowns
    C = np.zeros((4, N), dtype=float)
    xpow_us = space.x0 ** n
    xpow_phi = space.x0 ** (n - 1)

    for col in range(N):
        vals = space.basis_eval(x0, col)
        us = float(vals['u_s'][0]) / xpow_us
        un = float(vals['u_n'][0]) / xpow_us
        phi = float(vals['phi'][0]) / xpow_phi
        psi = float(vals['psi'][0]) / xpow_phi
        C[0, col] = us
        C[1, col] = phi
        C[2, col] = un + (lam_c / n) * phi
        C[3, col] = psi - lam_c * phi
    return C


def solve_constrained_mode(A: np.ndarray, C: np.ndarray, d: np.ndarray, reg: float = 1e-12) -> np.ndarray:
    """Constrained least squares via KKT: min ||A c||^2 + reg ||c||^2 s.t. C c = d."""
    N = A.shape[1]
    m = C.shape[0]
    ATA = A.T @ A + reg * np.eye(N)
    KKT = np.block([
        [ATA, C.T],
        [C, np.zeros((m, m), dtype=float)],
    ])
    rhs = np.concatenate([np.zeros(N, dtype=float), d.astype(float)])
    sol = np.linalg.solve(KKT, rhs)
    c = sol[:N]
    nrm = np.linalg.norm(c)
    if nrm > 0:
        c = c / nrm
    return c


def orthogonalize_against(c: np.ndarray, ref: np.ndarray) -> np.ndarray:
    c = c - ref * np.dot(ref, c)
    nrm = np.linalg.norm(c)
    if nrm > 0:
        c = c / nrm
    return c


def build_boundary_matrix_test_v2(
    n: int,
    sol,
    p_mpa: float,
    x0: float = 1.0e-3,
    m_basis: int = 6,
    n_collocation: int = 120,
    nd_base: int = 4000,
) -> BoundaryMatrixObjectsV2:
    base = mw.build_base_interp(sol, float(p_mpa), nd_base=nd_base)
    space, x_col, A_int, B_full = assemble_interior_and_boundary(
        n=n, base=base, x0=x0, m_basis=m_basis, n_collocation=n_collocation
    )
    C_center = make_center_constraint_matrix(space, base)

    # Mode 1: membrane-led central mode: u_s-leading = 1, phi-leading = 0
    d1 = np.array([1.0, 0.0, 0.0, 0.0], dtype=float)
    c1 = solve_constrained_mode(A_int, C_center, d1)

    # Mode 2: bending/twist-led central mode: u_s-leading = 0, phi-leading = 1
    d2 = np.array([0.0, 1.0, 0.0, 0.0], dtype=float)
    c2_raw = solve_constrained_mode(A_int, C_center, d2)
    c2 = orthogonalize_against(c2_raw, c1)

    V_reg = np.column_stack([c1, c2])
    B_mix = B_full @ V_reg
    sigma_Bmix = float(np.linalg.svd(B_mix, compute_uv=False)[-1])
    residual_norms = np.array([np.linalg.norm(A_int @ c1), np.linalg.norm(A_int @ c2)], dtype=float)
    center_values = C_center @ V_reg

    return BoundaryMatrixObjectsV2(
        n=int(n),
        p_mpa=float(p_mpa),
        x0=float(x0),
        m_basis=int(m_basis),
        A_int=A_int,
        B_full=B_full,
        C_center=C_center,
        V_reg=V_reg,
        residual_norms=residual_norms,
        B_mix=B_mix,
        sigma_Bmix=sigma_Bmix,
        x_col=x_col,
        space=space,
        base=base,
        center_values=center_values,
    )


# -----------------------------------------------------------------------------
# Mode / channel reconstruction diagnostics
# -----------------------------------------------------------------------------
def sample_indices(x_grid: np.ndarray, checkpoints: Sequence[float] = CHECKPOINTS) -> list[int]:
    n = len(x_grid)
    out: list[int] = []
    for a in checkpoints:
        j = int(round(float(a) * (n - 1)))
        j = max(0, min(n - 1, j))
        out.append(j)
    return sorted(set(out))


def _to_1d_float_array(val: Any, n_x: int) -> np.ndarray | None:
    arr = np.asarray(val, dtype=float)
    if arr.ndim == 0:
        arr = np.full(n_x, float(arr), dtype=float)
    else:
        arr = np.reshape(arr, (-1,))
        if arr.size == 1:
            arr = np.full(n_x, float(arr[0]), dtype=float)
        elif arr.size != n_x:
            return None
    return arr


def _normalize_channel_dict(vals: Any, n_x: int) -> dict[str, np.ndarray]:
    if not isinstance(vals, dict):
        return {}
    out: dict[str, np.ndarray] = {}
    for key, val in vals.items():
        arr = _to_1d_float_array(val, n_x)
        if arr is None:
            continue
        out[str(key)] = arr
    return out


def _merge_channel_dict(dst: dict[str, np.ndarray], src: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    for key, arr in src.items():
        dst[key] = np.asarray(arr, dtype=float)
    return dst


def _call_with_supported_kwargs(fn, **kwargs):
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError):
        return None
    params = sig.parameters
    accepts_varkw = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values())
    call_kwargs = {}
    for k, v in kwargs.items():
        if accepts_varkw or k in params:
            call_kwargs[k] = v
    try:
        return fn(**call_kwargs)
    except TypeError:
        return None


def _discover_extended_channel_dict(space, base, x: np.ndarray, col: int, core_vals: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    n_x = x.size
    candidates: list[tuple[str, Any]] = []

    candidate_names = [
        'basis_eval_full', 'basis_eval_extended', 'basis_eval_ex',
        'eval_full', 'evaluate_all_channels', 'evaluate_all_channels_for_basis',
        'evaluate_basis_channels', 'evaluate_basis_channels_full',
        'probe_basis_channels', 'reconstruct_basis_channels',
        'postprocess_basis_channels', 'postprocess_channels',
        'compute_extra_channels', 'compute_resultant_channels',
        'resultant_eval', 'resultant_basis_eval',
    ]

    for owner_name, owner in [('space', space), ('mw', mw), ('base', base)]:
        if owner is None:
            continue
        for name in candidate_names:
            fn = getattr(owner, name, None)
            if callable(fn):
                candidates.append((f'{owner_name}.{name}', fn))

    merged: dict[str, np.ndarray] = {}
    for _name, fn in candidates:
        vals = _call_with_supported_kwargs(
            fn,
            x=x,
            col=col,
            basis_col=col,
            j=col,
            idx=col,
            space=space,
            base=base,
            vals=core_vals,
            basis_vals=core_vals,
            core=core_vals,
        )
        extra = _normalize_channel_dict(vals, n_x)
        if extra:
            _merge_channel_dict(merged, extra)
    return merged


def _inject_exact_boundary_rows(
    channels: dict[str, np.ndarray],
    x: np.ndarray,
    boundary_mode: np.ndarray | None,
) -> dict[str, np.ndarray]:
    if boundary_mode is None:
        return channels
    idx = np.where(np.isclose(x, 1.0, atol=1.0e-12, rtol=0.0))[0]
    if idx.size == 0:
        return channels
    j = int(idx[-1])
    row_map = {
        'u_n': float(boundary_mode[0]),
        'phi': float(boundary_mode[1]),
        'T_s': float(boundary_mode[2]),
        'S': float(boundary_mode[3]),
        'H': float(boundary_mode[4]),
    }
    n_x = x.size
    for key, val in row_map.items():
        arr = np.asarray(channels.get(key, np.full(n_x, np.nan, dtype=float)), dtype=float).copy()
        if arr.size != n_x:
            arr = np.full(n_x, np.nan, dtype=float)
        arr[j] = val
        channels[key] = arr
    return channels


def evaluate_mode_channels(
    space,
    base,
    coeffs: np.ndarray,
    x: np.ndarray,
    B_full: np.ndarray | None = None,
) -> dict[str, np.ndarray]:
    """
    Reconstruct mode channels with several fallbacks.

    1) Always use TrialSpace.basis_eval(x, col) for the channels it exposes directly.
    2) If the solver provides any extended helper (basis_eval_full / evaluate_all_channels / ...),
       detect it at runtime and merge its output.
    3) If S/H are still unavailable locally, inject their exact boundary values at x=1 from
       the already assembled boundary rows B_full @ coeffs.
    """
    x = np.asarray(x, dtype=float)
    n_x = x.size
    keys_union: set[str] = set()
    cache: list[dict[str, np.ndarray]] = []
    coeffs = np.asarray(coeffs, dtype=float)

    for col, alpha in enumerate(coeffs):
        if abs(alpha) == 0.0:
            cache.append({})
            continue
        core = _normalize_channel_dict(space.basis_eval(x, col), n_x)
        extra = _discover_extended_channel_dict(space, base, x, col, core)
        cur = dict(core)
        _merge_channel_dict(cur, extra)
        for key in cur.keys():
            keys_union.add(str(key))
        cache.append(cur)

    out: dict[str, np.ndarray] = {key: np.zeros(n_x, dtype=float) for key in sorted(keys_union)}
    for alpha, cur in zip(coeffs, cache):
        if abs(alpha) == 0.0:
            continue
        for key, arr in cur.items():
            out[key] += float(alpha) * arr

    boundary_mode = None if B_full is None else (np.asarray(B_full, dtype=float) @ coeffs)
    out = _inject_exact_boundary_rows(out, x, boundary_mode)
    return out


def _channel_alias(channels: dict[str, np.ndarray], *names: str) -> np.ndarray | None:
    for name in names:
        if name in channels:
            return channels[name]
    return None


def build_local_Bmix_from_channels(ch1: dict[str, np.ndarray], ch2: dict[str, np.ndarray], j: int):
    row_specs = [
        ('u_n', ('u_n',)),
        ('M_s', ('M_s', 'Ms')),
        ('T_s', ('T_s', 'Ts')),
        ('S', ('S',)),
        ('H', ('H',)),
    ]
    rows = []
    missing: list[str] = []
    available_labels: list[str] = []
    nonfinite: list[str] = []
    for label, aliases in row_specs:
        a1 = _channel_alias(ch1, *aliases)
        a2 = _channel_alias(ch2, *aliases)
        if a1 is None or a2 is None:
            missing.append(label)
            continue
        v1 = float(a1[j])
        v2 = float(a2[j])
        if not (np.isfinite(v1) and np.isfinite(v2)):
            nonfinite.append(label)
            continue
        rows.append([v1, v2])
        available_labels.append(label)
    if not rows:
        return None, missing, nonfinite, available_labels
    return np.asarray(rows, dtype=float), missing, nonfinite, available_labels

def print_available_channels(space, base=None) -> None:
    x_probe = np.array([space.x0, 0.25, 0.75, 1.0], dtype=float)
    vals = _normalize_channel_dict(space.basis_eval(x_probe, 0), x_probe.size)
    extra = _discover_extended_channel_dict(space, base, x_probe, 0, vals)
    keys = sorted(set(vals.keys()) | set(extra.keys()))
    print("available reconstructed channels =", keys)


def print_center_diagnostics(obj: BoundaryMatrixObjectsV2) -> None:
    print("\ncenter-normalization diagnostics:")
    print("rows: [u_s/x^n, phi/x^(n-1), u_n/x^n + (lambda_c/n)phi/x^(n-1), psi/x^(n-1)-lambda_c phi/x^(n-1)]")
    with np.printoptions(precision=6, suppress=True):
        print(obj.center_values)


def print_mode_track(tag: str, x_grid: np.ndarray, channels: dict[str, np.ndarray]) -> None:
    idxs = sample_indices(x_grid)
    psi_arr = _channel_alias(channels, 'psi')
    H_arr = _channel_alias(channels, 'H')
    S_arr = _channel_alias(channels, 'S')
    T_s_arr = _channel_alias(channels, 'T_s', 'Ts')

    print(f"\n--- track: {tag} ---")
    print(" j      x           |psi|         |H|           |Ctw*H|       |S|           |2(1+nu)S|    |T_s|")
    for j in idxs:
        psi_v = abs(float(psi_arr[j])) if psi_arr is not None else float('nan')
        H_v = abs(float(H_arr[j])) if H_arr is not None else float('nan')
        Hbal_v = mw.C_twist * H_v if np.isfinite(H_v) else float('nan')
        S_v = abs(float(S_arr[j])) if S_arr is not None else float('nan')
        Sbal_v = 2.0 * (1.0 + mw.nu) * S_v if np.isfinite(S_v) else float('nan')
        Ts_v = abs(float(T_s_arr[j])) if T_s_arr is not None else float('nan')
        print(f"{j:4d}  {x_grid[j]:.6f}  {psi_v:.3e}  {H_v:.3e}  {Hbal_v:.3e}  {S_v:.3e}  {Sbal_v:.3e}  {Ts_v:.3e}")


def _safe_sigma_min(A: np.ndarray) -> float | None:
    A = np.asarray(A, dtype=float)
    if A.ndim != 2 or A.size == 0:
        return None
    if not np.all(np.isfinite(A)):
        return None
    try:
        s = np.linalg.svd(A, compute_uv=False)
    except np.linalg.LinAlgError:
        return None
    if s.size == 0:
        return None
    return float(s[-1])


def print_local_Bmix_diagnostics(tag: str, x_grid: np.ndarray, ch1: dict[str, np.ndarray], ch2: dict[str, np.ndarray]) -> None:
    idxs = sample_indices(x_grid)
    print(f"\n=== local B-like diagnostics: {tag} ===")
    print(" j      x           sigma_min(5x2)   sigma_min(4x2,noH)   sigma_min_bal   sigma_bal_noH   ||H-row||      ||Ctw*H-row||")
    for j in idxs:
        B_any, missing, nonfinite, labels = build_local_Bmix_from_channels(ch1, ch2, j)
        if B_any is None:
            extra = []
            if missing:
                extra.append(f"missing={missing}")
            if nonfinite:
                extra.append(f"nonfinite={nonfinite}")
            extra_txt = ', '.join(extra) if extra else 'no usable rows'
            print(f"{j:4d}  {x_grid[j]:.6f}  <{extra_txt}>")
            continue

        sigma5_txt = '<unavailable>'
        sigma4_txt = '<unavailable>'
        sigma5_bal_txt = '<unavailable>'
        sigma4_bal_txt = '<unavailable>'
        Hnorm_txt = '<unavailable>'
        Hbalnorm_txt = '<unavailable>'

        if len(labels) == 5:
            sigma5 = _safe_sigma_min(B_any)
            if sigma5 is not None:
                sigma5_txt = f'{sigma5:.3e}'
            Hnorm_txt = f'{np.linalg.norm(B_any[4, :]):.3e}'

            B_bal_any = balanced_Bmix(B_any)
            sigma5_bal = _safe_sigma_min(B_bal_any)
            if sigma5_bal is not None:
                sigma5_bal_txt = f'{sigma5_bal:.3e}'
            Hbalnorm_txt = f'{np.linalg.norm(B_bal_any[4, :]):.3e}'

        if labels[:4] == ['u_n', 'phi', 'T_s', 'S']:
            B4 = B_any[:4, :]
            sigma4 = _safe_sigma_min(B4)
            if sigma4 is not None:
                sigma4_txt = f'{sigma4:.3e}'
            B4_bal = balanced_Bmix(np.vstack([B4, np.zeros((1, B4.shape[1]), dtype=float)]))[:4, :]
            sigma4_bal = _safe_sigma_min(B4_bal)
            if sigma4_bal is not None:
                sigma4_bal_txt = f'{sigma4_bal:.3e}'
        elif all(name in labels for name in ['u_n', 'phi', 'T_s', 'S']):
            idx4 = [labels.index(name) for name in ['u_n', 'phi', 'T_s', 'S']]
            B4 = B_any[idx4, :]
            sigma4 = _safe_sigma_min(B4)
            if sigma4 is not None:
                sigma4_txt = f'{sigma4:.3e}'
            B4_bal = balanced_Bmix(np.vstack([B4, np.zeros((1, B4.shape[1]), dtype=float)]))[:4, :]
            sigma4_bal = _safe_sigma_min(B4_bal)
            if sigma4_bal is not None:
                sigma4_bal_txt = f'{sigma4_bal:.3e}'

        print(
            f"{j:4d}  {x_grid[j]:.6f}  {sigma5_txt:>12}   {sigma4_txt:>12}   "
            f"{sigma5_bal_txt:>12}   {sigma4_bal_txt:>12}   {Hnorm_txt:>12}   {Hbalnorm_txt:>14}"
        )
        rn = np.linalg.norm(B_any, axis=1)
        print(f"      available rows {labels} with norms =", np.array2string(rn, precision=3, suppress_small=False))
        if len(labels) == 5:
            rn_bal = np.linalg.norm(balanced_Bmix(B_any), axis=1)
            print("      balanced row norms [u_n, M_s, T_s, gamma_sθ, kappa_sθ] =",
                  np.array2string(rn_bal, precision=3, suppress_small=False))
        if missing:
            print(f"      missing rows = {missing}")
        if nonfinite:
            print(f"      nonfinite rows = {nonfinite}")

def print_boundary_matrix(obj: BoundaryMatrixObjectsV2) -> None:
    print("\nB_mix =")
    with np.printoptions(precision=6, suppress=True):
        print(obj.B_mix)
    print("row labels: [u_n(1), M_s(1), T_s(1), S(1), H(1)]")
    row_norms = np.linalg.norm(obj.B_mix, axis=1)
    col_norms = np.linalg.norm(obj.B_mix, axis=0)
    print("row norms =", row_norms)
    print("col norms =", col_norms)
    print("mode residual norms =", obj.residual_norms)
    print("singular values =", np.linalg.svd(obj.B_mix, compute_uv=False))
    print("sigma_min(B_mix) =", obj.sigma_Bmix)
    print("sigma_min(B_noH) =", np.linalg.svd(obj.B_mix[:4, :], compute_uv=False)[-1])

    B_bal = balanced_Bmix(obj.B_mix)
    print("\nB_mix_balanced =")
    with np.printoptions(precision=6, suppress=True):
        print(B_bal)
    print("balanced row labels: [u_n(1), M_s(1), T_s(1), gamma_sθ(1), kappa_sθ(1)]")
    print("balanced row norms =", np.linalg.norm(B_bal, axis=1))
    print("balanced col norms =", np.linalg.norm(B_bal, axis=0))
    s_bal = np.linalg.svd(B_bal, compute_uv=False)
    print("balanced singular values =", s_bal)
    print("sigma_min(B_mix_balanced) =", float(s_bal[-1]))
    print("sigma_min(B_bal_noH) =", float(np.linalg.svd(B_bal[:4, :], compute_uv=False)[-1]))


def deep_debug_object(obj: BoundaryMatrixObjectsV2) -> None:
    x_debug = np.array(sorted(set([float(obj.x0)] + list(CHECKPOINTS))), dtype=float)
    ch1 = evaluate_mode_channels(obj.space, obj.base, obj.V_reg[:, 0], x_debug, B_full=obj.B_full)
    ch2 = evaluate_mode_channels(obj.space, obj.base, obj.V_reg[:, 1], x_debug, B_full=obj.B_full)

    print(f"\n################ DEEP DEBUG n={obj.n}, p={obj.p_mpa:.3f} MPa ################")
    print(f"mode residual norms: res1={obj.residual_norms[0]:.3e}, res2={obj.residual_norms[1]:.3e}")
    print_available_channels(obj.space, obj.base)
    if PRINT_CENTER_DIAGNOSTICS:
        print_center_diagnostics(obj)
    print_mode_track("mode 1", x_debug, ch1)
    print_mode_track("mode 2", x_debug, ch2)
    print_local_Bmix_diagnostics(f"n={obj.n}, p={obj.p_mpa:.3f}", x_debug, ch1, ch2)
    print_boundary_matrix(obj)


# -----------------------------------------------------------------------------
# Scans and summaries
# -----------------------------------------------------------------------------
def scan_p_for_n_boundary_matrix_v2(
    p_grid: Sequence[float],
    sols: Sequence,
    n: int,
    x0: float = 1.0e-3,
    m_basis: int = 6,
    n_collocation: int = 120,
    verbose: bool = True,
):
    sigmas = []
    by_i: dict[int, BoundaryMatrixObjectsV2] = {}
    for i, (p_mpa, sol) in enumerate(zip(p_grid, sols)):
        obj = build_boundary_matrix_test_v2(
            n=n, sol=sol, p_mpa=float(p_mpa), x0=x0, m_basis=m_basis, n_collocation=n_collocation
        )
        sigmas.append(obj.sigma_Bmix)
        by_i[i] = obj
        if verbose and (i % 10 == 0 or i == len(p_grid) - 1):
            logsig = float(np.log(max(obj.sigma_Bmix, 1.0e-300)))
            print(
                f"[sig-Bmix-v2] n={n:02d} i={i:03d} p={p_mpa:.3f} MPa  "
                f"sigma_Bmix={obj.sigma_Bmix:.6e}  log(sig)={logsig:.3e}  "
                f"res1={obj.residual_norms[0]:.3e}  res2={obj.residual_norms[1]:.3e}"
            )
    return np.asarray(sigmas, dtype=float), by_i


def extract_metrics_from_objects(objs: dict[int, BoundaryMatrixObjectsV2]) -> dict[str, np.ndarray]:
    """Build raw / balanced metric arrays from already assembled objects indexed by grid point."""
    keys = sorted(objs.keys())
    sigma_raw = []
    sigma_raw_noH = []
    sigma_bal = []
    sigma_bal_noH = []
    for i in keys:
        obj = objs[i]
        B = np.asarray(obj.B_mix, dtype=float)
        sigma_raw.append(float(np.linalg.svd(B, compute_uv=False)[-1]))
        sigma_raw_noH.append(float(np.linalg.svd(B[:4, :], compute_uv=False)[-1]))
        B_bal = balanced_Bmix(B)
        sigma_bal.append(float(np.linalg.svd(B_bal, compute_uv=False)[-1]))
        sigma_bal_noH.append(float(np.linalg.svd(B_bal[:4, :], compute_uv=False)[-1]))
    return {
        'sigma_raw': np.asarray(sigma_raw, dtype=float),
        'sigma_raw_noH': np.asarray(sigma_raw_noH, dtype=float),
        'sigma_bal': np.asarray(sigma_bal, dtype=float),
        'sigma_bal_noH': np.asarray(sigma_bal_noH, dtype=float),
    }


def summarize_cross_mode(p_grid: Sequence[float], sig_by_n: dict[int, np.ndarray], label: str) -> None:
    print(f"\n=== Cross-mode comparison summary : {label} ===")
    for n in sorted(sig_by_n.keys()):
        arr = np.asarray(sig_by_n[n], dtype=float)
        i_best = int(np.argmin(arr))
        print(
            f"n={n:02d} | best at p={float(p_grid[i_best]):.3f} MPa | "
            f"sigma_Bmix={float(arr[i_best]):.6e} | log(sig)={float(np.log(max(arr[i_best], 1.0e-300))):.6e}"
        )


def nearest_p_index(p_grid: Sequence[float], p_target: float) -> int:
    arr = np.asarray(p_grid, dtype=float)
    return int(np.argmin(np.abs(arr - float(p_target))))


# -----------------------------------------------------------------------------
# Resolution-convergence study
# -----------------------------------------------------------------------------
def find_global_best(metric_by_n: dict[int, np.ndarray], objs_by_n: dict[int, dict[int, BoundaryMatrixObjectsV2]]):
    best = None
    for n, arr in metric_by_n.items():
        i = int(np.argmin(arr))
        val = float(arr[i])
        if best is None or val < best[2]:
            best = (n, i, val, objs_by_n[n][i])
    return best


def print_resolution_study_row(n: int, p_grid: np.ndarray, metrics: dict[str, np.ndarray]) -> None:
    labels = [('raw', 'sigma_raw'), ('balanced', 'sigma_bal'), ('balanced-noH', 'sigma_bal_noH')]
    parts = []
    for nice, key in labels:
        arr = np.asarray(metrics[key], dtype=float)
        i_best = int(np.argmin(arr))
        parts.append(f"{nice}: p_best={float(p_grid[i_best]):.3f} MPa, sigma={float(arr[i_best]):.6e}")
    print(f"n={n:02d} | " + " | ".join(parts))


def print_fine_scan_row(n: int, p_grid: np.ndarray, metrics: dict[str, np.ndarray]) -> None:
    labels = [('balanced', 'sigma_bal'), ('balanced-noH', 'sigma_bal_noH'), ('raw', 'sigma_raw')]
    parts = []
    for nice, key in labels:
        arr = np.asarray(metrics[key], dtype=float)
        i_best = int(np.argmin(arr))
        parts.append(f"{nice}: p_best={float(p_grid[i_best]):.3f} MPa, sigma={float(arr[i_best]):.6e}")
    print(f"n={n:02d} | " + " | ".join(parts))




def local_minima_indices(y: np.ndarray) -> np.ndarray:
    y = np.asarray(y, dtype=float)
    if y.size < 3:
        return np.array([], dtype=int)
    idx = []
    for i in range(1, y.size - 1):
        if np.isfinite(y[i-1]) and np.isfinite(y[i]) and np.isfinite(y[i+1]):
            if y[i] <= y[i-1] and y[i] <= y[i+1] and (y[i] < y[i-1] or y[i] < y[i+1]):
                idx.append(i)
    return np.asarray(idx, dtype=int)


def print_metric_row(name: str, p_grid: np.ndarray, arr: np.ndarray) -> str:
    arr = np.asarray(arr, dtype=float)
    i_best = int(np.argmin(arr))
    return f"{name}: p_best={float(p_grid[i_best]):.3f} MPa, sigma={float(arr[i_best]):.6e}"


def plot_full_range_linear_metrics(p_grid: np.ndarray, metrics_by_n: dict[str, dict[int, np.ndarray]]) -> None:
    if plt is None:
        return
    # Overview: balanced by mode with local minima markers
    plt.figure(figsize=(9, 5.5))
    for n, arr in sorted(metrics_by_n['sigma_bal'].items()):
        arr = np.asarray(arr, dtype=float)
        plt.plot(p_grid, arr, marker='o', ms=3, label=f'n={n} balanced')
        mins = local_minima_indices(arr)
        if mins.size:
            plt.plot(p_grid[mins], arr[mins], linestyle='none', marker='s', ms=6)
    plt.axhline(0.0, color='k', linewidth=0.8, alpha=0.5)
    plt.xlabel('pressure p [MPa]')
    plt.ylabel('sigma')
    plt.title('balanced sigma on full range (local minima marked)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Per-mode comparison: balanced vs balanced-noH on full range
    for n in sorted(metrics_by_n['sigma_bal'].keys()):
        bal = np.asarray(metrics_by_n['sigma_bal'][n], dtype=float)
        bal_noH = np.asarray(metrics_by_n['sigma_bal_noH'][n], dtype=float)
        raw = np.asarray(metrics_by_n['sigma_raw'][n], dtype=float)
        plt.figure(figsize=(9, 5.5))
        plt.plot(p_grid, bal, marker='o', ms=3, label=f'n={n} balanced')
        plt.plot(p_grid, bal_noH, marker='x', ms=4, linestyle='--', label=f'n={n} balanced-noH')
        plt.plot(p_grid, raw, marker='.', ms=4, linestyle=':', label=f'n={n} raw')
        for arr, mk in ((bal, 's'), (bal_noH, 'd')):
            mins = local_minima_indices(arr)
            if mins.size:
                plt.plot(p_grid[mins], arr[mins], linestyle='none', marker=mk, ms=6)
        plt.axhline(0.0, color='k', linewidth=0.8, alpha=0.5)
        plt.xlabel('pressure p [MPa]')
        plt.ylabel('sigma')
        plt.title(f'full-range linear sigma for n={n}')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.show()


def solve_axisymmetric_window_seeded(
    p_grid: np.ndarray,
    baseline_p_grid: np.ndarray,
    baseline_sols: Sequence,
    x0: float = 1.0e-3,
    nd_bvp: int = 1400,
    tol: float = 1.0e-4,
    max_nodes: int = 150000,
):
    """
    Robust local continuation on a pressure window using an already converged
    baseline solution as seed, then continuing upward and downward from the
    nearest available baseline pressure.
    """
    p_grid = np.asarray(p_grid, dtype=float)
    baseline_p_grid = np.asarray(baseline_p_grid, dtype=float)
    if p_grid.ndim != 1 or p_grid.size == 0:
        raise ValueError('p_grid must be a non-empty 1D array')
    if baseline_p_grid.ndim != 1 or baseline_p_grid.size != len(baseline_sols):
        raise ValueError('baseline_p_grid / baseline_sols mismatch')

    x_mesh = np.linspace(float(x0), 1.0, int(nd_bvp))
    k_seed = int(np.argmin(np.abs(p_grid - baseline_p_grid[np.argmin(np.abs(baseline_p_grid - p_grid[0]))])))
    # Better: choose baseline point nearest to the window midpoint, then map to nearest local index
    p_mid = 0.5 * float(p_grid[0] + p_grid[-1])
    j_base = int(np.argmin(np.abs(baseline_p_grid - p_mid)))
    seed_sol = baseline_sols[j_base]
    k_seed = int(np.argmin(np.abs(p_grid - baseline_p_grid[j_base])))

    sols = [None] * len(p_grid)

    def _solve_at(p_mpa: float, y_guess: np.ndarray):
        mw.q_pa = float(p_mpa) * 1.0e6
        bc = lambda ya, yb: mw.axisymmetric_fmin_bc(ya, yb, x0=float(x0))
        sol = mw.solve_bvp(
            mw.axisymmetric_fmin_ode, bc, x_mesh, y_guess,
            tol=tol, max_nodes=max_nodes, verbose=0
        )
        if not sol.success:
            sol = mw.solve_bvp(
                mw.axisymmetric_fmin_ode, bc, x_mesh, y_guess,
                tol=min(5.0e-4, 5.0 * tol), max_nodes=max_nodes, verbose=0
            )
        if not sol.success:
            raise RuntimeError(
                f"Axisymmetric seeded F_min BVP failed at p={p_mpa:.6f} MPa: {sol.message}"
            )
        return sol

    # solve at seed index from converged baseline shape
    y_guess = seed_sol.sol(x_mesh)
    sols[k_seed] = _solve_at(float(p_grid[k_seed]), y_guess)

    # upward continuation
    sol_prev = sols[k_seed]
    for i in range(k_seed + 1, len(p_grid)):
        y_guess = sol_prev.sol(x_mesh)
        sol_prev = _solve_at(float(p_grid[i]), y_guess)
        sols[i] = sol_prev

    # downward continuation
    sol_prev = sols[k_seed]
    for i in range(k_seed - 1, -1, -1):
        y_guess = sol_prev.sol(x_mesh)
        sol_prev = _solve_at(float(p_grid[i]), y_guess)
        sols[i] = sol_prev

    return x_mesh, sols


def run_resolution_study(x0: float = 1.0e-3, baseline_p_grid: np.ndarray | None = None, baseline_sols: Sequence | None = None) -> None:
    print("\n=== Resolution study for balanced/raw/balanced-noH ===")
    print(f"windows = {RESOLUTION_WINDOWS}, npts = {RESOLUTION_NPTS}")
    for m_basis, n_collocation in RESOLUTION_CASES:
        print(f"\n--- resolution case: m_basis={m_basis}, n_collocation={n_collocation} ---")
        for n in sorted(RESOLUTION_WINDOWS.keys()):
            p_lo, p_hi = RESOLUTION_WINDOWS[n]
            p_grid = np.linspace(float(p_lo), float(p_hi), int(RESOLUTION_NPTS))
            print(f"axisymmetric continuation for n={n} window [{p_lo:.3f}, {p_hi:.3f}] MPa")
            if baseline_p_grid is not None and baseline_sols is not None:
                _, sols = solve_axisymmetric_window_seeded(
                    p_grid, baseline_p_grid=np.asarray(baseline_p_grid, dtype=float), baseline_sols=baseline_sols,
                    nd_bvp=1400, x0=x0, tol=1.0e-4, max_nodes=150000
                )
            else:
                _, sols = mw.solve_axisymmetric_fmin_continuation(
                    p_grid,
                    nd_bvp=1400,
                    x0=x0,
                    tol=1.0e-4,
                    max_nodes=150000,
                    verbose=False,
                )
            _sigs, objs = scan_p_for_n_boundary_matrix_v2(
                p_grid, sols, n=n, x0=x0, m_basis=m_basis, n_collocation=n_collocation, verbose=False
            )
            metrics = extract_metrics_from_objects(objs)
            print_resolution_study_row(n, p_grid, metrics)




def run_fine_scan(x0: float = 1.0e-3, baseline_p_grid: np.ndarray | None = None, baseline_sols: Sequence | None = None) -> None:
    print("\n=== Fine scan around balanced candidates ===")
    print(f"windows = {FINE_SCAN_WINDOWS}, npts = {FINE_SCAN_NPTS}")
    for m_basis, n_collocation in FINE_SCAN_CASES:
        print(f"\n--- fine scan case: m_basis={m_basis}, n_collocation={n_collocation} ---")
        for n in sorted(FINE_SCAN_WINDOWS.keys()):
            p_lo, p_hi = FINE_SCAN_WINDOWS[n]
            p_grid = np.linspace(float(p_lo), float(p_hi), int(FINE_SCAN_NPTS))
            print(f"axisymmetric continuation for n={n} window [{p_lo:.3f}, {p_hi:.3f}] MPa")
            if baseline_p_grid is not None and baseline_sols is not None:
                _, sols = solve_axisymmetric_window_seeded(
                    p_grid, baseline_p_grid=np.asarray(baseline_p_grid, dtype=float), baseline_sols=baseline_sols,
                    nd_bvp=1400, x0=x0, tol=1.0e-4, max_nodes=150000
                )
            else:
                _, sols = mw.solve_axisymmetric_fmin_continuation(
                    p_grid,
                    nd_bvp=1400,
                    x0=x0,
                    tol=1.0e-4,
                    max_nodes=150000,
                    verbose=False,
                )
            _sigs, objs = scan_p_for_n_boundary_matrix_v2(
                p_grid, sols, n=n, x0=x0, m_basis=m_basis, n_collocation=n_collocation, verbose=False
            )
            metrics = extract_metrics_from_objects(objs)
            print_fine_scan_row(n, p_grid, metrics)



def print_adaptive_scan_row(n: int, p_grid: np.ndarray, metrics: dict[str, np.ndarray], note: str = '') -> None:
    parts = [
        print_metric_row('balanced', p_grid, metrics['sigma_bal']),
        print_metric_row('balanced-noH', p_grid, metrics['sigma_bal_noH']),
        print_metric_row('raw', p_grid, metrics['sigma_raw']),
    ]
    suffix = f' | {note}' if note else ''
    print(f"n={n:02d} | " + ' | '.join(parts) + suffix)


def shift_window_if_edge_hit(p_grid: np.ndarray, arr: np.ndarray, edge_pad: int = 1):
    arr = np.asarray(arr, dtype=float)
    i_best = int(np.argmin(arr))
    width = float(p_grid[-1] - p_grid[0])
    p_lo = float(p_grid[0]); p_hi = float(p_grid[-1])
    shift = 0.55 * width
    if i_best <= edge_pad:
        return (p_lo - shift, p_hi - shift), 'shift_left', i_best
    if i_best >= len(p_grid) - 1 - edge_pad:
        return (p_lo + shift, p_hi + shift), 'shift_right', i_best
    return (p_lo, p_hi), 'interior', i_best


def run_adaptive_scan(x0: float = 1.0e-3, baseline_p_grid: np.ndarray | None = None, baseline_sols: Sequence | None = None) -> None:
    print("\n=== Adaptive balanced tracking around candidate windows ===")
    print(f"windows0 = {ADAPTIVE_SCAN_WINDOWS}, npts = {ADAPTIVE_SCAN_NPTS}, max_iters = {ADAPTIVE_SCAN_MAX_ITERS}")
    for m_basis, n_collocation in ADAPTIVE_SCAN_CASES:
        print(f"\n--- adaptive scan case: m_basis={m_basis}, n_collocation={n_collocation} ---")
        for n in sorted(ADAPTIVE_SCAN_WINDOWS.keys()):
            p_lo, p_hi = ADAPTIVE_SCAN_WINDOWS[n]
            for it in range(ADAPTIVE_SCAN_MAX_ITERS):
                p_grid = np.linspace(float(p_lo), float(p_hi), int(ADAPTIVE_SCAN_NPTS))
                print(f"iter={it} | n={n} | window [{p_lo:.3f}, {p_hi:.3f}] MPa")
                if baseline_p_grid is not None and baseline_sols is not None:
                    _, sols = solve_axisymmetric_window_seeded(
                        p_grid, baseline_p_grid=np.asarray(baseline_p_grid, dtype=float), baseline_sols=baseline_sols,
                        nd_bvp=1400, x0=x0, tol=1.0e-4, max_nodes=150000
                    )
                else:
                    _, sols = mw.solve_axisymmetric_fmin_continuation(
                        p_grid, nd_bvp=1400, x0=x0, tol=1.0e-4, max_nodes=150000, verbose=False
                    )
                _sigs, objs = scan_p_for_n_boundary_matrix_v2(
                    p_grid, sols, n=n, x0=x0, m_basis=m_basis, n_collocation=n_collocation, verbose=False
                )
                metrics = extract_metrics_from_objects(objs)
                (new_lo, new_hi), status, i_best = shift_window_if_edge_hit(p_grid, metrics['sigma_bal'], edge_pad=ADAPTIVE_EDGE_PAD)
                print_adaptive_scan_row(n, p_grid, metrics, note=f"best_idx={i_best}, status={status}")
                if status == 'interior':
                    break
                p_lo, p_hi = new_lo, new_hi



# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main() -> None:
    p_grid = np.linspace(0.0, BASELINE_P_MAX_MPA, BASELINE_P_NPTS)
    modes = list(BASELINE_MODES)
    x0 = 1.0e-3
    m_basis = 6
    n_collocation = 120

    metrics_by_n: dict[str, dict[int, np.ndarray]] = {
        'sigma_raw': {},
        'sigma_raw_noH': {},
        'sigma_bal': {},
        'sigma_bal_noH': {},
    }
    objs_by_n: dict[int, dict[int, BoundaryMatrixObjectsV2]] = {}

    if RUN_BASELINE_SCAN:
        print(f"=== Axisymmetric continuation for F_min background (0..{p_grid[-1]:.1f} MPa) ===")
        _, sols = mw.solve_axisymmetric_fmin_continuation(
            p_grid,
            nd_bvp=1400,
            x0=x0,
            tol=1.0e-4,
            max_nodes=150000,
            verbose=BASELINE_VERBOSE,
        )

        sig_by_n: dict[int, np.ndarray] = {}
        sample_obj = None
        for n in modes:
            print(f"\n=== Boundary-matrix sigma scan for n={n} : mixed_weak_boundary_matrix_test_v2 ===")
            sigs, objs = scan_p_for_n_boundary_matrix_v2(
                p_grid, sols, n=n, x0=x0, m_basis=m_basis, n_collocation=n_collocation, verbose=BASELINE_VERBOSE
            )
            sig_by_n[n] = sigs
            objs_by_n[n] = objs
            if n == modes[0]:
                sample_obj = objs[int(np.argmin(sigs))]

            metrics = extract_metrics_from_objects(objs)
            for key in metrics_by_n:
                metrics_by_n[key][n] = metrics[key]

        summarize_cross_mode(p_grid, sig_by_n, label="mixed_weak_boundary_matrix_test_v2")
        summarize_cross_mode(p_grid, metrics_by_n['sigma_raw'], label="mixed_weak_boundary_matrix_test_v2 : raw")
        summarize_cross_mode(p_grid, metrics_by_n['sigma_bal'], label="mixed_weak_boundary_matrix_test_v2 : balanced")
        summarize_cross_mode(p_grid, metrics_by_n['sigma_bal_noH'], label="mixed_weak_boundary_matrix_test_v2 : balanced-noH")

        if SHOW_SAMPLE_MATRICES and sample_obj is not None:
            print(f"\n=== Sample B_mix for n={sample_obj.n}, p={sample_obj.p_mpa:.3f} MPa ===")
            print_boundary_matrix(sample_obj)

        best = find_global_best(metrics_by_n['sigma_bal'], objs_by_n)
        if SHOW_SAMPLE_MATRICES and best is not None:
            _, _, _, best_bal_obj = best
            print(f"\n=== Sample B_mix_balanced global minimum at n={best_bal_obj.n}, p={best_bal_obj.p_mpa:.3f} MPa ===")
            print_boundary_matrix(best_bal_obj)

        if DEEP_DEBUG_VERBOSE:
            for n, p_target in DEEP_DEBUG_TARGETS:
                if n not in objs_by_n:
                    continue
                i = nearest_p_index(p_grid, p_target)
                obj = objs_by_n[n][i]
                print(f"\n=== Deep debug target requested at n={n}, p~{p_target:.3f} MPa; using grid point p={obj.p_mpa:.3f} MPa ===")
                deep_debug_object(obj)

        if plt is not None and PLOT_LINEAR_FULL_RANGE:
            plot_full_range_linear_metrics(p_grid, metrics_by_n)

        if plt is not None and PLOT_LOG_FULL_RANGE:
            plt.figure(figsize=(8, 5))
            for n, arr in sorted(metrics_by_n['sigma_bal'].items()):
                plt.plot(p_grid, np.log(np.maximum(arr, 1.0e-300)), marker='o', ms=3, label=f'n={n}')
            plt.xlabel('pressure p [MPa]')
            plt.ylabel('log sigma_bal')
            plt.title('mixed_weak_boundary_matrix_test_v2 : balanced criterion (log)')
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.tight_layout()
            plt.show()

    if RUN_RESOLUTION_STUDY:
        run_resolution_study(x0=x0, baseline_p_grid=p_grid if RUN_BASELINE_SCAN else None, baseline_sols=sols if RUN_BASELINE_SCAN else None)
    if RUN_FINE_SCAN:
        run_fine_scan(x0=x0, baseline_p_grid=p_grid if RUN_BASELINE_SCAN else None, baseline_sols=sols if RUN_BASELINE_SCAN else None)
    if RUN_ADAPTIVE_SCAN:
        run_adaptive_scan(x0=x0, baseline_p_grid=p_grid if RUN_BASELINE_SCAN else None, baseline_sols=sols if RUN_BASELINE_SCAN else None)


if __name__ == '__main__':
    main()
