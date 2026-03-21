from __future__ import annotations

import argparse
import json
import math
import sys
import time
import warnings
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import solve_bvp


warnings.filterwarnings("ignore", category=RuntimeWarning)

THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parent if (THIS_FILE.parent / "src").exists() else THIS_FILE.parents[2]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from shell_buckling.mixed_weak.axisymmetric_simple_support_background import (
    AxisymmetricSimpleSupportConfig,
    STATE_LABELS,
    axisymmetric_simple_support_bc,
    axisymmetric_simple_support_ode,
    build_template_solution,
    default_x_mesh,
    solve_axisymmetric_simple_support_fixed_load,
)


PILOT_DIR = REPO_ROOT / "proof_pilots" / "pilot_10_high_load_simple_support_continuation"
DEFAULT_OUTPUT_JSON = PILOT_DIR / "campaign_results.json"
PREVIOUS_DOCUMENTED_CEILING_MPA = 4.343
PREVIOUS_DOCUMENTED_FAILURE_MPA = 4.344
DEFAULT_ANCHOR_LOADS_MPA = (4.30, 4.325, 4.3275, 4.328, 4.329, 4.330, 4.332, 4.335)
DEFAULT_LOCAL_BOOTSTRAP_LOADS_MPA = (4.336, 4.337, 4.338, 4.339, 4.340, 4.341, 4.342, 4.343)


@dataclass(frozen=True)
class SolverProfile:
    name: str
    config: AxisymmetricSimpleSupportConfig
    description: str


@dataclass(frozen=True)
class SeedSpec:
    label: str
    x_mesh: np.ndarray
    y_guess: np.ndarray


@dataclass
class BranchPoint:
    q_mpa: float
    x: np.ndarray
    y: np.ndarray
    solution: Any | None
    message: str
    nodes: int
    max_rms: float
    max_bc_residual: float
    min_r: float
    node_pressure: float
    right_edge_fraction_0_99: float
    right_edge_fraction_0_995: float
    right_edge_fraction_0_999: float
    min_dx: float
    min_dx_mid: float
    top_gradients: list[dict[str, float | str]]
    observables: dict[str, float]
    accepted_profile: str
    accepted_seed: str
    predictor_rel_correction: float | None
    predictor_abs_correction: float | None


@dataclass
class AttemptRecord:
    q_mpa: float
    profile_name: str
    seed_label: str
    success: bool
    attempt_seconds: float
    message: str
    nodes: int
    max_nodes: int
    max_rms: float
    max_bc_residual: float
    min_r: float
    node_pressure: float
    right_edge_fraction_0_99: float
    right_edge_fraction_0_995: float
    right_edge_fraction_0_999: float
    min_dx: float
    min_dx_mid: float
    top_gradients: list[dict[str, float | str]]
    observables: dict[str, float]
    mesh_pressure_only: bool
    right_edge_layer_suspicion: bool
    branch_turning_suspicion: bool
    predictor_rel_correction: float | None
    predictor_abs_correction: float | None


@dataclass
class CampaignOutcome:
    previous_documented_ceiling_mpa: float
    previous_documented_failure_mpa: float
    band_start_mpa: float
    band_end_mpa: float
    initial_step_mpa: float
    min_step_mpa: float
    budget_seconds: float
    mode: str
    anchor_loads_mpa: list[float]
    bootstrap_loads_mpa: list[float]
    profiles: list[dict[str, Any]]
    anchor_results: list[dict[str, Any]]
    accepted_points: list[dict[str, Any]]
    attempts: list[dict[str, Any]]
    highest_converged_q_mpa: float | None
    first_failed_attempt_q_mpa: float | None
    terminal_unresolved_q_mpa: float | None
    elapsed_seconds: float
    stopped_reason: str
    band_reached: bool
    progress_still_being_made: bool
    failure_diagnosis: dict[str, Any]
    branch_assessment: dict[str, Any]


def make_profiles(mode: str) -> list[SolverProfile]:
    strict = SolverProfile(
        name="strict_local",
        config=AxisymmetricSimpleSupportConfig(
            nd_bvp=950,
            tol=2.0e-4,
            relaxed_tol=1.0e-3,
            max_nodes=350000,
            right_edge_cluster_start=0.965,
            right_edge_cluster_fraction=0.60,
            right_edge_cluster_power=1.8,
        ),
        description="Pilot-09-like strict local profile on a right-edge-focused mesh.",
    )
    if mode == "strict":
        return [strict]

    rescue = SolverProfile(
        name="rescue_local",
        config=AxisymmetricSimpleSupportConfig(
            nd_bvp=950,
            tol=2.5e-4,
            relaxed_tol=1.2e-3,
            max_nodes=600000,
            right_edge_cluster_start=0.965,
            right_edge_cluster_fraction=0.60,
            right_edge_cluster_power=1.8,
        ),
        description="Relaxed local profile with a larger node budget on the same clustered mesh.",
    )
    edge_aggressive = SolverProfile(
        name="edge_aggressive",
        config=AxisymmetricSimpleSupportConfig(
            nd_bvp=1200,
            tol=2.5e-4,
            relaxed_tol=1.2e-3,
            max_nodes=600000,
            right_edge_cluster_start=0.982,
            right_edge_cluster_fraction=0.78,
            right_edge_cluster_power=3.0,
        ),
        description="Rescue profile with stronger right-edge clustering for the boundary layer near x=1.",
    )
    return [rescue]


