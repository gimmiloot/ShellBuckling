# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_bvp

from shell_buckling.mixed_weak.axisymmetric_simple_support_background import (
    AxisymmetricBackgroundSolve,
    AxisymmetricSimpleSupportConfig,
    BC_LABELS as SIMPLE_SUPPORT_BC_LABELS,
    STATE_LABELS as SIMPLE_SUPPORT_STATE_LABELS,
    build_template_solution,
    default_x_mesh,
    solve_axisymmetric_simple_support_fixed_load,
)


# ---------------- parameters ----------------
nu = 0.3
Ee = 205e9
h = 0.005
a = 0.5
mu = a / h
beta = np.sqrt(12.0 * (1.0 - nu**2)) * mu
gamma = 12.0 * (1.0 - nu**2) * mu**2

q = 0.0  # global Pa

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "output" / "supporting_simple_support_determinant_comparison"


# ---------------- SHALLOW SIMPLE SUPPORT ----------------
def fun_shallow(x, y):
    x = np.asarray(x, dtype=float)
    x_safe = np.maximum(x, 1.0e-12)
    return np.vstack(
        (
            -y[0] / x_safe + y[1] / x_safe**2 + y[3] * (y[1] / x_safe) + q * x_safe / 2.0 * beta**3 * mu / Ee,
            y[0],
            -y[2] / x_safe + y[3] / x_safe**2 - y[1] * (y[1] / (2.0 * x_safe)),
            y[2],
        )
    )


def bc_sh(ya, yb):
    return np.array([ya[1], yb[0] + nu * yb[1], ya[3], yb[3]], float)


def solve_shallow_one(q_pa, x_mesh, y_guess, tol, max_nodes):
    global q
    q = float(q_pa)
    return solve_bvp(fun_shallow, bc_sh, x_mesh, y_guess, tol=tol, max_nodes=max_nodes, verbose=0)


def solve_shallow_schedule(p_list, x_mesh):
    sols = []
    y_guess = np.zeros((4, x_mesh.size))
    sol_prev = None

    for p_mpa in p_list:
        if sol_prev is not None:
            y_guess = sol_prev.sol(x_mesh)

        sol = solve_shallow_one(p_mpa * 1.0e6, x_mesh, y_guess, tol=1.0e-5, max_nodes=80000)
        if not sol.success:
            sol = solve_shallow_one(p_mpa * 1.0e6, x_mesh, y_guess, tol=5.0e-5, max_nodes=80000)
        if not sol.success:
            raise RuntimeError(f"shallow simple-support solve failed at p={p_mpa:.3f} MPa: {sol.message}")

        sols.append(sol)
        sol_prev = sol

    return sols


# ---------------- det(U_N) via slogdet ----------------
def det_UN_slog(theta, dtheta, dphi, phi_p, delta, n):
    theta = np.asarray(theta, float)
    dtheta = np.asarray(dtheta, float)
    dphi = np.asarray(dphi, float)
    phi_p = np.asarray(phi_p, float)

    N = len(theta)
    n2 = n * n
    n4 = n2 * n2
    dd = delta * delta

    Dm = np.array(
        [
            [1 / (2 * delta), 0, 0, 0],
            [1 / (2 * delta), 0, 0, 0],
            [0, 1 / (2 * delta), 0, 0],
            [0, 0, 0, 0],
        ],
        float,
    )

    Em = np.array(
        [
            [-n2, 0, 0, 0],
            [-1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 1, 0, 0],
        ],
        float,
    )

    dth, dph, th, ph = dtheta[0], dphi[0], theta[0], phi_p[0]
    B = np.array(
        [
            [n2 * dth, (-4 * n2 + n4) / dd + dph * n2, -th * delta, -2 - (1 + 2 * n2) - delta * ph],
            [(-4 * n2 + n4) / dd, -n2 * dth, -2 - (1 + 2 * n2), th * delta],
            [-2, 0, -dd, 0],
            [0, -2, 0, -dd],
        ],
        float,
    )

    A = np.array(
        [
            [-dth / 2, (1 + 2 * n2) / (2 * dd) - dph / 2, 0, 2],
            [(1 + 2 * n2) / (2 * dd), dth / 2, 2, 0],
            [1, 0, 0, 0],
            [0, 1, 0, 0],
        ],
        float,
    )

    C = np.array(
        [
            [dth / 2, -(1 + 2 * n2) / (2 * dd) + dph / 2, 0, 0],
            [-(1 + 2 * n2) / (2 * dd), -dth / 2, 0, 0],
            [1, 0, 0, 0],
            [0, 1, 0, 0],
        ],
        float,
    )

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

        A = np.array(
            [
                [-dth / (2 * j), (1 + 2 * n2) / (2 * dd * (j**3)) - dph / (2 * j), 0, 1 + 1 / j],
                [(1 + 2 * n2) / (2 * dd * (j**3)), dth / (2 * j), 1 + 1 / j, 0],
                [1, 0, 0, 0],
                [0, 1, 0, 0],
            ],
            float,
        )

        B = np.array(
            [
                [
                    n2 * dth / (j**2),
                    (-4 * n2 + n4) / (dd * (j**4)) + dph * n2 / (j**2),
                    -th * delta / j,
                    -2 - (1 + 2 * n2) / (j**2) - delta * ph / j,
                ],
                [(-4 * n2 + n4) / (dd * (j**4)), -n2 * dth / (j**2), -2 - (1 + 2 * n2) / (j**2), th * delta / j],
                [-2, 0, -dd, 0],
                [0, -2, 0, -dd],
            ],
            float,
        )

        C = np.array(
            [
                [dth / (2 * j), -(1 + 2 * n2) / (2 * dd * (j**3)) + dph / (2 * j), 0, 1 - 1 / j],
                [-(1 + 2 * n2) / (2 * dd * (j**3)), -dth / (2 * j), 1 - 1 / j, 0],
                [1, 0, 0, 0],
                [0, 1, 0, 0],
            ],
            float,
        )

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


