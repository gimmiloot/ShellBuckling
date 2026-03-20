from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

import numpy as np
from scipy.integrate import solve_bvp


nu = 0.3
E = 205e9
h = 0.005
a = 0.5
mu = a / h

STATE_LABELS = ("T_s", "T_sn", "M_s", "u_r", "u_z", "varphi")
BC_LABELS = (
    "T_s(1)=0",
    "M_s(1)=0",
    "u_z(1)=0",
    "T_sn(x0)=0",
    "u_r(x0)=0",
    "varphi(x0)=0",
)
DEFAULT_FIXED_LOADS_MPA = (0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 4.2, 4.3, 4.33)
DEFAULT_CONTINUATION_LOADS_MPA = (0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 4.2, 4.3, 4.33)
DEFAULT_LOCAL_BRANCH_ANCHOR_LOADS_MPA = (4.30, 4.325, 4.3275, 4.328, 4.329, 4.330, 4.332, 4.335)
DEFAULT_LOCAL_BRANCH_LOADS_MPA = (4.335, 4.336, 4.337, 4.338, 4.339, 4.340, 4.341, 4.342, 4.343, 4.344)


@dataclass(frozen=True)
class AxisymmetricSimpleSupportConfig:
    x0: float = 1.0 / 600.0
    nd_bvp: int = 600
    tol: float = 1.0e-4
    relaxed_tol: float = 5.0e-4
    max_nodes: int = 120000
    template_q_mpa: float = 0.5
    right_edge_cluster_start: float = 1.0
    right_edge_cluster_fraction: float = 0.0
    right_edge_cluster_power: float = 1.0


@dataclass
class AxisymmetricBackgroundSolve:
    q_mpa: float
    success: bool
    message: str
    nodes: int
    max_rms: float
    seed_kind: str
    max_bc_residual: float
    min_r: float
    solution: Any | None = None

    def summary_line(self) -> str:
        rms_text = f"{self.max_rms:.2e}" if np.isfinite(self.max_rms) else "nan"
        bc_text = f"{self.max_bc_residual:.2e}" if np.isfinite(self.max_bc_residual) else "nan"
        min_r_text = f"{self.min_r:.6f}" if np.isfinite(self.min_r) else "nan"
        return (
            f"q={self.q_mpa:.2f} MPa  success={self.success}  seed={self.seed_kind}  "
            f"nodes={self.nodes}  max_rms={rms_text}  max_bc={bc_text}  min(r)={min_r_text}  "
            f"message={self.message}"
        )


@dataclass(frozen=True)
class AxisymmetricLocalBranchFollowConfig:
    anchor_config: AxisymmetricSimpleSupportConfig = field(
        default_factory=lambda: AxisymmetricSimpleSupportConfig(
            nd_bvp=600,
            tol=2.0e-4,
            relaxed_tol=1.0e-3,
            max_nodes=240000,
        )
    )
    strict_local_config: AxisymmetricSimpleSupportConfig = field(
        default_factory=lambda: AxisymmetricSimpleSupportConfig(
            nd_bvp=950,
            tol=2.0e-4,
            relaxed_tol=1.0e-3,
            max_nodes=350000,
            right_edge_cluster_start=0.965,
            right_edge_cluster_fraction=0.60,
            right_edge_cluster_power=1.8,
        )
    )
    relaxed_local_config: AxisymmetricSimpleSupportConfig = field(
        default_factory=lambda: AxisymmetricSimpleSupportConfig(
            nd_bvp=950,
            tol=2.5e-4,
            relaxed_tol=1.2e-3,
            max_nodes=350000,
            right_edge_cluster_start=0.965,
            right_edge_cluster_fraction=0.60,
            right_edge_cluster_power=1.8,
        )
    )
    anchor_loads_mpa: tuple[float, ...] = DEFAULT_LOCAL_BRANCH_ANCHOR_LOADS_MPA
    local_loads_mpa: tuple[float, ...] = DEFAULT_LOCAL_BRANCH_LOADS_MPA


