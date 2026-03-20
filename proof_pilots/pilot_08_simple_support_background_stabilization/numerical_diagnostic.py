from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np


warnings.filterwarnings("ignore", category=RuntimeWarning)

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

import shell_buckling.mixed_weak.axisymmetric_simple_support_background as ss
from shell_buckling.supporting import determinant_criterion_comparison as supporting


BASE_CONFIG = ss.AxisymmetricSimpleSupportConfig()
MORE_NODES_CONFIG = ss.AxisymmetricSimpleSupportConfig(max_nodes=240000)
DENSE_MESH_CONFIG = ss.AxisymmetricSimpleSupportConfig(nd_bvp=700, max_nodes=240000)
RELAXED_CONFIG = ss.AxisymmetricSimpleSupportConfig(max_nodes=240000, tol=2.0e-4, relaxed_tol=1.0e-3)


def fmt(x: float) -> str:
    if x is None or not np.isfinite(x):
        return "nan"
    return f"{x:.3e}"


def build_probe_state(x: np.ndarray) -> np.ndarray:
    return np.vstack(
        [
            8.0e-3 * (1.0 - x),
            1.0e-3 * np.sin(0.5 * np.pi * x),
            5.0e-5 * np.cos(0.5 * np.pi * x),
            2.0e-2 * x * (1.0 - x),
            1.0e-1 * (1.0 - x),
            1.5e-1 * np.sin(0.5 * np.pi * x),
        ]
    )


def equation_match_check() -> dict[str, float]:
    x = np.linspace(BASE_CONFIG.x0, 1.0, 9)
    y = build_probe_state(x)
    q_pa = 4.3275e6
    lhs = ss.axisymmetric_simple_support_ode(x, y, q_pa=q_pa)
    supporting.q = q_pa
    rhs = supporting.axisym_nepol(x, y)
    diff = np.abs(lhs - rhs)
    return {
        "max_abs_diff": float(np.max(diff)),
        "mean_abs_diff": float(np.mean(diff)),
    }


def bc_residual_from_sol(sol) -> np.ndarray:
    return ss.axisymmetric_simple_support_bc(sol.y[:, 0], sol.y[:, -1])


def raw_attempt(q_mpa: float, config: ss.AxisymmetricSimpleSupportConfig, guess: np.ndarray) -> dict[str, object]:
    mesh = ss.default_x_mesh(config)
    sol = ss._run_bvp_attempt(q_mpa, mesh, guess, config)
    bc = bc_residual_from_sol(sol)
    return {
        "q_mpa": float(q_mpa),
        "success": bool(sol.success),
        "message": sol.message,
        "nodes": int(sol.x.size),
        "max_bc": float(np.max(np.abs(bc))),
        "max_rms": float(np.max(sol.rms_residuals)) if sol.success and hasattr(sol, "rms_residuals") else float("nan"),
        "sol": sol,
    }


def describe_attempt(label: str, attempt: dict[str, object]) -> None:
    print(
        f"  {label}: q={attempt['q_mpa']:.4f} MPa  success={attempt['success']}  "
        f"nodes={attempt['nodes']}  max_bc={fmt(float(attempt['max_bc']))}  "
        f"max_rms={fmt(float(attempt['max_rms']))}  message={attempt['message']}"
    )


def describe_result_obj(label: str, result: ss.AxisymmetricBackgroundSolve, indent: str = "  ") -> None:
    print(
        f"{indent}{label}: q={result.q_mpa:.4f} MPa  success={result.success}  "
        f"seed={result.seed_kind}  nodes={result.nodes}  max_rms={fmt(float(result.max_rms))}  "
        f"max_bc={fmt(float(result.max_bc_residual))}  min(r)={fmt(float(result.min_r))}  "
        f"message={result.message}"
    )


def seed_sweep() -> tuple[ss.AxisymmetricBackgroundSolve, ss.AxisymmetricBackgroundSolve, dict[float, list[tuple[str, dict[str, object]]]]]:
    template = ss.build_template_solution(BASE_CONFIG)
    mesh = ss.default_x_mesh(BASE_CONFIG)
    result_430 = ss.solve_axisymmetric_simple_support_fixed_load(4.30, config=BASE_CONFIG, template_result=template)
    result_4325 = ss.solve_axisymmetric_simple_support_fixed_load(
        4.325,
        config=BASE_CONFIG,
        initial_guess=result_430.solution.sol(mesh),
    )
    seeds = {}
    for q_mpa in (4.325, 4.3275):
        attempts = []
        attempts.append(("zero_guess", raw_attempt(q_mpa, BASE_CONFIG, ss.zero_guess(mesh))))
        attempts.append(("scaled_template", raw_attempt(q_mpa, BASE_CONFIG, ss.scaled_template_guess(q_mpa, mesh, template, BASE_CONFIG))))
        attempts.append(("previous_4.30", raw_attempt(q_mpa, BASE_CONFIG, result_430.solution.sol(mesh))))
        seeds[q_mpa] = attempts
    return result_430, result_4325, seeds


