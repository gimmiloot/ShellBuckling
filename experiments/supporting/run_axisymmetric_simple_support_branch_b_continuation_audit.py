from __future__ import annotations

import argparse
import csv
import json
import warnings
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.mixed_weak import axisymmetric_simple_support_background as simple_bg
from shell_buckling.mixed_weak import simple_support_high_load_background_continuation as high_bg

warnings.filterwarnings("ignore", category=RuntimeWarning, module=r"scipy\.integrate\._bvp")

OUTPUT_DIR = REPO_ROOT / "output" / "axisymmetric_simple_support_branch_b_continuation_audit"
START_LOAD = 4.320
WINDOW1_END = 4.360
WINDOW2_END = 4.500
END_LOAD = 5.000
WINDOW1_STEP = 0.0005
WINDOW2_STEP = 0.005
WINDOW3_STEP = 0.005
A_BOOTSTRAP_START = 4.300
A_BOOTSTRAP_STEP = 0.005
B_HISTORY_SEED = 4.350
B_BOOTSTRAP_STEP = 0.005
REPAIR_MIN_STEP = 0.0005
ND_EVAL = 2000
CONTINUITY_JUMP_RATIO_MAX = 25.0
CONTINUITY_HISTORY_MIN = 3
CONTINUITY_HISTORY_WINDOW = 5
MERGE_REL_L2_MAX = 2.0e-5
MERGE_MARKER_REL_MAX = 2.0e-4
TRACKED_HISTORY_CONFIRM_LOADS = (4.350, 4.400, 4.500, 5.000)
CSV_FIELDS = [
    "branch", "q_mpa", "background_success", "solve_mode", "stage_label", "seed_kind", "tried_seeds",
    "repair_depth", "nodes", "max_rms", "max_bc_residual", "min_r", "message",
    "u_z_center", "varphi_edge", "T_s_center", "min_M_s", "min_M_theta",
    "state_norm_l2", "delta_prev_abs_l2", "delta_prev_rel_l2", "continuity_jump_ratio",
    "branch_jump_suspicion", "branch_jump_reason", "distance_to_A_abs_l2", "distance_to_A_rel_l2",
    "distance_to_A_marker_rel_max", "indistinguishable_from_A", "diff_u_z_center_to_A",
    "diff_varphi_edge_to_A", "diff_T_s_center_to_A", "diff_min_M_s_to_A", "diff_min_M_theta_to_A",
]


@dataclass(frozen=True)
class ProfileSpec:
    label: str
    stage_label: str
    config: simple_bg.AxisymmetricSimpleSupportConfig


@dataclass
class Step:
    branch: str
    q_mpa: float
    background_success: bool
    solve_mode: str
    stage_label: str
    seed_kind: str
    tried_seeds: str
    repair_depth: int
    nodes: int
    max_rms: float
    max_bc_residual: float
    min_r: float
    message: str
    u_z_center: float
    varphi_edge: float
    T_s_center: float
    min_M_s: float
    min_M_theta: float
    state_norm_l2: float
    delta_prev_abs_l2: float = float("nan")
    delta_prev_rel_l2: float = float("nan")
    continuity_jump_ratio: float = float("nan")
    branch_jump_suspicion: bool = False
    branch_jump_reason: str = ""
    distance_to_A_abs_l2: float = float("nan")
    distance_to_A_rel_l2: float = float("nan")
    distance_to_A_marker_rel_max: float = float("nan")
    indistinguishable_from_A: bool = False
    diff_u_z_center_to_A: float = float("nan")
    diff_varphi_edge_to_A: float = float("nan")
    diff_T_s_center_to_A: float = float("nan")
    diff_min_M_s_to_A: float = float("nan")
    diff_min_M_theta_to_A: float = float("nan")
    solution: Any | None = None
    state_eval: np.ndarray | None = None

    def row(self) -> dict[str, object]:
        return {key: getattr(self, key) for key in CSV_FIELDS}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit honest Branch B upward continuation for the full-state simple-support path.")
    parser.add_argument("--start-load", type=float, default=START_LOAD)
    parser.add_argument("--window1-end", type=float, default=WINDOW1_END)
    parser.add_argument("--window2-end", type=float, default=WINDOW2_END)
    parser.add_argument("--end-load", type=float, default=END_LOAD)
    parser.add_argument("--window1-step", type=float, default=WINDOW1_STEP)
    parser.add_argument("--window2-step", type=float, default=WINDOW2_STEP)
    parser.add_argument("--window3-step", type=float, default=WINDOW3_STEP)
    parser.add_argument("--a-bootstrap-start", type=float, default=A_BOOTSTRAP_START)
    parser.add_argument("--a-bootstrap-step", type=float, default=A_BOOTSTRAP_STEP)
    parser.add_argument("--b-history-seed", type=float, default=B_HISTORY_SEED)
    parser.add_argument("--b-bootstrap-step", type=float, default=B_BOOTSTRAP_STEP)
    parser.add_argument("--repair-min-step", type=float, default=REPAIR_MIN_STEP)
    parser.add_argument("--nd-eval", type=int, default=ND_EVAL)
    return parser.parse_args()


