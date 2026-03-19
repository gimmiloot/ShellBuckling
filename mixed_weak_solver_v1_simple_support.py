# -*- coding: utf-8 -*-
"""
mixed_weak_solver_v1.py

Первая тестовая версия solver-а для нового mixed weak criterion.

Идея этой версии:
1) осесимметрический фон считается на F_min background family;
2) неосесимметрическая задача НЕ приводится к старому 5D/6D shooting виду;
3) вместо этого используется глобальный trial-space / collocation surrogate для
   нового mixed weak class с полями

       U = (u_s, u_n, v, phi, psi)

   и главным окружным блоком

       (v, S), (psi, H, chi).

4) center-regularity зашивается через weighted basis functions x^p * t^k;
5) для заданных (n, q) собирается глобальная прямоугольная матрица residual-ов,
   а тестовым критерием служит ее sigma_min.

Это НЕ окончательный solver нового критерия. Это исследовательский prototype,
который нужен, чтобы проверить, меняется ли qualitative picture после перехода
к новому operator class.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

import numpy as np
from scipy.integrate import solve_bvp

try:
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover
    plt = None


# ============================================================
# Material / geometry constants
# ============================================================

nu = 0.3
E = 205e9
h = 0.005
a = 0.5
mu = a / h
Lambda = 12.0 * (1.0 - nu**2) * mu**2
C_twist = 12.0 * (1.0 + nu) * mu**2

# Global dimensional pressure inside axisymmetric BVP ODE
q_pa = 0.0


# ============================================================
# Axisymmetric F_min background (copied from the previous working solver)
# ============================================================

def axisymmetric_fmin_ode(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    global q_pa

    x_safe = np.maximum(np.asarray(x, dtype=float), 1.0e-12)

    T_s0 = y[0]
    Q0 = y[1]
    M_s0 = y[2]
    r0 = np.maximum(y[3], 1.0e-12)
    phi0 = y[4]

    e_theta0 = (r0 - x_safe) / x_safe
    e_s0 = (1.0 - nu**2) * T_s0 - nu * e_theta0
    T_theta0 = nu * T_s0 + e_theta0

    sinphi0 = np.sin(phi0)
    cosphi0 = np.cos(phi0)

    M_theta0 = nu * M_s0 + sinphi0 / (12.0 * mu**2 * r0)
    phi0_prime = Lambda * (M_s0 - nu * M_theta0)

    qbar = (q_pa * a) / (E * h)

    dT_s0 = -(T_s0 / r0) + (cosphi0 / r0) * T_theta0 - phi0_prime * Q0
    dQ0 = -(Q0 / r0) + (sinphi0 / r0) * T_theta0 + phi0_prime * T_s0 - qbar
    dM_s0 = -(M_s0 / r0) + (cosphi0 / r0) * M_theta0 + Q0
    dr0 = (1.0 + e_s0) * cosphi0
    dphi0 = phi0_prime

    return np.vstack([dT_s0, dQ0, dM_s0, dr0, dphi0])


def axisymmetric_fmin_bc(ya: np.ndarray, yb: np.ndarray, x0: float) -> np.ndarray:
    return np.array(
        [
            yb[0],              # T_s0(1) = 0
            yb[4],              # phi0(1) = 0
            ya[1],              # Q0(x0) = 0
            ya[3] - float(x0),  # r0(x0) = x0
            ya[4],              # phi0(x0) = 0
        ],
        dtype=float,
    )


def solve_axisymmetric_fmin_continuation(
    p_mpa_grid: Iterable[float],
    nd_bvp: int = 1400,
    x0: float = 1.0e-3,
    tol: float = 1.0e-4,
    max_nodes: int = 150000,
    verbose: bool = True,
) -> Tuple[np.ndarray, List]:
    global q_pa

    p_grid = np.asarray(list(p_mpa_grid), dtype=float)
    x_mesh = np.linspace(float(x0), 1.0, int(nd_bvp))

    y_guess = np.zeros((5, x_mesh.size), dtype=float)
    y_guess[3] = x_mesh

    sols = []
    sol_prev = None

    for i, p_mpa in enumerate(p_grid):
        q_pa = float(p_mpa) * 1.0e6

        if sol_prev is not None:
            y_guess = sol_prev.sol(x_mesh)

        bc = lambda ya, yb: axisymmetric_fmin_bc(ya, yb, x0=float(x0))
        sol = solve_bvp(
            axisymmetric_fmin_ode,
            bc,
            x_mesh,
            y_guess,
            tol=tol,
            max_nodes=max_nodes,
            verbose=0,
        )

        if not sol.success:
            sol = solve_bvp(
                axisymmetric_fmin_ode,
                bc,
                x_mesh,
                y_guess,
                tol=min(5.0e-4, 5.0 * tol),
                max_nodes=max_nodes,
                verbose=0,
            )

        if not sol.success:
            raise RuntimeError(f"Axisymmetric F_min BVP failed at p={p_mpa:.6f} MPa: {sol.message}")

        sols.append(sol)
        sol_prev = sol

        if verbose and (i % 10 == 0 or i == len(p_grid) - 1):
            yv = sol.sol(x_mesh)
            min_r = float(np.min(yv[3]))
            max_rms = float(np.max(sol.rms_residuals)) if hasattr(sol, "rms_residuals") else float("nan")
            print(
                f"[pre-Fmin] i={i:03d} p={p_mpa:.3f} MPa  nodes={sol.x.size}  "
                f"max_rms={max_rms:.2e}  min(r0)={min_r:.6f}"
            )

    return x_mesh, sols


# ============================================================
# Background interpolation and helpers
# ============================================================


def cumulative_trapezoid_from_values(x: np.ndarray, f: np.ndarray) -> np.ndarray:
    out = np.zeros_like(f)
    if len(x) <= 1:
        return out
    dx = np.diff(x)
    out[1:] = np.cumsum(0.5 * dx * (f[:-1] + f[1:]))
    return out


@dataclass
class BaseInterp:
    xb: np.ndarray
    r: np.ndarray
    r_prime: np.ndarray
    r_double_prime: np.ndarray
    z: np.ndarray
    T_s: np.ndarray
    T_sn: np.ndarray
    M_s: np.ndarray
    varphi: np.ndarray
    varphi_prime: np.ndarray
    e_s: np.ndarray
    T_theta: np.ndarray
    M_theta: np.ndarray
    q: float

    def at_many(self, x: np.ndarray) -> dict[str, np.ndarray]:
        xb = self.xb
        def interp(arr: np.ndarray) -> np.ndarray:
            return np.interp(x, xb, arr)
        r = interp(self.r)
        rp = interp(self.r_prime)
        rpp = interp(self.r_double_prime)
        phi = interp(self.varphi)
        phip = interp(self.varphi_prime)
        return {
            "r": r,
            "r_prime": rp,
            "r_double_prime": rpp,
            "z": interp(self.z),
            "T_s": interp(self.T_s),
            "T_sn": interp(self.T_sn),
            "M_s": interp(self.M_s),
            "varphi": phi,
            "varphi_prime": phip,
            "e_s": interp(self.e_s),
            "T_theta": interp(self.T_theta),
            "M_theta": interp(self.M_theta),
            "q": np.full_like(x, float(self.q), dtype=float),
            "c0": np.cos(phi),
            "s0": np.sin(phi),
            "a": rp / np.maximum(r, 1.0e-12),
            "a_prime": (rpp * np.maximum(r, 1.0e-12) - rp * rp) / np.maximum(r, 1.0e-12) ** 2,
            "lambda_s0": 1.0 + interp(self.e_s),
            "lambda_theta0": r / np.maximum(x, 1.0e-12),
            "kappa_s0": phip,
            "kappa_theta0": np.sin(phi) / np.maximum(r, 1.0e-12),
        }


def build_base_interp(sol, p_mpa: float, nd_base: int = 4000) -> BaseInterp:
    global q_pa
    q_pa = float(p_mpa) * 1.0e6
    qbar = (q_pa * a) / (E * h)

    xb = np.linspace(float(sol.x[0]), 1.0, int(nd_base))
    yb = sol.sol(xb)

    T_s0 = yb[0]
    Q0 = yb[1]
    M_s0 = yb[2]
    r0 = np.maximum(yb[3], 1.0e-12)
    phi0 = yb[4]

    e_theta0 = (r0 - xb) / np.maximum(xb, 1.0e-12)
    e_s0 = (1.0 - nu**2) * T_s0 - nu * e_theta0
    T_theta0 = nu * T_s0 + e_theta0
    M_theta0 = nu * M_s0 + np.sin(phi0) / (12.0 * mu**2 * r0)
    phi0_prime = Lambda * (M_s0 - nu * M_theta0)

    yprime = axisymmetric_fmin_ode(xb, yb)
    r0_prime = yprime[3]
    r0_double_prime = np.gradient(r0_prime, xb, edge_order=2)

    z0_prime = -(1.0 + e_s0) * np.sin(phi0)
    z0 = cumulative_trapezoid_from_values(xb, z0_prime)

    return BaseInterp(
        xb=xb,
        r=r0,
        r_prime=r0_prime,
        r_double_prime=r0_double_prime,
        z=z0,
        T_s=T_s0,
        T_sn=Q0,
        M_s=M_s0,
        varphi=phi0,
        varphi_prime=phi0_prime,
        e_s=e_s0,
        T_theta=T_theta0,
        M_theta=M_theta0,
        q=qbar,
    )


# ============================================================
# Weighted polynomial trial space
# ============================================================

FIELD_ORDER = ["u_s", "u_n", "v", "phi", "psi", "T_s", "Q_s", "M_s"]


def field_exponent(name: str, n: int) -> int:
    if name in ("u_s", "u_n", "v"):
        return n
    if name in ("phi", "psi", "T_s"):
        return n - 1
    if name in ("Q_s", "M_s"):
        return n - 2
    raise KeyError(name)


def poly_basis_triplet(x: np.ndarray, x0: float, p: int, k: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Basis function: x^p * t^k,  where t=(x-x0)/(1-x0).
    Returns value, first derivative, second derivative.
    """
    x = np.asarray(x, dtype=float)
    L = 1.0 - float(x0)
    t = (x - float(x0)) / L

    xpow = x**p
    tk = t**k if k > 0 else np.ones_like(x)

    val = xpow * tk

    if p == 0:
        dx_xpow = np.zeros_like(x)
        d2x_xpow = np.zeros_like(x)
    elif p == 1:
        dx_xpow = np.ones_like(x)
        d2x_xpow = np.zeros_like(x)
    else:
        dx_xpow = p * x**(p - 1)
        d2x_xpow = p * (p - 1) * x**(p - 2)

    if k == 0:
        dt_tk = np.zeros_like(x)
        d2t_tk = np.zeros_like(x)
    elif k == 1:
        dt_tk = np.ones_like(x)
        d2t_tk = np.zeros_like(x)
    else:
        dt_tk = k * t**(k - 1)
        d2t_tk = k * (k - 1) * t**(k - 2)

    d1 = dx_xpow * tk + xpow * dt_tk / L
    d2 = d2x_xpow * tk + 2.0 * dx_xpow * dt_tk / L + xpow * d2t_tk / (L * L)
    return val, d1, d2