@dataclass
class AxisymmetricLocalBranchStep:
    q_mpa: float
    success: bool
    config_label: str
    seed_labels: tuple[str, ...]
    accepted_seed_kind: str
    nodes: int
    max_rms: float
    max_bc_residual: float
    min_r: float
    message: str
    solution: Any | None = None

    def summary_line(self) -> str:
        rms_text = f"{self.max_rms:.2e}" if np.isfinite(self.max_rms) else "nan"
        bc_text = f"{self.max_bc_residual:.2e}" if np.isfinite(self.max_bc_residual) else "nan"
        min_r_text = f"{self.min_r:.6f}" if np.isfinite(self.min_r) else "nan"
        seeds = " -> ".join(self.seed_labels)
        return (
            f"q={self.q_mpa:.4f} MPa  success={self.success}  config={self.config_label}  "
            f"accepted_seed={self.accepted_seed_kind}  seeds={seeds}  nodes={self.nodes}  "
            f"max_rms={rms_text}  max_bc={bc_text}  min(r)={min_r_text}  message={self.message}"
        )


@dataclass
class AxisymmetricLocalBranchHistory:
    anchor_results: list[AxisymmetricBackgroundSolve]
    local_steps: list[AxisymmetricLocalBranchStep]

    def last_local_success(self) -> float | None:
        success = [step.q_mpa for step in self.local_steps if step.success]
        return success[-1] if success else None

    def first_local_failure(self) -> float | None:
        return next((step.q_mpa for step in self.local_steps if not step.success), None)


def axisymmetric_simple_support_ode(x: np.ndarray, y: np.ndarray, q_pa: float) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    x_safe = np.maximum(x, 1.0e-12)

    Ts, Tsn, Ms, ur, uz, phi = y

    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        r = x_safe + ur
        etheta = ur / x_safe
        es = Ts * (1.0 - nu**2) - nu * etheta
        Ttheta = nu * Ts + etheta
        kappa_s = 12.0 * (1.0 - nu**2) * Ms * mu**2 - nu * (np.sin(phi) / r)
        Mtheta = nu * Ms + np.sin(phi) / (12.0 * mu**2 * r)
        qbar = q_pa * a / (E * h)

        return np.vstack(
            (
                -(Ts / r) + (np.cos(phi) * Ttheta) / r - kappa_s * Tsn,
                -(Tsn / r) + (np.sin(phi) * Ttheta) / r + kappa_s * Ts - qbar,
                -(Ms / r) + (np.cos(phi) * Mtheta) / r + Tsn,
                (1.0 + es) * np.cos(phi) - 1.0,
                -mu * (1.0 + es) * np.sin(phi),
                kappa_s,
            )
        )


def axisymmetric_simple_support_bc(ya: np.ndarray, yb: np.ndarray) -> np.ndarray:
    return np.array([yb[0], yb[2], yb[4], ya[1], ya[3], ya[5]], dtype=float)


def default_x_mesh(config: AxisymmetricSimpleSupportConfig) -> np.ndarray:
    n_pts = int(config.nd_bvp)
    x0 = float(config.x0)

    if (
        config.right_edge_cluster_fraction <= 0.0
        or config.right_edge_cluster_start >= 1.0
        or config.right_edge_cluster_power <= 1.0
    ):
        return np.linspace(x0, 1.0, n_pts)

    split = min(max(float(config.right_edge_cluster_start), x0 + 1.0e-6), 0.999999)
    n_right = max(10, int(round(float(config.right_edge_cluster_fraction) * n_pts)))
    n_right = min(max(10, n_right), max(10, n_pts - 1))
    n_left = max(2, n_pts - n_right + 1)

    left = np.linspace(x0, split, n_left, endpoint=False)
    s = np.linspace(0.0, 1.0, n_right)
    right = split + (1.0 - split) * (1.0 - (1.0 - s) ** float(config.right_edge_cluster_power))

    x_mesh = np.unique(np.concatenate([left, right]))
    if x_mesh[0] > x0:
        x_mesh = np.insert(x_mesh, 0, x0)
    if x_mesh[-1] < 1.0:
        x_mesh = np.append(x_mesh, 1.0)
    return x_mesh


def zero_guess(x_mesh: np.ndarray) -> np.ndarray:
    return np.zeros((len(STATE_LABELS), x_mesh.size), dtype=float)


