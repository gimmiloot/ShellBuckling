from __future__ import annotations

from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]

SIMPLE_CORE = ROOT / "src" / "shell_buckling" / "mixed_weak" / "solver_simple_support_core.py"
PATCHED_CORE = ROOT / "src" / "shell_buckling" / "mixed_weak" / "solver_patched_core.py"
BROAD_SCAN = ROOT / "src" / "shell_buckling" / "mixed_weak" / "boundary_matrix_scan.py"
TARGETED_SCAN = ROOT / "src" / "shell_buckling" / "mixed_weak" / "boundary_matrix_targeted_scan.py"

THEORY = ROOT / "docs" / "theory" / "vyvod_uravneniy_updated17.md"
ASSUMPTIONS = ROOT / "docs" / "assumptions" / "assumptions.md"
JOURNAL = ROOT / "docs" / "journal" / "project_journal_updated14.md"


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def print_check(label: str, ok: bool, detail: str) -> None:
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")
    print(f"  {detail}")


def line_with(text: str, needle: str) -> str:
    for line in text.splitlines():
        if needle in line:
            return line.strip()
    raise ValueError(f"Needle not found: {needle}")


def separately_linear(expr: sp.Expr, vars_: list[sp.Symbol]) -> bool:
    zero_subs = {var: 0 for var in vars_}
    at_zero = sp.simplify(expr.subs(zero_subs)) == 0
    second_derivatives = all(
        sp.simplify(sp.diff(expr, a, b)) == 0 for a in vars_ for b in vars_
    )
    return bool(at_zero and second_derivatives)


def depends_on(expr: sp.Expr, var: sp.Symbol) -> bool:
    return sp.simplify(sp.diff(expr, var)) != 0