def run_bvp_attempt(
    q_mpa: float,
    x_mesh: np.ndarray,
    y_guess: np.ndarray,
    config: AxisymmetricSimpleSupportConfig,
):
    q_pa = float(q_mpa) * 1.0e6
    fun = lambda x, y: axisymmetric_simple_support_ode(x, y, q_pa=q_pa)
    sol = solve_bvp(
        fun,
        axisymmetric_simple_support_bc,
        x_mesh,
        y_guess,
        tol=config.tol,
        max_nodes=config.max_nodes,
        verbose=0,
    )
    if not sol.success:
        sol = solve_bvp(
            fun,
            axisymmetric_simple_support_bc,
            x_mesh,
            y_guess,
            tol=config.relaxed_tol,
            max_nodes=config.max_nodes,
            verbose=0,
        )
    return sol


def safe_max_rms(sol) -> float:
    if hasattr(sol, "rms_residuals") and sol.rms_residuals is not None and len(sol.rms_residuals):
        return float(np.max(sol.rms_residuals))
    return float("nan")


def compute_bc_residual(sol) -> float:
    try:
        bc = axisymmetric_simple_support_bc(sol.y[:, 0], sol.y[:, -1])
        return float(np.max(np.abs(bc)))
    except Exception:
        return float("nan")


def compute_min_r(sol) -> float:
    try:
        r = sol.x + sol.y[3]
        return float(np.min(r))
    except Exception:
        return float("nan")


def compute_gradient_diagnostics(sol) -> tuple[float, float, list[dict[str, float | str]]]:
    try:
        dx = np.diff(sol.x)
        min_idx = int(np.argmin(dx))
        min_dx = float(dx[min_idx])
        min_dx_mid = float(0.5 * (sol.x[min_idx] + sol.x[min_idx + 1]))
    except Exception:
        min_dx = float("nan")
        min_dx_mid = float("nan")

    gradients: list[dict[str, float | str]] = []
    try:
        for idx, name in enumerate(STATE_LABELS):
            grad = np.gradient(sol.y[idx], sol.x, edge_order=1)
            peak_idx = int(np.argmax(np.abs(grad)))
            gradients.append(
                {
                    "state": name,
                    "max_abs_grad": float(np.max(np.abs(grad))),
                    "x_at_peak": float(sol.x[peak_idx]),
                }
            )
        gradients.sort(key=lambda item: float(item["max_abs_grad"]), reverse=True)
    except Exception:
        pass
    return min_dx, min_dx_mid, gradients[:3]


def compute_observables(sol, config: AxisymmetricSimpleSupportConfig) -> dict[str, float]:
    try:
        x_probe = np.array([config.x0, 0.25, 0.50, 0.75, 0.95, 0.99, 0.995, 1.0], dtype=float)
        y_probe = sol.sol(x_probe)
        return {
            "Ts_x0": float(y_probe[0, 0]),
            "Tsn_1": float(y_probe[1, -1]),
            "Ms_x0": float(y_probe[2, 0]),
            "ur_1": float(y_probe[3, -1]),
            "uz_x0": float(y_probe[4, 0]),
            "phi_1": float(y_probe[5, -1]),
            "max_abs_phi": float(np.max(np.abs(sol.y[5]))),
            "max_abs_Tsn": float(np.max(np.abs(sol.y[1]))),
        }
    except Exception:
        return {}


def node_fractions(sol) -> tuple[float, float, float]:
    if not hasattr(sol, "x") or sol.x is None or len(sol.x) == 0:
        return float("nan"), float("nan"), float("nan")
    x = np.asarray(sol.x, dtype=float)
    n = float(len(x))
    return (
        float(np.count_nonzero(x > 0.99) / n),
        float(np.count_nonzero(x > 0.995) / n),
        float(np.count_nonzero(x > 0.999) / n),
    )


def predictor_correction_metrics(sol, seed: SeedSpec) -> tuple[float | None, float | None]:
    if not sol.success:
        return None, None
    try:
        corrected = sol.sol(seed.x_mesh)
        diff = corrected - seed.y_guess
        abs_corr = float(np.max(np.abs(diff)))
        scale = max(float(np.max(np.abs(corrected))), 1.0)
        rel_corr = abs_corr / scale
        return rel_corr, abs_corr
    except Exception:
        return None, None


