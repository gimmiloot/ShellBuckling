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
DEFAULT_MILESTONE_GRID_MPA = 0.5
DEFAULT_SUCCESS_GROWTH = float(pilot21.SUCCESS_GROWTH)
DEFAULT_CONDITIONING_SHRINK = 0.75
DEFAULT_SMOOTH_NODE_PRESSURE_MAX = 0.02
DEFAULT_SMOOTH_RIGHT_EDGE_FRACTION_MAX = 0.25
DEFAULT_CROWDED_NODE_PRESSURE_MIN = 0.10
DEFAULT_CROWDED_RIGHT_EDGE_FRACTION_MIN = 0.40
STRICT_REPRO_MAX_REL_L2 = 1.0e-7
STRICT_REPRO_MAX_REL_MAX = 1.0e-6
NEAR_REPRO_MAX_REL_L2 = 2.0e-5
NEAR_REPRO_MAX_REL_MAX = 2.0e-4
BC_RESIDUAL_SANITY_MAX = 1.0e-6
EXPECTED_GRADIENT_ORDER = ("u_z", "varphi", "T_s")
DEFAULT_FAILURE_PROBE_STEP_FACTOR = 1.0
DEFAULT_FAILURE_PROBE_MIN_STEP_MPA = 0.002
DEFAULT_FAILURE_PROBE_HIGH_LOAD_STEP_MPA = 0.004
DEFAULT_FAILURE_PROBE_HIGH_LOAD_THRESHOLD_MPA = 5.0
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


def unique_sorted_loads(values: Any) -> list[float]:
    if values in (None, ""):
        return []
    ordered: list[float] = []
    for item in values:
        value = float_or_none(item)
        if value is None:
            continue
        rounded = round(float(value), 4)
        if not any(abs(rounded - existing) <= 1.0e-9 for existing in ordered):
            ordered.append(rounded)
    ordered.sort()
    return ordered


def checkpoint_policy_summary(
    *,
    checkpoint_policy: str,
    max_rolling_checkpoints: int,
    checkpoint_every_n_accepted_steps: int,
    keep_milestone_checkpoints: bool,
    keep_failure_checkpoints: bool,
    keep_bootstrap_checkpoints: bool,
    prune_old_checkpoints: bool,
    milestone_grid_mpa: float = DEFAULT_MILESTONE_GRID_MPA,
    explicit_milestone_loads_mpa: list[float] | tuple[float, ...] | None = None,
) -> dict[str, Any]:
    grid = float_or_none(milestone_grid_mpa)
    return {
        "mode": str(checkpoint_policy),
        "max_rolling_checkpoints": max(0, int(max_rolling_checkpoints)),
        "checkpoint_every_n_accepted_steps": max(1, int(checkpoint_every_n_accepted_steps)),
        "keep_milestone_checkpoints": bool(keep_milestone_checkpoints),
        "keep_failure_checkpoints": bool(keep_failure_checkpoints),
        "keep_bootstrap_checkpoints": bool(keep_bootstrap_checkpoints),
        "prune_old_checkpoints": bool(prune_old_checkpoints),
        "milestone_grid_mpa": None if grid is None else float(grid),
        "explicit_milestone_loads_mpa": unique_sorted_loads(explicit_milestone_loads_mpa),
        "default_recommended_mode": DEFAULT_CHECKPOINT_POLICY,
        "canonical_milestones_mpa": [
            round(float(STATUS_CONVENTION["pilot20_bounded_ceiling_mpa"]), 4),
            round(float(STATUS_CONVENTION["pilot21_bounded_ceiling_mpa"]), 4),
            4.4000,
        ],
        "minimum_resume_anchors_always_retained": True,
    }


