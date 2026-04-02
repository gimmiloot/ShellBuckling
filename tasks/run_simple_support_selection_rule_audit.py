# -*- coding: utf-8 -*-
from __future__ import annotations

import csv
import importlib.util
import json
import sys
import time
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.mixed_weak import full_simple_support_critical_search as full_search
from shell_buckling.mixed_weak import simple_support_high_load_background_continuation as high_bg


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


family_sens = load_module(
    "selected_family_sensitivity_task",
    REPO_ROOT / "tasks" / "run_simple_support_selected_family_sensitivity.py",
)

OUTPUT_DIR = REPO_ROOT / "output" / "clean_full_simple_support"
SUMMARY_JSON = OUTPUT_DIR / "selection_rule_audit_summary.json"
SUMMARY_CSV = OUTPUT_DIR / "selection_rule_audit_table.csv"
CURVES_CSV = OUTPUT_DIR / "selection_rule_audit_curves.csv"
PAIR_MODES = (7, 8)
COMMON_WINDOW = {"q_min": 17.20, "q_max": 17.70, "npts": 201}
LOCAL_WINDOWS = {7: {"q_min": 17.20, "q_max": 17.50}, 8: {"q_min": 17.35, "q_max": 17.70}}
SETTINGS = (
    {"label": "baseline", "m_basis": 6, "n_collocation": 120, "nd_base": 4000},
    {"label": "basis_down", "m_basis": 5, "n_collocation": 120, "nd_base": 4000},
    {"label": "basis_up", "m_basis": 7, "n_collocation": 120, "nd_base": 4000},
    {"label": "collocation_down", "m_basis": 6, "n_collocation": 100, "nd_base": 4000},
    {"label": "collocation_up", "m_basis": 6, "n_collocation": 140, "nd_base": 4000},
    {"label": "paired_fine", "m_basis": 7, "n_collocation": 140, "nd_base": 4000},
)
RULES = (
    {"label": "tikhonov_direct_reg_3e-12", "group": "tikhonov_ladder", "kind": "tikhonov", "reg": 3.0e-12},
    {"label": "tikhonov_direct_reg_1e-12", "group": "tikhonov_ladder", "kind": "tikhonov", "reg": 1.0e-12},
    {"label": "tikhonov_direct_reg_3e-13", "group": "tikhonov_ladder", "kind": "tikhonov", "reg": 3.0e-13},
    {"label": "svd_min_norm", "group": "svd_limit", "kind": "svd", "ls_rcond": None},
    {"label": "svd_trunc_rel_1e-10", "group": "svd_limit", "kind": "svd", "ls_rcond": 1.0e-10},
)
AMP_COLUMNS = np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0], [0.0, 0.0]], dtype=float)
TARGET_CENTER_BLOCK = np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0], [0.0, 0.0]], dtype=float)
CONSTRAINT_RCOND = 1.0e-12
EPS = 1.0e-30
BASELINE_RULE = "tikhonov_direct_reg_1e-12"
STABILITY_MARGIN = 0.10


def svd_rank(values: np.ndarray, shape: tuple[int, int], rel_rcond: float | None) -> int:
    if values.size == 0:
        return 0
    tol = max(shape) * np.finfo(float).eps * values[0] if rel_rcond is None else float(rel_rcond) * values[0]
    return int(np.sum(values > tol))


def direct_tikhonov_map(A: np.ndarray, C: np.ndarray, reg: float) -> np.ndarray:
    n_unknowns = A.shape[1]
    n_constraints = C.shape[0]
    ata = A.T @ A + float(reg) * np.eye(n_unknowns, dtype=float)
    kkt = np.block([[ata, C.T], [C, np.zeros((n_constraints, n_constraints), dtype=float)]])
    rhs = np.vstack([np.zeros((n_unknowns, AMP_COLUMNS.shape[1]), dtype=float), AMP_COLUMNS])
    return np.linalg.solve(kkt, rhs)[:n_unknowns, :]