def build_attempt_record(
    q_mpa: float,
    profile: SolverProfile,
    seed: SeedSpec,
    sol,
    attempt_seconds: float,
) -> AttemptRecord:
    max_rms = safe_max_rms(sol)
    max_bc = compute_bc_residual(sol)
    min_r = compute_min_r(sol)
    frac_099, frac_0995, frac_0999 = node_fractions(sol)
    min_dx, min_dx_mid, top_gradients = compute_gradient_diagnostics(sol)
    observables = compute_observables(sol, profile.config)
    predictor_rel_correction, predictor_abs_correction = predictor_correction_metrics(sol, seed)
    right_edge_layer = any(float(item.get("x_at_peak", 0.0)) > 0.99 for item in top_gradients)
    node_pressure = float(sol.x.size) / float(profile.config.max_nodes)
    mesh_pressure_only = (
        "maximum number of mesh nodes" in str(sol.message).lower()
        and (frac_0995 > 0.10 or right_edge_layer or node_pressure > 0.90)
    )
    branch_turning_suspicion = (
        not mesh_pressure_only
        and not sol.success
        and "maximum number of mesh nodes" not in str(sol.message).lower()
    )
    return AttemptRecord(
        q_mpa=float(q_mpa),
        profile_name=profile.name,
        seed_label=seed.label,
        success=bool(sol.success),
        attempt_seconds=float(attempt_seconds),
        message=str(sol.message),
        nodes=int(sol.x.size),
        max_nodes=int(profile.config.max_nodes),
        max_rms=max_rms,
        max_bc_residual=max_bc,
        min_r=min_r,
        node_pressure=node_pressure,
        right_edge_fraction_0_99=frac_099,
        right_edge_fraction_0_995=frac_0995,
        right_edge_fraction_0_999=frac_0999,
        min_dx=min_dx,
        min_dx_mid=min_dx_mid,
        top_gradients=top_gradients,
        observables=observables,
        mesh_pressure_only=mesh_pressure_only,
        right_edge_layer_suspicion=right_edge_layer,
        branch_turning_suspicion=branch_turning_suspicion,
        predictor_rel_correction=predictor_rel_correction,
        predictor_abs_correction=predictor_abs_correction,
    )


def build_branch_point(record: AttemptRecord, sol) -> BranchPoint:
    return BranchPoint(
        q_mpa=record.q_mpa,
        x=np.asarray(sol.x, dtype=float),
        y=np.asarray(sol.y, dtype=float),
        solution=sol,
        message=record.message,
        nodes=record.nodes,
        max_rms=record.max_rms,
        max_bc_residual=record.max_bc_residual,
        min_r=record.min_r,
        node_pressure=record.node_pressure,
        right_edge_fraction_0_99=record.right_edge_fraction_0_99,
        right_edge_fraction_0_995=record.right_edge_fraction_0_995,
        right_edge_fraction_0_999=record.right_edge_fraction_0_999,
        min_dx=record.min_dx,
        min_dx_mid=record.min_dx_mid,
        top_gradients=record.top_gradients,
        observables=record.observables,
        accepted_profile=record.profile_name,
        accepted_seed=record.seed_label,
        predictor_rel_correction=record.predictor_rel_correction,
        predictor_abs_correction=record.predictor_abs_correction,
    )


def make_seed_specs(
    q_target_mpa: float,
    older: BranchPoint | None,
    previous: BranchPoint,
    anchor: BranchPoint,
    profile: SolverProfile,
) -> list[SeedSpec]:
    seeds: list[SeedSpec] = []
    previous_mesh = previous.x
    if older is not None and abs(previous.q_mpa - older.q_mpa) > 1.0e-14:
        if older.solution is None:
            raise RuntimeError("Older branch point is missing its solve_bvp solution object.")
        older_on_previous = older.solution.sol(previous_mesh)
        secant = previous.y + ((q_target_mpa - previous.q_mpa) / (previous.q_mpa - older.q_mpa)) * (
            previous.y - older_on_previous
        )
        seeds.append(SeedSpec(label="secant_prev_mesh", x_mesh=previous_mesh, y_guess=secant))
    seeds.append(SeedSpec(label="previous_raw_mesh", x_mesh=previous_mesh, y_guess=previous.y))

    profile_mesh = default_x_mesh(profile.config)
    if older is not None and abs(previous.q_mpa - older.q_mpa) > 1.0e-14:
        if previous.solution is None or older.solution is None:
            raise RuntimeError("Secant profile seed needs both previous and older solve_bvp solutions.")
        previous_on_profile = previous.solution.sol(profile_mesh)
        older_on_profile = older.solution.sol(profile_mesh)
        secant_profile = previous_on_profile + (
            (q_target_mpa - previous.q_mpa) / (previous.q_mpa - older.q_mpa)
        ) * (previous_on_profile - older_on_profile)
        seeds.append(SeedSpec(label="secant_profile_mesh", x_mesh=profile_mesh, y_guess=secant_profile))

    if previous.solution is None or anchor.solution is None:
        raise RuntimeError("Previous and anchor branch points must carry solve_bvp solutions.")
    previous_profile = previous.solution.sol(profile_mesh)
    seeds.append(SeedSpec(label="previous_profile_mesh", x_mesh=profile_mesh, y_guess=previous_profile))

    anchor_profile = anchor.solution.sol(profile_mesh)
    seeds.append(SeedSpec(label="anchor_profile_mesh", x_mesh=profile_mesh, y_guess=anchor_profile))
    return seeds


