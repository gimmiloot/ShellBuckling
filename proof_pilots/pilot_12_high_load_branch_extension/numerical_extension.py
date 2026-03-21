from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np


THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[2]
SRC_ROOT = REPO_ROOT / "src"
PILOT_DIR = THIS_FILE.parent
DEFAULT_OUTPUT_JSON = PILOT_DIR / "extension_results.json"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


pilot10 = load_module(
    "pilot10_continuation_campaign",
    REPO_ROOT / "proof_pilots" / "pilot_10_high_load_simple_support_continuation" / "continuation_campaign.py",
)

from shell_buckling.mixed_weak.axisymmetric_simple_support_background import STATE_LABELS


PRIMARY_PROFILE = pilot10.make_profiles("rescue")[0]
FIRST_LADDER_MPA = (4.3440, 4.3450, 4.3475, 4.3500)
SECOND_LADDER_MPA = (4.3525, 4.3550)
REFINEMENT_LOADS_MPA = (4.3431, 4.3432, 4.3433)
REPRO_TEST_LOAD_MPA = 4.3434
PREFERRED_SEED_ORDER = (
    "secant_profile_mesh",
    "previous_profile_mesh",
    "secant_prev_mesh",
    "previous_raw_mesh",
    "anchor_profile_mesh",
)
OBSERVABLE_KEYS = ("phi_1", "ur_1", "Tsn_1", "max_abs_phi", "max_abs_Tsn")


def float_key(value: float) -> str:
    return f"{value:.4f}"


def serializable(value: Any) -> Any:
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (list, tuple)):
        return [serializable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): serializable(item) for key, item in value.items()}
    return str(value)


def save_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(serializable(payload), indent=2), encoding="utf-8")


def elapsed_since(start_time: float) -> float:
    return time.perf_counter() - start_time


def ensure_budget(start_time: float, budget_seconds: float, stage: str) -> None:
    if elapsed_since(start_time) > budget_seconds:
        raise TimeoutError(f"Time budget exceeded during {stage}.")


def profile_summary(profile) -> dict[str, Any]:
    return {
        "name": profile.name,
        "description": profile.description,
        "config": asdict(profile.config),
    }


def branch_point_summary(point) -> dict[str, Any]:
    return {
        "q_mpa": float(point.q_mpa),
        "nodes": int(point.nodes),
        "max_rms": serializable(point.max_rms),
        "max_bc_residual": serializable(point.max_bc_residual),
        "min_r": serializable(point.min_r),
        "node_pressure": serializable(point.node_pressure),
        "right_edge_fraction_0_99": serializable(point.right_edge_fraction_0_99),
        "right_edge_fraction_0_995": serializable(point.right_edge_fraction_0_995),
        "right_edge_fraction_0_999": serializable(point.right_edge_fraction_0_999),
        "min_dx": serializable(point.min_dx),
        "min_dx_mid": serializable(point.min_dx_mid),
        "top_gradients": serializable(point.top_gradients),
        "observables": serializable(point.observables),
        "accepted_profile": str(point.accepted_profile),
        "accepted_seed": str(point.accepted_seed),
        "predictor_rel_correction": serializable(point.predictor_rel_correction),
        "predictor_abs_correction": serializable(point.predictor_abs_correction),
        "message": str(point.message),
    }


def attempt_summary(attempt) -> dict[str, Any]:
    return {
        "q_mpa": float(attempt.q_mpa),
        "profile_name": str(attempt.profile_name),
        "seed_label": str(attempt.seed_label),
        "success": bool(attempt.success),
        "attempt_seconds": float(attempt.attempt_seconds),
        "message": str(attempt.message),
        "nodes": int(attempt.nodes),
        "max_nodes": int(attempt.max_nodes),
        "max_rms": serializable(attempt.max_rms),
        "max_bc_residual": serializable(attempt.max_bc_residual),
        "min_r": serializable(attempt.min_r),
        "node_pressure": serializable(attempt.node_pressure),
        "right_edge_fraction_0_99": serializable(attempt.right_edge_fraction_0_99),
        "right_edge_fraction_0_995": serializable(attempt.right_edge_fraction_0_995),
        "right_edge_fraction_0_999": serializable(attempt.right_edge_fraction_0_999),
        "min_dx": serializable(attempt.min_dx),
        "min_dx_mid": serializable(attempt.min_dx_mid),
        "top_gradients": serializable(attempt.top_gradients),
        "observables": serializable(attempt.observables),
        "mesh_pressure_only": bool(attempt.mesh_pressure_only),
        "right_edge_layer_suspicion": bool(attempt.right_edge_layer_suspicion),
        "branch_turning_suspicion": bool(attempt.branch_turning_suspicion),
        "predictor_rel_correction": serializable(attempt.predictor_rel_correction),
        "predictor_abs_correction": serializable(attempt.predictor_abs_correction),
    }


