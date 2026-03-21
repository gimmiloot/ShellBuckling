from __future__ import annotations

import importlib.util
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np


THIS_FILE = Path(__file__).resolve()
PILOT_DIR = THIS_FILE.parent
REPO_ROOT = THIS_FILE.parents[2]
SRC_ROOT = REPO_ROOT / "src"
DEFAULT_CACHE_NPZ = PILOT_DIR / "branch_state_cache.npz"
DEFAULT_CACHE_JSON = PILOT_DIR / "branch_state_cache.json"
CONVERGED_LOADS_MPA = (4.34, 4.343, 4.3432, 4.3434)
FAILED_TARGET_LOAD_MPA = 4.3440

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
    "pilot18_pilot12_branch_extension",
    REPO_ROOT / "proof_pilots" / "pilot_12_high_load_branch_extension" / "numerical_extension.py",
)
pilot10 = load_module(
    "pilot18_pilot10_campaign",
    REPO_ROOT / "proof_pilots" / "pilot_10_high_load_simple_support_continuation" / "continuation_campaign.py",
)

from shell_buckling.mixed_weak.axisymmetric_simple_support_background import AxisymmetricSimpleSupportConfig, default_x_mesh


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


def build_jacobian_grid(config) -> np.ndarray:
    diagnostic = AxisymmetricSimpleSupportConfig(
        x0=float(config.x0),
        nd_bvp=36,
        tol=float(config.tol),
        relaxed_tol=float(config.relaxed_tol),
        max_nodes=int(config.max_nodes),
        template_q_mpa=float(config.template_q_mpa),
        right_edge_cluster_start=float(config.right_edge_cluster_start),
        right_edge_cluster_fraction=float(config.right_edge_cluster_fraction),
        right_edge_cluster_power=float(config.right_edge_cluster_power),
    )
    return default_x_mesh(diagnostic)


def build_balance_grid(config, n_left: int = 600, n_right: int = 800) -> np.ndarray:
    x0 = float(config.x0)
    split = 0.97
    left = np.linspace(x0, split, n_left, endpoint=False)
    s = np.linspace(0.0, 1.0, n_right)
    right = split + (1.0 - split) * (1.0 - (1.0 - s) ** 3.0)
    grid = np.unique(np.concatenate([left, right]))
    if grid[0] > x0:
        grid = np.insert(grid, 0, x0)
    if grid[-1] < 1.0:
        grid = np.append(grid, 1.0)
    return grid


def point_summary(point) -> dict[str, Any]:
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


def _collect_branch_bundle(budget_seconds: float) -> tuple[dict[str, Any], dict[float, Any], Any, Any, Any]:
    start_time = time.perf_counter()
    points_by_q, bootstrap_attempts, local_anchor, older_point, previous_point, bootstrap_payload = pilot12.bootstrap_branch(
        start_time,
        budget_seconds,
    )
    point_43434, attempts_43434 = pilot12.try_extension_step(
        4.3434,
        older_point,
        previous_point,
        local_anchor,
        pilot12.PRIMARY_PROFILE,
        start_time,
        budget_seconds,
    )
    if point_43434 is None:
        raise RuntimeError("Could not reproduce the 4.3434 MPa branch anchor while building pilot-18 diagnostics.")

    branch_points = {float(q): point for q, point in points_by_q.items()}
    branch_points[4.3434] = point_43434

    seeds = pilot10.make_seed_specs(
        FAILED_TARGET_LOAD_MPA,
        branch_points[4.3433],
        point_43434,
        local_anchor,
        pilot12.PRIMARY_PROFILE,
    )
    failed_seed = next(seed for seed in seeds if seed.label == "secant_profile_mesh")
    attempt_start = time.perf_counter()
    failed_sol = pilot10.run_bvp_attempt(
        FAILED_TARGET_LOAD_MPA,
        failed_seed.x_mesh,
        failed_seed.y_guess,
        pilot12.PRIMARY_PROFILE.config,
    )
    failed_record = pilot10.build_attempt_record(
        FAILED_TARGET_LOAD_MPA,
        pilot12.PRIMARY_PROFILE,
        failed_seed,
        failed_sol,
        attempt_seconds=time.perf_counter() - attempt_start,
    )

    metadata = {
        "profile": {
            "name": pilot12.PRIMARY_PROFILE.name,
            "description": pilot12.PRIMARY_PROFILE.description,
        },
        "elapsed_seconds": time.perf_counter() - start_time,
        "bootstrap": bootstrap_payload,
        "reproduced_43434": point_summary(point_43434),
        "failed_target_attempt": pilot12.attempt_summary(failed_record),
    }
    return metadata, branch_points, point_43434, failed_sol, failed_record