def round_load(value: float) -> float:
    return round(float(value), 7)


def float_tag(value: float) -> str:
    return f"{float(value):.4f}".replace("-", "m").replace(".", "p")


def inclusive_grid(start: float, end: float, step: float) -> list[float]:
    values = [round_load(start)]
    q = float(start)
    step = abs(float(step))
    while q + step < float(end) - 1.0e-12:
        q = round_load(q + step)
        values.append(float(q))
    if abs(values[-1] - float(end)) > 1.0e-12:
        values.append(round_load(end))
    return values


def descending_grid(start: float, end: float, step: float) -> list[float]:
    values: list[float] = []
    q = float(start)
    step = abs(float(step))
    while q - step > float(end) + 1.0e-12:
        q = round_load(q - step)
        values.append(float(q))
    if not values or abs(values[-1] - float(end)) > 1.0e-12:
        values.append(round_load(end))
    return values


def unique_sorted(values: list[float]) -> list[float]:
    ordered = sorted(round_load(value) for value in values)
    out: list[float] = []
    for value in ordered:
        if not out or abs(value - out[-1]) > 1.0e-12:
            out.append(value)
    return out


def schedule(args: argparse.Namespace) -> list[float]:
    w1 = inclusive_grid(args.start_load, args.window1_end, args.window1_step)
    w2 = inclusive_grid(args.window1_end, args.window2_end, args.window2_step)[1:]
    w3 = inclusive_grid(args.window2_end, args.end_load, args.window3_step)[1:]
    return unique_sorted(w1 + w2 + w3)


def local_profiles() -> list[ProfileSpec]:
    cfg = simple_bg.AxisymmetricLocalBranchFollowConfig()
    return [
        ProfileSpec("strict_local", "local_window", cfg.strict_local_config),
        ProfileSpec("relaxed_local", "local_window", cfg.relaxed_local_config),
    ]


def high_profiles() -> list[ProfileSpec]:
    return [
        ProfileSpec("high_load_profile", "high_window", high_bg.default_high_load_background_config(high_bg.DEFAULT_HISTORY_RUN_DIR))
    ]


def x_eval_grid(local_group: list[ProfileSpec], high_group: list[ProfileSpec], nd_eval: int) -> np.ndarray:
    x0 = max(float(profile.config.x0) for profile in local_group + high_group)
    return np.linspace(x0, 1.0, int(nd_eval))


def active_profiles(q_mpa: float, args: argparse.Namespace, local_group: list[ProfileSpec], high_group: list[ProfileSpec]) -> list[ProfileSpec]:
    return local_group if float(q_mpa) <= float(args.window1_end) + 1.0e-12 else high_group


def state_norm(values: np.ndarray, x_eval: np.ndarray) -> float:
    return float(np.sqrt(np.trapezoid(np.sum(np.asarray(values, dtype=float) ** 2, axis=0), x_eval)))


def state_distance(values_a: np.ndarray, values_b: np.ndarray, x_eval: np.ndarray) -> float:
    return float(np.sqrt(np.trapezoid(np.sum((np.asarray(values_a, dtype=float) - np.asarray(values_b, dtype=float)) ** 2, axis=0), x_eval)))


