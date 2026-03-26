from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import continuation_runtime as runtime


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Pointwise confirm/audit runner for fast pilot-21 checkpoints. "
            "It reruns selected milestone loads, checks continuity, and probes a small failure neighborhood."
        )
    )
    parser.add_argument("--run-dir", type=Path, default=runtime.FAST_RUN_DIR)
    parser.add_argument("--load-mpa", dest="loads_mpa", action="append", type=float)
    parser.add_argument("--failure-probe-step-mpa", type=float, default=0.002)
    parser.add_argument("--failure-probe-count", type=int, default=2)
    parser.add_argument("--output-json", type=Path, default=runtime.DEFAULT_CONFIRM_JSON)
    return parser.parse_args()


def load_step_point(run_dir: Path, accepted_steps: list[dict[str, Any]], index: int):
    return runtime.load_point_checkpoint(run_dir, accepted_steps[index]["checkpoint"])


def predecessor_for_retest(progress: dict[str, Any], run_dir: Path, step_index: int):
    accepted_steps = progress.get("accepted_steps") or []
    if step_index >= 1:
        return load_step_point(run_dir, accepted_steps, step_index - 1)
    bootstrap_previous = (progress.get("checkpoints") or {}).get("bootstrap_previous_checkpoint")
    if bootstrap_previous is None:
        raise RuntimeError("Missing bootstrap_previous_checkpoint in fast progress payload.")
    return runtime.load_point_checkpoint(run_dir, bootstrap_previous)


def older_for_continuity(progress: dict[str, Any], run_dir: Path, step_index: int):
    accepted_steps = progress.get("accepted_steps") or []
    if step_index >= 2:
        return load_step_point(run_dir, accepted_steps, step_index - 2)
    if step_index == 1:
        bootstrap_previous = (progress.get("checkpoints") or {}).get("bootstrap_previous_checkpoint")
        if bootstrap_previous is None:
            return None
        return runtime.load_point_checkpoint(run_dir, bootstrap_previous)
    return None


