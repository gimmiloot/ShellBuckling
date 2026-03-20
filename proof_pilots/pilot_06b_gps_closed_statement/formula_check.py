from __future__ import annotations

from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / "proof_pilots" / "pilot_06b_gps_closed_statement" / "gps_closed_statement.md"
SIMPLE_CORE = ROOT / "src" / "shell_buckling" / "mixed_weak" / "solver_simple_support_core.py"
PATCHED_CORE = ROOT / "src" / "shell_buckling" / "mixed_weak" / "solver_patched_core.py"


CONSOLIDATED_STATEMENT = """G_ps,n^repo(X, Xhat; q)
  := int_[x0,1] [ hat(T_s) * g_s^repo(X; q)
                + hat(Q_s) * g_n^repo(X; q)
                + hat(M_s) * g_m^repo(X; q) ] dx"""


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def print_check(label: str, ok: bool, detail: str) -> None:
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")
    print(f"  {detail}")


def separately_linear(expr: sp.Expr, vars_: list[sp.Symbol]) -> bool:
    zero_subs = {var: 0 for var in vars_}
    at_zero = sp.simplify(expr.subs(zero_subs)) == 0
    second_derivatives = all(
        sp.simplify(sp.diff(expr, a, b)) == 0 for a in vars_ for b in vars_
    )
    return bool(at_zero and second_derivatives)