def build_comparison_grid(config, n_left: int = 1800, n_right: int = 1200) -> np.ndarray:
    x0 = float(config.x0)
    split = 0.97
    left = np.linspace(x0, split, n_left, endpoint=False)
    s = np.linspace(0.0, 1.0, n_right)
    right = split + (1.0 - split) * (1.0 - (1.0 - s) ** 3.0)
    grid = np.unique(np.concatenate([left, right]))
    if grid[0] > x0:
        grid = np.insert(grid, 0, x0)
    if grid[-1] < 1.0:
        grid = np.append(grid, 1.0)
    return grid


def state_difference_metrics(sol_a, sol_b, x_grid: np.ndarray) -> dict[str, Any]:
    ya = np.asarray(sol_a.sol(x_grid), dtype=float)
    yb = np.asarray(sol_b.sol(x_grid), dtype=float)
    states: dict[str, dict[str, float]] = {}
    max_rel_l2 = 0.0
    max_rel_max = 0.0
    for idx, name in enumerate(STATE_LABELS):
        a = ya[idx]
        b = yb[idx]
        diff = a - b
        l2_diff = float(np.sqrt(np.trapezoid(diff**2, x_grid)))
        l2_a = float(np.sqrt(np.trapezoid(a**2, x_grid)))
        l2_b = float(np.sqrt(np.trapezoid(b**2, x_grid)))
        rel_l2 = l2_diff / max(l2_a, l2_b, 1.0e-12)
        max_diff = float(np.max(np.abs(diff)))
        scale_max = max(float(np.max(np.abs(a))), float(np.max(np.abs(b))), 1.0e-12)
        rel_max = max_diff / scale_max
        states[name] = {
            "rel_l2": rel_l2,
            "rel_max": rel_max,
            "max_abs_diff": max_diff,
        }
        max_rel_l2 = max(max_rel_l2, rel_l2)
        max_rel_max = max(max_rel_max, rel_max)
    states_sorted = sorted(states.items(), key=lambda item: item[1]["rel_l2"], reverse=True)
    return {
        "max_rel_l2": max_rel_l2,
        "max_rel_max": max_rel_max,
        "states": states,
        "top_states_by_rel_l2": [
            {
                "state": name,
                "rel_l2": metrics["rel_l2"],
                "rel_max": metrics["rel_max"],
                "max_abs_diff": metrics["max_abs_diff"],
            }
            for name, metrics in states_sorted[:3]
        ],
    }


def observable_delta_metrics(current_point, previous_point) -> dict[str, dict[str, float]]:
    result: dict[str, dict[str, float]] = {}
    for key in OBSERVABLE_KEYS:
        current = float(current_point.observables.get(key, 0.0))
        previous = float(previous_point.observables.get(key, 0.0))
        abs_delta = abs(current - previous)
        rel_delta = abs_delta / max(abs(current), abs(previous), 1.0)
        result[key] = {
            "current": current,
            "previous": previous,
            "abs_delta": abs_delta,
            "rel_delta": rel_delta,
        }
    return result