def point_from_solution(
    q_mpa: float,
    profile_name: str,
    seed_label: str,
    config: AxisymmetricSimpleSupportConfig,
    sol,
) -> BranchPoint:
    profile = SolverProfile(profile_name, config, "")
    seed = SeedSpec(seed_label, np.asarray(sol.x, dtype=float), np.asarray(sol.y, dtype=float))
    record = build_attempt_record(q_mpa, profile, seed, sol, attempt_seconds=0.0)
    return build_branch_point(record, sol)


def solve_anchor_schedule(anchor_loads_mpa: tuple[float, ...]) -> list[BranchPoint]:
    anchor_config = AxisymmetricSimpleSupportConfig(
        nd_bvp=600,
        tol=2.0e-4,
        relaxed_tol=1.0e-3,
        max_nodes=240000,
    )
    anchor_mesh = default_x_mesh(anchor_config)
    template = build_template_solution(anchor_config)
    results: list[BranchPoint] = []
    previous = None

    for q_mpa in anchor_loads_mpa:
        if previous is None:
            result = solve_axisymmetric_simple_support_fixed_load(
                q_mpa,
                config=anchor_config,
                template_result=template,
            )
        else:
            if previous.solution is None:
                raise RuntimeError("Anchor branch point is missing its solve_bvp solution object.")
            guess = previous.solution.sol(anchor_mesh)
            result = solve_axisymmetric_simple_support_fixed_load(
                q_mpa,
                config=anchor_config,
                initial_guess=guess,
            )
        if not result.success or result.solution is None:
            raise RuntimeError(f"Anchor continuation failed at q={q_mpa:.4f} MPa: {result.message}")
        point = point_from_solution(
            q_mpa=q_mpa,
            profile_name="anchor_config",
            seed_label="template_or_previous_anchor",
            config=anchor_config,
            sol=result.solution,
        )
        results.append(point)
        previous = point
    return results


def solve_local_bootstrap(
    anchor_point: BranchPoint,
    bootstrap_profile: SolverProfile,
    bootstrap_loads_mpa: tuple[float, ...],
) -> tuple[list[BranchPoint], list[AttemptRecord]]:
    points: list[BranchPoint] = []
    attempts: list[AttemptRecord] = []
    local_mesh = default_x_mesh(bootstrap_profile.config)

    if anchor_point.solution is None:
        raise RuntimeError("Anchor branch point is missing its solve_bvp solution object.")
    first_seed = SeedSpec(
        label="anchor_projected_to_local_mesh",
        x_mesh=local_mesh,
        y_guess=anchor_point.solution.sol(local_mesh),
    )
    sol = run_bvp_attempt(anchor_point.q_mpa, first_seed.x_mesh, first_seed.y_guess, bootstrap_profile.config)
    record = build_attempt_record(anchor_point.q_mpa, bootstrap_profile, first_seed, sol, attempt_seconds=0.0)
    attempts.append(record)
    if not record.success:
        raise RuntimeError("Local bootstrap failed at the 4.335 MPa anchor projection.")
    first_point = build_branch_point(record, sol)
    points.append(first_point)

    older: BranchPoint | None = None
    previous = first_point
    for q_mpa in bootstrap_loads_mpa:
        point, point_attempts = try_profiles(
            q_target_mpa=q_mpa,
            older=older,
            previous=previous,
            anchor=first_point,
            profiles=[bootstrap_profile],
        )
        attempts.extend(point_attempts)
        if point is None:
            raise RuntimeError(f"Local bootstrap failed at q={q_mpa:.4f} MPa.")
        points.append(point)
        older, previous = previous, point

    return points, attempts


def try_profiles(
    q_target_mpa: float,
    older: BranchPoint | None,
    previous: BranchPoint,
    anchor: BranchPoint,
    profiles: list[SolverProfile],
) -> tuple[BranchPoint | None, list[AttemptRecord]]:
    all_attempts: list[AttemptRecord] = []
    for profile in profiles:
        for seed in make_seed_specs(q_target_mpa, older, previous, anchor, profile):
            attempt_start = time.perf_counter()
            sol = run_bvp_attempt(q_target_mpa, seed.x_mesh, seed.y_guess, profile.config)
            record = build_attempt_record(
                q_target_mpa,
                profile,
                seed,
                sol,
                attempt_seconds=time.perf_counter() - attempt_start,
            )
            all_attempts.append(record)
            if record.success:
                return build_branch_point(record, sol), all_attempts
    return None, all_attempts


def next_step_size(current_step: float, initial_step: float, accepted: BranchPoint) -> float:
    if accepted.node_pressure > 0.50 or accepted.accepted_profile != "strict_local":
        return current_step
    if accepted.predictor_rel_correction is not None and accepted.predictor_rel_correction < 5.0e-3:
        return min(initial_step, current_step * 1.25)
    return current_step


