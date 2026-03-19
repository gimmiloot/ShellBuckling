# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_bvp

# ---------------- parameters ----------------
nu = 0.3
Ee = 205e9
h = 0.005
a = 0.5
mu = a / h
beta = np.sqrt(12.0 * (1.0 - nu**2)) * mu
gamma = 12.0 * (1.0 - nu**2) * mu**2

q = 0.0  # global Pa


# ---------------- NON-SHALLOW ----------------
def axisym_nepol(x, y):
    """
    Non-shallow axisymmetric prebuckling system with corrected plate geometry:
        r = x + u_r,
        e_theta = u_r / x,
        T_theta = nu*T_s + u_r/x.
    State:
        y = [T_s, T_sn, M_s, u_r, u_z, phi]
    """
    x = np.asarray(x, dtype=float)
    x_safe = np.maximum(x, 1.0e-12)

    Ts, Tsn, Ms, ur, uz, phi = y

    # corrected deformed radius
    r = x_safe + ur

    # circumferential strain / force closure
    etheta = ur / x_safe
    es = Ts * (1.0 - nu**2) - nu * etheta
    Ttheta = nu * Ts + etheta

    # curvature / circumferential moment
    kappa_s = 12.0 * (1.0 - nu**2) * Ms * mu**2 - nu * (np.sin(phi) / r)
    Mtheta  = nu * Ms + np.sin(phi) / (12.0 * mu**2 * r)

    qbar = q * a / (Ee * h)

    return np.vstack((
        # T_s'
        -(Ts / r) + (np.cos(phi) * Ttheta) / r - kappa_s * Tsn,
        # T_sn'
        -(Tsn / r) + (np.sin(phi) * Ttheta) / r + kappa_s * Ts - qbar,
        # M_s'
        -(Ms / r) + (np.cos(phi) * Mtheta) / r + Tsn,
        # u_r'
        (1.0 + es) * np.cos(phi) - 1.0,
        # u_z'
        -mu * (1.0 + es) * np.sin(phi),
        # phi'
        kappa_s
    ))


def bcNP(ya, yb):
    # Ts(1)=0, Tsn(r0)=0, ur(r0)=0, uz(1)=0, phi(r0)=0, phi(1)=0
    return np.array([yb[0], ya[1], ya[3], yb[4], ya[5], yb[5]], float)


# ---------------- SHALLOW ----------------
def fun_shallow(x, y):
    x = np.asarray(x, dtype=float)
    x_safe = np.maximum(x, 1.0e-12)
    return np.vstack((
        -y[0] / x_safe + y[1] / x_safe**2 + y[3] * (y[1] / x_safe) + q * x_safe / 2.0 * beta**3 * mu / Ee,
        y[0],
        -y[2] / x_safe + y[3] / x_safe**2 - y[1] * (y[1] / (2.0 * x_safe)),
        y[2]
    ))


def bc_sh(ya, yb):
    return np.array([ya[1], yb[1], ya[3], yb[3]], float)


def solve_one(system, q_pa, x_mesh, y_guess, tol, max_nodes):
    global q
    q = float(q_pa)
    if system == "nepol":
        return solve_bvp(axisym_nepol, bcNP, x_mesh, y_guess, tol=tol, max_nodes=max_nodes, verbose=0)
    else:
        return solve_bvp(fun_shallow, bc_sh, x_mesh, y_guess, tol=tol, max_nodes=max_nodes, verbose=0)


def continuation_to(system, q_target, nd, r0, tol, max_nodes, n_steps):
    q_list = np.linspace(0.0, float(q_target), n_steps)
    x_mesh = np.linspace(r0, 1.0, nd)
    ny = 6 if system == "nepol" else 4
    y_guess = np.zeros((ny, x_mesh.size))
    sol_prev = None

    for qk in q_list:
        if sol_prev is not None:
            y_guess = sol_prev.sol(x_mesh)

        sol = solve_one(system, qk, x_mesh, y_guess, tol, max_nodes)
        if not sol.success:
            sol = solve_one(system, qk, x_mesh, y_guess, min(5e-4, 5 * tol), max_nodes)
        if not sol.success:
            raise RuntimeError(f"{system} failed at q={qk}: {sol.message}")

        sol_prev = sol

    return sol_prev


