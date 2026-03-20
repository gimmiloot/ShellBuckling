from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import inspect
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from shell_buckling.mixed_weak import boundary_matrix_scan as broad_scan
from shell_buckling.mixed_weak import boundary_matrix_targeted_scan as targeted_scan


ND_BVP = 1400
X0 = 1.0e-3
TOL = 1.0e-4
MAX_NODES = 150000
SMALL_NORM = 1.0e-12
REFINED_SPREAD_LIMIT = 0.25
TARGETED_SPREAD_LIMIT = 0.05
RESOLUTION_SPREAD_LIMIT = 0.50


@dataclass
class WindowResult:
    workflow: str
    module_name: str
    case_label: str
    mode: int
    iterations: int
    p_best_raw: float
    sigma_best_raw: float
    p_best_bal: float
    sigma_best_bal: float
    p_best_bal_noh: float
    sigma_best_bal_noh: float


def print_check(name: str, ok: bool, detail: str) -> bool:
    print(f"[{name}] {'PASS' if ok else 'FAIL'}")
    print(f"  {detail}")
    return ok


def best_point(p_grid: np.ndarray, arr: np.ndarray) -> tuple[float, float, int]:
    arr = np.asarray(arr, dtype=float)
    i_best = int(np.argmin(arr))
    return float(p_grid[i_best]), float(arr[i_best]), i_best


def spread(values: list[float]) -> float:
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        return float("inf")
    return float(np.max(arr) - np.min(arr))


def source_guard() -> bool:
    ok_all = True

    broad_src = inspect.getsource(broad_scan)
    targeted_src = inspect.getsource(targeted_scan)
    task_broad = (ROOT / "tasks" / "run_mixed_weak_boundary_matrix_scan.py").read_text(encoding="utf-8")
    task_targeted = (ROOT / "tasks" / "run_mixed_weak_targeted_scan.py").read_text(encoding="utf-8")

    checks = [
        (
            "broad scan computes sigma_Bmix from singular values of B_mix",
            "sigma_Bmix = float(np.linalg.svd(B_mix, compute_uv=False)[-1])" in broad_src,
        ),
        (
            "targeted scan computes sigma_Bmix from singular values of B_mix",
            "sigma_Bmix = float(np.linalg.svd(B_mix, compute_uv=False)[-1])" in targeted_src,
        ),
        (
            "broad scan exposes raw and balanced metric extraction",
            "sigma_raw" in broad_src and "sigma_bal" in broad_src and "sigma_bal_noH" in broad_src,
        ),
        (
            "broad scan main includes fine and adaptive workflow hooks",
            "run_fine_scan" in broad_src and "run_adaptive_scan" in broad_src,
        ),
        (
            "targeted scan main includes targeted workflow hook",
            "run_targeted_local_scan" in targeted_src,
        ),
        (
            "task entry points launch the active mixed-weak scan modules",
            "boundary_matrix_scan import main" in task_broad and "boundary_matrix_targeted_scan import main" in task_targeted,
        ),
    ]

    print("Source guard for the current working criterion path:")
    for label, ok in checks:
        ok_all &= ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    print()
    return ok_all


def solve_baseline_family(scan_module) -> tuple[np.ndarray, list[Any]]:
    p_grid = np.linspace(0.0, scan_module.BASELINE_P_MAX_MPA, scan_module.BASELINE_P_NPTS)
    _, sols = scan_module.mw.solve_axisymmetric_fmin_continuation(
        p_grid,
        nd_bvp=ND_BVP,
        x0=X0,
        tol=TOL,
        max_nodes=MAX_NODES,
        verbose=False,
    )
    return p_grid, sols


def matrix_health(objs: dict[int, Any]) -> dict[str, float | bool]:
    sigma_max_values = []
    fro_values = []
    row_max_values = []
    finite_ok = True

    for obj in objs.values():
        B = np.asarray(obj.B_mix, dtype=float)
        svals = np.linalg.svd(B, compute_uv=False)
        sigma_max_values.append(float(svals[0]))
        fro_values.append(float(np.linalg.norm(B)))
        row_max_values.append(float(np.max(np.linalg.norm(B, axis=1))))
        finite_ok &= bool(np.all(np.isfinite(B)) and np.all(np.isfinite(svals)))

    return {
        "finite_ok": finite_ok,
        "min_sigma_max": float(np.min(sigma_max_values)),
        "min_fro": float(np.min(fro_values)),
        "min_row_max": float(np.min(row_max_values)),
    }


