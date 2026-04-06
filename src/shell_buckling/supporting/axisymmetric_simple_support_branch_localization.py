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

from shell_buckling.supporting import determinant_criterion_comparison_simple_support_n345_high_load as repaired_bg


warnings.filterwarnings("ignore", category=RuntimeWarning, module=r"scipy\.integrate\._bvp")

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "output" / "axisymmetric_simple_support_branch_localization"
DEFAULT_P_MIN = 4.0
DEFAULT_P_MAX = 5.0
DEFAULT_NUM_POINTS = 201
DEFAULT_X0 = 1.0e-4
DEFAULT_ND_EVAL = 2000
INDICATOR_ORDER = [
    "u_z_center",
    "varphi_edge",
    "T_s_center",
    "min_T_theta",
    "min_M_s",
    "min_M_theta",
]
INDICATOR_LABELS = {
    "u_z_center": r"$u_z(0)$ center proxy",
    "varphi_edge": r"$\varphi(1)$",
    "T_s_center": r"$T_s(0)$ center proxy",
    "min_T_theta": r"$\min_x T_{\theta}(x)$",
    "min_M_s": r"$\min_x M_s(x)$",
    "min_M_theta": r"$\min_x M_{\theta}(x)$",
}
CSV_FIELDNAMES = [
    "scan_direction",
    "continuation_step",
    "p_mpa",
    "success",
    "solve_mode",
    "nodes",
    "max_rms",
    "message",
    *INDICATOR_ORDER,
]


@dataclass(frozen=True)
class BranchIndicatorRow:
    scan_direction: str
    continuation_step: int
    p_mpa: float
    success: bool
    solve_mode: str
    nodes: int
    max_rms: float
    message: str
    u_z_center: float
    varphi_edge: float
    T_s_center: float
    min_T_theta: float
    min_M_s: float
    min_M_theta: float

    def to_csv_row(self) -> dict[str, object]:
        return {
            "scan_direction": self.scan_direction,
            "continuation_step": self.continuation_step,
            "p_mpa": self.p_mpa,
            "success": self.success,
            "solve_mode": self.solve_mode,
            "nodes": self.nodes,
            "max_rms": self.max_rms,
            "message": self.message,
            "u_z_center": self.u_z_center,
            "varphi_edge": self.varphi_edge,
            "T_s_center": self.T_s_center,
            "min_T_theta": self.min_T_theta,
            "min_M_s": self.min_M_s,
            "min_M_theta": self.min_M_theta,
        }


@dataclass(frozen=True)
class ScanRun:
    direction: str
    rows: list[BranchIndicatorRow]
    config: repaired_bg.base.AxisymmetricSimpleSupportConfig


@dataclass(frozen=True)
class TransitionAnalysis:
    coincide: bool
    highest_mismatch_p: float | None
    next_matching_p: float | None
    mismatch_interval: tuple[float, float] | None
    mismatch_range: tuple[float, float] | None
    max_up_jump_interval: tuple[float, float] | None
    max_up_jump_metric: float
    max_down_jump_interval: tuple[float, float] | None
    max_down_jump_metric: float


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Localize branch switching of the honest axisymmetric simple-support "
            "background by comparing up-scan and down-scan branch indicators."
        )
    )
    parser.add_argument("--p-min", type=float, default=DEFAULT_P_MIN)
    parser.add_argument("--p-max", type=float, default=DEFAULT_P_MAX)
    parser.add_argument("--num-points", type=int, default=DEFAULT_NUM_POINTS)
    parser.add_argument("--x0", type=float, default=DEFAULT_X0)
    parser.add_argument("--nd-eval", type=int, default=DEFAULT_ND_EVAL)
    args = parser.parse_args(argv)
    if args.p_max <= args.p_min:
        raise ValueError("--p-max must be greater than --p-min.")
    if args.num_points < 3:
        raise ValueError("--num-points must be at least 3.")
    if args.x0 <= 0.0 or args.x0 >= 1.0:
        raise ValueError("--x0 must lie in (0, 1).")
    if args.nd_eval < 50:
        raise ValueError("--nd-eval must be at least 50.")
    return args


def float_tag(value: float) -> str:
    return f"{float(value):.3f}".replace("-", "m").replace(".", "p")


def scan_stem(p_min: float, p_max: float, num_points: int) -> str:
    return (
        "axisymmetric_simple_support_branch_"
        f"p{float_tag(p_min)}_to_{float_tag(p_max)}_"
        f"{int(num_points)}pts"
    )