def continuity_assessment(current_point, previous_point, older_point, x_grid: np.ndarray) -> dict[str, Any]:
    current_step = state_difference_metrics(current_point.solution, previous_point.solution, x_grid)
    observable_deltas = observable_delta_metrics(current_point, previous_point)

    suspicion = False
    reasons: list[str] = []
    current_dq = float(current_point.q_mpa - previous_point.q_mpa)
    normalized_state_growth = None
    observable_growth: dict[str, float] = {}

    if older_point is not None:
        previous_step = state_difference_metrics(previous_point.solution, older_point.solution, x_grid)
        previous_dq = float(previous_point.q_mpa - older_point.q_mpa)
        expected_scale = current_dq / max(previous_dq, 1.0e-12)
        normalized_state_growth = current_step["max_rel_l2"] / max(previous_step["max_rel_l2"] * expected_scale, 1.0e-12)
        if normalized_state_growth > 8.0 and current_step["max_rel_l2"] > 0.02:
            suspicion = True
            reasons.append(
                f"state_change_growth={normalized_state_growth:.2f} exceeds the smooth-step threshold"
            )

        sign_flip_count = 0
        large_jump_count = 0
        for key in OBSERVABLE_KEYS:
            current_delta = float(current_point.observables.get(key, 0.0)) - float(previous_point.observables.get(key, 0.0))
            previous_delta = float(previous_point.observables.get(key, 0.0)) - float(older_point.observables.get(key, 0.0))
            growth = abs(current_delta) / max(abs(previous_delta) * max(expected_scale, 1.0e-12), 1.0e-14)
            observable_growth[key] = growth
            if growth > 8.0:
                large_jump_count += 1
                if np.sign(current_delta) != 0 and np.sign(previous_delta) != 0 and np.sign(current_delta) != np.sign(previous_delta):
                    sign_flip_count += 1
        if large_jump_count >= 2 and sign_flip_count >= 2:
            suspicion = True
            reasons.append("multiple observables show large step growth with direction flips")
    else:
        previous_step = None

    return {
        "q_previous_mpa": float(previous_point.q_mpa),
        "q_current_mpa": float(current_point.q_mpa),
        "dq_mpa": current_dq,
        "step_state_metrics": current_step,
        "observable_deltas": observable_deltas,
        "previous_step_state_metrics": previous_step,
        "normalized_state_growth": normalized_state_growth,
        "observable_growth": observable_growth,
        "branch_jump_suspicion": suspicion,
        "branch_jump_reasons": reasons,
    }


def reproducibility_assessment(point_a, point_b, x_grid: np.ndarray) -> dict[str, Any]:
    delta = state_difference_metrics(point_a.solution, point_b.solution, x_grid)
    same_seed = point_a.accepted_seed == point_b.accepted_seed
    reproducible = delta["max_rel_l2"] < 1.0e-7 and delta["max_rel_max"] < 1.0e-6
    return {
        "same_load_q_mpa": float(point_a.q_mpa),
        "accepted_seed_a": str(point_a.accepted_seed),
        "accepted_seed_b": str(point_b.accepted_seed),
        "same_accepted_seed": same_seed,
        "solution_delta": delta,
        "reproducible": reproducible,
        "reasons": [] if reproducible else ["repeat solves at the same load are not close enough"],
    }


def order_seed_specs(seed_specs) -> list[Any]:
    order_map = {label: idx for idx, label in enumerate(PREFERRED_SEED_ORDER)}
    return sorted(seed_specs, key=lambda seed: order_map.get(seed.label, len(order_map)))


def try_extension_step(
    q_target_mpa: float,
    older_point,
    previous_point,
    anchor_point,
    profile,
    start_time: float,
    budget_seconds: float,
):
    ensure_budget(start_time, budget_seconds, f"extension step to {q_target_mpa:.4f} MPa")
    seeds = order_seed_specs(
        pilot10.make_seed_specs(q_target_mpa, older_point, previous_point, anchor_point, profile)
    )
    attempt_records = []
    for seed in seeds:
        ensure_budget(start_time, budget_seconds, f"extension seed {seed.label} at {q_target_mpa:.4f} MPa")
        attempt_start = time.perf_counter()
        sol = pilot10.run_bvp_attempt(q_target_mpa, seed.x_mesh, seed.y_guess, profile.config)
        record = pilot10.build_attempt_record(
            q_target_mpa,
            profile,
            seed,
            sol,
            attempt_seconds=time.perf_counter() - attempt_start,
        )
        attempt_records.append(record)
        if record.success:
            return pilot10.build_branch_point(record, sol), attempt_records
    return None, attempt_records


