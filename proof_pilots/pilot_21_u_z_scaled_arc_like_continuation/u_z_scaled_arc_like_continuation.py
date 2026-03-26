from __future__ import annotations

import importlib.util
import json
import math
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

THIS_FILE = Path(__file__).resolve()
PILOT_DIR = THIS_FILE.parent
REPO_ROOT = THIS_FILE.parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from shell_buckling.mixed_weak.axisymmetric_simple_support_background import AxisymmetricSimpleSupportConfig


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


pilot10 = load_module(
    "pilot21_pilot10_campaign",
    REPO_ROOT / "proof_pilots" / "pilot_10_high_load_simple_support_continuation" / "continuation_campaign.py",
)
pilot12 = load_module(
    "pilot21_pilot12_extension",
    REPO_ROOT / "proof_pilots" / "pilot_12_high_load_branch_extension" / "numerical_extension.py",
)
pilot20 = load_module(
    "pilot21_pilot20_method_sweep",
    REPO_ROOT / "proof_pilots" / "pilot_20_method_sweep_for_simple_support_ceiling" / "method_sweep.py",
)


OUTPUT_JSON = PILOT_DIR / "u_z_scaled_arc_like_results.json"
OLD_PATH_ANCHOR_MPA = 4.3434
OLD_PATH_FAILURE_MPA = 4.3440
PILOT20_BEST_BOUNDED_CEILING_MPA = 4.3520
PILOT20_WARMUP_LOADS_MPA = (
    4.3434,
    4.3440,
    4.3445,
    4.3450,
    4.3455,
    4.3460,
    4.3470,
    4.3480,
    4.3490,
    4.3500,
    4.3510,
    4.3520,
)
EXTENSION_STAGE_TARGETS_MPA = (4.3550, 4.3600, 4.3700, 4.3800)
INITIAL_STEP_MPA = 6.0e-4
MIN_STEP_MPA = 1.5e-4
MAX_STEP_MPA = 2.5e-3
SUCCESS_GROWTH = 1.35
FAILURE_SHRINK = 0.5
TOTAL_BUDGET_SECONDS = 4.0 * 3600.0


def serializable(value: Any) -> Any:
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple)):
        return [serializable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): serializable(item) for key, item in value.items()}
    return str(value)


def save_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(serializable(payload), indent=2), encoding="utf-8")


def point_summary(point) -> dict[str, Any]:
    return pilot12.branch_point_summary(point)


def attempt_summary(attempt) -> dict[str, Any]:
    return pilot12.attempt_summary(attempt)


def first_failed_attempt(attempts: list[Any]) -> Any | None:
    return next((attempt for attempt in attempts if not attempt.success), None)


def strongest_states(summary: dict[str, Any] | None) -> list[str]:
    if summary is None:
        return []
    return [str(item.get("state")) for item in summary.get("top_gradients", [])]


def continuation_profile(context: dict[str, Any]):
    base_config = asdict(context["old_profile"].config)
    return pilot10.SolverProfile(
        name="u_z_scaled_arc_like_continuation",
        config=AxisymmetricSimpleSupportConfig(**base_config),
        description=(
            "Use the exact pilot-20 u_z-scaled solve as the main continuation path, "
            "then add bounded arc-like step adaptation above 4.3520 MPa."
        ),
    )


def stage_interpretation(
    first_failure_summary: dict[str, Any] | None,
    branch_jump_suspicion: bool,
    reproducible: bool,
) -> str:
    if branch_jump_suspicion:
        return "possible branch-jump / non-smooth continuation signal; not purely numerical"
    if not reproducible:
        return "retest did not close cleanly; interpretation is weaker than a purely numerical reading"
    if first_failure_summary is None:
        return "no non-numerical signal seen in the bounded stage; still consistent with a numerical / conditioning barrier"
    if first_failure_summary.get("branch_turning_suspicion"):
        return "a non-mesh failure signal appeared; no longer a clean numerical-only reading"
    if first_failure_summary.get("mesh_pressure_only"):
        return "first failure remains mesh-pressure / conditioning-like with right-edge concentration"
    return "failure signal is mixed; not enough to claim a physical end of branch"


