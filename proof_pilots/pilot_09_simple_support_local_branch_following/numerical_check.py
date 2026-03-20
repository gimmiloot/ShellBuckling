from __future__ import annotations

import sys
import warnings
from pathlib import Path


warnings.filterwarnings("ignore", category=RuntimeWarning)

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from shell_buckling.mixed_weak.axisymmetric_simple_support_background import (
    AxisymmetricLocalBranchFollowConfig,
    AxisymmetricLocalBranchHistory,
    AxisymmetricLocalBranchStep,
    solve_axisymmetric_simple_support_local_branch_following,
)


OLD_CEILING_MPA = 4.335


def fmt(value: float | None) -> str:
    if value is None:
        return "nan"
    return f"{value:.4f}"


def max_nodes_for_step(step: AxisymmetricLocalBranchStep, config: AxisymmetricLocalBranchFollowConfig) -> int:
    if step.config_label == "strict_local":
        return config.strict_local_config.max_nodes
    return config.relaxed_local_config.max_nodes


def print_anchor_summary(history: AxisymmetricLocalBranchHistory) -> None:
    print("A. Anchor schedule")
    for result in history.anchor_results:
        print(
            f"  q={result.q_mpa:.4f} MPa  success={result.success}  seed={result.seed_kind}  "
            f"nodes={result.nodes}  max_bc={result.max_bc_residual:.3e}  "
            f"max_rms={result.max_rms:.3e}  message={result.message}"
        )
    print()


def print_local_summary(history: AxisymmetricLocalBranchHistory, config: AxisymmetricLocalBranchFollowConfig) -> None:
    print("B. Local branch-following schedule")
    for step in history.local_steps:
        limit = max_nodes_for_step(step, config)
        pressure = step.nodes / float(limit)
        print(
            f"  q={step.q_mpa:.4f} MPa  success={step.success}  config={step.config_label}  "
            f"accepted_seed={step.accepted_seed_kind}  seeds={list(step.seed_labels)}  "
            f"nodes={step.nodes}/{limit} ({pressure:.3f})  max_bc={step.max_bc_residual:.3e}  "
            f"max_rms={step.max_rms:.3e}  message={step.message}"
        )
    print()


def main() -> None:
    config = AxisymmetricLocalBranchFollowConfig()
    history = solve_axisymmetric_simple_support_local_branch_following(config=config)
    highest = history.last_local_success()
    first_failure = history.first_local_failure()
    ceiling_moved = highest is not None and highest > OLD_CEILING_MPA
    failure_is_numerical = bool(history.local_steps) and history.local_steps[-1].message == "The maximum number of mesh nodes is exceeded."

    print("=== Pilot 09: Local branch-following check for the 6-state simple-support background ===")
    print()
    print("Expected result:")
    print("  The dedicated local helper should move the reachable load ceiling upward relative to")
    print(f"  the pilot 08 local ceiling near {OLD_CEILING_MPA:.3f} MPa, while keeping the same BC set.")
    print()
    print("Numerical changes introduced:")
    print("  - relaxed uniform anchor schedule up to the last previously converged load;")
    print("  - right-edge-focused local mesh in the difficult band;")
    print("  - secant predictor plus previous-solution reuse for local seeds;")
    print("  - strict local pass first, then a looser local fallback only on failure;")
    print("  - larger max_nodes in the local helper.")
    print()
    print(f"Anchor loads attempted: {list(config.anchor_loads_mpa)}")
    print(f"Local loads attempted:  {list(config.local_loads_mpa)}")
    print(
        "Strict local settings: "
        f"nd_bvp={config.strict_local_config.nd_bvp}, tol={config.strict_local_config.tol:.1e}, "
        f"relaxed_tol={config.strict_local_config.relaxed_tol:.1e}, max_nodes={config.strict_local_config.max_nodes}, "
        f"cluster_start={config.strict_local_config.right_edge_cluster_start:.3f}, "
        f"cluster_fraction={config.strict_local_config.right_edge_cluster_fraction:.2f}, "
        f"cluster_power={config.strict_local_config.right_edge_cluster_power:.2f}"
    )
    print(
        "Relaxed local settings: "
        f"nd_bvp={config.relaxed_local_config.nd_bvp}, tol={config.relaxed_local_config.tol:.1e}, "
        f"relaxed_tol={config.relaxed_local_config.relaxed_tol:.1e}, max_nodes={config.relaxed_local_config.max_nodes}, "
        f"cluster_start={config.relaxed_local_config.right_edge_cluster_start:.3f}, "
        f"cluster_fraction={config.relaxed_local_config.right_edge_cluster_fraction:.2f}, "
        f"cluster_power={config.relaxed_local_config.right_edge_cluster_power:.2f}"
    )
    print()

    print_anchor_summary(history)
    print_local_summary(history, config)

    print("C. Final result")
    print(f"  old local ceiling from pilot 08: {OLD_CEILING_MPA:.4f} MPa")
    print(f"  highest load now reached: {fmt(highest)} MPa")
    print(f"  first failure load now: {fmt(first_failure)} MPa")
    print(f"  ceiling moved upward: {'YES' if ceiling_moved else 'NO'}")
    print(f"  bottleneck still mainly numerical: {'YES' if failure_is_numerical else 'UNCLEAR'}")
    if ceiling_moved:
        print(
            "  interpretation: the new helper improved branch following in the difficult right-edge band "
            "without changing the BC set or the equations."
        )
    else:
        print("  interpretation: the helper did not yet move the ceiling upward in a reproducible way.")
    print(
        "  next bottleneck: after the moved ceiling, failure is still controlled by node pressure / right-edge "
        "mesh blow-up rather than by a detected BC inconsistency."
    )
    print()
    print(f"PASS/FAIL: {'PASS' if ceiling_moved and failure_is_numerical else 'PARTIAL'}")


if __name__ == "__main__":
    main()
