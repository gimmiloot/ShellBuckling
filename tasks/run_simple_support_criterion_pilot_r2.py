# -*- coding: utf-8 -*-
# Purpose:
#   Run the first practical R2 diagnostic pass for the clean full simple
#   support / podvizhnyi sharnir path without changing the main solver path.
# Typical use:
#   .venv\Scripts\python.exe tasks\run_simple_support_criterion_pilot_r2.py
# Outputs:
#   output/clean_full_simple_support/criterion_pilot_r2_summary.json
#   output/clean_full_simple_support/criterion_pilot_r2_table.csv

from __future__ import annotations

import csv
import json
import time
from pathlib import Path
import sys

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.mixed_weak import full_simple_support_critical_search as full_search
from shell_buckling.mixed_weak import simple_support_high_load_background_continuation as high_bg


OUTPUT_DIR = REPO_ROOT / "output" / "clean_full_simple_support"
SUMMARY_JSON = OUTPUT_DIR / "criterion_pilot_r2_summary.json"
SUMMARY_CSV = OUTPUT_DIR / "criterion_pilot_r2_table.csv"

DEFAULT_MODES = (4, 6, 7, 8)
DEFAULT_P_MIN_MPA = 10.5
DEFAULT_P_MAX_MPA = 18.5
DEFAULT_P_NPTS = 81

METRIC_SPECS: tuple[tuple[str, str], ...] = (
    ("sigma_bal", "sigma_bal(B_mix)"),
    ("sigma_Bred_bal", "sigma_Bred_bal"),
    ("rho_R2", "rho_R2"),
)
EPS = 1.0e-30


def condition_number(A: np.ndarray) -> float:
    singular_values = np.linalg.svd(np.asarray(A, dtype=float), compute_uv=False)
    if singular_values.size == 0:
        return float("nan")
    if singular_values[-1] <= EPS:
        return float("inf")
    return float(singular_values[0] / singular_values[-1])


def best_point_for_metric(point_rows: list[dict[str, object]], metric_key: str) -> dict[str, object] | None:
    if not point_rows:
        return None
    return min(
        point_rows,
        key=lambda row: (float(row[metric_key]), float(row["q_mpa"]), int(row["n"])),
    )



def build_metric_rankings(
    points_by_mode: dict[int, list[dict[str, object]]],
) -> tuple[dict[str, list[dict[str, object]]], dict[int, dict[str, int]]]:
    rankings: dict[str, list[dict[str, object]]] = {}
    rank_positions: dict[int, dict[str, int]] = {int(mode): {} for mode in points_by_mode}

    for metric_key, metric_label in METRIC_SPECS:
        metric_rows: list[dict[str, object]] = []
        for mode, point_rows in points_by_mode.items():
            best_row = best_point_for_metric(point_rows, metric_key)
            if best_row is None:
                continue
            row = {
                "n": int(mode),
                "q_mpa": float(best_row["q_mpa"]),
                "value": float(best_row[metric_key]),
                "metric_key": metric_key,
                "metric_label": metric_label,
                "cond_G_amp": float(best_row["cond_G_amp"]),
                "background_seed_kind": str(best_row["background_seed_kind"]),
            }
            if metric_key == "rho_R2":
                row["rho_R2_raw"] = float(best_row["rho_R2_raw"])
            metric_rows.append(row)

        metric_rows.sort(key=lambda row: (float(row["value"]), float(row["q_mpa"]), int(row["n"])))
        for rank, row in enumerate(metric_rows, start=1):
            row["rank"] = int(rank)
            rank_positions[int(row["n"])][metric_key] = int(rank)
        rankings[metric_key] = metric_rows

    return rankings, rank_positions


