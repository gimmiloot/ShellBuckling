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
DEFAULT_CHECKPOINT_POLICY = "rolling+milestones"
DEFAULT_MAX_ROLLING_CHECKPOINTS = 24
DEFAULT_CHECKPOINT_EVERY_N_ACCEPTED_STEPS = 5
DEFAULT_KEEP_MILESTONE_CHECKPOINTS = True
DEFAULT_KEEP_FAILURE_CHECKPOINTS = True
DEFAULT_KEEP_BOOTSTRAP_CHECKPOINTS = True
DEFAULT_PRUNE_OLD_CHECKPOINTS = True
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


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "no", "n", "off"}:
        return False
    raise ValueError(f"Could not interpret boolean value: {value!r}")


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


def checkpoint_dir(run_dir: Path) -> Path:
    return run_dir / "checkpoints"


def checkpoint_policy_summary(
    *,
    checkpoint_policy: str,
    max_rolling_checkpoints: int,
    checkpoint_every_n_accepted_steps: int,
    keep_milestone_checkpoints: bool,
    keep_failure_checkpoints: bool,
    keep_bootstrap_checkpoints: bool,
    prune_old_checkpoints: bool,
) -> dict[str, Any]:
    return {
        "mode": str(checkpoint_policy),
        "max_rolling_checkpoints": max(0, int(max_rolling_checkpoints)),
        "checkpoint_every_n_accepted_steps": max(1, int(checkpoint_every_n_accepted_steps)),
        "keep_milestone_checkpoints": bool(keep_milestone_checkpoints),
        "keep_failure_checkpoints": bool(keep_failure_checkpoints),
        "keep_bootstrap_checkpoints": bool(keep_bootstrap_checkpoints),
        "prune_old_checkpoints": bool(prune_old_checkpoints),
        "default_recommended_mode": DEFAULT_CHECKPOINT_POLICY,
        "minimum_resume_anchors_always_retained": True,
    }


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


def checkpoint_exists(run_dir: Path, relative_path: str | Path | None) -> bool:
    if relative_path in (None, ""):
        return False
    return (run_dir / Path(relative_path)).exists()


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


def count_checkpoint_files(run_dir: Path) -> int:
    base = checkpoint_dir(run_dir)
    if not base.exists():
        return 0
    return sum(1 for path in base.rglob("*.npz") if path.is_file())


def milestone_marker_loads(progress: dict[str, Any]) -> set[float]:
    metadata = progress.get("metadata") or {}
    markers = {
        round(float(STATUS_CONVENTION["pilot20_bounded_ceiling_mpa"]), 4),
        round(float(STATUS_CONVENTION["pilot21_bounded_ceiling_mpa"]), 4),
        4.4000,
    }
    for key in ("target_load_mpa", "bootstrap_target_mpa"):
        value = float_or_none(metadata.get(key))
        if value is not None:
            markers.add(round(float(value), 4))
    return markers


def is_round_milestone(q_mpa: float, step_mpa: float = 0.5, tol: float = 1.0e-9) -> bool:
    scaled = float(q_mpa) / float(step_mpa)
    return abs(scaled - round(scaled)) <= tol


def is_milestone_step(progress: dict[str, Any], step_entry: dict[str, Any]) -> bool:
    q_value = float_or_none(step_entry.get("q_mpa"))
    if q_value is None:
        return False
    if is_round_milestone(q_value):
        return True
    return any(abs(q_value - marker) <= 1.0e-6 for marker in milestone_marker_loads(progress))


def checkpoint_policy_config(progress: dict[str, Any]) -> dict[str, Any]:
    metadata = progress.get("metadata") or {}
    policy = dict(metadata.get("checkpoint_policy") or {})
    if not policy:
        policy = checkpoint_policy_summary(
            checkpoint_policy=DEFAULT_CHECKPOINT_POLICY,
            max_rolling_checkpoints=DEFAULT_MAX_ROLLING_CHECKPOINTS,
            checkpoint_every_n_accepted_steps=DEFAULT_CHECKPOINT_EVERY_N_ACCEPTED_STEPS,
            keep_milestone_checkpoints=DEFAULT_KEEP_MILESTONE_CHECKPOINTS,
            keep_failure_checkpoints=DEFAULT_KEEP_FAILURE_CHECKPOINTS,
            keep_bootstrap_checkpoints=DEFAULT_KEEP_BOOTSTRAP_CHECKPOINTS,
            prune_old_checkpoints=DEFAULT_PRUNE_OLD_CHECKPOINTS,
        )
    policy["mode"] = str(policy.get("mode", DEFAULT_CHECKPOINT_POLICY))
    policy["max_rolling_checkpoints"] = max(0, int(policy.get("max_rolling_checkpoints", DEFAULT_MAX_ROLLING_CHECKPOINTS)))
    policy["checkpoint_every_n_accepted_steps"] = max(1, int(policy.get("checkpoint_every_n_accepted_steps", DEFAULT_CHECKPOINT_EVERY_N_ACCEPTED_STEPS)))
    policy["keep_milestone_checkpoints"] = bool(policy.get("keep_milestone_checkpoints", DEFAULT_KEEP_MILESTONE_CHECKPOINTS))
    policy["keep_failure_checkpoints"] = bool(policy.get("keep_failure_checkpoints", DEFAULT_KEEP_FAILURE_CHECKPOINTS))
    policy["keep_bootstrap_checkpoints"] = bool(policy.get("keep_bootstrap_checkpoints", DEFAULT_KEEP_BOOTSTRAP_CHECKPOINTS))
    policy["prune_old_checkpoints"] = bool(policy.get("prune_old_checkpoints", DEFAULT_PRUNE_OLD_CHECKPOINTS))
    return policy