def nullspace_svd_map(A: np.ndarray, C: np.ndarray, ls_rcond: float | None) -> np.ndarray:
    U, s, Vt = np.linalg.svd(np.asarray(C, dtype=float), full_matrices=True)
    rank = svd_rank(s, C.shape, CONSTRAINT_RCOND)
    U_r = U[:, :rank]
    V_r = Vt[:rank, :].T
    particular = V_r @ ((U_r.T @ AMP_COLUMNS) / s[:rank][:, None])
    null_basis = Vt[rank:, :].T
    if null_basis.size == 0:
        return particular
    z, *_ = np.linalg.lstsq(np.asarray(A, dtype=float) @ null_basis, -(np.asarray(A, dtype=float) @ particular), rcond=ls_rcond)
    return particular + null_basis @ np.asarray(z, dtype=float)


def build_vreg(A: np.ndarray, C: np.ndarray, rule: dict[str, object]) -> np.ndarray:
    if str(rule["kind"]) == "tikhonov":
        return direct_tikhonov_map(A, C, float(rule["reg"]))
    return nullspace_svd_map(A, C, rule.get("ls_rcond"))


def build_obj(A: np.ndarray, B: np.ndarray, C: np.ndarray, rule: dict[str, object], ref: dict[str, np.ndarray] | None) -> dict[str, object]:
    C_amp = np.asarray(C[:2, :], dtype=float)
    C_reg = np.asarray(C[2:, :], dtype=float)
    V_reg = build_vreg(A, C, rule)
    G_amp = C_amp @ V_reg
    V_adm = V_reg @ np.linalg.inv(G_amp)
    B_red = B @ V_adm
    W_B = np.diag(full_search.ROW_SCALE**2)
    G_R2 = V_adm.T @ (A.T @ A + B.T @ W_B @ B) @ V_adm
    G_R2 = 0.5 * (G_R2 + G_R2.T)
    rho_raw = float(np.linalg.eigvalsh(G_R2)[0])
    rho = float(np.sqrt(max(rho_raw, 0.0)))
    projector = family_sens.orthonormal_projector(V_adm)
    return {
        "V_adm": V_adm,
        "projector": projector,
        "rho_R2": rho,
        "rho_R2_raw": rho_raw,
        "cond_G_amp": family_sens.condition_number(G_amp),
        "center_identity_residual": float(np.max(np.abs(C @ V_adm - TARGET_CENTER_BLOCK))),
        "reg_identity_residual": float(np.max(np.abs(C_reg @ V_adm))),
        "projector_diff": 0.0 if ref is None else float(np.linalg.norm(projector - ref["projector"], ord="fro")),
        "vadm_diff": 0.0 if ref is None else float(np.linalg.norm(V_adm - ref["V_adm"], ord="fro")),
        "sigma_Bred_bal": family_sens.smallest_singular_value(full_search.balanced_Bmix(B_red)),
    }


def winner(value: float) -> str:
    if not np.isfinite(value) or abs(value) <= EPS:
        return "tie"
    return "n8" if value > 0.0 else "n7"


def internal_agreement(rows: list[dict[str, object]]) -> int:
    total = 0
    for row in rows:
        labels = {str(row["pointwise_winner"]), str(row["signed_area_winner"]), str(row["ahead_fraction_winner"]), str(row["longest_interval_winner"])}
        if len(labels) == 1 and next(iter(labels)) in ("n7", "n8"):
            total += 1
    return total


def near_ties(rows: list[dict[str, object]]) -> int:
    total = 0
    for row in rows:
        frac = float(row["ahead_fraction_n8"])
        signed_area = float(row["signed_area_n8_minus_n7"])
        absolute_area = float(row["absolute_area"])
        if abs(frac - 0.5) <= 0.03 or (absolute_area > EPS and abs(signed_area) / absolute_area <= STABILITY_MARGIN):
            total += 1
    return total


def stability_fraction(rows: list[dict[str, object]], key: str) -> float:
    counts: dict[str, int] = {}
    for row in rows:
        label = str(row[key])
        counts[label] = counts.get(label, 0) + 1
    return float(max(counts.values()) / max(len(rows), 1))