def main() -> int:
    print("Pilot 06b: closed repository-level statement of G_ps")
    print()
    print("Expected result:")
    print("  the compact written G_ps statement should match the active code-level forcing block,")
    print("  remain bilinear in the intended mixed trial/test slots,")
    print("  and still only support V-S1 at a repository-level partial status.")
    print()

    note_text = load_text(NOTE)
    simple_text = load_text(SIMPLE_CORE)
    patched_text = load_text(PATCHED_CORE)

    required_note_snippets = [
        "G_ps,n^repo(X, Xhat; q)",
        "hat(T_s) * g_s^repo(X; q)",
        "hat(Q_s) * g_n^repo(X; q)",
        "hat(M_s) * g_m^repo(X; q)",
        "e_s^code(X)   = T_s - nu T_theta(X)",
        "T_sn^0 = Q_0",
        "it is still a repository-level consolidation",
    ]
    note_ok = all(snippet in note_text for snippet in required_note_snippets)

    core_ok = all(
        [
            'g_s = -(b["T_theta"] / r0) * r_x - b["T_sn"] * phi_x' in simple_text,
            'g_n = b["T_s"] * phi_x + (c0 / x_safe) * b["T_theta"] * phi' in simple_text,
            '- (b["q"] / x_safe) * (r0 * e_s + lam_s0 * r)' in simple_text,
            'R_Ts = Ts_x + a0 * Ts - (c0 / x_safe) * Ttheta + (n / x_safe) * S - kap_s0 * Qs - (s0 * c0 / (r0 * r0)) * Mtheta - g_s' in simple_text,
            'R_Qs = Qs_x + a0 * Qs - kap_s0 * Ts + (s0 / x_safe) * Ttheta - (s0 * s0 / (r0 * r0)) * Mtheta + b_m * chi - g_n' in simple_text,
            'R_Ms = Ms_x + a0 * Ms - a0 * Mtheta - Qs + (n / x_safe) * H - (b["M_theta"] / r0) * r_x' in simple_text,
            'T_sn=Q0' in simple_text,
            'g_s = -(b["T_theta"] / r0) * r_x - b["T_sn"] * phi_x' in patched_text,
            'g_n = b["T_s"] * phi_x + (c0 / x_safe) * b["T_theta"] * phi' in patched_text,
            '- (b["q"] / x_safe) * (r0 * e_s + lam_s0 * r)' in patched_text,
        ]
    )

    print("Exact consolidated statement being checked:")
    print(CONSOLIDATED_STATEMENT)
    print()
    print("Exact formulas used from the active code:")
    print('  g_s = -(T_theta^0 / r_0) * r_x - T_sn^0 * varphi\'')
    print('  g_n =  T_s^0 * varphi\' + (c_0 / x) * T_theta^0 * varphi - (q^0 / x) * (r_0 * e_s^code + lambda_s0 * r)')
    print('  g_m =  (M_theta^0 / r_0) * r_x')
    print()

    print("A. Written-statement guard")
    print_check(
        "gps_closed_statement.md contains the intended closed repository-level formula",
        note_ok,
        "expected: the note states the hat(T_s)/hat(Q_s)/hat(M_s) pairing, e_s^code, and the T_sn^0 = Q_0 identification",
    )
    print_check(
        "active code still contains the matching forcing and residual formulas",
        core_ok,
        "expected: both active cores match the consolidated statement's g_s, g_n, g_m structure",
    )
    print()

    x, n, nu = sp.symbols("x n nu", nonzero=True)
    c0, s0, kappa_s0, lambda_s0, r0 = sp.symbols("c0 s0 kappa_s0 lambda_s0 r0", nonzero=True)
    T_theta0, T_sn0, T_s0, M_theta0, q0 = sp.symbols("T_theta0 T_sn0 T_s0 M_theta0 q0")
    u_s, u_n, v, varphi = sp.symbols("u_s u_n v varphi")
    u_s_x, u_n_x, varphi_x = sp.symbols("u_s_x u_n_x varphi_x")
    T_s = sp.symbols("T_s")
    hat_T_s, hat_Q_s, hat_M_s = sp.symbols("hat_T_s hat_Q_s hat_M_s")

    r = c0 * u_s + s0 * u_n
    r_x = -kappa_s0 * s0 * u_s + c0 * u_s_x + kappa_s0 * c0 * u_n + s0 * u_n_x
    T_theta = sp.expand(nu * T_s + r / x + (n / x) * v)
    e_s_code = sp.expand(T_s - nu * T_theta)

    g_s_repo = sp.expand(-(T_theta0 / r0) * r_x - T_sn0 * varphi_x)
    g_n_repo = sp.expand(T_s0 * varphi_x + (c0 / x) * T_theta0 * varphi - (q0 / x) * (r0 * e_s_code + lambda_s0 * r))
    g_m_repo = sp.expand((M_theta0 / r0) * r_x)
    G_repo = sp.expand(hat_T_s * g_s_repo + hat_Q_s * g_n_repo + hat_M_s * g_m_repo)

    print("B. Structural properties of the consolidated statement")
    trial_vars = [u_s, u_s_x, u_n, u_n_x, v, varphi, varphi_x, T_s]
    test_vars = [hat_T_s, hat_Q_s, hat_M_s]

    trial_linearity_ok = all(separately_linear(expr, trial_vars) for expr in [g_s_repo, g_n_repo, g_m_repo])
    test_linearity_ok = separately_linear(G_repo, test_vars)
    mixed_slot_ok = all(sp.simplify(sp.diff(G_repo, var)) != 0 for var in test_vars)
    not_u_only_ok = sp.simplify(sp.diff(G_repo, T_s)) != 0

    print_check(
        "trial-side linearity in the intended slots",
        trial_linearity_ok,
        "expected: g_s^repo, g_n^repo, g_m^repo are linear in u_s, u_n, v, varphi, T_s and their active derivatives",
    )
    print_check(
        "test-side linearity in the intended slots",
        test_linearity_ok,
        "expected: the paired repository-level block is linear in hat(T_s), hat(Q_s), hat(M_s)",
    )
    print_check(
        "explicit mixed-slot dependence",
        mixed_slot_ok,
        "expected: G_ps,n^repo depends on all three mixed test slots rather than on one collapsed scalar slot",
    )
    print_check(
        "non-reduction to U-only scalar closure at the repository level",
        not_u_only_ok,
        f"actual symbolic derivative d(G_repo)/dT_s = {sp.simplify(sp.diff(G_repo, T_s))}",
    )
    print()

    print("C. Final explicit conclusion")
    final_ok = all([note_ok, core_ok, trial_linearity_ok, test_linearity_ok, mixed_slot_ok, not_u_only_ok])
    print("Actual result:")
    print(f"  PASS/FAIL = {'PASS' if final_ok else 'FAIL'}")
    print(
        "  Support level = "
        + ("STILL PARTIAL" if final_ok else "NO CONSISTENT CLOSED STATEMENT")
    )
    print()

    if final_ok:
        print("OVERALL: PASS  (the repository-level closed statement is consistent with the active code, but still partial rather than article-level final)")
        return 0

    print("OVERALL: FAIL  (the written closed statement is not consistent with the active repository formulas)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