def generate_branch_cache(
    cache_npz: Path = DEFAULT_CACHE_NPZ,
    cache_json: Path = DEFAULT_CACHE_JSON,
    budget_seconds: float = 1200.0,
) -> tuple[dict[str, Any], dict[str, np.ndarray]]:
    metadata, branch_points, point_43434, failed_sol, failed_record = _collect_branch_bundle(budget_seconds)
    jacobian_grid = build_jacobian_grid(pilot12.PRIMARY_PROFILE.config)
    balance_grid = build_balance_grid(pilot12.PRIMARY_PROFILE.config)

    jacobian_states = []
    balance_states = []
    point_summaries = []
    for q_mpa in CONVERGED_LOADS_MPA:
        point = point_43434 if abs(q_mpa - 4.3434) < 1.0e-12 else branch_points[q_mpa]
        jacobian_states.append(np.asarray(point.solution.sol(jacobian_grid), dtype=float))
        balance_states.append(np.asarray(point.solution.sol(balance_grid), dtype=float))
        point_summaries.append(point_summary(point))

    failed_balance_state = np.asarray(failed_sol.sol(balance_grid), dtype=float)

    np.savez_compressed(
        cache_npz,
        loads_mpa=np.asarray(CONVERGED_LOADS_MPA, dtype=float),
        jacobian_grid=np.asarray(jacobian_grid, dtype=float),
        jacobian_states=np.asarray(jacobian_states, dtype=float),
        balance_grid=np.asarray(balance_grid, dtype=float),
        balance_states=np.asarray(balance_states, dtype=float),
        failed_balance_state=np.asarray(failed_balance_state, dtype=float),
    )

    payload = {
        "metadata": {
            "pilot": "pilot_18_revised_analytic_barrier_diagnosis",
            "source": "active 6-state simple-support branch via pilot-12 bootstrap/retest strategy",
            "converged_loads_mpa": list(CONVERGED_LOADS_MPA),
            "failed_target_load_mpa": FAILED_TARGET_LOAD_MPA,
            "cache_npz": str(cache_npz),
            "budget_seconds": float(budget_seconds),
        },
        "branch_points": point_summaries,
        "failed_target_attempt": pilot12.attempt_summary(failed_record),
        "bootstrap_summary": metadata["bootstrap"],
        "elapsed_seconds": metadata["elapsed_seconds"],
    }
    save_json(cache_json, payload)

    arrays = {
        "loads_mpa": np.asarray(CONVERGED_LOADS_MPA, dtype=float),
        "jacobian_grid": np.asarray(jacobian_grid, dtype=float),
        "jacobian_states": np.asarray(jacobian_states, dtype=float),
        "balance_grid": np.asarray(balance_grid, dtype=float),
        "balance_states": np.asarray(balance_states, dtype=float),
        "failed_balance_state": np.asarray(failed_balance_state, dtype=float),
    }
    return payload, arrays


def load_branch_cache(
    cache_npz: Path = DEFAULT_CACHE_NPZ,
    cache_json: Path = DEFAULT_CACHE_JSON,
) -> tuple[dict[str, Any], dict[str, np.ndarray]]:
    payload = json.loads(cache_json.read_text(encoding="utf-8"))
    cache = np.load(cache_npz)
    arrays = {key: np.asarray(cache[key]) for key in cache.files}
    return payload, arrays


def ensure_branch_cache(
    cache_npz: Path = DEFAULT_CACHE_NPZ,
    cache_json: Path = DEFAULT_CACHE_JSON,
    budget_seconds: float = 1200.0,
    rebuild: bool = False,
) -> tuple[dict[str, Any], dict[str, np.ndarray]]:
    if not rebuild and cache_npz.exists() and cache_json.exists():
        return load_branch_cache(cache_npz=cache_npz, cache_json=cache_json)
    return generate_branch_cache(cache_npz=cache_npz, cache_json=cache_json, budget_seconds=budget_seconds)