@dataclass
class TrialSpace:
    n: int
    x0: float
    m_basis: int

    @property
    def n_unknowns(self) -> int:
        return len(FIELD_ORDER) * self.m_basis

    def decode_column(self, col: int) -> tuple[str, int]:
        fidx = col // self.m_basis
        k = col % self.m_basis
        return FIELD_ORDER[fidx], k

    def basis_eval(self, x: np.ndarray, col: int) -> dict[str, np.ndarray]:
        name, k = self.decode_column(col)
        p = field_exponent(name, self.n)
        val, d1, d2 = poly_basis_triplet(x, self.x0, p, k)

        out = {nm: np.zeros_like(x) for nm in FIELD_ORDER}
        out_d1 = {nm: np.zeros_like(x) for nm in FIELD_ORDER}
        out_d2 = {nm: np.zeros_like(x) for nm in FIELD_ORDER}

        out[name] = val
        out_d1[name] = d1
        out_d2[name] = d2

        merged = {}
        for nm in FIELD_ORDER:
            merged[nm] = out[nm]
            merged[nm + "_x"] = out_d1[nm]
            merged[nm + "_xx"] = out_d2[nm]
        return merged

    def basis_eval_full(self, x: np.ndarray, col: int, base: 'BaseInterp' | None = None) -> dict[str, np.ndarray]:
        """
        Extended basis evaluation.

        Returns the primary trial channels together with the algebraically
        reconstructed mixed-weak channels (S, H, chi, T_theta, M_theta, ... )
        whenever the axisymmetric background ``base`` is provided.
        """
        core = self.basis_eval(x, col)
        if base is None:
            return dict(core)
        return evaluate_all_channels_for_basis(x=x, base=base, space=self, col=col, vals=core)


