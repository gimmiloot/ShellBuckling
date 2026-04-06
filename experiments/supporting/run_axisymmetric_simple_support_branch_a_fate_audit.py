from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


warnings.filterwarnings("ignore", category=RuntimeWarning, module=r"scipy\.integrate\._bvp")

THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

OUTPUT_DIR = REPO_ROOT / "output" / "axisymmetric_simple_support_branch_a_fate_audit"
PREV_AUDIT_PATH = REPO_ROOT / "experiments" / "supporting" / "run_axisymmetric_simple_support_branch_b_continuation_audit.py"
PILOT10_PATH = REPO_ROOT / "proof_pilots" / "pilot_10_high_load_simple_support_continuation" / "continuation_campaign.py"
PILOT20_PATH = REPO_ROOT / "proof_pilots" / "pilot_20_method_sweep_for_simple_support_ceiling" / "method_sweep.py"

TRUSTED_A_LOADS = (4.3390, 4.3395, 4.3400, 4.3405)
STRICT_BOOTSTRAP_START_LOAD = 4.3200
STRICT_BOOTSTRAP_STEP = 0.0005
STRICT_END_LOAD = 4.3450
STRICT_STEP = 0.0001
STRICT_EXTENSION_END = 4.3500
STRICT_EXTENSION_STEP = 0.0002
BRANCH_AWARE_END = 4.3500
BRANCH_AWARE_INITIAL_STEP = 0.0005
BRANCH_AWARE_MIN_STEP = 0.00005
BRANCH_AWARE_MAX_STEP = 0.00075
BRANCH_AWARE_SUCCESS_GROWTH = 1.25
BRANCH_AWARE_CONDITIONING_SHRINK = 0.75
BRANCH_AWARE_FAILURE_SHRINK = 0.5
BRANCH_AWARE_MAX_ACCEPTED = 80
ND_EVAL = 2000

MERGE_REL_L2_MAX = 2.0e-5
MERGE_MARKER_REL_MAX = 2.0e-4
JUMP_TO_B_REL_L2_MAX = 1.0e-3
JUMP_TO_B_MARKER_REL_MAX = 1.0e-3

CSV_FIELDS = [
    "mode", "continuation_index", "continuation_step_mpa", "q_mpa", "background_success",
    "solve_mode", "stage_label", "seed_kind", "tried_seeds", "repair_depth", "nodes",
    "max_rms", "max_bc_residual", "min_r", "message", "u_z_center", "varphi_edge",
    "T_s_center", "min_M_s", "min_M_theta", "state_norm_l2", "delta_prev_abs_l2",
    "delta_prev_rel_l2", "continuity_jump_ratio", "branch_jump_suspicion", "branch_jump_reason",
    "distance_to_B_abs_l2", "distance_to_B_rel_l2", "distance_to_B_marker_rel_max",
    "indistinguishable_from_B", "diff_u_z_center_to_B", "diff_varphi_edge_to_B",
    "diff_T_s_center_to_B", "diff_min_M_s_to_B", "diff_min_M_theta_to_B",
    "turning_suspicion", "mesh_pressure_only", "attempt_seed_labels",
]


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


prev = load_module("branch_b_audit_support_module", PREV_AUDIT_PATH)
pilot10 = load_module("branch_a_fate_pilot10", PILOT10_PATH)
pilot20 = load_module("branch_a_fate_pilot20", PILOT20_PATH)


