from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


THIS_FILE = Path(__file__).resolve()
PILOT_DIR = THIS_FILE.parent
REPO_ROOT = THIS_FILE.parents[2]
SRC_ROOT = REPO_ROOT / "src"
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


pilot12 = load_module(
    "pilot22_high_load_branch_extension",
    REPO_ROOT / "proof_pilots" / "pilot_12_high_load_branch_extension" / "numerical_extension.py",
)
pilot16 = load_module(
    "pilot22_shallow_simple_support_solver",
    REPO_ROOT / "proof_pilots" / "pilot_16_shallow_simple_support_comparator" / "shallow_simple_support_solver.py",
)
pilot17 = load_module(
    "pilot22_shallow_vs_nonshallow_numerical_comparison",
    REPO_ROOT / "proof_pilots" / "pilot_17_shallow_vs_nonshallow_simple_support_divergence" / "numerical_comparison.py",
)
pilot21_runtime = load_module(
    "pilot22_pilot21_runtime",
    REPO_ROOT / "proof_pilots" / "pilot_21_u_z_scaled_arc_like_continuation" / "continuation_runtime.py",
)

from shell_buckling.mixed_weak.axisymmetric_simple_support_background import (
    AxisymmetricSimpleSupportConfig,
    solve_axisymmetric_simple_support_continuation,
)
from shell_buckling.supporting import determinant_criterion_comparison as detcomp


TARGET_LOADS_MPA = (4.0, 7.0, 10.0)
DISPLAY_NAMES = {
    "theta0": "theta",
    "theta0p": "theta'",
    "Phi0": "Phi",
    "Phi0p": "Phi'",
}
DEFAULT_FAST_RUN_DIR = (
    REPO_ROOT / "proof_pilots" / "pilot_21_u_z_scaled_arc_like_continuation" / "fast_run"
)
DEFAULT_RESULTS_JSON = PILOT_DIR / "comparison_results.json"
DEFAULT_NOTE_MD = PILOT_DIR / "pilot_22_exact_load_shallow_vs_current_simple_support_comparison.md"
DEFAULT_FIGURE_DIR = PILOT_DIR / "figures"


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


def load_fast_progress(run_dir: Path) -> dict[str, Any]:
    progress_path = run_dir / pilot21_runtime.DEFAULT_PROGRESS_JSON.name
    progress = pilot21_runtime.load_json(progress_path)
    if progress is None:
        raise RuntimeError(f"Missing fast progress file: {progress_path}")
    return progress


def load_confirm_payload(run_dir: Path) -> dict[str, Any] | None:
    confirm_path = run_dir / pilot21_runtime.DEFAULT_CONFIRM_JSON.name
    return pilot21_runtime.load_json(confirm_path)


def solve_shallow_targets(loads_mpa: tuple[float, ...]) -> tuple[dict[float, Any], list[dict[str, Any]]]:
    config = pilot16.ShallowSimpleSupportConfig(
        nd_bvp=1500,
        tol=1.0e-5,
        relaxed_tol=5.0e-5,
        max_nodes=80000,
        substep_max_delta_mpa=0.25,
    )
    results = pilot16.solve_shallow_simple_support_continuation(loads_mpa, config=config)
    by_q: dict[float, Any] = {}
    summaries: list[dict[str, Any]] = []
    for item in results:
        summaries.append(
            {
                "q_mpa": float(item.q_mpa),
                "success": bool(item.success),
                "message": str(item.message),
                "nodes": int(item.nodes),
                "max_rms": serializable(item.max_rms),
                "max_bc_residual": serializable(item.max_bc_residual),
                "edge_moment_residual": serializable(item.edge_moment_residual),
                "max_abs_theta0": serializable(item.max_abs_theta0),
                "max_abs_Phi0": serializable(item.max_abs_Phi0),
                "max_abs_u_z_recovered": serializable(item.max_abs_u_z_recovered),
            }
        )
        if item.success and item.solution is not None:
            by_q[float(item.q_mpa)] = item.solution
    return by_q, summaries


