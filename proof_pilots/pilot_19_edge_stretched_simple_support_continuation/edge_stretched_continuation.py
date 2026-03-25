from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np


THIS_FILE = Path(__file__).resolve()
PILOT_DIR = THIS_FILE.parent
REPO_ROOT = THIS_FILE.parents[2]
SRC_ROOT = REPO_ROOT / "src"
DEFAULT_OUTPUT_JSON = PILOT_DIR / "edge_stretched_results.json"
RECORDED_BASELINE_JSON = (
    REPO_ROOT / "proof_pilots" / "pilot_12_high_load_branch_extension" / "extension_results.json"
)
ANCHOR_LOADS_MPA = (4.34, 4.343, 4.3432, 4.3434)
FIRST_STAGE_LOADS_MPA = (4.3440, 4.3445, 4.3450)
SECOND_STAGE_LOADS_MPA = (4.3460, 4.3475)
MATERIAL_EDGE_SHIFT_THRESHOLD_MPA = 4.3445
MIN_MESH_SPACING = 1.0e-10

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
    "pilot19_pilot10_campaign",
    REPO_ROOT / "proof_pilots" / "pilot_10_high_load_simple_support_continuation" / "continuation_campaign.py",
)
pilot18_common = load_module(
    "pilot19_pilot18_analysis_common",
    REPO_ROOT / "proof_pilots" / "pilot_18_revised_analytic_barrier_diagnosis" / "analysis_common.py",
)

from shell_buckling.mixed_weak.axisymmetric_simple_support_background import (
    AxisymmetricSimpleSupportConfig,
    default_x_mesh,
)


@dataclass(frozen=True)
class MeshStrategy:
    name: str
    description: str
    mesh_kind: str
    config: AxisymmetricSimpleSupportConfig


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--budget-seconds", type=float, default=1800.0)
    parser.add_argument("--rebuild-cache", action="store_true")
    return parser


def ensure_budget(start_time: float, budget_seconds: float, stage: str) -> None:
    if time.perf_counter() - start_time > budget_seconds:
        raise TimeoutError(f"Time budget exceeded during {stage}.")


def stabilize_mesh(x_mesh: np.ndarray, min_spacing: float = MIN_MESH_SPACING) -> np.ndarray:
    x_sorted = np.sort(np.asarray(x_mesh, dtype=float))
    kept = [float(x_sorted[0])]
    for value in x_sorted[1:]:
        if float(value) - kept[-1] >= min_spacing:
            kept.append(float(value))
    if kept[-1] < 1.0:
        kept.append(1.0)
    return np.asarray(kept, dtype=float)


def build_double_tail_mesh(config: AxisymmetricSimpleSupportConfig) -> np.ndarray:
    n_pts = int(config.nd_bvp)
    x0 = float(config.x0)
    split_mid = 0.97
    split_tail = 0.992

    n_left = max(80, int(round(0.30 * n_pts)))
    n_mid = max(120, int(round(0.35 * n_pts)))
    n_right = max(160, n_pts - n_left - n_mid + 2)

    left = np.linspace(x0, split_mid, n_left, endpoint=False)
    s_mid = np.linspace(0.0, 1.0, n_mid, endpoint=False)
    mid = split_mid + (split_tail - split_mid) * (1.0 - (1.0 - s_mid) ** 2.0)
    s_right = np.linspace(0.0, 1.0, n_right)
    right = split_tail + (1.0 - split_tail) * (1.0 - (1.0 - s_right) ** 4.0)
    return stabilize_mesh(np.concatenate([left, mid, right]))


def build_mesh(strategy: MeshStrategy) -> np.ndarray:
    if strategy.mesh_kind == "power_tail":
        return stabilize_mesh(default_x_mesh(strategy.config))
    if strategy.mesh_kind == "double_tail":
        return build_double_tail_mesh(strategy.config)
    raise ValueError(f"Unknown mesh kind: {strategy.mesh_kind}")