def extract_markers(state_eval: np.ndarray, x_eval: np.ndarray) -> dict[str, float]:
    Ts = np.asarray(state_eval[0], dtype=float)
    Ms = np.asarray(state_eval[2], dtype=float)
    ur = np.asarray(state_eval[3], dtype=float)
    uz = np.asarray(state_eval[4], dtype=float)
    varphi = np.asarray(state_eval[5], dtype=float)
    x_safe = np.maximum(np.asarray(x_eval, dtype=float), 1.0e-12)
    r = x_safe + ur
    M_theta = simple_bg.nu * Ms + np.sin(varphi) / (12.0 * simple_bg.mu**2 * np.maximum(r, 1.0e-12))
    return {
        "u_z_center": float(uz[0]),
        "varphi_edge": float(varphi[-1]),
        "T_s_center": float(Ts[0]),
        "min_M_s": float(np.min(Ms)),
        "min_M_theta": float(np.min(M_theta)),
    }


def marker_rel_max(markers_a: dict[str, float], markers_b: dict[str, float]) -> float:
    vals = []
    for key in ("u_z_center", "varphi_edge", "T_s_center", "min_M_s", "min_M_theta"):
        vals.append(abs(float(markers_a[key]) - float(markers_b[key])) / max(abs(float(markers_b[key])), 1.0))
    return float(max(vals)) if vals else float("nan")


def make_step(branch: str, q_mpa: float, result: simple_bg.AxisymmetricBackgroundSolve, solve_mode: str, stage_label: str, seed_kind: str, tried: list[str], repair_depth: int, x_eval: np.ndarray) -> Step:
    state_eval = None
    state_norm_l2 = float("nan")
    markers = {"u_z_center": float("nan"), "varphi_edge": float("nan"), "T_s_center": float("nan"), "min_M_s": float("nan"), "min_M_theta": float("nan")}
    if result.success and result.solution is not None:
        try:
            state_eval = np.asarray(result.solution.sol(x_eval), dtype=float)
            if not np.all(np.isfinite(state_eval)):
                raise ValueError("non-finite state evaluation on common grid")
            state_norm_l2 = state_norm(state_eval, x_eval)
            markers = extract_markers(state_eval, x_eval)
        except Exception as exc:
            result = simple_bg.AxisymmetricBackgroundSolve(result.q_mpa, False, f"{result.message} | state_eval_failed: {exc}", result.nodes, result.max_rms, result.seed_kind, result.max_bc_residual, result.min_r, None)
            state_eval = None
    return Step(
        branch=branch,
        q_mpa=float(q_mpa),
        background_success=bool(result.success),
        solve_mode=str(solve_mode),
        stage_label=str(stage_label),
        seed_kind=str(seed_kind),
        tried_seeds=" -> ".join(tried),
        repair_depth=int(repair_depth),
        nodes=int(result.nodes),
        max_rms=float(result.max_rms),
        max_bc_residual=float(result.max_bc_residual),
        min_r=float(result.min_r),
        message=str(result.message),
        u_z_center=float(markers["u_z_center"]),
        varphi_edge=float(markers["varphi_edge"]),
        T_s_center=float(markers["T_s_center"]),
        min_M_s=float(markers["min_M_s"]),
        min_M_theta=float(markers["min_M_theta"]),
        state_norm_l2=float(state_norm_l2),
        solution=result.solution,
        state_eval=state_eval,
    )


def build_attempts(q_target: float, x_mesh: np.ndarray, previous: Step, older: Step | None, anchor: Step) -> list[tuple[str, np.ndarray]]:
    attempts: list[tuple[str, np.ndarray]] = []
    if older is not None and older.solution is not None and previous.solution is not None and abs(previous.q_mpa - older.q_mpa) > 1.0e-14:
        y_prev = np.asarray(previous.solution.sol(x_mesh), dtype=float)
        y_old = np.asarray(older.solution.sol(x_mesh), dtype=float)
        secant = y_prev + ((float(q_target) - previous.q_mpa) / (previous.q_mpa - older.q_mpa)) * (y_prev - y_old)
        attempts.append(("secant_predictor", secant))
    attempts.append(("previous_solution", np.asarray(previous.solution.sol(x_mesh), dtype=float)))
    if abs(previous.q_mpa - anchor.q_mpa) > 1.0e-12:
        attempts.append((f"{anchor.branch.lower()}_anchor", np.asarray(anchor.solution.sol(x_mesh), dtype=float)))
    return attempts


