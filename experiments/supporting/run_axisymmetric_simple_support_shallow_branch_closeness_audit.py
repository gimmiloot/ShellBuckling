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

OUTPUT_DIR = REPO_ROOT / "output" / "axisymmetric_simple_support_shallow_branch_closeness_audit"
PREV_AUDIT_PATH = REPO_ROOT / "experiments" / "supporting" / "run_axisymmetric_simple_support_branch_b_continuation_audit.py"
PILOT16_PATH = REPO_ROOT / "proof_pilots" / "pilot_16_shallow_simple_support_comparator" / "shallow_simple_support_solver.py"

LOADS_MPA = (0.5, 1.0, 2.0, 3.0, 4.0)
A_SCHEDULE_STEP = 0.25
B_DESCENT_STEP = 0.25
B_BOOTSTRAP_STEP = 0.005
REPAIR_MIN_STEP = 0.025
ND_EVAL = 2000
CSV_FIELDS = [
    "q_mpa", "branch", "background_success", "solve_mode", "seed_kind", "branch_jump_suspicion",
    "distance_to_other_branch_rel_l2", "u_z_abs_l2", "u_z_rel_l2", "theta0_abs_l2", "theta0_rel_l2",
    "T_theta_abs_l2", "T_theta_rel_l2", "T_s_abs_l2", "T_s_rel_l2", "mean_rel_l2_core",
    "max_rel_l2_core", "u_z_center_branch", "u_z_center_shallow", "u_z_center_diff", "u_z_min_branch",
    "u_z_min_shallow", "u_z_min_diff", "slope_edge_branch", "slope_edge_shallow", "slope_edge_diff",
    "T_theta_min_branch", "T_theta_min_shallow", "T_theta_min_diff", "T_s_center_branch", "T_s_center_shallow",
    "T_s_center_diff", "marker_rel_max_core",
]
PLOT_SPECS = [
    ("mean_rel_l2_core", "Mean relative L2 to shallow", "mean_rel_l2_core_vs_load.png", "Mean relative L2 vs shallow"),
    ("u_z_rel_l2", "u_z relative L2 to shallow", "u_z_rel_l2_vs_load.png", "u_z closeness to shallow"),
    ("theta0_rel_l2", "theta0 relative L2 to shallow", "theta0_rel_l2_vs_load.png", "Slope-channel closeness to shallow"),
    ("T_theta_rel_l2", "T_theta relative L2 to shallow", "T_theta_rel_l2_vs_load.png", "T_theta closeness to shallow"),
]
MAPPING_FORMULAS = {
    "Phi0": "Phi0(x) = gamma * x * T_s",
    "Phi0p": "Phi0'(x) = gamma * T_theta",
    "theta0": "theta0(x) = -beta * sin(varphi)",
    "theta0p": "theta0'(x) = -beta * cos(varphi) * kappa_s",
    "T_theta": "T_theta = nu * T_s + u_r / x",
}


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


prev = load_module("branch_shallow_closeness_prev_audit", PREV_AUDIT_PATH)
pilot16 = load_module("branch_shallow_closeness_pilot16", PILOT16_PATH)
from shell_buckling.supporting import dimensionless_background_comparison as dimcomp


def float_tag(value: float) -> str:
    return f"{float(value):.4f}".replace("-", "m").replace(".", "p")


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


def l2_norm(values: np.ndarray, x_grid: np.ndarray) -> float:
    arr = np.asarray(values, dtype=float)
    return float(np.sqrt(np.trapezoid(arr**2, x_grid)))


def profile_metrics(candidate: np.ndarray, reference: np.ndarray, x_grid: np.ndarray) -> dict[str, float]:
    candidate = np.asarray(candidate, dtype=float)
    reference = np.asarray(reference, dtype=float)
    diff = candidate - reference
    abs_l2 = l2_norm(diff, x_grid)
    cand_norm = l2_norm(candidate, x_grid)
    ref_norm = l2_norm(reference, x_grid)
    rel_l2 = abs_l2 / max(cand_norm, ref_norm, 1.0e-12)
    return {
        "abs_l2": float(abs_l2),
        "rel_l2": float(rel_l2),
    }


def relative_marker_gap(a: float, b: float) -> float:
    return abs(float(a) - float(b)) / max(abs(float(a)), abs(float(b)), 1.0e-12)


