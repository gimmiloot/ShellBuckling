from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Sequence

from shell_buckling.mixed_weak import axisymmetric_simple_support_background as simple_bg


THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[3]
RUNTIME_PATH = (
    REPO_ROOT
    / "proof_pilots"
    / "pilot_21_u_z_scaled_arc_like_continuation"
    / "continuation_runtime.py"
)
DEFAULT_DIRECT_SOLVE_MAX_MPA = 4.0


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


runtime = load_module("full_simple_support_high_load_runtime", RUNTIME_PATH)
DEFAULT_HISTORY_RUN_DIR = Path(runtime.FAST_RUN_DIR)


def load_fast_progress(run_dir: Path = DEFAULT_HISTORY_RUN_DIR) -> dict[str, Any] | None:
    return runtime.load_json(Path(run_dir) / runtime.DEFAULT_PROGRESS_JSON.name)


def default_high_load_background_config(run_dir: Path = DEFAULT_HISTORY_RUN_DIR) -> simple_bg.AxisymmetricSimpleSupportConfig:
    progress = load_fast_progress(run_dir)
    profile_payload = (((progress or {}).get("metadata") or {}).get("profile") or {}).get("config") or {}
    if profile_payload:
        return simple_bg.AxisymmetricSimpleSupportConfig(**dict(profile_payload))
    return simple_bg.AxisymmetricSimpleSupportConfig(
        nd_bvp=950,
        tol=2.5e-4,
        relaxed_tol=1.2e-3,
        max_nodes=600000,
        right_edge_cluster_start=0.965,
        right_edge_cluster_fraction=0.60,
        right_edge_cluster_power=1.8,
    )


def default_step_control(run_dir: Path = DEFAULT_HISTORY_RUN_DIR) -> dict[str, Any]:
    progress = load_fast_progress(run_dir) or {"metadata": {}}
    return runtime.step_control_config(progress)


def checkpoint_exists(run_dir: Path, relative_path: str | Path | None) -> bool:
    return runtime.checkpoint_exists(Path(run_dir), relative_path)


def retained_step_indices(progress: dict[str, Any], run_dir: Path) -> list[int]:
    accepted = list(progress.get("accepted_steps") or [])
    return [idx for idx, step in enumerate(accepted) if checkpoint_exists(run_dir, step.get("checkpoint"))]


def find_exact_retained_step_index(
    progress: dict[str, Any],
    run_dir: Path,
    q_mpa: float,
    tol: float = 1.0e-6,
) -> int | None:
    accepted = list(progress.get("accepted_steps") or [])
    for idx, step in enumerate(accepted):
        q_value = runtime.float_or_none(step.get("q_mpa"))
        if q_value is None:
            continue
        if abs(q_value - float(q_mpa)) <= tol and checkpoint_exists(run_dir, step.get("checkpoint")):
            return idx
    return None


def nearest_lower_retained_step_index(
    progress: dict[str, Any],
    run_dir: Path,
    q_mpa: float,
    tol: float = 1.0e-6,
) -> int | None:
    accepted = list(progress.get("accepted_steps") or [])
    candidate: int | None = None
    candidate_q: float | None = None
    for idx, step in enumerate(accepted):
        q_value = runtime.float_or_none(step.get("q_mpa"))
        if q_value is None or q_value > float(q_mpa) + tol:
            continue
        if not checkpoint_exists(run_dir, step.get("checkpoint")):
            continue
        if candidate_q is None or q_value > candidate_q:
            candidate = idx
            candidate_q = q_value
    return candidate


def load_retained_point(progress: dict[str, Any], run_dir: Path, step_index: int):
    accepted = list(progress.get("accepted_steps") or [])
    step = accepted[int(step_index)]
    return runtime.load_point_checkpoint(run_dir, step["checkpoint"])


def load_step_context(progress: dict[str, Any], run_dir: Path, step_index: int):
    retained = retained_step_indices(progress, run_dir)
    position = retained.index(int(step_index))
    previous = load_retained_point(progress, run_dir, retained[position])
    older = load_retained_point(progress, run_dir, retained[position - 1]) if position >= 1 else None
    return older, previous


