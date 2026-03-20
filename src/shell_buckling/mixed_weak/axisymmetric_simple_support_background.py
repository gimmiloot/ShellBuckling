from __future__ import annotations

from dataclasses import dataclass
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


@dataclass(frozen=True)
class AxisymmetricSimpleSupportConfig:
    x0: float = 1.0 / 600.0
    nd_bvp: int = 600
    tol: float = 1.0e-4
    relaxed_tol: float = 5.0e-4
    max_nodes: int = 120000
    template_q_mpa: float = 0.5


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
    return np.linspace(float(config.x0), 1.0, int(config.nd_bvp))


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


def main() -> None:
    report_main()


__all__ = [
    "AxisymmetricBackgroundSolve",
    "AxisymmetricSimpleSupportConfig",
    "BC_LABELS",
    "DEFAULT_CONTINUATION_LOADS_MPA",
    "DEFAULT_FIXED_LOADS_MPA",
    "STATE_LABELS",
    "axisymmetric_simple_support_bc",
    "axisymmetric_simple_support_ode",
    "build_template_solution",
    "report_main",
    "solve_axisymmetric_simple_support_continuation",
    "solve_axisymmetric_simple_support_fixed_load",
    "solve_fixed_load_schedule",
]