def save_figure(fig, filename: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


def save_csv(rows: list[BranchIndicatorRow], filename: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.to_csv_row().get(key, "") for key in CSV_FIELDNAMES})
    return path


def build_pressure_grid(p_min: float, p_max: float, num_points: int) -> tuple[np.ndarray, np.ndarray]:
    p_up = np.linspace(float(p_min), float(p_max), int(num_points))
    p_down = p_up[::-1].copy()
    return p_up, p_down


def extract_indicator_values(solution, x_eval: np.ndarray) -> dict[str, float]:
    y = np.asarray(solution.sol(x_eval), dtype=float)
    if not np.all(np.isfinite(y)):
        raise ValueError("non-finite solution evaluation on indicator grid")

    Ts = np.asarray(y[0], dtype=float)
    Ms = np.asarray(y[2], dtype=float)
    ur = np.asarray(y[3], dtype=float)
    uz = np.asarray(y[4], dtype=float)
    varphi = np.asarray(y[5], dtype=float)
    x_safe = np.maximum(x_eval, 1.0e-12)
    r = x_safe + ur
    T_theta = repaired_bg.base.nu * Ts + ur / x_safe
    M_theta = repaired_bg.base.nu * Ms + np.sin(varphi) / (12.0 * repaired_bg.base.mu**2 * np.maximum(r, 1.0e-12))

    return {
        "u_z_center": float(uz[0]),
        "varphi_edge": float(varphi[-1]),
        "T_s_center": float(Ts[0]),
        "min_T_theta": float(np.min(T_theta)),
        "min_M_s": float(np.min(Ms)),
        "min_M_theta": float(np.min(M_theta)),
    }


def make_row(
    direction: str,
    continuation_step: int,
    step: repaired_bg.BackgroundStep,
    x_eval: np.ndarray,
) -> BranchIndicatorRow:
    result = step.result
    values = {key: float("nan") for key in INDICATOR_ORDER}
    message = str(result.message)

    if result.success and result.solution is not None:
        try:
            values = extract_indicator_values(result.solution, x_eval)
        except Exception as exc:
            message = f"{message} | indicator_eval_failed: {exc}"

    return BranchIndicatorRow(
        scan_direction=direction,
        continuation_step=int(continuation_step),
        p_mpa=float(result.q_mpa),
        success=bool(result.success),
        solve_mode=str(step.solve_mode),
        nodes=int(result.nodes),
        max_rms=float(result.max_rms),
        message=message,
        u_z_center=float(values["u_z_center"]),
        varphi_edge=float(values["varphi_edge"]),
        T_s_center=float(values["T_s_center"]),
        min_T_theta=float(values["min_T_theta"]),
        min_M_s=float(values["min_M_s"]),
        min_M_theta=float(values["min_M_theta"]),
    )


def run_scan(direction: str, p_values: np.ndarray, x0: float, nd_eval: int) -> ScanRun:
    steps, config = repaired_bg.solve_simple_support_background_schedule_repaired(p_values, x0)
    x_eval = np.linspace(config.x0, 1.0, int(nd_eval))
    rows = [make_row(direction, index, step, x_eval) for index, step in enumerate(steps)]
    return ScanRun(direction=direction, rows=rows, config=config)


def finite_success_map(rows: list[BranchIndicatorRow]) -> dict[float, BranchIndicatorRow]:
    out: dict[float, BranchIndicatorRow] = {}
    for row in rows:
        if not row.success:
            continue
        values = [getattr(row, key) for key in INDICATOR_ORDER]
        if not np.all(np.isfinite(values)):
            continue
        out[round(float(row.p_mpa), 10)] = row
    return out


def indicator_scales(up_map: dict[float, BranchIndicatorRow], down_map: dict[float, BranchIndicatorRow]) -> dict[str, float]:
    scales: dict[str, float] = {}
    for key in INDICATOR_ORDER:
        values: list[float] = []
        for row in list(up_map.values()) + list(down_map.values()):
            value = float(getattr(row, key))
            if np.isfinite(value):
                values.append(abs(value))
        scales[key] = max(values) if values else 1.0
    return scales


def indicator_tolerance(scale: float) -> float:
    return max(1.0e-8, 1.0e-5 * float(scale))