def bootstrap_branch(start_time: float, budget_seconds: float) -> tuple[dict[float, Any], list[dict[str, Any]], Any, Any, Any]:
    ensure_budget(start_time, budget_seconds, "anchor schedule")
    anchor_points = pilot10.solve_anchor_schedule(pilot10.DEFAULT_ANCHOR_LOADS_MPA)
    anchor_point = anchor_points[-1]

    ensure_budget(start_time, budget_seconds, "local bootstrap")
    local_points, local_attempts = pilot10.solve_local_bootstrap(
        anchor_point,
        PRIMARY_PROFILE,
        pilot10.DEFAULT_LOCAL_BOOTSTRAP_LOADS_MPA,
    )
    all_attempts = [attempt_summary(item) for item in local_attempts]
    points_by_q = {float(point.q_mpa): point for point in anchor_points}
    points_by_q.update({float(point.q_mpa): point for point in local_points})

    local_anchor = local_points[0]
    older_point = local_points[-2]
    previous_point = local_points[-1]

    for q_target in REFINEMENT_LOADS_MPA:
        if q_target <= previous_point.q_mpa + 1.0e-12:
            continue
        point, attempts = try_extension_step(
            q_target,
            older_point,
            previous_point,
            local_anchor,
            PRIMARY_PROFILE,
            start_time,
            budget_seconds,
        )
        all_attempts.extend(attempt_summary(item) for item in attempts)
        if point is None:
            raise RuntimeError(f"Bootstrap refinement failed at q={q_target:.4f} MPa")
        points_by_q[float(point.q_mpa)] = point
        older_point, previous_point = previous_point, point

    bootstrap_payload = {
        "anchor_points": [branch_point_summary(point) for point in anchor_points],
        "local_points": [branch_point_summary(point) for point in local_points],
        "refined_points": [branch_point_summary(points_by_q[q]) for q in sorted(points_by_q) if q > 4.3430],
        "attempts": all_attempts,
    }
    return points_by_q, all_attempts, local_anchor, older_point, previous_point, bootstrap_payload


def summarize_failures(attempts: list[dict[str, Any]]) -> dict[str, Any]:
    failures = [attempt for attempt in attempts if not attempt["success"]]
    mesh_pressure = [attempt for attempt in failures if attempt["mesh_pressure_only"]]
    right_edge = [attempt for attempt in failures if attempt["right_edge_layer_suspicion"]]
    turning = [attempt for attempt in failures if attempt["branch_turning_suspicion"]]
    return {
        "failure_count": len(failures),
        "mesh_pressure_failure_count": len(mesh_pressure),
        "right_edge_layer_failure_count": len(right_edge),
        "turning_suspicion_count": len(turning),
        "mesh_pressure_dominant": bool(failures) and len(mesh_pressure) == len(failures),
        "right_edge_layer_dominant": bool(failures) and len(right_edge) == len(failures),
        "last_failure_messages": [attempt["message"] for attempt in failures[-3:]],
    }