# ============================================================
# Pointwise reconstruction of derived mixed-weak channels
# ============================================================

def evaluate_all_channels_for_basis(
    x: np.ndarray,
    base: BaseInterp,
    space: TrialSpace,
    col: int,
    vals: dict[str, np.ndarray] | None = None,
) -> dict[str, np.ndarray]:
    """
    Reconstruct all channels for a single basis column using the same algebraic
    formulas as in ``assemble_operator_column``.

    This makes the bulk channels S(x), H(x), chi(x), ... observable for the
    boundary-matrix diagnostics, instead of only appearing through the right
    boundary functional at x=1.
    """
    x = np.asarray(x, dtype=float)
    if vals is None:
        vals = space.basis_eval(x, col)
    else:
        vals = {k: np.asarray(v, dtype=float) for k, v in vals.items()}

    b = base.at_many(x)
    x_safe = np.maximum(x, 1.0e-10)
    r0 = np.maximum(b["r"], 1.0e-10)
    c0 = b["c0"]
    s0 = b["s0"]
    a0 = b["a"]
    a0_p = b["a_prime"]
    lam_s0 = b["lambda_s0"]
    lam_th0 = b["lambda_theta0"]
    kap_s0 = b["kappa_s0"]
    kap_th0 = b["kappa_theta0"]

    n = space.n
    b_s = n / x_safe
    b_m = n / x_safe
    b_theta = n / r0
    b_s_p = -n / (x_safe * x_safe)

    us = vals["u_s"]
    us_x = vals["u_s_x"]
    un = vals["u_n"]
    un_x = vals["u_n_x"]
    v = vals["v"]
    v_x = vals["v_x"]
    v_xx = vals["v_xx"]
    phi = vals["phi"]
    phi_x = vals["phi_x"]
    psi = vals["psi"]
    psi_x = vals["psi_x"]
    psi_xx = vals["psi_xx"]
    Ts = vals["T_s"]
    Ms = vals["M_s"]

    r = c0 * us + s0 * un
    r_x = (-kap_s0 * s0) * us + c0 * us_x + (kap_s0 * c0) * un + s0 * un_x

    e_theta = r / x_safe + (n / x_safe) * v
    T_theta = nu * Ts + e_theta
    e_s = Ts - nu * T_theta

    S = (v_x - a0 * v - (n / x_safe) * us) / (2.0 * (1.0 + nu))
    S_x = (v_xx - a0_p * v - a0 * v_x + (n / x_safe**2) * us - (n / x_safe) * us_x) / (2.0 * (1.0 + nu))

    kappa_theta_new = (c0 / r0) * phi - (s0 / (r0 * r0)) * r + b_theta * psi
    M_theta = nu * Ms + kappa_theta_new / Lambda

    phi_rhs = Lambda * (Ms - nu * M_theta)

    H = (psi_x - a0 * psi - b_s * phi) / C_twist
    H_x = (psi_xx - a0_p * psi - a0 * psi_x - b_s_p * phi - b_s * phi_x) / C_twist

    chi = (b_theta * M_theta - H_x - 2.0 * a0 * H) / lam_th0

    out = dict(vals)
    out.update({
        "r": r,
        "r_x": r_x,
        "e_theta": e_theta,
        "e_s": e_s,
        "T_theta": T_theta,
        "S": S,
        "S_x": S_x,
        "kappa_theta_new": kappa_theta_new,
        "M_theta": M_theta,
        "phi_rhs": phi_rhs,
        "H": H,
        "H_x": H_x,
        "chi": chi,
        "b_s": b_s,
        "b_m": b_m,
        "b_theta": b_theta,
        "lambda_s0": lam_s0,
        "lambda_theta0": lam_th0,
        "kappa_s0": kap_s0,
        "kappa_theta0": kap_th0,
    })
    return out