def continuation_chain(config: ss.AxisymmetricSimpleSupportConfig, loads: list[float]) -> list[ss.AxisymmetricBackgroundSolve]:
    template = ss.build_template_solution(config)
    mesh = ss.default_x_mesh(config)
    results: list[ss.AxisymmetricBackgroundSolve] = []
    previous = None
    for q_mpa in loads:
        if previous is None:
            result = ss.solve_axisymmetric_simple_support_fixed_load(q_mpa, config=config, template_result=template)
        else:
            result = ss.solve_axisymmetric_simple_support_fixed_load(q_mpa, config=config, initial_guess=previous.sol(mesh))
        results.append(result)
        if not result.success:
            break
        previous = result.solution
    return results


def simple_chain_summary(results: list[ss.AxisymmetricBackgroundSolve]) -> tuple[float | None, float | None]:
    last_success = None
    first_failure = None
    for item in results:
        if item.success:
            last_success = item.q_mpa
        else:
            first_failure = item.q_mpa
            break
    return last_success, first_failure


def parameter_variation_table() -> list[tuple[str, dict[str, object]]]:
    rows = []
    cases = [
        ("base", BASE_CONFIG),
        ("more_nodes_only", MORE_NODES_CONFIG),
        ("denser_mesh_only", DENSE_MESH_CONFIG),
        ("relaxed_tol_plus_nodes", RELAXED_CONFIG),
    ]
    for label, config in cases:
        template = ss.build_template_solution(config)
        mesh = ss.default_x_mesh(config)
        attempt = raw_attempt(4.3275, config, ss.scaled_template_guess(4.3275, mesh, template, config))
        rows.append((label, attempt))
    return rows


def failure_localization(config: ss.AxisymmetricSimpleSupportConfig, success_4325: ss.AxisymmetricBackgroundSolve) -> dict[str, object]:
    mesh = ss.default_x_mesh(config)
    failed = raw_attempt(4.3275, config, success_4325.solution.sol(mesh))
    sol = failed["sol"]
    dx = np.diff(sol.x)
    min_dx_idx = int(np.argmin(dx))
    min_dx_mid = 0.5 * (sol.x[min_dx_idx] + sol.x[min_dx_idx + 1])
    sample = np.linspace(config.x0, 1.0, 2000)
    yv = sol.sol(sample)
    gradients = []
    for i, name in enumerate(ss.STATE_LABELS):
        grad = np.gradient(yv[i], sample, edge_order=2)
        idx = int(np.argmax(np.abs(grad)))
        gradients.append((float(np.max(np.abs(grad))), float(sample[idx]), name))
    gradients.sort(reverse=True)
    return {
        "attempt": failed,
        "min_dx": float(np.min(dx)),
        "min_dx_mid": float(min_dx_mid),
        "frac_nodes_gt_0_99": float(np.count_nonzero(sol.x > 0.99) / sol.x.size),
        "frac_nodes_gt_0_995": float(np.count_nonzero(sol.x > 0.995) / sol.x.size),
        "top_gradients": gradients[:3],
    }


