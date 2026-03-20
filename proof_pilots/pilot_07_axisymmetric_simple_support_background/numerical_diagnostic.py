from __future__ import annotations

import inspect
import re
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_bvp


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from shell_buckling.mixed_weak import solver_patched_core as patched
from shell_buckling.mixed_weak import solver_simple_support_core as broad
from shell_buckling.supporting import determinant_criterion_comparison as support


def extract_indexed_state_map(source: str) -> list[tuple[int, str]]:
    pairs: list[tuple[int, str]] = []
    for name, idx in re.findall(r"^\s*([A-Za-z_]\w*)\s*=\s*y\[(\d+)\]", source, flags=re.MULTILINE):
        pairs.append((int(idx), name))
    for name, idx in re.findall(r"^\s*([A-Za-z_]\w*)\s*=\s*np\.maximum\(y\[(\d+)\]", source, flags=re.MULTILINE):
        pairs.append((int(idx), name))
    unique: dict[int, str] = {}
    for idx, name in pairs:
        unique[idx] = name
    return sorted(unique.items())


def actual_fmin_bc_matches(module, x0: float) -> tuple[bool, np.ndarray]:
    ya = np.array([11.0, 22.0, 33.0, 44.0, 55.0], dtype=float)
    yb = np.array([66.0, 77.0, 88.0, 99.0, 111.0], dtype=float)
    got = module.axisymmetric_fmin_bc(ya, yb, x0=float(x0))
    expected = np.array([yb[0], yb[4], ya[1], ya[3] - float(x0), ya[4]], dtype=float)
    return bool(np.allclose(got, expected)), got


