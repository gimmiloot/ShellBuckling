from __future__ import annotations

import argparse
import csv
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

from shell_buckling.mixed_weak import axisymmetric_simple_support_background as simple_bg
from shell_buckling.mixed_weak import simple_support_high_load_background_continuation as high_load_bg


warnings.filterwarnings("ignore", category=RuntimeWarning, module=r"scipy\.integrate\._bvp")

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "output" / "axisymmetric_background_bc_profile_comparison"
DEFAULT_LOADS_MPA = [4.0, 5.0]
DEFAULT_X0 = 1.0e-4
DEFAULT_ND_PLOT = 1500
DEFAULT_BRANCH_STEP_MPA = 0.01
COMMON_PROFILE_ORDER = ["T_s", "T_sn", "M_s", "T_theta", "M_theta", "varphi", "u_r", "u_z"]
PROFILE_LABELS = {
    "T_s": "Meridional Force $T_s(x)$",
    "T_sn": "Meridional Shear $T_{sn}(x)$",
    "M_s": "Meridional Moment $M_s(x)$",
    "T_theta": "Circumferential Force $T_{\\theta}(x)$",
    "M_theta": "Circumferential Moment $M_{\\theta}(x)$",
    "varphi": "Rotation Angle $\\varphi(x)$",
    "u_r": "Radial Displacement $u_r(x)$",
    "u_z": "Axial Displacement $u_z(x)$",
}
SUMMARY_FIELDNAMES = [
    "p_mpa",
    "success",
    "solve_mode",
    "seed_kind",
    "nodes",
    "max_rms",
    "branch_history",
    "message",
]


@dataclass(frozen=True)
class BackgroundProfileSolve:
    q_mpa: float
    success: bool
    solve_mode: str
    seed_kind: str
    nodes: int
    max_rms: float
    branch_history: str
    message: str
    solution: Any | None = None


@dataclass(frozen=True)
class BranchHistoryBundle:
    results: list[BackgroundProfileSolve]
    config: simple_bg.AxisymmetricSimpleSupportConfig
    branch_history: str
    anchor_load_mpa: float
    anchor_seed_kind: str
    actual_x0: float
    used_independent_fixed_load_as_main_source: bool


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Plot axisymmetric non-shallow simple-support background profiles for "
            "the selected load set, using one tracked branch history."
        )
    )
    parser.add_argument("--loads-mpa", nargs="+", type=float, default=DEFAULT_LOADS_MPA)
    parser.add_argument("--x0", type=float, default=DEFAULT_X0)
    parser.add_argument("--nd-plot", type=int, default=DEFAULT_ND_PLOT)
    parser.add_argument("--branch-step-mpa", type=float, default=DEFAULT_BRANCH_STEP_MPA)
    args = parser.parse_args(argv)
    if not args.loads_mpa:
        raise ValueError("--loads-mpa must contain at least one load value.")
    if args.x0 <= 0.0 or args.x0 >= 1.0:
        raise ValueError("--x0 must lie in (0, 1).")
    if args.nd_plot < 10:
        raise ValueError("--nd-plot must be at least 10.")
    if args.branch_step_mpa <= 0.0:
        raise ValueError("--branch-step-mpa must be positive.")
    return args


def save_figure(fig, filename: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


def save_summary_csv(rows: list[dict[str, object]], filename: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SUMMARY_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in SUMMARY_FIELDNAMES})
    return path


def summary_row(result: BackgroundProfileSolve) -> dict[str, object]:
    return {
        "p_mpa": float(result.q_mpa),
        "success": bool(result.success),
        "solve_mode": result.solve_mode,
        "seed_kind": result.seed_kind,
        "nodes": int(result.nodes),
        "max_rms": float(result.max_rms) if np.isfinite(result.max_rms) else float("nan"),
        "branch_history": result.branch_history,
        "message": result.message,
    }


def round_load(value: float) -> float:
    return round(float(value), 7)


def ordered_unique_loads(loads_mpa: list[float]) -> list[float]:
    ordered: list[float] = []
    for load_mpa in loads_mpa:
        q_value = round_load(load_mpa)
        if q_value not in ordered:
            ordered.append(q_value)
    return ordered