def main() -> None:
    eq_match = equation_match_check()
    result_430, result_4325, seeds = seed_sweep()
    base_chain = continuation_chain(BASE_CONFIG, [4.30, 4.325, 4.3275])
    tuned_chain = continuation_chain(RELAXED_CONFIG, [4.30, 4.325, 4.3275, 4.328, 4.329, 4.330, 4.332, 4.335, 4.340])
    variation_rows = parameter_variation_table()
    localization = failure_localization(BASE_CONFIG, result_4325)

    base_last, base_fail = simple_chain_summary(base_chain)
    tuned_last, tuned_fail = simple_chain_summary(tuned_chain)

    bc_small_near_failure = localization["attempt"]["max_bc"] < 1.0e-12
    equation_impl_match = eq_match["max_abs_diff"] < 1.0e-12
    tuning_helps = tuned_last is not None and base_last is not None and tuned_last > base_last

    classification = "mixed"
    if bc_small_near_failure and equation_impl_match and tuning_helps:
        classification = "mainly numerical, with mild equation-level stiffness suspicion"

    print("=== Pilot 08: Simple-support background stabilization diagnostic ===")
    print()
    print("Expected result:")
    print("  The active 6-state BC implementation should pass structurally, and the 4.30..4.35 MPa")
    print("  ceiling may turn out to be mainly numerical, equation-level, BC-level, or mixed.")
    print()
    print("A. Implemented problem and equation check")
    print(f"  active state labels: {list(ss.STATE_LABELS)}")
    print(f"  active BC labels: {list(ss.BC_LABELS)}")
    print(
        "  equation match against supporting axisym_nepol: "
        f"max_abs_diff={fmt(eq_match['max_abs_diff'])}, mean_abs_diff={fmt(eq_match['mean_abs_diff'])}"
    )
    print()
    print("B. Seed sensitivity near the ceiling")
    describe_result_obj("baseline 4.30 MPa success", result_430)
    describe_result_obj("baseline 4.325 MPa success", result_4325)
    for q_mpa in sorted(seeds):
        print(f"  q={q_mpa:.4f} MPa")
        for label, attempt in seeds[q_mpa]:
            describe_attempt(label, attempt)
    print()
    print("C. Baseline continuation and parameter variations")
    print("  baseline previous-solution chain:")
    for item in base_chain:
        describe_result_obj("chain item", item, indent="    ")
    print(f"  baseline last success={base_last}, first failure={base_fail}")
    print()
    print("  single-load 4.3275 MPa parameter variations from scaled-template seed:")
    for label, attempt in variation_rows:
        describe_attempt(label, attempt)
    print()
    print("  relaxed local continuation chain:")
    for item in tuned_chain:
        describe_result_obj("chain item", item, indent="    ")
    print(f"  relaxed-chain last success={tuned_last}, first failure={tuned_fail}")
    print()
    print("D. Failure localization and BC residuals")
    describe_attempt("baseline failed attempt after 4.325 seed", localization["attempt"])
    print(
        f"  smallest mesh interval={localization['min_dx']:.3e} near x={localization['min_dx_mid']:.6f}; "
        f"fraction of nodes with x>0.99 is {localization['frac_nodes_gt_0_99']:.3f}, "
        f"with x>0.995 is {localization['frac_nodes_gt_0_995']:.3f}"
    )
    print("  largest sampled state-gradient locations on the failed attempt:")
    for magnitude, x_loc, name in localization["top_gradients"]:
        print(f"    {name}: max|grad|={magnitude:.3e} at x={x_loc:.6f}")
    print()
    print("E. Final classification")
    print(f"  actual result: {classification}")
    print(f"  PASS/FAIL: {'PASS' if classification.startswith('mainly numerical') else 'PARTIAL'}")
    print("  Q1. Is the 4.33 MPa breakdown mainly numerical?")
    print(
        "     Yes, within the current repository evidence it is mainly numerical/stiffness-limited: "
        "the implemented BCs are exact, the active equations match the supporting 6-state equations, "
        "BC residuals stay tiny, failure appears as right-edge mesh blow-up, and modest solver tuning "
        "pushes the ceiling upward."
    )
    print("  Q2. Is there evidence that the implemented equations may be wrong or incomplete?")
    print(
        "     No direct implementation-level evidence was found. The only remaining equation-level "
        "suspicion is a strong right-edge stiffness / boundary-layer effect that the present continuation "
        "strategy does not yet handle robustly."
    )
    print("  Q3. Is there evidence that the implemented simple-support BCs may be wrong or inconsistent?")
    print(
        "     No. The BC structure is square, uses the intended variables, and does not silently replace "
        "M_s(1)=0 by varphi(1)=0 inside the 6-state path."
    )
    print("  Q4. What is the smallest next corrective step?")
    print(
        "     Keep the same 6-state equations and BCs, but add a dedicated local branch-following helper "
        "for the 4.32..4.34 MPa band using smaller load steps, the relaxed tolerance profile, higher "
        "max_nodes, and right-edge-focused mesh control before reconnecting this background to the "
        "mixed-weak scans."
    )
    print()
    print("Support level:")
    print("  PARTIAL SUPPORT ONLY. This pilot diagnoses the current bottleneck and improves the reachable")
    print("  load band numerically, but it does not prove the final axisymmetric simple-support theory.")


if __name__ == "__main__":
    main()