def run_broad_baseline() -> tuple[dict[int, dict[str, np.ndarray]], np.ndarray, list[Any], dict[str, Any]]:
    p_grid, sols = solve_baseline_family(broad_scan)

    metrics_by_n: dict[int, dict[str, np.ndarray]] = {}
    broad_summary: list[tuple[int, float, float, float, float]] = []
    broad_health_by_n: dict[int, dict[str, float | bool]] = {}

    for n in broad_scan.BASELINE_MODES:
        _sigs, objs = broad_scan.scan_p_for_n_boundary_matrix_v2(
            p_grid,
            sols,
            n=n,
            x0=X0,
            m_basis=6,
            n_collocation=120,
            verbose=False,
        )
        metrics = broad_scan.extract_metrics_from_objects(objs)
        metrics_by_n[n] = metrics
        broad_health_by_n[n] = matrix_health(objs)

        p_raw, sig_raw, _ = best_point(p_grid, metrics["sigma_raw"])
        p_bal, sig_bal, _ = best_point(p_grid, metrics["sigma_bal"])
        broad_summary.append((n, p_raw, sig_raw, p_bal, sig_bal))

    overall_health = {
        "all_finite": all(bool(health["finite_ok"]) for health in broad_health_by_n.values()),
        "min_sigma_max": min(float(health["min_sigma_max"]) for health in broad_health_by_n.values()),
        "min_fro": min(float(health["min_fro"]) for health in broad_health_by_n.values()),
        "min_row_max": min(float(health["min_row_max"]) for health in broad_health_by_n.values()),
    }

    return metrics_by_n, p_grid, sols, {"summary": broad_summary, "health": overall_health}


def run_fixed_windows(
    workflow: str,
    scan_module,
    case_list: list[tuple[int, int]],
    windows: dict[int, tuple[float, float]],
    baseline_p_grid: np.ndarray,
    baseline_sols: list[Any],
    npts: int,
) -> list[WindowResult]:
    results: list[WindowResult] = []
    for m_basis, n_collocation in case_list:
        case_label = f"m_basis={m_basis}, n_collocation={n_collocation}"
        for n in sorted(windows.keys()):
            p_lo, p_hi = windows[n]
            p_grid = np.linspace(float(p_lo), float(p_hi), int(npts))
            _, sols = scan_module.solve_axisymmetric_window_seeded(
                p_grid,
                baseline_p_grid=np.asarray(baseline_p_grid, dtype=float),
                baseline_sols=baseline_sols,
                nd_bvp=ND_BVP,
                x0=X0,
                tol=TOL,
                max_nodes=MAX_NODES,
            )
            _sigs, objs = scan_module.scan_p_for_n_boundary_matrix_v2(
                p_grid,
                sols,
                n=n,
                x0=X0,
                m_basis=m_basis,
                n_collocation=n_collocation,
                verbose=False,
            )
            metrics = scan_module.extract_metrics_from_objects(objs)
            p_raw, sig_raw, _ = best_point(p_grid, metrics["sigma_raw"])
            p_bal, sig_bal, _ = best_point(p_grid, metrics["sigma_bal"])
            p_bal_noh, sig_bal_noh, _ = best_point(p_grid, metrics["sigma_bal_noH"])
            results.append(
                WindowResult(
                    workflow=workflow,
                    module_name=scan_module.__name__,
                    case_label=case_label,
                    mode=n,
                    iterations=1,
                    p_best_raw=p_raw,
                    sigma_best_raw=sig_raw,
                    p_best_bal=p_bal,
                    sigma_best_bal=sig_bal,
                    p_best_bal_noh=p_bal_noh,
                    sigma_best_bal_noh=sig_bal_noh,
                )
            )
    return results