# ---------------- det(U_N) via slogdet (same as your working version) ----------------
def det_UN_slog(theta, dtheta, dphi, phi_p, delta, n):
    theta = np.asarray(theta, float)
    dtheta = np.asarray(dtheta, float)
    dphi = np.asarray(dphi, float)
    phi_p = np.asarray(phi_p, float)

    N = len(theta)
    n2 = n * n
    n4 = n2 * n2
    dd = delta * delta

    Dm = np.array([
        [1 / (2 * delta), 0, 0, 0],
        [1 / (2 * delta), 0, 0, 0],
        [0, 1 / (2 * delta), 0, 0],
        [0, 0, 0, 0]
    ], float)

    Em = np.array([
        [-n2, 0, 0, 0],
        [-1,  0, 0, 0],
        [0,   0, 0, 0],
        [0,   1, 0, 0]
    ], float)

    dth, dph, th, ph = dtheta[0], dphi[0], theta[0], phi_p[0]
    B = np.array([
        [n2 * dth, (-4 * n2 + n4) / dd + dph * n2, -th * delta, -2 - (1 + 2 * n2) - delta * ph],
        [(-4 * n2 + n4) / dd, -n2 * dth, -2 - (1 + 2 * n2), th * delta],
        [-2, 0, -dd, 0],
        [0, -2, 0, -dd]
    ], float)

    A = np.array([
        [-dth / 2, (1 + 2 * n2) / (2 * dd) - dph / 2, 0, 2],
        [(1 + 2 * n2) / (2 * dd), dth / 2, 2, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0]
    ], float)

    C = np.array([
        [dth / 2, -(1 + 2 * n2) / (2 * dd) + dph / 2, 0, 0],
        [-(1 + 2 * n2) / (2 * dd), -dth / 2, 0, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0]
    ], float)

    try:
        Q = -np.linalg.solve(B, A)
    except np.linalg.LinAlgError:
        return 0, np.inf

    V = Q.copy()
    lastA, lastB, lastC = A, B, C

    for j_int in range(2, N + 1):
        j = float(j_int)
        idx = j_int - 1
        dth, dph, th, ph = dtheta[idx], dphi[idx], theta[idx], phi_p[idx]

        A = np.array([
            [-dth / (2 * j), (1 + 2 * n2) / (2 * dd * (j**3)) - dph / (2 * j), 0, 1 + 1 / j],
            [(1 + 2 * n2) / (2 * dd * (j**3)), dth / (2 * j), 1 + 1 / j, 0],
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ], float)

        B = np.array([
            [n2 * dth / (j**2), (-4 * n2 + n4) / (dd * (j**4)) + dph * n2 / (j**2), -th * delta / j,
             -2 - (1 + 2 * n2) / (j**2) - delta * ph / j],
            [(-4 * n2 + n4) / (dd * (j**4)), -n2 * dth / (j**2), -2 - (1 + 2 * n2) / (j**2), th * delta / j],
            [-2, 0, -dd, 0],
            [0, -2, 0, -dd]
        ], float)

        C = np.array([
            [dth / (2 * j), -(1 + 2 * n2) / (2 * dd * (j**3)) + dph / (2 * j), 0, 1 - 1 / j],
            [-(1 + 2 * n2) / (2 * dd * (j**3)), -dth / (2 * j), 1 - 1 / j, 0],
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ], float)

        U = B + C @ Q
        V = Q
        try:
            Q = -np.linalg.solve(U, A)
        except np.linalg.LinAlgError:
            return 0, np.inf

        lastA, lastB, lastC = A, B, C

    A, B, C = lastA, lastB, lastC
    try:
        BN0 = -np.linalg.solve(A, B @ Dm) + Em
        CN0 = -np.linalg.solve(A, C @ Dm) - Dm
    except np.linalg.LinAlgError:
        return 0, np.inf

    UN = BN0 + CN0 @ V
    sign, logabs = np.linalg.slogdet(UN)
    return int(sign), float(logabs)


def build_det_grid(N):
    delta = 1.0 / N
    x = (np.arange(1, N + 1) * delta).astype(float)
    return x, delta


# ---------------- extract arrays ----------------
def arrays_shallow(sol, x_det):
    y = sol.sol(x_det)
    theta0p = y[0]
    theta0 = y[1]
    Phi0p = y[2]
    Phi0 = y[3]
    return theta0, theta0p, Phi0p, Phi0