def main() -> None:
    start_time = time.time()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    background_config = high_bg.default_high_load_background_config()
    load_grid = full_search.default_load_grid(DEFAULT_P_MIN_MPA, DEFAULT_P_MAX_MPA, DEFAULT_P_NPTS)
    modes = tuple(int(mode) for mode in DEFAULT_MODES)
    background_results = high_bg.solve_axisymmetric_simple_support_high_load_schedule(
        load_grid.tolist(),
        config=background_config,
        verbose=False,
    )

    points_by_mode: dict[int, list[dict[str, object]]] = {mode: [] for mode in modes}
    successful_backgrounds = 0
    first_failure: dict[str, object] | None = None

    for background_result in background_results:
        if not background_result.success or background_result.solution is None:
            first_failure = {
                "q_mpa": float(background_result.q_mpa),
                "seed_kind": str(background_result.seed_kind),
                "message": str(background_result.message),
            }
            break

        successful_backgrounds += 1
        for mode in modes:
            obj = full_search.build_boundary_matrix_objects(
                n=mode,
                background_result=background_result,
                x0=float(background_config.x0),
            )
            points_by_mode[mode].append(
                {
                    "n": int(mode),
                    "q_mpa": float(background_result.q_mpa),
                    "sigma_bal": float(obj.sigma_bal),
                    "sigma_Bred_bal": float(obj.sigma_Bred_bal),
                    "rho_R2": float(obj.rho_R2),
                    "rho_R2_raw": float(obj.rho_R2_raw),
                    "cond_G_amp": condition_number(obj.G_amp),
                    "sigma_raw": float(obj.sigma_raw),
                    "sigma_bal_noH": float(obj.sigma_bal_noH),
                    "background_seed_kind": str(background_result.seed_kind),
                }
            )

    best_by_mode: dict[int, dict[str, dict[str, object]]] = {}
    for mode, point_rows in points_by_mode.items():
        metric_best: dict[str, dict[str, object]] = {}
        for metric_key, metric_label in METRIC_SPECS:
            row = best_point_for_metric(point_rows, metric_key)
            if row is None:
                continue
            entry = {
                "metric_key": metric_key,
                "metric_label": metric_label,
                "q_mpa": float(row["q_mpa"]),
                "value": float(row[metric_key]),
                "cond_G_amp": float(row["cond_G_amp"]),
                "background_seed_kind": str(row["background_seed_kind"]),
            }
            if metric_key == "rho_R2":
                entry["rho_R2_raw"] = float(row["rho_R2_raw"])
            metric_best[metric_key] = entry
        best_by_mode[int(mode)] = metric_best

    rankings, rank_positions = build_metric_rankings(points_by_mode)
    ranking_differences: dict[int, dict[str, int | None]] = {}
    for mode in modes:
        mode_ranks = rank_positions.get(int(mode), {})
        base_rank = mode_ranks.get("sigma_bal")
        ranking_differences[int(mode)] = {
            "sigma_bal_rank": base_rank,
            "sigma_Bred_bal_rank": mode_ranks.get("sigma_Bred_bal"),
            "rho_R2_rank": mode_ranks.get("rho_R2"),
            "sigma_Bred_minus_sigma_bal": None if base_rank is None or "sigma_Bred_bal" not in mode_ranks else int(mode_ranks["sigma_Bred_bal"] - base_rank),
            "rho_R2_minus_sigma_bal": None if base_rank is None or "rho_R2" not in mode_ranks else int(mode_ranks["rho_R2"] - base_rank),
        }

    csv_rows: list[dict[str, object]] = []
    for mode in modes:
        metric_best = best_by_mode.get(int(mode), {})
        rank_diff = ranking_differences[int(mode)]
        csv_rows.append(
            {
                "n": int(mode),
                "sigma_bal_best_q_mpa": float(metric_best["sigma_bal"]["q_mpa"]) if "sigma_bal" in metric_best else float("nan"),
                "sigma_bal_best_value": float(metric_best["sigma_bal"]["value"]) if "sigma_bal" in metric_best else float("nan"),
                "sigma_bal_best_cond_G_amp": float(metric_best["sigma_bal"]["cond_G_amp"]) if "sigma_bal" in metric_best else float("nan"),
                "sigma_Bred_bal_best_q_mpa": float(metric_best["sigma_Bred_bal"]["q_mpa"]) if "sigma_Bred_bal" in metric_best else float("nan"),
                "sigma_Bred_bal_best_value": float(metric_best["sigma_Bred_bal"]["value"]) if "sigma_Bred_bal" in metric_best else float("nan"),
                "sigma_Bred_bal_best_cond_G_amp": float(metric_best["sigma_Bred_bal"]["cond_G_amp"]) if "sigma_Bred_bal" in metric_best else float("nan"),
                "rho_R2_best_q_mpa": float(metric_best["rho_R2"]["q_mpa"]) if "rho_R2" in metric_best else float("nan"),
                "rho_R2_best_value": float(metric_best["rho_R2"]["value"]) if "rho_R2" in metric_best else float("nan"),
                "rho_R2_best_raw": float(metric_best["rho_R2"]["rho_R2_raw"]) if "rho_R2" in metric_best else float("nan"),
                "rho_R2_best_cond_G_amp": float(metric_best["rho_R2"]["cond_G_amp"]) if "rho_R2" in metric_best else float("nan"),
                "sigma_bal_rank": rank_diff["sigma_bal_rank"],
                "sigma_Bred_bal_rank": rank_diff["sigma_Bred_bal_rank"],
                "rho_R2_rank": rank_diff["rho_R2_rank"],
                "sigma_Bred_minus_sigma_bal": rank_diff["sigma_Bred_minus_sigma_bal"],
                "rho_R2_minus_sigma_bal": rank_diff["rho_R2_minus_sigma_bal"],
            }
        )

    summary = {
        "method_note": (
            "First practical R2 diagnostic pass for the clean full simple-support path. "
            "The main clean search still uses sigma_bal(B_mix) operationally. "
            "This pilot adds selected-family stacked diagnostics on the same clean architecture: "
            "sigma_bal(B_mix), sigma_Bred_bal with B_red = B_full V_adm, and "
            "rho_R2 = sqrt(lambda_min(V_adm^T (A_int^T A_int + B_full^T W_B B_full) V_adm)). "
            "Pointwise output now also records cond(G_amp) together with rho_R2_raw so the R2 ranking can be read against conditioning."
        ),
        "defaults": {
            "modes": list(modes),
            "p_min_mpa": float(DEFAULT_P_MIN_MPA),
            "p_max_mpa": float(DEFAULT_P_MAX_MPA),
            "p_npts": int(DEFAULT_P_NPTS),
            "row_scale": full_search.ROW_SCALE.tolist(),
        },
        "background_config": dict(background_config.__dict__),
        "successful_background_solves": int(successful_backgrounds),
        "scheduled_load_points": int(load_grid.size),
        "first_background_failure": first_failure,
        "best_by_mode": {str(mode): best_by_mode[int(mode)] for mode in modes},
        "rankings_by_metric": rankings,
        "ranking_differences": {str(mode): ranking_differences[int(mode)] for mode in modes},
        "point_rows": {str(mode): points_by_mode[int(mode)] for mode in modes},
        "runtime_seconds": float(time.time() - start_time),
    }

    with SUMMARY_JSON.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False, allow_nan=True)
        fh.write("\n")

    csv_columns = [
        "n",
        "sigma_bal_best_q_mpa",
        "sigma_bal_best_value",
        "sigma_bal_best_cond_G_amp",
        "sigma_Bred_bal_best_q_mpa",
        "sigma_Bred_bal_best_value",
        "sigma_Bred_bal_best_cond_G_amp",
        "rho_R2_best_q_mpa",
        "rho_R2_best_value",
        "rho_R2_best_raw",
        "rho_R2_best_cond_G_amp",
        "sigma_bal_rank",
        "sigma_Bred_bal_rank",
        "rho_R2_rank",
        "sigma_Bred_minus_sigma_bal",
        "rho_R2_minus_sigma_bal",
    ]
    with SUMMARY_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(csv_rows)

    print("=== Criterion pilot R2 complete ===")
    print(
        "background solves: "
        f"{successful_backgrounds} / {len(background_results)}"
    )
    if first_failure is None:
        print("first background failure: not reached in the scheduled load grid")
    else:
        print(
            "first background failure: "
            f"q={first_failure['q_mpa']:.6f} MPa seed={first_failure['seed_kind']} "
            f"message={first_failure['message']}"
        )

    print("\n=== Best point per mode ===")
    for mode in modes:
        metric_best = best_by_mode.get(int(mode), {})
        print(f"n={mode:02d}")
        for metric_key, metric_label in METRIC_SPECS:
            if metric_key not in metric_best:
                print(f"  {metric_label}: no successful points")
                continue
            entry = metric_best[metric_key]
            extra = ""
            if metric_key == "rho_R2":
                extra = f"  rho_R2_raw={entry['rho_R2_raw']:.6e}"
            print(
                f"  {metric_label}: q={entry['q_mpa']:.6f} MPa  "
                f"value={entry['value']:.6e}  cond(G_amp)={entry['cond_G_amp']:.6e}{extra}  "
                f"seed={entry['background_seed_kind']}"
            )

    print("\n=== Cross-metric rankings ===")
    for metric_key, metric_label in METRIC_SPECS:
        ranking = rankings.get(metric_key, [])
        ranking_text = ", ".join(
            f"#{int(row['rank'])} n={int(row['n'])} @ {float(row['q_mpa']):.6f} MPa ({float(row['value']):.6e})"
            for row in ranking
        )
        print(f"{metric_label}: {ranking_text}")

    print("\n=== Ranking differences vs sigma_bal(B_mix) ===")
    for mode in modes:
        diff = ranking_differences[int(mode)]
        print(
            f"n={mode:02d}: sigma_bal_rank={diff['sigma_bal_rank']}  "
            f"sigma_Bred_bal_rank={diff['sigma_Bred_bal_rank']}  "
            f"rho_R2_rank={diff['rho_R2_rank']}  "
            f"delta_Bred={diff['sigma_Bred_minus_sigma_bal']}  "
            f"delta_R2={diff['rho_R2_minus_sigma_bal']}"
        )

    print(f"\nsummary json: {SUMMARY_JSON}")
    print(f"summary csv:  {SUMMARY_CSV}")
    print(f"runtime:      {summary['runtime_seconds']:.2f} s")


if __name__ == "__main__":
    main()