def run_adaptive_like(
    workflow: str,
    scan_module,
    case_list: list[tuple[int, int]],
    windows0: dict[int, tuple[float, float]],
    baseline_p_grid: np.ndarray,
    baseline_sols: list[Any],
    npts: int,
    max_iters: int,
    edge_pad: int,
) -> list[WindowResult]:
    results: list[WindowResult] = []
    for m_basis, n_collocation in case_list:
        case_label = f"m_basis={m_basis}, n_collocation={n_collocation}"
        for n in sorted(windows0.keys()):
            p_lo, p_hi = windows0[n]
            final_result: WindowResult | None = None
            for it in range(max_iters):
                p_grid = np.linspace(float(p_lo), float(p_hi), npts)
                _, sols = scan_module.solve_axisymmetric_window_seeded(
                    p_grid,
                    baseline_p_grid=np.asarray(baseline_p_grid, dtype=float),
                    baseline_sols=baseline_sols,
                    nd_bvp=ND_BVP,
                    x0=X0,
                    tol=TOL,
                    max_nodes=MAX_NODES,
                )
                _sigs, objs = scan_module.scan_p_for_n_boundary_matrix_v2(
                    p_grid,
                    sols,
                    n=n,
                    x0=X0,
                    m_basis=m_basis,
                    n_collocation=n_collocation,
                    verbose=False,
                )
                metrics = scan_module.extract_metrics_from_objects(objs)
                p_raw, sig_raw, _ = best_point(p_grid, metrics["sigma_raw"])
                p_bal, sig_bal, _ = best_point(p_grid, metrics["sigma_bal"])
                p_bal_noh, sig_bal_noh, _ = best_point(p_grid, metrics["sigma_bal_noH"])
                final_result = WindowResult(
                    workflow=workflow,
                    module_name=scan_module.__name__,
                    case_label=case_label,
                    mode=n,
                    iterations=it + 1,
                    p_best_raw=p_raw,
                    sigma_best_raw=sig_raw,
                    p_best_bal=p_bal,
                    sigma_best_bal=sig_bal,
                    p_best_bal_noh=p_bal_noh,
                    sigma_best_bal_noh=sig_bal_noh,
                )
                (new_lo, new_hi), status, _i_best = scan_module.shift_window_if_edge_hit(
                    p_grid, metrics["sigma_bal"], edge_pad=edge_pad
                )
                if status == "interior":
                    break
                p_lo, p_hi = new_lo, new_hi
            if final_result is None:
                raise RuntimeError(f"{workflow} scan failed to produce a result for n={n}")
            results.append(final_result)
    return results


def print_window_results(title: str, results: list[WindowResult]) -> None:
    print(title)
    for result in results:
        print(
            f"  {result.workflow:8s} | {result.case_label:31s} | n={result.mode:02d} | "
            f"iters={result.iterations} | raw: p_best={result.p_best_raw:.6f} MPa, sigma={result.sigma_best_raw:.6e} | "
            f"balanced: p_best={result.p_best_bal:.6f} MPa, sigma={result.sigma_best_bal:.6e} | "
            f"balanced-noH: p_best={result.p_best_bal_noh:.6f} MPa, sigma={result.sigma_best_bal_noh:.6e}"
        )
    print()


def mode_spreads(results: list[WindowResult], mode: int) -> dict[str, float]:
    raw_values = [result.p_best_raw for result in results if result.mode == mode]
    bal_values = [result.p_best_bal for result in results if result.mode == mode]
    return {
        "raw_spread": spread(raw_values),
        "balanced_spread": spread(bal_values),
    }


def old_architecture_evidence() -> dict[str, Any]:
    legacy_names = [
        "fmin_reduced_solver_v1.py",
        "fmin_full_solver_v2.py",
        "fmin_full_solver_v3_chernykh.py",
    ]
    legacy_found = []
    for name in legacy_names:
        legacy_found.extend(ROOT.rglob(name))

    journal_text = (ROOT / "docs" / "journal" / "project_journal_updated14.md").read_text(encoding="utf-8")
    theory_text = (ROOT / "docs" / "theory" / "vyvod_uravneniy_updated17.md").read_text(encoding="utf-8")
    supporting_det = (ROOT / "src" / "shell_buckling" / "supporting" / "determinant_criterion_comparison.py").exists()

    doc_checks = {
        "journal_names_old_architecture": all(token in journal_text for token in ["F_min_reduced", "F_min_full_v2", "F_min_full_v3_chernykh"]),
        "journal_records_p0_failure": "p=0" in journal_text,
        "journal_records_no_qualitative_shift": "qualitative shift" in journal_text,
        "theory_records_old_negative_result": (all(token in theory_text for token in ["F_min_reduced", "F_min_full_v2", "F_min_full_v3_chernykh"]) and ("\u043d\u0435 \u0434\u0430\u043b\u0438 \u043a\u0430\u0447\u0435\u0441\u0442\u0432\u0435\u043d\u043d\u043e \u043d\u043e\u0432\u043e\u0433\u043e \u043a\u0440\u0438\u0442\u0435\u0440\u0438\u044f" in theory_text or "\u0421\u0442\u0430\u0440\u0430\u044f reduced/full \u0430\u0440\u0445\u0438\u0442\u0435\u043a\u0442\u0443\u0440\u0430 \u043a\u0430\u043a \u043e\u0441\u043d\u043e\u0432\u043d\u043e\u0439 \u043f\u0443\u0442\u044c \u0438\u0441\u0447\u0435\u0440\u043f\u0430\u043d\u0430" in theory_text)),
        "theory_records_current_refined_scan_workflow": all(token in theory_text for token in ["resolution study", "fine scan", "adaptive tracking", "targeted scan"]),
    }
    return {
        "legacy_found": legacy_found,
        "supporting_det_exists": supporting_det,
        "doc_checks": doc_checks,
    }