# Runtime aliases used by diagnostic testbenches
basis_eval_full = evaluate_all_channels_for_basis
evaluate_basis_channels_full = evaluate_all_channels_for_basis
compute_resultant_channels = evaluate_all_channels_for_basis
postprocess_channels = evaluate_all_channels_for_basis

# ============================================================
# Mixed weak collocation residual assembly
# ============================================================


def assemble_operator_column(
    x: np.ndarray,
    base: BaseInterp,
    space: TrialSpace,
    col: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Assemble one column of the global collocation matrix and one column of the
    boundary functional matrix.

    Unknown primary trial fields are
        (u_s, u_n, v, phi, psi, T_s, Q_s, M_s)
    with weighted polynomial center-regular basis.

    All other fields are reconstructed algebraically:
        T_theta, S, M_theta, H, chi.
    """
    n = space.n
    vals = space.basis_eval(x, col)
    b = base.at_many(x)

    x_safe = np.maximum(x, 1.0e-10)
    r0 = np.maximum(b["r"], 1.0e-10)
    c0 = b["c0"]
    s0 = b["s0"]
    a0 = b["a"]
    a0_p = b["a_prime"]
    lam_s0 = b["lambda_s0"]
    lam_th0 = b["lambda_theta0"]
    kap_s0 = b["kappa_s0"]
    kap_th0 = b["kappa_theta0"]

    # first working coefficients in the corrected mixed weak class
    b_s = n / x_safe
    b_m = n / x_safe
    b_theta = n / r0
    b_s_p = -n / (x_safe * x_safe)

    us = vals["u_s"]
    us_x = vals["u_s_x"]
    un = vals["u_n"]
    un_x = vals["u_n_x"]
    v = vals["v"]
    v_x = vals["v_x"]
    v_xx = vals["v_xx"]
    phi = vals["phi"]
    phi_x = vals["phi_x"]
    psi = vals["psi"]
    psi_x = vals["psi_x"]
    psi_xx = vals["psi_xx"]
    Ts = vals["T_s"]
    Ts_x = vals["T_s_x"]
    Qs = vals["Q_s"]
    Qs_x = vals["Q_s_x"]
    Ms = vals["M_s"]
    Ms_x = vals["M_s_x"]

    # local tangent-normal -> radial perturbation
    r = c0 * us + s0 * un
    r_x = (-kap_s0 * s0) * us + c0 * us_x + (kap_s0 * c0) * un + s0 * un_x

    e_theta = r / x_safe + (n / x_safe) * v
    Ttheta = nu * Ts + e_theta
    e_s = Ts - nu * Ttheta

    # membrane shear resultant reconstructed from v'
    S = (v_x - a0 * v - (n / x_safe) * us) / (2.0 * (1.0 + nu))
    S_x = (v_xx - a0_p * v - a0 * v_x + (n / x_safe**2) * us - (n / x_safe) * us_x) / (2.0 * (1.0 + nu))

    kappa_theta_new = (c0 / r0) * phi - (s0 / (r0 * r0)) * r + b_theta * psi
    Mtheta = nu * Ms + kappa_theta_new / Lambda

    phi_rhs = Lambda * (Ms - nu * Mtheta)

    H = (psi_x - a0 * psi - b_s * phi) / C_twist
    H_x = (psi_xx - a0_p * psi - a0 * psi_x - b_s_p * phi - b_s * phi_x) / C_twist

    chi = (b_theta * Mtheta - H_x - 2.0 * a0 * H) / lam_th0

    # corrected prestress / load forcing from the weak reconstruction
    g_s = -(b["T_theta"] / r0) * r_x - b["T_sn"] * phi_x
    g_n = b["T_s"] * phi_x + (c0 / x_safe) * b["T_theta"] * phi - (b["q"] / x_safe) * (r0 * e_s + lam_s0 * r)

    # residuals (prototype mixed weak -> strong surrogate)
    R_us = us_x - (e_s + kap_s0 * un)
    R_un = un_x - (kap_s0 * us - lam_s0 * phi)
    R_gtheta = b_m * un + lam_th0 * psi - kap_th0 * v
    R_phi = phi_x - phi_rhs

    R_Ts = Ts_x + a0 * Ts - (c0 / x_safe) * Ttheta + (n / x_safe) * S - kap_s0 * Qs - (s0 * c0 / (r0 * r0)) * Mtheta - g_s

    R_Qs = Qs_x + a0 * Qs - kap_s0 * Ts + (s0 / x_safe) * Ttheta - (s0 * s0 / (r0 * r0)) * Mtheta + b_m * chi - g_n

    R_Ms = Ms_x + a0 * Ms - a0 * Mtheta - Qs + (n / x_safe) * H - (b["M_theta"] / r0) * r_x

    R_v = S_x + (2.0 / x_safe) * S - (n / x_safe) * Ttheta + kap_th0 * chi

    resid = np.vstack([R_us, R_un, R_gtheta, R_phi, R_Ts, R_Qs, R_Ms, R_v])

    # right-boundary functionals for the chosen support model:
    # u_n(1)=0, phi(1)=0, T_s(1)=0, S(1)=0, H(1)=0
    x1 = np.array([1.0], dtype=float)
    vals1 = space.basis_eval(x1, col)
    b1 = base.at_many(x1)

    us1 = vals1["u_s"][0]
    un1 = vals1["u_n"][0]
    v1 = vals1["v"][0]
    vx1 = vals1["v_x"][0]
    vxx1 = vals1["v_xx"][0]
    phi1 = vals1["phi"][0]
    phix1 = vals1["phi_x"][0]
    psi1 = vals1["psi"][0]
    psix1 = vals1["psi_x"][0]
    psixx1 = vals1["psi_xx"][0]
    Ts1 = vals1["T_s"][0]
    Ms1 = vals1["M_s"][0]

    r01 = float(b1["r"][0])
    c01 = float(b1["c0"][0])
    s01 = float(b1["s0"][0])
    a01 = float(b1["a"][0])
    a01p = float(b1["a_prime"][0])
    kap_th01 = float(b1["kappa_theta0"][0])
    lam_th01 = float(b1["lambda_theta0"][0])
    b_s1 = float(n / 1.0)
    b_theta1 = float(n / r01)

    r1 = c01 * us1 + s01 * un1
    e_theta1 = r1 + n * v1
    Ttheta1 = nu * Ts1 + e_theta1
    kappa_theta1 = (c01 / r01) * phi1 - (s01 / (r01 * r01)) * r1 + b_theta1 * psi1
    Mtheta1 = nu * Ms1 + kappa_theta1 / Lambda
    H1 = (psix1 - a01 * psi1 - b_s1 * phi1) / C_twist
    _ = (b_theta1 * Mtheta1 - (psixx1 - a01p * psi1 - a01 * psix1 + n * phi1 - b_s1 * phix1) / C_twist - 2.0 * a01 * H1) / lam_th01
    S1 = (vx1 - a01 * v1 - n * us1) / (2.0 * (1.0 + nu))

    # simple support (variant A): u_n(1)=0, M_s(1)=0, and natural conditions\n    # T_s(1)=0, S(1)=0, H(1)=0 for the free boundary dofs u_s, v, psi.
    bvec = np.array([un1, Ms1, Ts1, S1, H1], dtype=float)
    return resid, bvec


@dataclass
class MixedWeakObjects:
    space: TrialSpace
    x_col: np.ndarray
    A: np.ndarray
    B: np.ndarray
    sigma_min: float
    singvals: np.ndarray



def build_mixed_weak_objects(
    n: int,
    base: BaseInterp,
    x0: float = 1.0e-3,
    m_basis: int = 6,
    n_collocation: int = 120,
) -> MixedWeakObjects:
    """
    Assemble the global rectangular operator matrix for the prototype
    mixed weak criterion.

    Unknowns are weighted polynomial coefficients for the primary trial fields.
    """
    space = TrialSpace(n=int(n), x0=float(x0), m_basis=int(m_basis))
    x_col = np.linspace(float(x0), 1.0, int(n_collocation) + 2)[1:-1]

    n_eq = 8 * x_col.size
    n_bc = 5
    n_unknowns = space.n_unknowns

    A = np.zeros((n_eq + n_bc, n_unknowns), dtype=float)
    B = np.zeros((n_bc, n_unknowns), dtype=float)

    for col in range(n_unknowns):
        resid, bvec = assemble_operator_column(x_col, base, space, col)
        A[:n_eq, col] = resid.reshape(-1, order="F")
        A[n_eq:, col] = bvec
        B[:, col] = bvec

    svals = np.linalg.svd(A, compute_uv=False)
    sigma_min = float(svals[-1])

    return MixedWeakObjects(
        space=space,
        x_col=x_col,
        A=A,
        B=B,
        sigma_min=sigma_min,
        singvals=svals,
    )


# ============================================================
# Scanning utilities
# ============================================================


def sigma_metrics_mixed_weak(obj: MixedWeakObjects) -> tuple[float, float]:
    sigma_min = float(obj.sigma_min)
    log_sigma = float(np.log(max(sigma_min, 1.0e-300)))
    return sigma_min, log_sigma



def scan_p_for_n_mixed_weak(
    p_grid: Sequence[float],
    sols: Sequence,
    n: int,
    label: str,
    x0: float = 1.0e-3,
    m_basis: int = 6,
    n_collocation: int = 120,
    verbose: bool = True,
) -> tuple[np.ndarray, dict]:
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



def summarize_cross_mode(p_grid: Sequence[float], logsig_by_n: dict[int, np.ndarray], label: str) -> None:
    print(f"\n=== Cross-mode comparison summary : {label} ===")
    for n in sorted(logsig_by_n.keys()):
        arr = np.asarray(logsig_by_n[n], dtype=float)
        i_best = int(np.argmin(arr))
        print(
            f"n={n:02d} | best at p={float(p_grid[i_best]):.3f} MPa | "
            f"log(sigmin)={float(arr[i_best]):.6e}"
        )



def plot_sigma_curves(p_grid: Sequence[float], logsig_by_n: dict[int, np.ndarray], label: str) -> None:
    if plt is None:
        return
    plt.figure(figsize=(8, 5))
    for n, arr in sorted(logsig_by_n.items()):
        plt.plot(p_grid, arr, marker="o", ms=3, label=f"n={n}")
    plt.xlabel("pressure p [MPa]")
    plt.ylabel("log sigma_min")
    plt.title(label)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


# ============================================================
# Main
# ============================================================


def main() -> None:
    # Pressure scan
    p_grid = np.linspace(0.0, 6.0, 24)

    # Harmonics to compare
    modes = [12, 13, 14, 15]

    # Prototype weak discretization parameters
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