def diagnose_failures(
    attempts: list[AttemptRecord],
    accepted_points: list[BranchPoint],
) -> tuple[dict[str, Any], dict[str, Any]]:
    failures = [attempt for attempt in attempts if not attempt.success]
    mesh_pressure_failures = [attempt for attempt in failures if attempt.mesh_pressure_only]
    right_edge_failures = [attempt for attempt in failures if attempt.right_edge_layer_suspicion]
    turning_flags = [attempt for attempt in failures if attempt.branch_turning_suspicion]
    smooth_tail = accepted_points[-3:] if len(accepted_points) >= 3 else accepted_points

    tail_observables = [
        {
            "q_mpa": point.q_mpa,
            "phi_1": point.observables.get("phi_1"),
            "Tsn_1": point.observables.get("Tsn_1"),
            "predictor_rel_correction": point.predictor_rel_correction,
            "nodes": point.nodes,
        }
        for point in smooth_tail
    ]

    same_branch_beyond_previous = any(point.q_mpa > PREVIOUS_DOCUMENTED_CEILING_MPA for point in accepted_points)
    highest = accepted_points[-1].q_mpa if accepted_points else None
    first_failed_attempt = failures[0].q_mpa if failures else None

    failure_diagnosis = {
        "failure_count": len(failures),
        "mesh_pressure_failure_count": len(mesh_pressure_failures),
        "right_edge_layer_failure_count": len(right_edge_failures),
        "turning_suspicion_count": len(turning_flags),
        "mesh_pressure_dominant": bool(failures) and len(mesh_pressure_failures) == len(failures),
        "right_edge_layer_dominant": bool(failures) and len(right_edge_failures) == len(failures),
        "first_failed_attempt_q_mpa": first_failed_attempt,
        "last_failure_messages": [attempt.message for attempt in failures[-3:]],
        "last_failure_profiles": [attempt.profile_name for attempt in failures[-3:]],
        "last_failure_node_pressures": [attempt.node_pressure for attempt in failures[-3:]],
        "last_failure_top_gradients": [attempt.top_gradients for attempt in failures[-2:]],
    }
    branch_assessment = {
        "same_branch_continues_past_previous_ceiling": same_branch_beyond_previous,
        "highest_converged_q_mpa": highest,
        "smooth_tail_observables": tail_observables,
        "evidence_for_turning_or_branch_end": bool(turning_flags),
        "ten_mpa_reachable_on_present_evidence": False,
        "assessment_text": (
            "The branch continues smoothly beyond the previous pilot-09 ceiling if accepted points exceed "
            f"{PREVIOUS_DOCUMENTED_CEILING_MPA:.3f} MPa; current evidence supports that local statement only. "
            "The present evidence does not justify continuation all the way to 10 MPa on the same branch."
        ),
    }
    return failure_diagnosis, branch_assessment


def outcome_from_state(
    *,
    band_start_mpa: float,
    band_end_mpa: float,
    initial_step_mpa: float,
    min_step_mpa: float,
    budget_seconds: float,
    mode: str,
    anchor_points: list[BranchPoint],
    accepted_points: list[BranchPoint],
    all_attempts: list[AttemptRecord],
    first_failed_attempt_q_mpa: float | None,
    terminal_unresolved_q_mpa: float | None,
    elapsed_seconds: float,
    stopped_reason: str,
) -> CampaignOutcome:
    failure_diagnosis, branch_assessment = diagnose_failures(all_attempts, accepted_points)
    highest = accepted_points[-1].q_mpa if accepted_points else None
    band_reached = highest is not None and highest >= band_end_mpa - 1.0e-12
    progress_still_being_made = highest is not None and highest > PREVIOUS_DOCUMENTED_CEILING_MPA + 1.0e-12

    return CampaignOutcome(
        previous_documented_ceiling_mpa=PREVIOUS_DOCUMENTED_CEILING_MPA,
        previous_documented_failure_mpa=PREVIOUS_DOCUMENTED_FAILURE_MPA,
        band_start_mpa=float(band_start_mpa),
        band_end_mpa=float(band_end_mpa),
        initial_step_mpa=float(initial_step_mpa),
        min_step_mpa=float(min_step_mpa),
        budget_seconds=float(budget_seconds),
        mode=mode,
        anchor_loads_mpa=list(DEFAULT_ANCHOR_LOADS_MPA),
        bootstrap_loads_mpa=list(DEFAULT_LOCAL_BOOTSTRAP_LOADS_MPA),
        profiles=[
            {
                "name": profile.name,
                "description": profile.description,
                "config": asdict(profile.config),
            }
            for profile in make_profiles(mode)
        ],
        anchor_results=[
            {
                "q_mpa": point.q_mpa,
                "nodes": point.nodes,
                "max_rms": point.max_rms,
                "max_bc_residual": point.max_bc_residual,
                "min_r": point.min_r,
            }
            for point in anchor_points
        ],
        accepted_points=[
            {
                "q_mpa": point.q_mpa,
                "nodes": point.nodes,
                "max_rms": point.max_rms,
                "max_bc_residual": point.max_bc_residual,
                "min_r": point.min_r,
                "node_pressure": point.node_pressure,
                "right_edge_fraction_0_995": point.right_edge_fraction_0_995,
                "min_dx": point.min_dx,
                "min_dx_mid": point.min_dx_mid,
                "top_gradients": point.top_gradients,
                "observables": point.observables,
                "accepted_profile": point.accepted_profile,
                "accepted_seed": point.accepted_seed,
                "predictor_rel_correction": point.predictor_rel_correction,
                "predictor_abs_correction": point.predictor_abs_correction,
            }
            for point in accepted_points
        ],
        attempts=[asdict(attempt) for attempt in all_attempts],
        highest_converged_q_mpa=highest,
        first_failed_attempt_q_mpa=first_failed_attempt_q_mpa,
        terminal_unresolved_q_mpa=terminal_unresolved_q_mpa,
        elapsed_seconds=float(elapsed_seconds),
        stopped_reason=stopped_reason,
        band_reached=band_reached,
        progress_still_being_made=progress_still_being_made,
        failure_diagnosis=failure_diagnosis,
        branch_assessment=branch_assessment,
    )


