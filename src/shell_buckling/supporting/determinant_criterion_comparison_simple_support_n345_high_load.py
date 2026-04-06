# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import csv
import warnings
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from shell_buckling.mixed_weak import axisymmetric_simple_support_background as simple_bg
from shell_buckling.mixed_weak import simple_support_high_load_background_continuation as tracked_bg
from shell_buckling.supporting import determinant_criterion_comparison_simple_support as base


warnings.filterwarnings("ignore", category=RuntimeWarning, module=r"scipy\.integrate\._bvp")

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "output" / "supporting_simple_support_determinant_comparison_n345_high_load"

DEFAULT_N_LIST = [3, 4, 5]
DEFAULT_P_MIN = 0.0
DEFAULT_P_MAX = 15.0
DEFAULT_NUM_POINTS = 241
DEFAULT_ND_DET = 10000
MAX_FLOAT_LOG = float(np.log(np.finfo(float).max))
TRACKED_BRANCH_ANCHOR_MPA = 5.0
LOCAL_RESTART_STEP_MPA = 0.01
BRANCH_A_LAST_DISTINCT_LOAD_MPA = 4.34095
BRANCH_A_IDENTITY_LOSS_LOAD_MPA = 4.3410
BRANCH_A_LOW_HISTORY_START_MPA = 0.0
DIAGNOSTIC_FIELDNAMES = [
    "p",
    "solve_mode",
    "background_success",
    "background_failure_reason",
    "background_nodes",
    "background_residual",
    "background_all_finite",
    "adapter_all_finite",
    "det_inputs_all_finite",
    "det_value",
    "plot_point_used",
    "missing_reason",
]


@dataclass(frozen=True)
class BackgroundStep:
    result: base.AxisymmetricBackgroundSolve
    solve_mode: str
    warm_start_attempted: bool = False
    recovered_after_warm_failure: bool = False


@dataclass(frozen=True)
class TrackedBranchContext:
    config: base.AxisymmetricSimpleSupportConfig
    x_mesh: np.ndarray
    anchor_load_mpa: float
    anchor_history_result: base.AxisymmetricBackgroundSolve
    anchor_realized_result: base.AxisymmetricBackgroundSolve
    branch_source: str
    history_run_dir: Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Dense/high-load supporting determinant comparison for simple-support "
            "shallow vs honest non-shallow background, with the non-shallow path "
            "taken from one tracked simple-support branch."
        )
    )
    parser.add_argument("--n-list", nargs="+", type=int, default=DEFAULT_N_LIST)
    parser.add_argument("--p-min", type=float, default=DEFAULT_P_MIN)
    parser.add_argument("--p-max", type=float, default=DEFAULT_P_MAX)
    parser.add_argument("--num-points", type=int, default=DEFAULT_NUM_POINTS)
    parser.add_argument("--nd-det", type=int, default=DEFAULT_ND_DET)
    parser.add_argument(
        "--diagnose-gap",
        action="store_true",
        help=(
            "Run a tracked-branch non-shallow-only diagnostic: save a CSV with "
            "background/adapter/determinant stage status per load, print a short "
            "summary, and save one stage-marker diagnostic plot."
        ),
    )
    args = parser.parse_args(argv)
    if args.num_points < 2:
        raise ValueError("--num-points must be at least 2.")
    if args.nd_det < 2:
        raise ValueError("--nd-det must be at least 2.")
    if args.p_max <= args.p_min:
        raise ValueError("--p-max must be greater than --p-min.")
    if args.diagnose_gap and len(args.n_list) != 1:
        raise ValueError("--diagnose-gap currently requires exactly one n value in --n-list.")
    return args


def build_pressure_grid(p_min: float, p_max: float, num_points: int) -> np.ndarray:
    return np.linspace(float(p_min), float(p_max), int(num_points))


def round_load(value: float) -> float:
    return round(float(value), 7)


def unique_sorted(values: np.ndarray | list[float]) -> list[float]:
    ordered = sorted(round_load(value) for value in values)
    unique: list[float] = []
    for value in ordered:
        if not unique or abs(value - unique[-1]) > 1.0e-12:
            unique.append(value)
    return unique


def best_p_by_minlog_with_index(p_list, logabs_list):
    logabs_arr = np.asarray(logabs_list, dtype=float)
    finite = np.isfinite(logabs_arr)
    if not np.any(finite):
        return float("nan"), float("nan"), None
    masked = np.where(finite, logabs_arr, np.inf)
    j = int(np.argmin(masked))
    return float(p_list[j]), float(logabs_arr[j]), j


def save_figure(fig, filename):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


def signed_det_from_slog(sign, logabs):
    if int(sign) == 0:
        if np.isneginf(logabs):
            return 0.0
        return np.nan
    if not np.isfinite(logabs):
        return np.nan
    if logabs > MAX_FLOAT_LOG:
        return np.nan
    return float(sign) * float(np.exp(logabs))


def sign_indicator_from_slog(sign, logabs):
    if int(sign) == 0 and np.isposinf(logabs):
        return np.nan
    return float(sign)


def first_exact_zero_index(sign_list, logabs_list):
    sign_arr = np.asarray(sign_list, dtype=float)
    logabs_arr = np.asarray(logabs_list, dtype=float)
    for i in range(sign_arr.size):
        if np.isfinite(sign_arr[i]) and sign_arr[i] == 0.0 and np.isneginf(logabs_arr[i]):
            return int(i)
    return None