def arrays_nepol_sin(sol, x_det):
    """
    Extract shallow-like arrays from corrected non-shallow prebuckling solution:
        theta0  = -beta*sin(phi)
        theta0' = -beta*cos(phi)*kappa_s
        Phi0    = gamma*x*T_s
        Phi0'   = gamma*T_theta
    """
    x_det = np.asarray(x_det, dtype=float)
    x_safe = np.maximum(x_det, 1.0e-12)

    y = sol.sol(x_det)
    Ts = y[0]
    Ms = y[2]
    ur = y[3]
    phi = y[5]

    r = x_safe + ur
    Ttheta = nu * Ts + ur / x_safe
    kappa_s = 12.0 * (1.0 - nu**2) * Ms * mu**2 - nu * np.sin(phi) / r

    theta0 = -beta * np.sin(phi)
    theta0p = -beta * np.cos(phi) * kappa_s
    Phi0 = gamma * x_safe * Ts
    Phi0p = gamma * Ttheta

    return theta0, theta0p, Phi0p, Phi0


# ---------------- local replacement test ----------------
def replace_on_interval(x, base, repl, x1, x2):
    """Hard replace repl on [x1,x2], else base."""
    out = base.copy()
    m = (x >= x1) & (x <= x2)
    out[m] = repl[m]
    return out


def best_p_by_minlog(p_list, logabs_list):
    j = int(np.nanargmin(logabs_list))
    return float(p_list[j]), float(logabs_list[j])

def scan_local_replacement_component(
    p_list, solsS, solsN, x_det, delta, n_wave,
    component_name, x1, x2
):
    la_hyb = np.zeros_like(p_list)

    for i in range(len(p_list)):
        thS, dthS, dPhiS, PhiS = arrays_shallow(solsS[i], x_det)
        thN, dthN, dPhiN, PhiN = arrays_nepol_sin(solsN[i], x_det)

        th_use   = thS.copy()
        dth_use  = dthS.copy()
        dPhi_use = dPhiS.copy()
        Phi_use  = PhiS.copy()

        if component_name == "Phi0p":
            dPhi_use = replace_on_interval(x_det, dPhiS, dPhiN, x1, x2)
        elif component_name == "Phi0":
            Phi_use = replace_on_interval(x_det, PhiS, PhiN, x1, x2)
        elif component_name == "theta0":
            th_use = replace_on_interval(x_det, thS, thN, x1, x2)
        elif component_name == "theta0p":
            dth_use = replace_on_interval(x_det, dthS, dthN, x1, x2)
        else:
            raise ValueError("Unknown component_name")

        _, la = det_UN_slog(th_use, dth_use, dPhi_use, Phi_use, delta, n_wave)
        la_hyb[i] = la

    return la_hyb
def scan_local_replacement_combo(
    p_list, solsS, solsN, x_det, delta, n_wave,
    components, x1, x2
):
    """
    components: iterable of names from {"Phi0p", "Phi0", "theta0", "theta0p"}
    """
    la_hyb = np.zeros_like(p_list)

    for i in range(len(p_list)):
        thS, dthS, dPhiS, PhiS = arrays_shallow(solsS[i], x_det)
        thN, dthN, dPhiN, PhiN = arrays_nepol_sin(solsN[i], x_det)

        th_use   = thS.copy()
        dth_use  = dthS.copy()
        dPhi_use = dPhiS.copy()
        Phi_use  = PhiS.copy()

        comps = set(components)

        if "Phi0p" in comps:
            dPhi_use = replace_on_interval(x_det, dPhiS, dPhiN, x1, x2)
        if "Phi0" in comps:
            Phi_use = replace_on_interval(x_det, PhiS, PhiN, x1, x2)
        if "theta0" in comps:
            th_use = replace_on_interval(x_det, thS, thN, x1, x2)
        if "theta0p" in comps:
            dth_use = replace_on_interval(x_det, dthS, dthN, x1, x2)

        _, la = det_UN_slog(th_use, dth_use, dPhi_use, Phi_use, delta, n_wave)
        la_hyb[i] = la

    return la_hyb
