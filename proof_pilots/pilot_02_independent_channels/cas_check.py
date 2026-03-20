from __future__ import annotations

from pathlib import Path

try:
    import sympy as sp
except ModuleNotFoundError as exc:
    print("SymPy is required for proof_pilots/pilot_02_independent_channels/cas_check.py")
    print("Install it in the active environment, for example:")
    print("  .\\.venv\\Scripts\\python.exe -m pip install sympy")
    raise SystemExit(2) from exc


ROOT = Path(__file__).resolve().parents[2]
SOURCE_FILES = [
    ROOT / "src" / "shell_buckling" / "mixed_weak" / "solver_simple_support_core.py",
    ROOT / "src" / "shell_buckling" / "mixed_weak" / "solver_patched_core.py",
]

SOURCE_FORMULAS = {
    "r": "r = c0 * us + s0 * un",
    "S": "S = (v_x - a0 * v - (n / x_safe) * us) / (2.0 * (1.0 + nu))",
    "kappa_theta_new": "kappa_theta_new = (c0 / r0) * phi - (s0 / (r0 * r0)) * r + b_theta * psi",
    "M_theta": "M_theta = nu * Ms + kappa_theta_new / Lambda",
    "H": "H = (psi_x - a0 * psi - b_s * phi) / C_twist",
    "H_x": "H_x = (psi_xx - a0_p * psi - a0 * psi_x - b_s_p * phi - b_s * phi_x) / C_twist",
    "chi": "chi = (b_theta * M_theta - H_x - 2.0 * a0 * H) / lam_th0",
}


def expr_text(expr: sp.Expr) -> str:
    return sp.sstr(sp.simplify(expr))


def is_zero(expr: sp.Expr) -> bool:
    return sp.simplify(expr) == 0


def is_potentially_nonzero(expr: sp.Expr) -> bool:
    return not is_zero(expr)


def format_state(state: dict[sp.Symbol, sp.Expr]) -> str:
    items = [f"{symbol}={expr_text(value)}" for symbol, value in state.items()]
    return ", ".join(items)


def print_check(name: str, expected: str, actual: str, ok: bool) -> bool:
    print(f"[{name}] {'PASS' if ok else 'FAIL'}")
    print(f"  expected: {expected}")
    print(f"  actual:   {actual}")
    return ok


def source_guard() -> bool:
    print("Source guard:")
    ok_all = True
    for path in SOURCE_FILES:
        text = path.read_text(encoding="utf-8")
        for name, line in SOURCE_FORMULAS.items():
            ok = line in text
            ok_all &= ok
            print(f"  [{'PASS' if ok else 'FAIL'}] {path.relative_to(ROOT)} contains {name}")
            if not ok:
                print(f"    missing line: {line}")
    print()
    return ok_all


nu, n = sp.symbols("nu n")
a0, a0_p = sp.symbols("a0 a0_p")
b_s, b_s_p, b_theta = sp.symbols("b_s b_s_p b_theta")
c0, s0, r0 = sp.symbols("c0 s0 r0")
x_safe = sp.symbols("x_safe")
C_twist, Lambda, lam_th0 = sp.symbols("C_twist Lambda lam_th0")

us, un = sp.symbols("us un")
v, v_x = sp.symbols("v v_x")
phi, phi_x = sp.symbols("phi phi_x")
psi, psi_x, psi_xx = sp.symbols("psi psi_x psi_xx")
Ms = sp.symbols("Ms")

r = c0 * us + s0 * un
S = (v_x - a0 * v - (n / x_safe) * us) / (2.0 * (1.0 + nu))
kappa_theta_new = (c0 / r0) * phi - (s0 / (r0 * r0)) * r + b_theta * psi
M_theta = nu * Ms + kappa_theta_new / Lambda
H = (psi_x - a0 * psi - b_s * phi) / C_twist
H_x = (psi_xx - a0_p * psi - a0 * psi_x - b_s_p * phi - b_s * phi_x) / C_twist
chi = (b_theta * M_theta - H_x - 2.0 * a0 * H) / lam_th0

v0, vx0, psix0, psi0 = sp.symbols("v0 vx0 psix0 psi0")

v_block_state = {
    us: sp.Integer(0),
    un: sp.Integer(0),
    v: v0,
    v_x: vx0,
    phi: sp.Integer(0),
    phi_x: sp.Integer(0),
    psi: sp.Integer(0),
    psi_x: sp.Integer(0),
    psi_xx: sp.Integer(0),
    Ms: sp.Integer(0),
}

psi_block_state = {
    us: sp.Integer(0),
    un: sp.Integer(0),
    v: sp.Integer(0),
    v_x: sp.Integer(0),
    phi: sp.Integer(0),
    phi_x: sp.Integer(0),
    psi: sp.Integer(0),
    psi_x: psix0,
    psi_xx: sp.Integer(0),
    Ms: sp.Integer(0),
}

chi_only_state = {
    us: sp.Integer(0),
    un: sp.Integer(0),
    v: sp.Integer(0),
    v_x: sp.Integer(0),
    phi: sp.Integer(0),
    phi_x: sp.Integer(0),
    psi: psi0,
    psi_x: a0 * psi0,
    psi_xx: sp.Integer(0),
    Ms: sp.Integer(0),
}


def evaluate_state(state: dict[sp.Symbol, sp.Expr]) -> dict[str, sp.Expr]:
    return {
        "S": sp.simplify(S.subs(state)),
        "H": sp.simplify(H.subs(state)),
        "chi": sp.simplify(chi.subs(state)),
    }


