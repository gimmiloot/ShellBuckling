# Project Map

This map describes the repository after the current conservative cleanup pass.
It covers the files and directories present in the current checkout, while the
historical theory/journal documents continue to preserve older branches and
rejected directions.

## Current Main Working Direction

- The active research direction is still the mixed-weak criterion branch with
  independent circumferential channels `(v, S)` and `(psi, H, chi)`.
- For the full hinged/simple-support physical target, the preferred clean
  critical-search program is now:
  - `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`
  - `tasks/run_full_simple_support_critical_search.py`
- The older mixed-weak scan paths are preserved as hybrid testbenches and still
  matter for comparison and diagnostics:
  - `src/shell_buckling/mixed_weak/solver_simple_support_core.py`
  - `src/shell_buckling/mixed_weak/boundary_matrix_scan.py`
  - `tasks/run_mixed_weak_boundary_matrix_scan.py`
  - `src/shell_buckling/mixed_weak/solver_patched_core.py`
  - `src/shell_buckling/mixed_weak/boundary_matrix_targeted_scan.py`
  - `tasks/run_mixed_weak_targeted_scan.py`
- Current mixed-weak candidate loads remain exploratory. The operational memory
  for the separate 6-state simple-support path lives in
  `docs/theory/current_simple_support_status.md`.

## Boundary-Condition Task Separation

- Moving clamp / sliding clamp (`РїРѕРґРІРёР¶РЅР°СЏ Р·Р°РґРµР»РєР°`) appears most cleanly in the
  supporting comparison modules:
  - `src/shell_buckling/supporting/dimensionless_background_comparison.py`
  - `src/shell_buckling/supporting/determinant_criterion_comparison.py`
  - `experiments/supporting/run_supporting_dimensionless_comparison.py`
  - `experiments/supporting/run_supporting_determinant_comparison.py`
- The preserved hybrid mixed-weak scan tasks still reuse the older `F_min`
  background line. Their second right-boundary row differs:
  - broad scan: `M_s(1)`
  - targeted patched scan: `varphi(1)`
- The honest full-state axisymmetric simple-support background is kept in:
  - `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`
  - `tasks/run_axisymmetric_simple_support_background.py`
  - `tasks/run_axisymmetric_simple_support_background_report.py`
  - `tasks/run_axisymmetric_simple_support_local_branch_following.py`
- The new clean full simple-support critical-search path reconnects that honest
  background to the patched critical layer with boundary rows
  `[u_n(1), varphi(1), T_s(1), S(1), H(1)]` in:
  - `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`
  - `tasks/run_full_simple_support_critical_search.py`
- The pilot-21 fast/confirm continuation path remains the preferred high-load
  operational continuation workflow above the audited `4.3800 MPa` ceiling.

## Active Core

- `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`
  Honest 6-state axisymmetric simple-support background module with state
  `[T_s, T_sn, M_s, u_r, u_z, varphi]` and BCs
  `T_sn(x0)=0`, `u_r(x0)=0`, `varphi(x0)=0`, `T_s(1)=0`, `M_s(1)=0`, `u_z(1)=0`.

- `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`
  Reusable clean mixed-weak critical-search core for the full hinged/simple-
  support task. It uses the honest background plus the patched critical
  boundary-row set `[u_n(1), varphi(1), T_s(1), S(1), H(1)]`.

- `src/shell_buckling/mixed_weak/solver_simple_support_core.py`
  Reusable mixed-weak prototype for the preserved broad hybrid testbench. It
  still uses the older `F_min` continuation/background and the `M_s(1)` row.

- `src/shell_buckling/mixed_weak/solver_patched_core.py`
  Patched reusable operator core kept both for hybrid follow-up and for the new
  clean simple-support critical-search program.

- `src/shell_buckling/mixed_weak/boundary_matrix_scan.py`
  Preserved broad-scan hybrid boundary-matrix workflow.

- `src/shell_buckling/mixed_weak/boundary_matrix_targeted_scan.py`
  Preserved targeted hybrid boundary-matrix workflow.

## Runnable Task Scripts

### Active Tasks

- `tasks/run_full_simple_support_critical_search.py`
  Preferred clean runnable entry point for the standalone full simple-support
  critical-load search. The first-pass default mode range is `n=2..6`.

- `tasks/run_axisymmetric_simple_support_background.py`
  Active entry point for the full-state axisymmetric simple-support background.

- `tasks/run_axisymmetric_simple_support_background_report.py`
  Compact report entry point for the same full-state background path.

- `tasks/run_axisymmetric_simple_support_local_branch_following.py`
  Local branch-following entry point for the same honest background family.

- `tasks/run_mixed_weak_boundary_matrix_scan.py`
  Preserved runnable entry point for the broad hybrid mixed-weak scan.

- `tasks/run_mixed_weak_targeted_scan.py`
  Preserved runnable entry point for targeted hybrid follow-up scans.

### Proof-Pilot Operational Runners

- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_u_z_scaled_arc_like_continuation.py`
  Checkpointed fast continuation runner for the separate simple-support path.

- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/confirm_u_z_scaled_arc_like_continuation.py`
  Pointwise confirm/audit runner that reads fast-run checkpoints.

- `proof_pilots/pilot_22_exact_load_shallow_vs_current_simple_support_comparison/compare_exact_loads.py`
  Exact-load shallow-vs-current comparison pilot for selected loads.

### Supporting Tasks

- `experiments/supporting/run_supporting_determinant_comparison.py`
- `experiments/supporting/run_supporting_dimensionless_comparison.py`

## Supporting And Legacy Material

- `src/shell_buckling/supporting/determinant_criterion_comparison.py`
  Supporting shallow/non-shallow determinant comparison module.

- `src/shell_buckling/supporting/dimensionless_background_comparison.py`
  Supporting axisymmetric comparison module.

- `experiments/legacy/README.md`
  Placeholder note for archived work; older branches remain preserved mainly in
  the theory and journal documentation.

## Theory, Assumptions, And Project-State Documents

- `docs/theory/vyvod_uravneniy_updated17.md`
  Main theory-development document.

- `docs/theory/current_theory_verification_map.md`
  Verification/status map for the current mixed-weak theory.

- `docs/theory/current_mixed_weak_theory_note.tex`
  Compact supervisor-facing note for the current mixed-weak theory.

- `docs/theory/current_simple_support_status.md`
  Canonical operational status page for the separate 6-state simple-support
  path and for the preferred clean full simple-support critical-search program.

- `docs/theory/boundary_condition_task_audit.md`
  Audit note separating the moving-clamp, hybrid mixed-weak, and full
  simple-support tasks.

- `docs/theory/boundary_conditions_summary.md`
  Compact BC summary table for the moving-clamp and simple-support tasks.

- `docs/assumptions/assumptions.md`
  Register of active assumptions and their current status.

- `docs/journal/project_journal_updated14.md`
  Global project-state document with current stage, accepted/rejected paths,
  and open problems.

## Top-Level Project Files And Folders

- `README.md`
  Main human-oriented overview and manual run guide.

- `CHANGELOG.md`
  Ordinary repository change history.

- `AGENTS.md`
  Repository operating instructions for assistants.

- `src/`
  Reusable Python source code.

- `tasks/`
  Active runnable entry points.

- `experiments/`
  Supporting and archived experiment entry points.

- `docs/`
  Project documentation and literature.

- `output/`
  Reserved directory for generated artifacts.

- `.venv/`, `__pycache__/`
  Local environment and generated cache folders, not scientific source files.