@dataclass
class AuditEntry:
    mode: str
    continuation_index: int
    continuation_step_mpa: float | None
    step: Any
    turning_suspicion: bool = False
    mesh_pressure_only: bool = False
    attempt_seed_labels: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Audit the fate of honest full-state simple-support Branch A above 4.341 MPa "
            "using strict p-control and an A-only branch-aware continuation discipline."
        )
    )
    parser.add_argument("--strict-end", type=float, default=STRICT_END_LOAD)
    parser.add_argument("--strict-step", type=float, default=STRICT_STEP)
    parser.add_argument("--strict-extension-end", type=float, default=STRICT_EXTENSION_END)
    parser.add_argument("--strict-extension-step", type=float, default=STRICT_EXTENSION_STEP)
    parser.add_argument("--branch-aware-end", type=float, default=BRANCH_AWARE_END)
    parser.add_argument("--branch-aware-initial-step", type=float, default=BRANCH_AWARE_INITIAL_STEP)
    parser.add_argument("--branch-aware-min-step", type=float, default=BRANCH_AWARE_MIN_STEP)
    parser.add_argument("--branch-aware-max-step", type=float, default=BRANCH_AWARE_MAX_STEP)
    parser.add_argument("--nd-eval", type=int, default=ND_EVAL)
    args = parser.parse_args()
    if args.strict_step <= 0.0 or args.strict_extension_step <= 0.0:
        raise ValueError("Strict continuation steps must be positive.")
    if args.branch_aware_initial_step <= 0.0 or args.branch_aware_min_step <= 0.0 or args.branch_aware_max_step <= 0.0:
        raise ValueError("Branch-aware step controls must be positive.")
    if args.nd_eval < 200:
        raise ValueError("--nd-eval must be at least 200.")
    return args


def make_prev_args(args: argparse.Namespace) -> argparse.Namespace:
    return argparse.Namespace(
        start_load=STRICT_BOOTSTRAP_START_LOAD,
        window1_end=max(4.3600, float(args.branch_aware_end)),
        window2_end=max(4.5000, float(args.branch_aware_end)),
        end_load=max(5.0000, float(args.branch_aware_end)),
        window1_step=STRICT_BOOTSTRAP_STEP,
        window2_step=0.005,
        window3_step=0.005,
        a_bootstrap_start=4.3000,
        a_bootstrap_step=0.005,
        b_history_seed=4.3500,
        b_bootstrap_step=0.005,
        repair_min_step=min(float(args.strict_step), float(args.branch_aware_min_step)),
        nd_eval=int(args.nd_eval),
    )


def history_map(steps: list[Any]) -> dict[float, Any]:
    return {prev.round_load(step.q_mpa): step for step in steps if step.background_success}


def build_trusted_a_history(prev_args: argparse.Namespace, local_group: list[Any], high_group: list[Any], x_eval: np.ndarray) -> list[Any]:
    a_start = prev.build_branch_a_start(prev_args, local_group, x_eval)
    loads = prev.inclusive_grid(STRICT_BOOTSTRAP_START_LOAD, TRUSTED_A_LOADS[-1], STRICT_BOOTSTRAP_STEP)
    steps = prev.continue_branch("A", a_start, loads, prev_args, local_group, high_group, x_eval, False)
    step_map = history_map(steps)
    missing = [q for q in TRUSTED_A_LOADS if prev.round_load(q) not in step_map]
    if missing:
        raise RuntimeError(f"Could not recover all trustworthy A-side loads: {missing}")
    if any(step_map[prev.round_load(q)].branch_jump_suspicion for q in TRUSTED_A_LOADS):
        raise RuntimeError("Recovered trustworthy A-side window already carries branch-jump suspicion.")
    return steps


def seed_delta_history(seed_steps: list[Any], x_eval: np.ndarray) -> list[float]:
    deltas: list[float] = []
    for previous_step, current_step in zip(seed_steps[:-1], seed_steps[1:]):
        abs_l2 = prev.state_distance(current_step.state_eval, previous_step.state_eval, x_eval)
        rel_l2 = abs_l2 / max(previous_step.state_norm_l2, 1.0)
        deltas.append(float(rel_l2))
    return deltas


