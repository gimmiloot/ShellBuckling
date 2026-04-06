from __future__ import annotations

import csv
import importlib.util
import json
import sys
import warnings
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

OUTPUT_DIR = REPO_ROOT / "output" / "axisymmetric_simple_support_natural_branch_selection_audit"
PREV_AUDIT_PATH = REPO_ROOT / "experiments" / "supporting" / "run_axisymmetric_simple_support_branch_b_continuation_audit.py"

NATURAL_LOADS_MPA = (
    0.0,
    0.05,
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.75,
    1.00,
    1.25,
    1.50,
    1.75,
    2.00,
    2.50,
    3.00,
    3.50,
    4.00,
    4.10,
    4.20,
    4.25,
    4.30,
    4.325,
    4.330,
    4.335,
    4.338,
    4.339,
    4.340,
    4.3405,
    4.34095,
    4.3410,
    4.3415,
    4.3420,
    4.3430,
    4.3440,
    4.3450,
    4.3500,
    4.4000,
    4.5000,
)
A_REFERENCE_MAX_MPA = 4.34095
B_HISTORY_SEED_MPA = 4.3500
REFERENCE_REPAIR_MIN_STEP = 0.0005
REFERENCE_A_BOOTSTRAP_STEP = 0.05
REFERENCE_B_BOOTSTRAP_STEP = 0.005
ND_EVAL = 2000
CSV_FIELDS = [
    "run_mode", "q_mpa", "background_success", "solve_mode", "seed_kind", "tried_seeds", "repair_depth",
    "nodes", "max_rms", "max_bc_residual", "min_r", "message", "u_z_center", "varphi_edge", "T_s_center",
    "min_M_s", "min_M_theta", "state_norm_l2", "delta_prev_abs_l2", "delta_prev_rel_l2", "continuity_jump_ratio",
    "branch_jump_suspicion", "branch_jump_reason", "distance_to_A_abs_l2", "distance_to_A_rel_l2",
    "distance_to_A_marker_rel_max", "distance_to_B_abs_l2", "distance_to_B_rel_l2", "distance_to_B_marker_rel_max",
    "diff_u_z_center_to_A", "diff_varphi_edge_to_A", "diff_T_s_center_to_A", "diff_min_M_s_to_A", "diff_min_M_theta_to_A",
    "diff_u_z_center_to_B", "diff_varphi_edge_to_B", "diff_T_s_center_to_B", "diff_min_M_s_to_B", "diff_min_M_theta_to_B",
    "closer_reference_branch",
]


class NaturalMode:
    def __init__(self, label: str, use_secant: bool):
        self.label = str(label)
        self.use_secant = bool(use_secant)


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


prev = load_module("natural_branch_selection_prev_audit", PREV_AUDIT_PATH)


def save_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in CSV_FIELDS})


def save_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def float_tag(value: float) -> str:
    return f"{float(value):.4f}".replace("-", "m").replace(".", "p")


def build_reference_args() -> Any:
    return prev.argparse.Namespace(
        start_load=0.0,
        window1_end=4.3600,
        window2_end=4.5000,
        end_load=4.5000,
        window1_step=0.005,
        window2_step=0.005,
        window3_step=0.005,
        a_bootstrap_start=0.0,
        a_bootstrap_step=REFERENCE_A_BOOTSTRAP_STEP,
        b_history_seed=B_HISTORY_SEED_MPA,
        b_bootstrap_step=REFERENCE_B_BOOTSTRAP_STEP,
        repair_min_step=REFERENCE_REPAIR_MIN_STEP,
        nd_eval=ND_EVAL,
    )


def natural_config() -> Any:
    return prev.high_bg.default_high_load_background_config(prev.high_bg.DEFAULT_HISTORY_RUN_DIR)


def common_x_eval(local_group: list[Any], high_group: list[Any], config: Any, nd_eval: int) -> np.ndarray:
    x0 = max([float(config.x0)] + [float(profile.config.x0) for profile in local_group + high_group])
    return np.linspace(x0, 1.0, int(nd_eval))


def unique_success_map(steps: list[Any]) -> dict[float, Any]:
    return {prev.round_load(step.q_mpa): step for step in steps if step.background_success and step.state_eval is not None}