def step_control_summary(
    *,
    initial_step_mpa: float,
    min_step_mpa: float,
    max_step_mpa: float,
    success_growth: float,
    conditioning_shrink: float,
    failure_shrink: float,
    smooth_node_pressure_max: float = DEFAULT_SMOOTH_NODE_PRESSURE_MAX,
    smooth_right_edge_fraction_max: float = DEFAULT_SMOOTH_RIGHT_EDGE_FRACTION_MAX,
    crowded_node_pressure_min: float = DEFAULT_CROWDED_NODE_PRESSURE_MIN,
    crowded_right_edge_fraction_min: float = DEFAULT_CROWDED_RIGHT_EDGE_FRACTION_MIN,
) -> dict[str, Any]:
    return {
        "initial_step_mpa": float(initial_step_mpa),
        "min_step_mpa": float(min_step_mpa),
        "max_step_mpa": float(max_step_mpa),
        "success_growth": float(success_growth),
        "conditioning_shrink": float(conditioning_shrink),
        "failure_shrink": float(failure_shrink),
        "smooth_node_pressure_max": float(smooth_node_pressure_max),
        "smooth_right_edge_fraction_max": float(smooth_right_edge_fraction_max),
        "crowded_node_pressure_min": float(crowded_node_pressure_min),
        "crowded_right_edge_fraction_min": float(crowded_right_edge_fraction_min),
        "historical_bounded_pilot21_cap_mpa": float(pilot21.MAX_STEP_MPA),
        "adapt_rule": (
            "runtime-controlled fast-step policy: grow on smooth accepted steps, "
            "shrink on crowded accepted steps, and use failure_shrink after failed solves"
        ),
        "historical_reference": "pilot21.adapt_step_size remains only in the bounded historical pilot artifact",
    }


def step_control_config(progress: dict[str, Any]) -> dict[str, Any]:
    metadata = progress.get("metadata") or {}
    step_control = dict(metadata.get("step_control") or {})
    if not step_control:
        step_control = step_control_summary(
            initial_step_mpa=pilot21.INITIAL_STEP_MPA,
            min_step_mpa=pilot21.MIN_STEP_MPA,
            max_step_mpa=pilot21.MAX_STEP_MPA,
            success_growth=DEFAULT_SUCCESS_GROWTH,
            conditioning_shrink=DEFAULT_CONDITIONING_SHRINK,
            failure_shrink=pilot21.FAILURE_SHRINK,
        )
    step_control["initial_step_mpa"] = float(step_control.get("initial_step_mpa", pilot21.INITIAL_STEP_MPA))
    step_control["min_step_mpa"] = float(step_control.get("min_step_mpa", pilot21.MIN_STEP_MPA))
    step_control["max_step_mpa"] = float(step_control.get("max_step_mpa", pilot21.MAX_STEP_MPA))
    step_control["success_growth"] = float(step_control.get("success_growth", DEFAULT_SUCCESS_GROWTH))
    step_control["conditioning_shrink"] = float(step_control.get("conditioning_shrink", DEFAULT_CONDITIONING_SHRINK))
    step_control["failure_shrink"] = float(step_control.get("failure_shrink", pilot21.FAILURE_SHRINK))
    step_control["smooth_node_pressure_max"] = float(step_control.get("smooth_node_pressure_max", DEFAULT_SMOOTH_NODE_PRESSURE_MAX))
    step_control["smooth_right_edge_fraction_max"] = float(step_control.get("smooth_right_edge_fraction_max", DEFAULT_SMOOTH_RIGHT_EDGE_FRACTION_MAX))
    step_control["crowded_node_pressure_min"] = float(step_control.get("crowded_node_pressure_min", DEFAULT_CROWDED_NODE_PRESSURE_MIN))
    step_control["crowded_right_edge_fraction_min"] = float(step_control.get("crowded_right_edge_fraction_min", DEFAULT_CROWDED_RIGHT_EDGE_FRACTION_MIN))
    return step_control


def adapt_fast_step_size(current_step_mpa: float, point, step_control: dict[str, Any]) -> float:
    config = step_control_config({"metadata": {"step_control": step_control}})
    current_step = min(config["max_step_mpa"], max(config["min_step_mpa"], float(current_step_mpa)))
    node_pressure = float(getattr(point, "node_pressure", float("nan")))
    right_edge_fraction = float(getattr(point, "right_edge_fraction_0_995", float("nan")))

    if (
        node_pressure < config["smooth_node_pressure_max"]
        and right_edge_fraction < config["smooth_right_edge_fraction_max"]
    ):
        proposed = current_step * config["success_growth"]
    elif (
        node_pressure > config["crowded_node_pressure_min"]
        or right_edge_fraction > config["crowded_right_edge_fraction_min"]
    ):
        proposed = current_step * config["conditioning_shrink"]
    else:
        proposed = current_step

    return min(config["max_step_mpa"], max(config["min_step_mpa"], float(proposed)))


