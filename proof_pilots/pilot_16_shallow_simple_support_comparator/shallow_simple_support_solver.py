from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Sequence

import numpy as np
from scipy.integrate import cumulative_trapezoid, solve_bvp


nu = 0.3
E = 205e9
h = 0.005
a = 0.5
mu = a / h
beta = np.sqrt(12.0 * (1.0 - nu**2)) * mu
gamma = 12.0 * (1.0 - nu**2) * mu**2

STATE_LABELS = ("theta0'", "theta0", "Phi0'", "Phi0")
BC_LABELS = (
    "theta0(x0)=0",
    "Phi0(x0)=0",
    "Phi0(1)=0",
    "theta0'(1)+nu*theta0(1)=0",
)


@dataclass(frozen=True)
class ShallowSimpleSupportConfig:
    x0: float = 1.0 / 1500.0
    nd_bvp: int = 1500
    tol: float = 1.0e-5
    relaxed_tol: float = 5.0e-5
    max_nodes: int = 80000
    substep_max_delta_mpa: float = 0.25


@dataclass
class ShallowSimpleSupportSolve:
    q_mpa: float
    success: bool
    message: str
    nodes: int
    max_rms: float
    max_bc_residual: float
    edge_moment_residual: float
    max_abs_theta0: float
    max_abs_Phi0: float
    max_abs_u_z_recovered: float
    solution: object | None = None

    def summary_line(self) -> str:
        rms = f"{self.max_rms:.2e}" if np.isfinite(self.max_rms) else "nan"
        bc = f"{self.max_bc_residual:.2e}" if np.isfinite(self.max_bc_residual) else "nan"
        mres = f"{self.edge_moment_residual:.2e}" if np.isfinite(self.edge_moment_residual) else "nan"
        return (
            f"q={self.q_mpa:.4f} MPa  success={self.success}  nodes={self.nodes}  "
            f"max_rms={rms}  max_bc={bc}  edge_Ms_res={mres}  message={self.message}"
        )


def shallow_simple_support_ode(x: np.ndarray, y: np.ndarray, q_pa: float) -> np.ndarray:
    x_safe = np.maximum(np.asarray(x, dtype=float), 1.0e-12)
    load_term = q_pa * x_safe * beta**3 * mu / (2.0 * E)
    return np.vstack(
        (
            -y[0] / x_safe + y[1] / x_safe**2 + y[3] * (y[1] / x_safe) + load_term,
            y[0],
            -y[2] / x_safe + y[3] / x_safe**2 - y[1] * (y[1] / (2.0 * x_safe)),
            y[2],
        )
    )


def shallow_simple_support_bc(ya: np.ndarray, yb: np.ndarray) -> np.ndarray:
    return np.array([ya[1], ya[3], yb[3], yb[0] + nu * yb[1]], dtype=float)


def default_x_mesh(config: ShallowSimpleSupportConfig) -> np.ndarray:
    return np.linspace(float(config.x0), 1.0, int(config.nd_bvp))


def zero_guess(x_mesh: np.ndarray) -> np.ndarray:
    return np.zeros((len(STATE_LABELS), x_mesh.size), dtype=float)