def core_marker_rel_max(branch_profiles: dict[str, np.ndarray], shallow_profiles: dict[str, np.ndarray]) -> float:
    marker_pairs = [
        (float(branch_profiles["u_z"][0]), float(shallow_profiles["u_z"][0])),
        (float(np.min(branch_profiles["u_z"])), float(np.min(shallow_profiles["u_z"]))),
        (float(branch_profiles["slope_equiv"][-1]), float(shallow_profiles["slope_equiv"][-1])),
        (float(np.min(branch_profiles["T_theta"])), float(np.min(shallow_profiles["T_theta"]))),
        (float(branch_profiles["T_s"][0]), float(shallow_profiles["T_s"][0])),
    ]
    return float(max(relative_marker_gap(a, b) for a, b in marker_pairs))


def common_x_grid(local_group: list[Any], high_group: list[Any], shallow_config: Any, nd_eval: int) -> np.ndarray:
    x0_nonshallow = max(float(profile.config.x0) for profile in local_group + high_group)
    x0 = max(x0_nonshallow, float(shallow_config.x0))
    return np.linspace(x0, 1.0, int(nd_eval))


def make_prev_args(start_load: float, *, a_bootstrap_start: float, repair_min_step: float) -> Any:
    return prev.argparse.Namespace(
        start_load=float(start_load),
        window1_end=4.5000,
        window2_end=4.5000,
        end_load=4.5000,
        window1_step=A_SCHEDULE_STEP,
        window2_step=0.25,
        window3_step=0.25,
        a_bootstrap_start=float(a_bootstrap_start),
        a_bootstrap_step=A_SCHEDULE_STEP,
        b_history_seed=4.3500,
        b_bootstrap_step=B_BOOTSTRAP_STEP,
        repair_min_step=float(repair_min_step),
        nd_eval=ND_EVAL,
    )


def solve_branch_a(loads_mpa: tuple[float, ...], local_group: list[Any], high_group: list[Any], x_grid: np.ndarray) -> tuple[dict[float, Any], list[Any]]:
    args = make_prev_args(float(min(loads_mpa)), a_bootstrap_start=float(min(loads_mpa)), repair_min_step=REPAIR_MIN_STEP)
    start = prev.build_branch_a_start(args, local_group, x_grid)
    schedule = prev.inclusive_grid(float(min(loads_mpa)), float(max(loads_mpa)), A_SCHEDULE_STEP)
    steps = prev.continue_branch("A", start, schedule, args, local_group, high_group, x_grid, stop_on_jump=True)
    step_map = {prev.round_load(step.q_mpa): step for step in steps if step.background_success and not step.branch_jump_suspicion}
    missing = [float(q) for q in loads_mpa if prev.round_load(q) not in step_map]
    if missing:
        raise RuntimeError(f"Could not recover all Branch A loads without jump suspicion: {missing}")
    return step_map, steps


def solve_branch_b(loads_mpa: tuple[float, ...], local_group: list[Any], high_group: list[Any], x_grid: np.ndarray) -> tuple[dict[float, Any], list[Any], Any]:
    top_load = float(max(loads_mpa))
    args = make_prev_args(top_load, a_bootstrap_start=float(min(loads_mpa)), repair_min_step=REPAIR_MIN_STEP)
    start, history_seed = prev.build_branch_b_start(args, local_group, high_group, x_grid)
    schedule = [start.q_mpa] + prev.descending_grid(start.q_mpa, float(min(loads_mpa)), B_DESCENT_STEP)
    steps = prev.continue_branch("B", start, schedule, args, local_group, high_group, x_grid, stop_on_jump=False)
    step_map = {prev.round_load(step.q_mpa): step for step in steps if step.background_success}
    missing = [float(q) for q in loads_mpa if prev.round_load(q) not in step_map]
    if missing:
        raise RuntimeError(f"Could not recover all Branch B loads: {missing}")
    return step_map, steps, history_seed


def solve_shallow(loads_mpa: tuple[float, ...]) -> tuple[dict[float, Any], list[Any], Any]:
    config = pilot16.ShallowSimpleSupportConfig(
        nd_bvp=1500,
        tol=1.0e-5,
        relaxed_tol=5.0e-5,
        max_nodes=80000,
        substep_max_delta_mpa=0.25,
    )
    results = pilot16.solve_shallow_simple_support_continuation(loads_mpa, config=config)
    by_q = {float(item.q_mpa): item.solution for item in results if item.success and item.solution is not None}
    missing = [float(q) for q in loads_mpa if float(q) not in by_q]
    if missing:
        raise RuntimeError(f"Could not recover all shallow loads: {missing}")
    return by_q, results, config