def mismatch_flags(
    up_map: dict[float, BranchIndicatorRow],
    down_map: dict[float, BranchIndicatorRow],
    scales: dict[str, float],
) -> tuple[list[float], list[bool]]:
    common_p = sorted(set(up_map) & set(down_map))
    flags: list[bool] = []
    for p_value in common_p:
        up_row = up_map[p_value]
        down_row = down_map[p_value]
        mismatch = False
        for key in INDICATOR_ORDER:
            diff = abs(float(getattr(up_row, key)) - float(getattr(down_row, key)))
            if diff > indicator_tolerance(scales[key]):
                mismatch = True
                break
        flags.append(mismatch)
    return common_p, flags


def max_step_jump(rows: list[BranchIndicatorRow], scales: dict[str, float]) -> tuple[tuple[float, float] | None, float]:
    success_rows = [row for row in rows if row.success and np.all(np.isfinite([getattr(row, key) for key in INDICATOR_ORDER]))]
    if len(success_rows) < 2:
        return None, float("nan")

    best_interval: tuple[float, float] | None = None
    best_metric = -1.0
    for left, right in zip(success_rows[:-1], success_rows[1:]):
        metric = max(
            abs(float(getattr(right, key)) - float(getattr(left, key))) / max(scales[key], 1.0e-12)
            for key in INDICATOR_ORDER
        )
        if metric > best_metric:
            best_metric = float(metric)
            best_interval = (float(left.p_mpa), float(right.p_mpa))
    return best_interval, best_metric


def analyze_transition(up_rows: list[BranchIndicatorRow], down_rows: list[BranchIndicatorRow]) -> TransitionAnalysis:
    up_map = finite_success_map(up_rows)
    down_map = finite_success_map(down_rows)
    scales = indicator_scales(up_map, down_map)
    common_p, flags = mismatch_flags(up_map, down_map, scales)

    if not common_p or not any(flags):
        up_jump_interval, up_jump_metric = max_step_jump(up_rows, scales)
        down_jump_interval, down_jump_metric = max_step_jump(down_rows, scales)
        return TransitionAnalysis(
            coincide=True,
            highest_mismatch_p=None,
            next_matching_p=None,
            mismatch_interval=None,
            mismatch_range=None,
            max_up_jump_interval=up_jump_interval,
            max_up_jump_metric=up_jump_metric,
            max_down_jump_interval=down_jump_interval,
            max_down_jump_metric=down_jump_metric,
        )

    mismatch_indices = [index for index, flag in enumerate(flags) if flag]
    first_mismatch = common_p[mismatch_indices[0]]
    highest_mismatch = common_p[mismatch_indices[-1]]
    next_matching = common_p[mismatch_indices[-1] + 1] if mismatch_indices[-1] + 1 < len(common_p) else None
    mismatch_interval = (highest_mismatch, next_matching) if next_matching is not None else None
    up_jump_interval, up_jump_metric = max_step_jump(up_rows, scales)
    down_jump_interval, down_jump_metric = max_step_jump(down_rows, scales)

    return TransitionAnalysis(
        coincide=False,
        highest_mismatch_p=highest_mismatch,
        next_matching_p=next_matching,
        mismatch_interval=mismatch_interval,
        mismatch_range=(first_mismatch, highest_mismatch),
        max_up_jump_interval=up_jump_interval,
        max_up_jump_metric=up_jump_metric,
        max_down_jump_interval=down_jump_interval,
        max_down_jump_metric=down_jump_metric,
    )


def quantity_filename(key: str, p_min: float, p_max: float, num_points: int) -> str:
    return (
        f"axisymmetric_simple_support_{key}_up_down_"
        f"p{float_tag(p_min)}_to_{float_tag(p_max)}_"
        f"{int(num_points)}pts.png"
    )


def make_indicator_plot(
    key: str,
    rows_up: list[BranchIndicatorRow],
    rows_down: list[BranchIndicatorRow],
    p_min: float,
    p_max: float,
    num_points: int,
    mismatch_interval: tuple[float, float] | None,
) -> Path:
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    up_success = [row for row in rows_up if row.success and np.isfinite(getattr(row, key))]
    down_success = [row for row in rows_down if row.success and np.isfinite(getattr(row, key))]

    ax.plot(
        [row.p_mpa for row in up_success],
        [getattr(row, key) for row in up_success],
        color="tab:blue",
        linewidth=2.0,
        label="up-scan 4->5 MPa",
    )
    ax.plot(
        [row.p_mpa for row in down_success],
        [getattr(row, key) for row in down_success],
        color="tab:orange",
        linewidth=2.0,
        linestyle="--",
        label="down-scan 5->4 MPa",
    )
    if mismatch_interval is not None:
        ax.axvspan(mismatch_interval[0], mismatch_interval[1], color="0.85", alpha=0.5)
    ax.set_xlabel("p, MPa")
    ax.set_ylabel(INDICATOR_LABELS[key])
    ax.set_title(f"{INDICATOR_LABELS[key]} on honest simple-support path")
    ax.grid(True)
    ax.legend(loc="best")
    fig.tight_layout()
    return save_figure(fig, quantity_filename(key, p_min, p_max, num_points))