def first_neighbor_sign_change(sign_list):
    sign_arr = np.asarray(sign_list, dtype=float)
    for i in range(sign_arr.size - 1):
        s0 = sign_arr[i]
        s1 = sign_arr[i + 1]
        if not (np.isfinite(s0) and np.isfinite(s1)):
            continue
        if s0 == 0.0 or s1 == 0.0:
            continue
        if s0 * s1 < 0.0:
            return int(i), int(i + 1)
    return None, None


def format_sign_line(tag, p_list, sign_list, logabs_list):
    i0, i1 = first_neighbor_sign_change(sign_list)
    if i0 is not None:
        return f"{tag}: first sign change of det U_N between p={p_list[i0]:.3f} and p={p_list[i1]:.3f} MPa"

    j0 = first_exact_zero_index(sign_list, logabs_list)
    if j0 is not None:
        return f"{tag}: no neighboring sign flip detected; det U_N = 0 at sampled p={p_list[j0]:.3f} MPa"

    return f"{tag}: no sign change of det U_N on sampled neighboring loads"


def format_min_line(tag, p_min, log_min, idx, p_list):
    if idx is None:
        return f"{tag}: no finite determinant values"
    boundary = idx == len(p_list) - 1
    suffix = " (right boundary)" if boundary else ""
    return f"{tag}: min log|det U_N| at p~={p_min:.3f} MPa, value~={log_min:.6e}{suffix}"


def mark_failed_loads(ax, failed_loads, label=None):
    if not failed_loads:
        return
    y_marks = np.full(len(failed_loads), 0.04, dtype=float)
    ax.plot(
        failed_loads,
        y_marks,
        linestyle="None",
        marker="x",
        markersize=6,
        markeredgewidth=1.2,
        color="red",
        transform=ax.get_xaxis_transform(),
        label=label,
    )


def format_n_list_text(n_list: list[int]) -> str:
    return ",".join(str(int(n_wave)) for n_wave in n_list)


def float_tag(value: float) -> str:
    return f"{float(value):.3f}".replace("-", "m").replace(".", "p")


def diagnostic_stem(n_wave: int, p_list: np.ndarray) -> str:
    return (
        "tracked_branch_gap_diagnostic_"
        f"n{int(n_wave)}_"
        f"p{float_tag(p_list[0])}_to_{float_tag(p_list[-1])}_"
        f"{len(p_list)}pts"
    )


def background_residual_metric(result: base.AxisymmetricBackgroundSolve) -> float:
    if np.isfinite(result.max_rms):
        return float(result.max_rms)
    if np.isfinite(result.max_bc_residual):
        return float(result.max_bc_residual)
    return float("nan")

def build_tracked_branch_config(x0: float) -> base.AxisymmetricSimpleSupportConfig:
    high_cfg = tracked_bg.default_high_load_background_config(tracked_bg.DEFAULT_HISTORY_RUN_DIR)
    return base.AxisymmetricSimpleSupportConfig(
        x0=float(x0),
        nd_bvp=int(high_cfg.nd_bvp),
        tol=float(high_cfg.tol),
        relaxed_tol=float(high_cfg.relaxed_tol),
        max_nodes=int(high_cfg.max_nodes),
        template_q_mpa=float(high_cfg.template_q_mpa),
        right_edge_cluster_start=float(high_cfg.right_edge_cluster_start),
        right_edge_cluster_fraction=float(high_cfg.right_edge_cluster_fraction),
        right_edge_cluster_power=float(high_cfg.right_edge_cluster_power),
    )


def project_tracked_history_guess(
    history_result: base.AxisymmetricBackgroundSolve,
    x_mesh: np.ndarray,
) -> np.ndarray:
    if history_result.solution is None:
        raise ValueError("Tracked history result has no converged solution.")

    source_x0 = float(np.min(np.asarray(history_result.solution.x, dtype=float)))
    x_query = np.maximum(np.asarray(x_mesh, dtype=float), source_x0)
    guess = np.asarray(history_result.solution.sol(x_query), dtype=float)

    mask = np.asarray(x_mesh, dtype=float) < source_x0
    if np.any(mask):
        scale = np.asarray(x_mesh, dtype=float)[mask] / source_x0
        guess[1, mask] *= scale
        guess[3, mask] *= scale
        guess[5, mask] *= scale

    return guess


def build_tracked_branch_context(x0: float) -> TrackedBranchContext:
    history_run_dir = tracked_bg.DEFAULT_HISTORY_RUN_DIR
    config = build_tracked_branch_config(x0)
    x_mesh = base.default_x_mesh(config)

    anchor_history_result = tracked_bg.solve_axisymmetric_simple_support_high_load_schedule(
        [TRACKED_BRANCH_ANCHOR_MPA],
        history_run_dir=history_run_dir,
        prefer_established_history=True,
        verbose=False,
    )[0]
    if not anchor_history_result.success or anchor_history_result.solution is None:
        raise RuntimeError(
            f"Could not recover the tracked simple-support anchor at q={TRACKED_BRANCH_ANCHOR_MPA:.3f} MPa: "
            f"{anchor_history_result.message}"
        )

    projected_guess = project_tracked_history_guess(anchor_history_result, x_mesh)
    anchor_realized_result = base.solve_axisymmetric_simple_support_fixed_load(
        TRACKED_BRANCH_ANCHOR_MPA,
        config=config,
        initial_guess=projected_guess,
    )
    if not anchor_realized_result.success or anchor_realized_result.solution is None:
        raise RuntimeError(
            f"Could not realize the tracked anchor on the determinant mesh at q={TRACKED_BRANCH_ANCHOR_MPA:.3f} MPa: "
            f"{anchor_realized_result.message}"
        )

    branch_source = (
        "canonical pilot-21 compatible simple-support branch anchored at 5.000 MPa "
        f"from {history_run_dir} with retained seed {anchor_history_result.seed_kind}; "
        "the determinant-mesh branch history is generated from that anchor only"
    )
    return TrackedBranchContext(
        config=config,
        x_mesh=x_mesh,
        anchor_load_mpa=float(TRACKED_BRANCH_ANCHOR_MPA),
        anchor_history_result=anchor_history_result,
        anchor_realized_result=anchor_realized_result,
        branch_source=branch_source,
        history_run_dir=history_run_dir,
    )