def audit_policy_summary() -> dict[str, Any]:
    return {
        "same_branch_indicators": {
            "same_accepted_seed": "repeat solve keeps the same accepted seed family",
            "branch_jump_suspicion": "continuity check remains free of branch-jump warnings",
            "repeat_drift_smoothness": "repeat drift changes gradually across checked milestones",
            "repeat_vs_adjacent_step_ratio": "repeat drift stays smaller than an ordinary adjacent continuation step",
            "strongest_gradient_order_consistency": list(EXPECTED_GRADIENT_ORDER),
            "bc_residual_sanity_max": BC_RESIDUAL_SANITY_MAX,
        },
        "promotion_policy": {
            "strict_reproducible": {
                "definition": "same-load repeat solve closes under the inherited pilot-12 gate",
                "max_rel_l2": STRICT_REPRO_MAX_REL_L2,
                "max_rel_max": STRICT_REPRO_MAX_REL_MAX,
            },
            "near_reproducible": {
                "definition": "same-load repeat solve closes under the relaxed fast-workflow gate and keeps the same accepted seed",
                "requires_same_accepted_seed": True,
                "max_rel_l2": NEAR_REPRO_MAX_REL_L2,
                "max_rel_max": NEAR_REPRO_MAX_REL_MAX,
            },
            "stronger_milestone": "same-branch indicators stay strong, near_reproducible remains true, and a short confirm probe is recorded",
            "audited_ceiling": "promotion above the current audited ceiling requires explicit milestone audit closure, including strict_reproducible",
            "operational_continuation_evidence": "accepted fast-run continuation result without milestone-promotion closure",
            "open_policy_issue": "the inherited strict thresholds may be too rigid for the newer fast continuation workflow; this is tracked explicitly as an audit-policy issue rather than treated as silent branch loss",
        },
    }


def strict_reproducible(repeat_assessment: dict[str, Any] | None) -> bool:
    return bool((repeat_assessment or {}).get("reproducible"))


def near_reproducible(repeat_assessment: dict[str, Any] | None) -> bool:
    delta = (repeat_assessment or {}).get("solution_delta") or {}
    max_rel_l2 = float_or_none(delta.get("max_rel_l2"))
    max_rel_max = float_or_none(delta.get("max_rel_max"))
    return (
        bool((repeat_assessment or {}).get("same_accepted_seed"))
        and max_rel_l2 is not None
        and max_rel_max is not None
        and max_rel_l2 <= NEAR_REPRO_MAX_REL_L2
        and max_rel_max <= NEAR_REPRO_MAX_REL_MAX
    )


def bc_residual_sane(max_bc_residual: Any) -> bool:
    residual = float_or_none(max_bc_residual)
    return residual is not None and residual <= BC_RESIDUAL_SANITY_MAX


def gradient_order_consistent(order: list[str] | tuple[str, ...] | None) -> bool:
    values = list(order or [])
    expected = list(EXPECTED_GRADIENT_ORDER)
    return values[: len(expected)] == expected


def repeat_vs_adjacent_step_ratio(repeat_assessment: dict[str, Any] | None, continuity: dict[str, Any] | None) -> float | None:
    repeat_delta = (repeat_assessment or {}).get("solution_delta") or {}
    continuity_metrics = (continuity or {}).get("step_state_metrics") or {}
    repeat_l2 = float_or_none(repeat_delta.get("max_rel_l2"))
    adjacent_l2 = float_or_none(continuity_metrics.get("max_rel_l2"))
    if repeat_l2 is None or adjacent_l2 is None or repeat_l2 <= 0.0:
        return None
    return float(adjacent_l2 / repeat_l2)