def _run_bvp_attempt(
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


def _summarize_solution(q_mpa: float, sol, x_mesh: np.ndarray, seed_kind: str) -> AxisymmetricBackgroundSolve:
    if sol.success:
        yv = sol.sol(x_mesh)
        r = x_mesh + yv[3]
        bc_residual = axisymmetric_simple_support_bc(yv[:, 0], yv[:, -1])
        max_rms = float(np.max(sol.rms_residuals)) if hasattr(sol, "rms_residuals") else float("nan")
        max_bc = float(np.max(np.abs(bc_residual)))
        min_r = float(np.min(r))
    else:
        max_rms = float("nan")
        max_bc = float("nan")
        min_r = float("nan")

    return AxisymmetricBackgroundSolve(
        q_mpa=float(q_mpa),
        success=bool(sol.success),
        message=sol.message,
        nodes=int(sol.x.size),
        max_rms=max_rms,
        seed_kind=seed_kind,
        max_bc_residual=max_bc,
        min_r=min_r,
        solution=sol if sol.success else None,
    )


def _attempt_sequence(
    q_mpa: float,
    x_mesh: np.ndarray,
    attempts: Sequence[tuple[str, np.ndarray]],
    config: AxisymmetricSimpleSupportConfig,
) -> AxisymmetricBackgroundSolve:
    tried: list[str] = []
    last_result: AxisymmetricBackgroundSolve | None = None
    for seed_kind, guess in attempts:
        tried.append(seed_kind)
        sol = _run_bvp_attempt(q_mpa, x_mesh, guess, config)
        result = _summarize_solution(q_mpa, sol, x_mesh, seed_kind=seed_kind)
        if result.success:
            return result
        last_result = result

    if last_result is None:
        raise RuntimeError("No solve attempts were prepared.")

    return AxisymmetricBackgroundSolve(
        q_mpa=last_result.q_mpa,
        success=False,
        message=last_result.message,
        nodes=last_result.nodes,
        max_rms=last_result.max_rms,
        seed_kind=" -> ".join(tried),
        max_bc_residual=last_result.max_bc_residual,
        min_r=last_result.min_r,
        solution=None,
    )


def build_template_solution(
    config: AxisymmetricSimpleSupportConfig = AxisymmetricSimpleSupportConfig(),
) -> AxisymmetricBackgroundSolve:
    x_mesh = default_x_mesh(config)
    result = _attempt_sequence(
        config.template_q_mpa,
        x_mesh,
        [("zero_guess", zero_guess(x_mesh))],
        config,
    )
    if not result.success:
        raise RuntimeError(
            "Template simple-support fixed-load solve failed at "
            f"q={config.template_q_mpa:.2f} MPa: {result.message}"
        )
    return result


def scaled_template_guess(
    q_mpa: float,
    x_mesh: np.ndarray,
    template_result: AxisymmetricBackgroundSolve,
    config: AxisymmetricSimpleSupportConfig,
) -> np.ndarray:
    if template_result.solution is None:
        raise ValueError("Template result has no converged solution.")
    scale = float(q_mpa) / float(config.template_q_mpa)
    return template_result.solution.sol(x_mesh) * scale


def _clone_result(result: AxisymmetricBackgroundSolve, seed_kind: str) -> AxisymmetricBackgroundSolve:
    return AxisymmetricBackgroundSolve(
        q_mpa=result.q_mpa,
        success=result.success,
        message=result.message,
        nodes=result.nodes,
        max_rms=result.max_rms,
        seed_kind=seed_kind,
        max_bc_residual=result.max_bc_residual,
        min_r=result.min_r,
        solution=result.solution,
    )


def solve_axisymmetric_simple_support_fixed_load(
    q_mpa: float,
    config: AxisymmetricSimpleSupportConfig = AxisymmetricSimpleSupportConfig(),
    template_result: AxisymmetricBackgroundSolve | None = None,
    initial_guess: np.ndarray | None = None,
) -> AxisymmetricBackgroundSolve:
    x_mesh = default_x_mesh(config)

    if initial_guess is not None:
        attempts = [("provided_guess", np.asarray(initial_guess, dtype=float))]
        return _attempt_sequence(q_mpa, x_mesh, attempts, config)

    if abs(float(q_mpa)) < 1.0e-14:
        return _attempt_sequence(q_mpa, x_mesh, [("zero_guess", zero_guess(x_mesh))], config)

    if template_result is None:
        template_result = build_template_solution(config)
    if abs(float(q_mpa) - float(config.template_q_mpa)) < 1.0e-14:
        return _clone_result(template_result, seed_kind="template_solution")

    attempts = [
        ("scaled_template", scaled_template_guess(q_mpa, x_mesh, template_result, config)),
        ("zero_guess", zero_guess(x_mesh)),
    ]
    return _attempt_sequence(q_mpa, x_mesh, attempts, config)


def solve_fixed_load_schedule(
    q_values_mpa: Sequence[float],
    config: AxisymmetricSimpleSupportConfig = AxisymmetricSimpleSupportConfig(),
) -> list[AxisymmetricBackgroundSolve]:
    results: list[AxisymmetricBackgroundSolve] = []
    template_result: AxisymmetricBackgroundSolve | None = None
    need_template = any(abs(float(q)) > 1.0e-14 for q in q_values_mpa)
    if need_template:
        template_result = build_template_solution(config)

    for q_mpa in q_values_mpa:
        result = solve_axisymmetric_simple_support_fixed_load(
            q_mpa,
            config=config,
            template_result=template_result,
        )
        results.append(result)

    return results


def solve_axisymmetric_simple_support_continuation(
    q_values_mpa: Sequence[float],
    config: AxisymmetricSimpleSupportConfig = AxisymmetricSimpleSupportConfig(),
) -> list[AxisymmetricBackgroundSolve]:
    if not q_values_mpa:
        return []

    x_mesh = default_x_mesh(config)
    results: list[AxisymmetricBackgroundSolve] = []
    template_result = build_template_solution(config)
    previous_solution = None

    for q_mpa in q_values_mpa:
        q_mpa = float(q_mpa)

        if abs(q_mpa) < 1.0e-14:
            result = _attempt_sequence(q_mpa, x_mesh, [("zero_guess", zero_guess(x_mesh))], config)
        elif previous_solution is None and abs(q_mpa - float(config.template_q_mpa)) < 1.0e-14:
            result = _clone_result(template_result, seed_kind="template_solution")
        else:
            attempts: list[tuple[str, np.ndarray]] = []
            if previous_solution is not None:
                attempts.append(("previous_solution", previous_solution.sol(x_mesh)))
            attempts.append(("scaled_template", scaled_template_guess(q_mpa, x_mesh, template_result, config)))
            attempts.append(("zero_guess", zero_guess(x_mesh)))
            result = _attempt_sequence(q_mpa, x_mesh, attempts, config)

        results.append(result)
        if not result.success:
            break
        previous_solution = result.solution

    return results



def _secant_predictor_guess(
    q_target_mpa: float,
    x_mesh: np.ndarray,
    previous_step: AxisymmetricLocalBranchStep,
    older_step: AxisymmetricLocalBranchStep,
) -> np.ndarray | None:
    if previous_step.solution is None or older_step.solution is None:
        return None
    dq = previous_step.q_mpa - older_step.q_mpa
    if abs(dq) < 1.0e-14:
        return None
    y_prev = previous_step.solution.sol(x_mesh)
    y_old = older_step.solution.sol(x_mesh)
    return y_prev + ((float(q_target_mpa) - previous_step.q_mpa) / dq) * (y_prev - y_old)


def _local_step_from_result(
    q_mpa: float,
    config_label: str,
    seed_labels: Sequence[str],
    result: AxisymmetricBackgroundSolve,
) -> AxisymmetricLocalBranchStep:
    return AxisymmetricLocalBranchStep(
        q_mpa=float(q_mpa),
        success=result.success,
        config_label=config_label,
        seed_labels=tuple(seed_labels),
        accepted_seed_kind=result.seed_kind,
        nodes=result.nodes,
        max_rms=result.max_rms,
        max_bc_residual=result.max_bc_residual,
        min_r=result.min_r,
        message=result.message,
        solution=result.solution,
    )


def _run_local_branch_step(
    q_mpa: float,
    x_mesh: np.ndarray,
    attempts: Sequence[tuple[str, np.ndarray]],
    strict_config: AxisymmetricSimpleSupportConfig,
    relaxed_config: AxisymmetricSimpleSupportConfig,
) -> AxisymmetricLocalBranchStep:
    seed_labels = [label for label, _ in attempts]

    strict_result = _attempt_sequence(q_mpa, x_mesh, attempts, strict_config)
    if strict_result.success:
        return _local_step_from_result(q_mpa, "strict_local", seed_labels, strict_result)

    relaxed_result = _attempt_sequence(q_mpa, x_mesh, attempts, relaxed_config)
    return _local_step_from_result(q_mpa, "relaxed_local", seed_labels, relaxed_result)


def solve_axisymmetric_simple_support_local_branch_following(
    config: AxisymmetricLocalBranchFollowConfig = AxisymmetricLocalBranchFollowConfig(),
) -> AxisymmetricLocalBranchHistory:
    anchor_results: list[AxisymmetricBackgroundSolve] = []
    anchor_template = build_template_solution(config.anchor_config)
    anchor_mesh = default_x_mesh(config.anchor_config)
    previous_anchor: AxisymmetricBackgroundSolve | None = None

    for q_mpa in config.anchor_loads_mpa:
        if previous_anchor is None:
            result = solve_axisymmetric_simple_support_fixed_load(
                q_mpa,
                config=config.anchor_config,
                template_result=anchor_template,
            )
        else:
            result = solve_axisymmetric_simple_support_fixed_load(
                q_mpa,
                config=config.anchor_config,
                initial_guess=previous_anchor.solution.sol(anchor_mesh),
            )
        anchor_results.append(result)
        if not result.success:
            return AxisymmetricLocalBranchHistory(anchor_results=anchor_results, local_steps=[])
        previous_anchor = result

    if previous_anchor is None or previous_anchor.solution is None:
        return AxisymmetricLocalBranchHistory(anchor_results=anchor_results, local_steps=[])

    local_steps: list[AxisymmetricLocalBranchStep] = []
    local_mesh = default_x_mesh(config.strict_local_config)
    local_loads = list(config.local_loads_mpa)
    if not local_loads:
        return AxisymmetricLocalBranchHistory(anchor_results=anchor_results, local_steps=local_steps)

    anchor_q = float(previous_anchor.q_mpa)
    if abs(local_loads[0] - anchor_q) > 1.0e-12:
        local_loads.insert(0, anchor_q)

    anchor_attempts = [("uniform_anchor_projection", previous_anchor.solution.sol(local_mesh))]
    anchor_step = _run_local_branch_step(
        local_loads[0],
        local_mesh,
        anchor_attempts,
        config.strict_local_config,
        config.relaxed_local_config,
    )
    local_steps.append(anchor_step)
    if not anchor_step.success:
        return AxisymmetricLocalBranchHistory(anchor_results=anchor_results, local_steps=local_steps)

    older_step: AxisymmetricLocalBranchStep | None = None
    previous_step = anchor_step

    for q_mpa in local_loads[1:]:
        attempts: list[tuple[str, np.ndarray]] = []
        if older_step is not None:
            secant_guess = _secant_predictor_guess(q_mpa, local_mesh, previous_step, older_step)
            if secant_guess is not None:
                attempts.append(("secant_predictor", secant_guess))
        if previous_step.solution is not None:
            attempts.append(("previous_solution", previous_step.solution.sol(local_mesh)))
        attempts.append(("local_anchor", anchor_step.solution.sol(local_mesh)))

        step = _run_local_branch_step(
            q_mpa,
            local_mesh,
            attempts,
            config.strict_local_config,
            config.relaxed_local_config,
        )
        local_steps.append(step)
        if not step.success:
            break
        older_step, previous_step = previous_step, step

    return AxisymmetricLocalBranchHistory(anchor_results=anchor_results, local_steps=local_steps)


def summarize_results(results: Sequence[AxisymmetricBackgroundSolve]) -> tuple[list[float], float | None, float | None]:
    success_loads = [result.q_mpa for result in results if result.success]
    last_success = success_loads[-1] if success_loads else None
    first_failure = next((result.q_mpa for result in results if not result.success), None)
    return success_loads, last_success, first_failure


def print_result_block(title: str, results: Sequence[AxisymmetricBackgroundSolve]) -> None:
    print(title)
    for result in results:
        print(f"  {result.summary_line()}")
    success_loads, last_success, first_failure = summarize_results(results)
    print(f"  success loads: {success_loads}")
    print(f"  last success: {last_success}")
    print(f"  first failure: {first_failure}")
    print()


def print_local_branch_result_block(title: str, results: Sequence[AxisymmetricLocalBranchStep]) -> None:
    print(title)
    for result in results:
        print(f"  {result.summary_line()}")
    success_loads = [result.q_mpa for result in results if result.success]
    last_success = success_loads[-1] if success_loads else None
    first_failure = next((result.q_mpa for result in results if not result.success), None)
    print(f"  success loads: {success_loads}")
    print(f"  last success: {last_success}")
    print(f"  first failure: {first_failure}")
    print()


def report_main() -> None:
    config = AxisymmetricSimpleSupportConfig()
    fixed_results = solve_fixed_load_schedule(DEFAULT_FIXED_LOADS_MPA, config=config)
    continuation_results = solve_axisymmetric_simple_support_continuation(DEFAULT_CONTINUATION_LOADS_MPA, config=config)

    print("=== Full-state axisymmetric simple-support background report ===")
    print(f"state: {list(STATE_LABELS)}")
    print(f"BCs:   {list(BC_LABELS)}")
    print(f"config: x0={config.x0:.6f}, nd_bvp={config.nd_bvp}, tol={config.tol:.1e}, max_nodes={config.max_nodes}")
    print()
    print_result_block("Fixed-load schedule", fixed_results)
    print_result_block("Continuation schedule", continuation_results)


def report_local_branch_following_main() -> None:
    config = AxisymmetricLocalBranchFollowConfig()
    history = solve_axisymmetric_simple_support_local_branch_following(config=config)

    print("=== Full-state simple-support local branch-following report ===")
    print(f"state: {list(STATE_LABELS)}")
    print(f"BCs:   {list(BC_LABELS)}")
    print(
        "anchor config: "
        f"nd_bvp={config.anchor_config.nd_bvp}, tol={config.anchor_config.tol:.1e}, "
        f"relaxed_tol={config.anchor_config.relaxed_tol:.1e}, max_nodes={config.anchor_config.max_nodes}"
    )
    print(
        "strict local config: "
        f"nd_bvp={config.strict_local_config.nd_bvp}, tol={config.strict_local_config.tol:.1e}, "
        f"relaxed_tol={config.strict_local_config.relaxed_tol:.1e}, max_nodes={config.strict_local_config.max_nodes}, "
        f"right_edge_cluster_start={config.strict_local_config.right_edge_cluster_start:.3f}, "
        f"right_edge_cluster_fraction={config.strict_local_config.right_edge_cluster_fraction:.2f}, "
        f"right_edge_cluster_power={config.strict_local_config.right_edge_cluster_power:.2f}"
    )
    print(
        "relaxed local config: "
        f"nd_bvp={config.relaxed_local_config.nd_bvp}, tol={config.relaxed_local_config.tol:.1e}, "
        f"relaxed_tol={config.relaxed_local_config.relaxed_tol:.1e}, max_nodes={config.relaxed_local_config.max_nodes}, "
        f"right_edge_cluster_start={config.relaxed_local_config.right_edge_cluster_start:.3f}, "
        f"right_edge_cluster_fraction={config.relaxed_local_config.right_edge_cluster_fraction:.2f}, "
        f"right_edge_cluster_power={config.relaxed_local_config.right_edge_cluster_power:.2f}"
    )
    print(f"anchor loads: {list(config.anchor_loads_mpa)}")
    print(f"local loads:  {list(config.local_loads_mpa)}")
    print()
    print_result_block("Anchor schedule", history.anchor_results)
    print_local_branch_result_block("Local branch-following schedule", history.local_steps)


def main() -> None:
    report_main()


__all__ = [
    "AxisymmetricBackgroundSolve",
    "AxisymmetricLocalBranchFollowConfig",
    "AxisymmetricLocalBranchHistory",
    "AxisymmetricLocalBranchStep",
    "AxisymmetricSimpleSupportConfig",
    "BC_LABELS",
    "DEFAULT_CONTINUATION_LOADS_MPA",
    "DEFAULT_FIXED_LOADS_MPA",
    "DEFAULT_LOCAL_BRANCH_ANCHOR_LOADS_MPA",
    "DEFAULT_LOCAL_BRANCH_LOADS_MPA",
    "STATE_LABELS",
    "axisymmetric_simple_support_bc",
    "axisymmetric_simple_support_ode",
    "build_template_solution",
    "default_x_mesh",
    "report_local_branch_following_main",
    "report_main",
    "solve_axisymmetric_simple_support_continuation",
    "solve_axisymmetric_simple_support_fixed_load",
    "solve_axisymmetric_simple_support_local_branch_following",
    "solve_fixed_load_schedule",
]