def solve_with_previous_guess(
    q_mpa: float,
    config: base.AxisymmetricSimpleSupportConfig,
    x_mesh: np.ndarray,
    previous_success: base.AxisymmetricBackgroundSolve,
) -> base.AxisymmetricBackgroundSolve:
    previous_guess = previous_success.solution.sol(x_mesh)
    return base.solve_axisymmetric_simple_support_fixed_load(
        q_mpa,
        config=config,
        initial_guess=previous_guess,
    )


def build_local_restart_grid(start_q: float, target_q: float, step_mpa: float = LOCAL_RESTART_STEP_MPA) -> np.ndarray:
    start_q = float(start_q)
    target_q = float(target_q)
    if abs(target_q - start_q) <= 1.0e-12:
        return np.asarray([start_q], dtype=float)

    direction = 1.0 if target_q > start_q else -1.0
    q_values = [start_q]
    q_value = start_q
    while True:
        next_q = q_value + direction * float(step_mpa)
        if (direction > 0.0 and next_q >= target_q - 1.0e-12) or (direction < 0.0 and next_q <= target_q + 1.0e-12):
            break
        q_value = round_load(next_q)
        q_values.append(float(q_value))
    if abs(q_values[-1] - target_q) > 1.0e-12:
        q_values.append(float(target_q))
    return np.asarray(q_values, dtype=float)


def attempt_same_branch_refinement(
    start_result: base.AxisymmetricBackgroundSolve,
    target_q_mpa: float,
    context: TrackedBranchContext,
) -> base.AxisymmetricBackgroundSolve | None:
    if not start_result.success or start_result.solution is None:
        return None

    local_grid = build_local_restart_grid(start_result.q_mpa, target_q_mpa)
    local_previous = start_result
    local_target_result: base.AxisymmetricBackgroundSolve | None = start_result

    for q_local in local_grid[1:]:
        local_result = solve_with_previous_guess(q_local, context.config, context.x_mesh, local_previous)
        if not local_result.success:
            return None
        local_previous = local_result
        local_target_result = local_result

    return local_target_result


def solve_directional_schedule(
    target_loads: list[float],
    context: TrackedBranchContext,
    *,
    allow_repair: bool,
) -> list[BackgroundStep]:
    steps: list[BackgroundStep] = []
    previous_success = context.anchor_realized_result

    for target_q in target_loads:
        warm_result = solve_with_previous_guess(target_q, context.config, context.x_mesh, previous_success)
        if warm_result.success:
            step = BackgroundStep(
                result=warm_result,
                solve_mode="warm_start",
                warm_start_attempted=True,
                recovered_after_warm_failure=False,
            )
            steps.append(step)
            previous_success = warm_result
            continue

        if allow_repair:
            repaired_result = attempt_same_branch_refinement(previous_success, target_q, context)
            if repaired_result is None and abs(previous_success.q_mpa - context.anchor_realized_result.q_mpa) > 1.0e-12:
                repaired_result = attempt_same_branch_refinement(context.anchor_realized_result, target_q, context)
            if repaired_result is not None and repaired_result.success:
                step = BackgroundStep(
                    result=repaired_result,
                    solve_mode="local_restart",
                    warm_start_attempted=True,
                    recovered_after_warm_failure=True,
                )
                steps.append(step)
                previous_success = repaired_result
                continue

        step = BackgroundStep(
            result=warm_result,
            solve_mode="failure",
            warm_start_attempted=True,
            recovered_after_warm_failure=False,
        )
        steps.append(step)

    return steps


def solve_simple_support_background_schedule_tracked_branch(
    p_list: np.ndarray,
    x0: float,
    *,
    allow_repair: bool,
    context: TrackedBranchContext | None = None,
) -> tuple[list[BackgroundStep], TrackedBranchContext]:
    context = build_tracked_branch_context(x0) if context is None else context
    requested = unique_sorted(np.asarray(p_list, dtype=float))
    anchor_q = float(context.anchor_load_mpa)

    lower_targets = sorted((q for q in requested if q < anchor_q - 1.0e-12), reverse=True)
    upper_targets = sorted(q for q in requested if q > anchor_q + 1.0e-12)

    lower_steps = solve_directional_schedule(lower_targets, context, allow_repair=allow_repair)
    upper_steps = solve_directional_schedule(upper_targets, context, allow_repair=allow_repair)

    step_map: dict[float, BackgroundStep] = {
        round_load(context.anchor_realized_result.q_mpa): BackgroundStep(
            result=context.anchor_realized_result,
            solve_mode="tracked_branch_anchor",
            warm_start_attempted=False,
            recovered_after_warm_failure=False,
        )
    }
    step_map.update({round_load(step.result.q_mpa): step for step in lower_steps})
    step_map.update({round_load(step.result.q_mpa): step for step in upper_steps})

    ordered_steps = [step_map[round_load(p_mpa)] for p_mpa in np.asarray(p_list, dtype=float)]
    return ordered_steps, context


