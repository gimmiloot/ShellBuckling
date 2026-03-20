# Project Map

This map describes the repository after the structural refactor.
It covers the files and directories that exist in the current checkout.
Historical branches discussed in the theory and journal documents remain part of
project memory even when they are not present here as separate source files.

## Current main working direction

- The active research path is the mixed-weak criterion branch with independent
  circumferential channels `(v, S)` and `(psi, H, chi)`.
- The main active code path is:
  - `src/shell_buckling/mixed_weak/solver_simple_support_core.py`
  - `src/shell_buckling/mixed_weak/boundary_matrix_scan.py`
  - `tasks/run_mixed_weak_boundary_matrix_scan.py`
- A nearby working variant is kept for targeted follow-up scans:
  - `src/shell_buckling/mixed_weak/solver_patched_core.py`
  - `src/shell_buckling/mixed_weak/boundary_matrix_targeted_scan.py`
  - `tasks/run_mixed_weak_targeted_scan.py`
- Current mixed-weak candidate loads remain exploratory. The main open issue is
  no longer the absence of a separate full-state simple-support background path,
  but stabilizing and reconnecting that path to the active mixed-weak scans.

## Boundary-condition task separation

- Moving clamp / sliding clamp (`подвижная заделка`) currently appears most
  cleanly in the supporting axisymmetric comparison modules
  `src/shell_buckling/supporting/dimensionless_background_comparison.py` and
  `src/shell_buckling/supporting/determinant_criterion_comparison.py`, together
  with their runnable wrappers in `experiments/supporting/`.
- The active mixed-weak scan tasks are not yet a separate full simple-support
  program. They reuse the older `F_min` background line, and the two active
  scan variants currently differ on the second right-boundary row:
  `M_s(1)` in the broad scan and `varphi(1)` in the targeted patched scan.
- The full hinged/simple-support axisymmetric task
  (`подвижный шарнир / simple support`) is now available as a separate active
  full-state background path in
  `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`,
  with task wrappers in `tasks/`.
  In the current implementation that path reaches `4.30 MPa` and fails near
  `4.33 MPa`, so it is runnable but not yet fully stabilized or connected to
  the active mixed-weak scans.

## Active core

- `src/shell_buckling/mixed_weak/solver_simple_support_core.py`
  Reusable mixed-weak prototype for the broad hybrid simple-support-oriented
  testbench. It still uses the older `F_min` continuation/background and its
  boundary matrix currently uses the `M_s(1)` broad-scan row variant.

- `src/shell_buckling/mixed_weak/solver_patched_core.py`
  Patched working variant of the same mixed-weak prototype. It is kept as a
  separate active branch for targeted numerical follow-up and currently uses the
  `varphi(1)` right-boundary testbench row in the patched scan path.

- `src/shell_buckling/mixed_weak/boundary_matrix_scan.py`
  Reusable broad-scan module for the active mixed-weak boundary-matrix workflow.

- `src/shell_buckling/mixed_weak/boundary_matrix_targeted_scan.py`
  Reusable targeted-scan module for local follow-up around selected candidate
  windows.

- `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`
  Separate active full-state axisymmetric simple-support background module with
  state `[T_s, T_sn, M_s, u_r, u_z, varphi]`, fixed-load solves first, and a
  continuation wrapper added on top. In the current implementation it reaches
  `4.30 MPa` and fails near `4.33 MPa`.

## Runnable task scripts

### Active tasks

- `tasks/run_mixed_weak_boundary_matrix_scan.py`
  Main active entry point for the broad mixed-weak scan.

- `tasks/run_mixed_weak_targeted_scan.py`
  Active entry point for targeted follow-up scans.

- `tasks/run_axisymmetric_simple_support_background.py`
  Active entry point for the separate full-state simple-support background path.

- `tasks/run_axisymmetric_simple_support_background_report.py`
  Compact diagnostic/report entry point for the same full-state background path.

### Supporting tasks

- `experiments/supporting/run_supporting_determinant_comparison.py`
  Runnable entry point for the determinant-based comparison workflow.

- `experiments/supporting/run_supporting_dimensionless_comparison.py`
  Runnable entry point for the dimensionless background-comparison workflow.

## Supporting scripts and modules

- `src/shell_buckling/supporting/determinant_criterion_comparison.py`
  Supporting comparison module for shallow vs non-shallow determinant scans.

- `src/shell_buckling/supporting/dimensionless_background_comparison.py`
  Supporting diagnostic module for dimensionless fields and branch-A checks on
  the axisymmetric comparison line that currently plays the moving-clamp /
  sliding-clamp role in the repository discussion.

## Archived / legacy path

- `experiments/legacy/README.md`
  Placeholder note for archived work. The current checkout does not contain
  separate legacy source files from the older reduced/full branches.

- Historical legacy branches are still documented in:
  - `docs/theory/vyvod_uravneniy_updated17.md`
  - `docs/assumptions/assumptions.md`
  - `docs/journal/project_journal_updated14.md`

## Theory, assumptions, and project-state documents

- `docs/theory/vyvod_uravneniy_updated17.md`
  Main theory-development document.

- `docs/theory/current_theory_verification_map.md`
  Verification boundary and status map for the current mixed-weak theory.

- `docs/theory/current_mixed_weak_theory_note.tex`
  Compact supervisor-facing note for the current mixed-weak theory.

- `docs/theory/boundary_condition_task_audit.md`
  Audit note separating the moving-clamp, hybrid mixed-weak testbench, and full
  simple-support tasks.

- `docs/theory/boundary_conditions_summary.md`
  Compact BC summary table for the moving-clamp and simple-support tasks.

- `docs/assumptions/assumptions.md`
  Register of active assumptions and their current status.

- `docs/journal/project_journal_updated14.md`
  Global project-state document with current stage, accepted/rejected paths, and
  open problems.

## Literature and reference material

- `docs/literature/SOURCE_INDEX.md`
  Literature map for the current project configuration.

- `docs/literature/notes/*.md`
  Repository-specific notes for the source literature.

- `docs/literature/pdf/*.pdf`
  Source PDFs and scans used for theory checks and comparison.

## Top-level project files and folders

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

- `notes/`
  Present but empty in the current checkout.

- `.venv/`, `__pycache__/`
  Local environment and generated cache folders, not scientific source files.