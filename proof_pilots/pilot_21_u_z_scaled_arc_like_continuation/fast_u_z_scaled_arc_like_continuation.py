from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Any

import continuation_runtime as runtime


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fast resumable continuation for the separate 6-state simple-support path "
            "using the pilot-20 u_z-scaled formulation with bounded arc-like step adaptation."
        )
    )
    parser.add_argument("--target-load-mpa", type=float, default=4.50)
    parser.add_argument("--bootstrap-target-mpa", type=float, default=runtime.DEFAULT_BOOTSTRAP_TARGET_MPA)
    parser.add_argument("--initial-step-mpa", type=float, default=runtime.pilot21.INITIAL_STEP_MPA)
    parser.add_argument("--min-step-mpa", type=float, default=runtime.pilot21.MIN_STEP_MPA)
    parser.add_argument("--max-step-mpa", type=float, default=runtime.pilot21.MAX_STEP_MPA)
    parser.add_argument("--failure-shrink", type=float, default=runtime.pilot21.FAILURE_SHRINK)
    parser.add_argument("--max-new-steps", type=int, default=200)
    parser.add_argument("--max-runtime-seconds", type=float, default=3600.0)
    parser.add_argument("--run-dir", type=Path, default=runtime.FAST_RUN_DIR)
    return parser.parse_args()


def compact_attempts(attempts: list[Any]) -> list[dict[str, Any]]:
    return [runtime.compact_attempt_summary(runtime.pilot21.attempt_summary(item)) for item in attempts]


def build_progress_payload(run_dir: Path, target_load_mpa: float, bootstrap_target_mpa: float, profile) -> dict[str, Any]:
    return {
        "metadata": {
            "runner": "pilot_21_fast_u_z_scaled_arc_like_continuation",
            "goal": "fast resumable continuation for the separate 6-state simple-support background path",
            "workflow": runtime.STATUS_CONVENTION["preferred_workflow"],
            "same_equations_as_active_6_state_path": True,
            "same_simple_support_bcs": True,
            "status_convention": runtime.STATUS_CONVENTION,
            "target_load_mpa": float(target_load_mpa),
            "bootstrap_target_mpa": float(bootstrap_target_mpa),
            "profile": runtime.profile_summary(profile),
            "step_control": {},
            "run_dir": str(run_dir),
        },
        "bootstrap": {},
        "checkpoints": {},
        "state": {
            "status": "initialized",
            "current_load_mpa": None,
            "current_step_size_mpa": None,
            "resume_older_checkpoint": None,
            "resume_previous_checkpoint": None,
            "terminal_failure_q_mpa": None,
        },
        "accepted_steps": [],
        "failure_events": [],
        "summary": {},
    }


def record_accepted_step(
    *,
    progress: dict[str, Any],
    run_dir: Path,
    progress_path: Path,
    log_path: Path,
    point,
    attempts: list[Any],
    q_target_mpa: float,
    step_size_mpa: float,
    older_checkpoint_rel: Path,
    next_step_mpa: float,
    stage: str,
    elapsed_seconds: float,
) -> Path:
    step_index = len(progress["accepted_steps"])
    checkpoint_rel = runtime.save_point_checkpoint(run_dir, step_index, point)
    point_payload = runtime.pilot21.point_summary(point)
    entry = {
        "index": step_index,
        "stage": stage,
        "q_mpa": float(point.q_mpa),
        "q_target_mpa": float(q_target_mpa),
        "step_size_mpa": float(step_size_mpa),
        "checkpoint": str(checkpoint_rel).replace("\\", "/"),
        "accepted_point": runtime.compact_point_summary(point_payload),
        "attempt_count": len(attempts),
        "attempts": compact_attempts(attempts),
        "strongest_gradient_order": runtime.pilot21.strongest_states(point_payload),
        "elapsed_seconds": float(elapsed_seconds),
    }
    progress["accepted_steps"].append(entry)
    if not progress["checkpoints"].get("scaled_anchor_checkpoint"):
        progress["checkpoints"]["scaled_anchor_checkpoint"] = str(checkpoint_rel).replace("\\", "/")
    progress["state"]["status"] = "running"
    progress["state"]["current_load_mpa"] = float(point.q_mpa)
    progress["state"]["current_step_size_mpa"] = float(next_step_mpa)
    progress["state"]["resume_older_checkpoint"] = str(older_checkpoint_rel).replace("\\", "/")
    progress["state"]["resume_previous_checkpoint"] = str(checkpoint_rel).replace("\\", "/")
    runtime.refresh_progress_summary(progress)
    runtime.save_json(progress_path, progress)
    runtime.append_jsonl(
        log_path,
        {
            "event": "accepted",
            "stage": stage,
            "q_mpa": float(point.q_mpa),
            "q_target_mpa": float(q_target_mpa),
            "step_size_mpa": float(step_size_mpa),
            "attempt_count": len(attempts),
            "checkpoint": str(checkpoint_rel).replace("\\", "/"),
            "accepted_seed": point_payload.get("accepted_seed"),
            "node_pressure": point_payload.get("node_pressure"),
            "right_edge_fraction_0_995": point_payload.get("right_edge_fraction_0_995"),
            "strongest_gradient_order": runtime.pilot21.strongest_states(point_payload),
            "elapsed_seconds": float(elapsed_seconds),
        },
    )
    return checkpoint_rel