def save_progress(
    progress_path: Path,
    *,
    band_start_mpa: float,
    band_end_mpa: float,
    initial_step_mpa: float,
    min_step_mpa: float,
    budget_seconds: float,
    mode: str,
    anchor_points: list[BranchPoint],
    accepted_points: list[BranchPoint],
    all_attempts: list[AttemptRecord],
    first_failed_attempt_q_mpa: float | None,
    terminal_unresolved_q_mpa: float | None,
    elapsed_seconds: float,
    stopped_reason: str,
) -> None:
    outcome = outcome_from_state(
        band_start_mpa=band_start_mpa,
        band_end_mpa=band_end_mpa,
        initial_step_mpa=initial_step_mpa,
        min_step_mpa=min_step_mpa,
        budget_seconds=budget_seconds,
        mode=mode,
        anchor_points=anchor_points,
        accepted_points=accepted_points,
        all_attempts=all_attempts,
        first_failed_attempt_q_mpa=first_failed_attempt_q_mpa,
        terminal_unresolved_q_mpa=terminal_unresolved_q_mpa,
        elapsed_seconds=elapsed_seconds,
        stopped_reason=stopped_reason,
    )
    progress_path.write_text(json.dumps(to_builtin(asdict(outcome)), indent=2), encoding="utf-8")