def solve_simple_support_background_schedule_repaired(
    p_list: np.ndarray,
    x0: float,
) -> tuple[list[BackgroundStep], base.AxisymmetricSimpleSupportConfig]:
    steps, context = solve_simple_support_background_schedule_tracked_branch(
        p_list,
        x0,
        allow_repair=True,
        context=None,
    )
    return steps, context.config


def build_branch_a_history_low_targets(p_list: np.ndarray) -> list[float]:
    sampled_low_targets = [
        round_load(q_mpa)
        for q_mpa in np.asarray(p_list, dtype=float)
        if float(q_mpa) < BRANCH_A_IDENTITY_LOSS_LOAD_MPA - 1.0e-12
    ]
    sampled_low_targets = unique_sorted(sampled_low_targets)
    if not sampled_low_targets:
        return []
    if sampled_low_targets[0] > BRANCH_A_LOW_HISTORY_START_MPA + 1.0e-12:
        return unique_sorted([BRANCH_A_LOW_HISTORY_START_MPA] + sampled_low_targets)
    return sampled_low_targets


def solve_natural_branch_a_low_history(
    p_list: np.ndarray,
    context: TrackedBranchContext,
) -> tuple[dict[float, base.AxisymmetricBackgroundSolve], list[base.AxisymmetricBackgroundSolve], float | None, float | None]:
    low_targets = build_branch_a_history_low_targets(p_list)
    if not low_targets:
        return {}, [], None, None

    low_history_config = tracked_bg.low_load_direct_config(context.config)
    results = simple_bg.solve_axisymmetric_simple_support_continuation(low_targets, config=low_history_config)
    result_map = {
        round_load(result.q_mpa): result
        for result in results
        if result.success and result.solution is not None
    }
    sampled_targets = [
        round_load(q_mpa)
        for q_mpa in np.asarray(p_list, dtype=float)
        if float(q_mpa) < BRANCH_A_IDENTITY_LOSS_LOAD_MPA - 1.0e-12
    ]
    sampled_targets = unique_sorted(sampled_targets)
    missing = [q_mpa for q_mpa in sampled_targets if round_load(q_mpa) not in result_map]
    if missing:
        raise RuntimeError(
            "Could not realize the low-load Branch-A determinant history on all sampled pre-jump loads: "
            f"{missing}"
        )

    last_a_sampled = float(sampled_targets[-1]) if sampled_targets else None
    first_merged_sampled = next(
        (float(q_mpa) for q_mpa in np.asarray(p_list, dtype=float) if float(q_mpa) >= BRANCH_A_IDENTITY_LOSS_LOAD_MPA - 1.0e-12),
        None,
    )
    return result_map, results, last_a_sampled, first_merged_sampled


def merge_branch_a_to_tracked_b_schedule(
    p_list: np.ndarray,
    tracked_steps: list[BackgroundStep],
    context: TrackedBranchContext,
) -> tuple[list[BackgroundStep], float | None, float | None]:
    tracked_map = {round_load(step.result.q_mpa): step for step in tracked_steps}
    branch_a_map, _, last_a_sampled, first_merged_sampled = solve_natural_branch_a_low_history(p_list, context)

    merged_steps: list[BackgroundStep] = []
    for q_mpa in np.asarray(p_list, dtype=float):
        q_key = round_load(q_mpa)
        if float(q_mpa) < BRANCH_A_IDENTITY_LOSS_LOAD_MPA - 1.0e-12:
            result = branch_a_map[q_key]
            merged_steps.append(
                BackgroundStep(
                    result=result,
                    solve_mode="branch_a_low_natural",
                    warm_start_attempted=result.seed_kind != "zero_guess",
                    recovered_after_warm_failure=False,
                )
            )
            continue

        tracked_step = tracked_map[q_key]
        merged_steps.append(
            BackgroundStep(
                result=tracked_step.result,
                solve_mode="branch_a_to_b_merge",
                warm_start_attempted=tracked_step.warm_start_attempted,
                recovered_after_warm_failure=tracked_step.recovered_after_warm_failure,
            )
        )

    return merged_steps, last_a_sampled, first_merged_sampled


def recovered_points_count(steps: list[BackgroundStep]) -> int:
    return int(sum(1 for step in steps if step.recovered_after_warm_failure and step.result.success))

def evaluate_background_solution(result: base.AxisymmetricBackgroundSolve, x_det: np.ndarray) -> np.ndarray | None:
    if result.solution is None:
        return None
    try:
        values = np.asarray(result.solution.sol(x_det), dtype=float)
    except Exception:
        return None
    return values


def arrays_simple_support_background_safe(
    result: base.AxisymmetricBackgroundSolve,
    x_det: np.ndarray,
) -> tuple[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray] | None, bool]:
    try:
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            arrays = base.arrays_simple_support_background(result, x_det)
    except Exception:
        return None, False

    arrays = tuple(np.asarray(arr, dtype=float) for arr in arrays)
    all_finite = bool(all(np.all(np.isfinite(arr)) for arr in arrays))
    return arrays, all_finite