def build_a_reference(loads_mpa: tuple[float, ...], args: Any, local_group: list[Any], high_group: list[Any], x_eval: np.ndarray) -> tuple[dict[float, Any], list[Any]]:
    a_start = prev.build_branch_a_start(args, local_group, x_eval)
    requested = [float(q) for q in loads_mpa if float(q) <= float(A_REFERENCE_MAX_MPA) + 1.0e-12]
    a_steps = prev.continue_branch("A", a_start, requested, args, local_group, high_group, x_eval, stop_on_jump=True)
    a_map = {
        prev.round_load(step.q_mpa): step
        for step in a_steps
        if step.background_success and not step.branch_jump_suspicion and step.state_eval is not None
    }
    missing = [q for q in requested if prev.round_load(q) not in a_map]
    if missing:
        raise RuntimeError(f"Could not realize trustworthy Branch A references at loads: {missing}")
    return a_map, a_steps


def build_b_reference(loads_mpa: tuple[float, ...], args: Any, local_group: list[Any], high_group: list[Any], x_eval: np.ndarray) -> tuple[dict[float, Any], list[Any], Any]:
    history = prev.high_bg.solve_axisymmetric_simple_support_high_load_schedule(
        [B_HISTORY_SEED_MPA],
        history_run_dir=prev.high_bg.DEFAULT_HISTORY_RUN_DIR,
        prefer_established_history=True,
        verbose=False,
    )[0]
    if not history.success or history.solution is None:
        raise RuntimeError(f"Could not recover retained Branch B seed at q={B_HISTORY_SEED_MPA:.4f} MPa: {history.message}")
    start_local = prev.realize_on_local("B", B_HISTORY_SEED_MPA, history, local_group, x_eval, "tracked_history_projection")
    down_loads = [B_HISTORY_SEED_MPA] + [float(q) for q in reversed(loads_mpa) if float(q) < B_HISTORY_SEED_MPA - 1.0e-12]
    up_loads = [B_HISTORY_SEED_MPA] + [float(q) for q in loads_mpa if float(q) > B_HISTORY_SEED_MPA + 1.0e-12]
    down_steps = prev.continue_branch("B", start_local, down_loads, args, local_group, high_group, x_eval, stop_on_jump=False)
    up_steps = prev.continue_branch("B", start_local, up_loads, args, local_group, high_group, x_eval, stop_on_jump=False)
    b_map = unique_success_map(down_steps + up_steps)
    missing = [float(q) for q in loads_mpa if prev.round_load(q) not in b_map]
    if missing:
        raise RuntimeError(f"Could not realize Branch B references at loads: {missing}")
    return b_map, down_steps + up_steps, history


def secant_guess(q_target: float, x_mesh: np.ndarray, previous_step: Any, older_step: Any) -> np.ndarray | None:
    if older_step is None or previous_step.solution is None or older_step.solution is None:
        return None
    dq = float(previous_step.q_mpa) - float(older_step.q_mpa)
    if abs(dq) < 1.0e-14:
        return None
    y_prev = np.asarray(previous_step.solution.sol(x_mesh), dtype=float)
    y_old = np.asarray(older_step.solution.sol(x_mesh), dtype=float)
    return y_prev + ((float(q_target) - float(previous_step.q_mpa)) / dq) * (y_prev - y_old)


def attempt_natural_step(q_mpa: float, config: Any, attempts: list[tuple[str, np.ndarray]], x_eval: np.ndarray, mode: NaturalMode) -> Any:
    tried = []
    last_result = prev.simple_bg.AxisymmetricBackgroundSolve(
        q_mpa=float(q_mpa),
        success=False,
        message="No natural attempts were prepared.",
        nodes=0,
        max_rms=float("nan"),
        seed_kind="none",
        max_bc_residual=float("nan"),
        min_r=float("nan"),
        solution=None,
    )
    accepted_seed = "failure"
    for seed_label, guess in attempts:
        tried.append(f"{mode.label}:{seed_label}")
        result = prev.simple_bg.solve_axisymmetric_simple_support_fixed_load(
            q_mpa,
            config=config,
            initial_guess=np.asarray(guess, dtype=float),
        )
        if result.success:
            accepted_seed = seed_label
            return prev.make_step(
                mode.label,
                q_mpa,
                result,
                mode.label,
                "natural_continuation",
                accepted_seed,
                tried,
                0,
                x_eval,
            )
        last_result = result
    return prev.make_step(
        mode.label,
        q_mpa,
        last_result,
        mode.label,
        "natural_continuation",
        accepted_seed,
        tried,
        0,
        x_eval,
    )