def branch_result_from_axisymmetric_result(
    result: simple_bg.AxisymmetricBackgroundSolve,
    *,
    solve_mode: str,
    branch_history: str,
) -> BackgroundProfileSolve:
    return BackgroundProfileSolve(
        q_mpa=float(result.q_mpa),
        success=bool(result.success),
        solve_mode=str(solve_mode),
        seed_kind=str(result.seed_kind),
        nodes=int(result.nodes),
        max_rms=float(result.max_rms),
        branch_history=str(branch_history),
        message=str(result.message),
        solution=result.solution,
    )


def load_suffix(loads_mpa: list[float]) -> str:
    labels = []
    for load_mpa in loads_mpa:
        if abs(load_mpa - round(load_mpa)) < 1.0e-12:
            labels.append(str(int(round(load_mpa))))
        else:
            labels.append(str(load_mpa).replace(".", "p"))
    return "_".join(labels) + "MPa"


def quantity_filename(key: str, loads_mpa: list[float]) -> str:
    return f"axisymmetric_profile_{key}_simple_support_{load_suffix(loads_mpa)}.png"


def build_high_load_branch_anchor(
    anchor_load_mpa: float,
    *,
    config: simple_bg.AxisymmetricSimpleSupportConfig,
    history_run_dir: Path,
) -> tuple[simple_bg.AxisymmetricBackgroundSolve, str]:
    progress = high_load_bg.load_fast_progress(history_run_dir)
    if progress is None:
        raise RuntimeError(f"Could not load pilot-21 fast progress from {history_run_dir}.")

    if float(anchor_load_mpa) > float(high_load_bg.DEFAULT_DIRECT_SOLVE_MAX_MPA) + 1.0e-12:
        anchor_result = high_load_bg.solve_axisymmetric_simple_support_high_load_schedule(
            [float(anchor_load_mpa)],
            config=config,
            history_run_dir=history_run_dir,
            prefer_established_history=True,
            verbose=False,
        )[0]
        branch_history = (
            "pilot21 fast continuation history "
            f"({history_run_dir}) anchor q={float(anchor_result.q_mpa):.3f} MPa"
        )
        return anchor_result, branch_history

    scaled_anchor = high_load_bg.load_named_anchor(progress, history_run_dir)
    anchor_result = high_load_bg.axisymmetric_result_from_point(
        scaled_anchor,
        seed_kind=f"retained::{scaled_anchor.accepted_seed}",
    )
    branch_history = (
        "pilot21 scaled-anchor checkpoint "
        f"({history_run_dir}) anchor q={float(anchor_result.q_mpa):.4f} MPa"
    )
    return anchor_result, branch_history


def descending_load_grid(start_q_mpa: float, target_q_mpa: float, step_mpa: float) -> list[float]:
    start_q = float(start_q_mpa)
    target_q = float(target_q_mpa)
    if target_q > start_q + 1.0e-12:
        raise ValueError("Descending grid requires target_q <= start_q.")
    if abs(target_q - start_q) <= 1.0e-12:
        return [round_load(start_q)]

    values = [round_load(start_q)]
    q_value = start_q
    while q_value - float(step_mpa) > target_q + 1.0e-12:
        q_value = round_load(q_value - float(step_mpa))
        values.append(float(q_value))
    if abs(values[-1] - target_q) > 1.0e-12:
        values.append(round_load(target_q))
    return values


def solve_descending_branch_target(
    start_result: simple_bg.AxisymmetricBackgroundSolve,
    target_q_mpa: float,
    *,
    config: simple_bg.AxisymmetricSimpleSupportConfig,
    initial_step_mpa: float,
    min_step_mpa: float,
) -> simple_bg.AxisymmetricBackgroundSolve:
    if start_result.solution is None:
        raise ValueError("Descending continuation requires a converged start_result.")

    x_mesh = simple_bg.default_x_mesh(config)
    current_result = start_result
    current_q = float(start_result.q_mpa)
    target_q = float(target_q_mpa)
    step_mpa = float(initial_step_mpa)

    while current_q > target_q + 1.0e-12:
        raw_step = min(step_mpa, current_q - target_q)
        q_trial = round_load(current_q - raw_step)
        previous_guess = current_result.solution.sol(x_mesh)
        trial_result = simple_bg.solve_axisymmetric_simple_support_fixed_load(
            q_trial,
            config=config,
            initial_guess=previous_guess,
        )
        if trial_result.success:
            current_result = trial_result
            current_q = float(trial_result.q_mpa)
            continue

        if raw_step <= float(min_step_mpa) + 1.0e-12:
            return trial_result

        step_mpa = max(float(min_step_mpa), 0.5 * raw_step)

    return current_result