def run_campaign(
    band_start_mpa: float,
    band_end_mpa: float,
    initial_step_mpa: float,
    min_step_mpa: float,
    budget_seconds: float,
    mode: str,
    progress_json: Path,
) -> CampaignOutcome:
    start_time = time.perf_counter()
    profiles = make_profiles(mode)
    anchor_points = solve_anchor_schedule(DEFAULT_ANCHOR_LOADS_MPA)
    anchor = anchor_points[-1]
    accepted_points, all_attempts = solve_local_bootstrap(
        anchor_point=anchor,
        bootstrap_profile=profiles[0],
        bootstrap_loads_mpa=DEFAULT_LOCAL_BOOTSTRAP_LOADS_MPA,
    )

    older: BranchPoint | None = accepted_points[-2] if len(accepted_points) >= 2 else None
    previous = accepted_points[-1]
    current_step = initial_step_mpa
    first_failed_attempt_q_mpa: float | None = None
    terminal_unresolved_q_mpa: float | None = None
    stopped_reason = "band_not_started"
    save_progress(
        progress_json,
        band_start_mpa=band_start_mpa,
        band_end_mpa=band_end_mpa,
        initial_step_mpa=initial_step_mpa,
        min_step_mpa=min_step_mpa,
        budget_seconds=budget_seconds,
        mode=mode,
        anchor_points=anchor_points,
        accepted_points=accepted_points,
        all_attempts=all_attempts,
        first_failed_attempt_q_mpa=first_failed_attempt_q_mpa,
        terminal_unresolved_q_mpa=terminal_unresolved_q_mpa,
        elapsed_seconds=time.perf_counter() - start_time,
        stopped_reason="bootstrap_complete",
    )

    if previous.q_mpa < band_start_mpa - 1.0e-12:
        stopped_reason = "did_not_reach_band_start"
        return outcome_from_state(
            band_start_mpa=band_start_mpa,
            band_end_mpa=band_end_mpa,
            initial_step_mpa=initial_step_mpa,
            min_step_mpa=min_step_mpa,
            budget_seconds=budget_seconds,
            mode=mode,
            anchor_points=anchor_points,
            accepted_points=accepted_points,
            all_attempts=all_attempts,
            first_failed_attempt_q_mpa=first_failed_attempt_q_mpa,
            terminal_unresolved_q_mpa=terminal_unresolved_q_mpa,
            elapsed_seconds=time.perf_counter() - start_time,
            stopped_reason=stopped_reason,
        )

    stopped_reason = "band_complete"
    while previous.q_mpa < band_end_mpa:
        if time.perf_counter() - start_time >= budget_seconds:
            stopped_reason = "budget_exhausted"
            break
        q_target = min(band_end_mpa, previous.q_mpa + current_step)
        point, attempts = try_profiles(q_target, older, previous, accepted_points[0], profiles)
        all_attempts.extend(attempts)

        if point is not None:
            older, previous = previous, point
            accepted_points.append(point)
            current_step = next_step_size(current_step, initial_step_mpa, point)
            last_attempt_seconds = attempts[-1].attempt_seconds if attempts else 0.0
            if last_attempt_seconds >= max(60.0, 0.25 * budget_seconds):
                stopped_reason = "slow_attempt_detected"
                save_progress(
                    progress_json,
                    band_start_mpa=band_start_mpa,
                    band_end_mpa=band_end_mpa,
                    initial_step_mpa=initial_step_mpa,
                    min_step_mpa=min_step_mpa,
                    budget_seconds=budget_seconds,
                    mode=mode,
                    anchor_points=anchor_points,
                    accepted_points=accepted_points,
                    all_attempts=all_attempts,
                    first_failed_attempt_q_mpa=first_failed_attempt_q_mpa,
                    terminal_unresolved_q_mpa=terminal_unresolved_q_mpa,
                    elapsed_seconds=time.perf_counter() - start_time,
                    stopped_reason=stopped_reason,
                )
                break
            save_progress(
                progress_json,
                band_start_mpa=band_start_mpa,
                band_end_mpa=band_end_mpa,
                initial_step_mpa=initial_step_mpa,
                min_step_mpa=min_step_mpa,
                budget_seconds=budget_seconds,
                mode=mode,
                anchor_points=anchor_points,
                accepted_points=accepted_points,
                all_attempts=all_attempts,
                first_failed_attempt_q_mpa=first_failed_attempt_q_mpa,
                terminal_unresolved_q_mpa=terminal_unresolved_q_mpa,
                elapsed_seconds=time.perf_counter() - start_time,
                stopped_reason="progress_saved_after_success",
            )
            continue

        if first_failed_attempt_q_mpa is None:
            first_failed_attempt_q_mpa = q_target

        if current_step <= min_step_mpa + 1.0e-14:
            terminal_unresolved_q_mpa = q_target
            stopped_reason = "min_step_reached_after_failure"
            save_progress(
                progress_json,
                band_start_mpa=band_start_mpa,
                band_end_mpa=band_end_mpa,
                initial_step_mpa=initial_step_mpa,
                min_step_mpa=min_step_mpa,
                budget_seconds=budget_seconds,
                mode=mode,
                anchor_points=anchor_points,
                accepted_points=accepted_points,
                all_attempts=all_attempts,
                first_failed_attempt_q_mpa=first_failed_attempt_q_mpa,
                terminal_unresolved_q_mpa=terminal_unresolved_q_mpa,
                elapsed_seconds=time.perf_counter() - start_time,
                stopped_reason=stopped_reason,
            )
            break

        current_step = max(min_step_mpa, 0.5 * current_step)
        save_progress(
            progress_json,
            band_start_mpa=band_start_mpa,
            band_end_mpa=band_end_mpa,
            initial_step_mpa=initial_step_mpa,
            min_step_mpa=min_step_mpa,
            budget_seconds=budget_seconds,
            mode=mode,
            anchor_points=anchor_points,
            accepted_points=accepted_points,
            all_attempts=all_attempts,
            first_failed_attempt_q_mpa=first_failed_attempt_q_mpa,
            terminal_unresolved_q_mpa=terminal_unresolved_q_mpa,
            elapsed_seconds=time.perf_counter() - start_time,
            stopped_reason="progress_saved_after_failure_retry",
        )

    return outcome_from_state(
        band_start_mpa=band_start_mpa,
        band_end_mpa=band_end_mpa,
        initial_step_mpa=initial_step_mpa,
        min_step_mpa=min_step_mpa,
        budget_seconds=budget_seconds,
        mode=mode,
        anchor_points=anchor_points,
        accepted_points=accepted_points,
        all_attempts=all_attempts,
        first_failed_attempt_q_mpa=first_failed_attempt_q_mpa,
        terminal_unresolved_q_mpa=terminal_unresolved_q_mpa,
        elapsed_seconds=time.perf_counter() - start_time,
        stopped_reason=stopped_reason,
    )


def to_builtin(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): to_builtin(val) for key, val in value.items()}
    if isinstance(value, list):
        return [to_builtin(item) for item in value]
    if isinstance(value, tuple):
        return [to_builtin(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.floating):
        return None if not math.isfinite(float(value)) else float(value)
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, float):
        return None if not math.isfinite(value) else value
    return value