def attempt_step(branch: str, q_target: float, previous: Step, older: Step | None, anchor: Step, profiles: list[ProfileSpec], x_eval: np.ndarray, repair_depth: int) -> Step:
    tried: list[str] = []
    last_result = simple_bg.AxisymmetricBackgroundSolve(q_target, False, "No branch-preserving attempts were prepared.", 0, float("nan"), "none", float("nan"), float("nan"), None)
    last_profile = profiles[-1]
    for profile in profiles:
        x_mesh = simple_bg.default_x_mesh(profile.config)
        for seed_label, guess in build_attempts(q_target, x_mesh, previous, older, anchor):
            tried.append(f"{profile.label}:{seed_label}")
            result = simple_bg.solve_axisymmetric_simple_support_fixed_load(q_target, config=profile.config, initial_guess=guess)
            if result.success:
                return make_step(branch, q_target, result, profile.label, profile.stage_label, seed_label, tried, repair_depth, x_eval)
            last_result = result
            last_profile = profile
    return make_step(branch, q_target, last_result, last_profile.label, last_profile.stage_label, "failure", tried, repair_depth, x_eval)


def continuity_baseline(delta_history: list[float]) -> float | None:
    finite = [float(value) for value in delta_history if np.isfinite(value)]
    if len(finite) < CONTINUITY_HISTORY_MIN:
        return None
    return float(np.median(np.asarray(finite[-CONTINUITY_HISTORY_WINDOW:], dtype=float)))


def annotate_continuity(step: Step, previous: Step | None, delta_history: list[float], x_eval: np.ndarray) -> None:
    if previous is None or step.state_eval is None or previous.state_eval is None or not step.background_success or not previous.background_success:
        return
    abs_l2 = state_distance(step.state_eval, previous.state_eval, x_eval)
    rel_l2 = abs_l2 / max(previous.state_norm_l2, 1.0)
    step.delta_prev_abs_l2 = float(abs_l2)
    step.delta_prev_rel_l2 = float(rel_l2)
    baseline = continuity_baseline(delta_history)
    if baseline is not None:
        jump_ratio = rel_l2 / max(baseline, 1.0e-16)
        step.continuity_jump_ratio = float(jump_ratio)
        if jump_ratio > CONTINUITY_JUMP_RATIO_MAX:
            step.branch_jump_suspicion = True
            step.branch_jump_reason = f"continuity_jump_ratio={jump_ratio:.2f} exceeds {CONTINUITY_JUMP_RATIO_MAX:.2f}"
    if np.isfinite(rel_l2) and not step.branch_jump_suspicion:
        delta_history.append(float(rel_l2))


def advance_with_repair(branch: str, previous: Step, older: Step | None, anchor: Step, target_q: float, args: argparse.Namespace, local_group: list[ProfileSpec], high_group: list[ProfileSpec], x_eval: np.ndarray, delta_history: list[float], stop_on_jump: bool, repair_depth: int = 0) -> list[Step]:
    step = attempt_step(branch, target_q, previous, older, anchor, active_profiles(target_q, args, local_group, high_group), x_eval, repair_depth)
    annotate_continuity(step, previous, delta_history, x_eval)
    if step.background_success and not (stop_on_jump and step.branch_jump_suspicion):
        return [step]
    delta_q = abs(float(target_q) - previous.q_mpa)
    if delta_q <= float(args.repair_min_step) + 1.0e-12:
        return [step]
    q_mid = round_load(0.5 * (previous.q_mpa + float(target_q)))
    if abs(q_mid - previous.q_mpa) <= 1.0e-12 or abs(q_mid - float(target_q)) <= 1.0e-12:
        return [step]
    prefix = advance_with_repair(branch, previous, older, anchor, q_mid, args, local_group, high_group, x_eval, delta_history, stop_on_jump, repair_depth + 1)
    if not prefix or not prefix[-1].background_success or (stop_on_jump and prefix[-1].branch_jump_suspicion):
        return prefix
    suffix = advance_with_repair(branch, prefix[-1], previous, anchor, target_q, args, local_group, high_group, x_eval, delta_history, stop_on_jump, repair_depth + 1)
    return prefix + suffix