def inferred_moment_from_shallow_state(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    x_safe = np.maximum(np.asarray(x, dtype=float), 1.0e-12)
    return -(y[0] + nu * y[1] / x_safe) / (beta * gamma)


def recover_u_z_shallow(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    theta0 = np.asarray(y[1], dtype=float)
    integrand = (mu / beta) * theta0
    reversed_integral = cumulative_trapezoid(integrand[::-1], x[::-1], initial=0.0)
    return (-reversed_integral)[::-1]


def run_bvp_attempt(q_mpa: float, x_mesh: np.ndarray, y_guess: np.ndarray, config: ShallowSimpleSupportConfig):
    q_pa = float(q_mpa) * 1.0e6
    fun = lambda x, y: shallow_simple_support_ode(x, y, q_pa=q_pa)
    sol = solve_bvp(
        fun,
        shallow_simple_support_bc,
        x_mesh,
        y_guess,
        tol=config.tol,
        max_nodes=config.max_nodes,
        verbose=0,
    )
    if not sol.success:
        sol = solve_bvp(
            fun,
            shallow_simple_support_bc,
            x_mesh,
            y_guess,
            tol=config.relaxed_tol,
            max_nodes=config.max_nodes,
            verbose=0,
        )
    return sol


def summarize_solution(q_mpa: float, sol, x_mesh: np.ndarray) -> ShallowSimpleSupportSolve:
    if sol.success:
        yv = sol.sol(x_mesh)
        bc_residual = shallow_simple_support_bc(yv[:, 0], yv[:, -1])
        edge_moment = inferred_moment_from_shallow_state(np.array([1.0]), yv[:, -1][:, None])[0]
        uz_recovered = recover_u_z_shallow(x_mesh, yv)
        max_rms = float(np.max(sol.rms_residuals)) if hasattr(sol, "rms_residuals") else float("nan")
        max_bc = float(np.max(np.abs(bc_residual)))
        max_theta0 = float(np.max(np.abs(yv[1])))
        max_Phi0 = float(np.max(np.abs(yv[3])))
        max_uz = float(np.max(np.abs(uz_recovered)))
    else:
        max_rms = float("nan")
        max_bc = float("nan")
        edge_moment = float("nan")
        max_theta0 = float("nan")
        max_Phi0 = float("nan")
        max_uz = float("nan")

    return ShallowSimpleSupportSolve(
        q_mpa=float(q_mpa),
        success=bool(sol.success),
        message=str(sol.message),
        nodes=int(sol.x.size),
        max_rms=max_rms,
        max_bc_residual=max_bc,
        edge_moment_residual=float(edge_moment),
        max_abs_theta0=max_theta0,
        max_abs_Phi0=max_Phi0,
        max_abs_u_z_recovered=max_uz,
        solution=sol if sol.success else None,
    )


def continuation_substeps(q_from: float, q_to: float, max_delta: float) -> list[float]:
    delta = abs(float(q_to) - float(q_from))
    if delta < 1.0e-12:
        return [float(q_to)]
    n_steps = max(1, int(np.ceil(delta / max_delta)))
    return np.linspace(float(q_from), float(q_to), n_steps + 1)[1:].tolist()


def solve_shallow_simple_support_continuation(
    q_values_mpa: Sequence[float],
    config: ShallowSimpleSupportConfig = ShallowSimpleSupportConfig(),
) -> list[ShallowSimpleSupportSolve]:
    if not q_values_mpa:
        return []

    x_mesh = default_x_mesh(config)
    results: list[ShallowSimpleSupportSolve] = []
    previous_solution = None
    previous_q = 0.0

    for q_target in q_values_mpa:
        q_target = float(q_target)
        substeps = continuation_substeps(previous_q, q_target, config.substep_max_delta_mpa)
        for q_step in substeps:
            if previous_solution is None or abs(q_step) < 1.0e-14:
                y_guess = zero_guess(x_mesh)
            else:
                y_guess = previous_solution.sol(x_mesh)
            sol = run_bvp_attempt(q_step, x_mesh, y_guess, config)
            result = summarize_solution(q_step, sol, x_mesh)
            if not result.success:
                results.append(result)
                return results
            previous_solution = result.solution
            previous_q = q_step
        results.append(result)

    return results


def print_result_block(results: Sequence[ShallowSimpleSupportSolve]) -> None:
    print("=== Shallow simple-support continuation report ===")
    print(f"state: {list(STATE_LABELS)}")
    print(f"BCs:   {list(BC_LABELS)}")
    print()
    for result in results:
        print(f"  {result.summary_line()}")
    success_loads = [result.q_mpa for result in results if result.success]
    last_success = success_loads[-1] if success_loads else None
    first_failure = next((result.q_mpa for result in results if not result.success), None)
    print()
    print(f"  success loads: {success_loads}")
    print(f"  last success: {last_success}")
    print(f"  first failure: {first_failure}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--loads-mpa",
        type=float,
        nargs="+",
        default=[0.0, 0.5, 1.0, 2.0, 3.0, 4.0, 4.3434],
        help="Continuation target loads in MPa.",
    )
    parser.add_argument("--nd-bvp", type=int, default=1500)
    parser.add_argument("--tol", type=float, default=1.0e-5)
    parser.add_argument("--relaxed-tol", type=float, default=5.0e-5)
    parser.add_argument("--max-nodes", type=int, default=80000)
    parser.add_argument("--substep-max-delta-mpa", type=float, default=0.25)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = ShallowSimpleSupportConfig(
        nd_bvp=int(args.nd_bvp),
        tol=float(args.tol),
        relaxed_tol=float(args.relaxed_tol),
        max_nodes=int(args.max_nodes),
        substep_max_delta_mpa=float(args.substep_max_delta_mpa),
    )
    results = solve_shallow_simple_support_continuation(args.loads_mpa, config=config)
    print_result_block(results)


if __name__ == "__main__":
    main()
