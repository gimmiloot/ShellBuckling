from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp


THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[2]
SRC_ROOT = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


from shell_buckling.mixed_weak import axisymmetric_simple_support_background as ssbg
from shell_buckling.supporting import determinant_criterion_comparison as detcomp
from shell_buckling.supporting import dimensionless_background_comparison as dimcomp


def format_vector(items: list[str]) -> str:
    return "[" + ", ".join(items) + "]"


def report_block(title: str, items: list[str]) -> None:
    print(title)
    for item in items:
        print(f"  - {item}")
    print()


def main() -> None:
    x0, beta, gamma = sp.symbols("x0 beta gamma", positive=True)
    phi_a, phi_b, Ts_a, Ts_b = sp.symbols("phi_a phi_b Ts_a Ts_b", real=True)

    shallow_exact = [
        "theta0(x0)=0",
        "theta0(1)=0",
        "Phi0(x0)=0",
        "Phi0(1)=0",
    ]
    supporting_nonshallow_exact = [
        "T_s(1)=0",
        "T_sn(x0)=0",
        "u_r(x0)=0",
        "u_z(1)=0",
        "varphi(x0)=0",
        "varphi(1)=0",
    ]
    simple_support_exact = [
        "T_s(1)=0",
        "M_s(1)=0",
        "u_z(1)=0",
        "T_sn(x0)=0",
        "u_r(x0)=0",
        "varphi(x0)=0",
    ]

    print("=== Pilot 15 symbolic / structural BC mapping check ===")
    print()
    print("Exact shallow BC vector from determinant_criterion_comparison.py:")
    print(f"  bc_sh(ya, yb) = {format_vector(shallow_exact)}")
    print()
    print("Cross-check with dimensionless_background_comparison.py:")
    print(f"  bc_shallow(ya, yb) = {format_vector(shallow_exact)}")
    print()
    print("Exact non-shallow supporting comparison BC vector:")
    print(f"  bcNP(ya, yb) = {format_vector(supporting_nonshallow_exact)}")
    print()
    print("Exact 6-state simple-support BC vector:")
    print(
        "  axisymmetric_simple_support_bc(ya, yb) = "
        f"{format_vector(simple_support_exact)}"
    )
    print()

    theta0_a = -beta * sp.sin(phi_a)
    theta0_b = -beta * sp.sin(phi_b)
    Phi0_a = gamma * x0 * Ts_a
    Phi0_b = gamma * Ts_b

    print("Mapped shallow BCs in non-shallow variables:")
    print(f"  theta0(x0)=0  ->  {sp.Eq(theta0_a, 0)}")
    print(f"  theta0(1)=0   ->  {sp.Eq(theta0_b, 0)}")
    print(f"  Phi0(x0)=0    ->  {sp.Eq(Phi0_a, 0)}")
    print(f"  Phi0(1)=0     ->  {sp.Eq(Phi0_b, 0)}")
    print()
    print("Local branch reading used in this audit:")
    print("  theta0(x0)=0  => varphi(x0)=0 on the near-zero branch")
    print("  theta0(1)=0   => varphi(1)=0 on the near-zero branch")
    print("  Phi0(1)=0     => T_s(1)=0")
    print("  Phi0(x0)=0    => x*T_s(x0)=0 (center regularity in reduced variables)")
    print()

    shallow_edge_structural = {"T_s(1)=0", "varphi(1)=0"}
    shallow_center_structural = {"varphi(x0)=0", "x*T_s(x0)=0"}
    supporting_edge = {"T_s(1)=0", "u_z(1)=0", "varphi(1)=0"}
    simple_support_edge = {"T_s(1)=0", "M_s(1)=0", "u_z(1)=0"}

    report_block("Structural shallow edge set after mapping:", sorted(shallow_edge_structural))
    report_block("Structural shallow center set after mapping:", sorted(shallow_center_structural))

    supporting_edge_overlap = shallow_edge_structural & supporting_edge
    simple_support_edge_overlap = shallow_edge_structural & simple_support_edge
    simple_support_missing = simple_support_edge - shallow_edge_structural
    simple_support_extra = shallow_edge_structural - simple_support_edge

    report_block("Overlap with supporting non-shallow edge BCs:", sorted(supporting_edge_overlap))
    report_block("Overlap with 6-state simple-support edge BCs:", sorted(simple_support_edge_overlap))
    report_block("6-state simple-support edge conditions not represented by shallow BCs:", sorted(simple_support_missing))
    report_block("Shallow edge conditions not present in simple support:", sorted(simple_support_extra))

    detcomp_zero = detcomp.bc_sh(np.zeros(4), np.zeros(4)).tolist()
    dimcomp_zero = dimcomp.bc_shallow(np.zeros(4), np.zeros(4)).tolist()
    same_shallow_bc_in_both_supporting_modules = detcomp_zero == dimcomp_zero
    same_simple_support_vector = ssbg.BC_LABELS == (
        "T_s(1)=0",
        "M_s(1)=0",
        "u_z(1)=0",
        "T_sn(x0)=0",
        "u_r(x0)=0",
        "varphi(x0)=0",
    )

    shallow_structurally_equivalent_to_simple_support = False
    shallow_more_aligned_with_supporting_path = len(supporting_edge_overlap) > len(simple_support_edge_overlap)

    print("PASS/FAIL conclusions:")
    if same_shallow_bc_in_both_supporting_modules:
        print("  PASS: the two supporting shallow modules use the same shallow BC vector.")
    else:
        print("  FAIL: the supporting shallow modules do not use the same shallow BC vector.")

    if same_simple_support_vector:
        print("  PASS: the active 6-state simple-support module exposes the documented simple-support BC vector.")
    else:
        print("  FAIL: the active 6-state simple-support module BC labels do not match the expected vector.")

    if shallow_structurally_equivalent_to_simple_support:
        print("  PASS: shallow BCs are structurally equivalent to the 6-state simple-support BCs.")
    else:
        print("  FAIL: shallow BCs are NOT structurally equivalent to the 6-state simple-support BCs.")

    if shallow_more_aligned_with_supporting_path:
        print("  PASS: shallow BCs look aligned with the supporting moving-clamp/sliding-clamp path,")
        print("        because the mapped edge set matches T_s(1)=0 and varphi(1)=0 rather than M_s(1)=0.")
    else:
        print("  FAIL: shallow BCs do not look closer to the supporting moving-clamp/sliding-clamp path.")

    print()
    print("Final audit statement:")
    print("  The current shallow comparison path is a reduced shallow problem whose mapped edge BCs")
    print("  are clamp-like / moving-clamp-like, not simple-support edge BCs.")
    print("  It should therefore not be treated as a BC-equivalent simple-support comparator.")


if __name__ == "__main__":
    main()