def solve_current_low_target(q_mpa: float) -> tuple[Any, list[dict[str, Any]]]:
    low_schedule = (0.02, 0.05, 0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, float(q_mpa))
    config = AxisymmetricSimpleSupportConfig(
        nd_bvp=600,
        tol=2.0e-4,
        relaxed_tol=1.0e-3,
        max_nodes=240000,
    )
    results = solve_axisymmetric_simple_support_continuation(low_schedule, config=config)
    summaries = [
        {
            "q_mpa": float(item.q_mpa),
            "success": bool(item.success),
            "message": str(item.message),
            "nodes": int(item.nodes),
            "seed_kind": str(item.seed_kind),
            "max_rms": serializable(item.max_rms),
            "max_bc_residual": serializable(item.max_bc_residual),
            "min_r": serializable(item.min_r),
        }
        for item in results
    ]
    last = results[-1]
    if not last.success or last.solution is None or abs(float(last.q_mpa) - float(q_mpa)) > 1.0e-9:
        raise RuntimeError(f"Low-load current-system solve did not reach q={q_mpa:.4f} MPa exactly.")
    return last.solution, summaries


def load_current_fast_target(run_dir: Path, progress: dict[str, Any], q_mpa: float) -> tuple[Any, dict[str, Any]]:
    step_index = pilot21_runtime.find_step_index(progress, float(q_mpa))
    accepted_steps = progress.get("accepted_steps") or []
    step_entry = accepted_steps[step_index]
    pilot21_runtime.ensure_step_checkpoint_available(run_dir, step_entry)
    point = pilot21_runtime.load_point_checkpoint(run_dir, step_entry["checkpoint"])
    if getattr(point, "solution", None) is None:
        raise RuntimeError(
            f"Stored checkpoint at q={q_mpa:.4f} MPa does not contain a reconstructable solution proxy."
        )
    metadata = {
        "q_mpa": float(q_mpa),
        "step_index": int(step_index),
        "checkpoint": str(step_entry["checkpoint"]),
        "step_size_mpa": pilot21_runtime.float_or_none(step_entry.get("step_size_mpa")),
        "checkpoint_retained": bool(step_entry.get("checkpoint_retained")),
        "checkpoint_tags": list(step_entry.get("checkpoint_tags") or []),
        "accepted_point": step_entry.get("accepted_point") or pilot21_runtime.pilot21.point_summary(point),
    }
    return point.solution, metadata


def load_confirm_summaries(confirm_payload: dict[str, Any] | None) -> dict[float, dict[str, Any]]:
    if not confirm_payload:
        return {}
    mapped: dict[float, dict[str, Any]] = {}
    for item in confirm_payload.get("results") or []:
        mapped[float(item["q_mpa"])] = item
    return mapped


def plot_load(
    *,
    q_mpa: float,
    x_grid: np.ndarray,
    shallow_data: dict[str, np.ndarray],
    current_data: dict[str, np.ndarray],
    figure_path: Path,
) -> None:
    figure_path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 4, figsize=(22, 4.8), constrained_layout=True)
    order = ("theta0", "theta0p", "Phi0", "Phi0p")
    for ax, name in zip(axes, order, strict=True):
        ax.plot(x_grid, shallow_data[name], color="#1f4e79", linewidth=2.0, label="old shallow")
        ax.plot(
            x_grid,
            current_data[name],
            color="#b22222",
            linewidth=1.8,
            linestyle="--",
            label="mapped current 6-state",
        )
        ax.set_title(DISPLAY_NAMES[name])
        ax.set_xlabel("x")
        ax.grid(True, alpha=0.25)
    axes[0].set_ylabel("value")
    axes[-1].legend(loc="best", frameon=False)
    fig.suptitle(
        f"Exact-load shallow vs mapped current simple-support comparison at q={q_mpa:.1f} MPa",
        fontsize=13,
    )
    fig.savefig(figure_path, dpi=180)
    plt.close(fig)


def qualitative_label(mean_bulk_rel_l2: float, clear_variables: list[str]) -> str:
    if mean_bulk_rel_l2 < 0.05 and not clear_variables:
        return "curves stay fairly close on the shared grid"
    if mean_bulk_rel_l2 < 0.15:
        return "visible but still moderate divergence"
    return "clear visible divergence"