def entry(mode: str, index: int, step: Any, continuation_step_mpa: float | None, turning: bool = False, mesh_pressure_only: bool = False, attempt_seed_labels: str = "") -> AuditEntry:
    return AuditEntry(
        mode=mode,
        continuation_index=int(index),
        continuation_step_mpa=None if continuation_step_mpa is None else float(continuation_step_mpa),
        step=step,
        turning_suspicion=bool(turning),
        mesh_pressure_only=bool(mesh_pressure_only),
        attempt_seed_labels=str(attempt_seed_labels),
    )


def continue_strict_p(prev_args: argparse.Namespace, local_group: list[Any], high_group: list[Any], x_eval: np.ndarray, trusted_steps: list[Any], args: argparse.Namespace) -> list[AuditEntry]:
    step_map = history_map(trusted_steps)
    trusted_window = [step_map[prev.round_load(q)] for q in TRUSTED_A_LOADS]
    out = [entry("strict_p", idx, step, None) for idx, step in enumerate(trusted_window)]

    older = trusted_window[-2]
    previous_step = trusted_window[-1]
    anchor = trusted_window[-1]
    delta_history = seed_delta_history(trusted_window, x_eval)
    continuation_index = len(out)

    def run_target_list(target_list: list[float]) -> bool:
        nonlocal older, previous_step, continuation_index
        for target_q in target_list:
            chunk = prev.advance_with_repair(
                "A",
                previous_step,
                older,
                anchor,
                target_q,
                prev_args,
                local_group,
                high_group,
                x_eval,
                delta_history,
                True,
            )
            local_previous = previous_step
            for step in chunk:
                out.append(entry("strict_p", continuation_index, step, float(step.q_mpa - local_previous.q_mpa)))
                continuation_index += 1
                if step.background_success:
                    local_previous = step
            last_step = chunk[-1]
            if not last_step.background_success or last_step.branch_jump_suspicion:
                return False
            good = [step for step in chunk if step.background_success]
            if good:
                older = good[-2] if len(good) >= 2 else previous_step
                previous_step = good[-1]
        return True

    primary_loads = prev.inclusive_grid(TRUSTED_A_LOADS[-1], float(args.strict_end), float(args.strict_step))[1:]
    primary_ok = run_target_list(primary_loads)
    if primary_ok and previous_step.q_mpa >= float(args.strict_end) - 1.0e-12:
        extension_loads = prev.inclusive_grid(float(args.strict_end), float(args.strict_extension_end), float(args.strict_extension_step))[1:]
        run_target_list(extension_loads)

    return out


def config_map(local_group: list[Any], high_group: list[Any]) -> dict[str, Any]:
    mapping = {profile.label: profile.config for profile in local_group + high_group}
    mapping["trusted_history"] = local_group[0].config
    return mapping


def to_branch_point(step: Any, cfg_map: dict[str, Any]):
    cfg = cfg_map.get(str(step.solve_mode), next(iter(cfg_map.values())))
    return pilot10.point_from_solution(
        float(step.q_mpa),
        str(step.solve_mode),
        str(step.seed_kind),
        cfg,
        step.solution,
    )


def failed_axis_result(q_mpa: float, attempts: list[Any]):
    if attempts:
        last = attempts[-1]
        seed_kind = " -> ".join(str(item.seed_label) for item in attempts)
        return prev.simple_bg.AxisymmetricBackgroundSolve(
            q_mpa=float(q_mpa),
            success=False,
            message=str(last.message),
            nodes=int(last.nodes),
            max_rms=float(last.max_rms),
            seed_kind=seed_kind,
            max_bc_residual=float(last.max_bc_residual),
            min_r=float(last.min_r),
            solution=None,
        )
    return prev.simple_bg.AxisymmetricBackgroundSolve(
        q_mpa=float(q_mpa),
        success=False,
        message="No scaled A-side continuation attempts were prepared.",
        nodes=0,
        max_rms=float("nan"),
        seed_kind="none",
        max_bc_residual=float("nan"),
        min_r=float("nan"),
        solution=None,
    )