def record_failure_event(
    *,
    progress: dict[str, Any],
    progress_path: Path,
    log_path: Path,
    attempts: list[Any],
    q_target_mpa: float,
    step_size_mpa: float,
    next_step_mpa: float,
    stage: str,
    elapsed_seconds: float,
    terminal: bool,
) -> None:
    attempt_payload = compact_attempts(attempts)
    failed_summary = attempt_payload[0] if attempt_payload else None
    event = {
        "stage": stage,
        "q_target_mpa": float(q_target_mpa),
        "step_size_mpa": float(step_size_mpa),
        "next_step_mpa": float(next_step_mpa),
        "attempt_count": len(attempts),
        "attempts": attempt_payload,
        "terminal": bool(terminal),
        "elapsed_seconds": float(elapsed_seconds),
    }
    progress["failure_events"].append(event)
    progress["state"]["current_step_size_mpa"] = float(next_step_mpa)
    if terminal:
        progress["state"]["terminal_failure_q_mpa"] = float(q_target_mpa)
    runtime.refresh_progress_summary(progress)
    runtime.save_json(progress_path, progress)
    runtime.append_jsonl(
        log_path,
        {
            "event": "failure",
            "stage": stage,
            "q_target_mpa": float(q_target_mpa),
            "step_size_mpa": float(step_size_mpa),
            "next_step_mpa": float(next_step_mpa),
            "terminal": bool(terminal),
            "message": None if failed_summary is None else failed_summary.get("message"),
            "seed_label": None if failed_summary is None else failed_summary.get("seed_label"),
            "elapsed_seconds": float(elapsed_seconds),
        },
    )


def maybe_stop(invocation_start: float, args: argparse.Namespace, accepted_new_steps: int) -> str | None:
    if accepted_new_steps >= int(args.max_new_steps):
        return "paused_after_max_new_steps"
    if time.perf_counter() - invocation_start >= float(args.max_runtime_seconds):
        return "paused_after_runtime_budget"
    return None