def build_overall_summary(payload: dict[str, Any]) -> dict[str, Any]:
    stages = payload.get("stages", [])
    highest_stage = None
    for stage in stages:
        accepted = stage.get("accepted_highest_converged_load_mpa")
        if accepted is None:
            continue
        if highest_stage is None or float(accepted) > float(highest_stage.get("accepted_highest_converged_load_mpa") or -1.0):
            highest_stage = stage
    highest_q = None if highest_stage is None else highest_stage.get("accepted_highest_converged_load_mpa")
    first_terminal_failure = next(
        (
            stage.get("first_failure_q_mpa")
            for stage in stages
            if str(stage.get("stop_reason", "")).startswith("failed")
        ),
        None,
    )
    highest_summary = None if highest_stage is None else highest_stage.get("accepted_highest_summary")
    return {
        "old_path_anchor_mpa": OLD_PATH_ANCHOR_MPA,
        "old_path_first_failure_mpa": OLD_PATH_FAILURE_MPA,
        "pilot20_best_bounded_ceiling_mpa": PILOT20_BEST_BOUNDED_CEILING_MPA,
        "workflow": "exact pilot-20 u_z-scaled path + auxiliary arc-like step adaptation",
        "highest_converged_q_mpa": highest_q,
        "first_terminal_failure_q_mpa": first_terminal_failure,
        "moved_above_4_3520_mpa": highest_q is not None and float(highest_q) > PILOT20_BEST_BOUNDED_CEILING_MPA + 1.0e-12,
        "highest_stage_name": None if highest_stage is None else highest_stage.get("name"),
        "strongest_gradient_order_at_highest": strongest_states(highest_summary),
        "current_barrier_reading": None if highest_stage is None else highest_stage.get("stage_interpretation"),
    }


def save_progress(payload: dict[str, Any]) -> None:
    payload["overall"] = build_overall_summary(payload)
    save_json(OUTPUT_JSON, payload)


def adapt_step_size(current_step_mpa: float, point) -> float:
    if point.node_pressure < 0.02 and point.right_edge_fraction_0_995 < 0.25:
        return min(MAX_STEP_MPA, current_step_mpa * SUCCESS_GROWTH)
    if point.node_pressure > 0.10 or point.right_edge_fraction_0_995 > 0.40:
        return max(MIN_STEP_MPA, current_step_mpa * 0.75)
    return float(current_step_mpa)


def run_retest(highest_point, older_point, scaled_anchor_point, profile, x_grid: Any) -> tuple[Any | None, list[dict[str, Any]], dict[str, Any]]:
    repeat_point, repeat_attempts = pilot20.try_scaled_attempts(
        float(highest_point.q_mpa),
        pilot20.scaled_seed_specs(
            float(highest_point.q_mpa),
            older_point,
            highest_point,
            scaled_anchor_point,
            profile,
            pilot20.U_Z_SCALE,
        ),
        profile,
        pilot20.U_Z_SCALE,
    )
    repeat_attempts_payload = [attempt_summary(attempt) for attempt in repeat_attempts]
    if repeat_point is not None:
        repeat_assessment = pilot12.reproducibility_assessment(highest_point, repeat_point, x_grid)
    else:
        failed = first_failed_attempt(repeat_attempts)
        repeat_assessment = {
            "same_load_q_mpa": float(highest_point.q_mpa),
            "accepted_seed_a": str(highest_point.accepted_seed),
            "accepted_seed_b": None if failed is None else str(failed.seed_label),
            "same_accepted_seed": False,
            "solution_delta": None,
            "reproducible": False,
            "reasons": ["repeat solve failed at the accepted stage load"],
        }
    return repeat_point, repeat_attempts_payload, repeat_assessment


