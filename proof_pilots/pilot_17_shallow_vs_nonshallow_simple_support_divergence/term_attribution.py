from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np


THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[2]
SRC_ROOT = REPO_ROOT / "src"
PILOT_DIR = THIS_FILE.parent
DEFAULT_SWEEP_JSON = PILOT_DIR / "comparison_results.json"
DEFAULT_CACHE_NPZ = PILOT_DIR / "comparison_cache.npz"
DEFAULT_OUTPUT_JSON = PILOT_DIR / "term_attribution_results.json"
SIGNIFICANCE_THRESHOLD = 0.05
VARIABLE_KEYS = ("theta0", "theta0p", "Phi0", "Phi0p")

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from shell_buckling.supporting import determinant_criterion_comparison as detcomp


GROUP_CATALOG: dict[str, dict[str, str]] = {
    "theta0_small_angle_trig": {
        "family": "theta0",
        "base_key": "theta0_actual",
        "description": "Difference between mapped theta0 = -beta*sin(phi) and linearized theta0 = -beta*phi.",
    },
    "theta0p_radius_correction": {
        "family": "theta0p",
        "base_key": "theta0p_actual",
        "description": "Contribution from replacing x by deformed radius r in the curvature term of theta0'.",
    },
    "theta0p_sine_curvature_correction": {
        "family": "theta0p",
        "base_key": "theta0p_actual",
        "description": "Contribution from replacing phi by sin(phi) in the curvature term of theta0'.",
    },
    "theta0p_cosine_factor_correction": {
        "family": "theta0p",
        "base_key": "theta0p_actual",
        "description": "Contribution from the prefactor cos(phi) in theta0' = -beta*cos(phi)*kappa_s.",
    },
    "theta0p_combined_nonshallow_correction": {
        "family": "theta0p",
        "base_key": "theta0p_actual",
        "description": "Total gap between mapped theta0' and its small-angle / undeformed-radius linearization.",
    },
    "Phi0p_hoop_geometric_contribution": {
        "family": "Phi0p",
        "base_key": "Phi0p_actual",
        "description": "Contribution of the geometric hoop term ur/x inside Phi0' = gamma*(nu*T_s + ur/x).",
    },
    "inverse_radius_gap": {
        "family": "global",
        "base_key": "inverse_radius_base",
        "description": "Magnitude of the deformed-radius change 1/r - 1/x.",
    },
    "hoop_strain_geometric_factor": {
        "family": "global",
        "base_key": "Ttheta_actual",
        "description": "Magnitude of the geometric hoop-strain factor ur/x entering T_theta.",
    },
    "ur_kinematic_cosine_gap": {
        "family": "global",
        "base_key": "ur_prime_actual",
        "description": "Kinematic gap in u_r' from the factor (1+e_s)*cos(phi) - 1 versus the linearized e_s.",
    },
    "uz_small_angle_trig_gap": {
        "family": "global",
        "base_key": "uz_prime_actual",
        "description": "Kinematic gap in u_z' from sin(phi) versus phi while keeping the same (1+e_s) prefactor.",
    },
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


def pearson(x: np.ndarray, y: np.ndarray) -> float | None:
    if x.size != y.size or x.size < 2:
        return None
    if float(np.std(x)) <= 0.0 or float(np.std(y)) <= 0.0:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def contribution_metrics(x: np.ndarray, contribution: np.ndarray, base: np.ndarray, mask: np.ndarray) -> dict[str, float]:
    x_seg = x[mask]
    contribution_seg = contribution[mask]
    base_seg = base[mask]

    abs_l2 = float(np.sqrt(np.trapezoid(contribution_seg**2, x_seg)))
    base_l2 = float(np.sqrt(np.trapezoid(base_seg**2, x_seg)))
    rel_l2 = abs_l2 / max(base_l2, 1.0e-12)

    max_abs = float(np.max(np.abs(contribution_seg)))
    base_max = float(np.max(np.abs(base_seg)))
    rel_max = max_abs / max(base_max, 1.0e-12)

    return {
        "abs_l2": abs_l2,
        "rel_l2": rel_l2,
        "max_abs": max_abs,
        "rel_max": rel_max,
    }


def first_significant_load(loads: np.ndarray, values: np.ndarray, threshold: float) -> float | None:
    for load, value in zip(loads, values, strict=True):
        if float(value) >= threshold:
            return float(load)
    return None


def float_key(value: float) -> str:
    return f"{value:.4f}"


def build_group_arrays(x_grid: np.ndarray, state: np.ndarray) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray], dict[str, float]]:
    x_safe = np.maximum(np.asarray(x_grid, dtype=float), 1.0e-12)
    Ts, Tsn, Ms, ur, uz, phi = state

    r = x_safe + ur
    etheta = ur / x_safe
    es = Ts * (1.0 - detcomp.nu**2) - detcomp.nu * etheta
    A = 12.0 * (1.0 - detcomp.nu**2) * Ms * detcomp.mu**2

    kappa_actual = A - detcomp.nu * np.sin(phi) / r
    kappa_phi_over_r = A - detcomp.nu * phi / r
    kappa_linear = A - detcomp.nu * phi / x_safe

    theta0_linear = -detcomp.beta * phi
    theta0_actual = -detcomp.beta * np.sin(phi)

    theta0p_linear = -detcomp.beta * kappa_linear
    theta0p_after_radius = -detcomp.beta * kappa_phi_over_r
    theta0p_after_sine = -detcomp.beta * kappa_actual
    theta0p_actual = -detcomp.beta * np.cos(phi) * kappa_actual

    Ttheta_actual = detcomp.nu * Ts + etheta
    Phi0p_membrane = detcomp.gamma * detcomp.nu * Ts
    Phi0p_actual = detcomp.gamma * Ttheta_actual

    inverse_radius_base = 1.0 / x_safe
    inverse_radius_actual = 1.0 / r

    ur_prime_actual = (1.0 + es) * np.cos(phi) - 1.0
    ur_prime_linear = es
    uz_prime_actual = -detcomp.mu * (1.0 + es) * np.sin(phi)
    uz_prime_small_angle = -detcomp.mu * (1.0 + es) * phi

    groups = {
        "theta0_small_angle_trig": theta0_actual - theta0_linear,
        "theta0p_radius_correction": theta0p_after_radius - theta0p_linear,
        "theta0p_sine_curvature_correction": theta0p_after_sine - theta0p_after_radius,
        "theta0p_cosine_factor_correction": theta0p_actual - theta0p_after_sine,
        "theta0p_combined_nonshallow_correction": theta0p_actual - theta0p_linear,
        "Phi0p_hoop_geometric_contribution": Phi0p_actual - Phi0p_membrane,
        "inverse_radius_gap": inverse_radius_actual - inverse_radius_base,
        "hoop_strain_geometric_factor": etheta,
        "ur_kinematic_cosine_gap": ur_prime_actual - ur_prime_linear,
        "uz_small_angle_trig_gap": uz_prime_actual - uz_prime_small_angle,
    }

    bases = {
        "theta0_actual": theta0_actual,
        "theta0p_actual": theta0p_actual,
        "Phi0p_actual": Phi0p_actual,
        "inverse_radius_base": inverse_radius_base,
        "Ttheta_actual": Ttheta_actual,
        "ur_prime_actual": ur_prime_actual,
        "uz_prime_actual": uz_prime_actual,
    }

    diagnostics = {
        "max_abs_phi": float(np.max(np.abs(phi))),
        "max_abs_ur": float(np.max(np.abs(ur))),
        "min_r": float(np.min(r)),
        "max_abs_es": float(np.max(np.abs(es))),
        "max_abs_etheta": float(np.max(np.abs(etheta))),
    }
    return groups, bases, diagnostics


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--comparison-json", type=Path, default=DEFAULT_SWEEP_JSON)
    parser.add_argument("--cache-npz", type=Path, default=DEFAULT_CACHE_NPZ)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    comparison_payload = json.loads(args.comparison_json.read_text(encoding="utf-8"))
    cache = np.load(args.cache_npz)

    loads = np.asarray(cache["loads_mpa"], dtype=float)
    x_grid = np.asarray(cache["x_grid"], dtype=float)
    nonshallow_states = np.asarray(cache["nonshallow_states"], dtype=float)

    comparison_results = comparison_payload.get("results", [])
    comparison_by_load = {float(item["q_mpa"]): item for item in comparison_results}
    missing = [float(load) for load in loads if float(load) not in comparison_by_load]
    if missing:
        raise RuntimeError(f"Comparison JSON is missing loads present in cache: {missing}")

    full_mask = np.ones_like(x_grid, dtype=bool)
    center_mask = x_grid <= 0.15
    bulk_mask = x_grid <= 0.95
    edge_mask = x_grid >= 0.95

    payload: dict[str, Any] = {
        "metadata": {
            "pilot": "pilot_17_shallow_vs_nonshallow_simple_support_divergence",
            "source_comparison_json": str(args.comparison_json),
            "source_cache_npz": str(args.cache_npz),
            "loads_mpa": loads.tolist(),
            "significance_threshold_bulk_rel_l2": SIGNIFICANCE_THRESHOLD,
            "group_catalog": GROUP_CATALOG,
        },
        "status": "started",
    }
    save_json(args.output_json, payload)

    per_load_results: list[dict[str, Any]] = []
    for idx, load in enumerate(loads):
        groups, bases, diagnostics = build_group_arrays(x_grid, nonshallow_states[idx])
        load_entry: dict[str, Any] = {
            "q_mpa": float(load),
            "diagnostics": diagnostics,
            "groups": {},
        }
        for key, field in groups.items():
            base = bases[GROUP_CATALOG[key]["base_key"]]
            load_entry["groups"][key] = {
                "full": contribution_metrics(x_grid, field, base, full_mask),
                "center": contribution_metrics(x_grid, field, base, center_mask),
                "bulk": contribution_metrics(x_grid, field, base, bulk_mask),
                "edge": contribution_metrics(x_grid, field, base, edge_mask),
            }
        per_load_results.append(load_entry)
        payload["per_load_results"] = per_load_results
        payload["status"] = f"completed_{float_key(float(load))}"
        save_json(args.output_json, payload)

    overall_bulk_mismatch = np.array(
        [comparison_by_load[float(load)]["overall"]["mean_bulk_rel_l2"] for load in loads],
        dtype=float,
    )
    variable_bulk_mismatch = {
        name: np.array([comparison_by_load[float(load)]["variables"][name]["bulk"]["rel_l2"] for load in loads], dtype=float)
        for name in VARIABLE_KEYS
    }

    group_summary: dict[str, Any] = {}
    for key in GROUP_CATALOG:
        bulk_series = np.array([item["groups"][key]["bulk"]["rel_l2"] for item in per_load_results], dtype=float)
        edge_series = np.array([item["groups"][key]["edge"]["rel_l2"] for item in per_load_results], dtype=float)
        center_series = np.array([item["groups"][key]["center"]["rel_l2"] for item in per_load_results], dtype=float)
        family = GROUP_CATALOG[key]["family"]
        family_series = variable_bulk_mismatch.get(family)
        peak_idx = int(np.argmax(bulk_series))
        group_summary[key] = {
            "family": family,
            "first_significant_load_mpa": first_significant_load(loads, bulk_series, SIGNIFICANCE_THRESHOLD),
            "low_load_bulk_rel_l2": float(bulk_series[0]),
            "high_load_bulk_rel_l2": float(bulk_series[-1]),
            "high_load_edge_rel_l2": float(edge_series[-1]),
            "high_load_center_rel_l2": float(center_series[-1]),
            "peak_bulk_rel_l2": float(np.max(bulk_series)),
            "peak_bulk_rel_l2_load_mpa": float(loads[peak_idx]),
            "bulk_growth_ratio": float(bulk_series[-1] / max(bulk_series[0], 1.0e-12)),
            "pearson_with_overall_bulk_mismatch": pearson(bulk_series, overall_bulk_mismatch),
            "pearson_with_family_bulk_mismatch": pearson(bulk_series, family_series) if family_series is not None else None,
        }

    low_dominant = sorted(GROUP_CATALOG, key=lambda key: group_summary[key]["low_load_bulk_rel_l2"], reverse=True)
    high_dominant = sorted(GROUP_CATALOG, key=lambda key: group_summary[key]["high_load_bulk_rel_l2"], reverse=True)
    strongest_overall = sorted(
        GROUP_CATALOG,
        key=lambda key: abs(group_summary[key]["pearson_with_overall_bulk_mismatch"] or 0.0),
        reverse=True,
    )
    strongest_family = sorted(
        GROUP_CATALOG,
        key=lambda key: abs(group_summary[key]["pearson_with_family_bulk_mismatch"] or 0.0),
        reverse=True,
    )
    theta0p_components = [
        "theta0p_radius_correction",
        "theta0p_sine_curvature_correction",
        "theta0p_cosine_factor_correction",
        "theta0p_combined_nonshallow_correction",
    ]
    theta0p_rank = sorted(theta0p_components, key=lambda key: group_summary[key]["high_load_bulk_rel_l2"], reverse=True)

    summary = {
        "significance_threshold_bulk_rel_l2": SIGNIFICANCE_THRESHOLD,
        "low_load_dominant_groups_by_size": low_dominant[:5],
        "high_load_dominant_groups_by_size": high_dominant[:5],
        "strongest_overall_correlates": strongest_overall[:5],
        "strongest_family_correlates": strongest_family[:5],
        "theta0p_high_load_component_rank": theta0p_rank,
        "interpretation": {
            "theta0": (
                "theta0 has a single direct mapped non-shallow correction in this pilot: the small-angle trig gap "
                "between sin(phi) and phi."
            ),
            "theta0p": (
                "theta0' is decomposed additively into radius, sine-curvature, and cosine-prefactor corrections, plus "
                "their exact combined gap from the small-angle / undeformed-radius form."
            ),
            "Phi0": (
                "Phi0 = gamma*x*T_s has no separate mapping-only non-shallow correction in the current comparison, so "
                "this pilot does not uniquely attribute Phi0 mismatch to a single term group."
            ),
            "Phi0p": (
                "Phi0' is checked against the geometric hoop contribution gamma*(ur/x). This is informative for trend "
                "tracking but is not a proof of uniqueness."
            ),
            "global": (
                "The geometric groups involving ur/x, 1/r - 1/x, and the kinematic cosine/sine gaps are tracked as "
                "candidate drivers rather than theorem-level unique causes."
            ),
        },
    }

    payload["group_summary"] = group_summary
    payload["summary"] = summary
    payload["status"] = "completed"
    save_json(args.output_json, payload)

    print("=== Pilot 17 term attribution ===")
    print(f"Loads analyzed: {', '.join(float_key(load) for load in loads)} MPa")
    print(f"Low-load dominant groups: {', '.join(summary['low_load_dominant_groups_by_size'])}")
    print(f"High-load dominant groups: {', '.join(summary['high_load_dominant_groups_by_size'])}")
    print(f"Strongest overall correlates: {', '.join(summary['strongest_overall_correlates'])}")
    print(f"Results written to: {args.output_json}")


if __name__ == "__main__":
    main()
