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


THIS_FILE = Path(__file__).resolve()
PILOT_DIR = THIS_FILE.parent
DEFAULT_OUTPUT_JSON = PILOT_DIR / "term_balance_results.json"
nu = 0.3
E = 205e9
h = 0.005
a = 0.5
mu = a / h
GAMMA = 12.0 * (1.0 - nu**2) * mu**2


def region_metrics(x: np.ndarray, field: np.ndarray, mask: np.ndarray) -> dict[str, float]:
    x_seg = x[mask]
    f_seg = field[mask]
    peak_idx = int(np.argmax(np.abs(f_seg)))
    return {
        "abs_l2": float(np.sqrt(np.trapezoid(f_seg**2, x_seg))),
        "max_abs": float(np.max(np.abs(f_seg))),
        "x_at_peak": float(x_seg[peak_idx]),
    }


def compute_groups(q_mpa: float, x: np.ndarray, state: np.ndarray) -> dict[str, np.ndarray]:
    Ts, Tsn, Ms, ur, uz, phi = state
    x_safe = np.maximum(x, 1.0e-12)
    r = x_safe + ur
    etheta = ur / x_safe
    es = Ts * (1.0 - nu**2) - nu * etheta
    Ttheta = nu * Ts + etheta
    phi_bending = GAMMA * Ms
    phi_hoop = -nu * np.sin(phi) / r
    kappa_s = phi_bending + phi_hoop
    Mtheta = nu * Ms + np.sin(phi) / (12.0 * mu**2 * r)
    qbar = float(q_mpa) * 1.0e6 * a / (E * h)

    return {
        "radius_inverse_gap": 1.0 / r - 1.0 / x_safe,
        "hoop_geometric_factor": etheta,
        "Ttheta_membrane": nu * Ts,
        "Ttheta_geometric": etheta,
        "Tsprime_radius": -(Ts / r),
        "Tsprime_hoop": (np.cos(phi) * Ttheta) / r,
        "Tsprime_shear": -kappa_s * Tsn,
        "Tsnprime_radius": -(Tsn / r),
        "Tsnprime_hoop_trig": (np.sin(phi) * Ttheta) / r,
        "Tsnprime_curvature": kappa_s * Ts,
        "Tsnprime_load": np.full_like(x, -qbar),
        "Msprime_radius": -(Ms / r),
        "Msprime_hoop": (np.cos(phi) * Mtheta) / r,
        "Msprime_shear": Tsn,
        "phi_bending": phi_bending,
        "phi_hoop": phi_hoop,
        "uz_linear": -mu * (1.0 + es) * phi,
        "uz_trig_gap": -mu * (1.0 + es) * (np.sin(phi) - phi),
        "sin_minus_phi": np.sin(phi) - phi,
        "one_minus_cos": 1.0 - np.cos(phi),
    }


def summarize_load(q_mpa: float, x: np.ndarray, state: np.ndarray) -> dict[str, Any]:
    groups = compute_groups(q_mpa, x, state)
    edge_mask = x >= 0.95
    ultra_mask = x >= 0.99
    per_group = {
        name: {
            "edge": region_metrics(x, field, edge_mask),
            "ultra_edge": region_metrics(x, field, ultra_mask),
        }
        for name, field in groups.items()
    }

    def l2(name: str, region: str) -> float:
        return per_group[name][region]["abs_l2"]

    return {
        "q_mpa": float(q_mpa),
        "groups": per_group,
        "ratios": {
            "Ttheta_geometric_over_membrane_ultra": l2("Ttheta_geometric", "ultra_edge") / max(l2("Ttheta_membrane", "ultra_edge"), 1.0e-30),
            "phi_hoop_over_bending_ultra": l2("phi_hoop", "ultra_edge") / max(l2("phi_bending", "ultra_edge"), 1.0e-30),
            "uz_trig_gap_over_linear_ultra": l2("uz_trig_gap", "ultra_edge") / max(l2("uz_linear", "ultra_edge"), 1.0e-30),
        },
        "dominant_terms": {
            "Tsprime_edge": max(("Tsprime_radius", "Tsprime_hoop", "Tsprime_shear"), key=lambda name: l2(name, "edge")),
            "Tsnprime_edge": max(("Tsnprime_radius", "Tsnprime_hoop_trig", "Tsnprime_curvature", "Tsnprime_load"), key=lambda name: l2(name, "edge")),
            "Msprime_edge": max(("Msprime_radius", "Msprime_hoop", "Msprime_shear"), key=lambda name: l2(name, "edge")),
            "phi_edge": max(("phi_bending", "phi_hoop"), key=lambda name: l2(name, "edge")),
            "uz_edge": max(("uz_linear", "uz_trig_gap"), key=lambda name: l2(name, "edge")),
        },
    }