def successful_axis_result(point) -> Any:
    return prev.simple_bg.AxisymmetricBackgroundSolve(
        q_mpa=float(point.q_mpa),
        success=True,
        message=str(point.message),
        nodes=int(point.nodes),
        max_rms=float(point.max_rms),
        seed_kind=str(point.accepted_seed),
        max_bc_residual=float(point.max_bc_residual),
        min_r=float(point.min_r),
        solution=point.solution,
    )


def adapt_branch_aware_step(current_step_mpa: float, point) -> float:
    step = float(current_step_mpa)
    if point.node_pressure < 0.02 and point.right_edge_fraction_0_995 < 0.25:
        step *= BRANCH_AWARE_SUCCESS_GROWTH
    elif point.node_pressure > 0.10 or point.right_edge_fraction_0_995 > 0.40:
        step *= BRANCH_AWARE_CONDITIONING_SHRINK
    return min(BRANCH_AWARE_MAX_STEP, max(BRANCH_AWARE_MIN_STEP, float(step)))


def continue_branch_aware_u_z_scaled(local_group: list[Any], high_group: list[Any], x_eval: np.ndarray, trusted_steps: list[Any], args: argparse.Namespace) -> list[AuditEntry]:
    step_map = history_map(trusted_steps)
    trusted_window = [step_map[prev.round_load(q)] for q in TRUSTED_A_LOADS]
    cfg_map = config_map(local_group, high_group)

    anchor_step = trusted_window[0]
    older_step = trusted_window[-2]
    previous_step = trusted_window[-1]
    anchor_point = to_branch_point(anchor_step, cfg_map)
    older_point = to_branch_point(older_step, cfg_map)
    previous_point = to_branch_point(previous_step, cfg_map)

    profile = pilot10.SolverProfile(
        name="a_u_z_scaled_arc_like",
        config=prev.high_bg.default_high_load_background_config(prev.high_bg.DEFAULT_HISTORY_RUN_DIR),
        description="A-only u_z-scaled continuation with auxiliary arc-like step adaptation.",
    )

    delta_history = seed_delta_history(trusted_window, x_eval)
    entries = [entry("branch_aware_u_z_scaled", idx, step, None) for idx, step in enumerate(trusted_window)]
    continuation_index = len(entries)
    step_mpa = float(args.branch_aware_initial_step)
    accepted_count = 0

    while previous_point.q_mpa < float(args.branch_aware_end) - 1.0e-12 and accepted_count < BRANCH_AWARE_MAX_ACCEPTED:
        q_target = prev.round_load(previous_point.q_mpa + step_mpa)
        seed_specs = pilot20.scaled_seed_specs(q_target, older_point, previous_point, anchor_point, profile, pilot20.U_Z_SCALE)
        point, attempts = pilot20.try_scaled_attempts(q_target, seed_specs, profile, pilot20.U_Z_SCALE)
        attempt_labels = " -> ".join(str(item.seed_label) for item in attempts)

        if point is None:
            failed_step = prev.make_step(
                "A",
                q_target,
                failed_axis_result(q_target, attempts),
                profile.name,
                "branch_aware_u_z_scaled",
                "failure",
                [f"{profile.name}:{str(item.seed_label)}" for item in attempts],
                0,
                x_eval,
            )
            entries.append(
                entry(
                    "branch_aware_u_z_scaled",
                    continuation_index,
                    failed_step,
                    step_mpa,
                    turning=any(bool(item.branch_turning_suspicion) for item in attempts),
                    mesh_pressure_only=bool(attempts) and all(bool(item.mesh_pressure_only) for item in attempts),
                    attempt_seed_labels=attempt_labels,
                )
            )
            continuation_index += 1
            if step_mpa <= float(args.branch_aware_min_step) + 1.0e-12:
                break
            step_mpa = max(float(args.branch_aware_min_step), step_mpa * BRANCH_AWARE_FAILURE_SHRINK)
            continue

        accepted_step = prev.make_step(
            "A",
            float(point.q_mpa),
            successful_axis_result(point),
            profile.name,
            "branch_aware_u_z_scaled",
            str(point.accepted_seed),
            [f"{profile.name}:{str(item.seed_label)}" for item in attempts],
            0,
            x_eval,
        )
        prev.annotate_continuity(accepted_step, previous_step, delta_history, x_eval)
        entries.append(entry("branch_aware_u_z_scaled", continuation_index, accepted_step, float(accepted_step.q_mpa - previous_step.q_mpa), False, False, attempt_labels))
        continuation_index += 1
        accepted_count += 1
        older_point, previous_point = previous_point, point
        older_step, previous_step = previous_step, accepted_step
        step_mpa = adapt_branch_aware_step(step_mpa, point)
        if accepted_step.branch_jump_suspicion:
            break

    return entries


