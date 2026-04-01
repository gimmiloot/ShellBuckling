# -*- coding: utf-8 -*-
"""
Internal shared helpers for mixed-weak boundary assembly and reduced-mode
diagnostics.

These utilities are structural extractions only: they keep the current
equations and boundary meaning untouched while removing repeated assembly and
diagnostic code from the task-facing scan/search modules.
"""
from __future__ import annotations

import inspect
from typing import Any, Sequence

import numpy as np


def make_row_scale(nu: float, c_twist: float) -> np.ndarray:
    return np.array([1.0, 1.0, 1.0, 2.0 * (1.0 + float(nu)), float(c_twist)], dtype=float)


def balanced_Bmix(
    B: np.ndarray,
    *,
    row_scale: np.ndarray | None = None,
    nu: float | None = None,
    c_twist: float | None = None,
) -> np.ndarray:
    if row_scale is None:
        if nu is None or c_twist is None:
            raise ValueError("Either row_scale or both nu/c_twist must be provided.")
        row_scale = make_row_scale(nu, c_twist)
    return np.asarray(row_scale, dtype=float)[:, None] * np.asarray(B, dtype=float)


def assemble_interior_and_boundary(
    *,
    mw_module: Any,
    n: int,
    base: Any,
    x0: float = 1.0e-3,
    m_basis: int = 6,
    n_collocation: int = 120,
) -> tuple[Any, np.ndarray, np.ndarray, np.ndarray]:
    space = mw_module.TrialSpace(n=int(n), x0=float(x0), m_basis=int(m_basis))
    x_col = np.linspace(float(x0), 1.0, int(n_collocation) + 2, dtype=float)[1:-1]
    n_eq = 8 * x_col.size
    n_unknowns = space.n_unknowns
    A_int = np.zeros((n_eq, n_unknowns), dtype=float)
    B_full = np.zeros((5, n_unknowns), dtype=float)
    for col in range(n_unknowns):
        resid, bvec = mw_module.assemble_operator_column(x_col, base, space, col)
        A_int[:, col] = resid.reshape(-1, order="F")
        B_full[:, col] = bvec
    return space, x_col, A_int, B_full


def make_center_constraint_matrix(space: Any, base: Any) -> np.ndarray:
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
    lam_c = float(b0["lambda_s0"][0])
    n = space.n
    C = np.zeros((4, space.n_unknowns), dtype=float)
    xpow_us = space.x0**n
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
    """Constrained least squares via KKT: min ||A c||^2 + reg ||c||^2 s.t. C c = d."""
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


def build_two_mode_regular_family(A_int: np.ndarray, C_center: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    d1 = np.array([1.0, 0.0, 0.0, 0.0], dtype=float)
    d2 = np.array([0.0, 1.0, 0.0, 0.0], dtype=float)
    c1 = solve_constrained_mode(A_int, C_center, d1)
    c2_raw = solve_constrained_mode(A_int, C_center, d2)
    c2 = orthogonalize_against(c2_raw, c1)
    V_reg = np.column_stack([c1, c2])
    residual_norms = np.array([np.linalg.norm(A_int @ c1), np.linalg.norm(A_int @ c2)], dtype=float)
    center_values = C_center @ V_reg
    return c1, c2, V_reg, residual_norms, center_values


def sample_indices(x_grid: np.ndarray, checkpoints: Sequence[float]) -> list[int]:
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


def _call_with_supported_kwargs(fn: Any, **kwargs: Any) -> Any:
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError):
        return None
    params = sig.parameters
    accepts_varkw = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values())
    call_kwargs: dict[str, Any] = {}
    for key, val in kwargs.items():
        if accepts_varkw or key in params:
            call_kwargs[key] = val
    try:
        return fn(**call_kwargs)
    except TypeError:
        return None


def _discover_extended_channel_dict(
    *,
    mw_module: Any,
    space: Any,
    base: Any,
    x: np.ndarray,
    col: int,
    core_vals: dict[str, np.ndarray],
) -> dict[str, np.ndarray]:
    n_x = x.size
    candidates: list[tuple[str, Any]] = []

    candidate_names = [
        "basis_eval_full",
        "basis_eval_extended",
        "basis_eval_ex",
        "eval_full",
        "evaluate_all_channels",
        "evaluate_all_channels_for_basis",
        "evaluate_basis_channels",
        "evaluate_basis_channels_full",
        "probe_basis_channels",
        "reconstruct_basis_channels",
        "postprocess_basis_channels",
        "postprocess_channels",
        "compute_extra_channels",
        "compute_resultant_channels",
        "resultant_eval",
        "resultant_basis_eval",
    ]

    for owner_name, owner in [("space", space), ("mw", mw_module), ("base", base)]:
        if owner is None:
            continue
        for name in candidate_names:
            fn = getattr(owner, name, None)
            if callable(fn):
                candidates.append((f"{owner_name}.{name}", fn))

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
        "u_n": float(boundary_mode[0]),
        "phi": float(boundary_mode[1]),
        "T_s": float(boundary_mode[2]),
        "S": float(boundary_mode[3]),
        "H": float(boundary_mode[4]),
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
    *,
    mw_module: Any,
    space: Any,
    base: Any,
    coeffs: np.ndarray,
    x: np.ndarray,
    B_full: np.ndarray | None = None,
) -> dict[str, np.ndarray]:
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
        extra = _discover_extended_channel_dict(
            mw_module=mw_module,
            space=space,
            base=base,
            x=x,
            col=col,
            core_vals=core,
        )
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
    return _inject_exact_boundary_rows(out, x, boundary_mode)


def available_channel_names(*, mw_module: Any, space: Any, base: Any = None) -> list[str]:
    x_probe = np.array([space.x0, 0.25, 0.75, 1.0], dtype=float)
    vals = _normalize_channel_dict(space.basis_eval(x_probe, 0), x_probe.size)
    extra = _discover_extended_channel_dict(
        mw_module=mw_module,
        space=space,
        base=base,
        x=x_probe,
        col=0,
        core_vals=vals,
    )
    return sorted(set(vals.keys()) | set(extra.keys()))


def channel_alias(channels: dict[str, np.ndarray], *names: str) -> np.ndarray | None:
    for name in names:
        if name in channels:
            return channels[name]
    return None


def build_local_Bmix_from_channels(
    ch1: dict[str, np.ndarray],
    ch2: dict[str, np.ndarray],
    j: int,
    row_specs: Sequence[tuple[str, Sequence[str]]],
) -> tuple[np.ndarray | None, list[str], list[str], list[str]]:
    rows = []
    missing: list[str] = []
    available_labels: list[str] = []
    nonfinite: list[str] = []
    for label, aliases in row_specs:
        a1 = channel_alias(ch1, *aliases)
        a2 = channel_alias(ch2, *aliases)
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


def safe_sigma_min(A: np.ndarray) -> float | None:
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