def main():
    # --- settings ---
    n_list = [12, 13, 14, 15]
    p_list = np.linspace(0.0, 7.0, 100)   # тот же диапазон нагружения
    q_list = p_list * 1e6

    ND_DET = 10000
    x_det, delta = build_det_grid(ND_DET)
    r0 = x_det[0]

    # ---------------- solve prebuckling only once ----------------
    solsN = []
    solsS = []

    solN_prev = None
    solS_prev = None
    xN_mesh = np.linspace(r0, 1.0, 2000)
    xS_mesh = np.linspace(r0, 1.0, 1500)
    yN_guess = np.zeros((6, xN_mesh.size))
    yS_guess = np.zeros((4, xS_mesh.size))

    for qt in q_list:
        if solN_prev is not None:
            yN_guess = solN_prev.sol(xN_mesh)

        solN = solve_one("nepol", qt, xN_mesh, yN_guess, tol=1e-4, max_nodes=150000)
        if not solN.success:
            solN = solve_one("nepol", qt, xN_mesh, yN_guess, tol=5e-4, max_nodes=150000)
        if not solN.success:
            raise RuntimeError(solN.message)

        solsN.append(solN)
        solN_prev = solN

        if solS_prev is not None:
            yS_guess = solS_prev.sol(xS_mesh)

        solS = solve_one("shallow", qt, xS_mesh, yS_guess, tol=1e-5, max_nodes=80000)
        if not solS.success:
            solS = solve_one("shallow", qt, xS_mesh, yS_guess, tol=5e-5, max_nodes=80000)
        if not solS.success:
            raise RuntimeError(solS.message)

        solsS.append(solS)
        solS_prev = solS

    # ---------------- determinant scans for n = 12,13,14,15 ----------------
    logabs_sh_all = {}
    logabs_ne_all = {}
    pmin_sh = {}
    pmin_ne = {}

    for n_wave in n_list:
        logabs_sh = np.zeros_like(p_list)
        logabs_ne = np.zeros_like(p_list)

        for i in range(len(p_list)):
            thS, dthS, dPhiS, PhiS = arrays_shallow(solsS[i], x_det)
            thN, dthN, dPhiN, PhiN = arrays_nepol_sin(solsN[i], x_det)

            _, laS = det_UN_slog(thS, dthS, dPhiS, PhiS, delta, n_wave)
            _, laN = det_UN_slog(thN, dthN, dPhiN, PhiN, delta, n_wave)

            logabs_sh[i] = laS
            logabs_ne[i] = laN

        logabs_sh_all[n_wave] = logabs_sh
        logabs_ne_all[n_wave] = logabs_ne

        j_sh = int(np.nanargmin(logabs_sh))
        j_ne = int(np.nanargmin(logabs_ne))

        pmin_sh[n_wave] = p_list[j_sh]
        pmin_ne[n_wave] = p_list[j_ne]

        print(
            f"n={n_wave}: "
            f"shallow  p_min≈{p_list[j_sh]:.3f} MPa, log|det|≈{logabs_sh[j_sh]:.6e}; "
            f"nepol    p_min≈{p_list[j_ne]:.3f} MPa, log|det|≈{logabs_ne[j_ne]:.6e}"
        )

    # ---------------- plot 1: shallow, all n ----------------
    plt.figure(figsize=(9, 6))
    for n_wave in n_list:
        plt.plot(p_list, logabs_sh_all[n_wave], label=f"shallow, n={n_wave}")
        j = int(np.nanargmin(logabs_sh_all[n_wave]))
        plt.plot(p_list[j], logabs_sh_all[n_wave][j], "o")

    plt.grid(True)
    plt.xlabel("p, MPa")
    plt.ylabel("log|det U_N|")
    plt.title("Determinant scan: shallow model, n = 12,13,14,15")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ---------------- plot 2: non-shallow, all n ----------------
    plt.figure(figsize=(9, 6))
    for n_wave in n_list:
        plt.plot(p_list, logabs_ne_all[n_wave], label=f"non-shallow, n={n_wave}")
        j = int(np.nanargmin(logabs_ne_all[n_wave]))
        plt.plot(p_list[j], logabs_ne_all[n_wave][j], "o")

    plt.grid(True)
    plt.xlabel("p, MPa")
    plt.ylabel("log|det U_N|")
    plt.title("Determinant scan: non-shallow model, n = 12,13,14,15")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ---------------- plot 3: shallow vs non-shallow for each n ----------------
    fig, axes = plt.subplots(2, 2, figsize=(12, 9), sharex=True, sharey=True)
    axes = axes.ravel()

    for ax, n_wave in zip(axes, n_list):
        ax.plot(p_list, logabs_sh_all[n_wave], label="shallow")
        ax.plot(p_list, logabs_ne_all[n_wave], label="non-shallow")

        j_sh = int(np.nanargmin(logabs_sh_all[n_wave]))
        j_ne = int(np.nanargmin(logabs_ne_all[n_wave]))

        ax.plot(p_list[j_sh], logabs_sh_all[n_wave][j_sh], "o")
        ax.plot(p_list[j_ne], logabs_ne_all[n_wave][j_ne], "o")

        ax.axvline(p_list[j_sh], linestyle="--", linewidth=1)
        ax.axvline(p_list[j_ne], linestyle="--", linewidth=1)

        ax.set_title(f"n = {n_wave}")
        ax.grid(True)

    axes[0].legend()
    fig.supxlabel("p, MPa")
    fig.supylabel("log|det U_N|")
    fig.suptitle("Comparison of determinant scans: shallow vs non-shallow")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()