def bootstrap_if_needed(
    *,
    args: argparse.Namespace,
    run_dir: Path,
    progress: dict[str, Any],
    progress_path: Path,
    log_path: Path,
    invocation_start: float,
) -> tuple[Any, Any, Any, float, Any]:
    if progress["accepted_steps"]:
        profile = runtime.profile_from_metadata(progress["metadata"]["profile"])
        scaled_anchor, older_point, previous_point = runtime.load_resume_points(progress, run_dir)
        return scaled_anchor, older_point, previous_point, float(progress["state"]["current_step_size_mpa"]), profile

    context = runtime.pilot20.build_context()
    profile = runtime.pilot21.continuation_profile(context)
    progress["metadata"]["profile"] = runtime.profile_summary(profile)
    progress["metadata"]["step_control"] = {
        "initial_step_mpa": float(args.initial_step_mpa),
        "min_step_mpa": float(args.min_step_mpa),
        "max_step_mpa": float(args.max_step_mpa),
        "failure_shrink": float(args.failure_shrink),
        "adapt_rule": "pilot21.adapt_step_size on success, shrink on failure",
    }
    progress["bootstrap"] = {
        "bootstrap_elapsed_seconds": context.get("bootstrap_elapsed_seconds"),
        "bootstrap_payload": context.get("bootstrap_payload"),
        "reproduced_old_anchor_4_3434": runtime.compact_point_summary(runtime.pilot21.point_summary(context["point_43434"])),
    }
    runtime.save_json(progress_path, progress)

    older_point = context["branch_points"][4.3432]
    previous_point = context["branch_points"][4.3433]
    local_anchor = context["local_anchor"]
    previous_checkpoint_rel = runtime.save_named_point_checkpoint(run_dir, "bootstrap_previous_4p3433_mpa.npz", previous_point)
    progress["checkpoints"]["bootstrap_previous_checkpoint"] = str(previous_checkpoint_rel).replace("\\", "/")
    runtime.save_json(progress_path, progress)

    scaled_anchor_point = None
    step_mpa = float(args.initial_step_mpa)
    warmup_limit = min(float(args.target_load_mpa), float(args.bootstrap_target_mpa), float(runtime.pilot21.PILOT20_BEST_BOUNDED_CEILING_MPA))

    for q_target_mpa in runtime.pilot21.PILOT20_WARMUP_LOADS_MPA:
        if q_target_mpa > warmup_limit + 1.0e-12:
            break
        anchor_for_step = local_anchor if scaled_anchor_point is None else scaled_anchor_point
        point, attempts = runtime.pilot20.try_scaled_attempts(
            q_target_mpa,
            runtime.pilot20.scaled_seed_specs(
                q_target_mpa,
                older_point,
                previous_point,
                anchor_for_step,
                profile,
                runtime.pilot20.U_Z_SCALE,
            ),
            profile,
            runtime.pilot20.U_Z_SCALE,
        )
        elapsed = time.perf_counter() - invocation_start
        if point is None:
            next_step = max(float(args.min_step_mpa), float(q_target_mpa - previous_point.q_mpa) * float(args.failure_shrink))
            record_failure_event(
                progress=progress,
                progress_path=progress_path,
                log_path=log_path,
                attempts=attempts,
                q_target_mpa=q_target_mpa,
                step_size_mpa=float(q_target_mpa - previous_point.q_mpa),
                next_step_mpa=next_step,
                stage="bootstrap_warmup",
                elapsed_seconds=elapsed,
                terminal=True,
            )
            progress["state"]["status"] = "stopped_during_bootstrap_warmup"
            runtime.save_json(progress_path, progress)
            raise RuntimeError(f"Bootstrap warmup failed at {q_target_mpa:.4f} MPa.")

        step_mpa = max(float(args.initial_step_mpa), float(point.q_mpa - previous_point.q_mpa))
        checkpoint_rel = record_accepted_step(
            progress=progress,
            run_dir=run_dir,
            progress_path=progress_path,
            log_path=log_path,
            point=point,
            attempts=attempts,
            q_target_mpa=q_target_mpa,
            step_size_mpa=float(q_target_mpa - previous_point.q_mpa),
            older_checkpoint_rel=previous_checkpoint_rel,
            next_step_mpa=step_mpa,
            stage="bootstrap_warmup",
            elapsed_seconds=elapsed,
        )
        if scaled_anchor_point is None:
            scaled_anchor_point = point
            progress["checkpoints"]["scaled_anchor_checkpoint"] = str(checkpoint_rel).replace("\\", "/")
            runtime.save_json(progress_path, progress)
        older_point, previous_point = previous_point, point
        previous_checkpoint_rel = checkpoint_rel
        stop_reason = maybe_stop(invocation_start, args, 0)
        if stop_reason is not None and previous_point.q_mpa < min(float(args.target_load_mpa), float(args.bootstrap_target_mpa)) - 1.0e-12:
            progress["state"]["status"] = stop_reason
            runtime.save_json(progress_path, progress)
            return scaled_anchor_point, older_point, previous_point, step_mpa, profile

    if scaled_anchor_point is None:
        raise RuntimeError("Bootstrap did not reach the first scaled anchor at 4.3434 MPa.")

    bootstrap_target = min(float(args.target_load_mpa), float(args.bootstrap_target_mpa))
    accepted_new_steps = 0
    while previous_point.q_mpa < bootstrap_target - 1.0e-12:
        raw_step = min(step_mpa, float(bootstrap_target - previous_point.q_mpa))
        q_trial = round(float(previous_point.q_mpa + raw_step), 7)
        point, attempts = runtime.pilot20.try_scaled_attempts(
            q_trial,
            runtime.pilot20.scaled_seed_specs(
                q_trial,
                older_point,
                previous_point,
                scaled_anchor_point,
                profile,
                runtime.pilot20.U_Z_SCALE,
            ),
            profile,
            runtime.pilot20.U_Z_SCALE,
        )
        elapsed = time.perf_counter() - invocation_start
        if point is None:
            step_mpa = max(float(args.min_step_mpa), float(raw_step) * float(args.failure_shrink))
            terminal = raw_step <= float(args.min_step_mpa) + 1.0e-12
            record_failure_event(
                progress=progress,
                progress_path=progress_path,
                log_path=log_path,
                attempts=attempts,
                q_target_mpa=q_trial,
                step_size_mpa=raw_step,
                next_step_mpa=step_mpa,
                stage="bootstrap_extension",
                elapsed_seconds=elapsed,
                terminal=terminal,
            )
            if terminal:
                progress["state"]["status"] = "stopped_during_bootstrap_extension"
                runtime.save_json(progress_path, progress)
                return scaled_anchor_point, older_point, previous_point, step_mpa, profile
            continue

        step_mpa = min(float(args.max_step_mpa), float(runtime.pilot21.adapt_step_size(raw_step, point)))
        checkpoint_rel = record_accepted_step(
            progress=progress,
            run_dir=run_dir,
            progress_path=progress_path,
            log_path=log_path,
            point=point,
            attempts=attempts,
            q_target_mpa=q_trial,
            step_size_mpa=raw_step,
            older_checkpoint_rel=previous_checkpoint_rel,
            next_step_mpa=step_mpa,
            stage="bootstrap_extension",
            elapsed_seconds=elapsed,
        )
        older_point, previous_point = previous_point, point
        previous_checkpoint_rel = checkpoint_rel
        accepted_new_steps += 1
        stop_reason = maybe_stop(invocation_start, args, accepted_new_steps)
        if stop_reason is not None and previous_point.q_mpa < bootstrap_target - 1.0e-12:
            progress["state"]["status"] = stop_reason
            runtime.save_json(progress_path, progress)
            return scaled_anchor_point, older_point, previous_point, step_mpa, profile

    return scaled_anchor_point, older_point, previous_point, step_mpa, profile