def print_summary(outcome: CampaignOutcome) -> None:
    print("=== Pilot 10: High-load simple-support continuation campaign ===")
    print()
    print(
        f"Previous documented ceiling: {outcome.previous_documented_ceiling_mpa:.4f} MPa; "
        f"first documented failure: {outcome.previous_documented_failure_mpa:.4f} MPa"
    )
    print(
        f"Campaign mode: {outcome.mode}  band={outcome.band_start_mpa:.3f}..{outcome.band_end_mpa:.3f} MPa  "
        f"initial_step={outcome.initial_step_mpa:.5f} MPa  min_step={outcome.min_step_mpa:.5f} MPa  "
        f"budget={outcome.budget_seconds:.0f}s"
    )
    print()
    print("Profiles:")
    for profile in outcome.profiles:
        config = profile["config"]
        print(
            f"  {profile['name']}: nd_bvp={config['nd_bvp']}, tol={config['tol']:.1e}, "
            f"relaxed_tol={config['relaxed_tol']:.1e}, max_nodes={config['max_nodes']}, "
            f"cluster_start={config['right_edge_cluster_start']:.3f}, "
            f"cluster_fraction={config['right_edge_cluster_fraction']:.2f}, "
            f"cluster_power={config['right_edge_cluster_power']:.2f}"
        )
    print()
    print("Accepted branch points:")
    for point in outcome.accepted_points:
        grads = ", ".join(
            f"{item['state']}@x={item['x_at_peak']:.5f} ({item['max_abs_grad']:.3e})"
            for item in point["top_gradients"]
        )
        pred_rel = point["predictor_rel_correction"]
        pred_rel_text = "nan" if pred_rel is None else f"{pred_rel:.3e}"
        print(
            f"  q={point['q_mpa']:.5f} MPa  profile={point['accepted_profile']}  seed={point['accepted_seed']}  "
            f"nodes={point['nodes']}  max_rms={point['max_rms']:.3e}  max_bc={point['max_bc_residual']:.3e}  "
            f"node_pressure={point['node_pressure']:.3f}  x>0.995={point['right_edge_fraction_0_995']:.3f}  "
            f"predictor_rel_corr={pred_rel_text}"
        )
        print(f"    top gradients: {grads}")
    print()
    failed_attempts = [attempt for attempt in outcome.attempts if not attempt["success"]]
    if failed_attempts:
        print("Last failed attempts:")
        for attempt in failed_attempts[-3:]:
            grads = ", ".join(
                f"{item['state']}@x={item['x_at_peak']:.5f} ({item['max_abs_grad']:.3e})"
                for item in attempt["top_gradients"]
            )
            print(
                f"  q={attempt['q_mpa']:.5f} MPa  profile={attempt['profile_name']}  seed={attempt['seed_label']}  "
                f"nodes={attempt['nodes']}/{attempt['max_nodes']} ({attempt['node_pressure']:.3f})  "
                f"max_bc={attempt['max_bc_residual']:.3e}  message={attempt['message']}"
            )
            print(f"    top gradients: {grads}")
    print()
    print(f"Highest converged load: {outcome.highest_converged_q_mpa}")
    print(f"First failed attempted load: {outcome.first_failed_attempt_q_mpa}")
    print(f"Terminal unresolved load: {outcome.terminal_unresolved_q_mpa}")
    print(f"Elapsed seconds: {outcome.elapsed_seconds:.1f}")
    print(f"Stopped reason: {outcome.stopped_reason}")
    print(f"Band reached: {outcome.band_reached}")
    print(f"Progress still being made: {outcome.progress_still_being_made}")
    print(
        "Failure diagnosis: "
        f"mesh_pressure_dominant={outcome.failure_diagnosis['mesh_pressure_dominant']}, "
        f"right_edge_layer_dominant={outcome.failure_diagnosis['right_edge_layer_dominant']}, "
        f"turning_suspicion_count={outcome.failure_diagnosis['turning_suspicion_count']}"
    )
    print(
        "Branch assessment: "
        f"same_branch_past_previous_ceiling={outcome.branch_assessment['same_branch_continues_past_previous_ceiling']}, "
        f"evidence_for_turning_or_branch_end={outcome.branch_assessment['evidence_for_turning_or_branch_end']}, "
        f"ten_mpa_reachable_on_present_evidence={outcome.branch_assessment['ten_mpa_reachable_on_present_evidence']}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the pilot-10 high-load continuation campaign for the 6-state simple-support background."
    )
    parser.add_argument("--band-start-mpa", type=float, required=True)
    parser.add_argument("--band-end-mpa", type=float, required=True)
    parser.add_argument("--initial-step-mpa", type=float, default=1.0e-3)
    parser.add_argument("--min-step-mpa", type=float, default=5.0e-5)
    parser.add_argument("--budget-seconds", type=float, default=900.0)
    parser.add_argument("--mode", choices=("strict", "rescue"), default="rescue")
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    outcome = run_campaign(
        band_start_mpa=float(args.band_start_mpa),
        band_end_mpa=float(args.band_end_mpa),
        initial_step_mpa=float(args.initial_step_mpa),
        min_step_mpa=float(args.min_step_mpa),
        budget_seconds=float(args.budget_seconds),
        mode=str(args.mode),
        progress_json=args.output_json,
    )
    payload = to_builtin(asdict(outcome))
    args.output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print_summary(outcome)
    print()
    print(f"JSON log written to: {args.output_json}")


if __name__ == "__main__":
    main()