def build_gap_diagnostic_row(
    p_mpa: float,
    result: base.AxisymmetricBackgroundSolve,
    solve_mode: str,
    x_det: np.ndarray,
    delta: float,
    n_wave: int,
) -> dict[str, object]:
    row: dict[str, object] = {
        "p": float(p_mpa),
        "solve_mode": str(solve_mode),
        "background_success": bool(result.success),
        "background_failure_reason": result.message if not result.success else "",
        "background_nodes": int(result.nodes),
        "background_residual": background_residual_metric(result),
        "background_all_finite": False,
        "adapter_all_finite": False,
        "det_inputs_all_finite": False,
        "det_value": float("nan"),
        "plot_point_used": False,
        "missing_reason": "background_failure" if not result.success else "filtered_out",
    }

    if not result.success:
        return row

    y_background = evaluate_background_solution(result, x_det)
    if y_background is None or not np.all(np.isfinite(y_background)):
        row["missing_reason"] = "background_nonfinite"
        return row

    row["background_all_finite"] = True

    arrays, adapter_all_finite = arrays_simple_support_background_safe(result, x_det)
    row["adapter_all_finite"] = bool(adapter_all_finite)
    if arrays is None or not adapter_all_finite:
        row["missing_reason"] = "adapter_nonfinite"
        return row

    theta, dtheta, dphi, phi_p = arrays
    det_inputs_all_finite = bool(
        np.all(np.isfinite(theta))
        and np.all(np.isfinite(dtheta))
        and np.all(np.isfinite(dphi))
        and np.all(np.isfinite(phi_p))
        and np.isfinite(delta)
    )
    row["det_inputs_all_finite"] = det_inputs_all_finite
    if not det_inputs_all_finite:
        row["missing_reason"] = "determinant_nonfinite"
        return row

    sign, logabs = base.det_UN_slog(theta, dtheta, dphi, phi_p, delta, n_wave)
    det_value = signed_det_from_slog(sign, logabs)
    row["det_value"] = float(det_value) if np.isfinite(det_value) else float("nan")
    if not np.isfinite(det_value):
        row["missing_reason"] = "determinant_nonfinite"
        return row

    row["plot_point_used"] = True
    row["missing_reason"] = "ok"
    return row


def save_gap_diagnostic_csv(rows: list[dict[str, object]], filename: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=DIAGNOSTIC_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in DIAGNOSTIC_FIELDNAMES})
    return path


def build_gap_summary(rows: list[dict[str, object]]) -> list[str]:
    lines: list[str] = []
    problem_indices = [i for i, row in enumerate(rows) if row["missing_reason"] != "ok"]
    if not problem_indices:
        lines.append("first problematic point: none")
        lines.append("last problematic point: none")
        lines.append("first successful point after gap: not needed (no gap detected)")
        lines.append("gap stage: none")
        return lines

    first_idx = problem_indices[0]
    last_idx = first_idx
    while last_idx + 1 < len(rows) and rows[last_idx + 1]["missing_reason"] != "ok":
        last_idx += 1

    recovery_idx = next((j for j in range(last_idx + 1, len(rows)) if rows[j]["missing_reason"] == "ok"), None)
    gap_reasons = [str(rows[j]["missing_reason"]) for j in range(first_idx, last_idx + 1)]
    gap_stage = gap_reasons[0] if len(set(gap_reasons)) == 1 else "mixed: " + ", ".join(sorted(set(gap_reasons)))

    first_row = rows[first_idx]
    last_row = rows[last_idx]
    lines.append(f"first problematic point: p={float(first_row['p']):.3f} MPa, missing_reason={first_row['missing_reason']}")
    lines.append(f"last problematic point: p={float(last_row['p']):.3f} MPa, missing_reason={last_row['missing_reason']}")
    if recovery_idx is None:
        lines.append("first successful point after gap: none on sampled loads")
    else:
        recovery_row = rows[recovery_idx]
        lines.append(f"first successful point after gap: p={float(recovery_row['p']):.3f} MPa")
    lines.append(f"gap stage: {gap_stage}")
    return lines


def save_gap_diagnostic_plot(rows: list[dict[str, object]], filename: str, n_wave: int) -> Path:
    p_values = np.array([float(row["p"]) for row in rows], dtype=float)
    background_success = np.array([bool(row["background_success"]) for row in rows], dtype=bool)
    background_missing = np.array(
        [row["missing_reason"] in {"background_failure", "background_nonfinite"} for row in rows],
        dtype=bool,
    )
    adapter_missing = np.array([row["missing_reason"] == "adapter_nonfinite" for row in rows], dtype=bool)
    determinant_missing = np.array([row["missing_reason"] == "determinant_nonfinite" for row in rows], dtype=bool)
    filtered_missing = np.array([row["missing_reason"] == "filtered_out" for row in rows], dtype=bool)

    fig, ax = plt.subplots(figsize=(11, 4.8))
    if np.any(background_success):
        ax.plot(p_values[background_success], np.zeros(np.count_nonzero(background_success)), linestyle="None", marker="o", markersize=5, color="tab:green", label="background success")
    if np.any(background_missing):
        ax.plot(p_values[background_missing], np.ones(np.count_nonzero(background_missing)), linestyle="None", marker="x", markersize=6, markeredgewidth=1.4, color="tab:red", label="background failure")
    if np.any(adapter_missing):
        ax.plot(p_values[adapter_missing], np.full(np.count_nonzero(adapter_missing), 2.0), linestyle="None", marker="s", markersize=5.5, color="tab:orange", label="adapter failure")
    if np.any(determinant_missing):
        ax.plot(p_values[determinant_missing], np.full(np.count_nonzero(determinant_missing), 3.0), linestyle="None", marker="^", markersize=6, color="tab:purple", label="determinant failure")
    if np.any(filtered_missing):
        ax.plot(p_values[filtered_missing], np.full(np.count_nonzero(filtered_missing), 4.0), linestyle="None", marker="D", markersize=5, color="tab:gray", label="filtered out")

    ax.set_yticks([0.0, 1.0, 2.0, 3.0, 4.0])
    ax.set_yticklabels(["background success", "background failure", "adapter failure", "determinant failure", "filtered out"])
    ax.set_xlabel("p, MPa")
    ax.set_title(f"Tracked-branch diagnostic: non-shallow simple-support path, n = {int(n_wave)}")
    ax.grid(True, axis="x")
    ax.legend(loc="upper left")
    fig.tight_layout()
    return save_figure(fig, filename)