def mapped_nonshallow_profiles(step: Any, x_grid: np.ndarray) -> dict[str, np.ndarray]:
    state = np.asarray(step.solution.sol(x_grid), dtype=float)
    Ts = np.asarray(state[0], dtype=float)
    Tsn = np.asarray(state[1], dtype=float)
    Ms = np.asarray(state[2], dtype=float)
    ur = np.asarray(state[3], dtype=float)
    uz = np.asarray(state[4], dtype=float)
    varphi = np.asarray(state[5], dtype=float)
    diag = dimcomp.compute_branchA_diagnostics(x_grid, Ts, Tsn, Ms, ur, varphi)
    return {
        "u_z": uz,
        "theta0": np.asarray(diag["theta0"], dtype=float),
        "theta0p": np.asarray(diag["theta0p"], dtype=float),
        "Phi0": np.asarray(diag["Phi0"], dtype=float),
        "Phi0p": np.asarray(diag["Phi0p"], dtype=float),
        "T_theta": np.asarray(diag["Ttheta"], dtype=float),
        "T_s": Ts,
        "slope_equiv": -np.asarray(diag["theta0"], dtype=float) / float(dimcomp.beta),
        "varphi": varphi,
    }


def shallow_profiles(sol: Any, x_grid: np.ndarray) -> dict[str, np.ndarray]:
    y = np.asarray(sol.sol(x_grid), dtype=float)
    x_safe = np.maximum(np.asarray(x_grid, dtype=float), 1.0e-12)
    theta0p = np.asarray(y[0], dtype=float)
    theta0 = np.asarray(y[1], dtype=float)
    Phi0p = np.asarray(y[2], dtype=float)
    Phi0 = np.asarray(y[3], dtype=float)
    return {
        "u_z": np.asarray(pilot16.recover_u_z_shallow(x_grid, y), dtype=float),
        "theta0": theta0,
        "theta0p": theta0p,
        "Phi0": Phi0,
        "Phi0p": Phi0p,
        "T_theta": Phi0p / float(dimcomp.gamma),
        "T_s": Phi0 / (float(dimcomp.gamma) * x_safe),
        "slope_equiv": -theta0 / float(dimcomp.beta),
    }


def mean_metric(values: list[float]) -> float:
    arr = np.asarray(values, dtype=float)
    return float(np.mean(arr))


def max_metric(values: list[float]) -> float:
    arr = np.asarray(values, dtype=float)
    return float(np.max(arr))


