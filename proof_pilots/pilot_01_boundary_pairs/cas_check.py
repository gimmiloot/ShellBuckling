from __future__ import annotations

try:
    import sympy as sp
except ModuleNotFoundError as exc:
    print("SymPy is required for proof_pilots/pilot_01_boundary_pairs/cas_check.py")
    print("Install it in the active environment, for example:")
    print("  .\\.venv\\Scripts\\python.exe -m pip install sympy")
    raise SystemExit(2) from exc


Ts, Qs, S, Ms, H = sp.symbols("T_s Q_s S M_s H")
us_hat, un_hat, v_hat, varphi_hat, psi_hat = sp.symbols(
    "u_s_hat u_n_hat v_hat varphi_hat psi_hat"
)

# Alias kept for the task statement: phi_hat means the same variation as varphi_hat.
phi_hat = varphi_hat

boundary_form = Ts * us_hat + Qs * un_hat + S * v_hat + Ms * varphi_hat + H * psi_hat
expected_reduced_form = Ts * us_hat + S * v_hat + H * psi_hat
reduced_form = sp.expand(boundary_form.subs({un_hat: 0, phi_hat: 0}))


def check_equal(name: str, lhs: sp.Expr, rhs: sp.Expr) -> bool:
    diff = sp.simplify(lhs - rhs)
    ok = diff == 0
    print(f"[{name}] {'OK' if ok else 'FAIL'}")
    print(f"  lhs = {sp.sstr(lhs)}")
    print(f"  rhs = {sp.sstr(rhs)}")
    if not ok:
        print(f"  lhs - rhs = {sp.sstr(diff)}")
    return ok


def basis_value(name: str, triple: tuple[int, int, int]) -> sp.Expr:
    value = sp.expand(
        reduced_form.subs({us_hat: triple[0], v_hat: triple[1], psi_hat: triple[2]})
    )
    print(f"[basis {name}] (u_s_hat, v_hat, psi_hat) = {triple} -> {sp.sstr(value)}")
    return value


def main() -> int:
    print("Pilot 01: boundary-pair reduction check")
    print()
    print("Full boundary form:")
    print(f"  {sp.sstr(boundary_form)}")
    print()
    print("Admissibility conditions:")
    print("  u_n_hat = 0")
    print("  varphi_hat = 0  (applied through phi_hat alias in the task statement)")
    print()
    print("Reduced boundary form:")
    print(f"  {sp.sstr(reduced_form)}")
    print()

    ok_reduce = check_equal("reduction", reduced_form, expected_reduced_form)
    print()

    b1 = basis_value("e_us", (1, 0, 0))
    b2 = basis_value("e_v", (0, 1, 0))
    b3 = basis_value("e_psi", (0, 0, 1))
    print()

    ok_b1 = check_equal("basis e_us", b1, Ts)
    print()
    ok_b2 = check_equal("basis e_v", b2, S)
    print()
    ok_b3 = check_equal("basis e_psi", b3, H)
    print()

    success = all([ok_reduce, ok_b1, ok_b2, ok_b3])
    print("Summary:")
    print(f"  {'PASS' if success else 'FAIL'}")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
