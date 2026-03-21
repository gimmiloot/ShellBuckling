from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np

from analysis_common import (
    DEFAULT_CACHE_JSON,
    DEFAULT_CACHE_NPZ,
    ensure_branch_cache,
    save_json,
)
from shell_buckling.mixed_weak.axisymmetric_simple_support_background import (
    STATE_LABELS,
    axisymmetric_simple_support_bc,
    axisymmetric_simple_support_ode,
)


THIS_FILE = Path(__file__).resolve()
PILOT_DIR = THIS_FILE.parent
DEFAULT_OUTPUT_JSON = PILOT_DIR / "jacobian_conditioning_results.json"


def discrete_bvp_residual(state: np.ndarray, x_grid: np.ndarray, q_pa: float) -> np.ndarray:
    y = np.asarray(state, dtype=float).reshape(len(STATE_LABELS), x_grid.size)
    f = axisymmetric_simple_support_ode(x_grid, y, q_pa=q_pa)
    dx = np.diff(x_grid)
    interval_residual = y[:, 1:] - y[:, :-1] - 0.5 * dx * (f[:, 1:] + f[:, :-1])
    bc_residual = axisymmetric_simple_support_bc(y[:, 0], y[:, -1])[:, None]
    return np.concatenate([interval_residual, bc_residual], axis=1).reshape(-1)


def approximate_jacobian(state: np.ndarray, x_grid: np.ndarray, q_pa: float, rel_step: float) -> np.ndarray:
    y0 = np.asarray(state, dtype=float).reshape(-1)
    base = discrete_bvp_residual(y0, x_grid, q_pa=q_pa)
    jac = np.empty((base.size, y0.size), dtype=float)
    for idx in range(y0.size):
        step = rel_step * max(1.0, abs(float(y0[idx])))
        probe = y0.copy()
        probe[idx] += step
        jac[:, idx] = (discrete_bvp_residual(probe, x_grid, q_pa=q_pa) - base) / step
    return jac


def singular_vector_summary(vh_last: np.ndarray, x_grid: np.ndarray) -> dict[str, Any]:
    vector = np.asarray(vh_last, dtype=float).reshape(len(STATE_LABELS), x_grid.size)
    mass = vector**2
    total = float(np.sum(mass))
    edge_mask = x_grid >= 0.95
    ultra_mask = x_grid >= 0.99
    center_mask = x_grid <= 0.15
    by_state = {
        STATE_LABELS[idx]: float(np.sum(mass[idx]) / max(total, 1.0e-30))
        for idx in range(len(STATE_LABELS))
    }
    return {
        "edge_mass_fraction": float(np.sum(mass[:, edge_mask]) / max(total, 1.0e-30)),
        "ultra_edge_mass_fraction": float(np.sum(mass[:, ultra_mask]) / max(total, 1.0e-30)),
        "center_mass_fraction": float(np.sum(mass[:, center_mask]) / max(total, 1.0e-30)),
        "by_state_mass_fraction": by_state,
        "dominant_state": max(by_state.items(), key=lambda item: item[1])[0],
    }


def classify(results: list[dict[str, Any]]) -> dict[str, Any]:
    sigma_min = np.array([item["sigma_min"] for item in results], dtype=float)
    cond = np.array([item["condition_number"] for item in results], dtype=float)
    ratio = float(sigma_min[-1] / max(sigma_min[0], 1.0e-30))
    cond_ratio = float(cond[-1] / max(cond[0], 1.0e-30))
    near_zero = bool(sigma_min[-1] < 0.5 * sigma_min[0] and cond_ratio > 2.0)
    if near_zero:
        label = "possible_near_fold_signal"
    else:
        label = "ill_conditioned_but_no_clear_near_fold_signal"
    return {
        "label": label,
        "sigma_min_ratio_high_to_low": ratio,
        "condition_number_ratio_high_to_low": cond_ratio,
        "near_zero_singular_value_signal": near_zero,
        "highest_load_soft_mode": results[-1]["soft_mode"],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-npz", type=Path, default=DEFAULT_CACHE_NPZ)
    parser.add_argument("--cache-json", type=Path, default=DEFAULT_CACHE_JSON)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--budget-seconds", type=float, default=1200.0)
    parser.add_argument("--fd-rel-step", type=float, default=1.0e-7)
    parser.add_argument("--rebuild-cache", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    cache_payload, arrays = ensure_branch_cache(
        cache_npz=args.cache_npz,
        cache_json=args.cache_json,
        budget_seconds=float(args.budget_seconds),
        rebuild=bool(args.rebuild_cache),
    )
    loads = np.asarray(arrays["loads_mpa"], dtype=float)
    x_grid = np.asarray(arrays["jacobian_grid"], dtype=float)
    states = np.asarray(arrays["jacobian_states"], dtype=float)

    results = []
    for idx, q_mpa in enumerate(loads):
        jac = approximate_jacobian(states[idx], x_grid, q_pa=float(q_mpa) * 1.0e6, rel_step=float(args.fd_rel_step))
        _, singular_values, vh = np.linalg.svd(jac, full_matrices=False)
        soft_summary = singular_vector_summary(vh[-1], x_grid)
        result = {
            "q_mpa": float(q_mpa),
            "sigma_max": float(singular_values[0]),
            "sigma_min": float(singular_values[-1]),
            "sigma_5_from_bottom": float(singular_values[-5]),
            "condition_number": float(singular_values[0] / max(singular_values[-1], 1.0e-30)),
            "soft_mode": soft_summary,
        }
        results.append(result)

    summary = classify(results)
    payload = {
        "metadata": {
            "pilot": "pilot_18_revised_analytic_barrier_diagnosis",
            "source_cache_npz": str(args.cache_npz),
            "source_cache_json": str(args.cache_json),
            "fd_rel_step": float(args.fd_rel_step),
            "loads_mpa": loads.tolist(),
        },
        "branch_cache_summary": cache_payload,
        "results": results,
        "summary": summary,
    }
    save_json(args.output_json, payload)

    print("=== Pilot 18 Jacobian conditioning check ===")
    print(f"Loads checked: {', '.join(f'{q:.4f}' for q in loads)} MPa")
    for item in results:
        print(
            f"  q={item['q_mpa']:.4f} MPa  sigma_min={item['sigma_min']:.3e}  "
            f"sigma_5={item['sigma_5_from_bottom']:.3e}  cond={item['condition_number']:.3e}  "
            f"soft_state={item['soft_mode']['dominant_state']}  "
            f"edge_mass={item['soft_mode']['edge_mass_fraction']:.3f}"
        )
    print(f"Conditioning diagnosis: {summary['label']}")
    print(f"Near-zero-singular-value signal: {summary['near_zero_singular_value_signal']}")
    print(f"Results written to: {args.output_json}")


if __name__ == "__main__":
    main()