def build_markdown_note(results_payload: dict[str, Any]) -> str:
    lines = [
        "# Pilot 22 Exact-Load Shallow vs Current Simple-Support Comparison",
        "",
        "## Scope",
        "",
        "- old shallow system: `proof_pilots/pilot_16_shallow_simple_support_comparator/shallow_simple_support_solver.py`",
        "- current mapped quantities: `src/shell_buckling/supporting/determinant_criterion_comparison.py::arrays_nepol_sin`",
        "- exact comparison loads: `4.0`, `7.0`, `10.0 MPa`",
        "- equations unchanged, simple-support BCs unchanged, mixed-weak scans untouched",
        "",
        "## Mapping Used",
        "",
        "- old shallow arrays: `arrays_shallow(sol, x)` with `theta0=y[1]`, `theta0'=y[0]`, `Phi0=y[3]`, `Phi0'=y[2]`",
        "- mapped current arrays: `arrays_nepol_sin(sol, x)`",
        "- `theta0 = -beta * sin(phi)`",
        "- `theta0' = -beta * cos(phi) * kappa_s`",
        "- `Phi0 = gamma * x * T_s`",
        "- `Phi0' = gamma * T_theta`",
        "- `T_theta = nu * T_s + u_r / x`",
        "- `kappa_s = 12 * (1 - nu^2) * M_s * mu^2 - nu * sin(phi) / r`, `r = x + u_r`",
        "",
        "## Load Summary",
        "",
        "| Load MPa | Old shallow | Current 6-state | Figure | Interpretation |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in results_payload["loads"]:
        lines.append(
            f"| {item['q_mpa']:.1f} | {item['old_source']} | {item['current_source']} | "
            f"`{Path(item['figure']).name}` | {item['interpretation']} |"
        )
    lines.extend(
        [
            "",
            "## Operational Outcome",
            "",
            f"- current fast path highest stored load: `{results_payload['current_fast_run']['highest_converged_q_mpa']:.4f} MPa`",
            f"- current fast path bounded first failure: `{results_payload['current_fast_run']['terminal_failure_q_mpa']}`",
            f"- shallow path last success in this pilot: `{results_payload['shallow_path']['last_success_mpa']}`",
            f"- shallow path first failure in this pilot: `{results_payload['shallow_path']['first_failure_mpa']}`",
            "",
            "## Notes",
            "",
            "- `4.0 MPa` on the current 6-state side is an exact low-load continuation solve, not an interpolated fast-run checkpoint.",
            "- `7.0` and `10.0 MPa` on the current 6-state side are exact retained pilot-21 fast-run checkpoints.",
            "- The status language above the audited `4.3800 MPa` ceiling remains operational only; nothing here promotes `7..10 MPa` to a new audited ceiling.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fast-run-dir", type=Path, default=DEFAULT_FAST_RUN_DIR)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_RESULTS_JSON)
    parser.add_argument("--note-md", type=Path, default=DEFAULT_NOTE_MD)
    parser.add_argument("--figure-dir", type=Path, default=DEFAULT_FIGURE_DIR)
    parser.add_argument("--loads-mpa", type=float, nargs="+", default=list(TARGET_LOADS_MPA))
    return parser


def main() -> None:
    args = build_parser().parse_args()
    start = time.perf_counter()
    target_loads = tuple(float(value) for value in args.loads_mpa)
    fast_run_dir = args.fast_run_dir.resolve()
    progress = load_fast_progress(fast_run_dir)
    confirm_payload = load_confirm_payload(fast_run_dir)
    confirm_by_q = load_confirm_summaries(confirm_payload)

    profile = pilot21_runtime.profile_from_metadata(progress["metadata"]["profile"])
    x_grid = pilot12.build_comparison_grid(profile.config, n_left=1400, n_right=1000)

    shallow_by_q, shallow_summaries = solve_shallow_targets(target_loads)
    low_current_solution, low_current_summaries = solve_current_low_target(4.0)

    current_by_q: dict[float, Any] = {4.0: low_current_solution}
    current_sources: dict[float, dict[str, Any]] = {
        4.0: {
            "source": "exact low-load 6-state continuation solve",
            "details": low_current_summaries[-1],
        }
    }
    for q_mpa in target_loads:
        if q_mpa <= 4.0 + 1.0e-12:
            continue
        point, metadata = load_current_fast_target(fast_run_dir, progress, q_mpa)
        current_by_q[float(q_mpa)] = point
        current_sources[float(q_mpa)] = {
            "source": "exact retained pilot-21 fast-run checkpoint",
            "details": metadata,
            "confirm": confirm_by_q.get(float(q_mpa)),
        }

    missing_shallow = [q for q in target_loads if q not in shallow_by_q]
    missing_current = [q for q in target_loads if q not in current_by_q]
    if missing_shallow or missing_current:
        raise RuntimeError(f"Missing exact-load solutions. shallow={missing_shallow}, current={missing_current}")

    load_results: list[dict[str, Any]] = []
    comparison_results: list[dict[str, Any]] = []
    for q_mpa in target_loads:
        shallow_sol = shallow_by_q[q_mpa]
        current_sol = current_by_q[q_mpa]
        compare_summary, _state, _mapped_stack, _shallow_stack = pilot17.compare_load(
            q_mpa,
            shallow_sol,
            current_sol,
            x_grid,
        )
        comparison_results.append(compare_summary)
        shallow_data = pilot17.shallow_arrays(shallow_sol, x_grid)
        current_data, _ = pilot17.mapped_nonshallow_arrays(current_sol, x_grid)

        figure_path = args.figure_dir.resolve() / f"current_vs_shallow_exact_{q_mpa:.1f}_mpa.png"
        plot_load(
            q_mpa=q_mpa,
            x_grid=x_grid,
            shallow_data=shallow_data,
            current_data=current_data,
            figure_path=figure_path,
        )
        overall = compare_summary["overall"]
        load_results.append(
            {
                "q_mpa": float(q_mpa),
                "old_source": "exact pilot-16 shallow continuation solve",
                "current_source": current_sources[q_mpa]["source"],
                "figure": str(figure_path),
                "interpretation": qualitative_label(
                    float(overall["mean_bulk_rel_l2"]),
                    list(overall["clear_variables_at_threshold"]),
                ),
                "comparison": compare_summary,
                "current_source_details": current_sources[q_mpa]["details"],
                "confirm": current_sources[q_mpa].get("confirm"),
            }
        )

    current_fast_summary = progress.get("summary") or {}
    shallow_success = [item["q_mpa"] for item in shallow_summaries if item["success"]]
    shallow_first_failure = next((item["q_mpa"] for item in shallow_summaries if not item["success"]), None)
    payload = {
        "metadata": {
            "pilot": "pilot_22_exact_load_shallow_vs_current_simple_support_comparison",
            "created_at_seconds": float(time.perf_counter() - start),
            "target_loads_mpa": list(target_loads),
            "same_equations_as_active_6_state_path": True,
            "same_simple_support_bcs": True,
            "mapping_source_function": "src/shell_buckling/supporting/determinant_criterion_comparison.py::arrays_nepol_sin",
            "shallow_source_function": "src/shell_buckling/supporting/determinant_criterion_comparison.py::arrays_shallow",
            "mapping_formulas": {
                "theta0": "-beta * sin(phi)",
                "theta0p": "-beta * cos(phi) * kappa_s",
                "Phi0": "gamma * x * T_s",
                "Phi0p": "gamma * T_theta",
                "T_theta": "nu * T_s + u_r / x",
                "kappa_s": "12 * (1 - nu^2) * M_s * mu^2 - nu * sin(phi) / r",
                "r": "x + u_r",
            },
            "fast_run_dir": str(fast_run_dir),
        },
        "current_fast_run": {
            "highest_converged_q_mpa": pilot21_runtime.float_or_none(current_fast_summary.get("highest_converged_q_mpa")),
            "terminal_failure_q_mpa": pilot21_runtime.float_or_none(current_fast_summary.get("terminal_failure_q_mpa")),
            "accepted_step_count": int(current_fast_summary.get("accepted_step_count") or 0),
            "retained_confirmable_loads_mpa": list(current_fast_summary.get("retained_confirmable_loads_mpa") or []),
            "planned_long_climb_milestones_mpa": list(current_fast_summary.get("planned_long_climb_milestones_mpa") or []),
        },
        "shallow_path": {
            "summaries": shallow_summaries,
            "last_success_mpa": None if not shallow_success else float(shallow_success[-1]),
            "first_failure_mpa": None if shallow_first_failure is None else float(shallow_first_failure),
        },
        "current_low_load_path": {
            "summaries": low_current_summaries,
        },
        "loads": load_results,
        "sweep_summary": pilot17.summarize_sweep(comparison_results),
    }

    output_json = args.output_json.resolve()
    output_note = args.note_md.resolve()
    save_json(output_json, payload)
    output_note.parent.mkdir(parents=True, exist_ok=True)
    output_note.write_text(build_markdown_note(payload), encoding="utf-8")

    print("=== Pilot 22 exact-load comparison ===")
    print(f"Loads: {list(target_loads)}")
    print(f"Current fast highest load: {payload['current_fast_run']['highest_converged_q_mpa']}")
    print(f"Shallow last success: {payload['shallow_path']['last_success_mpa']}")
    for item in load_results:
        overall = item["comparison"]["overall"]
        print(
            f"q={item['q_mpa']:.1f} MPa: mean_bulk_rel_l2={overall['mean_bulk_rel_l2']:.4f}, "
            f"clear_variables={overall['clear_variables_at_threshold']}, figure={Path(item['figure']).name}"
        )
    print(f"Saved results to: {output_json}")
    print(f"Saved note to: {output_note}")


if __name__ == "__main__":
    main()