def ensure_checkpoint_tracking(progress: dict[str, Any]) -> None:
    checkpoints = progress.setdefault("checkpoints", {})
    checkpoints.setdefault("failure_context_step_indices", [])
    checkpoints.setdefault("suspicious_step_indices", [])
    accepted_steps = progress.get("accepted_steps") or []
    run_dir = Path((progress.get("metadata") or {}).get("run_dir", FAST_RUN_DIR))
    for step in accepted_steps:
        step.setdefault("checkpoint_tags", [])
        if "checkpoint_retained" not in step:
            step["checkpoint_retained"] = checkpoint_exists(run_dir, step.get("checkpoint"))


def add_special_step_indices(progress: dict[str, Any], bucket: str, indices: list[int]) -> None:
    checkpoints = progress.setdefault("checkpoints", {})
    items = checkpoints.setdefault(bucket, [])
    accepted_steps = progress.get("accepted_steps") or []
    allowed = set(range(len(accepted_steps)))
    merged = sorted({int(idx) for idx in items if int(idx) in allowed} | {int(idx) for idx in indices if int(idx) in allowed and int(idx) >= 0})
    checkpoints[bucket] = merged


def rolling_candidate_indices(progress: dict[str, Any], every_n: int) -> list[int]:
    accepted_steps = progress.get("accepted_steps") or []
    stride = max(1, int(every_n))
    return [idx for idx, _ in enumerate(accepted_steps) if ((idx + 1) % stride) == 0]


def milestone_context_indices(progress: dict[str, Any]) -> set[int]:
    accepted_steps = progress.get("accepted_steps") or []
    keep: set[int] = set()
    for idx, step in enumerate(accepted_steps):
        if not is_milestone_step(progress, step):
            continue
        keep.add(idx)
        if idx >= 1:
            keep.add(idx - 1)
        if idx >= 2:
            keep.add(idx - 2)
    return keep


def active_resume_indices(progress: dict[str, Any]) -> set[int]:
    accepted_steps = progress.get("accepted_steps") or []
    keep: set[int] = set()
    if accepted_steps:
        keep.add(len(accepted_steps) - 1)
    if len(accepted_steps) >= 2:
        keep.add(len(accepted_steps) - 2)
    return keep


def named_checkpoint_paths(progress: dict[str, Any]) -> set[str]:
    checkpoints = progress.get("checkpoints") or {}
    keep: set[str] = set()
    for key in ("scaled_anchor_checkpoint", "bootstrap_previous_checkpoint"):
        path = checkpoints.get(key)
        if path:
            keep.add(str(path))
    return keep


def checkpoint_retention_targets(progress: dict[str, Any]) -> tuple[set[int], set[str]]:
    ensure_checkpoint_tracking(progress)
    policy = checkpoint_policy_config(progress)
    accepted_steps = progress.get("accepted_steps") or []
    keep_step_indices = active_resume_indices(progress)
    mode = str(policy["mode"])

    if mode == "all":
        keep_step_indices.update(range(len(accepted_steps)))
    else:
        if "rolling" in mode and int(policy["max_rolling_checkpoints"]) > 0:
            eligible = rolling_candidate_indices(progress, int(policy["checkpoint_every_n_accepted_steps"]))
            keep_step_indices.update(eligible[-int(policy["max_rolling_checkpoints"]):])
        if "milestones" in mode and bool(policy["keep_milestone_checkpoints"]):
            keep_step_indices.update(milestone_context_indices(progress))

    checkpoints = progress.get("checkpoints") or {}
    if bool(policy["keep_failure_checkpoints"]):
        keep_step_indices.update(int(idx) for idx in checkpoints.get("failure_context_step_indices") or [])
        keep_step_indices.update(int(idx) for idx in checkpoints.get("suspicious_step_indices") or [])

    return keep_step_indices, named_checkpoint_paths(progress)