def run_ladder_stage(
    stage_name: str,
    loads_mpa: tuple[float, ...],
    older_point,
    previous_point,
    anchor_point,
    x_grid: np.ndarray,
    start_time: float,
    budget_seconds: float,
    payload: dict[str, Any],
    output_json: Path,
) -> tuple[Any, Any, dict[str, Any], list[dict[str, Any]]]:
    stage_steps: list[dict[str, Any]] = []
    stage_attempts: list[dict[str, Any]] = []
    stopped_reason = "completed"
    first_failure_q = None
    branch_jump_seen = False

    for q_target in loads_mpa:
        point, attempts = try_extension_step(
            q_target,
            older_point,
            previous_point,
            anchor_point,
            PRIMARY_PROFILE,
            start_time,
            budget_seconds,
        )
        attempt_payload = [attempt_summary(item) for item in attempts]
        stage_attempts.extend(attempt_payload)
        step_record = {
            "q_target_mpa": float(q_target),
            "attempts": attempt_payload,
            "success": point is not None,
        }
        if point is None:
            first_failure_q = float(q_target)
            stopped_reason = f"failure at {q_target:.4f} MPa"
            step_record["failure_diagnosis"] = summarize_failures(attempt_payload)
            stage_steps.append(step_record)
            payload.setdefault("stages", []).append(
                {
                    "name": stage_name,
                    "loads_mpa": list(loads_mpa),
                    "steps": stage_steps,
                    "stopped_reason": stopped_reason,
                    "first_failure_q_mpa": first_failure_q,
                }
            )
            save_json(output_json, payload)
            return older_point, previous_point, payload["stages"][-1], stage_attempts

        continuity = continuity_assessment(point, previous_point, older_point, x_grid)
        step_record["accepted_point"] = branch_point_summary(point)
        step_record["continuity"] = continuity
        stage_steps.append(step_record)
        older_point, previous_point = previous_point, point

        if continuity["branch_jump_suspicion"]:
            branch_jump_seen = True
            stopped_reason = f"branch-jump suspicion at {q_target:.4f} MPa"
            payload.setdefault("stages", []).append(
                {
                    "name": stage_name,
                    "loads_mpa": list(loads_mpa),
                    "steps": stage_steps,
                    "stopped_reason": stopped_reason,
                    "first_failure_q_mpa": first_failure_q,
                }
            )
            save_json(output_json, payload)
            return older_point, previous_point, payload["stages"][-1], stage_attempts

        payload["latest_success"] = {
            "q_mpa": float(previous_point.q_mpa),
            "stage": stage_name,
        }
        payload.setdefault("stages", [])
        stage_snapshot = {
            "name": stage_name,
            "loads_mpa": list(loads_mpa),
            "steps": stage_steps,
            "stopped_reason": "in_progress",
            "first_failure_q_mpa": None,
        }
        if payload["stages"] and payload["stages"][-1].get("name") == stage_name:
            payload["stages"][-1] = stage_snapshot
        else:
            payload["stages"].append(stage_snapshot)
        save_json(output_json, payload)

    stage_record = {
        "name": stage_name,
        "loads_mpa": list(loads_mpa),
        "steps": stage_steps,
        "stopped_reason": stopped_reason,
        "first_failure_q_mpa": first_failure_q,
        "branch_jump_seen": branch_jump_seen,
    }
    if payload["stages"] and payload["stages"][-1].get("name") == stage_name:
        payload["stages"][-1] = stage_record
    else:
        payload["stages"].append(stage_record)
    save_json(output_json, payload)
    return older_point, previous_point, stage_record, stage_attempts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--time-budget-seconds", type=float, default=1800.0)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    start_time = time.perf_counter()
    output_json = args.output_json
    x_grid = build_comparison_grid(PRIMARY_PROFILE.config)

    payload: dict[str, Any] = {
        "metadata": {
            "pilot": "pilot_12_high_load_branch_extension",
            "primary_profile": profile_summary(PRIMARY_PROFILE),
            "repro_test_load_mpa": REPRO_TEST_LOAD_MPA,
            "first_ladder_mpa": list(FIRST_LADDER_MPA),
            "second_ladder_mpa": list(SECOND_LADDER_MPA),
            "preferred_seed_order": list(PREFERRED_SEED_ORDER),
            "time_budget_seconds": float(args.time_budget_seconds),
        },
        "status": "started",
        "stages": [],
    }
    save_json(output_json, payload)

    print("=== Pilot 12 high-load branch extension ===")
    print("Bootstrapping the validated high-load branch to 4.3433 MPa...")
    points_by_q, bootstrap_attempts, local_anchor, older_point, previous_point, bootstrap_payload = bootstrap_branch(
        start_time,
        float(args.time_budget_seconds),
    )
    payload["bootstrap"] = bootstrap_payload
    payload["status"] = "bootstrap_completed"
    save_json(output_json, payload)

    print("Retesting 4.3434 MPa from the same predecessor pair...")
    older_for_retest = older_point
    previous_for_retest = previous_point
    retest_a, attempts_a = try_extension_step(
        REPRO_TEST_LOAD_MPA,
        older_for_retest,
        previous_for_retest,
        local_anchor,
        PRIMARY_PROFILE,
        start_time,
        float(args.time_budget_seconds),
    )
    retest_b = None
    attempts_b = []
    if retest_a is not None:
        retest_b, attempts_b = try_extension_step(
            REPRO_TEST_LOAD_MPA,
            older_for_retest,
            previous_for_retest,
            local_anchor,
            PRIMARY_PROFILE,
            start_time,
            float(args.time_budget_seconds),
        )

    reproducibility_payload = {
        "attempts_a": [attempt_summary(item) for item in attempts_a],
        "attempts_b": [attempt_summary(item) for item in attempts_b],
        "success_a": retest_a is not None,
        "success_b": retest_b is not None,
        "point_a": branch_point_summary(retest_a) if retest_a is not None else None,
        "point_b": branch_point_summary(retest_b) if retest_b is not None else None,
        "same_load_assessment": reproducibility_assessment(retest_a, retest_b, x_grid)
        if retest_a is not None and retest_b is not None
        else None,
    }
    payload["reproducibility"] = reproducibility_payload
    payload["status"] = "reproducibility_checked"
    save_json(output_json, payload)

    if retest_a is None:
        payload["status"] = "terminated"
        payload["overall"] = {
            "highest_converged_q_mpa": float(previous_point.q_mpa),
            "first_failure_q_mpa": REPRO_TEST_LOAD_MPA,
            "branch_jump_suspicion": False,
            "ceiling_moved_beyond_4_35_mpa": False,
            "bottleneck_summary": summarize_failures([attempt_summary(item) for item in attempts_a]),
            "stopped_reason": "4.3434 retest A failed",
        }
        save_json(output_json, payload)
        print("4.3434 MPa could not be reproduced on the first retest.")
        print(f"Results written to: {output_json}")
        return

    # Use one successful 4.3434 point as the branch start.
    point_43434 = retest_a
    older_point = previous_for_retest
    previous_point = point_43434

    print("Running the first ladder above 4.3434 MPa...")
    older_point, previous_point, first_stage_record, first_stage_attempts = run_ladder_stage(
        "first_ladder",
        FIRST_LADDER_MPA,
        older_point,
        previous_point,
        local_anchor,
        x_grid,
        start_time,
        float(args.time_budget_seconds),
        payload,
        output_json,
    )

    all_extension_attempts = (
        [attempt_summary(item) for item in attempts_a]
        + [attempt_summary(item) for item in attempts_b]
        + first_stage_attempts
    )

    second_stage_record = None
    second_stage_attempts: list[dict[str, Any]] = []
    first_stage_success = (
        first_stage_record.get("first_failure_q_mpa") is None
        and first_stage_record.get("stopped_reason") == "completed"
        and not first_stage_record.get("branch_jump_seen", False)
    )
    if first_stage_success:
        print("First ladder is smooth enough to justify a second ladder above 4.3500 MPa...")
        older_point, previous_point, second_stage_record, second_stage_attempts = run_ladder_stage(
            "second_ladder",
            SECOND_LADDER_MPA,
            older_point,
            previous_point,
            local_anchor,
            x_grid,
            start_time,
            float(args.time_budget_seconds),
            payload,
            output_json,
        )
        all_extension_attempts.extend(second_stage_attempts)
    else:
        payload["stages"].append(
            {
                "name": "second_ladder",
                "loads_mpa": list(SECOND_LADDER_MPA),
                "steps": [],
                "stopped_reason": "not_attempted_because_first_ladder_was_not_cleanly_successful",
                "first_failure_q_mpa": None,
            }
        )
        save_json(output_json, payload)

    highest_converged = float(previous_point.q_mpa)
    first_failure = None
    for stage in payload["stages"]:
        if stage.get("first_failure_q_mpa") is not None:
            first_failure = float(stage["first_failure_q_mpa"])
            break

    branch_jump_suspicion = any(
        step.get("continuity", {}).get("branch_jump_suspicion", False)
        for stage in payload["stages"]
        for step in stage.get("steps", [])
    )
    failure_summary = summarize_failures(all_extension_attempts)
    beyond_435 = highest_converged > 4.35 + 1.0e-12

    payload["status"] = "completed"
    payload["elapsed_seconds"] = elapsed_since(start_time)
    payload["overall"] = {
        "highest_converged_q_mpa": highest_converged,
        "first_failure_q_mpa": first_failure,
        "retest_4_3434_reproducible": bool(
            reproducibility_payload.get("success_a")
            and reproducibility_payload.get("success_b")
            and reproducibility_payload.get("same_load_assessment", {}).get("reproducible", False)
        ),
        "branch_jump_suspicion": branch_jump_suspicion,
        "ceiling_moved_beyond_4_35_mpa": beyond_435,
        "bottleneck_summary": failure_summary,
        "stopped_reason": (
            second_stage_record.get("stopped_reason")
            if second_stage_record is not None
            else first_stage_record.get("stopped_reason")
        ),
    }
    save_json(output_json, payload)

    print(f"4.3434 retest A success: {retest_a is not None}")
    print(f"4.3434 retest B success: {retest_b is not None}")
    if reproducibility_payload.get("same_load_assessment") is not None:
        print(
            "4.3434 same-load reproducible: "
            f"{reproducibility_payload['same_load_assessment']['reproducible']}"
        )
    print(f"Highest converged load: {highest_converged:.4f} MPa")
    print(f"First failure load: {first_failure}")
    print(f"Branch-jump suspicion: {branch_jump_suspicion}")
    print(f"Ceiling beyond 4.35 MPa: {beyond_435}")
    print(f"Results written to: {output_json}")


if __name__ == "__main__":
    main()