def build_b_reference(prev_args: argparse.Namespace, local_group: list[Any], high_group: list[Any], x_eval: np.ndarray, q_values: list[float]) -> dict[float, Any]:
    if not q_values:
        return {}
    b_start, _ = prev.build_branch_b_start(prev_args, local_group, high_group, x_eval)
    loads = prev.unique_sorted([STRICT_BOOTSTRAP_START_LOAD] + [float(q) for q in q_values])
    steps = prev.continue_branch("B", b_start, loads, prev_args, local_group, high_group, x_eval, False)
    return {prev.round_load(step.q_mpa): step for step in steps if step.background_success and step.state_eval is not None}


def distance_payload(step: Any, b_step: Any, x_eval: np.ndarray) -> dict[str, Any]:
    abs_l2 = prev.state_distance(step.state_eval, b_step.state_eval, x_eval)
    rel_l2 = abs_l2 / max(b_step.state_norm_l2, 1.0)
    marker_rel = prev.marker_rel_max(prev.markers_from_step(step), prev.markers_from_step(b_step))
    return {
        "distance_to_B_abs_l2": float(abs_l2),
        "distance_to_B_rel_l2": float(rel_l2),
        "distance_to_B_marker_rel_max": float(marker_rel),
        "indistinguishable_from_B": bool(rel_l2 <= MERGE_REL_L2_MAX and marker_rel <= MERGE_MARKER_REL_MAX),
        "diff_u_z_center_to_B": float(step.u_z_center - b_step.u_z_center),
        "diff_varphi_edge_to_B": float(step.varphi_edge - b_step.varphi_edge),
        "diff_T_s_center_to_B": float(step.T_s_center - b_step.T_s_center),
        "diff_min_M_s_to_B": float(step.min_M_s - b_step.min_M_s),
        "diff_min_M_theta_to_B": float(step.min_M_theta - b_step.min_M_theta),
    }