def apply_checkpoint_policy(progress: dict[str, Any], run_dir: Path) -> dict[str, int]:
    ensure_checkpoint_tracking(progress)
    policy = checkpoint_policy_config(progress)
    accepted_steps = progress.get("accepted_steps") or []
    keep_step_indices, keep_named = checkpoint_retention_targets(progress)
    active_indices = active_resume_indices(progress)
    milestone_indices = milestone_context_indices(progress)
    rolling_indices: set[int] = set()
    if "rolling" in str(policy["mode"]) and int(policy["max_rolling_checkpoints"]) > 0:
        rolling_indices = set(
            rolling_candidate_indices(progress, int(policy["checkpoint_every_n_accepted_steps"]))[-int(policy["max_rolling_checkpoints"]):]
        )
    failure_indices = set(int(idx) for idx in (progress.get("checkpoints") or {}).get("failure_context_step_indices") or [])
    suspicious_indices = set(int(idx) for idx in (progress.get("checkpoints") or {}).get("suspicious_step_indices") or [])

    deleted = 0
    for idx, step in enumerate(accepted_steps):
        relpath = step.get("checkpoint")
        tags: list[str] = []
        if idx in active_indices:
            tags.append("active")
        if idx in milestone_indices:
            tags.append("milestone")
        if idx in rolling_indices:
            tags.append("rolling")
        if idx in failure_indices:
            tags.append("failure_context")
        if idx in suspicious_indices:
            tags.append("suspicious")
        step["checkpoint_tags"] = tags

        if not relpath:
            step["checkpoint_retained"] = False
            continue

        full_path = run_dir / Path(relpath)
        should_keep = (str(policy["mode"]) == "all") or (idx in keep_step_indices)
        if should_keep:
            step["checkpoint_retained"] = full_path.exists()
            continue

        if bool(policy["prune_old_checkpoints"]):
            if full_path.exists():
                full_path.unlink()
                deleted += 1
            step["checkpoint_retained"] = False
        else:
            step["checkpoint_retained"] = full_path.exists()

    referenced = {str(step.get("checkpoint")) for idx, step in enumerate(accepted_steps) if idx in keep_step_indices and step.get("checkpoint")}
    referenced.update(keep_named)
    if bool(policy["prune_old_checkpoints"]):
        base = checkpoint_dir(run_dir)
        if base.exists():
            for file_path in base.rglob("*.npz"):
                relpath = str(file_path.relative_to(run_dir)).replace("\\", "/")
                if relpath not in referenced:
                    file_path.unlink()
                    deleted += 1

    return {
        "retained_step_checkpoints": sum(1 for step in accepted_steps if bool(step.get("checkpoint_retained"))),
        "named_checkpoint_count": sum(1 for relpath in keep_named if checkpoint_exists(run_dir, relpath)),
        "checkpoint_file_count": count_checkpoint_files(run_dir),
        "deleted_checkpoint_count": int(deleted),
    }


def ensure_step_checkpoint_available(run_dir: Path, step_entry: dict[str, Any]) -> None:
    relpath = step_entry.get("checkpoint")
    if not relpath:
        raise RuntimeError("Accepted step has no stored checkpoint path.")
    if checkpoint_exists(run_dir, relpath):
        return
    q_value = float_or_none(step_entry.get("q_mpa"))
    raise RuntimeError(
        f"Checkpoint for q={q_value:.4f} MPa is not currently retained in this run directory. "
        "Rerun the fast runner with a more archival checkpoint policy or keep that load as a milestone."
    )


def refresh_progress_summary(progress: dict[str, Any]) -> None:
    ensure_checkpoint_tracking(progress)
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
    run_dir = Path((progress.get("metadata") or {}).get("run_dir", FAST_RUN_DIR))
    progress["summary"] = {
        "highest_converged_q_mpa": highest_q,
        "terminal_failure_q_mpa": float_or_none((progress.get("state") or {}).get("terminal_failure_q_mpa")),
        "accepted_step_count": len(accepted_steps),
        "retained_step_checkpoint_count": sum(1 for step in accepted_steps if bool(step.get("checkpoint_retained"))),
        "named_checkpoint_count": sum(1 for relpath in named_checkpoint_paths(progress) if checkpoint_exists(run_dir, relpath)),
        "checkpoint_file_count": count_checkpoint_files(run_dir),
        "failure_event_count": len(progress.get("failure_events") or []),
        "suggested_confirm_loads_mpa": suggested,
        "checkpoint_policy": checkpoint_policy_config(progress),
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