def continue_adaptively(
    *,
    args: argparse.Namespace,
    run_dir: Path,
    progress: dict[str, Any],
    progress_path: Path,
    log_path: Path,
    invocation_start: float,
    scaled_anchor_point,
    older_point,
    previous_point,
    step_mpa: float,
    profile,
) -> None:
    accepted_new_steps = 0
    previous_checkpoint_rel = Path(progress["state"]["resume_previous_checkpoint"])

    while previous_point.q_mpa < float(args.target_load_mpa) - 1.0e-12:
        stop_reason = maybe_stop(invocation_start, args, accepted_new_steps)
        if stop_reason is not None:
            progress["state"]["status"] = stop_reason
            runtime.refresh_progress_summary(progress)
            runtime.save_json(progress_path, progress)
            return

        raw_step = min(float(step_mpa), float(args.target_load_mpa - previous_point.q_mpa))
        if raw_step <= 1.0e-12:
            break
        q_trial = round(float(previous_point.q_mpa + raw_step), 7)
        point, attempts = runtime.pilot20.try_scaled_attempts(
            q_trial,
            runtime.pilot20.scaled_seed_specs(
                q_trial,
                older_point,
                previous_point,
                scaled_anchor_point,
                profile,
                runtime.pilot20.U_Z_SCALE,
            ),
            profile,
            runtime.pilot20.U_Z_SCALE,
        )
        elapsed = time.perf_counter() - invocation_start
        if point is None:
            step_mpa = max(float(args.min_step_mpa), float(raw_step) * float(args.failure_shrink))
            terminal = raw_step <= float(args.min_step_mpa) + 1.0e-12
            record_failure_event(
                progress=progress,
                progress_path=progress_path,
                log_path=log_path,
                attempts=attempts,
                q_target_mpa=q_trial,
                step_size_mpa=raw_step,
                next_step_mpa=step_mpa,
                stage="fast_continuation",
                elapsed_seconds=elapsed,
                terminal=terminal,
            )
            if terminal:
                progress["state"]["status"] = "stopped_at_min_step_failure"
                runtime.save_json(progress_path, progress)
                return
            continue

        step_mpa = min(float(args.max_step_mpa), float(runtime.pilot21.adapt_step_size(raw_step, point)))
        checkpoint_rel = record_accepted_step(
            progress=progress,
            run_dir=run_dir,
            progress_path=progress_path,
            log_path=log_path,
            point=point,
            attempts=attempts,
            q_target_mpa=q_trial,
            step_size_mpa=raw_step,
            older_checkpoint_rel=previous_checkpoint_rel,
            next_step_mpa=step_mpa,
            stage="fast_continuation",
            elapsed_seconds=elapsed,
        )
        older_point, previous_point = previous_point, point
        previous_checkpoint_rel = checkpoint_rel
        accepted_new_steps += 1

    progress["state"]["status"] = "completed_target"
    runtime.refresh_progress_summary(progress)
    runtime.save_json(progress_path, progress)