def row_from_entry(entry_obj: AuditEntry, b_map: dict[float, Any], x_eval: np.ndarray) -> dict[str, object]:
    step = entry_obj.step
    row = {
        "mode": entry_obj.mode,
        "continuation_index": int(entry_obj.continuation_index),
        "continuation_step_mpa": float("nan") if entry_obj.continuation_step_mpa is None else float(entry_obj.continuation_step_mpa),
        "q_mpa": float(step.q_mpa),
        "background_success": bool(step.background_success),
        "solve_mode": str(step.solve_mode),
        "stage_label": str(step.stage_label),
        "seed_kind": str(step.seed_kind),
        "tried_seeds": str(step.tried_seeds),
        "repair_depth": int(step.repair_depth),
        "nodes": int(step.nodes),
        "max_rms": float(step.max_rms),
        "max_bc_residual": float(step.max_bc_residual),
        "min_r": float(step.min_r),
        "message": str(step.message),
        "u_z_center": float(step.u_z_center),
        "varphi_edge": float(step.varphi_edge),
        "T_s_center": float(step.T_s_center),
        "min_M_s": float(step.min_M_s),
        "min_M_theta": float(step.min_M_theta),
        "state_norm_l2": float(step.state_norm_l2),
        "delta_prev_abs_l2": float(step.delta_prev_abs_l2),
        "delta_prev_rel_l2": float(step.delta_prev_rel_l2),
        "continuity_jump_ratio": float(step.continuity_jump_ratio),
        "branch_jump_suspicion": bool(step.branch_jump_suspicion),
        "branch_jump_reason": str(step.branch_jump_reason),
        "distance_to_B_abs_l2": float("nan"),
        "distance_to_B_rel_l2": float("nan"),
        "distance_to_B_marker_rel_max": float("nan"),
        "indistinguishable_from_B": False,
        "diff_u_z_center_to_B": float("nan"),
        "diff_varphi_edge_to_B": float("nan"),
        "diff_T_s_center_to_B": float("nan"),
        "diff_min_M_s_to_B": float("nan"),
        "diff_min_M_theta_to_B": float("nan"),
        "turning_suspicion": bool(entry_obj.turning_suspicion),
        "mesh_pressure_only": bool(entry_obj.mesh_pressure_only),
        "attempt_seed_labels": str(entry_obj.attempt_seed_labels),
    }
    if step.background_success and step.state_eval is not None and prev.round_load(step.q_mpa) in b_map:
        row.update(distance_payload(step, b_map[prev.round_load(step.q_mpa)], x_eval))
    return row


def summarize_rows(rows: list[dict[str, object]]) -> dict[str, Any]:
    last_success = None
    last_distinct = None
    first_failure = None
    first_jump = None
    first_jump_to_B = None
    first_merge = None
    first_turning_failure = None

    for row in rows:
        success = bool(row["background_success"])
        q_mpa = float(row["q_mpa"])
        rel_b = float(row["distance_to_B_rel_l2"]) if np.isfinite(row["distance_to_B_rel_l2"]) else float("nan")
        marker_b = float(row["distance_to_B_marker_rel_max"]) if np.isfinite(row["distance_to_B_marker_rel_max"]) else float("nan")
        if success:
            last_success = q_mpa
            if not bool(row["branch_jump_suspicion"]) and not bool(row["indistinguishable_from_B"]):
                last_distinct = q_mpa
            if first_jump is None and bool(row["branch_jump_suspicion"]):
                first_jump = q_mpa
                if (np.isfinite(rel_b) and rel_b <= JUMP_TO_B_REL_L2_MAX) or (np.isfinite(marker_b) and marker_b <= JUMP_TO_B_MARKER_REL_MAX):
                    first_jump_to_B = q_mpa
            if first_merge is None and bool(row["indistinguishable_from_B"]) and not bool(row["branch_jump_suspicion"]):
                first_merge = q_mpa
        else:
            if first_failure is None:
                first_failure = q_mpa
            if first_turning_failure is None and bool(row["turning_suspicion"]):
                first_turning_failure = q_mpa

    return {
        "last_success_mpa": last_success,
        "last_distinct_from_B_mpa": last_distinct,
        "first_failure_mpa": first_failure,
        "first_identity_lost_mpa": first_jump if first_jump is not None else first_merge,
        "first_jump_suspicion_mpa": first_jump,
        "first_jump_to_B_mpa": first_jump_to_B,
        "first_merge_with_B_mpa": first_merge,
        "first_turning_failure_mpa": first_turning_failure,
    }