def main() -> int:
    print("Pilot 05: sigma_min(B_mix) as working criterion")
    print()
    print("Expected result for this pilot:")
    print("  sigma_min(B_mix) should be computable in the live mixed-weak workflow;")
    print("  refined local scans should reproduce the current candidate neighborhoods well enough for exploratory use;")
    print("  but if coarse / resolution-level behavior still shifts noticeably, V-N1 may remain only partially confirmed.")
    print()

    src_ok = source_guard()

    print("A. Computability")
    metrics_by_n, broad_p_grid, broad_sols, broad_data = run_broad_baseline()
    print("Broad baseline summary (raw vs balanced best points by mode):")
    for n, p_raw, sig_raw, p_bal, sig_bal in broad_data["summary"]:
        print(
            f"  n={n:02d} | raw: p_best={p_raw:.3f} MPa, sigma={sig_raw:.6e} | "
            f"balanced: p_best={p_bal:.3f} MPa, sigma={sig_bal:.6e}"
        )
    print()

    health = broad_data["health"]
    computable_ok = all(
        [
            src_ok,
            bool(health["all_finite"]),
            float(health["min_sigma_max"]) > SMALL_NORM,
            float(health["min_fro"]) > SMALL_NORM,
            float(health["min_row_max"]) > SMALL_NORM,
        ]
    )
    print_check(
        "computability over active broad q-range",
        computable_ok,
        f"all_finite={health['all_finite']}, min sigma_max={float(health['min_sigma_max']):.6e}, "
        f"min ||B_mix||_F={float(health['min_fro']):.6e}, min max-row-norm={float(health['min_row_max']):.6e}",
    )
    print()

    print("B. Scan consistency")
    fine_results = run_fixed_windows(
        workflow="fine",
        scan_module=broad_scan,
        case_list=list(broad_scan.FINE_SCAN_CASES),
        windows=dict(broad_scan.FINE_SCAN_WINDOWS),
        baseline_p_grid=broad_p_grid,
        baseline_sols=broad_sols,
        npts=int(broad_scan.FINE_SCAN_NPTS),
    )
    adaptive_results = run_adaptive_like(
        workflow="adaptive",
        scan_module=broad_scan,
        case_list=list(broad_scan.ADAPTIVE_SCAN_CASES),
        windows0=dict(broad_scan.ADAPTIVE_SCAN_WINDOWS),
        baseline_p_grid=broad_p_grid,
        baseline_sols=broad_sols,
        npts=int(broad_scan.ADAPTIVE_SCAN_NPTS),
        max_iters=int(broad_scan.ADAPTIVE_SCAN_MAX_ITERS),
        edge_pad=int(broad_scan.ADAPTIVE_EDGE_PAD),
    )

    targeted_p_grid, targeted_sols = solve_baseline_family(targeted_scan)
    targeted_results = run_adaptive_like(
        workflow="targeted",
        scan_module=targeted_scan,
        case_list=list(targeted_scan.TARGETED_CASES),
        windows0=dict(targeted_scan.TARGETED_WINDOWS0),
        baseline_p_grid=targeted_p_grid,
        baseline_sols=targeted_sols,
        npts=int(targeted_scan.TARGETED_NPTS),
        max_iters=int(targeted_scan.TARGETED_MAX_ITERS),
        edge_pad=int(targeted_scan.TARGETED_EDGE_PAD),
    )

    print_window_results("Fine-scan results:", fine_results)
    print_window_results("Adaptive-scan results:", adaptive_results)
    print_window_results("Targeted-scan results:", targeted_results)

    refined_results = fine_results + adaptive_results + targeted_results
    spreads_refined_13 = mode_spreads(refined_results, 13)
    spreads_refined_14 = mode_spreads(refined_results, 14)
    targeted_spreads_13 = mode_spreads(targeted_results, 13)
    targeted_spreads_14 = mode_spreads(targeted_results, 14)

    refined_consistency_ok = (
        spreads_refined_13["raw_spread"] <= REFINED_SPREAD_LIMIT
        and spreads_refined_14["raw_spread"] <= REFINED_SPREAD_LIMIT
        and targeted_spreads_13["raw_spread"] <= TARGETED_SPREAD_LIMIT
        and targeted_spreads_14["raw_spread"] <= TARGETED_SPREAD_LIMIT
    )
    print_check(
        "refined fine/adaptive/targeted raw minima remain in moderate candidate neighborhoods",
        refined_consistency_ok,
        f"n=13 refined raw spread={spreads_refined_13['raw_spread']:.6f} MPa, "
        f"n=14 refined raw spread={spreads_refined_14['raw_spread']:.6f} MPa, "
        f"targeted spreads=({targeted_spreads_13['raw_spread']:.6f}, {targeted_spreads_14['raw_spread']:.6f}) MPa",
    )
    print()

    print("C. Sensitivity / robustness")
    resolution_results = run_fixed_windows(
        workflow="resolution",
        scan_module=broad_scan,
        case_list=list(broad_scan.RESOLUTION_CASES),
        windows=dict(broad_scan.RESOLUTION_WINDOWS),
        baseline_p_grid=broad_p_grid,
        baseline_sols=broad_sols,
        npts=int(broad_scan.RESOLUTION_NPTS),
    )
    print_window_results("Resolution-study results:", resolution_results)

    spreads_resolution_13 = mode_spreads(resolution_results, 13)
    spreads_resolution_14 = mode_spreads(resolution_results, 14)
    sensitivity_ok = (
        spreads_resolution_13["raw_spread"] <= RESOLUTION_SPREAD_LIMIT
        and spreads_resolution_14["raw_spread"] <= RESOLUTION_SPREAD_LIMIT
    )
    print_check(
        "modest resolution changes do not break the raw criterion completely",
        sensitivity_ok,
        f"resolution raw spreads: n=13 -> {spreads_resolution_13['raw_spread']:.6f} MPa, "
        f"n=14 -> {spreads_resolution_14['raw_spread']:.6f} MPa",
    )
    print()

    print("D. Qualitative novelty")
    old_evidence = old_architecture_evidence()
    legacy_found = old_evidence["legacy_found"]
    doc_checks = old_evidence["doc_checks"]

    if legacy_found:
        print("Direct live comparison to the old reduced/full architecture is available in this checkout.")
        for path in legacy_found:
            print(f"  found: {path.relative_to(ROOT)}")
    else:
        print("Direct live comparison to the old reduced/full architecture is not practical in this checkout.")
        print("  The legacy solver files named in the project journal are not present here.")
        if old_evidence["supporting_det_exists"]:
            print("  A supporting determinant comparison path exists, but it is not the same rejected reduced/full architecture.")
    print()

    novelty_ok = all(bool(v) for v in doc_checks.values()) and refined_consistency_ok
    for label, ok in doc_checks.items():
        print_check(label, ok, label.replace("_", " "))
    print_check(
        "current mixed-weak branch still shows the strongest available qualitative-novelty evidence",
        novelty_ok,
        "uses recorded old-architecture failure evidence plus current refined mixed-weak candidate neighborhoods",
    )
    print()

    print("E. Final explicit conclusion")
    working_support_ok = bool(computable_ok and refined_consistency_ok and novelty_ok)
    tighten_ok = bool(working_support_ok and sensitivity_ok)

    print(f"  Supported as current working exploratory criterion: {'YES' if working_support_ok else 'NO'}")
    print(f"  Strong enough to tighten V-N1 beyond its current partial status: {'YES' if tighten_ok else 'NO'}")
    print(
        "  Recommended V-N1 status: "
        + ("partially confirmed, tightened by pilot 05" if tighten_ok else "partially confirmed")
    )
    print()

    print("Summary of actual outcome:")
    print(
        f"  broad computability: {'PASS' if computable_ok else 'FAIL'} | "
        f"refined consistency: {'PASS' if refined_consistency_ok else 'FAIL'} | "
        f"resolution robustness: {'PASS' if sensitivity_ok else 'FAIL'} | "
        f"qualitative novelty evidence: {'PASS' if novelty_ok else 'FAIL'}"
    )
    print(
        "  WORKING-CRITERION SUPPORT: "
        + ("PASS" if working_support_ok else "FAIL")
    )
    print(
        "  TIGHTENING TEST: "
        + ("PASS" if tighten_ok else "FAIL")
    )
    print()

    if working_support_ok:
        print("OVERALL: PASS  (supports sigma_min(B_mix) as a working exploratory criterion in the current repository boundary)")
        return 0

    print("OVERALL: FAIL  (does not support sigma_min(B_mix) even as the current working exploratory criterion)")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())