def run_natural_continuation(loads_mpa: tuple[float, ...], mode: NaturalMode, config: Any, x_eval: np.ndarray) -> list[Any]:
    x_mesh = prev.simple_bg.default_x_mesh(config)
    steps: list[Any] = []
    older_step = None
    previous_step = None
    delta_history: list[float] = []

    for q_mpa in loads_mpa:
        attempts: list[tuple[str, np.ndarray]] = []
        if abs(float(q_mpa)) < 1.0e-14:
            attempts.append(("zero_guess", prev.simple_bg.zero_guess(x_mesh)))
        else:
            if mode.use_secant and previous_step is not None and older_step is not None:
                guess = secant_guess(q_mpa, x_mesh, previous_step, older_step)
                if guess is not None:
                    attempts.append(("secant_predictor", guess))
            if previous_step is not None and previous_step.solution is not None:
                attempts.append(("previous_solution", np.asarray(previous_step.solution.sol(x_mesh), dtype=float)))
            attempts.append(("zero_guess", prev.simple_bg.zero_guess(x_mesh)))

        step = attempt_natural_step(float(q_mpa), config, attempts, x_eval, mode)
        prev.annotate_continuity(step, previous_step, delta_history, x_eval)
        steps.append(step)
        if not step.background_success:
            break
        older_step, previous_step = previous_step, step
    return steps


def marker_diff_payload(step: Any, ref_step: Any, ref_label: str) -> dict[str, float]:
    return {
        f"diff_u_z_center_to_{ref_label}": float(step.u_z_center - ref_step.u_z_center),
        f"diff_varphi_edge_to_{ref_label}": float(step.varphi_edge - ref_step.varphi_edge),
        f"diff_T_s_center_to_{ref_label}": float(step.T_s_center - ref_step.T_s_center),
        f"diff_min_M_s_to_{ref_label}": float(step.min_M_s - ref_step.min_M_s),
        f"diff_min_M_theta_to_{ref_label}": float(step.min_M_theta - ref_step.min_M_theta),
    }


def compare_row(step: Any, a_map: dict[float, Any], b_map: dict[float, Any], x_eval: np.ndarray) -> dict[str, object]:
    row = {
        "run_mode": str(step.solve_mode),
        "q_mpa": float(step.q_mpa),
        "background_success": bool(step.background_success),
        "solve_mode": str(step.solve_mode),
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
        "distance_to_A_abs_l2": float("nan"),
        "distance_to_A_rel_l2": float("nan"),
        "distance_to_A_marker_rel_max": float("nan"),
        "distance_to_B_abs_l2": float("nan"),
        "distance_to_B_rel_l2": float("nan"),
        "distance_to_B_marker_rel_max": float("nan"),
        "diff_u_z_center_to_A": float("nan"),
        "diff_varphi_edge_to_A": float("nan"),
        "diff_T_s_center_to_A": float("nan"),
        "diff_min_M_s_to_A": float("nan"),
        "diff_min_M_theta_to_A": float("nan"),
        "diff_u_z_center_to_B": float("nan"),
        "diff_varphi_edge_to_B": float("nan"),
        "diff_T_s_center_to_B": float("nan"),
        "diff_min_M_s_to_B": float("nan"),
        "diff_min_M_theta_to_B": float("nan"),
        "closer_reference_branch": "unknown",
    }
    if not step.background_success or step.state_eval is None:
        return row

    q_key = prev.round_load(step.q_mpa)
    a_step = a_map.get(q_key)
    b_step = b_map.get(q_key)

    if a_step is not None:
        abs_a = prev.state_distance(step.state_eval, a_step.state_eval, x_eval)
        rel_a = abs_a / max(a_step.state_norm_l2, 1.0)
        marker_a = prev.marker_rel_max(prev.markers_from_step(step), prev.markers_from_step(a_step))
        row.update(
            {
                "distance_to_A_abs_l2": float(abs_a),
                "distance_to_A_rel_l2": float(rel_a),
                "distance_to_A_marker_rel_max": float(marker_a),
            }
        )
        row.update(marker_diff_payload(step, a_step, "A"))

    if b_step is not None:
        abs_b = prev.state_distance(step.state_eval, b_step.state_eval, x_eval)
        rel_b = abs_b / max(b_step.state_norm_l2, 1.0)
        marker_b = prev.marker_rel_max(prev.markers_from_step(step), prev.markers_from_step(b_step))
        row.update(
            {
                "distance_to_B_abs_l2": float(abs_b),
                "distance_to_B_rel_l2": float(rel_b),
                "distance_to_B_marker_rel_max": float(marker_b),
            }
        )
        row.update(marker_diff_payload(step, b_step, "B"))

    rel_a = row["distance_to_A_rel_l2"]
    rel_b = row["distance_to_B_rel_l2"]
    if np.isfinite(rel_a) and np.isfinite(rel_b):
        if float(rel_a) + 1.0e-12 < float(rel_b):
            row["closer_reference_branch"] = "A"
        elif float(rel_b) + 1.0e-12 < float(rel_a):
            row["closer_reference_branch"] = "B"
        else:
            row["closer_reference_branch"] = "tie"
    elif np.isfinite(rel_a):
        row["closer_reference_branch"] = "A_only_available"
    elif np.isfinite(rel_b):
        row["closer_reference_branch"] = "B_only_available"
    return row