def load_named_anchor(progress: dict[str, Any], run_dir: Path):
    checkpoints = dict(progress.get("checkpoints") or {})
    relpath = checkpoints.get("scaled_anchor_checkpoint")
    if not checkpoint_exists(run_dir, relpath):
        relpath = str(runtime.named_checkpoint_relpath(runtime.SCALED_ANCHOR_FILENAME)).replace("\\", "/")
    if not checkpoint_exists(run_dir, relpath):
        raise FileNotFoundError(f"Could not find the scaled anchor checkpoint in {run_dir}.")
    return runtime.load_point_checkpoint(run_dir, relpath)


def axisymmetric_result_from_point(point, *, seed_kind: str | None = None) -> simple_bg.AxisymmetricBackgroundSolve:
    return simple_bg.AxisymmetricBackgroundSolve(
        q_mpa=float(point.q_mpa),
        success=True,
        message=str(point.message),
        nodes=int(point.nodes),
        max_rms=float(point.max_rms),
        seed_kind=str(seed_kind or point.accepted_seed),
        max_bc_residual=float(point.max_bc_residual),
        min_r=float(point.min_r),
        solution=point.solution,
    )


def failed_axisymmetric_result(q_mpa: float, attempts: Sequence[Any]) -> simple_bg.AxisymmetricBackgroundSolve:
    if attempts:
        last = attempts[-1]
        seed_kind = " -> ".join(str(item.seed_label) for item in attempts)
        return simple_bg.AxisymmetricBackgroundSolve(
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
    return simple_bg.AxisymmetricBackgroundSolve(
        q_mpa=float(q_mpa),
        success=False,
        message="No scaled continuation attempts were prepared.",
        nodes=0,
        max_rms=float("nan"),
        seed_kind="none",
        max_bc_residual=float("nan"),
        min_r=float("nan"),
        solution=None,
    )


def low_load_direct_config(config: simple_bg.AxisymmetricSimpleSupportConfig) -> simple_bg.AxisymmetricSimpleSupportConfig:
    return simple_bg.AxisymmetricSimpleSupportConfig(
        x0=float(config.x0),
        nd_bvp=int(config.nd_bvp),
        tol=float(config.tol),
        relaxed_tol=float(config.relaxed_tol),
        max_nodes=int(config.max_nodes),
        template_q_mpa=float(config.template_q_mpa),
        right_edge_cluster_start=1.0,
        right_edge_cluster_fraction=0.0,
        right_edge_cluster_power=1.0,
    )


def solve_low_load_targets(
    q_values_mpa: Sequence[float],
    config: simple_bg.AxisymmetricSimpleSupportConfig,
) -> dict[float, simple_bg.AxisymmetricBackgroundSolve]:
    if not q_values_mpa:
        return {}
    ordered = [float(q) for q in q_values_mpa]
    low_config = low_load_direct_config(config)
    results = simple_bg.solve_fixed_load_schedule(ordered, config=low_config)
    return {round(float(result.q_mpa), 7): result for result in results}


def solve_axisymmetric_simple_support_high_load_schedule(
    q_values_mpa: Sequence[float],
    config: simple_bg.AxisymmetricSimpleSupportConfig | None = None,
    *,
    history_run_dir: Path = DEFAULT_HISTORY_RUN_DIR,
    direct_solve_max_mpa: float = DEFAULT_DIRECT_SOLVE_MAX_MPA,
    step_control: dict[str, Any] | None = None,
    prefer_established_history: bool = True,
    verbose: bool = False,
) -> list[simple_bg.AxisymmetricBackgroundSolve]:
    if not q_values_mpa:
        return []

    loads = [float(q) for q in q_values_mpa]
    if any(loads[idx] > loads[idx + 1] + 1.0e-12 for idx in range(len(loads) - 1)):
        raise ValueError("High-load schedule expects nondecreasing load values.")

    run_dir = Path(history_run_dir)
    config = default_high_load_background_config(run_dir) if config is None else config
    step_control = default_step_control(run_dir) if step_control is None else dict(step_control)
    profile = runtime.pilot10.SolverProfile(
        name="clean_full_simple_support_high_load_background",
        config=config,
        description="Standalone clean critical-search background continuation using the proven u_z-scaled state representation.",
    )
    progress = load_fast_progress(run_dir) if prefer_established_history else None

    results_by_q: dict[float, simple_bg.AxisymmetricBackgroundSolve] = {}
    low_targets = [q for q in loads if q <= float(direct_solve_max_mpa) + 1.0e-12]
    results_by_q.update(solve_low_load_targets(low_targets, config=config))

    if progress is not None:
        for q in loads:
            if q <= float(direct_solve_max_mpa) + 1.0e-12:
                continue
            step_index = find_exact_retained_step_index(progress, run_dir, q)
            if step_index is None:
                continue
            point = load_retained_point(progress, run_dir, step_index)
            results_by_q[round(float(q), 7)] = axisymmetric_result_from_point(point, seed_kind=f"retained::{point.accepted_seed}")
            if verbose:
                print(f"[clean-bg-history] exact q={q:.6f} MPa seed={point.accepted_seed}")

    pending_targets = [q for q in loads if q > float(direct_solve_max_mpa) + 1.0e-12 and round(float(q), 7) not in results_by_q]
    if pending_targets:
        if progress is None:
            raise RuntimeError(
                "Missing established high-load history for the clean background continuation above the direct low-load band."
            )
        start_index = nearest_lower_retained_step_index(progress, run_dir, pending_targets[0])
        if start_index is None:
            raise RuntimeError(
                f"Could not find a retained high-load background checkpoint below {pending_targets[0]:.4f} MPa."
            )
        scaled_anchor = load_named_anchor(progress, run_dir)
        older_point, previous_point = load_step_context(progress, run_dir, start_index)
        step_mpa = float(step_control.get("initial_step_mpa", runtime.pilot21.INITIAL_STEP_MPA))
        if older_point is not None:
            step_mpa = max(step_mpa, float(previous_point.q_mpa - older_point.q_mpa))

        for target_q in pending_targets:
            while previous_point.q_mpa < float(target_q) - 1.0e-12:
                raw_step = min(float(step_mpa), float(target_q - previous_point.q_mpa))
                q_trial = round(float(previous_point.q_mpa + raw_step), 7)
                point, attempts = runtime.pilot20.try_scaled_attempts(
                    q_trial,
                    runtime.pilot20.scaled_seed_specs(
                        q_trial,
                        older_point,
                        previous_point,
                        scaled_anchor,
                        profile,
                        runtime.pilot20.U_Z_SCALE,
                    ),
                    profile,
                    runtime.pilot20.U_Z_SCALE,
                )
                if point is None:
                    if raw_step <= float(step_control.get("min_step_mpa", runtime.pilot21.MIN_STEP_MPA)) + 1.0e-12:
                        results_by_q[round(float(target_q), 7)] = failed_axisymmetric_result(target_q, attempts)
                        for q in loads:
                            key = round(float(q), 7)
                            if key in results_by_q:
                                continue
                            if q <= target_q + 1.0e-12:
                                continue
                            results_by_q[key] = simple_bg.AxisymmetricBackgroundSolve(
                                q_mpa=float(q),
                                success=False,
                                message="Not attempted after earlier clean high-load continuation failure.",
                                nodes=0,
                                max_rms=float("nan"),
                                seed_kind="not_attempted",
                                max_bc_residual=float("nan"),
                                min_r=float("nan"),
                                solution=None,
                            )
                        if verbose:
                            seed_text = " -> ".join(str(item.seed_label) for item in attempts) or "none"
                            print(f"[clean-bg-fail] target={target_q:.6f} MPa q_trial={q_trial:.6f} MPa seeds={seed_text}")
                        return [results_by_q[round(float(q), 7)] for q in loads]
                    step_mpa = max(
                        float(step_control.get("min_step_mpa", runtime.pilot21.MIN_STEP_MPA)),
                        raw_step * float(step_control.get("failure_shrink", runtime.pilot21.FAILURE_SHRINK)),
                    )
                    continue
                older_point, previous_point = previous_point, point
                step_mpa = runtime.adapt_fast_step_size(raw_step, point, step_control)
                if verbose and abs(previous_point.q_mpa - float(target_q)) <= 1.0e-12:
                    print(
                        "[clean-bg-continue] "
                        f"q={previous_point.q_mpa:.6f} MPa seed={previous_point.accepted_seed} "
                        f"node_pressure={previous_point.node_pressure:.4f} right_edge={previous_point.right_edge_fraction_0_995:.4f}"
                    )
            results_by_q[round(float(target_q), 7)] = axisymmetric_result_from_point(previous_point, seed_kind=f"scaled::{previous_point.accepted_seed}")

    return [results_by_q[round(float(q), 7)] for q in loads]


__all__ = [
    "DEFAULT_DIRECT_SOLVE_MAX_MPA",
    "DEFAULT_HISTORY_RUN_DIR",
    "default_high_load_background_config",
    "default_step_control",
    "solve_axisymmetric_simple_support_high_load_schedule",
]