def choose_failure_probe_step(
    *,
    load_mpa: float,
    accepted_step_mpa: float | None,
    explicit_step_mpa: float | None,
    step_factor: float,
    min_step_mpa: float,
    high_load_step_mpa: float,
    high_load_threshold_mpa: float,
) -> float:
    if explicit_step_mpa is not None:
        return float(explicit_step_mpa)
    accepted = 0.0 if accepted_step_mpa is None else float(accepted_step_mpa)
    base = max(float(min_step_mpa), accepted * float(step_factor))
    if float(load_mpa) >= float(high_load_threshold_mpa):
        base = max(base, float(high_load_step_mpa))
    return float(base)


def annotate_repeat_drift_smoothness(results: list[dict[str, Any]]) -> None:
    previous_l2 = None
    for item in sorted(results, key=lambda entry: float(entry.get("q_mpa", 0.0))):
        repeat_delta = ((item.get("reproducibility") or {}).get("solution_delta") or {})
        current_l2 = float_or_none(repeat_delta.get("max_rel_l2"))
        if current_l2 is None or previous_l2 is None or previous_l2 <= 0.0:
            item["repeat_drift_smooth"] = True
            item["repeat_drift_smoothness"] = "baseline"
        else:
            ratio = current_l2 / previous_l2
            smooth = 0.5 <= ratio <= 2.0
            item["repeat_drift_smooth"] = bool(smooth)
            item["repeat_drift_smoothness"] = "smooth_change" if smooth else "abrupt_change"
        if current_l2 is not None:
            previous_l2 = current_l2


def same_branch_indicators(
    *,
    accepted_point_summary: dict[str, Any],
    repeat_assessment: dict[str, Any] | None,
    continuity: dict[str, Any] | None,
    strongest_gradient_order: list[str],
    repeat_drift_smooth: bool | None,
    repeat_drift_smoothness: str | None,
) -> dict[str, Any]:
    ratio = repeat_vs_adjacent_step_ratio(repeat_assessment, continuity)
    branch_jump = False if continuity is None else bool(continuity.get("branch_jump_suspicion"))
    same_seed = bool((repeat_assessment or {}).get("same_accepted_seed"))
    residual = accepted_point_summary.get("max_bc_residual")
    return {
        "same_accepted_seed": same_seed,
        "branch_jump_suspicion": branch_jump,
        "branch_jump_reasons": [] if continuity is None else list(continuity.get("branch_jump_reasons") or []),
        "repeat_drift_smooth": repeat_drift_smooth,
        "repeat_drift_smoothness": repeat_drift_smoothness,
        "repeat_vs_adjacent_step_l2_ratio": ratio,
        "repeat_smaller_than_adjacent_step": None if ratio is None else bool(ratio > 1.0),
        "strongest_gradient_order": strongest_gradient_order,
        "strongest_gradient_order_consistent": gradient_order_consistent(strongest_gradient_order),
        "bc_residual": float_or_none(residual),
        "bc_residual_sane": bc_residual_sane(residual),
        "overall_same_branch_signal": bool(
            same_seed
            and not branch_jump
            and bc_residual_sane(residual)
            and gradient_order_consistent(strongest_gradient_order)
            and (ratio is None or ratio > 1.0)
            and (repeat_drift_smooth is None or bool(repeat_drift_smooth))
        ),
    }