def summarize_mode(rows: list[dict[str, object]]) -> dict[str, object]:
    success_rows = [row for row in rows if bool(row["background_success"])]
    last_success = float(success_rows[-1]["q_mpa"]) if success_rows else None
    first_failure = next((float(row["q_mpa"]) for row in rows if not bool(row["background_success"])), None)
    last_closer_to_A = None
    first_closer_to_B = None
    first_jump = None
    first_B_like_after_A = None

    for row in rows:
        q_mpa = float(row["q_mpa"])
        closer = str(row["closer_reference_branch"])
        if closer == "A":
            last_closer_to_A = q_mpa
        if first_closer_to_B is None and closer == "B":
            first_closer_to_B = q_mpa
        if first_jump is None and bool(row["branch_jump_suspicion"]):
            first_jump = q_mpa
        if (
            first_B_like_after_A is None
            and bool(row["background_success"])
            and np.isfinite(float(row["distance_to_B_rel_l2"]))
            and float(row["distance_to_B_rel_l2"]) <= 1.0e-3
            and (bool(row["branch_jump_suspicion"]) or closer in {"B", "B_only_available"})
        ):
            first_B_like_after_A = q_mpa

    jump_interval = None
    if last_closer_to_A is not None and first_B_like_after_A is not None and first_B_like_after_A >= last_closer_to_A:
        jump_interval = [float(last_closer_to_A), float(first_B_like_after_A)]

    return {
        "run_mode": str(rows[0]["run_mode"]) if rows else "unknown",
        "last_success_mpa": last_success,
        "first_failure_mpa": first_failure,
        "last_closer_to_A_mpa": last_closer_to_A,
        "first_closer_to_B_mpa": first_closer_to_B,
        "first_jump_suspicion_mpa": first_jump,
        "first_B_like_after_A_mpa": first_B_like_after_A,
        "A_identity_loss_interval_mpa": jump_interval,
    }


def verdict_from_summary(summary: dict[str, object]) -> str:
    low_label = "A" if summary["last_closer_to_A_mpa"] is not None else "unknown"
    first_jump = summary["first_jump_suspicion_mpa"]
    first_b_like = summary["first_B_like_after_A_mpa"]
    last_success = summary["last_success_mpa"]
    first_failure = summary["first_failure_mpa"]
    if low_label == "A" and first_jump is not None and first_b_like is not None:
        return (
            f"Natural near-zero-start continuation selects Branch A at low loads and then undergoes a jump / identity loss near "
            f"{float(first_jump):.4f} MPa, landing on the Branch-B side by {float(first_b_like):.4f} MPa."
        )
    if low_label == "A" and last_success is not None and first_failure is not None:
        return (
            f"Natural near-zero-start continuation selects Branch A at low loads, stays far from Branch B through the last successful point "
            f"{float(last_success):.4f} MPa, and then fails at {float(first_failure):.4f} MPa without a detected B-side jump."
        )
    if low_label == "A":
        return "Natural near-zero-start continuation selects Branch A on the checked load window with no detected Branch-B takeover."
    return "Current evidence is insufficient to classify the natural near-zero-start branch selection."


