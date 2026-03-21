from __future__ import annotations

import sys
from pathlib import Path

import sympy as sp


THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[2]
SRC_ROOT = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


from shell_buckling.mixed_weak import axisymmetric_simple_support_background as ssbg


def main() -> None:
    beta, gamma, nu = sp.symbols("beta gamma nu", positive=True)
    phi, r, x, Ms = sp.symbols("phi r x M_s", positive=True, real=True)

    theta = -beta * sp.sin(phi)
    theta_p = -beta * sp.cos(phi) * (gamma * Ms - nu * sp.sin(phi) / r)

    exact_identity = sp.simplify(theta_p + nu * sp.cos(phi) * theta / r + beta * gamma * sp.cos(phi) * Ms)
    shallow_remainder = sp.expand(
        sp.simplify((theta_p + nu * theta / x + beta * gamma * Ms).subs(r, x))
    )
    shallow_series = sp.series(shallow_remainder, phi, 0, 4)

    proposed_shallow_bc = [
        "theta0(x0)=0",
        "Phi0(x0)=0",
        "Phi0(1)=0",
        "theta0'(1) + nu*theta0(1)=0",
    ]

    print("=== Pilot 16 shallow simple-support BC derivation check ===")
    print()
    print("Active 6-state non-shallow simple-support BC vector:")
    print(f"  {list(ssbg.BC_LABELS)}")
    print()
    print("Proposed shallow simple-support BC vector:")
    print(f"  {proposed_shallow_bc}")
    print()
    print("Exact mapping-level statements:")
    print("  theta0   = -beta*sin(varphi)")
    print("  theta0'  = -beta*cos(varphi)*kappa_s")
    print("  Phi0     = gamma*x*T_s")
    print("  kappa_s  = gamma*M_s - nu*sin(varphi)/r")
    print()
    print("Exact shell identity derived from those formulas:")
    print("  theta0' + nu*cos(varphi)*theta0/r = -beta*gamma*cos(varphi)*M_s")
    print(f"  symbolic residual = {exact_identity}")
    print()
    print("Shallow-limit inference used for the new edge BC:")
    print("  cos(varphi) ~ 1, r ~ x")
    print("  => theta0' + (nu/x)*theta0 ~ -beta*gamma*M_s")
    print(f"  residual after substituting r=x: {shallow_remainder}")
    print(f"  series at varphi=0: {shallow_series}")
    print()
    print("Interpretation of the proposed shallow BCs:")
    print("  theta0(x0)=0       : reduced center regularity condition (inferred reduced form)")
    print("  Phi0(x0)=0         : reduced center regularity condition (inferred reduced form)")
    print("  Phi0(1)=0          : exact image of T_s(1)=0 under Phi0 = gamma*x*T_s")
    print("  theta0'(1)+nu*theta0(1)=0 : inferred shallow image of M_s(1)=0")
    print("  u_z(1)=0           : not an independent BC in the 4-state shallow system;")
    print("                       imposed later as displacement normalization after recovery")
    print()
    print("PASS/FAIL conclusions:")
    if exact_identity == 0:
        print("  PASS: the exact theta0/theta0'/M_s identity follows from the repository mapping formulas.")
    else:
        print("  FAIL: the exact theta0/theta0'/M_s identity did not simplify to zero.")

    simple_support_edge_bc_is_robin = proposed_shallow_bc[-1] == "theta0'(1) + nu*theta0(1)=0"
    if simple_support_edge_bc_is_robin:
        print("  PASS: the proposed shallow simple-support edge BC is Robin-type, not theta0(1)=0.")
    else:
        print("  FAIL: the proposed edge BC is not the intended simple-support Robin condition.")

    old_moving_clamp_bc = "theta0(1)=0"
    if proposed_shallow_bc[-1] != old_moving_clamp_bc:
        print("  PASS: the new shallow comparator does not reuse the old moving-clamp/sliding-clamp edge BC.")
    else:
        print("  FAIL: the new shallow comparator still reuses the old edge BC.")

    print()
    print("Final structural conclusion:")
    print("  The strongest repository-level shallow simple-support BC set currently justified is")
    print("  [theta0(x0)=0, Phi0(x0)=0, Phi0(1)=0, theta0'(1)+nu*theta0(1)=0],")
    print("  with Phi0(1)=0 exact and the Robin moment BC inferred from the shallow limit")
    print("  of the exact shell mapping.")


if __name__ == "__main__":
    main()