def overall_verdict(strict_summary: dict[str, Any], branch_summary: dict[str, Any]) -> str:
    strict_last = strict_summary["last_distinct_from_B_mpa"]
    branch_last = branch_summary["last_distinct_from_B_mpa"]
    branch_merge = branch_summary["first_merge_with_B_mpa"]
    strict_merge = strict_summary["first_merge_with_B_mpa"]
    branch_turn = branch_summary["first_turning_failure_mpa"]
    strict_label = f"{strict_last:.4f}" if strict_last is not None else "unknown"

    if strict_last is not None and strict_last > 4.3410 + 1.0e-12:
        return f"Branch A continues as a separate branch above 4.341 MPa up to {strict_last:.4f} MPa with strict p-control."
    if branch_last is not None and branch_last > 4.3410 + 1.0e-12:
        return f"Branch A cannot be continued beyond {strict_label} MPa with strict p-control, but can be continued with branch-aware continuation up to {branch_last:.4f} MPa as a distinct branch."
    if strict_merge is not None or branch_merge is not None:
        merge_q = branch_merge if branch_merge is not None else strict_merge
        return f"Branch A merges with B near {merge_q:.4f} MPa."
    if branch_turn is not None:
        return f"Branch A reaches a fold/turning point near {branch_turn:.4f} MPa."
    if strict_last is not None:
        return (
            f"Branch A cannot be continued beyond {strict_last:.4f} MPa with strict p-control, "
            f"and the present A-only branch-aware continuation does not recover a distinct A branch above that load."
        )
    return "Current evidence is insufficient to distinguish physical termination from numerical continuation failure."


