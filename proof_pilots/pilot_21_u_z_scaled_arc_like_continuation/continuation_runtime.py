from __future__ import annotations

import importlib.util
import json
import math
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np
from scipy.interpolate import PchipInterpolator

THIS_FILE = Path(__file__).resolve()
PILOT_DIR = THIS_FILE.parent
REPO_ROOT = THIS_FILE.parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from shell_buckling.mixed_weak.axisymmetric_simple_support_background import AxisymmetricSimpleSupportConfig


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module {module_name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


pilot10 = load_module(
    "pilot21_runtime_pilot10_campaign",
    REPO_ROOT / "proof_pilots" / "pilot_10_high_load_simple_support_continuation" / "continuation_campaign.py",
)
pilot12 = load_module(
    "pilot21_runtime_pilot12_extension",
    REPO_ROOT / "proof_pilots" / "pilot_12_high_load_branch_extension" / "numerical_extension.py",
)
pilot20 = load_module(
    "pilot21_runtime_pilot20_method_sweep",
    REPO_ROOT / "proof_pilots" / "pilot_20_method_sweep_for_simple_support_ceiling" / "method_sweep.py",
)
pilot21 = load_module(
    "pilot21_runtime_pilot21_script",
    PILOT_DIR / "u_z_scaled_arc_like_continuation.py",
)

FAST_RUN_DIR = PILOT_DIR / "fast_run"
DEFAULT_PROGRESS_JSON = FAST_RUN_DIR / "fast_progress.json"
DEFAULT_PROGRESS_LOG = FAST_RUN_DIR / "progress_log.jsonl"
DEFAULT_CONFIRM_JSON = FAST_RUN_DIR / "confirm_results.json"
DEFAULT_BOOTSTRAP_TARGET_MPA = float(pilot21.EXTENSION_STAGE_TARGETS_MPA[-1])
STATUS_CONVENTION = {
    "old_path_anchor_mpa": float(pilot21.OLD_PATH_ANCHOR_MPA),
    "old_path_first_failure_mpa": float(pilot21.OLD_PATH_FAILURE_MPA),
    "pilot20_bounded_ceiling_mpa": float(pilot21.PILOT20_BEST_BOUNDED_CEILING_MPA),
    "pilot21_bounded_ceiling_mpa": float(pilot21.EXTENSION_STAGE_TARGETS_MPA[-1]),
    "preferred_workflow": "u_z-scaled continuation + auxiliary arc-like step adaptation",
    "barrier_reading": "still numerical / conditioning-related, not a proven physical end of branch",
}


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


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(serializable(payload), ensure_ascii=False) + "\n")


def float_or_none(value: Any) -> float | None:
    if value is None:
        return None
    try:
        converted = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(converted) or math.isinf(converted):
        return None
    return converted


def float_or_nan(value: Any) -> float:
    converted = float_or_none(value)
    return float("nan") if converted is None else float(converted)


def sanitize_load(q_mpa: float) -> str:
    return f"{float(q_mpa):.4f}".replace("-", "m").replace(".", "p")


def make_checkpoint_relpath(step_index: int, q_mpa: float) -> Path:
    return Path("checkpoints") / f"point_{step_index:05d}_q_{sanitize_load(q_mpa)}_mpa.npz"


class StoredSolutionProxy:
    def __init__(self, x: np.ndarray, y: np.ndarray, message: str = "checkpoint"):
        self.x = np.asarray(x, dtype=float)
        self.y = np.asarray(y, dtype=float)
        self.success = True
        self.message = str(message)
        self.rms_residuals = None
        self._interpolators = [
            PchipInterpolator(self.x, self.y[idx], extrapolate=True)
            for idx in range(self.y.shape[0])
        ]

    def sol(self, x_query: np.ndarray) -> np.ndarray:
        x_arr = np.asarray(x_query, dtype=float)
        values = np.vstack([interp(x_arr) for interp in self._interpolators])
        if x_arr.ndim == 0:
            return values[:, 0]
        return values


def build_branch_point_from_checkpoint(summary: dict[str, Any], x: np.ndarray, y: np.ndarray):
    message = str(summary.get("message", "checkpoint"))
    return pilot10.BranchPoint(
        q_mpa=float(summary.get("q_mpa")),
        x=np.asarray(x, dtype=float),
        y=np.asarray(y, dtype=float),
        solution=StoredSolutionProxy(x, y, message=message),
        message=message,
        nodes=int(summary.get("nodes", len(x))),
        max_rms=float_or_nan(summary.get("max_rms")),
        max_bc_residual=float_or_nan(summary.get("max_bc_residual")),
        min_r=float_or_nan(summary.get("min_r")),
        node_pressure=float_or_nan(summary.get("node_pressure")),
        right_edge_fraction_0_99=float_or_nan(summary.get("right_edge_fraction_0_99")),
        right_edge_fraction_0_995=float_or_nan(summary.get("right_edge_fraction_0_995")),
        right_edge_fraction_0_999=float_or_nan(summary.get("right_edge_fraction_0_999")),
        min_dx=float_or_nan(summary.get("min_dx")),
        min_dx_mid=float_or_nan(summary.get("min_dx_mid")),
        top_gradients=list(summary.get("top_gradients") or []),
        observables=dict(summary.get("observables") or {}),
        accepted_profile=str(summary.get("accepted_profile", "checkpoint")),
        accepted_seed=str(summary.get("accepted_seed", "checkpoint")),
        predictor_rel_correction=float_or_none(summary.get("predictor_rel_correction")),
        predictor_abs_correction=float_or_none(summary.get("predictor_abs_correction")),
    )