def comparison_axes(n_panels: int) -> tuple[plt.Figure, np.ndarray]:
    n_cols = min(3, max(1, int(n_panels)))
    n_rows = int(np.ceil(float(n_panels) / float(n_cols)))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5.0 * n_cols, 4.8 * n_rows), sharex=True, sharey=True)
    axes_arr = np.atleast_1d(axes).ravel()
    for ax in axes_arr[n_panels:]:
        ax.set_visible(False)
    return fig, axes_arr[:n_panels]

def run_gap_diagnostic(n_wave: int, p_list: np.ndarray, nd_det: int) -> None:
    x_det, delta = base.build_det_grid(nd_det)
    r0 = x_det[0]

    baseline_steps, context = solve_simple_support_background_schedule_tracked_branch(
        p_list,
        r0,
        allow_repair=False,
        context=None,
    )
    repaired_steps, context = solve_simple_support_background_schedule_tracked_branch(
        p_list,
        r0,
        allow_repair=True,
        context=context,
    )
    baseline_results = [step.result for step in baseline_steps]
    repaired_results = [step.result for step in repaired_steps]

    print("=== Narrow non-shallow tracked-branch diagnostic: simple support ===")
    print("diagnostic scope: honest simple-support background only; no shallow branch")
    print("criterion path: legacy determinant adapter on the honest simple-support background")
    print("non-shallow background source: shell_buckling.mixed_weak.axisymmetric_simple_support_background")
    print("tracked branch source: shell_buckling.mixed_weak.simple_support_high_load_background_continuation")
    print(f"state: {list(base.SIMPLE_SUPPORT_STATE_LABELS)}")
    print(f"BCs:   {list(base.SIMPLE_SUPPORT_BC_LABELS)}")
    print(
        "background config: "
        f"x0={context.config.x0:.6f}, nd_bvp={context.config.nd_bvp}, tol={context.config.tol:.1e}, "
        f"relaxed_tol={context.config.relaxed_tol:.1e}, max_nodes={context.config.max_nodes}"
    )
    print(f"tracked branch anchor: q={context.anchor_load_mpa:.3f} MPa, seed={context.anchor_history_result.seed_kind}")
    print(f"pressure range: {p_list[0]:.3f}..{p_list[-1]:.3f} MPa with {len(p_list)} points")
    print(f"diagnostic n: {int(n_wave)}")
    print()

    rows = [
        build_gap_diagnostic_row(float(p_mpa), step.result, step.solve_mode, x_det, delta, n_wave)
        for p_mpa, step in zip(p_list, repaired_steps)
    ]

    stem = diagnostic_stem(n_wave, p_list)
    csv_path = save_gap_diagnostic_csv(rows, stem + ".csv")
    plot_path = save_gap_diagnostic_plot(rows, stem + ".png", n_wave)

    before_failed_points = [result.q_mpa for result in baseline_results if not result.success]
    first_failed_before = before_failed_points[0] if before_failed_points else None
    recovered_count = recovered_points_count(repaired_steps)
    remaining_failed_points = [result.q_mpa for result in repaired_results if not result.success]

    gap_removed = False
    if before_failed_points:
        gap_start = before_failed_points[0]
        gap_end = before_failed_points[-1]
        gap_removed = not any(
            (not step.result.success) and (gap_start - 1.0e-12 <= step.result.q_mpa <= gap_end + 1.0e-12)
            for step in repaired_steps
        )
    else:
        gap_start = float("nan")
        gap_end = float("nan")
        gap_removed = True

    for line in build_gap_summary(rows):
        print(line)
    print("first failed point before fix: " + (f"p={first_failed_before:.3f} MPa" if first_failed_before is not None else "none"))
    print(f"failed points before fix: {len(before_failed_points)}")
    print(f"recovered points count: {recovered_count}")
    print(f"remaining failed points count: {len(remaining_failed_points)}")
    if before_failed_points:
        print(f"gap on {gap_start:.3f}..{gap_end:.3f} MPa removed: {'yes' if gap_removed else 'no'}")
    else:
        print("gap on failed interval removed: not needed (no failures before fix)")
    print(f"full-scan continuity restored: {'yes' if not remaining_failed_points else 'no'}")
    print(f"branch source: {context.branch_source}")
    print(f"diagnostic csv:  {csv_path}")
    print(f"diagnostic plot: {plot_path}")