def plot_distances(all_rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10.0, 5.6))
    style = {
        "natural_previous_only": ("tab:blue", "-"),
        "natural_previous_secant": ("tab:red", "--"),
    }
    for run_mode, suffix in (("natural_previous_only", "to A"), ("natural_previous_secant", "to A")):
        rows = [row for row in all_rows if str(row["run_mode"]) == run_mode and bool(row["background_success"]) and np.isfinite(float(row["distance_to_A_rel_l2"]))]
        if not rows:
            continue
        color, linestyle = style[run_mode]
        ax.plot([float(row["q_mpa"]) for row in rows], [float(row["distance_to_A_rel_l2"]) for row in rows], color=color, linestyle=linestyle, linewidth=2.0, label=f"{run_mode} -> A")
    for run_mode, suffix in (("natural_previous_only", "to B"), ("natural_previous_secant", "to B")):
        rows = [row for row in all_rows if str(row["run_mode"]) == run_mode and bool(row["background_success"]) and np.isfinite(float(row["distance_to_B_rel_l2"]))]
        if not rows:
            continue
        color, linestyle = style[run_mode]
        ax.plot([float(row["q_mpa"]) for row in rows], [float(row["distance_to_B_rel_l2"]) for row in rows], color=color, linestyle=":" if run_mode == "natural_previous_only" else "-.", linewidth=2.0, label=f"{run_mode} -> B")
    ax.set_xlabel("p, MPa")
    ax.set_ylabel("relative full-state L2 distance")
    ax.set_title("Natural simple-support continuation: distance to Branch A / Branch B")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_markers(all_rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 1, figsize=(10.0, 8.5), sharex=True)
    style = {
        "natural_previous_only": ("tab:blue", "-"),
        "natural_previous_secant": ("tab:red", "--"),
    }
    for run_mode in style:
        color, linestyle = style[run_mode]
        rows = [row for row in all_rows if str(row["run_mode"]) == run_mode and bool(row["background_success"])]
        if not rows:
            continue
        axes[0].plot([float(row["q_mpa"]) for row in rows], [float(row["u_z_center"]) for row in rows], color=color, linestyle=linestyle, linewidth=2.0, label=run_mode)
        axes[1].plot([float(row["q_mpa"]) for row in rows], [float(row["varphi_edge"]) for row in rows], color=color, linestyle=linestyle, linewidth=2.0, label=run_mode)
    axes[0].set_ylabel("u_z(x0)")
    axes[0].set_title("Natural continuation marker: u_z(x0)")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(loc="best")
    axes[1].set_ylabel("varphi(1)")
    axes[1].set_xlabel("p, MPa")
    axes[1].set_title("Natural continuation marker: varphi(1)")
    axes[1].grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def print_summary(summary: dict[str, object]) -> None:
    print("=== Natural simple-support branch selection audit ===")
    print("primary background source: src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py")
    print("Branch B reference source: src/shell_buckling/mixed_weak/simple_support_high_load_background_continuation.py")
    print(f"loads: {', '.join(f'{value:.5g}' for value in NATURAL_LOADS_MPA)} MPa")
    print(f"Branch B retained history seed for reference only: {summary['branch_b_reference_seed_mpa']:.4f} MPa ({summary['branch_b_reference_seed_kind']})")
    print(f"A reference available through: {summary['a_reference_max_mpa']:.5f} MPa")
    for mode_summary in summary["mode_summaries"]:
        print(f"mode {mode_summary['run_mode']}: {mode_summary['verdict']}")
        print(f"  last closer-to-A load: {mode_summary['last_closer_to_A_mpa']}")
        print(f"  first B-like load: {mode_summary['first_B_like_after_A_mpa']}")
        print(f"  first jump suspicion: {mode_summary['first_jump_suspicion_mpa']}")
    print(f"overall verdict: {summary['overall_verdict']}")
    print(f"csv: {summary['csv_path']}")
    print(f"distance plot: {summary['distance_plot_path']}")
    print(f"marker plot: {summary['marker_plot_path']}")