def promotion_policy_assessment(
    *,
    strict_reproducible_flag: bool,
    near_reproducible_flag: bool,
    same_branch: dict[str, Any],
    failure_probe: list[dict[str, Any]],
) -> dict[str, Any]:
    probe_without_failure = bool(failure_probe) and all(bool(item.get("success")) for item in failure_probe)
    stronger_milestone = bool(
        near_reproducible_flag
        and same_branch.get("overall_same_branch_signal")
        and probe_without_failure
    )
    eligible_for_audited_promotion = bool(stronger_milestone and strict_reproducible_flag)
    if eligible_for_audited_promotion:
        classification = "eligible_for_audited_promotion"
    elif stronger_milestone:
        classification = "stronger_milestone"
    elif same_branch.get("overall_same_branch_signal"):
        classification = "operational_continuation_evidence"
    else:
        classification = "ambiguous_follow_up_required"
    return {
        "strict_reproducible": bool(strict_reproducible_flag),
        "near_reproducible": bool(near_reproducible_flag),
        "stronger_milestone": stronger_milestone,
        "eligible_for_audited_promotion": eligible_for_audited_promotion,
        "operational_continuation_evidence": classification == "operational_continuation_evidence",
        "probe_without_failure": probe_without_failure,
        "classification": classification,
        "open_audit_policy_issue": bool(stronger_milestone and not strict_reproducible_flag),
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
    policy = checkpoint_policy_config(progress)
    markers = {
        round(float(STATUS_CONVENTION["pilot20_bounded_ceiling_mpa"]), 4),
        round(float(STATUS_CONVENTION["pilot21_bounded_ceiling_mpa"]), 4),
        4.4000,
    }
    markers.update(float(value) for value in unique_sorted_loads(policy.get("explicit_milestone_loads_mpa") or []))
    for key in ("target_load_mpa", "bootstrap_target_mpa"):
        value = float_or_none(metadata.get(key))
        if value is not None:
            markers.add(round(float(value), 4))
    return markers


def is_round_milestone(q_mpa: float, step_mpa: float | None = DEFAULT_MILESTONE_GRID_MPA, tol: float = 1.0e-9) -> bool:
    if step_mpa is None or float(step_mpa) <= 0.0:
        return False
    scaled = float(q_mpa) / float(step_mpa)
    return abs(scaled - round(scaled)) <= tol


def is_milestone_step(progress: dict[str, Any], step_entry: dict[str, Any]) -> bool:
    q_value = float_or_none(step_entry.get("q_mpa"))
    if q_value is None:
        return False
    milestone_grid = checkpoint_policy_config(progress).get("milestone_grid_mpa")
    if is_round_milestone(q_value, milestone_grid):
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
    grid = float_or_none(policy.get("milestone_grid_mpa", DEFAULT_MILESTONE_GRID_MPA))
    policy["milestone_grid_mpa"] = None if grid is None else float(grid)
    policy["explicit_milestone_loads_mpa"] = unique_sorted_loads(policy.get("explicit_milestone_loads_mpa") or [])
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
        "Rerun the fast runner with a more archival checkpoint policy or add that load via --milestone-load-mpa."
    )


def refresh_progress_summary(progress: dict[str, Any]) -> None:
    ensure_checkpoint_tracking(progress)
    highest_q = current_highest_q(progress)
    accepted_steps = progress.get("accepted_steps") or []
    suggested: list[float] = []
    for marker in (
        STATUS_CONVENTION["pilot20_bounded_ceiling_mpa"],
        STATUS_CONVENTION["pilot21_bounded_ceiling_mpa"],
        4.4000,
        highest_q,
    ):
        if marker is None:
            continue
        if any(abs(float(step.get("q_mpa")) - float(marker)) < 1.0e-9 for step in accepted_steps):
            if not any(abs(existing - float(marker)) < 1.0e-9 for existing in suggested):
                suggested.append(float(marker))
    run_dir = Path((progress.get("metadata") or {}).get("run_dir", FAST_RUN_DIR))
    retained_milestones = [
        round(float(step.get("q_mpa")), 4)
        for step in accepted_steps
        if bool(step.get("checkpoint_retained")) and "milestone" in list(step.get("checkpoint_tags") or [])
    ]
    progress["summary"] = {
        "highest_converged_q_mpa": highest_q,
        "terminal_failure_q_mpa": float_or_none((progress.get("state") or {}).get("terminal_failure_q_mpa")),
        "accepted_step_count": len(accepted_steps),
        "retained_step_checkpoint_count": sum(1 for step in accepted_steps if bool(step.get("checkpoint_retained"))),
        "named_checkpoint_count": sum(1 for relpath in named_checkpoint_paths(progress) if checkpoint_exists(run_dir, relpath)),
        "checkpoint_file_count": count_checkpoint_files(run_dir),
        "failure_event_count": len(progress.get("failure_events") or []),
        "suggested_confirm_loads_mpa": suggested,
        "retained_confirmable_loads_mpa": sorted({float(value) for value in retained_milestones}),
        "checkpoint_policy": checkpoint_policy_config(progress),
        "audit_policy": audit_policy_summary(),
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