def build_rows(
    loads_mpa: tuple[float, ...],
    branch_a: dict[float, Any],
    branch_b: dict[float, Any],
    shallow_map: dict[float, Any],
    x_grid: np.ndarray,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for q_mpa in loads_mpa:
        qa = prev.round_load(q_mpa)
        steps_by_branch = {
            "A": branch_a[qa],
            "B": branch_b[qa],
        }
        shallow = shallow_profiles(shallow_map[float(q_mpa)], x_grid)
        other_state_map = {
            "A": branch_b[qa].state_eval,
            "B": branch_a[qa].state_eval,
        }
        for branch_label, step in steps_by_branch.items():
            branch_profiles = mapped_nonshallow_profiles(step, x_grid)
            u_z_metrics = profile_metrics(branch_profiles["u_z"], shallow["u_z"], x_grid)
            theta0_metrics = profile_metrics(branch_profiles["theta0"], shallow["theta0"], x_grid)
            T_theta_metrics = profile_metrics(branch_profiles["T_theta"], shallow["T_theta"], x_grid)
            T_s_metrics = profile_metrics(branch_profiles["T_s"], shallow["T_s"], x_grid)
            rel_values = [
                u_z_metrics["rel_l2"],
                theta0_metrics["rel_l2"],
                T_theta_metrics["rel_l2"],
                T_s_metrics["rel_l2"],
            ]
            other_state = other_state_map[branch_label]
            other_rel_l2 = prev.state_distance(step.state_eval, other_state, x_grid) / max(prev.state_norm(other_state, x_grid), 1.0)
            rows.append(
                {
                    "q_mpa": float(q_mpa),
                    "branch": branch_label,
                    "background_success": bool(step.background_success),
                    "solve_mode": str(step.solve_mode),
                    "seed_kind": str(step.seed_kind),
                    "branch_jump_suspicion": bool(step.branch_jump_suspicion),
                    "distance_to_other_branch_rel_l2": float(other_rel_l2),
                    "u_z_abs_l2": u_z_metrics["abs_l2"],
                    "u_z_rel_l2": u_z_metrics["rel_l2"],
                    "theta0_abs_l2": theta0_metrics["abs_l2"],
                    "theta0_rel_l2": theta0_metrics["rel_l2"],
                    "T_theta_abs_l2": T_theta_metrics["abs_l2"],
                    "T_theta_rel_l2": T_theta_metrics["rel_l2"],
                    "T_s_abs_l2": T_s_metrics["abs_l2"],
                    "T_s_rel_l2": T_s_metrics["rel_l2"],
                    "mean_rel_l2_core": mean_metric(rel_values),
                    "max_rel_l2_core": max_metric(rel_values),
                    "u_z_center_branch": float(branch_profiles["u_z"][0]),
                    "u_z_center_shallow": float(shallow["u_z"][0]),
                    "u_z_center_diff": float(branch_profiles["u_z"][0] - shallow["u_z"][0]),
                    "u_z_min_branch": float(np.min(branch_profiles["u_z"])),
                    "u_z_min_shallow": float(np.min(shallow["u_z"])),
                    "u_z_min_diff": float(np.min(branch_profiles["u_z"]) - np.min(shallow["u_z"])),
                    "slope_edge_branch": float(branch_profiles["slope_equiv"][-1]),
                    "slope_edge_shallow": float(shallow["slope_equiv"][-1]),
                    "slope_edge_diff": float(branch_profiles["slope_equiv"][-1] - shallow["slope_equiv"][-1]),
                    "T_theta_min_branch": float(np.min(branch_profiles["T_theta"])),
                    "T_theta_min_shallow": float(np.min(shallow["T_theta"])),
                    "T_theta_min_diff": float(np.min(branch_profiles["T_theta"]) - np.min(shallow["T_theta"])),
                    "T_s_center_branch": float(branch_profiles["T_s"][0]),
                    "T_s_center_shallow": float(shallow["T_s"][0]),
                    "T_s_center_diff": float(branch_profiles["T_s"][0] - shallow["T_s"][0]),
                    "marker_rel_max_core": core_marker_rel_max(branch_profiles, shallow),
                }
            )
    return rows


def rows_by_branch(rows: list[dict[str, object]], branch: str) -> list[dict[str, object]]:
    return [row for row in rows if str(row["branch"]) == branch]


def make_metric_plot(rows: list[dict[str, object]], metric: str, ylabel: str, title: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8.5, 5.0))
    for branch, color in (("A", "tab:blue"), ("B", "tab:red")):
        branch_rows = rows_by_branch(rows, branch)
        ax.plot(
            [float(row["q_mpa"]) for row in branch_rows],
            [float(row[metric]) for row in branch_rows],
            marker="o",
            linewidth=2.0,
            color=color,
            label=f"Branch {branch}",
        )
    ax.set_xlabel("p, MPa")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def leader(a_value: float, b_value: float, tol: float = 1.0e-12) -> str:
    if a_value + tol < b_value:
        return "A"
    if b_value + tol < a_value:
        return "B"
    return "tie"