def solve_simple_support_tracked_branch(loads_mpa: list[float], *, requested_x0: float, branch_step_mpa: float) -> BranchHistoryBundle:
    ordered_loads = ordered_unique_loads(loads_mpa)
    anchor_load_mpa = max(float(value) for value in ordered_loads)
    history_run_dir = high_load_bg.DEFAULT_HISTORY_RUN_DIR
    config = high_load_bg.default_high_load_background_config(history_run_dir)
    step_control = high_load_bg.default_step_control(history_run_dir)
    min_step_mpa = float(step_control.get("min_step_mpa", 0.0025))

    anchor_result, branch_history = build_high_load_branch_anchor(
        anchor_load_mpa,
        config=config,
        history_run_dir=history_run_dir,
    )
    if not anchor_result.success or anchor_result.solution is None:
        raise RuntimeError(
            f"Could not get a tracked high-load branch anchor at q={anchor_load_mpa:.3f} MPa: {anchor_result.message}"
        )

    results_by_q: dict[float, BackgroundProfileSolve] = {}
    results_by_q[round_load(anchor_result.q_mpa)] = branch_result_from_axisymmetric_result(
        anchor_result,
        solve_mode="tracked_branch_anchor",
        branch_history=branch_history,
    )

    current_result = anchor_result
    for target_q_mpa in sorted((float(value) for value in ordered_loads if float(value) < anchor_load_mpa - 1.0e-12), reverse=True):
        descended_result = solve_descending_branch_target(
            current_result,
            target_q_mpa,
            config=config,
            initial_step_mpa=float(branch_step_mpa),
            min_step_mpa=min_step_mpa,
        )
        branch_result = branch_result_from_axisymmetric_result(
            descended_result,
            solve_mode="tracked_branch_descend",
            branch_history=branch_history,
        )
        results_by_q[round_load(target_q_mpa)] = branch_result
        if not descended_result.success or descended_result.solution is None:
            current_result = descended_result
            break
        current_result = descended_result

    results = [results_by_q[round_load(load_mpa)] for load_mpa in ordered_loads]
    actual_x0 = max(float(requested_x0), float(config.x0))
    return BranchHistoryBundle(
        results=results,
        config=config,
        branch_history=branch_history,
        anchor_load_mpa=float(anchor_result.q_mpa),
        anchor_seed_kind=str(anchor_result.seed_kind),
        actual_x0=float(actual_x0),
        used_independent_fixed_load_as_main_source=False,
    )


def extract_common_profiles_from_state(y: np.ndarray, x: np.ndarray, *, nu: float, mu: float) -> dict[str, np.ndarray]:
    x = np.asarray(x, dtype=float)
    x_safe = np.maximum(x, 1.0e-12)
    Ts = np.asarray(y[0], dtype=float)
    Tsn = np.asarray(y[1], dtype=float)
    Ms = np.asarray(y[2], dtype=float)
    ur = np.asarray(y[3], dtype=float)
    uz = np.asarray(y[4], dtype=float)
    phi = np.asarray(y[5], dtype=float)

    r = x_safe + ur
    etheta = ur / x_safe
    Ttheta = nu * Ts + etheta
    Mtheta = nu * Ms + np.sin(phi) / (12.0 * mu**2 * np.maximum(r, 1.0e-12))

    return {
        "T_s": Ts,
        "T_sn": Tsn,
        "M_s": Ms,
        "T_theta": Ttheta,
        "M_theta": Mtheta,
        "varphi": phi,
        "u_r": ur,
        "u_z": uz,
    }


def evaluate_profile_set(result: BackgroundProfileSolve, x_plot: np.ndarray, *, nu: float, mu: float) -> dict[str, np.ndarray] | None:
    if not result.success or result.solution is None:
        return None
    y = np.asarray(result.solution.sol(x_plot), dtype=float)
    if not np.all(np.isfinite(y)):
        return None
    return extract_common_profiles_from_state(y, x_plot, nu=nu, mu=mu)