def continue_branch(branch: str, start_step: Step, loads: list[float], args: argparse.Namespace, local_group: list[ProfileSpec], high_group: list[ProfileSpec], x_eval: np.ndarray, stop_on_jump: bool) -> list[Step]:
    out = [start_step]
    delta_history: list[float] = []
    older: Step | None = None
    previous = start_step
    anchor = start_step
    for q_target in loads[1:]:
        chunk = advance_with_repair(branch, previous, older, anchor, q_target, args, local_group, high_group, x_eval, delta_history, stop_on_jump)
        if not chunk:
            break
        out.extend(chunk)
        last = chunk[-1]
        if not last.background_success:
            break
        if stop_on_jump and last.branch_jump_suspicion:
            break
        good = [step for step in chunk if step.background_success]
        if good:
            older = good[-2] if len(good) >= 2 else previous
            previous = good[-1]
    return out


def realize_on_local(branch: str, q_mpa: float, source: simple_bg.AxisymmetricBackgroundSolve, local_group: list[ProfileSpec], x_eval: np.ndarray, seed_label: str) -> Step:
    last_failure = None
    for profile in local_group:
        x_mesh = simple_bg.default_x_mesh(profile.config)
        result = simple_bg.solve_axisymmetric_simple_support_fixed_load(q_mpa, config=profile.config, initial_guess=np.asarray(source.solution.sol(x_mesh), dtype=float))
        step = make_step(branch, q_mpa, result, profile.label, profile.stage_label, seed_label, [f"{profile.label}:{seed_label}"], 0, x_eval)
        if step.background_success:
            return step
        last_failure = step
    raise RuntimeError(f"Could not realize branch {branch} at q={q_mpa:.4f} MPa: {last_failure.message}")


def build_branch_a_start(args: argparse.Namespace, local_group: list[ProfileSpec], x_eval: np.ndarray) -> Step:
    anchor_config = simple_bg.AxisymmetricLocalBranchFollowConfig().anchor_config
    anchor_mesh = simple_bg.default_x_mesh(anchor_config)
    template = simple_bg.build_template_solution(anchor_config)
    loads = inclusive_grid(args.a_bootstrap_start, args.start_load, args.a_bootstrap_step)
    previous = simple_bg.solve_axisymmetric_simple_support_fixed_load(loads[0], config=anchor_config, template_result=template)
    if not previous.success or previous.solution is None:
        raise RuntimeError(f"Branch A bootstrap failed at q={loads[0]:.4f} MPa: {previous.message}")
    for q_mpa in loads[1:]:
        previous = simple_bg.solve_axisymmetric_simple_support_fixed_load(q_mpa, config=anchor_config, initial_guess=previous.solution.sol(anchor_mesh))
        if not previous.success or previous.solution is None:
            raise RuntimeError(f"Branch A bootstrap failed at q={q_mpa:.4f} MPa: {previous.message}")
    return realize_on_local("A", args.start_load, previous, local_group, x_eval, "low_load_branch_projection")


def build_branch_b_start(args: argparse.Namespace, local_group: list[ProfileSpec], high_group: list[ProfileSpec], x_eval: np.ndarray) -> tuple[Step, simple_bg.AxisymmetricBackgroundSolve]:
    history = high_bg.solve_axisymmetric_simple_support_high_load_schedule([args.b_history_seed], history_run_dir=high_bg.DEFAULT_HISTORY_RUN_DIR, prefer_established_history=True, verbose=False)[0]
    if not history.success or history.solution is None:
        raise RuntimeError(f"Could not recover Branch B history seed at q={args.b_history_seed:.4f} MPa: {history.message}")
    start_local = realize_on_local("B", args.b_history_seed, history, local_group, x_eval, "tracked_history_projection")
    bootstrap_loads = [start_local.q_mpa] + descending_grid(start_local.q_mpa, args.start_load, args.b_bootstrap_step)
    boot = continue_branch("B", start_local, bootstrap_loads, args, local_group, high_group, x_eval, stop_on_jump=False)
    last = boot[-1]
    if not last.background_success or abs(last.q_mpa - float(args.start_load)) > 1.0e-9:
        raise RuntimeError(f"Could not bootstrap Branch B down to q={args.start_load:.4f} MPa from retained seed q={args.b_history_seed:.4f} MPa.")
    return last, history