def sequential_failure_probe(
    *,
    profile,
    scaled_anchor_point,
    older_point,
    previous_point,
    step_mpa: float,
    count: int,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    local_older = older_point
    local_previous = previous_point
    for _ in range(max(0, int(count))):
        q_trial = round(float(local_previous.q_mpa + step_mpa), 7)
        point, attempts = runtime.pilot20.try_scaled_attempts(
            q_trial,
            runtime.pilot20.scaled_seed_specs(
                q_trial,
                local_older,
                local_previous,
                scaled_anchor_point,
                profile,
                runtime.pilot20.U_Z_SCALE,
            ),
            profile,
            runtime.pilot20.U_Z_SCALE,
        )
        attempt_payload = [runtime.pilot21.attempt_summary(item) for item in attempts]
        entry = {
            "q_target_mpa": q_trial,
            "success": point is not None,
            "attempt_count": len(attempts),
            "attempts": [runtime.compact_attempt_summary(item) for item in attempt_payload],
            "accepted_point": None if point is None else runtime.pilot21.point_summary(point),
        }
        results.append(entry)
        if point is None:
            break
        local_older, local_previous = local_previous, point
    return results


def near_reproducible(repeat_assessment: dict[str, Any]) -> bool:
    delta = (repeat_assessment or {}).get("solution_delta") or {}
    max_rel_l2 = runtime.float_or_none(delta.get("max_rel_l2"))
    max_rel_max = runtime.float_or_none(delta.get("max_rel_max"))
    return (
        bool((repeat_assessment or {}).get("same_accepted_seed"))
        and max_rel_l2 is not None
        and max_rel_max is not None
        and max_rel_l2 <= 2.0e-5
        and max_rel_max <= 2.0e-4
    )


def main() -> None:
    args = parse_args()
    run_dir = args.run_dir.resolve()
    progress_path = run_dir / runtime.DEFAULT_PROGRESS_JSON.name
    progress = runtime.load_json(progress_path)
    if progress is None:
        raise RuntimeError(f"Missing fast progress file: {progress_path}")

    profile = runtime.profile_from_metadata(progress["metadata"]["profile"])
    x_grid = runtime.pilot12.build_comparison_grid(profile.config)
    scaled_anchor_path = (progress.get("checkpoints") or {}).get("scaled_anchor_checkpoint")
    if scaled_anchor_path is None:
        raise RuntimeError("Missing scaled_anchor_checkpoint in fast progress payload.")
    scaled_anchor_point = runtime.load_point_checkpoint(run_dir, scaled_anchor_path)

    requested_loads = args.loads_mpa
    if not requested_loads:
        requested_loads = list((progress.get("summary") or {}).get("suggested_confirm_loads_mpa") or [])
    if not requested_loads:
        highest_q = runtime.current_highest_q(progress)
        if highest_q is not None:
            requested_loads = [highest_q]
    if not requested_loads:
        raise RuntimeError("No accepted loads are available for confirm mode.")

    accepted_steps = progress.get("accepted_steps") or []
    results: list[dict[str, Any]] = []
    for q_target_mpa in requested_loads:
        step_index = runtime.find_step_index(progress, float(q_target_mpa))
        accepted_point = load_step_point(run_dir, accepted_steps, step_index)
        retest_predecessor = predecessor_for_retest(progress, run_dir, step_index)
        continuity_older = older_for_continuity(progress, run_dir, step_index)

        repeat_point, repeat_attempts, repeat_assessment = runtime.pilot21.run_retest(
            accepted_point,
            retest_predecessor,
            scaled_anchor_point,
            profile,
            x_grid,
        )
        continuity = None
        if step_index >= 1 and continuity_older is not None:
            continuity = runtime.pilot12.continuity_assessment(
                accepted_point,
                retest_predecessor,
                continuity_older,
                x_grid,
            )

        failure_probe = sequential_failure_probe(
            profile=profile,
            scaled_anchor_point=scaled_anchor_point,
            older_point=retest_predecessor,
            previous_point=accepted_point,
            step_mpa=float(args.failure_probe_step_mpa),
            count=int(args.failure_probe_count),
        )

        results.append(
            {
                "q_mpa": float(q_target_mpa),
                "step_index": step_index,
                "accepted_point": runtime.pilot21.point_summary(accepted_point),
                "repeat_point": None if repeat_point is None else runtime.pilot21.point_summary(repeat_point),
                "repeat_attempts": repeat_attempts,
                "reproducibility": repeat_assessment,
                "strict_reproducible": bool(repeat_assessment.get("reproducible")),
                "near_reproducible": near_reproducible(repeat_assessment),
                "continuity": continuity,
                "branch_jump_suspicion": False if continuity is None else bool(continuity.get("branch_jump_suspicion")),
                "failure_probe": failure_probe,
                "strongest_gradient_order": runtime.pilot21.strongest_states(runtime.pilot21.point_summary(accepted_point)),
            }
        )

    payload = {
        "metadata": {
            "runner": "pilot_21_confirm_u_z_scaled_arc_like_continuation",
            "workflow": runtime.STATUS_CONVENTION["preferred_workflow"],
            "same_equations_as_active_6_state_path": True,
            "same_simple_support_bcs": True,
            "status_convention": runtime.STATUS_CONVENTION,
            "source_progress": str(progress_path),
            "profile": runtime.profile_summary(profile),
            "failure_probe_step_mpa": float(args.failure_probe_step_mpa),
            "failure_probe_count": int(args.failure_probe_count),
        },
        "results": results,
    }
    output_path = args.output_json.resolve() if not args.output_json.is_absolute() else args.output_json
    runtime.save_json(output_path, payload)

    print("=== Pilot 21 confirm runner ===")
    for item in results:
        repro = item.get("reproducibility") or {}
        failure_probe = item.get("failure_probe") or []
        first_probe_failure = next((probe.get("q_target_mpa") for probe in failure_probe if not probe.get("success")), None)
        print(
            f"q={item['q_mpa']:.4f} MPa: strict_repro={item.get('strict_reproducible')}, "
            f"near_repro={item.get('near_reproducible')}, branch_jump={item['branch_jump_suspicion']}, "
            f"first_probe_failure={first_probe_failure}"
        )
    print(f"Saved confirm results to: {output_path}")


if __name__ == "__main__":
    main()