def make_quantity_plot(
    key: str,
    label: str,
    loads_mpa: list[float],
    x_plot: np.ndarray,
    simple_profiles: dict[float, dict[str, np.ndarray]],
) -> Path:
    colors = plt.cm.plasma(np.linspace(0.20, 0.80, len(loads_mpa)))

    fig, ax = plt.subplots(figsize=(10.0, 6.0))
    for color, load_mpa in zip(colors, loads_mpa):
        if load_mpa in simple_profiles:
            ax.plot(
                x_plot,
                simple_profiles[load_mpa][key],
                color=color,
                linestyle="-",
                linewidth=2.0,
                label=f"p={load_mpa:g} MPa",
            )

    load_handles = [
        Line2D([0], [0], color=color, linestyle="-", linewidth=2.0, label=f"p={load_mpa:g} MPa")
        for color, load_mpa in zip(colors, loads_mpa)
    ]
    ax.legend(handles=load_handles, title="simple support tracked-branch loads", loc="best")
    ax.set_xlabel("solver radial coordinate x")
    ax.set_ylabel(label)
    ax.set_title(f"{label}: simple support tracked branch")
    ax.grid(True)
    fig.tight_layout()
    return save_figure(fig, quantity_filename(key, loads_mpa))


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    loads_mpa = [float(value) for value in args.loads_mpa]
    branch_bundle = solve_simple_support_tracked_branch(
        loads_mpa,
        requested_x0=float(args.x0),
        branch_step_mpa=float(args.branch_step_mpa),
    )

    x_plot = np.linspace(branch_bundle.actual_x0, 1.0, int(args.nd_plot))
    simple_profiles: dict[float, dict[str, np.ndarray]] = {}
    for result in branch_bundle.results:
        profiles = evaluate_profile_set(result, x_plot, nu=simple_bg.nu, mu=simple_bg.mu)
        if profiles is not None:
            simple_profiles[float(result.q_mpa)] = profiles

    figure_paths = []
    for key in COMMON_PROFILE_ORDER:
        figure_paths.append(
            make_quantity_plot(
                key,
                PROFILE_LABELS[key],
                loads_mpa,
                x_plot,
                simple_profiles,
            )
        )

    summary_csv_path = save_summary_csv(
        [summary_row(result) for result in branch_bundle.results],
        f"axisymmetric_background_profile_simple_support_{load_suffix(loads_mpa)}_summary.csv",
    )

    simple_failures = [result for result in branch_bundle.results if not result.success]

    print("=== Axisymmetric Non-Shallow Background Profiles: Simple Support Only ===")
    print("simple support source: shell_buckling.mixed_weak.axisymmetric_simple_support_background")
    print(
        "tracked branch source: shell_buckling.mixed_weak.simple_support_high_load_background_continuation "
        "via the pilot-21 u_z-scaled / arc-like fast history"
    )
    print(f"loads, MPa: {loads_mpa}")
    print(f"plotted quantities: {COMMON_PROFILE_ORDER}")
    print("BC content on figures: simple support only")
    print(f"tracked branch history: {branch_bundle.branch_history}")
    print(f"anchor load on tracked branch: {branch_bundle.anchor_load_mpa:.3f} MPa")
    print(f"anchor seed kind: {branch_bundle.anchor_seed_kind}")
    print(
        "load extraction policy: highest requested load from tracked high-load history; "
        "lower requested loads by descending previous-solution continuation on the same branch only"
    )
    print(
        "independent fixed-load solve used as main source: "
        f"{'yes' if branch_bundle.used_independent_fixed_load_as_main_source else 'no'}"
    )
    print(f"requested x0: {float(args.x0):.6f}")
    print(f"actual plot x0: {branch_bundle.actual_x0:.6f}")
    print(f"summary csv: {summary_csv_path}")
    print("saved figures:")
    for path in figure_paths:
        print(f"  {path}")

    if simple_failures:
        print("nonconverged loads:")
        for result in simple_failures:
            print(
                f"  simple support  p={result.q_mpa:.3f} MPa  mode={result.solve_mode}  "
                f"seed={result.seed_kind}  message={result.message}"
            )
    else:
        print("nonconverged loads: none")


if __name__ == "__main__":
    main()