def classify(converged_results: list[dict[str, Any]], failed_partial: dict[str, Any] | None) -> dict[str, Any]:
    high = converged_results[-1]
    geom_ratio = float(high["ratios"]["Ttheta_geometric_over_membrane_ultra"])
    phi_ratio = float(high["ratios"]["phi_hoop_over_bending_ultra"])
    uz_ratio = float(high["ratios"]["uz_trig_gap_over_linear_ultra"])

    smooth = True
    for key in ("Ttheta_geometric_over_membrane_ultra", "phi_hoop_over_bending_ultra", "uz_trig_gap_over_linear_ultra"):
        series = np.array([item["ratios"][key] for item in converged_results], dtype=float)
        if float(np.max(series) - np.min(series)) > 0.15 * max(float(np.max(series)), 1.0):
            smooth = False

    if geom_ratio > 100.0 and phi_ratio < 0.5 and uz_ratio < 0.4 and smooth:
        label = "edge_layer_geometric_balance_with_moderate_trig_corrections"
    else:
        label = "mixed_or_unresolved_balance"

    return {
        "label": label,
        "highest_load_ratios": {
            "Ttheta_geometric_over_membrane_ultra": geom_ratio,
            "phi_hoop_over_bending_ultra": phi_ratio,
            "uz_trig_gap_over_linear_ultra": uz_ratio,
        },
        "smooth_term_trends_in_converged_range": smooth,
        "failed_target_partial_available": failed_partial is not None,
        "failed_target_partial_note": (
            "The nonconverged 4.3440 MPa secant-profile attempt is reported only as supportive context."
            if failed_partial is not None
            else None
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-npz", type=Path, default=DEFAULT_CACHE_NPZ)
    parser.add_argument("--cache-json", type=Path, default=DEFAULT_CACHE_JSON)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--budget-seconds", type=float, default=1200.0)
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
    x_grid = np.asarray(arrays["balance_grid"], dtype=float)
    states = np.asarray(arrays["balance_states"], dtype=float)
    failed_state = np.asarray(arrays["failed_balance_state"], dtype=float)

    converged_results = [summarize_load(float(q_mpa), x_grid, states[idx]) for idx, q_mpa in enumerate(loads)]
    failed_partial = summarize_load(float(cache_payload["metadata"]["failed_target_load_mpa"]), x_grid, failed_state)
    summary = classify(converged_results, failed_partial)

    payload = {
        "metadata": {
            "pilot": "pilot_18_revised_analytic_barrier_diagnosis",
            "source_cache_npz": str(args.cache_npz),
            "source_cache_json": str(args.cache_json),
            "loads_mpa": loads.tolist(),
        },
        "branch_cache_summary": cache_payload,
        "converged_results": converged_results,
        "failed_target_partial": failed_partial,
        "summary": summary,
    }
    save_json(args.output_json, payload)

    print("=== Pilot 18 term balance check ===")
    print(f"Loads checked: {', '.join(f'{q:.4f}' for q in loads)} MPa")
    for item in converged_results:
        print(
            f"  q={item['q_mpa']:.4f} MPa  Ttheta_geo/mem={item['ratios']['Ttheta_geometric_over_membrane_ultra']:.3e}  "
            f"phi_hoop/bending={item['ratios']['phi_hoop_over_bending_ultra']:.3e}  "
            f"uz_trig/linear={item['ratios']['uz_trig_gap_over_linear_ultra']:.3e}  "
            f"dominant_Tsnprime={item['dominant_terms']['Tsnprime_edge']}  dominant_Msprime={item['dominant_terms']['Msprime_edge']}"
        )
    print(f"Balance diagnosis: {summary['label']}")
    print(f"Results written to: {args.output_json}")


if __name__ == "__main__":
    main()
