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
    parser.add_argument("--failure-probe-step-mpa", type=float)
    parser.add_argument("--failure-probe-step-factor", type=float, default=runtime.DEFAULT_FAILURE_PROBE_STEP_FACTOR)
    parser.add_argument("--failure-probe-min-step-mpa", type=float, default=runtime.DEFAULT_FAILURE_PROBE_MIN_STEP_MPA)
    parser.add_argument("--failure-probe-high-load-step-mpa", type=float, default=runtime.DEFAULT_FAILURE_PROBE_HIGH_LOAD_STEP_MPA)
    parser.add_argument("--failure-probe-high-load-threshold-mpa", type=float, default=runtime.DEFAULT_FAILURE_PROBE_HIGH_LOAD_THRESHOLD_MPA)
    parser.add_argument("--failure-probe-count", type=int, default=2)
    parser.add_argument("--output-json", type=Path)
    return parser.parse_args()


def load_step_point(run_dir: Path, accepted_steps: list[dict[str, Any]], index: int):
    runtime.ensure_step_checkpoint_available(run_dir, accepted_steps[index])
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
        accepted_step = accepted_steps[step_index]
        accepted_point = load_step_point(run_dir, accepted_steps, step_index)
        accepted_point_summary = runtime.pilot21.point_summary(accepted_point)
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

        accepted_step_mpa = runtime.float_or_none(accepted_step.get("step_size_mpa"))
        probe_step_mpa = runtime.choose_failure_probe_step(
            load_mpa=float(q_target_mpa),
            accepted_step_mpa=accepted_step_mpa,
            explicit_step_mpa=runtime.float_or_none(args.failure_probe_step_mpa),
            step_factor=float(args.failure_probe_step_factor),
            min_step_mpa=float(args.failure_probe_min_step_mpa),
            high_load_step_mpa=float(args.failure_probe_high_load_step_mpa),
            high_load_threshold_mpa=float(args.failure_probe_high_load_threshold_mpa),
        )
        failure_probe = sequential_failure_probe(
            profile=profile,
            scaled_anchor_point=scaled_anchor_point,
            older_point=retest_predecessor,
            previous_point=accepted_point,
            step_mpa=probe_step_mpa,
            count=int(args.failure_probe_count),
        )

        results.append(
            {
                "q_mpa": float(q_target_mpa),
                "step_index": step_index,
                "accepted_step_mpa": accepted_step_mpa,
                "accepted_point": accepted_point_summary,
                "repeat_point": None if repeat_point is None else runtime.pilot21.point_summary(repeat_point),
                "repeat_attempts": repeat_attempts,
                "reproducibility": repeat_assessment,
                "strict_reproducible": runtime.strict_reproducible(repeat_assessment),
                "near_reproducible": runtime.near_reproducible(repeat_assessment),
                "continuity": continuity,
                "branch_jump_suspicion": False if continuity is None else bool(continuity.get("branch_jump_suspicion")),
                "failure_probe_step_mpa": probe_step_mpa,
                "failure_probe": failure_probe,
                "strongest_gradient_order": runtime.pilot21.strongest_states(accepted_point_summary),
            }
        )

    runtime.annotate_repeat_drift_smoothness(results)
    for item in results:
        strongest_gradient_order = list(item.get("strongest_gradient_order") or [])
        same_branch = runtime.same_branch_indicators(
            accepted_point_summary=item["accepted_point"],
            repeat_assessment=item.get("reproducibility"),
            continuity=item.get("continuity"),
            strongest_gradient_order=strongest_gradient_order,
            repeat_drift_smooth=item.get("repeat_drift_smooth"),
            repeat_drift_smoothness=item.get("repeat_drift_smoothness"),
        )
        promotion_policy = runtime.promotion_policy_assessment(
            strict_reproducible_flag=bool(item.get("strict_reproducible")),
            near_reproducible_flag=bool(item.get("near_reproducible")),
            same_branch=same_branch,
            failure_probe=list(item.get("failure_probe") or []),
        )
        item["same_branch_indicators"] = same_branch
        item["promotion_policy"] = promotion_policy

    payload = {
        "metadata": {
            "runner": "pilot_21_confirm_u_z_scaled_arc_like_continuation",
            "workflow": runtime.STATUS_CONVENTION["preferred_workflow"],
            "same_equations_as_active_6_state_path": True,
            "same_simple_support_bcs": True,
            "status_convention": runtime.STATUS_CONVENTION,
            "audit_policy": runtime.audit_policy_summary(),
            "source_progress": str(progress_path),
            "profile": runtime.profile_summary(profile),
            "failure_probe_step_mpa": runtime.float_or_none(args.failure_probe_step_mpa),
            "failure_probe_step_factor": float(args.failure_probe_step_factor),
            "failure_probe_min_step_mpa": float(args.failure_probe_min_step_mpa),
            "failure_probe_high_load_step_mpa": float(args.failure_probe_high_load_step_mpa),
            "failure_probe_high_load_threshold_mpa": float(args.failure_probe_high_load_threshold_mpa),
            "failure_probe_count": int(args.failure_probe_count),
        },
        "results": results,
    }
    if args.output_json is None:
        output_path = run_dir / runtime.DEFAULT_CONFIRM_JSON.name
    else:
        output_path = args.output_json.resolve() if not args.output_json.is_absolute() else args.output_json
    runtime.save_json(output_path, payload)

    print("=== Pilot 21 confirm runner ===")
    for item in results:
        failure_probe = item.get("failure_probe") or []
        first_probe_failure = next((probe.get("q_target_mpa") for probe in failure_probe if not probe.get("success")), None)
        same_branch = item.get("same_branch_indicators") or {}
        promotion = item.get("promotion_policy") or {}
        print(
            f"q={item['q_mpa']:.4f} MPa: strict_repro={item.get('strict_reproducible')}, "
            f"near_repro={item.get('near_reproducible')}, branch_jump={item['branch_jump_suspicion']}, "
            f"same_branch={same_branch.get('overall_same_branch_signal')}, "
            f"classification={promotion.get('classification')}, first_probe_failure={first_probe_failure}"
        )
    print(f"Saved confirm results to: {output_path}")


if __name__ == "__main__":
    main()