def main() -> int:
    print("Pilot 02: independent circumferential channels")
    print()

    ok_source = source_guard()

    print("Exact formulas used:")
    print(f"  {SOURCE_FORMULAS['S']}")
    print(f"  {SOURCE_FORMULAS['H']}")
    print(f"  {SOURCE_FORMULAS['chi']}")
    print("  Auxiliary exact formulas required by chi:")
    print(f"    {SOURCE_FORMULAS['r']}")
    print(f"    {SOURCE_FORMULAS['kappa_theta_new']}")
    print(f"    {SOURCE_FORMULAS['M_theta']}")
    print(f"    {SOURCE_FORMULAS['H_x']}")
    print()

    print("Structural symbolic checks:")
    checks_structural = []

    s_twist_derivs = [
        ("dS/dphi", sp.diff(S, phi)),
        ("dS/dphi_x", sp.diff(S, phi_x)),
        ("dS/dpsi", sp.diff(S, psi)),
        ("dS/dpsi_x", sp.diff(S, psi_x)),
        ("dS/dpsi_xx", sp.diff(S, psi_xx)),
        ("dS/dMs", sp.diff(S, Ms)),
    ]
    for name, expr in s_twist_derivs:
        checks_structural.append(print_check(name, "0", expr_text(expr), is_zero(expr)))
    print()

    h_v_derivs = [
        ("dH/dus", sp.diff(H, us)),
        ("dH/dv", sp.diff(H, v)),
        ("dH/dv_x", sp.diff(H, v_x)),
    ]
    for name, expr in h_v_derivs:
        checks_structural.append(print_check(name, "0", expr_text(expr), is_zero(expr)))
    print()

    chi_v_derivs = [
        ("dchi/dv", sp.diff(chi, v)),
        ("dchi/dv_x", sp.diff(chi, v_x)),
    ]
    for name, expr in chi_v_derivs:
        checks_structural.append(print_check(name, "0", expr_text(expr), is_zero(expr)))
    print()

    print("Witness states:")
    print(f"  v-block witness:   {format_state(v_block_state)}")
    print(f"  psi-block witness: {format_state(psi_block_state)}")
    print(f"  chi-only witness:  {format_state(chi_only_state)}")
    print()

    v_results = evaluate_state(v_block_state)
    psi_results = evaluate_state(psi_block_state)
    chi_results = evaluate_state(chi_only_state)

    print("A. v-block witness")
    checks_v = [
        print_check(
            "A1 S potentially nonzero",
            "S is not identically zero",
            f"S = {expr_text(v_results['S'])}",
            is_potentially_nonzero(v_results["S"]),
        ),
        print_check(
            "A2 H zero",
            "H = 0",
            f"H = {expr_text(v_results['H'])}",
            is_zero(v_results["H"]),
        ),
        print_check(
            "A3 chi zero",
            "chi = 0",
            f"chi = {expr_text(v_results['chi'])}",
            is_zero(v_results["chi"]),
        ),
    ]
    print()

    print("B. psi-block witness")
    checks_psi = [
        print_check(
            "B1 S zero",
            "S = 0",
            f"S = {expr_text(psi_results['S'])}",
            is_zero(psi_results["S"]),
        ),
        print_check(
            "B2 H potentially nonzero",
            "H is not identically zero",
            f"H = {expr_text(psi_results['H'])}",
            is_potentially_nonzero(psi_results["H"]),
        ),
        print_check(
            "B3 chi potentially nonzero",
            "chi is not identically zero",
            f"chi = {expr_text(psi_results['chi'])}",
            is_potentially_nonzero(psi_results["chi"]),
        ),
    ]
    print()

    print("C. Structural non-collapse")
    checks_collapse = [
        print_check(
            "C1 S/H witness separation",
            "v witness gives S != 0 and H = 0, psi witness gives S = 0 and H != 0",
            (
                f"v witness: S = {expr_text(v_results['S'])}, H = {expr_text(v_results['H'])}; "
                f"psi witness: S = {expr_text(psi_results['S'])}, H = {expr_text(psi_results['H'])}"
            ),
            is_potentially_nonzero(v_results["S"])
            and is_zero(v_results["H"])
            and is_zero(psi_results["S"])
            and is_potentially_nonzero(psi_results["H"]),
        ),
        print_check(
            "C2 S/chi witness separation",
            "v witness gives S != 0 and chi = 0, chi witness gives S = 0 and chi != 0",
            (
                f"v witness: S = {expr_text(v_results['S'])}, chi = {expr_text(v_results['chi'])}; "
                f"chi witness: S = {expr_text(chi_results['S'])}, chi = {expr_text(chi_results['chi'])}"
            ),
            is_potentially_nonzero(v_results["S"])
            and is_zero(v_results["chi"])
            and is_zero(chi_results["S"])
            and is_potentially_nonzero(chi_results["chi"]),
        ),
    ]
    print()

    success = all([ok_source, *checks_structural, *checks_v, *checks_psi, *checks_collapse])
    print("Summary:")
    print(f"  Source guard: {'PASS' if ok_source else 'FAIL'}")
    print(f"  Structural symbolic checks: {'PASS' if all(checks_structural) else 'FAIL'}")
    print(f"  A. v-block witness: {'PASS' if all(checks_v) else 'FAIL'}")
    print(f"  B. psi-block witness: {'PASS' if all(checks_psi) else 'FAIL'}")
    print(f"  C. structural non-collapse: {'PASS' if all(checks_collapse) else 'FAIL'}")
    print(f"  OVERALL: {'PASS' if success else 'FAIL'}")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
