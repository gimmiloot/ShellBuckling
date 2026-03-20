from __future__ import annotations

from pathlib import Path
import sys

try:
    import sympy as sp
except ModuleNotFoundError as exc:
    print("SymPy is required for proof_pilots/pilot_03_central_regular_family/cas_check.py")
    print("Install it in the active environment, for example:")
    print("  .\\.venv\\Scripts\\python.exe -m pip install sympy")
    raise SystemExit(2) from exc


ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.mixed_weak import solver_simple_support_core as simple_core
from shell_buckling.mixed_weak import solver_patched_core as patched_core


THEORY_FILE = ROOT / "docs" / "theory" / "vyvod_uravneniy_updated17.md"
SCAN_FILES = [
    ROOT / "src" / "shell_buckling" / "mixed_weak" / "boundary_matrix_scan.py",
    ROOT / "src" / "shell_buckling" / "mixed_weak" / "boundary_matrix_targeted_scan.py",
]

THEORY_LINES = [
    "u_s, u_n, v = O(x^n),",
    "varphi, psi = O(x^(n-1)),",
    "T_s, S, T_theta = O(x^(n-1)),",
    "Q_s, M_s, M_theta, H, chi = O(x^(n-2)).",
]

CENTER_LINES = [
    "0: u_s / x^n",
    "1: phi / x^(n-1)",
    "2: u_n / x^n + (lambda_c / n) * phi / x^(n-1)",
    "3: psi / x^(n-1) - lambda_c * phi / x^(n-1)",
]


def print_check(name: str, ok: bool, detail: str) -> bool:
    print(f"[{name}] {'PASS' if ok else 'FAIL'}")
    print(f"  {detail}")
    return ok


def source_guard() -> bool:
    ok_all = True

    theory_text = THEORY_FILE.read_text(encoding="utf-8")
    print("Source guard: theory scaling block")
    for line in THEORY_LINES:
        ok = line in theory_text
        ok_all &= ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {line}")
    print()

    print("Source guard: center constraint formulas")
    for path in SCAN_FILES:
        text = path.read_text(encoding="utf-8")
        for line in CENTER_LINES:
            ok = line in text
            ok_all &= ok
            print(f"  [{'PASS' if ok else 'FAIL'}] {path.relative_to(ROOT)} contains `{line}`")
    print()
    return ok_all


def exponent_check(n_value: int = 13) -> bool:
    expected = {
        "u_s": n_value,
        "u_n": n_value,
        "v": n_value,
        "phi": n_value - 1,
        "psi": n_value - 1,
        "T_s": n_value - 1,
        "Q_s": n_value - 2,
        "M_s": n_value - 2,
    }

    ok_all = True
    print(f"Exponent check at n={n_value}")
    for name, exp in expected.items():
        got_simple = simple_core.field_exponent(name, n_value)
        got_patched = patched_core.field_exponent(name, n_value)
        ok = (got_simple == exp) and (got_patched == exp)
        ok_all &= ok
        print(
            f"  [{'PASS' if ok else 'FAIL'}] {name}: "
            f"simple={got_simple}, patched={got_patched}, expected={exp}"
        )
    print()
    return ok_all


def main() -> int:
    print("Pilot 03: central regular family")
    print()

    ok_source = source_guard()
    ok_exponents = exponent_check()

    n, lambda_c = sp.symbols("n lambda_c", nonzero=True)
    a_us, a_phi, a_un, a_psi = sp.symbols("a_us a_phi a_un a_psi")
    alpha, beta = sp.symbols("alpha beta")

    lead_vec = sp.Matrix([a_us, a_phi, a_un, a_psi])
    regularity_matrix = sp.Matrix(
        [
            [0, sp.simplify(lambda_c / n), 1, 0],
            [0, -lambda_c, 0, 1],
        ]
    )
    center_functionals = sp.Matrix(
        [
            a_us,
            a_phi,
            a_un + (lambda_c / n) * a_phi,
            a_psi - lambda_c * a_phi,
        ]
    )

    print("Current reduced center ansatz on leading amplitudes:")
    print("  coordinates = [u_s/x^n, phi/x^(n-1), u_n/x^n, psi/x^(n-1)]")
    print("  regularity relations:")
    print("    u_n/x^n + (lambda_c/n) * phi/x^(n-1) = 0")
    print("    psi/x^(n-1) - lambda_c * phi/x^(n-1) = 0")
    print()

    rank = regularity_matrix.rank()
    nullity = int(lead_vec.rows - rank)
    nullspace = regularity_matrix.nullspace()
    ok_rank = print_check(
        "rank/nullity",
        rank == 2 and nullity == 2 and len(nullspace) == 2,
        f"rank={rank}, nullity={nullity}, nullspace basis count={len(nullspace)}",
    )
    print()

    print("Nullspace basis returned by SymPy:")
    for i, basis_vec in enumerate(nullspace, start=1):
        print(f"  basis {i}: {sp.sstr(sp.simplify(basis_vec))}")
    print()

    parameterized_family = sp.Matrix(
        [
            alpha,
            beta,
            -(lambda_c / n) * beta,
            lambda_c * beta,
        ]
    )
    residual_param = sp.simplify(regularity_matrix * parameterized_family)
    ok_param = print_check(
        "two-parameter family",
        residual_param == sp.zeros(2, 1),
        f"regularity_matrix * parameterized_family = {sp.sstr(residual_param)}",
    )
    print("  parameterization:")
    print(f"    u_s/x^n      = {alpha}")
    print(f"    phi/x^(n-1)  = {beta}")
    print(f"    u_n/x^n      = {sp.sstr(-(lambda_c / n) * beta)}")
    print(f"    psi/x^(n-1)  = {sp.sstr(lambda_c * beta)}")
    print()

    mode1 = sp.Matrix([1, 0, 0, 0])
    mode2 = sp.Matrix([0, 1, -(lambda_c / n), lambda_c])
    mode1_eval = sp.simplify(center_functionals.subs(dict(zip(lead_vec, mode1))))
    mode2_eval = sp.simplify(center_functionals.subs(dict(zip(lead_vec, mode2))))

    ok_mode1 = print_check(
        "normalized mode 1",
        mode1_eval == sp.Matrix([1, 0, 0, 0]),
        f"center functionals on mode 1 = {sp.sstr(mode1_eval)}",
    )
    ok_mode2 = print_check(
        "normalized mode 2",
        mode2_eval == sp.Matrix([0, 1, 0, 0]),
        f"center functionals on mode 2 = {sp.sstr(mode2_eval)}",
    )
    print()

    success = all([ok_source, ok_exponents, ok_rank, ok_param, ok_mode1, ok_mode2])
    print("Summary:")
    print(f"  Source guard: {'PASS' if ok_source else 'FAIL'}")
    print(f"  Exponent check: {'PASS' if ok_exponents else 'FAIL'}")
    print(f"  Reduced center nullity = 2: {'PASS' if ok_rank else 'FAIL'}")
    print(f"  Two-parameter reduced family: {'PASS' if ok_param else 'FAIL'}")
    print(f"  Normalized modes: {'PASS' if (ok_mode1 and ok_mode2) else 'FAIL'}")
    print()
    print(
        "OVERALL: "
        + ("PASS" if success else "FAIL")
        + "  (for the current reduced center ansatz used by the repository)"
    )
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