def trustworthy_a_map(a_steps: list[Step]) -> dict[float, Step]:
    return {round_load(step.q_mpa): step for step in a_steps if step.background_success and not step.branch_jump_suspicion and step.state_eval is not None}


def markers_from_step(step: Step) -> dict[str, float]:
    return {
        "u_z_center": float(step.u_z_center),
        "varphi_edge": float(step.varphi_edge),
        "T_s_center": float(step.T_s_center),
        "min_M_s": float(step.min_M_s),
        "min_M_theta": float(step.min_M_theta),
    }


def augment_b_to_a(b_steps: list[Step], a_steps: list[Step], x_eval: np.ndarray) -> None:
    a_map = trustworthy_a_map(a_steps)
    for step in b_steps:
        if not step.background_success or step.state_eval is None:
            continue
        a_step = a_map.get(round_load(step.q_mpa))
        if a_step is None:
            continue
        abs_l2 = state_distance(step.state_eval, a_step.state_eval, x_eval)
        rel_l2 = abs_l2 / max(a_step.state_norm_l2, 1.0)
        step.distance_to_A_abs_l2 = float(abs_l2)
        step.distance_to_A_rel_l2 = float(rel_l2)
        step.diff_u_z_center_to_A = float(step.u_z_center - a_step.u_z_center)
        step.diff_varphi_edge_to_A = float(step.varphi_edge - a_step.varphi_edge)
        step.diff_T_s_center_to_A = float(step.T_s_center - a_step.T_s_center)
        step.diff_min_M_s_to_A = float(step.min_M_s - a_step.min_M_s)
        step.diff_min_M_theta_to_A = float(step.min_M_theta - a_step.min_M_theta)
        marker_rel = marker_rel_max(markers_from_step(step), markers_from_step(a_step))
        step.distance_to_A_marker_rel_max = float(marker_rel)
        step.indistinguishable_from_A = rel_l2 <= MERGE_REL_L2_MAX and marker_rel <= MERGE_MARKER_REL_MAX


def compare_with_history(b_steps: list[Step], x_eval: np.ndarray) -> list[dict[str, object]]:
    b_map = {round_load(step.q_mpa): step for step in b_steps if step.background_success and step.state_eval is not None}
    requested = [round_load(q) for q in TRACKED_HISTORY_CONFIRM_LOADS if round_load(q) in b_map]
    if not requested:
        return []
    history_results = high_bg.solve_axisymmetric_simple_support_high_load_schedule(requested, history_run_dir=high_bg.DEFAULT_HISTORY_RUN_DIR, prefer_established_history=True, verbose=False)
    rows = []
    for history in history_results:
        row = {"q_mpa": float(history.q_mpa), "success": bool(history.success), "history_seed_kind": str(history.seed_kind), "abs_l2": float("nan"), "rel_l2": float("nan"), "marker_rel_max": float("nan")}
        if history.success and history.solution is not None:
            step = b_map[round_load(history.q_mpa)]
            hist_eval = np.asarray(history.solution.sol(x_eval), dtype=float)
            row["abs_l2"] = state_distance(step.state_eval, hist_eval, x_eval)
            row["rel_l2"] = row["abs_l2"] / max(state_norm(hist_eval, x_eval), 1.0)
            row["marker_rel_max"] = marker_rel_max(markers_from_step(step), extract_markers(hist_eval, x_eval))
        rows.append(row)
    return rows


def last_success(steps: list[Step]) -> float | None:
    vals = [step.q_mpa for step in steps if step.background_success]
    return float(vals[-1]) if vals else None


def first_failure(steps: list[Step]) -> float | None:
    value = next((step.q_mpa for step in steps if not step.background_success), None)
    return None if value is None else float(value)


def first_jump(steps: list[Step]) -> float | None:
    value = next((step.q_mpa for step in steps if step.branch_jump_suspicion), None)
    return None if value is None else float(value)


def first_merge(b_steps: list[Step]) -> float | None:
    value = next((step.q_mpa for step in b_steps if step.indistinguishable_from_A), None)
    return None if value is None else float(value)


def last_trustworthy_a(a_steps: list[Step]) -> float | None:
    vals = [step.q_mpa for step in a_steps if step.background_success and not step.branch_jump_suspicion]
    return float(vals[-1]) if vals else None


