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
  the fully consistent simple-support problem, especially the axisymmetric
  simple-support background.

## Active core

- `src/shell_buckling/mixed_weak/solver_simple_support_core.py`
  Reusable mixed-weak prototype for the active simple-support line. It contains
  the axisymmetric `F_min` continuation, background interpolation, trial-space
  construction, operator assembly, boundary functionals, and scan helpers.

- `src/shell_buckling/mixed_weak/solver_patched_core.py`
  Patched working variant of the same mixed-weak prototype. It is kept as a
  separate active branch for targeted numerical follow-up rather than as an
  archived file.

- `src/shell_buckling/mixed_weak/boundary_matrix_scan.py`
  Reusable broad-scan module for the active mixed-weak boundary-matrix workflow.

- `src/shell_buckling/mixed_weak/boundary_matrix_targeted_scan.py`
  Reusable targeted-scan module for local follow-up around selected candidate
  windows.

## Runnable task scripts

### Active tasks

- `tasks/run_mixed_weak_boundary_matrix_scan.py`
  Main active entry point for the broad mixed-weak scan.

- `tasks/run_mixed_weak_targeted_scan.py`
  Active entry point for targeted follow-up scans.

### Supporting tasks

- `experiments/supporting/run_supporting_determinant_comparison.py`
  Runnable entry point for the determinant-based comparison workflow.

- `experiments/supporting/run_supporting_dimensionless_comparison.py`
  Runnable entry point for the dimensionless background-comparison workflow.

## Supporting scripts and modules

- `src/shell_buckling/supporting/determinant_criterion_comparison.py`
  Supporting comparison module for shallow vs non-shallow determinant scans.

- `src/shell_buckling/supporting/dimensionless_background_comparison.py`
  Supporting diagnostic module for dimensionless fields and branch-A checks.

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
