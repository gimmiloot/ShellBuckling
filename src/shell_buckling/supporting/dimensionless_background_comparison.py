# -*- coding: utf-8 -*-
"""
ПРОГРАММА ДЛЯ СРАВНЕНИЯ БЕЗРАЗМЕРНЫХ ФУНКЦИЙ
theta0, theta0', Phi0, Phi0'

Две осесимметричные предкритические системы:
1) Непологая (новая): y = [T_s, T_sn, M_s, u_r, u_z, phi]
   Обезразмеривание:
     T_s = T_s_dim/(E h),  u_r = u_r_dim/a,  u_z = u_z_dim/h,  qbar = q_dim*a/(E h)

   Исправленная геометрия пластины:
     r = x + u_r
     lambda_theta = r/x = 1 + u_r/x
     e_theta = u_r/x
     T_theta = nu*T_s + u_r/x

   Связь с функциями из пологой системы:
     Phi0(x)   = gamma * x * T_s
     Phi0'(x)  = gamma * T_theta
     theta0(x) = -beta * sin(phi)
     theta0'(x)= -beta * cos(phi) * kappa_s,
                 kappa_s = phi' = 12(1-nu^2) M_s mu^2 - nu*sin(phi)/r

   Дополнительные диагностики branch-A:
     J_branchA(x) = r - x - (x*Phi0' - nu*Phi0)/gamma
     K_branchA(x) = gamma + (1-nu)*Phi0' + x*Phi0''
                    - (gamma + Phi0/x - nu*Phi0')*cos(phi)

2) Пологая (Bauer-like): y = [theta0', theta0, Phi0', Phi0]

Сравнение строится по общей сетке x ∈ (0,1].

Решение: solve_bvp + continuation по q: 0 -> q_target (Па).
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_bvp

# -------------------- параметры --------------------
nu = 0.3
Ee = 205e9
h = 0.005
a = 0.5

mu = a / h
beta = np.sqrt(12.0 * (1.0 - nu**2)) * mu
gamma = 12.0 * (1.0 - nu**2) * mu**2

q = 0.0  # Pa, глобально


# -------------------- НЕПОЛОГАЯ система --------------------
def axisym_nepol(x, y):
    """
    y = [T_s, T_sn, M_s, u_r, u_z, phi] — безразмерные

    Исправленная геометрия пластины:
        r = x + u_r
        e_theta = u_r / x
        qbar = q*a/(E h)
    """
    x_safe = np.maximum(np.asarray(x, dtype=float), 1.0e-12)

    Ts = y[0]
    Tsn = y[1]
    Ms = y[2]
    ur = y[3]
    uz = y[4]
    phi = y[5]

    # Исправленный безразмерный деформированный радиус
    r = x_safe + ur

    # Окружная деформация и окружное усилие
    etheta = ur / x_safe
    es = Ts * (1.0 - nu**2) - nu * etheta
    Ttheta = nu * Ts + etheta

    # Кривизна и окружной момент
    kappa_s = 12.0 * (1.0 - nu**2) * Ms * mu**2 - nu * (np.sin(phi) / r)
    Mtheta = nu * Ms + (np.sin(phi) / (12.0 * mu**2 * r))

    qbar = q * a / (Ee * h)

    return np.vstack((
        # T_s'
        -(1.0 / r) * Ts + (np.cos(phi) / r) * Ttheta - kappa_s * Tsn,
        # T_sn'
        -(1.0 / r) * Tsn + (np.sin(phi) / r) * Ttheta + kappa_s * Ts - qbar,
        # M_s'
        -(1.0 / r) * Ms + (np.cos(phi) / r) * Mtheta + Tsn,
        # u_r'
        (es + 1.0) * np.cos(phi) - 1.0,
        # u_z'
        -mu * (1.0 + es) * np.sin(phi),
        # phi'
        kappa_s
    ))


def bcNP(ya, yb):
    """
    BC:
      Ts(1)=0,
      Tsn(x0)=0,
      ur(x0)=0,
      uz(1)=0,
      phi(x0)=0,
      phi(1)=0
    """
    return np.array([yb[0], ya[1], ya[3], yb[4], ya[5], yb[5]], dtype=float)


# -------------------- ПОЛОГАЯ система --------------------
def fun_shallow(x, y):
    # y = [theta0', theta0, Phi0', Phi0]
    x_safe = np.maximum(np.asarray(x, dtype=float), 1.0e-12)
    return np.vstack((
        -y[0] / x_safe + y[1] / x_safe**2 + y[3] * (y[1] / x_safe) + q * x_safe / 2.0 * beta**3 * mu / Ee,
        y[0],
        -y[2] / x_safe + y[3] / x_safe**2 - y[1] * (y[1] / (2.0 * x_safe)),
        y[2]
    ))


def bc_shallow(ya, yb):
    return np.array([ya[1], yb[1], ya[3], yb[3]], dtype=float)


# -------------------- continuation solve_bvp --------------------
def solve_bvp_continuation(system: str,
                           q_target: float,
                           n_steps: int,
                           nd: int,
                           tol: float,
                           max_nodes: int):
    global q
    q_list = np.linspace(0.0, float(q_target), n_steps)

    sp = 1.0 / nd
    x = np.linspace(sp, 1.0, nd)

    ny = 6 if system == "nepol" else 4
    y_guess = np.zeros((ny, x.size), dtype=float)

    sol_prev = None
    for qk in q_list:
        q = float(qk)
        if sol_prev is not None:
            y_guess = sol_prev.sol(x)

        if system == "nepol":
            sol = solve_bvp(axisym_nepol, bcNP, x, y_guess,
                            tol=tol, max_nodes=max_nodes, verbose=0)
        else:
            sol = solve_bvp(fun_shallow, bc_shallow, x, y_guess,
                            tol=tol, max_nodes=max_nodes, verbose=0)

        if not sol.success:
            tol2 = min(5e-4, 5 * tol)
            if system == "nepol":
                sol = solve_bvp(axisym_nepol, bcNP, x, y_guess,
                                tol=tol2, max_nodes=max_nodes, verbose=0)
            else:
                sol = solve_bvp(fun_shallow, bc_shallow, x, y_guess,
                                tol=tol2, max_nodes=max_nodes, verbose=0)

        if not sol.success:
            raise RuntimeError(f"[{system}] fail at q={qk:.3e} Pa: {sol.message}")

        sol_prev = sol

    return sol_prev


# -------------------- branch-A diagnostics --------------------
def compute_branchA_diagnostics(x, Ts, Tsn, Ms, ur, phi):
    """
    Возвращает словарь с background-каналами и branch-A diagnostics.
    Все массивы считаются на одной и той же сетке x.
    """
    x_safe = np.maximum(np.asarray(x, dtype=float), 1.0e-12)

    r = x_safe + ur
    etheta = ur / x_safe
    es = Ts * (1.0 - nu**2) - nu * etheta
    Ttheta = nu * Ts + etheta

    sinphi = np.sin(phi)
    cosphi = np.cos(phi)

    kappa_s = 12.0 * (1.0 - nu**2) * Ms * mu**2 - nu * (sinphi / r)
    Mtheta = nu * Ms + sinphi / (12.0 * mu**2 * r)

    # Аналоги shallow background channels
    Phi0 = gamma * x_safe * Ts
    Phi0p = gamma * Ttheta
    theta0 = -beta * sinphi
    theta0p = -beta * cosphi * kappa_s

    # Производные, вычисленные аналитически через exact shell-system
    Ts_p = -(1.0 / r) * Ts + (cosphi / r) * Ttheta - kappa_s * Tsn
    ur_p = (es + 1.0) * cosphi - 1.0
    Ttheta_p = nu * Ts_p + ur_p / x_safe - ur / (x_safe**2)
    Phi0pp = gamma * Ttheta_p

    # Branch-A diagnostics
    J_branchA = r - x_safe - (x_safe * Phi0p - nu * Phi0) / gamma
    K_branchA = (
        gamma
        + (1.0 - nu) * Phi0p
        + x_safe * Phi0pp
        - (gamma + Phi0 / x_safe - nu * Phi0p) * cosphi
    )

    return {
        "r": r,
        "es": es,
        "Ttheta": Ttheta,
        "kappa_s": kappa_s,
        "Mtheta": Mtheta,
        "Phi0": Phi0,
        "Phi0p": Phi0p,
        "Phi0pp": Phi0pp,
        "theta0": theta0,
        "theta0p": theta0p,
        "J_branchA": J_branchA,
        "K_branchA": K_branchA,
    }


# -------------------- сравнение безразмерных функций --------------------
def compare_dimensionless(q_target: float, n_plot: int = 4000, make_branchA_plots: bool = True):
    # Решаем обе задачи
    solN = solve_bvp_continuation("nepol", q_target, n_steps=20, nd=2000, tol=1e-4, max_nodes=150000)
    solS = solve_bvp_continuation("shallow", q_target, n_steps=10, nd=1500, tol=1e-5, max_nodes=80000)

    x = np.linspace(1.0 / n_plot, 1.0, n_plot)

    # --- непологие ---
    yN = solN.sol(x)
    Ts = yN[0]
    Tsn = yN[1]
    Ms = yN[2]
    ur = yN[3]
    phi = yN[5]

    diag = compute_branchA_diagnostics(x, Ts, Tsn, Ms, ur, phi)
    r = diag["r"]
    Phi0_N = diag["Phi0"]
    Phi0p_N = diag["Phi0p"]
    theta0_N = diag["theta0"]
    theta0p_N = diag["theta0p"]
    J_branchA = diag["J_branchA"]
    K_branchA = diag["K_branchA"]

    # --- пологие ---
    yS = solS.sol(x)
    theta0p_S = yS[0]
    theta0_S = yS[1]
    Phi0p_S = yS[2]
    Phi0_S = yS[3]

    title = f"q = {q_target / 1e6:.3f} MPa"

    # theta0
    plt.figure()
    plt.plot(x, theta0_S, label="пологая θ0")
    plt.plot(x, theta0_N, "--", label="непологая θ0 = -β sin(φ)")
    plt.grid(True)
    plt.xlabel("x = r/a")
    plt.ylabel("θ0 (безразм.)")
    plt.title("θ0(x) — " + title)
    plt.legend()
    plt.show()

    # theta0'
    plt.figure()
    plt.plot(x, theta0p_S, label="пологая θ0'")
    plt.plot(x, theta0p_N, "--", label="непологая θ0' = -β cos(φ) κ_s")
    plt.grid(True)
    plt.xlabel("x = r/a")
    plt.ylabel("θ0' (безразм.)")
    plt.title("θ0'(x) — " + title)
    plt.legend()
    plt.show()

    # Phi0
    plt.figure()
    plt.plot(x, Phi0_S, label="пологая Φ0")
    plt.plot(x, Phi0_N, "--", label="непологая Φ0 = γ x Ts")
    plt.grid(True)
    plt.xlabel("x = r/a")
    plt.ylabel("Φ0 (безразм.)")
    plt.title("Φ0(x) — " + title)
    plt.legend()
    plt.show()

    # Phi0'
    plt.figure()
    plt.plot(x, Phi0p_S, label="пологая Φ0'")
    plt.plot(x, Phi0p_N, "--", label="непологая Φ0' = γ Tθ")
    plt.grid(True)
    plt.xlabel("x = r/a")
    plt.ylabel("Φ0' (безразм.)")
    plt.title("Φ0'(x) — " + title)
    plt.legend()
    plt.show()

    if make_branchA_plots:
        # J_branchA
        plt.figure()
        plt.plot(x, J_branchA, label="J_branchA")
        plt.grid(True)
        plt.xlabel("x = r/a")
        plt.ylabel("J_branchA")
        plt.title("J_branchA(x) — " + title)
        plt.legend()
        plt.show()

        # K_branchA
        plt.figure()
        plt.plot(x, K_branchA, label="K_branchA")
        plt.grid(True)
        plt.xlabel("x = r/a")
        plt.ylabel("K_branchA")
        plt.title("K_branchA(x) — " + title)
        plt.legend()
        plt.show()

    # Быстрые диагностические масштабы
    print("\nDiagnostics (max abs):")
    print("  max|phi|         =", float(np.max(np.abs(phi))))
    print("  min(r)           =", float(np.min(r)))
    print("  max|θ0_sh|       =", float(np.max(np.abs(theta0_S))))
    print("  max|θ0_new|      =", float(np.max(np.abs(theta0_N))))
    print("  max|Φ0_sh|       =", float(np.max(np.abs(Phi0_S))))
    print("  max|Φ0_new|      =", float(np.max(np.abs(Phi0_N))))
    print("  max|Φ0p_sh|      =", float(np.max(np.abs(Phi0p_S))))
    print("  max|Φ0p_new|     =", float(np.max(np.abs(Phi0p_N))))
    print("  max|J_branchA|   =", float(np.max(np.abs(J_branchA))))
    print("  max|K_branchA|   =", float(np.max(np.abs(K_branchA))))

    return {
        "x": x,
        "sol_nonshallow": solN,
        "sol_shallow": solS,
        "theta0_nonshallow": theta0_N,
        "theta0p_nonshallow": theta0p_N,
        "Phi0_nonshallow": Phi0_N,
        "Phi0p_nonshallow": Phi0p_N,
        "theta0_shallow": theta0_S,
        "theta0p_shallow": theta0p_S,
        "Phi0_shallow": Phi0_S,
        "Phi0p_shallow": Phi0p_S,
        "J_branchA": J_branchA,
        "K_branchA": K_branchA,
    }


if __name__ == "__main__":
    q_target = 6.0e6  # Па
    compare_dimensionless(q_target)