def make_edge_aware_strategies() -> list[MeshStrategy]:
    return [
        MeshStrategy(
            name="edge_power_tail",
            description=(
                "Single power-stretched tail mesh with moderately stronger clustering near x=1 "
                "than the current rescue-local profile."
            ),
            mesh_kind="power_tail",
            config=AxisymmetricSimpleSupportConfig(
                nd_bvp=1150,
                tol=2.5e-4,
                relaxed_tol=1.2e-3,
                max_nodes=600000,
                right_edge_cluster_start=0.978,
                right_edge_cluster_fraction=0.72,
                right_edge_cluster_power=2.6,
            ),
        ),
        MeshStrategy(
            name="edge_double_tail",
            description=(
                "Two-zone stretched tail mesh with a separate ultra-edge layer inside "
                "x in [0.992, 1]."
            ),
            mesh_kind="double_tail",
            config=AxisymmetricSimpleSupportConfig(
                nd_bvp=1250,
                tol=2.5e-4,
                relaxed_tol=1.2e-3,
                max_nodes=600000,
                right_edge_cluster_start=1.0,
                right_edge_cluster_fraction=0.0,
                right_edge_cluster_power=1.0,
            ),
        ),
    ]


def project_state(x_source: np.ndarray, y_source: np.ndarray, x_target: np.ndarray) -> np.ndarray:
    return np.vstack([np.interp(x_target, x_source, y_source[idx]) for idx in range(y_source.shape[0])])


def summarize_attempt(record) -> dict[str, Any]:
    return serializable(asdict(record))


def summarize_point(point) -> dict[str, Any]:
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