def arrays_shallow(sol, x_det):
    y = sol.sol(x_det)
    theta0p = y[0]
    theta0 = y[1]
    Phi0p = y[2]
    Phi0 = y[3]
    return theta0, theta0p, Phi0p, Phi0


def arrays_simple_support_background(result: AxisymmetricBackgroundSolve, x_det):
    """
    Minimal adapter layer from the full-state simple-support background solver to
    the shallow-style arrays expected by the legacy determinant criterion.
    """
    if result.solution is None:
        raise ValueError("Simple-support background result has no converged solution.")

    x_det = np.asarray(x_det, dtype=float)
    x_safe = np.maximum(x_det, 1.0e-12)

    y = result.solution.sol(x_det)
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


def best_p_by_minlog(p_list, logabs_list):
    logabs_arr = np.asarray(logabs_list, dtype=float)
    finite = np.isfinite(logabs_arr)
    if not np.any(finite):
        return float("nan"), float("nan"), None
    masked = np.where(finite, logabs_arr, np.inf)
    j = int(np.argmin(masked))
    return float(p_list[j]), float(logabs_arr[j]), j


def solve_simple_support_background_schedule(p_list, x0):
    config = AxisymmetricSimpleSupportConfig(
        x0=float(x0),
        nd_bvp=600,
        tol=1.0e-4,
        relaxed_tol=5.0e-4,
        max_nodes=150000,
        template_q_mpa=0.5,
    )
    x_mesh = default_x_mesh(config)
    template_result = build_template_solution(config)

    results: list[AxisymmetricBackgroundSolve] = []
    previous_success: AxisymmetricBackgroundSolve | None = None

    for p_mpa in p_list:
        result: AxisymmetricBackgroundSolve | None = None
        if previous_success is not None and previous_success.solution is not None:
            previous_guess = previous_success.solution.sol(x_mesh)
            result = solve_axisymmetric_simple_support_fixed_load(
                p_mpa,
                config=config,
                initial_guess=previous_guess,
            )

        if result is None or not result.success:
            result = solve_axisymmetric_simple_support_fixed_load(
                p_mpa,
                config=config,
                template_result=template_result,
            )

        results.append(result)
        if result.success:
            previous_success = result

    return results, config


def save_figure(fig, filename):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


