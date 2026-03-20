# CHANGELOG

## 2026-03-20 - Integrate pilot 03 Lean result into V-S4 status

Affected files:
- `proof_pilots/pilot_03_central_regular_family/pilot_03_central_regular_family.md`
- `docs/theory/current_theory_verification_map.md`
- `CHANGELOG.md`

- Recorded that `CentralRegularFamily.lean` now typechecks in the local Lean setup and named the abstract theorems used by pilot 03.
- Tightened the V-S4 verification-map wording to include the Lean layer together with the already completed CAS and numerical checks, without upgrading the claim beyond the current ansatz/testbench boundary.
- Marked proof pilot 03 as integrated in the verification map and removed stale pending-pilot / Lean-unavailable summary wording.

## 2026-03-20 - Repair Lean typecheck for central regular family pilot

Affected files:
- `proof_pilots/pilot_03_central_regular_family/lean/CentralRegularFamily.lean`
- `CHANGELOG.md`

- Removed the UTF-8 BOM that caused Lean 4.28.0 to fail immediately at the start of the file.
- Re-expressed the two-dimensional-family encoding using Lean core inverse notions available in the local toolchain, preserving the pilot's mathematical meaning.
- Verified that all three proof-pilot Lean files typecheck in the current local Lean installation.

## 2026-03-20 - Add proof pilot for central regular family

Affected files:
- `proof_pilots/pilot_03_central_regular_family/pilot_03_central_regular_family.md`
- `proof_pilots/pilot_03_central_regular_family/cas_check.py`
- `proof_pilots/pilot_03_central_regular_family/numerical_check.py`
- `proof_pilots/pilot_03_central_regular_family/lean/CentralRegularFamily.lean`
- `docs/theory/current_theory_verification_map.md`
- `CHANGELOG.md`

- Added a dedicated V-S4 proof pilot for the center-scaling and mode-count logic of the current mixed-weak branch.
- Added a SymPy reduction showing that the current reduced center ansatz has two free amplitudes.
- Added a numerical diagnostic showing that the current `v2` workflow constructs two center-regular directions rather than reusing raw surrogate-nullspace vectors.
- Added a minimal Lean abstraction for the two-parameter mode-count logic; local typechecking is still pending because `lean.exe` is unavailable in the current environment.
- Refined the V-S4 verification-map entry while keeping its status at partially confirmed.

## 2026-03-20 - Add current mixed-weak discussion note and refine theory guidance

Affected files:
- `AGENTS.md`
- `docs/theory/AGENTS.md`
- `docs/theory/current_mixed_weak_theory_note.tex`
- `README.md`
- `CHANGELOG.md`

- Refined the root assistant guidance with explicit policies for the current mixed-weak theory note, verification-status separation, and hypothesis categories.
- Added a theory-local `docs/theory/AGENTS.md` that distinguishes the roles of the main derivation, the verification map, and the compact theory note.
- Added a compact supervisor-facing mixed-weak theory note grounded in the current repository theory, current boundary-matrix workflow, and the present established-vs-exploratory split.
- Added the verification map and the new theory note to the `README.md` key-document list.

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