def run_warmup_stage(context: dict[str, Any], profile, x_grid: Any) -> tuple[Any, Any, Any | None, float, dict[str, Any]]:
    branch = context["branch_points"]
    local_anchor = context["local_anchor"]
    old_path_anchor = context["point_43434"]
    older_point = branch[4.3432]
    previous_point = branch[4.3433]
    scaled_anchor_point = None
    stage_steps: list[dict[str, Any]] = []
    all_attempts: list[dict[str, Any]] = []
    first_failure_obj = None
    stop_reason = "completed"

    for q_target_mpa in PILOT20_WARMUP_LOADS_MPA:
        anchor_for_step = local_anchor if scaled_anchor_point is None else scaled_anchor_point
        point, attempts = pilot20.try_scaled_attempts(
            q_target_mpa,
            pilot20.scaled_seed_specs(q_target_mpa, older_point, previous_point, anchor_for_step, profile, pilot20.U_Z_SCALE),
            profile,
            pilot20.U_Z_SCALE,
        )
        attempt_payload = [attempt_summary(attempt) for attempt in attempts]
        all_attempts.extend(attempt_payload)
        step_record = {
            "q_target_mpa": q_target_mpa,
            "step_size_mpa": float(q_target_mpa - previous_point.q_mpa),
            "attempts": attempt_payload,
            "success": point is not None,
        }
        if point is None:
            failed = first_failed_attempt(attempts)
            if first_failure_obj is None and failed is not None:
                first_failure_obj = failed
            step_record["first_failed_attempt"] = None if failed is None else attempt_summary(failed)
            stage_steps.append(step_record)
            stop_reason = f"failed during fixed warmup at {q_target_mpa:.4f} MPa"
            break

        if scaled_anchor_point is None:
            continuity = {
                "q_previous_mpa": float(previous_point.q_mpa),
                "q_current_mpa": float(point.q_mpa),
                "dq_mpa": float(point.q_mpa - previous_point.q_mpa),
                "step_state_metrics": None,
                "observable_deltas": None,
                "previous_step_state_metrics": None,
                "normalized_state_growth": None,
                "observable_growth": {},
                "branch_jump_suspicion": False,
                "branch_jump_reasons": [
                    "first scaled 4.3434 anchor handoff from the old-path bootstrap is not used as a branch-jump test"
                ],
            }
        else:
            continuity = pilot12.continuity_assessment(point, previous_point, older_point, x_grid)
        step_record["accepted_point"] = point_summary(point)
        step_record["continuity"] = continuity
        stage_steps.append(step_record)
        older_point, previous_point = previous_point, point
        if scaled_anchor_point is None:
            scaled_anchor_point = point
        if continuity["branch_jump_suspicion"]:
            step_record["continuity_note"] = "recorded during warmup only; exact pilot-20 warmup path is allowed to continue"

    highest_point = previous_point
    highest_summary = point_summary(highest_point)
    retest_anchor = scaled_anchor_point if scaled_anchor_point is not None else local_anchor
    repeat_point, repeat_attempts_payload, repeat_assessment = run_retest(
        highest_point,
        older_point,
        retest_anchor,
        profile,
        x_grid,
    )
    first_failure_summary = None if first_failure_obj is None else attempt_summary(first_failure_obj)
    step_after_stage = max(INITIAL_STEP_MPA, float(highest_point.q_mpa - older_point.q_mpa))
    stage_record = {
        "name": "stage_01_reproduce_4.3520_mpa",
        "start_load_mpa": float(old_path_anchor.q_mpa),
        "target_load_mpa": PILOT20_BEST_BOUNDED_CEILING_MPA,
        "reached_target": abs(highest_point.q_mpa - PILOT20_BEST_BOUNDED_CEILING_MPA) < 1.0e-12,
        "accepted_highest_converged_load_mpa": float(highest_point.q_mpa),
        "accepted_highest_summary": highest_summary,
        "scaled_anchor_summary": None if scaled_anchor_point is None else point_summary(scaled_anchor_point),
        "first_failure_q_mpa": None if first_failure_obj is None else float(first_failure_obj.q_mpa),
        "first_failure_summary": first_failure_summary,
        "branch_jump_suspicion": False,
        "branch_jump_reasons": [
            reason
            for step in stage_steps
            for reason in list((step.get("continuity") or {}).get("branch_jump_reasons", []))
        ],
        "repeat_summary": None if repeat_point is None else point_summary(repeat_point),
        "repeat_attempts": repeat_attempts_payload,
        "reproducibility": repeat_assessment,
        "strongest_gradient_order": strongest_states(highest_summary),
        "stage_interpretation": stage_interpretation(
            first_failure_summary,
            False,
            bool(repeat_assessment.get("reproducible")),
        ),
        "stop_reason": stop_reason,
        "steps": stage_steps,
        "attempt_count": len(all_attempts) + len(repeat_attempts_payload),
        "step_size_after_stage_mpa": step_after_stage,
    }
    return older_point, previous_point, scaled_anchor_point, step_after_stage, stage_record