def main() -> None:
    args = build_reference_args()
    local_group = prev.local_profiles()
    high_group = prev.high_profiles()
    natural_cfg = natural_config()
    x_eval = common_x_eval(local_group, high_group, natural_cfg, ND_EVAL)

    a_map, a_steps = build_a_reference(NATURAL_LOADS_MPA, args, local_group, high_group, x_eval)
    b_map, b_steps, b_history = build_b_reference(NATURAL_LOADS_MPA, args, local_group, high_group, x_eval)

    modes = [
        NaturalMode("natural_previous_only", use_secant=False),
        NaturalMode("natural_previous_secant", use_secant=True),
    ]

    all_rows: list[dict[str, object]] = []
    mode_summaries: list[dict[str, object]] = []
    for mode in modes:
        steps = run_natural_continuation(NATURAL_LOADS_MPA, mode, natural_cfg, x_eval)
        rows = [compare_row(step, a_map, b_map, x_eval) for step in steps]
        mode_summary = summarize_mode(rows)
        mode_summary["verdict"] = verdict_from_summary(mode_summary)
        mode_summaries.append(mode_summary)
        all_rows.extend(rows)

    any_jump = any(item["first_B_like_after_A_mpa"] is not None or item["first_jump_suspicion_mpa"] is not None for item in mode_summaries)
    if any_jump:
        overall_verdict = "Natural near-zero-start continuation selects Branch A at low loads, and at least one natural mode shows a later A-to-B identity loss / jump."
    elif len({item["first_failure_mpa"] for item in mode_summaries}) == 1 and len({item["last_success_mpa"] for item in mode_summaries}) == 1:
        overall_verdict = (
            f"Natural near-zero-start continuation selects Branch A at low loads in both natural modes, remains far from Branch B through "
            f"{float(mode_summaries[0]['last_success_mpa']):.4f} MPa, and then fails at {float(mode_summaries[0]['first_failure_mpa']):.4f} MPa without evidence of a jump to Branch B."
        )
    else:
        overall_verdict = "Natural branch selection depends on the chosen natural continuation mode / seed order in the checked window."

    stem = f"natural_branch_selection_q{float_tag(NATURAL_LOADS_MPA[0])}_to_{float_tag(NATURAL_LOADS_MPA[-1])}"
    csv_path = OUTPUT_DIR / f"{stem}.csv"
    distance_plot_path = OUTPUT_DIR / f"{stem}_distances.png"
    marker_plot_path = OUTPUT_DIR / f"{stem}_markers.png"
    summary_path = OUTPUT_DIR / f"{stem}_summary.json"

    save_csv(csv_path, all_rows)
    plot_distances(all_rows, distance_plot_path)
    plot_markers(all_rows, marker_plot_path)

    summary = {
        "loads_mpa": list(NATURAL_LOADS_MPA),
        "natural_modes": [mode.label for mode in modes],
        "allowed_natural_seeds": ["zero_guess", "previous_solution", "secant_predictor (optional natural mode only)"],
        "forbidden_primary_seeds": ["Branch-A anchor", "Branch-B anchor", "retained tracked Branch-B history as primary seed", "branch-aware A-only/B-only continuation"],
        "natural_config": {
            "x0": float(natural_cfg.x0),
            "nd_bvp": int(natural_cfg.nd_bvp),
            "tol": float(natural_cfg.tol),
            "relaxed_tol": float(natural_cfg.relaxed_tol),
            "max_nodes": int(natural_cfg.max_nodes),
            "right_edge_cluster_start": float(natural_cfg.right_edge_cluster_start),
            "right_edge_cluster_fraction": float(natural_cfg.right_edge_cluster_fraction),
            "right_edge_cluster_power": float(natural_cfg.right_edge_cluster_power),
        },
        "a_reference_max_mpa": float(max(a_map)),
        "branch_b_reference_seed_mpa": float(b_history.q_mpa),
        "branch_b_reference_seed_kind": str(b_history.seed_kind),
        "mode_summaries": mode_summaries,
        "overall_verdict": overall_verdict,
        "csv_path": str(csv_path),
        "distance_plot_path": str(distance_plot_path),
        "marker_plot_path": str(marker_plot_path),
    }
    save_json(summary_path, summary)
    print_summary(summary)


if __name__ == "__main__":
    main()
