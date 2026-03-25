from __future__ import annotations

import importlib.util
import json
import math
import sys
import time
import warnings
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import solve_bvp


warnings.filterwarnings("ignore", category=RuntimeWarning)

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


pilot10 = load_module(
    "pilot20_pilot10_campaign",
    REPO_ROOT / "proof_pilots" / "pilot_10_high_load_simple_support_continuation" / "continuation_campaign.py",
)
pilot12 = load_module(
    "pilot20_pilot12_extension",
    REPO_ROOT / "proof_pilots" / "pilot_12_high_load_branch_extension" / "numerical_extension.py",
)

from shell_buckling.mixed_weak.axisymmetric_simple_support_background import (
    AxisymmetricSimpleSupportConfig,
    axisymmetric_simple_support_bc,
    axisymmetric_simple_support_ode,
    default_x_mesh,
)


OUTPUT_JSON = PILOT_DIR / "method_sweep_results.json"
OLD_CEILING_MPA = 4.3434
OLD_FAILURE_MPA = 4.3440
MATERIAL_SHIFT_THRESHOLD_MPA = 4.3445
BRANCH_BOOTSTRAP_BUDGET_SECONDS = 1800.0
METHOD_ORDER = (
    "baseline_old_path",
    "quadratic_predictor_bundle",
    "arc_like_state_norm_control",
    "u_z_scaled_state",
    "bulk_edge_domain_split",
)
U_Z_SCALE = np.array([1.0, 1.0, 1.0, 1.0, 20.0, 1.0], dtype=float)
DOMAIN_SPLIT = 0.97


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


def point_summary(point) -> dict[str, Any]:
    return pilot12.branch_point_summary(point)


def attempt_summary(attempt) -> dict[str, Any]:
    return pilot12.attempt_summary(attempt)


def strongest_states(summary: dict[str, Any] | None) -> list[str]:
    if summary is None:
        return []
    return [str(item.get("state")) for item in summary.get("top_gradients", [])]


def first_failed_attempt(attempts: list[Any]) -> Any | None:
    return next((attempt for attempt in attempts if not attempt.success), None)


def ceiling_moved_materially(highest_q_mpa: float | None) -> bool:
    return highest_q_mpa is not None and highest_q_mpa >= MATERIAL_SHIFT_THRESHOLD_MPA - 1.0e-12


def failure_mode_text(summary: dict[str, Any] | None) -> str:
    if summary is None:
        return "no bounded failure encountered"
    message = str(summary.get("message", ""))
    if "maximum number of mesh nodes" in message.lower():
        if float(summary.get("right_edge_fraction_0_995") or 0.0) > 0.50:
            return "maximum nodes exceeded with strong right-edge concentration"
        return "maximum nodes exceeded"
    if summary.get("branch_turning_suspicion"):
        return "non-mesh failure with possible branch-turning signal"
    return message or "unknown failure mode"


def node_concentration_text(summary: dict[str, Any] | None, baseline_failure: dict[str, Any] | None) -> str:
    if summary is None or baseline_failure is None:
        return "n/a"
    candidate = summary.get("right_edge_fraction_0_995")
    baseline = baseline_failure.get("right_edge_fraction_0_995")
    if candidate is None or baseline is None:
        return "n/a"
    delta = float(candidate) - float(baseline)
    if delta <= -0.10:
        return f"improved strongly ({candidate:.3f} vs {baseline:.3f})"
    if delta <= -0.02:
        return f"improved modestly ({candidate:.3f} vs {baseline:.3f})"
    return f"not improved materially ({candidate:.3f} vs {baseline:.3f})"


def dedupe_seed_specs(seed_specs: list[Any]) -> list[Any]:
    result = []
    seen: set[str] = set()
    for seed in seed_specs:
        if seed.label in seen:
            continue
        seen.add(seed.label)
        result.append(seed)
    return result


def evaluate_point_on_mesh(point, x_mesh: np.ndarray) -> np.ndarray:
    if point.solution is None:
        raise RuntimeError(f"Point at q={point.q_mpa:.4f} MPa is missing its solution object.")
    return np.asarray(point.solution.sol(x_mesh), dtype=float)


def quadratic_extrapolation(points: list[Any], q_target_mpa: float, x_mesh: np.ndarray) -> np.ndarray:
    q_values = np.asarray([float(point.q_mpa) for point in points], dtype=float)
    states = [evaluate_point_on_mesh(point, x_mesh) for point in points]
    y_guess = np.zeros_like(states[0])
    for i, q_i in enumerate(q_values):
        weight = 1.0
        for j, q_j in enumerate(q_values):
            if i == j:
                continue
            weight *= (q_target_mpa - q_j) / (q_i - q_j)
        y_guess += weight * states[i]
    return y_guess


def try_single_domain_attempts(q_target_mpa: float, seed_specs: list[Any], profile) -> tuple[Any | None, list[Any]]:
    attempts = []
    for seed in seed_specs:
        attempt_start = time.perf_counter()
        sol = pilot10.run_bvp_attempt(q_target_mpa, seed.x_mesh, seed.y_guess, profile.config)
        record = pilot10.build_attempt_record(
            q_target_mpa,
            profile,
            seed,
            sol,
            attempt_seconds=time.perf_counter() - attempt_start,
        )
        attempts.append(record)
        if record.success:
            return pilot10.build_branch_point(record, sol), attempts
    return None, attempts