def save_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def save_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def plot_rows(strict_rows: list[dict[str, object]], branch_rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    strict_good = [row for row in strict_rows if bool(row["background_success"])]
    branch_good = [row for row in branch_rows if bool(row["background_success"])]
    fig, axes = plt.subplots(3, 1, figsize=(11, 11), sharex=True)

    axes[0].plot([row["q_mpa"] for row in strict_good], [row["u_z_center"] for row in strict_good], label="strict p-control", color="#1f77b4")
    axes[0].plot([row["q_mpa"] for row in branch_good], [row["u_z_center"] for row in branch_good], label="branch-aware", color="#d62728")
    axes[0].set_ylabel("u_z(x0)")
    axes[0].set_title("Branch A marker u_z(x0)")
    axes[0].grid(True, alpha=0.25)
    axes[0].legend()

    axes[1].plot([row["q_mpa"] for row in strict_good], [row["varphi_edge"] for row in strict_good], color="#1f77b4")
    axes[1].plot([row["q_mpa"] for row in branch_good], [row["varphi_edge"] for row in branch_good], color="#d62728")
    axes[1].set_ylabel("varphi(1)")
    axes[1].set_title("Branch A marker varphi(1)")
    axes[1].grid(True, alpha=0.25)

    strict_dist = [row for row in strict_good if np.isfinite(row["distance_to_B_rel_l2"])]
    branch_dist = [row for row in branch_good if np.isfinite(row["distance_to_B_rel_l2"])]
    axes[2].plot([row["q_mpa"] for row in strict_dist], [row["distance_to_B_rel_l2"] for row in strict_dist], color="#1f77b4")
    axes[2].plot([row["q_mpa"] for row in branch_dist], [row["distance_to_B_rel_l2"] for row in branch_dist], color="#d62728")
    axes[2].set_ylabel("distance-to-B rel L2")
    axes[2].set_title("Distance of Branch A to Branch B")
    axes[2].set_xlabel("p, MPa")
    axes[2].grid(True, alpha=0.25)

    fig.suptitle("Honest simple-support Branch A fate audit", fontsize=14)
    fig.tight_layout()
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def print_summary(summary: dict[str, Any]) -> None:
    print("=== Branch A fate audit ===")
    print("background source: src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py")
    print("tracked-branch bridge: src/shell_buckling/mixed_weak/simple_support_high_load_background_continuation.py")
    print(f"strict run started from trustworthy A-point: {summary['strict_start_point_mpa']:.4f} MPa")
    print(f"strict allowed restart modes: {', '.join(summary['strict_allowed_restart_modes'])}")
    print(f"strict forbidden restart modes: {', '.join(summary['strict_forbidden_restart_modes'])}")
    print(f"strict last distinct-from-B point: {summary['strict_summary']['last_distinct_from_B_mpa']}")
    print(f"strict first identity-lost point: {summary['strict_summary']['first_identity_lost_mpa']}")
    print(f"branch-aware method: {summary['branch_aware_method']}")
    print(f"branch-aware last distinct-from-B point: {summary['branch_aware_summary']['last_distinct_from_B_mpa']}")
    print(f"branch-aware first identity-lost point: {summary['branch_aware_summary']['first_identity_lost_mpa']}")
    print(f"overall verdict: {summary['overall_verdict']}")
    print(f"strict CSV: {summary['strict_csv']}")
    print(f"branch-aware CSV: {summary['branch_aware_csv']}")
    print(f"plot: {summary['plot_path']}")


def main() -> None:
    args = parse_args()
    prev_args = make_prev_args(args)
    local_group = prev.local_profiles()
    high_group = prev.high_profiles()
    x_eval = prev.x_eval_grid(local_group, high_group, int(args.nd_eval))

    trusted_history = build_trusted_a_history(prev_args, local_group, high_group, x_eval)
    strict_entries = continue_strict_p(prev_args, local_group, high_group, x_eval, trusted_history, args)
    branch_entries = continue_branch_aware_u_z_scaled(local_group, high_group, x_eval, trusted_history, args)

    q_values = sorted({float(item.step.q_mpa) for item in strict_entries + branch_entries if bool(item.step.background_success)})
    b_map = build_b_reference(prev_args, local_group, high_group, x_eval, q_values)

    strict_rows = [row_from_entry(item, b_map, x_eval) for item in strict_entries]
    branch_rows = [row_from_entry(item, b_map, x_eval) for item in branch_entries]

    strict_summary = summarize_rows(strict_rows)
    branch_summary = summarize_rows(branch_rows)
    verdict = overall_verdict(strict_summary, branch_summary)

    stem = (
        f"branch_a_fate_q{float(STRICT_BOOTSTRAP_START_LOAD):.4f}".replace(".", "p")
        + f"_strict_to_{float(args.strict_end):.4f}".replace(".", "p")
        + f"_aware_to_{float(args.branch_aware_end):.4f}".replace(".", "p")
    )
    strict_csv = OUTPUT_DIR / f"{stem}_strict_p_history.csv"
    branch_csv = OUTPUT_DIR / f"{stem}_branch_aware_history.csv"
    plot_path = OUTPUT_DIR / f"{stem}_markers.png"
    summary_path = OUTPUT_DIR / f"{stem}_summary.json"

    save_csv(strict_csv, strict_rows)
    save_csv(branch_csv, branch_rows)
    plot_rows(strict_rows, branch_rows, plot_path)

    summary = {
        "strict_start_point_mpa": TRUSTED_A_LOADS[-1],
        "trusted_A_seed_window_mpa": list(TRUSTED_A_LOADS),
        "strict_allowed_restart_modes": [
            "previous_solution",
            "secant_predictor",
            "midpoint repair only from A-side states",
            "local branch-anchor projection only from A-side states",
        ],
        "strict_forbidden_restart_modes": [
            "scaled_template",
            "zero_guess",
            "generic template restart",
            "any B-seeded fallback",
        ],
        "branch_aware_method": "A-only u_z-scaled continuation with auxiliary arc-like step adaptation (pilot20/21-style seed discipline)",
        "branch_aware_anchor_load_mpa": TRUSTED_A_LOADS[0],
        "branch_aware_start_point_mpa": TRUSTED_A_LOADS[-1],
        "strict_summary": strict_summary,
        "branch_aware_summary": branch_summary,
        "overall_verdict": verdict,
        "strict_csv": str(strict_csv),
        "branch_aware_csv": str(branch_csv),
        "plot_path": str(plot_path),
    }
    save_json(summary_path, summary)
    print_summary(summary)


if __name__ == "__main__":
    main()