def main() -> None:
    start_time = time.time()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    background_config = high_bg.default_high_load_background_config()
    q_grid = family_sens.make_grid(COMMON_WINDOW["q_min"], COMMON_WINDOW["q_max"], COMMON_WINDOW["npts"])
    backgrounds, background_method = family_sens.solve_window_backgrounds(q_grid, config=background_config)
    summary = {
        "method_note": "Selection-rule audit for the clean full simple-support path. Representation-only basis choices are factored out; nearby selected-family rules are compared through direct amplitude maps before canonical rebasing.",
        "current_rule_interpretation": {
            "formula": "min ||A_int c||^2 + reg ||c||^2 subject to C_center c = d",
            "split": {
                "amplitude_constraints": "C_center fixes the two leading amplitudes and enforces the two regularity rows.",
                "interior_selector": "The chosen family minimizes the interior weak residual inside that affine constraint class.",
                "regularization_artifact": "The Tikhonov reg term is recipe-dependent, not theorem-canonical.",
                "rebasing": "V_adm = V_reg (C_amp V_reg)^(-1) is canonical once the span is chosen.",
            },
            "audit_reading": "This task compares rules through their direct amplitude maps, so raw normalization and orthogonalization choices are intentionally removed from the comparison.",
        },
        "background_method": background_method,
        "background_config": dict(background_config.__dict__),
        "common_window": dict(COMMON_WINDOW),
        "local_windows": dict(LOCAL_WINDOWS),
        "settings": [dict(item) for item in SETTINGS],
        "rules": [dict(item) for item in RULES],
        "setting_rule_overview": {},
        "rule_across_settings": {},
    }
    table_rows: list[dict[str, object]] = []
    curve_rows: list[dict[str, object]] = []

    for setting in SETTINGS:
        setting_label = str(setting["label"])
        cache: dict[tuple[int, float], tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
        for mode in PAIR_MODES:
            for q_mpa, background in zip(q_grid, backgrounds):
                base = full_search.build_full_simple_support_base_interp(background.solution, q_mpa=float(q_mpa), nd_base=int(setting["nd_base"]))
                space, _x_col, A, B = full_search.assemble_interior_and_boundary(
                    n=int(mode),
                    base=base,
                    x0=float(background_config.x0),
                    m_basis=int(setting["m_basis"]),
                    n_collocation=int(setting["n_collocation"]),
                )
                C = full_search.make_center_constraint_matrix(space, base)
                cache[(int(mode), float(q_mpa))] = (np.asarray(A, dtype=float), np.asarray(B, dtype=float), np.asarray(C, dtype=float))

        baseline_rule = next(rule for rule in RULES if str(rule["label"]) == BASELINE_RULE)
        refs: dict[tuple[int, float], dict[str, np.ndarray]] = {}
        for mode in PAIR_MODES:
            for q_mpa in q_grid:
                A, B, C = cache[(int(mode), float(q_mpa))]
                obj = build_obj(A, B, C, baseline_rule, None)
                refs[(int(mode), float(q_mpa))] = {"V_adm": np.asarray(obj["V_adm"], dtype=float), "projector": np.asarray(obj["projector"], dtype=float)}

        summary["setting_rule_overview"][setting_label] = {}
        for rule in RULES:
            rows_by_mode = {7: [], 8: []}
            for mode in PAIR_MODES:
                for q_mpa in q_grid:
                    A, B, C = cache[(int(mode), float(q_mpa))]
                    obj = build_obj(A, B, C, rule, refs[(int(mode), float(q_mpa))])
                    obj["q_mpa"] = float(q_mpa)
                    rows_by_mode[int(mode)].append(obj)
            rows7 = rows_by_mode[7]
            rows8 = rows_by_mode[8]
            best7 = family_sens.best_row_in_window(rows7, q_min=LOCAL_WINDOWS[7]["q_min"], q_max=LOCAL_WINDOWS[7]["q_max"])
            best8 = family_sens.best_row_in_window(rows8, q_min=LOCAL_WINDOWS[8]["q_min"], q_max=LOCAL_WINDOWS[8]["q_max"])
            q = np.asarray([float(row["q_mpa"]) for row in rows7], dtype=float)
            rho7 = np.asarray([float(row["rho_R2"]) for row in rows7], dtype=float)
            rho8 = np.asarray([float(row["rho_R2"]) for row in rows8], dtype=float)
            cond7 = np.asarray([float(row["cond_G_amp"]) for row in rows7], dtype=float)
            cond8 = np.asarray([float(row["cond_G_amp"]) for row in rows8], dtype=float)
            proj7 = np.asarray([float(row["projector_diff"]) for row in rows7], dtype=float)
            proj8 = np.asarray([float(row["projector_diff"]) for row in rows8], dtype=float)
            vadm7 = np.asarray([float(row["vadm_diff"]) for row in rows7], dtype=float)
            vadm8 = np.asarray([float(row["vadm_diff"]) for row in rows8], dtype=float)
            advantage_n8 = rho7 - rho8
            signed_area = float(np.trapezoid(advantage_n8, q))
            absolute_area = float(np.trapezoid(np.abs(advantage_n8), q))
            n8_segments = family_sens.collect_sign_segments(q, advantage_n8, positive=True)
            n7_segments = family_sens.collect_sign_segments(q, advantage_n8, positive=False)
            window_length = float(q[-1] - q[0])
            ahead_fraction_n8 = float(sum(item[2] for item in n8_segments) / max(window_length, EPS))
            ahead_fraction_n7 = float(sum(item[2] for item in n7_segments) / max(window_length, EPS))
            longest_n8 = float(max((item[2] for item in n8_segments), default=0.0))
            longest_n7 = float(max((item[2] for item in n7_segments), default=0.0))
            pointwise_gap = float(best8["rho_R2"] - best7["rho_R2"])
            row = {
                "setting": setting_label,
                "m_basis": int(setting["m_basis"]),
                "n_collocation": int(setting["n_collocation"]),
                "rule": str(rule["label"]),
                "family_group": str(rule["group"]),
                "best_n7_q_mpa": float(best7["q_mpa"]),
                "best_n7_rho_R2": float(best7["rho_R2"]),
                "best_n7_cond_G_amp": float(best7["cond_G_amp"]),
                "best_n8_q_mpa": float(best8["q_mpa"]),
                "best_n8_rho_R2": float(best8["rho_R2"]),
                "best_n8_cond_G_amp": float(best8["cond_G_amp"]),
                "pointwise_gap_n8_minus_n7": pointwise_gap,
                "pointwise_winner": winner(-pointwise_gap),
                "signed_area_n8_minus_n7": signed_area,
                "absolute_area": absolute_area,
                "signed_area_winner": winner(signed_area),
                "ahead_fraction_n8": ahead_fraction_n8,
                "ahead_fraction_n7": ahead_fraction_n7,
                "ahead_fraction_winner": "n8" if ahead_fraction_n8 > ahead_fraction_n7 else "n7" if ahead_fraction_n7 > ahead_fraction_n8 else "tie",
                "longest_interval_n8_mpa": longest_n8,
                "longest_interval_n7_mpa": longest_n7,
                "longest_interval_winner": "n8" if longest_n8 > longest_n7 else "n7" if longest_n7 > longest_n8 else "tie",
                "mean_projector_diff_n7": float(np.mean(proj7)),
                "max_projector_diff_n7": float(np.max(proj7)),
                "mean_projector_diff_n8": float(np.mean(proj8)),
                "max_projector_diff_n8": float(np.max(proj8)),
                "mean_vadm_diff_n7": float(np.mean(vadm7)),
                "max_vadm_diff_n7": float(np.max(vadm7)),
                "mean_vadm_diff_n8": float(np.mean(vadm8)),
                "max_vadm_diff_n8": float(np.max(vadm8)),
                "max_center_identity_residual": float(max(max(float(item["center_identity_residual"]) for item in rows7), max(float(item["center_identity_residual"]) for item in rows8))),
                "max_reg_identity_residual": float(max(max(float(item["reg_identity_residual"]) for item in rows7), max(float(item["reg_identity_residual"]) for item in rows8))),
                "max_cond_G_amp": float(max(np.max(cond7), np.max(cond8))),
            }
            table_rows.append(row)
            summary["setting_rule_overview"][setting_label][str(rule["label"])] = {
                "pointwise_winner": row["pointwise_winner"],
                "signed_area_winner": row["signed_area_winner"],
                "ahead_fraction_winner": row["ahead_fraction_winner"],
                "longest_interval_winner": row["longest_interval_winner"],
                "max_projector_diff_to_current": float(max(row["max_projector_diff_n7"], row["max_projector_diff_n8"])),
                "max_center_identity_residual": row["max_center_identity_residual"],
                "max_reg_identity_residual": row["max_reg_identity_residual"],
            }
            for idx, q_mpa in enumerate(q):
                curve_rows.append({
                    "setting": setting_label,
                    "rule": str(rule["label"]),
                    "family_group": str(rule["group"]),
                    "q_mpa": float(q_mpa),
                    "rho_R2_n7": float(rho7[idx]),
                    "rho_R2_n8": float(rho8[idx]),
                    "advantage_n8_minus_n7": float(advantage_n8[idx]),
                    "cond_G_amp_n7": float(cond7[idx]),
                    "cond_G_amp_n8": float(cond8[idx]),
                    "projector_diff_n7": float(proj7[idx]),
                    "projector_diff_n8": float(proj8[idx]),
                    "vadm_diff_n7": float(vadm7[idx]),
                    "vadm_diff_n8": float(vadm8[idx]),
                })

    for rule in RULES:
        label = str(rule["label"])
        rows = [row for row in table_rows if str(row["rule"]) == label]
        summary["rule_across_settings"][label] = {
            "pointwise_winners": [str(row["pointwise_winner"]) for row in rows],
            "signed_area_winners": [str(row["signed_area_winner"]) for row in rows],
            "ahead_fraction_winners": [str(row["ahead_fraction_winner"]) for row in rows],
            "longest_interval_winners": [str(row["longest_interval_winner"]) for row in rows],
            "pointwise_stability_fraction": stability_fraction(rows, "pointwise_winner"),
            "signed_area_stability_fraction": stability_fraction(rows, "signed_area_winner"),
            "ahead_fraction_stability_fraction": stability_fraction(rows, "ahead_fraction_winner"),
            "internal_full_agreement_count": internal_agreement(rows),
            "near_tie_count": near_ties(rows),
            "max_projector_diff_to_current": float(max(max(float(row["max_projector_diff_n7"]), float(row["max_projector_diff_n8"])) for row in rows)),
        }

    baseline_reg_probe = [row for row in table_rows if str(row["setting"]) == "baseline" and str(row["rule"]).startswith("tikhonov_direct_reg_")]
    baseline_reg_probe.sort(key=lambda row: float(next(rule["reg"] for rule in RULES if str(rule["label"]) == str(row["rule"]))), reverse=True)
    summary["reg_to_zero_baseline_probe"] = [
        {
            "rule": str(row["rule"]),
            "pointwise_winner": str(row["pointwise_winner"]),
            "signed_area_winner": str(row["signed_area_winner"]),
            "ahead_fraction_winner": str(row["ahead_fraction_winner"]),
            "signed_area_n8_minus_n7": float(row["signed_area_n8_minus_n7"]),
            "ahead_fraction_n8": float(row["ahead_fraction_n8"]),
            "max_projector_diff_to_current": float(max(float(row["max_projector_diff_n7"]), float(row["max_projector_diff_n8"]))),
        }
        for row in baseline_reg_probe
    ]

    svd_rows = [row for row in table_rows if str(row["family_group"]) == "svd_limit"]
    current_rows = [row for row in table_rows if str(row["rule"]) == BASELINE_RULE]
    svd_pointwise_consistent = all(str(row["pointwise_winner"]) == str(svd_rows[0]["pointwise_winner"]) for row in svd_rows)
    svd_area_consistent = all(str(row["signed_area_winner"]) == str(svd_rows[0]["signed_area_winner"]) for row in svd_rows)
    svd_ahead_consistent = all(str(row["ahead_fraction_winner"]) == str(svd_rows[0]["ahead_fraction_winner"]) for row in svd_rows)
    current_area_flips = sum(1 for row in current_rows if str(row["signed_area_winner"]) != str(current_rows[0]["signed_area_winner"]))
    svd_internal_agreement = max(summary["rule_across_settings"]["svd_min_norm"]["internal_full_agreement_count"], summary["rule_across_settings"]["svd_trunc_rel_1e-10"]["internal_full_agreement_count"])
    svd_near_ties = near_ties(svd_rows)
    svd_max_projector_diff = max(max(float(row["max_projector_diff_n7"]), float(row["max_projector_diff_n8"])) for row in svd_rows)

    if svd_pointwise_consistent and svd_area_consistent and svd_ahead_consistent and svd_internal_agreement >= 5 and svd_near_ties <= 1:
        decision = "C"
        conclusion = "one nearby selection rule looks materially more canonical and stable: the nullspace-SVD constrained solve is the best next diagnostic baseline"
        recommendation = "nominate the nullspace-SVD constrained solve for deeper follow-up"
    elif current_area_flips > 0 and svd_max_projector_diff > 0.02:
        decision = "B"
        conclusion = "the current Tikhonov-based selector is too recipe-sensitive for criterion conclusions; small reg changes move the selected family materially"
        recommendation = "mark the current rule as not criterion-authoritative and treat it only as one exploratory selector"
    else:
        decision = "A"
        conclusion = "ambiguity persists across plausible nearby selection rules, so the selection layer itself remains unresolved"
        recommendation = "keep the current rule only as one diagnostic; no nearby rule is yet strong enough to promote"

    summary["decision"] = {
        "code": decision,
        "conclusion": conclusion,
        "recommendation": recommendation,
        "svd_rule_consistency": {"pointwise": svd_pointwise_consistent, "signed_area": svd_area_consistent, "ahead_fraction": svd_ahead_consistent, "near_tie_count": svd_near_ties},
        "current_rule_area_flip_count": int(current_area_flips),
    }
    summary["runtime_seconds"] = float(time.time() - start_time)

    with SUMMARY_JSON.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False, allow_nan=True)
        fh.write("\n")

    summary_cols = [
        "setting", "m_basis", "n_collocation", "rule", "family_group", "best_n7_q_mpa", "best_n7_rho_R2", "best_n7_cond_G_amp",
        "best_n8_q_mpa", "best_n8_rho_R2", "best_n8_cond_G_amp", "pointwise_gap_n8_minus_n7", "pointwise_winner", "signed_area_n8_minus_n7",
        "absolute_area", "signed_area_winner", "ahead_fraction_n8", "ahead_fraction_n7", "ahead_fraction_winner", "longest_interval_n8_mpa",
        "longest_interval_n7_mpa", "longest_interval_winner", "mean_projector_diff_n7", "max_projector_diff_n7", "mean_projector_diff_n8", "max_projector_diff_n8",
        "mean_vadm_diff_n7", "max_vadm_diff_n7", "mean_vadm_diff_n8", "max_vadm_diff_n8", "max_center_identity_residual", "max_reg_identity_residual", "max_cond_G_amp",
    ]
    with SUMMARY_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=summary_cols)
        writer.writeheader()
        writer.writerows(table_rows)

    curve_cols = ["setting", "rule", "family_group", "q_mpa", "rho_R2_n7", "rho_R2_n8", "advantage_n8_minus_n7", "cond_G_amp_n7", "cond_G_amp_n8", "projector_diff_n7", "projector_diff_n8", "vadm_diff_n7", "vadm_diff_n8"]
    with CURVES_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=curve_cols)
        writer.writeheader()
        writer.writerows(curve_rows)

    print("=== Selection-rule audit complete ===")
    for rule in RULES:
        label = str(rule["label"])
        across = summary["rule_across_settings"][label]
        print(f"{label}: pointwise={across['pointwise_winners']} | area={across['signed_area_winners']} | ahead={across['ahead_fraction_winners']} | internal_agreement={across['internal_full_agreement_count']}/6 | near_ties={across['near_tie_count']}")
    print("decision: " + decision)
    print("conclusion: " + conclusion)
    print("recommendation: " + recommendation)
    print(f"summary json: {SUMMARY_JSON}")
    print(f"summary csv:  {SUMMARY_CSV}")
    print(f"curves csv:   {CURVES_CSV}")
    print(f"runtime:      {summary['runtime_seconds']:.2f} s")


if __name__ == "__main__":
    main()