def run_extension_stage(
    *,
    stage_name: str,
    target_q_mpa: float,
    older_point,
    previous_point,
    scaled_anchor_point,
    profile,
    step_mpa: float,
    x_grid: Any,
) -> tuple[Any, Any, float, dict[str, Any]]:
    stage_start_q = float(previous_point.q_mpa)
    stage_steps: list[dict[str, Any]] = []
    all_attempts: list[dict[str, Any]] = []
    first_failure_obj = None
    branch_jump_suspicion = False
    branch_jump_reasons: list[str] = []
    stop_reason = "completed"

    while previous_point.q_mpa < target_q_mpa - 1.0e-12:
        raw_step = min(step_mpa, float(target_q_mpa - previous_point.q_mpa))
        q_trial = round(float(previous_point.q_mpa + raw_step), 7)
        if q_trial <= previous_point.q_mpa + 1.0e-12:
            q_trial = round(float(min(target_q_mpa, previous_point.q_mpa + MIN_STEP_MPA)), 7)
        point, attempts = pilot20.try_scaled_attempts(
            q_trial,
            pilot20.scaled_seed_specs(q_trial, older_point, previous_point, scaled_anchor_point, profile, pilot20.U_Z_SCALE),
            profile,
            pilot20.U_Z_SCALE,
        )
        attempt_payload = [attempt_summary(attempt) for attempt in attempts]
        all_attempts.extend(attempt_payload)
        step_record = {
            "q_target_mpa": q_trial,
            "step_size_mpa": raw_step,
            "attempts": attempt_payload,
            "success": point is not None,
        }
        if point is None:
            failed = first_failed_attempt(attempts)
            if first_failure_obj is None and failed is not None:
                first_failure_obj = failed
            step_mpa = max(MIN_STEP_MPA, float(raw_step) * FAILURE_SHRINK)
            step_record["first_failed_attempt"] = None if failed is None else attempt_summary(failed)
            step_record["next_step_size_mpa"] = step_mpa
            stage_steps.append(step_record)
            if raw_step <= MIN_STEP_MPA + 1.0e-12:
                stop_reason = f"failed at {q_trial:.4f} MPa with min step"
                break
            continue

        continuity = pilot12.continuity_assessment(point, previous_point, older_point, x_grid)
        step_record["accepted_point"] = point_summary(point)
        step_record["continuity"] = continuity
        older_point, previous_point = previous_point, point
        step_mpa = adapt_step_size(step_mpa, point)
        step_record["next_step_size_mpa"] = step_mpa
        stage_steps.append(step_record)
        if continuity["branch_jump_suspicion"]:
            branch_jump_suspicion = True
            branch_jump_reasons.extend(list(continuity.get("branch_jump_reasons", [])))
            stop_reason = f"branch-jump suspicion at {q_trial:.4f} MPa"
            break

    highest_point = previous_point
    highest_summary = point_summary(highest_point)
    repeat_point, repeat_attempts_payload, repeat_assessment = run_retest(
        highest_point,
        older_point,
        scaled_anchor_point,
        profile,
        x_grid,
    )
    first_failure_summary = None if first_failure_obj is None else attempt_summary(first_failure_obj)
    stage_record = {
        "name": stage_name,
        "start_load_mpa": stage_start_q,
        "target_load_mpa": float(target_q_mpa),
        "reached_target": previous_point.q_mpa >= target_q_mpa - 1.0e-12,
        "accepted_highest_converged_load_mpa": float(highest_point.q_mpa),
        "accepted_highest_summary": highest_summary,
        "first_failure_q_mpa": None if first_failure_obj is None else float(first_failure_obj.q_mpa),
        "first_failure_summary": first_failure_summary,
        "branch_jump_suspicion": branch_jump_suspicion,
        "branch_jump_reasons": branch_jump_reasons,
        "repeat_summary": None if repeat_point is None else point_summary(repeat_point),
        "repeat_attempts": repeat_attempts_payload,
        "reproducibility": repeat_assessment,
        "strongest_gradient_order": strongest_states(highest_summary),
        "stage_interpretation": stage_interpretation(
            first_failure_summary,
            branch_jump_suspicion,
            bool(repeat_assessment.get("reproducible")),
        ),
        "stop_reason": stop_reason,
        "steps": stage_steps,
        "attempt_count": len(all_attempts) + len(repeat_attempts_payload),
        "step_size_after_stage_mpa": float(step_mpa),
    }
    return older_point, previous_point, step_mpa, stage_record


