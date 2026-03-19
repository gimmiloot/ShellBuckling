# CHANGELOG

## 2026-03-19 - Make run workflow explicit

Affected files:
- `tasks/run_mixed_weak_boundary_matrix_scan.py`
- `tasks/run_mixed_weak_targeted_scan.py`
- `experiments/supporting/run_supporting_determinant_comparison.py`
- `experiments/supporting/run_supporting_dimensionless_comparison.py`
- `README.md`
- `CHANGELOG.md`

- Added explicit top-of-file run comments to every main `run_*.py` entry point.
- Added a compact command list to `README.md` so the manual launch flow is visible at a glance.

## 2026-03-19 - Restructure repository into src tasks experiments docs

Affected files:
- `src/shell_buckling/mixed_weak/solver_simple_support_core.py`
- `src/shell_buckling/mixed_weak/solver_patched_core.py`
- `src/shell_buckling/mixed_weak/boundary_matrix_scan.py`
- `src/shell_buckling/mixed_weak/boundary_matrix_targeted_scan.py`
- `src/shell_buckling/supporting/determinant_criterion_comparison.py`
- `src/shell_buckling/supporting/dimensionless_background_comparison.py`
- `tasks/run_mixed_weak_boundary_matrix_scan.py`
- `tasks/run_mixed_weak_targeted_scan.py`
- `experiments/supporting/run_supporting_determinant_comparison.py`
- `experiments/supporting/run_supporting_dimensionless_comparison.py`
- `experiments/legacy/README.md`
- `docs/project_map.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/assumptions/assumptions.md`
- `docs/journal/project_journal_updated14.md`
- `docs/literature/...`
- `README.md`
- `CHANGELOG.md`

- Moved reusable Python logic out of the repository root into `src/`.
- Replaced vague root entry scripts with explicit `run_*.py` entry points in
  `tasks/` and `experiments/supporting/`.
- Moved the project documentation and literature tree from `data/` to `docs/`.
- Updated the manual run documentation and project map to match the new layout.
- Preserved the mathematical meaning and numerical workflows while changing only
  structure, names, imports, and launch flow.

## 2026-03-19 - Add repository project map

Affected files: `data/project_map.md`, `CHANGELOG.md`

- Added `data/project_map.md` to classify the current checkout into active core, runnable tasks, supporting scripts, documentation, and non-source folders.
- Recorded the present working direction as the mixed-weak path and noted that no dedicated archived source directory exists in this checkout.
