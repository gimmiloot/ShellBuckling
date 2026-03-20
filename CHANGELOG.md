# CHANGELOG

## 2026-03-20 - Add current mixed-weak theory verification map

Affected files:
- `docs/theory/current_theory_verification_map.md`
- `docs/project_map.md`
- `CHANGELOG.md`

- Added a verification map that separates the accepted working base of the current mixed-weak branch from structural, formula-level, numerical, interpretation, and strategy items.
- Integrated the existing proof-pilot results into the verification status map without upgrading local checks into full-theory proofs.
- Added the new verification-map document to `docs/project_map.md`.

## 2026-03-20 - Add proof pilot for independent circumferential channels

Affected files:
- `proof_pilots/pilot_02_independent_channels/pilot_02_independent_channels.md`
- `proof_pilots/pilot_02_independent_channels/cas_check.py`
- `proof_pilots/pilot_02_independent_channels/lean/IndependentChannels.lean`
- `CHANGELOG.md`

- Added a second proof pilot for assumption A4 using the current mixed-weak formulas for `S`, `H`, and `chi`.
- Added a SymPy witness check showing separation of the `(v,S)` and `(psi,H,chi)` circumferential blocks.
- Added a minimal Lean file proving the abstract witness-separation logic behind channel independence.
## 2026-03-19 - Align proof pilot theorem names with verification checklist

Affected files:
- `proof_pilots/pilot_01_boundary_pairs/lean/BoundaryPairs.lean`
- `proof_pilots/pilot_01_boundary_pairs/pilot_01_boundary_pairs.md`
- `CHANGELOG.md`

- Renamed the Lean theorems to match the explicit verification checklist used for the boundary-pair pilot.
- Updated the pilot note so the theorem names and the Lean verification report use the same labels.
- Rewrote the Lean file in ASCII-safe syntax so it typechecks cleanly in the local Windows setup.

## 2026-03-19 - Add proof pilot for mixed-weak boundary pairs

Affected files:
- `proof_pilots/pilot_01_boundary_pairs/pilot_01_boundary_pairs.md`
- `proof_pilots/pilot_01_boundary_pairs/cas_check.py`
- `proof_pilots/pilot_01_boundary_pairs/lean/BoundaryPairs.lean`
- `CHANGELOG.md`

- Added a self-contained proof pilot for the right boundary-pair reduction step of the current mixed-weak formulation.
- Added a SymPy script for the admissible reduction and basis checks.
- Added a minimal Lean file for the coefficient-extraction step after admissibility is imposed.

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