def distinct_overlap_max(b_steps: list[Step]) -> float | None:
    vals = [step.q_mpa for step in b_steps if step.background_success and np.isfinite(step.distance_to_A_rel_l2) and not step.indistinguishable_from_A]
    return float(vals[-1]) if vals else None


def verdict(b_steps: list[Step], a_steps: list[Step], args: argparse.Namespace) -> str:
    b_last = last_success(b_steps)
    b_fail = first_failure(b_steps)
    b_jump = first_jump(b_steps)
    b_merge = first_merge(b_steps)
    a_last = last_trustworthy_a(a_steps)
    if b_merge is not None:
        return f"B merges with A near {b_merge:.3f} MPa on the present full-state distance tolerance."
    if b_jump is not None:
        return f"B continuation reaches {b_last:.3f} MPa, but branch identity becomes suspicious near {b_jump:.3f} MPa."
    if b_last is not None and b_last >= float(args.end_load) - 1.0e-9:
        if a_last is None:
            return f"B continues to {b_last:.3f} MPa with current honest continuation; no trustworthy A-reference overlap remained."
        return f"B continues to {b_last:.3f} MPa; over the trustworthy A-overlap the branches remain distinct through {a_last:.3f} MPa."
    if b_last is not None:
        return f"B cannot be continued beyond {b_last:.3f} MPa with current honest continuation; the first failed target is {b_fail:.3f} MPa."
    return "B could not be started on the requested honest continuation audit."


def stem(args: argparse.Namespace) -> str:
    return f"branch_b_audit_q{float_tag(args.start_load)}_to_{float_tag(args.end_load)}_w1s{float_tag(args.window1_step)}_w2s{float_tag(args.window2_step)}_w3s{float_tag(args.window3_step)}"