def save_point_checkpoint(run_dir: Path, step_index: int, point) -> Path:
    relative_path = make_checkpoint_relpath(step_index, float(point.q_mpa))
    full_path = run_dir / relative_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        full_path,
        x=np.asarray(point.x, dtype=float),
        y=np.asarray(point.y, dtype=float),
        summary_json=json.dumps(serializable(pilot21.point_summary(point))),
    )
    return relative_path


def save_named_point_checkpoint(run_dir: Path, filename: str, point) -> Path:
    relative_path = Path("checkpoints") / filename
    full_path = run_dir / relative_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        full_path,
        x=np.asarray(point.x, dtype=float),
        y=np.asarray(point.y, dtype=float),
        summary_json=json.dumps(serializable(pilot21.point_summary(point))),
    )
    return relative_path


def load_point_checkpoint(run_dir: Path, relative_path: str | Path):
    full_path = run_dir / Path(relative_path)
    with np.load(full_path, allow_pickle=False) as data:
        x = np.asarray(data["x"], dtype=float)
        y = np.asarray(data["y"], dtype=float)
        summary = json.loads(str(data["summary_json"].tolist()))
    return build_branch_point_from_checkpoint(summary, x, y)


def compact_attempt_summary(attempt_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "q_mpa": float_or_none(attempt_payload.get("q_mpa")),
        "seed_label": attempt_payload.get("seed_label"),
        "success": bool(attempt_payload.get("success")),
        "nodes": attempt_payload.get("nodes"),
        "message": attempt_payload.get("message"),
        "max_bc_residual": float_or_none(attempt_payload.get("max_bc_residual")),
        "node_pressure": float_or_none(attempt_payload.get("node_pressure")),
        "right_edge_fraction_0_995": float_or_none(attempt_payload.get("right_edge_fraction_0_995")),
        "predictor_rel_correction": float_or_none(attempt_payload.get("predictor_rel_correction")),
        "mesh_pressure_only": bool(attempt_payload.get("mesh_pressure_only", False)),
        "branch_turning_suspicion": bool(attempt_payload.get("branch_turning_suspicion", False)),
    }


def compact_point_summary(point_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "q_mpa": float_or_none(point_payload.get("q_mpa")),
        "nodes": point_payload.get("nodes"),
        "max_bc_residual": float_or_none(point_payload.get("max_bc_residual")),
        "node_pressure": float_or_none(point_payload.get("node_pressure")),
        "right_edge_fraction_0_995": float_or_none(point_payload.get("right_edge_fraction_0_995")),
        "top_gradients": point_payload.get("top_gradients"),
        "accepted_profile": point_payload.get("accepted_profile"),
        "accepted_seed": point_payload.get("accepted_seed"),
        "message": point_payload.get("message"),
    }


def profile_summary(profile) -> dict[str, Any]:
    return {
        "name": profile.name,
        "description": profile.description,
        "config": asdict(profile.config),
    }


def profile_from_metadata(profile_payload: dict[str, Any]):
    return pilot10.SolverProfile(
        name=str(profile_payload["name"]),
        description=str(profile_payload["description"]),
        config=AxisymmetricSimpleSupportConfig(**dict(profile_payload["config"])),
    )


def current_highest_q(progress: dict[str, Any]) -> float | None:
    accepted_steps = progress.get("accepted_steps") or []
    if not accepted_steps:
        return None
    return float_or_none(accepted_steps[-1].get("q_mpa"))


def refresh_progress_summary(progress: dict[str, Any]) -> None:
    highest_q = current_highest_q(progress)
    accepted_steps = progress.get("accepted_steps") or []
    suggested: list[float] = []
    for marker in (
        STATUS_CONVENTION["pilot20_bounded_ceiling_mpa"],
        STATUS_CONVENTION["pilot21_bounded_ceiling_mpa"],
        highest_q,
    ):
        if marker is None:
            continue
        if any(abs(float(step.get("q_mpa")) - float(marker)) < 1.0e-9 for step in accepted_steps):
            if not any(abs(existing - float(marker)) < 1.0e-9 for existing in suggested):
                suggested.append(float(marker))
    progress["summary"] = {
        "highest_converged_q_mpa": highest_q,
        "terminal_failure_q_mpa": float_or_none((progress.get("state") or {}).get("terminal_failure_q_mpa")),
        "accepted_step_count": len(accepted_steps),
        "failure_event_count": len(progress.get("failure_events") or []),
        "suggested_confirm_loads_mpa": suggested,
        "status_convention": STATUS_CONVENTION,
    }


def find_step_index(progress: dict[str, Any], q_target_mpa: float, tol: float = 1.0e-6) -> int:
    accepted_steps = progress.get("accepted_steps") or []
    for idx, step in enumerate(accepted_steps):
        q_value = float(step.get("q_mpa"))
        if abs(q_value - float(q_target_mpa)) <= tol:
            return idx
    raise KeyError(f"No accepted step stored at q={q_target_mpa:.6f} MPa.")


def load_resume_points(progress: dict[str, Any], run_dir: Path):
    state = progress.get("state") or {}
    checkpoints = progress.get("checkpoints") or {}
    scaled_anchor = load_point_checkpoint(run_dir, checkpoints["scaled_anchor_checkpoint"])
    older_point = load_point_checkpoint(run_dir, state["resume_older_checkpoint"])
    previous_point = load_point_checkpoint(run_dir, state["resume_previous_checkpoint"])
    return scaled_anchor, older_point, previous_point