def can_continue_after_stage(stage: dict[str, Any]) -> bool:
    if not stage.get("reached_target"):
        return False
    if stage.get("branch_jump_suspicion"):
        return False
    return stage.get("repeat_summary") is not None


def print_stage_summary(stage: dict[str, Any]) -> None:
    repro = stage.get("reproducibility") or {}
    print(
        f"{stage['name']}: accepted={stage['accepted_highest_converged_load_mpa']:.4f} MPa, "
        f"target={stage['target_load_mpa']:.4f} MPa, first_failure={stage['first_failure_q_mpa']}, "
        f"reached_target={stage['reached_target']}, reproducible={repro.get('reproducible')}, "
        f"stop_reason={stage['stop_reason']}"
    )


def main() -> None:
    context = pilot20.build_context()
    profile = continuation_profile(context)
    x_grid = pilot12.build_comparison_grid(profile.config)

    payload: dict[str, Any] = {
        "metadata": {
            "pilot": "pilot_21_u_z_scaled_arc_like_continuation",
            "goal": "conservatively continue the separate 6-state simple-support background path above the bounded 4.3520 MPa pilot-20 ceiling",
            "workflow": "exact pilot-20 u_z-scaled path + auxiliary arc-like step adaptation",
            "same_equations_as_active_6_state_path": True,
            "same_simple_support_bcs": True,
            "old_path_anchor_mpa": OLD_PATH_ANCHOR_MPA,
            "old_path_first_failure_mpa": OLD_PATH_FAILURE_MPA,
            "pilot20_best_bounded_ceiling_mpa": PILOT20_BEST_BOUNDED_CEILING_MPA,
            "pilot20_warmup_loads_mpa": list(PILOT20_WARMUP_LOADS_MPA),
            "extension_stage_targets_mpa": list(EXTENSION_STAGE_TARGETS_MPA),
            "profile": {
                "name": profile.name,
                "description": profile.description,
                "config": asdict(profile.config),
            },
            "u_z_scale": serializable(pilot20.U_Z_SCALE),
            "step_control": {
                "initial_step_mpa": INITIAL_STEP_MPA,
                "min_step_mpa": MIN_STEP_MPA,
                "max_step_mpa": MAX_STEP_MPA,
                "success_growth_factor": SUCCESS_GROWTH,
                "failure_shrink_factor": FAILURE_SHRINK,
            },
        },
        "bootstrap": {
            "bootstrap_elapsed_seconds": context.get("bootstrap_elapsed_seconds"),
            "bootstrap_payload": context["bootstrap_payload"],
            "local_anchor_summary": point_summary(context["local_anchor"]),
            "reproduced_old_anchor_4_3434": point_summary(context["point_43434"]),
            "reproduced_old_anchor_attempts": [attempt_summary(item) for item in context["attempts_43434"]],
        },
        "stages": [],
    }
    save_progress(payload)

    older_point, previous_point, scaled_anchor_point, step_mpa, warmup_stage = run_warmup_stage(context, profile, x_grid)
    payload["stages"].append(warmup_stage)
    save_progress(payload)
    print_stage_summary(warmup_stage)

    if scaled_anchor_point is not None and can_continue_after_stage(warmup_stage):
        for idx, target in enumerate(EXTENSION_STAGE_TARGETS_MPA, start=2):
            older_point, previous_point, step_mpa, stage_record = run_extension_stage(
                stage_name=f"stage_{idx:02d}_to_{target:.4f}_mpa",
                target_q_mpa=float(target),
                older_point=older_point,
                previous_point=previous_point,
                scaled_anchor_point=scaled_anchor_point,
                profile=profile,
                step_mpa=step_mpa,
                x_grid=x_grid,
            )
            payload["stages"].append(stage_record)
            save_progress(payload)
            print_stage_summary(stage_record)
            if not can_continue_after_stage(stage_record):
                break

    payload["status"] = "completed"
    save_progress(payload)

    overall = payload["overall"]
    print("=== Pilot 21 u_z-scaled arc-like continuation ===")
    print(f"Highest converged load: {overall['highest_converged_q_mpa']} MPa")
    print(f"First terminal failure: {overall['first_terminal_failure_q_mpa']}")
    print(f"Moved above 4.3520 MPa: {overall['moved_above_4_3520_mpa']}")
    print(f"Barrier reading: {overall['current_barrier_reading']}")


if __name__ == "__main__":
    main()