def run_standard_scan(n_list: list[int], p_list: np.ndarray, nd_det: int) -> None:
    x_det, delta = base.build_det_grid(nd_det)
    r0 = x_det[0]

    xS_mesh = np.linspace(r0, 1.0, 1500)
    solsS = base.solve_shallow_schedule(p_list, xS_mesh)

    baseline_steps, context = solve_simple_support_background_schedule_tracked_branch(
        p_list,
        r0,
        allow_repair=False,
        context=None,
    )
    solsN_steps, context = solve_simple_support_background_schedule_tracked_branch(
        p_list,
        r0,
        allow_repair=True,
        context=context,
    )
    baseline_results = [step.result for step in baseline_steps]
    solsN = [step.result for step in solsN_steps]
    solsA_history_steps, branch_a_last_distinct_sampled, branch_a_first_merged_sampled = merge_branch_a_to_tracked_b_schedule(
        p_list,
        solsN_steps,
        context,
    )
    solsA_history = [step.result for step in solsA_history_steps]

    success_loads = [result.q_mpa for result in solsN if result.success]
    failed_loads = [result.q_mpa for result in solsN if not result.success]
    before_failed_loads = [result.q_mpa for result in baseline_results if not result.success]
    recovered_count = recovered_points_count(solsN_steps)
    last_success = success_loads[-1] if success_loads else float("nan")
    first_failure = failed_loads[0] if failed_loads else float("nan")
    n_label = format_n_list_text(n_list)

    print(f"=== Supporting determinant comparison: simple support, n = {n_label}, tracked-branch high-load scan ===")
    print("main plotted quantity: signed det U_N(p)")
    print("auxiliary diagnostic: log|det U_N(p)|")
    print("non-shallow background source: shell_buckling.mixed_weak.axisymmetric_simple_support_background")
    print("tracked branch source: shell_buckling.mixed_weak.simple_support_high_load_background_continuation")
    print(f"state: {list(base.SIMPLE_SUPPORT_STATE_LABELS)}")
    print(f"BCs:   {list(base.SIMPLE_SUPPORT_BC_LABELS)}")
    print(
        "background config: "
        f"x0={context.config.x0:.6f}, nd_bvp={context.config.nd_bvp}, tol={context.config.tol:.1e}, "
        f"relaxed_tol={context.config.relaxed_tol:.1e}, max_nodes={context.config.max_nodes}"
    )
    print(f"tracked branch anchor on determinant mesh: q={context.anchor_load_mpa:.3f} MPa")
    print(f"tracked history anchor seed: {context.anchor_history_result.seed_kind}")
    print(f"pressure range: {p_list[0]:.3f}..{p_list[-1]:.3f} MPa with {len(p_list)} points")
    print(f"n list: {n_list}")
    print(f"branch source statement: {context.branch_source}")
    print("independent fixed-load solves used as main background source: no")
    print(f"tracked-branch background last_success={last_success:.3f} MPa")
    print(f"failed points before repair={len(before_failed_loads)}")
    print(f"recovered via local restart={recovered_count}")
    if failed_loads:
        print(f"tracked-branch background first_failure={first_failure:.3f} MPa; failed load count after repair={len(failed_loads)}")
        print("non-shallow failed loads are marked on the plots with red x symbols")
    else:
        print("tracked-branch background: no failed loads on this scan")
    print(
        "Branch A -> B determinant curve source: natural near-zero-start Branch-A history on sampled loads below "
        f"the audited A-identity-loss load {BRANCH_A_IDENTITY_LOSS_LOAD_MPA:.4f} MPa, then the unchanged tracked Branch-B history above it"
    )
    print(
        "audited Branch-A distinct interval used for the splice: "
        f"A separate through {BRANCH_A_LAST_DISTINCT_LOAD_MPA:.5f} MPa, identity-loss / jump at about {BRANCH_A_IDENTITY_LOSS_LOAD_MPA:.4f} MPa"
    )
    if branch_a_last_distinct_sampled is not None:
        print(f"on the current sampled grid the A-specific determinant points extend through p={branch_a_last_distinct_sampled:.3f} MPa")
    if branch_a_first_merged_sampled is not None:
        print(f"on the current sampled grid the merged tracked-B segment begins at p={branch_a_first_merged_sampled:.3f} MPa")
    print()

    det_sh_all = {}
    det_ne_all = {}
    det_ne_a_hist_all = {}
    logabs_sh_all = {}
    logabs_ne_all = {}
    logabs_ne_a_hist_all = {}
    sign_sh_all = {}
    sign_ne_all = {}
    sign_ne_a_hist_all = {}

    for n_wave in n_list:
        det_sh = np.full_like(p_list, np.nan)
        det_ne = np.full_like(p_list, np.nan)
        det_ne_a_hist = np.full_like(p_list, np.nan)
        logabs_sh = np.full_like(p_list, np.nan)
        logabs_ne = np.full_like(p_list, np.nan)
        logabs_ne_a_hist = np.full_like(p_list, np.nan)
        sign_sh = np.full_like(p_list, np.nan)
        sign_ne = np.full_like(p_list, np.nan)
        sign_ne_a_hist = np.full_like(p_list, np.nan)

        for i in range(len(p_list)):
            thS, dthS, dPhiS, PhiS = base.arrays_shallow(solsS[i], x_det)
            signS, laS = base.det_UN_slog(thS, dthS, dPhiS, PhiS, delta, n_wave)
            det_sh[i] = signed_det_from_slog(signS, laS)
            logabs_sh[i] = laS
            sign_sh[i] = sign_indicator_from_slog(signS, laS)

            if solsN[i].success and solsN[i].solution is not None:
                thN, dthN, dPhiN, PhiN = base.arrays_simple_support_background(solsN[i], x_det)
                signN, laN = base.det_UN_slog(thN, dthN, dPhiN, PhiN, delta, n_wave)
                det_ne[i] = signed_det_from_slog(signN, laN)
                logabs_ne[i] = laN
                sign_ne[i] = sign_indicator_from_slog(signN, laN)

            if solsA_history[i].success and solsA_history[i].solution is not None:
                thA, dthA, dPhiA, PhiA = base.arrays_simple_support_background(solsA_history[i], x_det)
                signA, laA = base.det_UN_slog(thA, dthA, dPhiA, PhiA, delta, n_wave)
                det_ne_a_hist[i] = signed_det_from_slog(signA, laA)
                logabs_ne_a_hist[i] = laA
                sign_ne_a_hist[i] = sign_indicator_from_slog(signA, laA)

        det_sh_all[n_wave] = det_sh
        det_ne_all[n_wave] = det_ne
        det_ne_a_hist_all[n_wave] = det_ne_a_hist
        logabs_sh_all[n_wave] = logabs_sh
        logabs_ne_all[n_wave] = logabs_ne
        logabs_ne_a_hist_all[n_wave] = logabs_ne_a_hist
        sign_sh_all[n_wave] = sign_sh
        sign_ne_all[n_wave] = sign_ne
        sign_ne_a_hist_all[n_wave] = sign_ne_a_hist

        p_sh, la_sh, j_sh = best_p_by_minlog_with_index(p_list, logabs_sh)
        p_ne, la_ne, j_ne = best_p_by_minlog_with_index(p_list, logabs_ne)
        p_ne_a_hist, la_ne_a_hist, j_ne_a_hist = best_p_by_minlog_with_index(p_list, logabs_ne_a_hist)

        print(f"n={n_wave}")
        print("  " + format_sign_line("shallow", p_list, sign_sh, logabs_sh))
        print("  " + format_sign_line("non-shallow tracked branch", p_list, sign_ne, logabs_ne))
        print("  " + format_sign_line("non-shallow Branch A -> B", p_list, sign_ne_a_hist, logabs_ne_a_hist))
        print("  " + format_min_line("shallow auxiliary", p_sh, la_sh, j_sh, p_list))
        print("  " + format_min_line("non-shallow tracked auxiliary", p_ne, la_ne, j_ne, p_list))
        print("  " + format_min_line("non-shallow Branch A -> B auxiliary", p_ne_a_hist, la_ne_a_hist, j_ne_a_hist, p_list))
        print(f"  tracked-branch background failed points before/after repair: {len(before_failed_loads)}/{len(failed_loads)}")
        print()

    fig1, ax1 = plt.subplots(figsize=(9, 6))
    for n_wave in n_list:
        ax1.plot(p_list, det_ne_all[n_wave], label=f"non-shallow tracked branch, n={n_wave}")
    ax1.axhline(0.0, color="black", linewidth=1.0)
    mark_failed_loads(ax1, failed_loads, label="tracked-branch bg failed")
    ax1.grid(True)
    ax1.set_xlabel("p, MPa")
    ax1.set_ylabel("det U_N")
    ax1.set_title(f"Signed determinant scan: non-shallow tracked-branch simple-support background, n = {n_label}")
    ax1.legend()
    fig1.tight_layout()
    fig1_path = save_figure(fig1, f"determinant_scan_non_shallow_simple_support_tracked_branch_n{n_label.replace(',', '')}.png")

    fig2, axes = comparison_axes(len(n_list))
    for j_ax, (ax, n_wave) in enumerate(zip(axes, n_list)):
        ax.plot(p_list, det_sh_all[n_wave], label="shallow")
        ax.plot(p_list, det_ne_all[n_wave], label="non-shallow tracked branch")
        ax.axhline(0.0, color="black", linewidth=1.0)
        mark_failed_loads(ax, failed_loads, label="tracked-branch bg failed" if j_ax == 0 else None)
        ax.set_title(f"n = {n_wave}")
        ax.grid(True)
    axes[0].legend()
    fig2.supxlabel("p, MPa")
    fig2.supylabel("det U_N")
    fig2.suptitle(f"Comparison of signed determinant scans: shallow vs tracked-branch non-shallow simple support (n = {n_label})")
    fig2.tight_layout()
    fig2_path = save_figure(fig2, f"determinant_scan_comparison_simple_support_tracked_branch_n{n_label.replace(',', '')}.png")

    fig3, axes = comparison_axes(len(n_list))
    for j_ax, (ax, n_wave) in enumerate(zip(axes, n_list)):
        ax.plot(p_list, det_sh_all[n_wave], label="shallow")
        ax.plot(p_list, det_ne_all[n_wave], label="non-shallow Branch B (tracked)")
        ax.plot(p_list, det_ne_a_hist_all[n_wave], label="non-shallow Branch A -> B")
        ax.axvline(
            BRANCH_A_IDENTITY_LOSS_LOAD_MPA,
            color="0.35",
            linewidth=1.0,
            linestyle="--",
            label="A identity loss ~4.341 MPa" if j_ax == 0 else None,
        )
        ax.axhline(0.0, color="black", linewidth=1.0)
        mark_failed_loads(ax, failed_loads, label="tracked-branch bg failed" if j_ax == 0 else None)
        ax.set_title(f"n = {n_wave}")
        ax.grid(True)
    axes[0].legend()
    fig3.supxlabel("p, MPa")
    fig3.supylabel("det U_N")
    fig3.suptitle(
        f"Comparison of signed determinant scans: shallow vs non-shallow Branch B and Branch A -> B simple support (n = {n_label})"
    )
    fig3.tight_layout()
    fig3_path = save_figure(fig3, f"determinant_scan_comparison_simple_support_branchA_and_trackedB_n{n_label.replace(',', '')}.png")

    print("saved figures:")
    print(f"  {fig1_path}")
    print(f"  {fig2_path}")
    print(f"  {fig3_path}")


def main(argv: list[str] | None = None):
    args = parse_args(argv)
    p_list = build_pressure_grid(args.p_min, args.p_max, args.num_points)
    n_list = [int(n_wave) for n_wave in args.n_list]

    if args.diagnose_gap:
        run_gap_diagnostic(n_list[0], p_list, args.nd_det)
    else:
        run_standard_scan(n_list, p_list, args.nd_det)


if __name__ == "__main__":
    main()