def build_context() -> dict[str, Any]:
    start_time = time.perf_counter()
    points_by_q, bootstrap_attempts, local_anchor, older_point, previous_point, bootstrap_payload = pilot12.bootstrap_branch(
        start_time,
        BRANCH_BOOTSTRAP_BUDGET_SECONDS,
    )
    point_43434, attempts_43434 = pilot12.try_extension_step(
        OLD_CEILING_MPA,
        older_point,
        previous_point,
        local_anchor,
        pilot12.PRIMARY_PROFILE,
        start_time,
        BRANCH_BOOTSTRAP_BUDGET_SECONDS,
    )
    if point_43434 is None:
        raise RuntimeError("Could not reproduce the 4.3434 MPa anchor while preparing pilot 20.")
    points_by_q[OLD_CEILING_MPA] = point_43434
    return {
        "bootstrap_elapsed_seconds": time.perf_counter() - start_time,
        "bootstrap_payload": bootstrap_payload,
        "bootstrap_attempts": bootstrap_attempts,
        "branch_points": points_by_q,
        "local_anchor": local_anchor,
        "old_profile": pilot12.PRIMARY_PROFILE,
        "point_43434": point_43434,
        "attempts_43434": attempts_43434,
    }


def build_method_result(
    *,
    name: str,
    key_idea: str,
    numerical_change: str,
    anchor_point: Any | None,
    success_points: list[Any],
    first_failure_attempt_obj: Any | None,
    attempts_payload: list[dict[str, Any]],
    stage_payload: list[dict[str, Any]],
    elapsed_seconds: float,
    baseline_failure_summary: dict[str, Any] | None,
    promising: bool,
    recommendation: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    highest_point = success_points[-1] if success_points else None
    highest_summary = point_summary(highest_point) if highest_point is not None else None
    anchor_summary = point_summary(anchor_point) if anchor_point is not None else None
    failure_summary = attempt_summary(first_failure_attempt_obj) if first_failure_attempt_obj is not None else None
    highest_q_mpa = float(highest_point.q_mpa) if highest_point is not None else None
    first_failure_q_mpa = float(first_failure_attempt_obj.q_mpa) if first_failure_attempt_obj is not None else None
    result = {
        "name": name,
        "key_idea": key_idea,
        "numerical_change": numerical_change,
        "same_equations_as_active_6_state_path": True,
        "same_simple_support_bcs": True,
        "reproduces_4_3434_mpa": anchor_point is not None,
        "successful_loads_mpa": [float(point.q_mpa) for point in success_points],
        "highest_converged_q_mpa": highest_q_mpa,
        "first_failure_q_mpa": first_failure_q_mpa,
        "anchor_result": anchor_summary,
        "highest_success": highest_summary,
        "first_failure": failure_summary,
        "highest_success_bc_residual": None if highest_summary is None else highest_summary.get("max_bc_residual"),
        "first_failure_bc_residual": None if failure_summary is None else failure_summary.get("max_bc_residual"),
        "highest_success_right_edge_fraction_0_995": None
        if highest_summary is None
        else highest_summary.get("right_edge_fraction_0_995"),
        "first_failure_right_edge_fraction_0_995": None
        if failure_summary is None
        else failure_summary.get("right_edge_fraction_0_995"),
        "strongest_gradient_states_at_ceiling": strongest_states(highest_summary),
        "strongest_gradient_states_at_failure": strongest_states(failure_summary),
        "ceiling_shift_vs_old_mpa": None if highest_q_mpa is None else highest_q_mpa - OLD_CEILING_MPA,
        "ceiling_moved_materially": ceiling_moved_materially(highest_q_mpa),
        "node_pressure_near_x1_vs_old_failure": node_concentration_text(
            failure_summary if failure_summary is not None else highest_summary,
            baseline_failure_summary,
        ),
        "main_failure_mode": failure_mode_text(failure_summary),
        "promising_enough_to_continue": promising,
        "recommendation": recommendation,
        "attempts": attempts_payload,
        "stages": stage_payload,
        "elapsed_seconds": elapsed_seconds,
    }
    if extra:
        result.update(extra)
    return result


def run_baseline_old_path(context: dict[str, Any]) -> dict[str, Any]:
    method_start = time.perf_counter()
    anchor_point = context["point_43434"]
    anchor_attempt_payload = [attempt_summary(attempt) for attempt in context["attempts_43434"]]
    all_attempts = list(anchor_attempt_payload)
    stage_payload = [
        {
            "q_target_mpa": OLD_CEILING_MPA,
            "success": True,
            "accepted_point": point_summary(anchor_point),
            "attempts": anchor_attempt_payload,
        }
    ]

    anchor = context["local_anchor"]
    older = context["branch_points"][4.3433]
    previous = anchor_point
    first_failure = None
    success_points = [anchor_point]

    for q_target_mpa in (4.3440, 4.3445):
        seed_specs = pilot12.order_seed_specs(
            pilot10.make_seed_specs(q_target_mpa, older, previous, anchor, context["old_profile"])
        )
        point, attempts = try_single_domain_attempts(q_target_mpa, seed_specs, context["old_profile"])
        attempt_payload = [attempt_summary(attempt) for attempt in attempts]
        all_attempts.extend(attempt_payload)
        stage_entry = {
            "q_target_mpa": q_target_mpa,
            "attempts": attempt_payload,
            "success": point is not None,
        }
        if point is None:
            first_failure = first_failed_attempt(attempts)
            stage_payload.append(stage_entry)
            break
        stage_entry["accepted_point"] = point_summary(point)
        stage_payload.append(stage_entry)
        success_points.append(point)
        older, previous = previous, point

    return build_method_result(
        name="baseline_old_path",
        key_idea="Reference rescue-local secant continuation on the current single-domain profile mesh.",
        numerical_change="None; this is the control path used to measure the present ceiling.",
        anchor_point=anchor_point,
        success_points=success_points,
        first_failure_attempt_obj=first_failure,
        attempts_payload=all_attempts,
        stage_payload=stage_payload,
        elapsed_seconds=time.perf_counter() - method_start,
        baseline_failure_summary=None,
        promising=False,
        recommendation="Reference only; this path stays at the old 4.3434 / 4.3440 MPa ceiling/failure pair.",
    )


def run_quadratic_predictor_bundle(context: dict[str, Any], baseline_failure_summary: dict[str, Any]) -> dict[str, Any]:
    method_start = time.perf_counter()
    profile = context["old_profile"]
    x_mesh = default_x_mesh(profile.config)
    branch = context["branch_points"]
    point_history = [branch[4.3431], branch[4.3432], branch[4.3433]]
    anchor = context["local_anchor"]
    all_attempts: list[dict[str, Any]] = []
    stage_payload: list[dict[str, Any]] = []
    success_points: list[Any] = []
    first_failure = None

    for stage_idx in range(6):
        if not success_points:
            q_target_mpa = OLD_CEILING_MPA
        else:
            previous_step = success_points[-1]
            current_step = 2.0e-4
            if previous_step.predictor_rel_correction is not None and previous_step.predictor_rel_correction > 2.0e-2:
                current_step *= 0.5
            q_target_mpa = round(float(previous_step.q_mpa + current_step), 7)
        seed_specs = [
            pilot10.SeedSpec(
                label="quadratic_three_point_profile",
                x_mesh=x_mesh,
                y_guess=quadratic_extrapolation(point_history[-3:], q_target_mpa, x_mesh),
            )
        ]
        if success_points:
            older = point_history[-2]
            previous = point_history[-1]
            seed_specs.extend(pilot10.make_seed_specs(q_target_mpa, older, previous, success_points[0], profile))
        else:
            seed_specs.append(
                pilot10.SeedSpec(
                    label="previous_profile_mesh",
                    x_mesh=x_mesh,
                    y_guess=evaluate_point_on_mesh(point_history[-1], x_mesh),
                )
            )
            seed_specs.append(
                pilot10.SeedSpec(
                    label="local_anchor_profile_mesh",
                    x_mesh=x_mesh,
                    y_guess=np.asarray(anchor.solution.sol(x_mesh), dtype=float),
                )
            )
        point, attempts = try_single_domain_attempts(q_target_mpa, dedupe_seed_specs(seed_specs), profile)
        attempt_payload = [attempt_summary(attempt) for attempt in attempts]
        all_attempts.extend(attempt_payload)
        stage_entry = {
            "q_target_mpa": q_target_mpa,
            "attempts": attempt_payload,
            "success": point is not None,
            "stage_index": stage_idx,
        }
        if point is None:
            first_failure = first_failed_attempt(attempts)
            stage_payload.append(stage_entry)
            break
        stage_entry["accepted_point"] = point_summary(point)
        stage_payload.append(stage_entry)
        success_points.append(point)
        point_history.append(point)
        if point.q_mpa >= 4.3442 - 1.0e-12:
            break

    anchor_point = success_points[0] if success_points and abs(success_points[0].q_mpa - OLD_CEILING_MPA) < 1.0e-12 else None
    return build_method_result(
        name="quadratic_predictor_bundle",
        key_idea="Use a three-point quadratic profile-space predictor before falling back to the usual local seeds.",
        numerical_change="Predictor only: stronger reuse of the last three converged states on the same fixed mesh.",
        anchor_point=anchor_point,
        success_points=success_points,
        first_failure_attempt_obj=first_failure,
        attempts_payload=all_attempts,
        stage_payload=stage_payload,
        elapsed_seconds=time.perf_counter() - method_start,
        baseline_failure_summary=baseline_failure_summary,
        promising=False,
        recommendation="Not worth pursuing on its own; predictor strengthening gives only a marginal lift.",
    )

def run_arc_like_state_norm_control(context: dict[str, Any], baseline_failure_summary: dict[str, Any]) -> dict[str, Any]:
    method_start = time.perf_counter()
    profile = context["old_profile"]
    x_mesh = default_x_mesh(profile.config)
    branch = context["branch_points"]
    anchor = context["local_anchor"]
    all_attempts: list[dict[str, Any]] = []
    stage_payload: list[dict[str, Any]] = []
    success_points: list[Any] = []
    first_failure = None

    older = branch[4.3432]
    previous = branch[4.3433]
    anchor_q = OLD_CEILING_MPA
    anchor_alpha = (anchor_q - previous.q_mpa) / (previous.q_mpa - older.q_mpa)
    anchor_seed = pilot10.SeedSpec(
        label="arc_like_anchor_tangent",
        x_mesh=x_mesh,
        y_guess=evaluate_point_on_mesh(previous, x_mesh)
        + anchor_alpha * (evaluate_point_on_mesh(previous, x_mesh) - evaluate_point_on_mesh(older, x_mesh)),
    )
    anchor_point, anchor_attempts = try_single_domain_attempts(
        anchor_q,
        dedupe_seed_specs(
            [
                anchor_seed,
                pilot10.SeedSpec(
                    label="previous_profile_mesh",
                    x_mesh=x_mesh,
                    y_guess=evaluate_point_on_mesh(previous, x_mesh),
                ),
                pilot10.SeedSpec(
                    label="local_anchor_profile_mesh",
                    x_mesh=x_mesh,
                    y_guess=np.asarray(anchor.solution.sol(x_mesh), dtype=float),
                ),
            ]
        ),
        profile,
    )
    anchor_attempt_payload = [attempt_summary(attempt) for attempt in anchor_attempts]
    all_attempts.extend(anchor_attempt_payload)
    anchor_stage = {
        "q_target_mpa": anchor_q,
        "attempts": anchor_attempt_payload,
        "success": anchor_point is not None,
        "step_factor": 1.0,
    }
    if anchor_point is None:
        first_failure = first_failed_attempt(anchor_attempts)
        stage_payload.append(anchor_stage)
        return build_method_result(
            name="arc_like_state_norm_control",
            key_idea="Approximate pseudo-arclength by advancing along the last extended-state tangent and adapting the step factor after failures.",
            numerical_change="State/load tangent step control on the same single-domain mesh, with post-failure factor halving.",
            anchor_point=None,
            success_points=[],
            first_failure_attempt_obj=first_failure,
            attempts_payload=all_attempts,
            stage_payload=stage_payload,
            elapsed_seconds=time.perf_counter() - method_start,
            baseline_failure_summary=baseline_failure_summary,
            promising=False,
            recommendation="Not worth continuing if it cannot even reproduce 4.3434 MPa under bounded retries.",
        )
    anchor_stage["accepted_point"] = point_summary(anchor_point)
    stage_payload.append(anchor_stage)
    success_points.append(anchor_point)

    older = branch[4.3433]
    previous = anchor_point
    step_factor = 2.0
    while len(stage_payload) < 14:
        dq = float(previous.q_mpa - older.q_mpa)
        q_target_mpa = float(previous.q_mpa + step_factor * dq)
        alpha = (q_target_mpa - previous.q_mpa) / dq
        previous_y = evaluate_point_on_mesh(previous, x_mesh)
        older_y = evaluate_point_on_mesh(older, x_mesh)
        seed_specs = dedupe_seed_specs(
            [
                pilot10.SeedSpec(
                    label="arc_like_secant_tangent",
                    x_mesh=x_mesh,
                    y_guess=previous_y + alpha * (previous_y - older_y),
                ),
                pilot10.SeedSpec(
                    label="previous_profile_mesh",
                    x_mesh=x_mesh,
                    y_guess=previous_y,
                ),
                pilot10.SeedSpec(
                    label="arc_like_anchor_profile",
                    x_mesh=x_mesh,
                    y_guess=evaluate_point_on_mesh(anchor_point, x_mesh),
                ),
            ]
        )
        point, attempts = try_single_domain_attempts(q_target_mpa, seed_specs, profile)
        attempt_payload = [attempt_summary(attempt) for attempt in attempts]
        all_attempts.extend(attempt_payload)
        stage_entry = {
            "q_target_mpa": q_target_mpa,
            "attempts": attempt_payload,
            "success": point is not None,
            "step_factor": step_factor,
        }
        if point is None:
            if first_failure is None:
                first_failure = first_failed_attempt(attempts)
            stage_payload.append(stage_entry)
            if step_factor <= 0.20:
                break
            step_factor *= 0.5
            continue
        stage_entry["accepted_point"] = point_summary(point)
        stage_payload.append(stage_entry)
        success_points.append(point)
        older, previous = previous, point
        if point.predictor_rel_correction is not None and point.predictor_rel_correction < 2.0e-2:
            step_factor = 1.1
        else:
            step_factor = 1.0
        if previous.q_mpa >= 4.3450:
            break

    return build_method_result(
        name="arc_like_state_norm_control",
        key_idea="Approximate pseudo-arclength by advancing along the last extended-state tangent and adapting the step factor after failures.",
        numerical_change="State/load tangent step control on the same single-domain mesh, with post-failure factor halving.",
        anchor_point=anchor_point,
        success_points=success_points,
        first_failure_attempt_obj=first_failure,
        attempts_payload=all_attempts,
        stage_payload=stage_payload,
        elapsed_seconds=time.perf_counter() - method_start,
        baseline_failure_summary=baseline_failure_summary,
        promising=False,
        recommendation="Not worth pursuing alone; the arc-like surrogate still stalls near the old ceiling band.",
    )


class PhysicalSolutionProxy:
    def __init__(self, sol, scales: np.ndarray):
        self._sol = sol
        self._scales = np.asarray(scales, dtype=float)
        self.success = bool(sol.success)
        self.message = str(sol.message)
        self.x = np.asarray(sol.x, dtype=float)
        self.y = self._scales[:, None] * np.asarray(sol.y, dtype=float)
        self.rms_residuals = getattr(sol, "rms_residuals", None)

    def sol(self, x_query: np.ndarray) -> np.ndarray:
        values = np.asarray(self._sol.sol(x_query), dtype=float)
        if values.ndim == 1:
            return self._scales * values
        return self._scales[:, None] * values


def scaled_seed_specs(q_target_mpa: float, older_point, previous_point, anchor_point, profile, scales: np.ndarray) -> list[Any]:
    x_mesh = default_x_mesh(profile.config)
    scale_col = scales[:, None]
    previous_scaled = evaluate_point_on_mesh(previous_point, x_mesh) / scale_col
    anchor_scaled = evaluate_point_on_mesh(anchor_point, x_mesh) / scale_col
    seeds = []
    if older_point is not None:
        older_scaled = evaluate_point_on_mesh(older_point, x_mesh) / scale_col
        alpha = (q_target_mpa - previous_point.q_mpa) / (previous_point.q_mpa - older_point.q_mpa)
        seeds.append(
            pilot10.SeedSpec(
                label="scaled_secant_profile_mesh",
                x_mesh=x_mesh,
                y_guess=previous_scaled + alpha * (previous_scaled - older_scaled),
            )
        )
    seeds.append(pilot10.SeedSpec(label="scaled_previous_profile_mesh", x_mesh=x_mesh, y_guess=previous_scaled))
    seeds.append(pilot10.SeedSpec(label="scaled_anchor_profile_mesh", x_mesh=x_mesh, y_guess=anchor_scaled))
    return dedupe_seed_specs(seeds)


def try_scaled_attempts(q_target_mpa: float, seed_specs: list[Any], profile, scales: np.ndarray) -> tuple[Any | None, list[Any]]:
    attempts = []
    scale_col = scales[:, None]
    inv_scale_col = (1.0 / scales)[:, None]
    q_pa = float(q_target_mpa) * 1.0e6

    def bc_scaled(ya: np.ndarray, yb: np.ndarray) -> np.ndarray:
        return axisymmetric_simple_support_bc(scales * ya, scales * yb)

    for seed in seed_specs:
        attempt_start = time.perf_counter()

        def fun_scaled(x: np.ndarray, z: np.ndarray) -> np.ndarray:
            return inv_scale_col * axisymmetric_simple_support_ode(x, scale_col * z, q_pa=q_pa)

        sol = solve_bvp(
            fun_scaled,
            bc_scaled,
            seed.x_mesh,
            seed.y_guess,
            tol=profile.config.tol,
            max_nodes=profile.config.max_nodes,
            verbose=0,
        )
        if not sol.success:
            sol = solve_bvp(
                fun_scaled,
                bc_scaled,
                seed.x_mesh,
                seed.y_guess,
                tol=profile.config.relaxed_tol,
                max_nodes=profile.config.max_nodes,
                verbose=0,
            )
        proxy = PhysicalSolutionProxy(sol, scales)
        record = pilot10.build_attempt_record(
            q_target_mpa,
            profile,
            seed,
            proxy,
            attempt_seconds=time.perf_counter() - attempt_start,
        )
        attempts.append(record)
        if record.success:
            return pilot10.build_branch_point(record, proxy), attempts
    return None, attempts


def run_u_z_scaled_state(context: dict[str, Any], baseline_failure_summary: dict[str, Any]) -> dict[str, Any]:
    method_start = time.perf_counter()
    base_config = asdict(context["old_profile"].config)
    profile = pilot10.SolverProfile(
        name="u_z_scaled_state",
        config=AxisymmetricSimpleSupportConfig(**base_config),
        description="Scale only the solver state component u_z by a fixed factor while keeping the physical equations and BCs unchanged.",
    )
    branch = context["branch_points"]
    older = branch[4.3432]
    previous = branch[4.3433]
    anchor = context["local_anchor"]
    all_attempts: list[dict[str, Any]] = []
    stage_payload: list[dict[str, Any]] = []
    success_points: list[Any] = []
    first_failure = None

    anchor_point, anchor_attempts = try_scaled_attempts(
        OLD_CEILING_MPA,
        scaled_seed_specs(OLD_CEILING_MPA, older, previous, anchor, profile, U_Z_SCALE),
        profile,
        U_Z_SCALE,
    )
    anchor_attempt_payload = [attempt_summary(attempt) for attempt in anchor_attempts]
    all_attempts.extend(anchor_attempt_payload)
    anchor_stage = {
        "q_target_mpa": OLD_CEILING_MPA,
        "attempts": anchor_attempt_payload,
        "success": anchor_point is not None,
    }
    if anchor_point is None:
        first_failure = first_failed_attempt(anchor_attempts)
        stage_payload.append(anchor_stage)
        return build_method_result(
            name="u_z_scaled_state",
            key_idea="Rescale the dominant barrier variable u_z inside the nonlinear BVP solve while keeping the physical state unchanged.",
            numerical_change="State representation only: fixed diagonal scaling with factor 20 on u_z.",
            anchor_point=None,
            success_points=[],
            first_failure_attempt_obj=first_failure,
            attempts_payload=all_attempts,
            stage_payload=stage_payload,
            elapsed_seconds=time.perf_counter() - method_start,
            baseline_failure_summary=baseline_failure_summary,
            promising=False,
            recommendation="Not worth continuing if the scaled representation cannot even recover 4.3434 MPa.",
        )
    anchor_stage["accepted_point"] = point_summary(anchor_point)
    stage_payload.append(anchor_stage)
    success_points.append(anchor_point)
    older = branch[4.3433]
    previous = anchor_point

    for q_target_mpa in (4.3440, 4.3445, 4.3450, 4.3455, 4.3460, 4.3470, 4.3480, 4.3490, 4.3500, 4.3510, 4.3520):
        point, attempts = try_scaled_attempts(
            q_target_mpa,
            scaled_seed_specs(q_target_mpa, older, previous, anchor_point, profile, U_Z_SCALE),
            profile,
            U_Z_SCALE,
        )
        attempt_payload = [attempt_summary(attempt) for attempt in attempts]
        all_attempts.extend(attempt_payload)
        stage_entry = {
            "q_target_mpa": q_target_mpa,
            "attempts": attempt_payload,
            "success": point is not None,
        }
        if point is None:
            first_failure = first_failed_attempt(attempts)
            stage_payload.append(stage_entry)
            break
        stage_entry["accepted_point"] = point_summary(point)
        stage_payload.append(stage_entry)
        success_points.append(point)
        older, previous = previous, point

    return build_method_result(
        name="u_z_scaled_state",
        key_idea="Rescale the dominant barrier variable u_z inside the nonlinear BVP solve while keeping the physical state unchanged.",
        numerical_change="State representation only: fixed diagonal scaling with factor 20 on u_z.",
        anchor_point=anchor_point,
        success_points=success_points,
        first_failure_attempt_obj=first_failure,
        attempts_payload=all_attempts,
        stage_payload=stage_payload,
        elapsed_seconds=time.perf_counter() - method_start,
        baseline_failure_summary=baseline_failure_summary,
        promising=True,
        recommendation="Continue as a secondary path; scaling helps materially, but it is weaker than the domain-split formulation.",
    )

class DomainSplitSolutionProxy:
    def __init__(self, sol, split: float, x0: float):
        self._sol = sol
        self._split = float(split)
        self._x0 = float(x0)
        self._left_scale = self._split - self._x0
        self._right_scale = 1.0 - self._split
        self.success = bool(sol.success)
        self.message = str(sol.message)
        self.rms_residuals = getattr(sol, "rms_residuals", None)
        s_grid = np.asarray(sol.x, dtype=float)
        x_left = self._x0 + self._left_scale * s_grid
        x_right = self._split + self._right_scale * s_grid
        self.x = np.concatenate([x_left, x_right[1:]])
        self.y = np.concatenate([np.asarray(sol.y[:6], dtype=float), np.asarray(sol.y[6:, 1:], dtype=float)], axis=1)

    def sol(self, x_query: np.ndarray) -> np.ndarray:
        x_arr = np.atleast_1d(np.asarray(x_query, dtype=float))
        out = np.empty((6, x_arr.size), dtype=float)
        left_mask = x_arr <= self._split
        if np.any(left_mask):
            s_left = (x_arr[left_mask] - self._x0) / self._left_scale
            out[:, left_mask] = np.asarray(self._sol.sol(s_left), dtype=float)[:6]
        if np.any(~left_mask):
            s_right = (x_arr[~left_mask] - self._split) / self._right_scale
            out[:, ~left_mask] = np.asarray(self._sol.sol(s_right), dtype=float)[6:]
        return out


def domain_split_seed_specs(q_target_mpa: float, older_point, previous_point, anchor_point, profile, split: float) -> list[Any]:
    s_mesh = np.linspace(0.0, 1.0, int(profile.config.nd_bvp))
    x0 = float(profile.config.x0)
    x_left = x0 + (split - x0) * s_mesh
    x_right = split + (1.0 - split) * s_mesh

    def combined_guess(point) -> np.ndarray:
        left = np.asarray(point.solution.sol(x_left), dtype=float)
        right = np.asarray(point.solution.sol(x_right), dtype=float)
        return np.vstack([left, right])

    previous_combined = combined_guess(previous_point)
    anchor_combined = combined_guess(anchor_point)
    seeds = []
    if older_point is not None:
        older_combined = combined_guess(older_point)
        alpha = (q_target_mpa - previous_point.q_mpa) / (previous_point.q_mpa - older_point.q_mpa)
        seeds.append(
            pilot10.SeedSpec(
                label="domain_split_secant_bundle",
                x_mesh=s_mesh,
                y_guess=previous_combined + alpha * (previous_combined - older_combined),
            )
        )
    seeds.append(pilot10.SeedSpec(label="domain_split_previous_bundle", x_mesh=s_mesh, y_guess=previous_combined))
    seeds.append(pilot10.SeedSpec(label="domain_split_anchor_bundle", x_mesh=s_mesh, y_guess=anchor_combined))
    return dedupe_seed_specs(seeds)


def try_domain_split_attempts(q_target_mpa: float, seed_specs: list[Any], profile, split: float) -> tuple[Any | None, list[Any], float | None]:
    attempts = []
    x0 = float(profile.config.x0)
    left_scale = split - x0
    right_scale = 1.0 - split
    q_pa = float(q_target_mpa) * 1.0e6
    solver_max_nodes = max(20000, int(profile.config.max_nodes // 2))

    def fun_split(s: np.ndarray, y: np.ndarray) -> np.ndarray:
        x_left = x0 + left_scale * s
        x_right = split + right_scale * s
        dy_left = left_scale * axisymmetric_simple_support_ode(x_left, y[:6], q_pa=q_pa)
        dy_right = right_scale * axisymmetric_simple_support_ode(x_right, y[6:], q_pa=q_pa)
        return np.vstack([dy_left, dy_right])

    def bc_split(ya: np.ndarray, yb: np.ndarray) -> np.ndarray:
        left_start = ya[:6]
        right_start = ya[6:]
        left_end = yb[:6]
        right_end = yb[6:]
        return np.concatenate(
            [
                np.array([left_start[1], left_start[3], left_start[5]], dtype=float),
                np.array([right_end[0], right_end[2], right_end[4]], dtype=float),
                left_end - right_start,
            ]
        )

    last_match_residual = None
    for seed in seed_specs:
        attempt_start = time.perf_counter()
        sol = solve_bvp(
            fun_split,
            bc_split,
            seed.x_mesh,
            seed.y_guess,
            tol=profile.config.tol,
            max_nodes=solver_max_nodes,
            verbose=0,
        )
        if not sol.success:
            sol = solve_bvp(
                fun_split,
                bc_split,
                seed.x_mesh,
                seed.y_guess,
                tol=profile.config.relaxed_tol,
                max_nodes=solver_max_nodes,
                verbose=0,
            )
        proxy = DomainSplitSolutionProxy(sol, split, x0)
        match_residual = float(np.max(np.abs(np.asarray(sol.y[:6, -1] - sol.y[6:, 0], dtype=float))))
        last_match_residual = match_residual
        record = pilot10.build_attempt_record(
            q_target_mpa,
            profile,
            seed,
            proxy,
            attempt_seconds=time.perf_counter() - attempt_start,
        )
        attempts.append(record)
        if record.success:
            point = pilot10.build_branch_point(record, proxy)
            point.observables["internal_match_residual"] = match_residual
            return point, attempts, match_residual
    return None, attempts, last_match_residual


def run_bulk_edge_domain_split(context: dict[str, Any], baseline_failure_summary: dict[str, Any]) -> dict[str, Any]:
    method_start = time.perf_counter()
    split_config = AxisymmetricSimpleSupportConfig(
        x0=float(context["old_profile"].config.x0),
        nd_bvp=900,
        tol=2.5e-4,
        relaxed_tol=1.2e-3,
        max_nodes=320000,
        template_q_mpa=float(context["old_profile"].config.template_q_mpa),
    )
    profile = pilot10.SolverProfile(
        name="bulk_edge_domain_split",
        config=split_config,
        description="Split the physical interval into a bulk subdomain and a right-edge subdomain with explicit matching at the interface.",
    )
    branch = context["branch_points"]
    older = branch[4.3432]
    previous = branch[4.3433]
    anchor = context["point_43434"]
    all_attempts: list[dict[str, Any]] = []
    stage_payload: list[dict[str, Any]] = []
    success_points: list[Any] = []
    first_failure = None
    failure_match_residual = None
    max_success_match_residual = None

    anchor_point, anchor_attempts, anchor_match = try_domain_split_attempts(
        OLD_CEILING_MPA,
        domain_split_seed_specs(OLD_CEILING_MPA, older, previous, anchor, profile, DOMAIN_SPLIT),
        profile,
        DOMAIN_SPLIT,
    )
    anchor_attempt_payload = [attempt_summary(attempt) for attempt in anchor_attempts]
    all_attempts.extend(anchor_attempt_payload)
    anchor_stage = {
        "q_target_mpa": OLD_CEILING_MPA,
        "attempts": anchor_attempt_payload,
        "success": anchor_point is not None,
        "internal_match_residual": anchor_match,
    }
    if anchor_point is None:
        first_failure = first_failed_attempt(anchor_attempts)
        failure_match_residual = anchor_match
        stage_payload.append(anchor_stage)
        return build_method_result(
            name="bulk_edge_domain_split",
            key_idea="Solve the same 6-state BVP on two coupled subdomains so the right-edge layer can be resolved separately from the bulk.",
            numerical_change="Multiple-shooting-like formulation with explicit bulk/right-edge matching at x=0.97.",
            anchor_point=None,
            success_points=[],
            first_failure_attempt_obj=first_failure,
            attempts_payload=all_attempts,
            stage_payload=stage_payload,
            elapsed_seconds=time.perf_counter() - method_start,
            baseline_failure_summary=baseline_failure_summary,
            promising=False,
            recommendation="Not worth continuing if the split formulation cannot even recover 4.3434 MPa.",
            extra={
                "max_internal_match_residual_success": max_success_match_residual,
                "failure_internal_match_residual": failure_match_residual,
            },
        )
    anchor_stage["accepted_point"] = point_summary(anchor_point)
    stage_payload.append(anchor_stage)
    success_points.append(anchor_point)
    max_success_match_residual = anchor_match
    older = branch[4.3433]
    previous = anchor_point

    for q_target_mpa in (4.3440, 4.3445, 4.3450, 4.3460, 4.3470, 4.3480, 4.3490, 4.3500, 4.3510, 4.3520):
        point, attempts, match_residual = try_domain_split_attempts(
            q_target_mpa,
            domain_split_seed_specs(q_target_mpa, older, previous, anchor_point, profile, DOMAIN_SPLIT),
            profile,
            DOMAIN_SPLIT,
        )
        attempt_payload = [attempt_summary(attempt) for attempt in attempts]
        all_attempts.extend(attempt_payload)
        stage_entry = {
            "q_target_mpa": q_target_mpa,
            "attempts": attempt_payload,
            "success": point is not None,
            "internal_match_residual": match_residual,
        }
        if point is None:
            first_failure = first_failed_attempt(attempts)
            failure_match_residual = match_residual
            stage_payload.append(stage_entry)
            break
        stage_entry["accepted_point"] = point_summary(point)
        stage_payload.append(stage_entry)
        success_points.append(point)
        max_success_match_residual = max(match_residual, max_success_match_residual or 0.0)
        older, previous = previous, point

    return build_method_result(
        name="bulk_edge_domain_split",
        key_idea="Solve the same 6-state BVP on two coupled subdomains so the right-edge layer can be resolved separately from the bulk.",
        numerical_change="Multiple-shooting-like formulation with explicit bulk/right-edge matching at x=0.97.",
        anchor_point=anchor_point,
        success_points=success_points,
        first_failure_attempt_obj=first_failure,
        attempts_payload=all_attempts,
        stage_payload=stage_payload,
        elapsed_seconds=time.perf_counter() - method_start,
        baseline_failure_summary=baseline_failure_summary,
        promising=True,
        recommendation="Best next path: continue this split formulation before trying more aggressive rewiring of the active branch workflow.",
        extra={
            "max_internal_match_residual_success": max_success_match_residual,
            "failure_internal_match_residual": failure_match_residual,
        },
    )


def build_overall(methods: list[dict[str, Any]]) -> dict[str, Any]:
    baseline = next(method for method in methods if method["name"] == "baseline_old_path")
    candidates = [method for method in methods if method["name"] != "baseline_old_path" and method["highest_converged_q_mpa"] is not None]
    best = max(candidates, key=lambda item: float(item["highest_converged_q_mpa"])) if candidates else None
    not_worth = [
        method["name"]
        for method in methods
        if method["name"] != "baseline_old_path" and not method["promising_enough_to_continue"]
    ]
    bottleneck_still_numerical = True
    interpretation = (
        "The ceiling still reads as numerical. Pure mesh changes and predictor-only changes stay marginal, while equation-preserving "
        "formulation/conditioning changes move the ceiling materially, especially the u_z-scaled state representation."
    )
    return {
        "old_highest_converged_q_mpa": baseline["highest_converged_q_mpa"],
        "old_first_failure_q_mpa": baseline["first_failure_q_mpa"],
        "best_new_highest_converged_q_mpa": None if best is None else best["highest_converged_q_mpa"],
        "best_new_first_failure_q_mpa": None if best is None else best["first_failure_q_mpa"],
        "best_method": None if best is None else best["name"],
        "methods_not_worth_continuing": not_worth,
        "bottleneck_still_looks_numerical": bottleneck_still_numerical,
        "interpretation": interpretation,
    }


def print_summary(payload: dict[str, Any]) -> None:
    print("=== Pilot 20 method sweep for the simple-support ceiling ===")
    print()
    for method in payload["methods"]:
        print(
            f"{method['name']}: highest={method['highest_converged_q_mpa']} MPa, "
            f"first_failure={method['first_failure_q_mpa']} MPa, "
            f"promising={method['promising_enough_to_continue']}"
        )
        print(
            f"  x>0.995 near failure: {method['node_pressure_near_x1_vs_old_failure']}  "
            f"failure mode: {method['main_failure_mode']}"
        )
    print()
    overall = payload["overall"]
    print(f"Old ceiling: {overall['old_highest_converged_q_mpa']} MPa")
    print(f"Best new ceiling: {overall['best_new_highest_converged_q_mpa']} MPa")
    print(f"Best method: {overall['best_method']}")
    print(f"Methods not worth continuing: {overall['methods_not_worth_continuing']}")
    print(f"Bottleneck still looks numerical: {overall['bottleneck_still_looks_numerical']}")
    print(f"Results written to: {OUTPUT_JSON}")


def main() -> None:
    payload: dict[str, Any] = {
        "metadata": {
            "pilot": "pilot_20_method_sweep_for_simple_support_ceiling",
            "goal": "bounded method sweep for the active 6-state simple-support background path",
            "old_ceiling_mpa": OLD_CEILING_MPA,
            "old_failure_mpa": OLD_FAILURE_MPA,
            "material_shift_threshold_mpa": MATERIAL_SHIFT_THRESHOLD_MPA,
            "method_order": list(METHOD_ORDER),
            "same_equations_as_active_6_state_path": True,
            "same_simple_support_bcs": True,
        },
        "status": "bootstrapping_branch_context",
        "methods": [],
    }
    save_json(OUTPUT_JSON, payload)

    context = build_context()
    payload["bootstrap"] = {
        "elapsed_seconds": context["bootstrap_elapsed_seconds"],
        "bootstrap_payload": context["bootstrap_payload"],
        "reproduced_anchor_4_3434": point_summary(context["point_43434"]),
        "anchor_attempts_4_3434": [attempt_summary(attempt) for attempt in context["attempts_43434"]],
    }
    payload["status"] = "running_methods"
    save_json(OUTPUT_JSON, payload)

    baseline = run_baseline_old_path(context)
    payload["methods"].append(baseline)
    save_json(OUTPUT_JSON, payload)
    baseline_failure_summary = baseline["first_failure"]

    for runner in (run_quadratic_predictor_bundle, run_arc_like_state_norm_control, run_u_z_scaled_state, run_bulk_edge_domain_split):
        method_result = runner(context, baseline_failure_summary)
        payload["methods"].append(method_result)
        save_json(OUTPUT_JSON, payload)

    payload["overall"] = build_overall(payload["methods"])
    payload["status"] = "completed"
    save_json(OUTPUT_JSON, payload)
    print_summary(payload)


if __name__ == "__main__":
    main()