def save_csv(path: Path, steps: list[Step]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for step in steps:
            writer.writerow(step.row())


def plot(branch_b_steps: list[Step], branch_a_steps: list[Step], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    a_good = [step for step in branch_a_steps if step.background_success]
    b_good = [step for step in branch_b_steps if step.background_success]
    b_dist = [step for step in b_good if np.isfinite(step.distance_to_A_rel_l2)]
    fig, axes = plt.subplots(4, 1, figsize=(11, 14), sharex=True)
    axes[0].plot([step.q_mpa for step in a_good], [step.u_z_center for step in a_good], label="Branch A", color="#1f77b4")
    axes[0].plot([step.q_mpa for step in b_good], [step.u_z_center for step in b_good], label="Branch B", color="#d62728")
    axes[0].set_ylabel("u_z(x0)")
    axes[0].set_title("Center proxy u_z(x0)")
    axes[0].grid(True, alpha=0.25)
    axes[0].legend()
    axes[1].plot([step.q_mpa for step in a_good], [step.varphi_edge for step in a_good], color="#1f77b4")
    axes[1].plot([step.q_mpa for step in b_good], [step.varphi_edge for step in b_good], color="#d62728")
    axes[1].set_ylabel("varphi(1)")
    axes[1].set_title("Edge angle varphi(1)")
    axes[1].grid(True, alpha=0.25)
    axes[2].plot([step.q_mpa for step in a_good], [step.min_M_s for step in a_good], color="#1f77b4")
    axes[2].plot([step.q_mpa for step in b_good], [step.min_M_s for step in b_good], color="#d62728")
    axes[2].set_ylabel("min_x M_s(x)")
    axes[2].set_title("Minimum meridional moment")
    axes[2].grid(True, alpha=0.25)
    axes[3].plot([step.q_mpa for step in b_dist], [step.distance_to_A_rel_l2 for step in b_dist], color="#2ca02c")
    axes[3].set_ylabel("rel L2")
    axes[3].set_title("Branch B distance-to-A")
    axes[3].set_xlabel("p, MPa")
    axes[3].grid(True, alpha=0.25)
    fig.suptitle("Honest full-state simple-support Branch B upward continuation audit", fontsize=14)
    fig.tight_layout()
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    args = parse_args()
    local_group = local_profiles()
    high_group = high_profiles()
    x_eval = x_eval_grid(local_group, high_group, args.nd_eval)
    loads = schedule(args)

    a_start = build_branch_a_start(args, local_group, x_eval)
    b_start, b_history_seed = build_branch_b_start(args, local_group, high_group, x_eval)

    a_steps = continue_branch("A", a_start, loads, args, local_group, high_group, x_eval, stop_on_jump=True)
    b_steps = continue_branch("B", b_start, loads, args, local_group, high_group, x_eval, stop_on_jump=False)
    augment_b_to_a(b_steps, a_steps, x_eval)
    tracked_alignment = compare_with_history(b_steps, x_eval)

    file_stem = stem(args)
    b_csv = OUTPUT_DIR / f"{file_stem}_branch_b_history.csv"
    a_csv = OUTPUT_DIR / f"{file_stem}_branch_a_reference.csv"
    plot_path = OUTPUT_DIR / f"{file_stem}_markers.png"
    summary_path = OUTPUT_DIR / f"{file_stem}_summary.json"
    save_csv(b_csv, b_steps)
    save_csv(a_csv, a_steps)
    plot(b_steps, a_steps, plot_path)

    summary = {
        "branch_b_seed_load_mpa": float(args.start_load),
        "branch_b_seed_source_mpa": float(args.b_history_seed),
        "branch_b_seed_source_kind": str(b_history_seed.seed_kind),
        "branch_a_seed_load_mpa": float(args.start_load),
        "branch_a_bootstrap_start_mpa": float(args.a_bootstrap_start),
        "allowed_restart_modes": [
            "previous_solution on the same branch",
            "secant_predictor from the two latest same-branch states",
            "fixed branch anchor projection on the same branch",
            "midpoint repair using only same-branch states when a coarse target fails",
        ],
        "forbidden_restart_modes": ["scaled_template", "zero_guess", "generic template restart"],
        "branch_b_last_success_mpa": last_success(b_steps),
        "branch_b_first_failure_mpa": first_failure(b_steps),
        "branch_a_last_trustworthy_mpa": last_trustworthy_a(a_steps),
        "branch_a_first_failure_mpa": first_failure(a_steps),
        "branch_a_first_jump_suspicion_mpa": first_jump(a_steps),
        "branch_b_first_jump_suspicion_mpa": first_jump(b_steps),
        "branch_b_first_merge_with_a_mpa": first_merge(b_steps),
        "branch_b_distinct_from_a_through_mpa": distinct_overlap_max(b_steps),
        "verdict": verdict(b_steps, a_steps, args),
        "tracked_history_alignment": tracked_alignment,
        "branch_b_history_csv": str(b_csv),
        "branch_a_history_csv": str(a_csv),
        "plot_path": str(plot_path),
    }
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=== Branch B honest continuation audit ===")
    print("background source: src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py")
    print("tracked-branch bridge: src/shell_buckling/mixed_weak/simple_support_high_load_background_continuation.py")
    print(f"Branch B seed load: {summary['branch_b_seed_load_mpa']:.4f} MPa")
    print(f"Branch B seed source: {summary['branch_b_seed_source_mpa']:.4f} MPa from tracked history ({summary['branch_b_seed_source_kind']})")
    print(f"Branch A seed load: {summary['branch_a_seed_load_mpa']:.4f} MPa")
    print(f"Branch B last success: {summary['branch_b_last_success_mpa']}")
    print(f"Branch B first failure: {summary['branch_b_first_failure_mpa']}")
    print(f"Branch A last trustworthy point: {summary['branch_a_last_trustworthy_mpa']}")
    print(f"Branch A first jump suspicion: {summary['branch_a_first_jump_suspicion_mpa']}")
    if tracked_alignment:
        print("Tracked-history alignment checks:")
        for item in tracked_alignment:
            rel_text = "nan" if not np.isfinite(item['rel_l2']) else f"{item['rel_l2']:.3e}"
            marker_text = "nan" if not np.isfinite(item['marker_rel_max']) else f"{item['marker_rel_max']:.3e}"
            print(f"  q={item['q_mpa']:.3f} MPa  success={item['success']}  rel_l2={rel_text}  marker_rel_max={marker_text}  history_seed={item['history_seed_kind']}")
    print(f"Verdict: {summary['verdict']}")
    print(f"Branch B CSV: {summary['branch_b_history_csv']}")
    print(f"Branch A CSV: {summary['branch_a_history_csv']}")
    print(f"Plot: {summary['plot_path']}")


if __name__ == "__main__":
    main()