def run_active_fallback_check() -> dict[str, object]:
    p_grid = np.array([0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
    try:
        _, sols = broad.solve_axisymmetric_fmin_continuation(
            p_grid,
            nd_bvp=1400,
            x0=1.0e-3,
            tol=1.0e-4,
            max_nodes=150000,
            verbose=False,
        )
        return {
            "success": True,
            "grid_mpa": p_grid.tolist(),
            "n_solutions": len(sols),
            "last_nodes": int(sols[-1].x.size),
        }
    except Exception as exc:  # pragma: no cover
        return {
            "success": False,
            "grid_mpa": p_grid.tolist(),
            "error": f"{type(exc).__name__}: {exc}",
        }


def bc_simple_support(ya: np.ndarray, yb: np.ndarray) -> np.ndarray:
    return np.array(
        [
            yb[0],
            yb[2],
            yb[4],
            ya[1],
            ya[3],
            ya[5],
        ],
        dtype=float,
    )


def solve_direct_simple_support_step(
    q_mpa: float,
    x_mesh: np.ndarray,
    y_guess: np.ndarray,
    tol: float = 1.0e-4,
    max_nodes: int = 150000,
):
    support.q = float(q_mpa) * 1.0e6
    sol = solve_bvp(
        support.axisym_nepol,
        bc_simple_support,
        x_mesh,
        y_guess,
        tol=tol,
        max_nodes=max_nodes,
        verbose=0,
    )
    if not sol.success:
        sol = solve_bvp(
            support.axisym_nepol,
            bc_simple_support,
            x_mesh,
            y_guess,
            tol=min(5.0e-4, 5.0 * tol),
            max_nodes=max_nodes,
            verbose=0,
        )
    return sol


def run_direct_simple_support_diagnostic() -> dict[str, object]:
    x0 = 1.0 / 700.0
    x_mesh = np.linspace(x0, 1.0, 700)
    y_guess = np.zeros((6, x_mesh.size), dtype=float)
    sol_prev = None
    history: list[dict[str, object]] = []

    coarse_grid = np.linspace(0.0, 4.2, 22)
    refine_grid = [4.25, 4.30, 4.33, 4.34, 4.35, 4.36, 4.37, 4.38, 4.39, 4.40]

    for q_mpa in coarse_grid:
        if sol_prev is not None:
            y_guess = sol_prev.sol(x_mesh)
        sol = solve_direct_simple_support_step(q_mpa, x_mesh, y_guess)
        record = {
            "q_mpa": float(q_mpa),
            "success": bool(sol.success),
            "nodes": int(sol.x.size),
            "message": sol.message,
            "max_rms": float(np.max(sol.rms_residuals)) if sol.success and hasattr(sol, "rms_residuals") else float("nan"),
        }
        history.append(record)
        if not sol.success:
            return {
                "history": history,
                "last_success_mpa": None,
                "first_failure_mpa": float(q_mpa),
                "failure_message": sol.message,
            }
        sol_prev = sol

    last_success_mpa = float(history[-1]["q_mpa"])
    first_failure_mpa = None
    failure_message = None

    for q_mpa in refine_grid:
        y_guess = sol_prev.sol(x_mesh)
        sol = solve_direct_simple_support_step(q_mpa, x_mesh, y_guess)
        record = {
            "q_mpa": float(q_mpa),
            "success": bool(sol.success),
            "nodes": int(sol.x.size),
            "message": sol.message,
            "max_rms": float(np.max(sol.rms_residuals)) if sol.success and hasattr(sol, "rms_residuals") else float("nan"),
        }
        history.append(record)
        if not sol.success:
            first_failure_mpa = float(q_mpa)
            failure_message = sol.message
            break
        sol_prev = sol
        last_success_mpa = float(q_mpa)

    return {
        "history": history,
        "last_success_mpa": last_success_mpa,
        "first_failure_mpa": first_failure_mpa,
        "failure_message": failure_message,
    }


def main() -> None:
    x0 = 1.0e-3

    broad_source = inspect.getsource(broad.axisymmetric_fmin_ode)
    patched_source = inspect.getsource(patched.axisymmetric_fmin_ode)
    broad_state_map = extract_indexed_state_map(broad_source)
    patched_state_map = extract_indexed_state_map(patched_source)
    broad_bc_ok, broad_bc_vector = actual_fmin_bc_matches(broad, x0=x0)
    patched_bc_ok, patched_bc_vector = actual_fmin_bc_matches(patched, x0=x0)
    active_has_uz_slot = any(name in {"uz", "u_z", "u_z0"} for _, name in broad_state_map)

    active_fallback = run_active_fallback_check()
    direct_simple = run_direct_simple_support_diagnostic()

    current_bc = "T_s0(1)=0, varphi0(1)=0, Q0(x0)=0, r0(x0)=x0, varphi0(x0)=0"
    intended_bc = "center: T_sn(x0)=0, u_r(x0)=0, varphi(x0)=0; edge: T_s(1)=0, M_s(1)=0, u_z(1)=0"
    bc_match = False

    if not active_has_uz_slot:
        mismatch_reason = "The active 5-state background has no u_z slot, so u_z(1)=0 cannot be imposed there."
    else:
        mismatch_reason = "The active background BC set does not coincide with the intended simple-support BC set."

    verdict = "ONLY HYBRID/PARTIAL"
    if active_has_uz_slot and bc_match and direct_simple["first_failure_mpa"] is None:
        verdict = "AVAILABLE"
    elif direct_simple["last_success_mpa"] is None:
        verdict = "UNAVAILABLE"

    next_step = (
        "Extract the full 6-state non-shallow axisymmetric background "
        "[T_s, T_sn, M_s, u_r, u_z, varphi] into a separate active module, "
        "expose the simple-support BC set T_sn(x0)=0, u_r(x0)=0, varphi(x0)=0, "
        "T_s(1)=0, M_s(1)=0, u_z(1)=0, and stabilize fixed-load solves before "
        "reconnecting continuation and mixed-weak scans."
    )

    print("=== Pilot 07: Axisymmetric simple-support background diagnostic ===")
    print()
    print("A. Current background solver path currently exists")
    print("  active core modules:")
    print("   - shell_buckling.mixed_weak.solver_simple_support_core")
    print("   - shell_buckling.mixed_weak.solver_patched_core")
    print(f"  broad 5-state map from live code: {broad_state_map}")
    print(f"  patched 5-state map from live code: {patched_state_map}")
    print(f"  broad BC check against live implementation: {'PASS' if broad_bc_ok else 'FAIL'} -> {broad_bc_vector.tolist()}")
    print(f"  patched BC check against live implementation: {'PASS' if patched_bc_ok else 'FAIL'} -> {patched_bc_vector.tolist()}")
    print(f"  actual active BC set: {current_bc}")
    print()
    print("B. Intended simple-support BC set")
    print(f"  intended simple-support BCs: {intended_bc}")
    print(f"  current/intent match: {'YES' if bc_match else 'NO'}")
    print(f"  mismatch reason: {mismatch_reason}")
    print()
    print("C. Active hybrid fallback check")
    if active_fallback["success"]:
        print(
            "  PASS: current F_min fallback continuation ran on "
            f"{active_fallback['grid_mpa']} MPa with {active_fallback['n_solutions']} solutions; "
            f"last nodes={active_fallback['last_nodes']}"
        )
    else:
        print(f"  FAIL: current F_min fallback check failed -> {active_fallback['error']}")
    print()
    print("D. Direct full-state simple-support diagnostic")
    print("  closest current full-state axisymmetric equations: shell_buckling.supporting.determinant_criterion_comparison.axisym_nepol")
    print("  direct BC used diagnostically: T_s(1)=0, M_s(1)=0, u_z(1)=0, T_sn(x0)=0, u_r(x0)=0, varphi(x0)=0")
    print(f"  last successful continued load: {direct_simple['last_success_mpa']}")
    print(f"  first failed load: {direct_simple['first_failure_mpa']}")
    print(f"  failure message: {direct_simple['failure_message']}")
    print("  representative continuation history:")
    for item in direct_simple["history"][-6:]:
        rms = item["max_rms"]
        rms_str = f"{rms:.2e}" if np.isfinite(rms) else "nan"
        print(
            f"   q={item['q_mpa']:.3f} MPa  success={item['success']}  "
            f"nodes={item['nodes']}  max_rms={rms_str}  message={item['message']}"
        )
    print()
    print("E. Final diagnostic result")
    print(f"  verdict: {verdict}")
    if verdict == "AVAILABLE":
        print("  The full axisymmetric simple-support background is already available as a clean stable runnable solver path.")
    elif verdict == "UNAVAILABLE":
        print("  The full axisymmetric simple-support background is currently unavailable even as a partial direct diagnostic.")
    else:
        print("  The full axisymmetric simple-support background is not available as a clean stable runnable solver path.")
        print("  What exists is a hybrid active fallback plus a partial direct full-state diagnostic that loses continuation near 4.3..4.4 MPa.")
    print()
    print("F. Smallest next actionable implementation step")
    print(f"  {next_step}")


if __name__ == "__main__":
    main()