def main() -> int:
    print("Pilot 06: G_ps as mixed-weak prestress/load block")
    print()
    print("Expected result for this pilot:")
    print("  the current repository should expose a mixed-slot prestress/load block,")
    print("  not just a scalar closure G(U);")
    print("  the active solver-level forcing should be bilinear after pairing with")
    print("  independent test slots;")
    print("  but the support should still remain partial because the full article-level")
    print("  formula for G_ps is not yet closed in the repository.")
    print()

    simple_text = load_text(SIMPLE_CORE)
    patched_text = load_text(PATCHED_CORE)
    broad_text = load_text(BROAD_SCAN)
    targeted_text = load_text(TARGETED_SCAN)
    theory_text = load_text(THEORY)
    assumptions_text = load_text(ASSUMPTIONS)
    journal_text = load_text(JOURNAL)

    print("Blocks used from the current repository:")
    print(f"  {SIMPLE_CORE.relative_to(ROOT)}")
    print(f"    {line_with(simple_text, 'g_s = ')}")
    print(f"    {line_with(simple_text, 'g_n = ')}")
    print(f"    {line_with(simple_text, 'R_Ts = ')}")
    print(f"    {line_with(simple_text, 'R_Qs = ')}")
    print(f"    {line_with(simple_text, 'R_Ms = ')}")
    print(f"  {PATCHED_CORE.relative_to(ROOT)}")
    print(f"    {line_with(patched_text, 'g_s = ')}")
    print(f"    {line_with(patched_text, 'g_n = ')}")
    print(f"    {line_with(patched_text, 'R_Ts = ')}")
    print(f"    {line_with(patched_text, 'R_Qs = ')}")
    print(f"    {line_with(patched_text, 'R_Ms = ')}")
    print()

    print("A. Repository-source guard")
    docs_ok = all(
        [
            "A_n(X, Xhat; q) = K_n(X, Xhat) - G_ps,n(X, Xhat; q) + B_partial,n(X, Xhat) = 0," in theory_text,
            "scalar potential `G(U)`" in theory_text,
            "weak-form `G_ps`" in theory_text,
            "`G_ps(U,Uhat)`" in assumptions_text,
            "scalar-potential route" in assumptions_text,
            "`G_ps(U, Uhat)`" in journal_text,
        ]
    )
    core_formula_ok = all(
        [
            'g_s = -(b["T_theta"] / r0) * r_x - b["T_sn"] * phi_x' in simple_text,
            'g_n = b["T_s"] * phi_x + (c0 / x_safe) * b["T_theta"] * phi - (b["q"] / x_safe) * (r0 * e_s + lam_s0 * r)' in simple_text,
            'R_Ts = Ts_x + a0 * Ts - (c0 / x_safe) * Ttheta + (n / x_safe) * S - kap_s0 * Qs - (s0 * c0 / (r0 * r0)) * Mtheta - g_s' in simple_text,
            'R_Qs = Qs_x + a0 * Qs - kap_s0 * Ts + (s0 / x_safe) * Ttheta - (s0 * s0 / (r0 * r0)) * Mtheta + b_m * chi - g_n' in simple_text,
            'R_Ms = Ms_x + a0 * Ms - a0 * Mtheta - Qs + (n / x_safe) * H - (b["M_theta"] / r0) * r_x' in simple_text,
            'g_s = -(b["T_theta"] / r0) * r_x - b["T_sn"] * phi_x' in patched_text,
            'g_n = b["T_s"] * phi_x + (c0 / x_safe) * b["T_theta"] * phi - (b["q"] / x_safe) * (r0 * e_s + lam_s0 * r)' in patched_text,
            'R_Ts = Ts_x + a0 * Ts - (c0 / x_safe) * Ttheta + (n / x_safe) * S - kap_s0 * Qs - (s0 * c0 / (r0 * r0)) * Mtheta - g_s' in patched_text,
            'R_Qs = Qs_x + a0 * Qs - kap_s0 * Ts + (s0 / x_safe) * Ttheta - (s0 * s0 / (r0 * r0)) * Mtheta + b_m * chi - g_n' in patched_text,
            'R_Ms = Ms_x + a0 * Ms - a0 * Mtheta - Qs + (n / x_safe) * H - (b["M_theta"] / r0) * r_x' in patched_text,
        ]
    )
    active_path_ok = all(
        [
            "from shell_buckling.mixed_weak import solver_simple_support_core as mw" in broad_text,
            "from shell_buckling.mixed_weak import solver_patched_core as mw" in targeted_text,
        ]
    )

    print_check(
        "theory/assumptions/journal explicitly record the mixed weak G_ps statement",
        docs_ok,
        "expected: current docs say the branch uses G_ps rather than one scalar potential G(U)",
    )
    print_check(
        "both active solver cores contain the same forcing-block formulas",
        core_formula_ok,
        "expected: g_s, g_n and the moment-row background term appear in both active cores",
    )
    print_check(
        "active broad/targeted scan paths are wired to those mixed-weak cores",
        active_path_ok,
        "expected: the live scan workflow uses the same solver-level forcing block",
    )
    print()

    x, n, nu = sp.symbols("x n nu", nonzero=True)
    c0, s0, kap_s0, lam_s0, r0 = sp.symbols("c0 s0 kap_s0 lam_s0 r0", nonzero=True)
    Ttheta_bg, Tsn_bg, Ts_bg, Mtheta_bg, q_bg = sp.symbols(
        "Ttheta_bg Tsn_bg Ts_bg Mtheta_bg q_bg"
    )
    us, un, v, phi = sp.symbols("u_s u_n v phi")
    us_x, un_x, phi_x = sp.symbols("u_s_x u_n_x phi_x")
    Ts = sp.symbols("T_s")
    T_hat, Q_hat, M_hat = sp.symbols("T_hat Q_hat M_hat")

    r = c0 * us + s0 * un
    r_x = -(kap_s0 * s0) * us + c0 * us_x + (kap_s0 * c0) * un + s0 * un_x
    e_theta = r / x + (n / x) * v
    Ttheta = nu * Ts + e_theta
    e_s = sp.expand(Ts - nu * Ttheta)

    g_s = sp.expand(-(Ttheta_bg / r0) * r_x - Tsn_bg * phi_x)
    g_n = sp.expand(Ts_bg * phi_x + (c0 / x) * Ttheta_bg * phi - (q_bg / x) * (r0 * e_s + lam_s0 * r))
    g_m = sp.expand((Mtheta_bg / r0) * r_x)
    G_ps_code = sp.expand(T_hat * g_s + Q_hat * g_n + M_hat * g_m)

    print("Symbolic formulas used in the CAS layer:")
    print(f"  g_s = {g_s}")
    print(f"  g_n = {g_n}")
    print(f"  g_m = {g_m}")
    print(f"  G_ps^code = {G_ps_code}")
    print()

    trial_vars = [us, us_x, un, un_x, v, phi, phi_x, Ts]
    test_vars = [T_hat, Q_hat, M_hat]

    print("B. Bilinear / mixed-slot structural checks")
    trial_linearity_ok = all(separately_linear(expr, trial_vars) for expr in [g_s, g_n, g_m])
    test_linearity_ok = separately_linear(G_ps_code, test_vars)
    trial_slot_zero_ok = sp.simplify(G_ps_code.subs({var: 0 for var in trial_vars})) == 0
    test_slot_zero_ok = sp.simplify(G_ps_code.subs({var: 0 for var in test_vars})) == 0

    print_check(
        "trial-side forcing expressions are linear in the active trial variables",
        trial_linearity_ok,
        "expected: g_s, g_n, g_m are background-weighted linear forms in the current trial slot",
    )
    print_check(
        "paired block is linear in the independent mixed test slot",
        test_linearity_ok and trial_slot_zero_ok and test_slot_zero_ok,
        "expected: after pairing with (T_hat, Q_hat, M_hat), the active block is bilinear in trial/test slots",
    )
    print()

    print("C. Scalar-closure versus genuine mixed-block checks")
    depends_on_test_slots_ok = all(depends_on(G_ps_code, var) for var in test_vars)
    depends_on_stress_trial_ok = depends_on(G_ps_code, Ts)
    channel_coupling_ok = all(
        [
            depends_on(g_n, v),
            depends_on(g_n, Ts),
            depends_on(g_s, phi_x),
            depends_on(g_m, us_x),
        ]
    )

    print_check(
        "active block depends on independent mixed test slots",
        depends_on_test_slots_ok,
        "expected: the current forcing block acts through mixed test variables, not only through one scalar slot",
    )
    print_check(
        "active block depends on the stress-like trial variable T_s",
        depends_on_stress_trial_ok,
        f"actual symbolic derivative d(G_ps^code)/dT_s = {sp.simplify(sp.diff(G_ps_code, Ts))}",
    )
    print_check(
        "active forcing couples multiple current mixed-weak channels",
        channel_coupling_ok,
        "expected: current forcing should see displacement/rotation-type content and stress-like content together",
    )
    print()

    print("D. Final explicit conclusion")
    structural_pass = all(
        [
            docs_ok,
            core_formula_ok,
            active_path_ok,
            trial_linearity_ok,
            test_linearity_ok,
            trial_slot_zero_ok,
            test_slot_zero_ok,
            depends_on_test_slots_ok,
            depends_on_stress_trial_ok,
            channel_coupling_ok,
        ]
    )

    print("What exact property was tested:")
    print("  whether the current repository exposes a solver-level prestress/load block")
    print("  that is genuinely mixed and bilinear in the current sense, rather than")
    print("  collapsing to one scalar potential G(U) of the displacement/rotation slot alone.")
    print()
    print("Expected result:")
    print("  PASS on structural bilinearity and mixed-slot dependence,")
    print("  but only PARTIAL support overall because the full article-level G_ps formula")
    print("  is still not finalized in the repository.")
    print()
    print(f"Actual result: {'PASS' if structural_pass else 'FAIL'}")
    print(
        "Support level: "
        + ("PARTIAL SUPPORT ONLY" if structural_pass else "NO STRUCTURAL SUPPORT")
    )
    print()

    if structural_pass:
        print(
            "OVERALL: PASS  (the current repository supports V-S1 structurally, "
            "but only at a clarified-and-still-partial level)"
        )
        return 0

    print(
        "OVERALL: FAIL  (the current repository does not currently support the intended "
        "mixed-bilinear G_ps statement even at the structural/CAS level)"
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