def main():
    # --- settings ---
    n_list = [12, 13, 14, 15]
    p_list = np.linspace(0.0, 7.0, 100)

    ND_DET = 10000
    x_det, delta = build_det_grid(ND_DET)
    r0 = x_det[0]

    # ---------------- solve prebuckling only once ----------------
    xS_mesh = np.linspace(r0, 1.0, 1500)
    solsS = solve_shallow_schedule(p_list, xS_mesh)
    solsN, bg_config = solve_simple_support_background_schedule(p_list, r0)

    success_loads = [result.q_mpa for result in solsN if result.success]
    last_success = success_loads[-1] if success_loads else float("nan")
    first_failure = next((result.q_mpa for result in solsN if not result.success), float("nan"))

    print("=== Supporting determinant comparison: simple support ===")
    print("non-shallow background source: shell_buckling.mixed_weak.axisymmetric_simple_support_background")
    print(f"state: {list(SIMPLE_SUPPORT_STATE_LABELS)}")
    print(f"BCs:   {list(SIMPLE_SUPPORT_BC_LABELS)}")
    print(
        "background config: "
        f"x0={bg_config.x0:.6f}, nd_bvp={bg_config.nd_bvp}, tol={bg_config.tol:.1e}, "
        f"relaxed_tol={bg_config.relaxed_tol:.1e}, max_nodes={bg_config.max_nodes}"
    )
    print(f"pressure range: {p_list[0]:.3f}..{p_list[-1]:.3f} MPa with {len(p_list)} points")
    print(f"n list: {n_list}")
    print(f"simple-support background last_success={last_success:.3f} MPa; first_failure={first_failure:.3f} MPa")
    print()

    # ---------------- determinant scans for n = 12,13,14,15 ----------------
    logabs_sh_all = {}
    logabs_ne_all = {}

    for n_wave in n_list:
        logabs_sh = np.zeros_like(p_list)
        logabs_ne = np.full_like(p_list, np.nan)

        for i in range(len(p_list)):
            thS, dthS, dPhiS, PhiS = arrays_shallow(solsS[i], x_det)
            _, laS = det_UN_slog(thS, dthS, dPhiS, PhiS, delta, n_wave)
            logabs_sh[i] = laS

            if solsN[i].success and solsN[i].solution is not None:
                thN, dthN, dPhiN, PhiN = arrays_simple_support_background(solsN[i], x_det)
                _, laN = det_UN_slog(thN, dthN, dPhiN, PhiN, delta, n_wave)
                logabs_ne[i] = laN

        logabs_sh_all[n_wave] = logabs_sh
        logabs_ne_all[n_wave] = logabs_ne

        p_sh, la_sh, _ = best_p_by_minlog(p_list, logabs_sh)
        p_ne, la_ne, j_ne = best_p_by_minlog(p_list, logabs_ne)

        ne_text = (
            f"simple_support p_min~={p_ne:.3f} MPa, log|det|~={la_ne:.6e}"
            if j_ne is not None
            else "simple_support no finite determinant values"
        )
        print(
            f"n={n_wave}: "
            f"shallow p_min~={p_sh:.3f} MPa, log|det|~={la_sh:.6e}; "
            f"{ne_text}"
        )

    print()

    # ---------------- plot 1: shallow, all n ----------------
    fig1 = plt.figure(figsize=(9, 6))
    for n_wave in n_list:
        plt.plot(p_list, logabs_sh_all[n_wave], label=f"shallow, n={n_wave}")
        _, _, j = best_p_by_minlog(p_list, logabs_sh_all[n_wave])
        if j is not None:
            plt.plot(p_list[j], logabs_sh_all[n_wave][j], "o")

    plt.grid(True)
    plt.xlabel("p, MPa")
    plt.ylabel("log|det U_N|")
    plt.title("Determinant scan: shallow simple-support model, n = 12,13,14,15")
    plt.legend()
    plt.tight_layout()
    fig1_path = save_figure(fig1, "determinant_scan_shallow_simple_support.png")

    # ---------------- plot 2: non-shallow, all n ----------------
    fig2 = plt.figure(figsize=(9, 6))
    for n_wave in n_list:
        plt.plot(p_list, logabs_ne_all[n_wave], label=f"non-shallow simple-support, n={n_wave}")
        _, _, j = best_p_by_minlog(p_list, logabs_ne_all[n_wave])
        if j is not None:
            plt.plot(p_list[j], logabs_ne_all[n_wave][j], "o")

    plt.grid(True)
    plt.xlabel("p, MPa")
    plt.ylabel("log|det U_N|")
    plt.title("Determinant scan: non-shallow simple-support background, n = 12,13,14,15")
    plt.legend()
    plt.tight_layout()
    fig2_path = save_figure(fig2, "determinant_scan_non_shallow_simple_support.png")

    # ---------------- plot 3: shallow vs non-shallow for each n ----------------
    fig3, axes = plt.subplots(2, 2, figsize=(12, 9), sharex=True, sharey=True)
    axes = axes.ravel()

    for ax, n_wave in zip(axes, n_list):
        ax.plot(p_list, logabs_sh_all[n_wave], label="shallow")
        ax.plot(p_list, logabs_ne_all[n_wave], label="non-shallow simple-support")

        _, _, j_sh = best_p_by_minlog(p_list, logabs_sh_all[n_wave])
        _, _, j_ne = best_p_by_minlog(p_list, logabs_ne_all[n_wave])

        if j_sh is not None:
            ax.plot(p_list[j_sh], logabs_sh_all[n_wave][j_sh], "o")
            ax.axvline(p_list[j_sh], linestyle="--", linewidth=1)
        if j_ne is not None:
            ax.plot(p_list[j_ne], logabs_ne_all[n_wave][j_ne], "o")
            ax.axvline(p_list[j_ne], linestyle="--", linewidth=1)

        ax.set_title(f"n = {n_wave}")
        ax.grid(True)

    axes[0].legend()
    fig3.supxlabel("p, MPa")
    fig3.supylabel("log|det U_N|")
    fig3.suptitle("Comparison of determinant scans: shallow vs non-shallow simple support")
    plt.tight_layout()
    fig3_path = save_figure(fig3, "determinant_scan_comparison_simple_support.png")

    print("saved figures:")
    print(f"  {fig1_path}")
    print(f"  {fig2_path}")
    print(f"  {fig3_path}")


if __name__ == "__main__":
    main()