def select_failure_representative_payload(attempts: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not attempts:
        return None
    mesh_pressure = [attempt for attempt in attempts if attempt.get("mesh_pressure_only")]
    if mesh_pressure:
        return max(mesh_pressure, key=lambda attempt: (attempt.get("node_pressure", 0.0), attempt.get("nodes", 0)))
    return attempts[0]


def load_recorded_baseline() -> dict[str, Any]:
    payload = json.loads(RECORDED_BASELINE_JSON.read_text(encoding="utf-8"))
    return {
        "source": "pilot_12_high_load_branch_extension",
        "highest_converged_q_mpa": payload["overall"]["highest_converged_q_mpa"],
        "first_failure_q_mpa": payload["overall"]["first_failure_q_mpa"],
        "highest_success": payload["reproducibility"]["point_a"],
        "first_failure": payload["stages"][0]["steps"][0]["attempts"][0],
        "bottleneck_summary": payload["overall"]["bottleneck_summary"],
        "retest_4_3434_reproducible": payload["overall"]["retest_4_3434_reproducible"],
    }


def load_cached_states(rebuild_cache: bool, budget_seconds: float) -> tuple[np.ndarray, dict[float, np.ndarray]]:
    _, arrays = pilot18_common.ensure_branch_cache(
        rebuild=rebuild_cache,
        budget_seconds=budget_seconds,
    )
    loads = np.asarray(arrays["loads_mpa"], dtype=float)
    balance_grid = np.asarray(arrays["balance_grid"], dtype=float)
    balance_states = np.asarray(arrays["balance_states"], dtype=float)
    states_by_load = {
        float(load): np.asarray(balance_states[idx], dtype=float)
        for idx, load in enumerate(loads)
    }
    missing = [load for load in ANCHOR_LOADS_MPA if load not in states_by_load]
    if missing:
        raise RuntimeError(f"Cached branch data is missing required loads: {missing}")
    return balance_grid, states_by_load


def solve_with_seeds(q_mpa: float, strategy: MeshStrategy, seeds: list[Any]) -> tuple[Any | None, list[dict[str, Any]]]:
    profile = pilot10.SolverProfile(strategy.name, strategy.config, strategy.description)
    attempt_payloads: list[dict[str, Any]] = []
    for seed in seeds:
        attempt_start = time.perf_counter()
        sol = pilot10.run_bvp_attempt(q_mpa, seed.x_mesh, seed.y_guess, strategy.config)
        record = pilot10.build_attempt_record(
            q_mpa,
            profile,
            seed,
            sol,
            attempt_seconds=time.perf_counter() - attempt_start,
        )
        attempt_payloads.append(summarize_attempt(record))
        if record.success:
            return pilot10.build_branch_point(record, sol), attempt_payloads
    return None, attempt_payloads


def cached_seed(label: str, x_mesh: np.ndarray, x_cache: np.ndarray, y_cache: np.ndarray):
    return pilot10.SeedSpec(label=label, x_mesh=x_mesh, y_guess=project_state(x_cache, y_cache, x_mesh))


def previous_seed(label: str, point):
    return pilot10.SeedSpec(label=label, x_mesh=point.x, y_guess=point.y)


def secant_seed(q_target_mpa: float, older_point, previous_point):
    dq = float(previous_point.q_mpa - older_point.q_mpa)
    if abs(dq) < 1.0e-14:
        return None
    older_on_previous = project_state(older_point.x, older_point.y, previous_point.x)
    guess = previous_point.y + ((float(q_target_mpa) - previous_point.q_mpa) / dq) * (previous_point.y - older_on_previous)
    return pilot10.SeedSpec(label="secant_predictor", x_mesh=previous_point.x, y_guess=guess)


def run_strategy(
    strategy: MeshStrategy,
    x_cache: np.ndarray,
    states_by_load: dict[float, np.ndarray],
    start_time: float,
    budget_seconds: float,
) -> dict[str, Any]:
    x_mesh = build_mesh(strategy)
    anchor_results: list[dict[str, Any]] = []
    anchor_points: list[Any] = []

    for q_mpa in ANCHOR_LOADS_MPA:
        ensure_budget(start_time, budget_seconds, f"{strategy.name} anchor {q_mpa:.4f} MPa")
        seeds = []
        if anchor_points:
            seeds.append(previous_seed("previous_anchor_solution", anchor_points[-1]))
        seeds.append(cached_seed("cached_branch_projection", x_mesh, x_cache, states_by_load[q_mpa]))
        point, attempts = solve_with_seeds(q_mpa, strategy, seeds)
        anchor_results.append(
            {
                "q_mpa": float(q_mpa),
                "attempts": attempts,
                "success": point is not None,
            }
        )
        if point is None:
            failure = select_failure_representative_payload(attempts)
            return {
                "strategy": {
                    "name": strategy.name,
                    "description": strategy.description,
                    "mesh_kind": strategy.mesh_kind,
                    "config": serializable(asdict(strategy.config)),
                },
                "anchor_results": anchor_results,
                "stages": [],
                "highest_converged_q_mpa": None,
                "first_failure_q_mpa": float(q_mpa),
                "highest_success": None,
                "first_failure": failure,
                "ceiling_moved_materially": False,
                "bottleneck_still_looks_numerical": bool(
                    failure is not None and failure.get("mesh_pressure_only") and not failure.get("branch_turning_suspicion")
                ),
                "stopped_reason": f"anchor failure at {q_mpa:.4f} MPa",
            }
        anchor_points.append(point)

    stages: list[dict[str, Any]] = []
    older_point = anchor_points[-2]
    previous_point = anchor_points[-1]
    anchor_point = anchor_points[-1]

    for stage_name, loads in (("first_stage", FIRST_STAGE_LOADS_MPA), ("second_stage", SECOND_STAGE_LOADS_MPA)):
        steps: list[dict[str, Any]] = []
        first_failure_q_mpa = None
        for q_target in loads:
            ensure_budget(start_time, budget_seconds, f"{strategy.name} {stage_name} {q_target:.4f} MPa")
            seeds = []
            secant = secant_seed(q_target, older_point, previous_point)
            if secant is not None:
                seeds.append(secant)
            seeds.append(previous_seed("previous_solution", previous_point))
            seeds.append(previous_seed("anchor_solution", anchor_point))
            point, attempts = solve_with_seeds(q_target, strategy, seeds)
            step = {
                "q_target_mpa": float(q_target),
                "attempts": attempts,
                "success": point is not None,
                "failure_representative": select_failure_representative_payload(attempts),
            }
            if point is None:
                first_failure_q_mpa = float(q_target)
                steps.append(step)
                stages.append(
                    {
                        "name": stage_name,
                        "loads_mpa": list(loads),
                        "steps": steps,
                        "stopped_reason": f"failure at {q_target:.4f} MPa",
                        "first_failure_q_mpa": first_failure_q_mpa,
                    }
                )
                highest_success = previous_point
                failure = step["failure_representative"]
                return {
                    "strategy": {
                        "name": strategy.name,
                        "description": strategy.description,
                        "mesh_kind": strategy.mesh_kind,
                        "config": serializable(asdict(strategy.config)),
                    },
                    "anchor_results": anchor_results,
                    "stages": stages,
                    "highest_converged_q_mpa": float(highest_success.q_mpa),
                    "first_failure_q_mpa": first_failure_q_mpa,
                    "highest_success": summarize_point(highest_success),
                    "first_failure": failure,
                    "ceiling_moved_materially": float(highest_success.q_mpa) >= MATERIAL_EDGE_SHIFT_THRESHOLD_MPA - 1.0e-12,
                    "bottleneck_still_looks_numerical": bool(
                        failure is not None and failure.get("mesh_pressure_only") and not failure.get("branch_turning_suspicion")
                    ),
                    "stopped_reason": f"failure at {q_target:.4f} MPa",
                }
            step["accepted_point"] = summarize_point(point)
            steps.append(step)
            older_point, previous_point = previous_point, point

        stages.append(
            {
                "name": stage_name,
                "loads_mpa": list(loads),
                "steps": steps,
                "stopped_reason": "completed",
                "first_failure_q_mpa": None,
            }
        )

    highest_success = previous_point
    return {
        "strategy": {
            "name": strategy.name,
            "description": strategy.description,
            "mesh_kind": strategy.mesh_kind,
            "config": serializable(asdict(strategy.config)),
        },
        "anchor_results": anchor_results,
        "stages": stages,
        "highest_converged_q_mpa": float(highest_success.q_mpa),
        "first_failure_q_mpa": None,
        "highest_success": summarize_point(highest_success),
        "first_failure": None,
        "ceiling_moved_materially": float(highest_success.q_mpa) >= MATERIAL_EDGE_SHIFT_THRESHOLD_MPA - 1.0e-12,
        "bottleneck_still_looks_numerical": None,
        "stopped_reason": "completed bounded ladder",
    }


def best_edge_aware_run(runs: list[dict[str, Any]]) -> dict[str, Any] | None:
    finished = [run for run in runs if run.get("highest_converged_q_mpa") is not None]
    if not finished:
        return None
    return max(
        finished,
        key=lambda run: (
            float(run["highest_converged_q_mpa"]),
            float("inf") if run.get("first_failure_q_mpa") is None else float(run["first_failure_q_mpa"]),
        ),
    )


def print_baseline_summary(baseline: dict[str, Any]) -> None:
    highest = baseline["highest_success"]
    failure = baseline["first_failure"]
    print("Recorded old path from pilot 12")
    print(
        f"  highest converged load: {baseline['highest_converged_q_mpa']:.4f} MPa  "
        f"BC={highest['max_bc_residual']:.3e}  x>0.995={highest['right_edge_fraction_0_995']:.3f}"
    )
    print(
        f"  first failure load:     {baseline['first_failure_q_mpa']:.4f} MPa  "
        f"BC={failure['max_bc_residual']:.3e}  x>0.995={failure['right_edge_fraction_0_995']:.3f}"
    )
    print()


def print_edge_run_summary(run: dict[str, Any]) -> None:
    highest = run.get("highest_success")
    failure = run.get("first_failure")
    print(run["strategy"]["name"])
    print(f"  description: {run['strategy']['description']}")
    if highest is None:
        print(f"  stopped early: {run['stopped_reason']}")
        print()
        return
    print(
        f"  highest converged load: {run['highest_converged_q_mpa']:.4f} MPa  "
        f"BC={highest['max_bc_residual']:.3e}  x>0.995={highest['right_edge_fraction_0_995']:.3f}"
    )
    if failure is not None and run.get("first_failure_q_mpa") is not None:
        print(
            f"  first failure load:     {run['first_failure_q_mpa']:.4f} MPa  "
            f"BC={failure['max_bc_residual']:.3e}  x>0.995={failure['right_edge_fraction_0_995']:.3f}"
        )
    else:
        print("  first failure load:     none inside the bounded ladder")
    print(f"  moved materially beyond 4.3440 MPa band: {run['ceiling_moved_materially']}")
    print(f"  bottleneck still looks numerical:        {run['bottleneck_still_looks_numerical']}")
    print()


def main() -> None:
    args = build_parser().parse_args()
    start_time = time.perf_counter()

    baseline = load_recorded_baseline()
    x_cache, states_by_load = load_cached_states(
        rebuild_cache=bool(args.rebuild_cache),
        budget_seconds=float(args.budget_seconds),
    )
    payload: dict[str, Any] = {
        "metadata": {
            "pilot": "pilot_19_edge_stretched_simple_support_continuation",
            "baseline_source_json": str(RECORDED_BASELINE_JSON),
            "branch_cache_source_json": str(
                REPO_ROOT / "proof_pilots" / "pilot_18_revised_analytic_barrier_diagnosis" / "branch_state_cache.json"
            ),
            "anchor_loads_mpa": list(ANCHOR_LOADS_MPA),
            "first_stage_loads_mpa": list(FIRST_STAGE_LOADS_MPA),
            "second_stage_loads_mpa": list(SECOND_STAGE_LOADS_MPA),
            "material_edge_shift_threshold_mpa": MATERIAL_EDGE_SHIFT_THRESHOLD_MPA,
            "same_equations_as_active_6_state_path": True,
            "same_simple_support_bcs": True,
            "changes_only_numerical_representation_near_x1": True,
            "budget_seconds": float(args.budget_seconds),
        },
        "baseline_old_path": baseline,
        "edge_aware_runs": [],
        "status": "started",
    }
    save_json(args.output_json, payload)

    print("=== Pilot 19 edge-stretched simple-support continuation ===")
    print_baseline_summary(baseline)

    for strategy in make_edge_aware_strategies():
        ensure_budget(start_time, float(args.budget_seconds), f"strategy {strategy.name}")
        run = run_strategy(strategy, x_cache, states_by_load, start_time, float(args.budget_seconds))
        payload["edge_aware_runs"].append(run)
        payload["status"] = f"completed_{strategy.name}"
        save_json(args.output_json, payload)
        print_edge_run_summary(run)

    best_run = best_edge_aware_run(payload["edge_aware_runs"])
    payload["status"] = "completed"
    payload["elapsed_seconds"] = time.perf_counter() - start_time
    payload["best_edge_aware"] = best_run
    payload["overall"] = {
        "old_highest_converged_q_mpa": baseline["highest_converged_q_mpa"],
        "old_first_failure_q_mpa": baseline["first_failure_q_mpa"],
        "best_edge_aware_highest_converged_q_mpa": None if best_run is None else best_run["highest_converged_q_mpa"],
        "best_edge_aware_first_failure_q_mpa": None if best_run is None else best_run["first_failure_q_mpa"],
        "best_edge_aware_strategy": None if best_run is None else best_run["strategy"]["name"],
        "ceiling_shift_mpa": None
        if best_run is None
        else float(best_run["highest_converged_q_mpa"] - baseline["highest_converged_q_mpa"]),
        "ceiling_moved_materially": False if best_run is None else best_run["ceiling_moved_materially"],
        "bottleneck_still_looks_numerical": None
        if best_run is None
        else best_run["bottleneck_still_looks_numerical"],
    }
    save_json(args.output_json, payload)

    print("Overall best edge-aware result")
    if best_run is None:
        print("  no edge-aware strategy reached a converged high-load anchor.")
    else:
        print(
            f"  best strategy: {best_run['strategy']['name']}  "
            f"highest={best_run['highest_converged_q_mpa']:.4f} MPa  "
            f"first_failure={best_run['first_failure_q_mpa']}"
        )
        print(f"  ceiling moved materially: {best_run['ceiling_moved_materially']}")
        print(f"  bottleneck still looks numerical: {best_run['bottleneck_still_looks_numerical']}")
    print(f"Results written to: {args.output_json}")


if __name__ == "__main__":
    main()