def build_summary(rows: list[dict[str, object]], history_seed: Any) -> dict[str, object]:
    loads_summary: list[dict[str, object]] = []
    a_rows = {float(row["q_mpa"]): row for row in rows_by_branch(rows, "A")}
    b_rows = {float(row["q_mpa"]): row for row in rows_by_branch(rows, "B")}
    aggregate_leaders: list[str] = []
    quantity_counts = {key: {"A": 0, "B": 0, "tie": 0} for key in ("mean_rel_l2_core", "u_z_rel_l2", "theta0_rel_l2", "T_theta_rel_l2", "T_s_rel_l2")}
    for q_mpa in LOADS_MPA:
        a_row = a_rows[float(q_mpa)]
        b_row = b_rows[float(q_mpa)]
        per_load = {"q_mpa": float(q_mpa), "leaders": {}}
        for key in quantity_counts:
            lead = leader(float(a_row[key]), float(b_row[key]))
            per_load["leaders"][key] = lead
            quantity_counts[key][lead] += 1
            if key == "mean_rel_l2_core":
                aggregate_leaders.append(lead)
        loads_summary.append(per_load)

    a_wins = aggregate_leaders.count("A")
    b_wins = aggregate_leaders.count("B")
    if a_wins == len(LOADS_MPA):
        verdict = f"Branch A is closer to shallow at low loads {LOADS_MPA[0]:.1f}..{LOADS_MPA[-1]:.1f} MPa."
    elif b_wins == len(LOADS_MPA):
        verdict = f"Branch B is closer to shallow at low loads {LOADS_MPA[0]:.1f}..{LOADS_MPA[-1]:.1f} MPa."
    else:
        verdict = "Closeness to shallow depends on load interval / quantity."

    return {
        "loads_mpa": list(LOADS_MPA),
        "mapping_source": str(REPO_ROOT / "src" / "shell_buckling" / "supporting" / "dimensionless_background_comparison.py"),
        "mapping_formulas": MAPPING_FORMULAS,
        "shallow_deflection_source": str(PILOT16_PATH),
        "note_on_slope_quantity": "Raw shallow varphi is not present in the existing mapping; closeness is measured with the mapped slope channel theta0 and its exact normalized proxy -theta0/beta.",
        "branch_a_source": "honest low-load simple-support continuation",
        "branch_b_source": "retained tracked high-load branch projected to local simple-support and continued downward",
        "branch_b_history_seed_mpa": float(history_seed.q_mpa),
        "branch_b_history_seed_kind": str(history_seed.seed_kind),
        "aggregate_leader_by_load": [{"q_mpa": item["q_mpa"], "leader": item["leaders"]["mean_rel_l2_core"]} for item in loads_summary],
        "per_load_leaders": loads_summary,
        "leader_counts": quantity_counts,
        "overall_verdict": verdict,
    }


def print_summary(summary: dict[str, object], csv_path: Path, plot_paths: list[Path]) -> None:
    print("=== Branch-vs-shallow low-load closeness audit ===")
    print("mapping source: src/shell_buckling/supporting/dimensionless_background_comparison.py")
    print("non-shallow source: src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py")
    print("tracked-branch source for Branch B: src/shell_buckling/mixed_weak/simple_support_high_load_background_continuation.py")
    print("shallow deflection helper: proof_pilots/pilot_16_shallow_simple_support_comparator/shallow_simple_support_solver.py")
    print(f"loads: {', '.join(f'{value:.1f}' for value in LOADS_MPA)} MPa")
    print(f"Branch B history seed: {summary['branch_b_history_seed_mpa']:.4f} MPa ({summary['branch_b_history_seed_kind']})")
    for item in summary["aggregate_leader_by_load"]:
        print(f"aggregate leader at {item['q_mpa']:.1f} MPa: Branch {item['leader']}")
    print(f"overall verdict: {summary['overall_verdict']}")
    print(f"csv: {csv_path}")
    print("plots:")
    for path in plot_paths:
        print(f"  {path}")


def main() -> None:
    local_group = prev.local_profiles()
    high_group = prev.high_profiles()
    _, _, shallow_config = solve_shallow((LOADS_MPA[0],))
    x_grid = common_x_grid(local_group, high_group, shallow_config, ND_EVAL)

    branch_a_map, branch_a_steps = solve_branch_a(LOADS_MPA, local_group, high_group, x_grid)
    branch_b_map, branch_b_steps, history_seed = solve_branch_b(LOADS_MPA, local_group, high_group, x_grid)
    shallow_map, _, _ = solve_shallow(LOADS_MPA)

    rows = build_rows(LOADS_MPA, branch_a_map, branch_b_map, shallow_map, x_grid)
    summary = build_summary(rows, history_seed)

    stem = f"branch_vs_shallow_low_load_q{float_tag(LOADS_MPA[0])}_to_{float_tag(LOADS_MPA[-1])}"
    csv_path = OUTPUT_DIR / f"{stem}.csv"
    json_path = OUTPUT_DIR / f"{stem}_summary.json"
    save_csv(csv_path, rows)
    save_json(json_path, summary)

    plot_paths: list[Path] = []
    for metric, ylabel, filename, title in PLOT_SPECS:
        plot_path = OUTPUT_DIR / f"{stem}_{filename}"
        make_metric_plot(rows, metric, ylabel, title, plot_path)
        plot_paths.append(plot_path)

    print_summary(summary, csv_path, plot_paths)


if __name__ == "__main__":
    main()