def summarize_modes(rows: list[BranchIndicatorRow]) -> str:
    counts = {
        "warm_start": sum(1 for row in rows if row.solve_mode == "warm_start"),
        "local_restart": sum(1 for row in rows if row.solve_mode == "local_restart"),
        "failure": sum(1 for row in rows if row.solve_mode == "failure"),
    }
    return ", ".join(f"{key}={value}" for key, value in counts.items())


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    p_up, p_down = build_pressure_grid(args.p_min, args.p_max, args.num_points)

    up_run = run_scan("up", p_up, float(args.x0), int(args.nd_eval))
    down_run = run_scan("down", p_down, float(args.x0), int(args.nd_eval))
    analysis = analyze_transition(up_run.rows, down_run.rows)

    stem = scan_stem(args.p_min, args.p_max, args.num_points)
    csv_path = save_csv(up_run.rows + down_run.rows, stem + ".csv")

    figure_paths = []
    for key in INDICATOR_ORDER:
        figure_paths.append(
            make_indicator_plot(
                key,
                up_run.rows,
                down_run.rows,
                args.p_min,
                args.p_max,
                args.num_points,
                analysis.mismatch_interval,
            )
        )

    up_failures = [row for row in up_run.rows if not row.success]
    down_failures = [row for row in down_run.rows if not row.success]

    print("=== Axisymmetric Simple-Support Branch Localization ===")
    print("background source: shell_buckling.mixed_weak.axisymmetric_simple_support_background")
    print("continuation wrapper: repaired warm_start with one local_restart on failure")
    print(f"pressure window: {args.p_min:.3f}..{args.p_max:.3f} MPa with {int(args.num_points)} points per direction")
    print(f"center proxy for u_z(0), T_s(0): x0 = {up_run.config.x0:.6f}")
    print(f"indicator grid points: {int(args.nd_eval)}")
    print(f"up-scan success: {len(up_run.rows) - len(up_failures)}/{len(up_run.rows)} ({summarize_modes(up_run.rows)})")
    print(f"down-scan success: {len(down_run.rows) - len(down_failures)}/{len(down_run.rows)} ({summarize_modes(down_run.rows)})")
    print(f"up/down coincide on common successful loads: {'yes' if analysis.coincide else 'no'}")
    if analysis.mismatch_range is not None:
        print(
            "same-load mismatch range: "
            f"{analysis.mismatch_range[0]:.3f}..{analysis.mismatch_range[1]:.3f} MPa"
        )
    else:
        print("same-load mismatch range: none")
    if analysis.mismatch_interval is not None:
        print(
            "localized transition interval: "
            f"{analysis.mismatch_interval[0]:.3f}..{analysis.mismatch_interval[1]:.3f} MPa"
        )
    else:
        print("localized transition interval: none detected")
    if analysis.max_up_jump_interval is not None:
        print(
            "largest up-scan jump: "
            f"{analysis.max_up_jump_interval[0]:.3f}..{analysis.max_up_jump_interval[1]:.3f} MPa "
            f"(normalized metric={analysis.max_up_jump_metric:.6e})"
        )
    if analysis.max_down_jump_interval is not None:
        print(
            "largest down-scan jump: "
            f"{analysis.max_down_jump_interval[0]:.3f}..{analysis.max_down_jump_interval[1]:.3f} MPa "
            f"(normalized metric={analysis.max_down_jump_metric:.6e})"
        )
    print(f"csv: {csv_path}")
    print("saved figures:")
    for path in figure_paths:
        print(f"  {path}")
    if up_failures or down_failures:
        print("failed loads:")
        for row in up_failures + down_failures:
            print(
                f"  {row.scan_direction}  step={row.continuation_step}  p={row.p_mpa:.3f} MPa  "
                f"mode={row.solve_mode}  message={row.message}"
            )
    else:
        print("failed loads: none")


if __name__ == "__main__":
    main()