def main() -> None:
    args = parse_args()
    run_dir = args.run_dir.resolve()
    progress_path = run_dir / runtime.DEFAULT_PROGRESS_JSON.name
    log_path = run_dir / runtime.DEFAULT_PROGRESS_LOG.name
    progress = runtime.load_json(progress_path)
    invocation_start = time.perf_counter()

    if progress is None:
        placeholder_profile = runtime.pilot10.SolverProfile(
            name="u_z_scaled_arc_like_fast_continuation",
            description="Fast resumable continuation using the pilot-20 scaled formulation.",
            config=runtime.AxisymmetricSimpleSupportConfig(),
        )
        progress = build_progress_payload(run_dir, float(args.target_load_mpa), float(args.bootstrap_target_mpa), placeholder_profile)
        runtime.refresh_progress_summary(progress)
        runtime.save_json(progress_path, progress)

    progress["metadata"]["target_load_mpa"] = float(args.target_load_mpa)
    progress["metadata"]["bootstrap_target_mpa"] = float(args.bootstrap_target_mpa)
    runtime.refresh_progress_summary(progress)
    runtime.save_json(progress_path, progress)

    scaled_anchor_point, older_point, previous_point, step_mpa, profile = bootstrap_if_needed(
        args=args,
        run_dir=run_dir,
        progress=progress,
        progress_path=progress_path,
        log_path=log_path,
        invocation_start=invocation_start,
    )

    continue_adaptively(
        args=args,
        run_dir=run_dir,
        progress=progress,
        progress_path=progress_path,
        log_path=log_path,
        invocation_start=invocation_start,
        scaled_anchor_point=scaled_anchor_point,
        older_point=older_point,
        previous_point=previous_point,
        step_mpa=step_mpa,
        profile=profile,
    )

    progress = runtime.load_json(progress_path) or progress
    summary = progress.get("summary") or {}
    print("=== Pilot 21 fast u_z-scaled continuation ===")
    print(f"Status: {(progress.get('state') or {}).get('status')}")
    print(f"Highest converged load: {summary.get('highest_converged_q_mpa')} MPa")
    print(f"Terminal failure: {summary.get('terminal_failure_q_mpa')}")
    print(f"Accepted steps stored: {summary.get('accepted_step_count')}")
    print(f"Suggested confirm loads: {summary.get('suggested_confirm_loads_mpa')}")


if __name__ == "__main__":
    main()

