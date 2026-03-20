# CHANGELOG

## 2026-03-20 - Add pilot 09 local branch-following helper for the 6-state simple-support background

Affected files:
- `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`
- `tasks/run_axisymmetric_simple_support_local_branch_following.py`
- `proof_pilots/pilot_09_simple_support_local_branch_following/pilot_09_simple_support_local_branch_following.md`
- `proof_pilots/pilot_09_simple_support_local_branch_following/numerical_check.py`
- `docs/theory/current_theory_verification_map.md`
- `CHANGELOG.md`

- Added a separate local branch-following helper for the 6-state axisymmetric simple-support background, built on top of the existing full-state path without changing the BC set or reconnecting the mixed-weak scans.
- Added a right-edge-focused local mesh option, secant-based seed reuse, and a strict-first / looser-on-failure local continuation workflow with larger `max_nodes`.
- Added a runnable task wrapper and a pilot 09 numerical check showing that the local ceiling moves from about `4.335 MPa` to about `4.343 MPa`, with first failure near `4.344 MPa`, while the bottleneck remains numerical.
- Refined the V-ST1 wording in the verification map without changing its status from `strategy only`.

## 2026-03-20 - Add pilot 08 for simple-support background stabilization

Affected files:
- `proof_pilots/pilot_08_simple_support_background_stabilization/pilot_08_simple_support_background_stabilization.md`
- `proof_pilots/pilot_08_simple_support_background_stabilization/problem_audit.md`
- `proof_pilots/pilot_08_simple_support_background_stabilization/bc_structure_check.py`
- `proof_pilots/pilot_08_simple_support_background_stabilization/numerical_diagnostic.py`
- `proof_pilots/pilot_08_simple_support_background_stabilization/equation_structure_note.md`
- `docs/theory/current_theory_verification_map.md`
- `CHANGELOG.md`

- Added a dedicated stabilization pilot for the active 6-state axisymmetric simple-support background in the `4.30..4.35 MPa` band.
- Added a compact problem audit and a BC structure check confirming that the live 6-state path imposes the intended simple-support BC set with a square 6-equation / 6-condition structure.
- Added a numerical diagnostic showing that the present ceiling is mainly numerical/stiffness-limited: the active equations match the supporting 6-state equations, baseline failure localizes as right-edge mesh blow-up near `4.3275 MPa`, and a relaxed local continuation profile reaches about `4.335 MPa` before failing near `4.34 MPa`.
- Refined the verification-map wording for V-ST1 without changing its status from `strategy only`.

## 2026-03-20 - Add separate full-state simple-support background path

Affected files:
- `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`
- `tasks/run_axisymmetric_simple_support_background.py`
- `tasks/run_axisymmetric_simple_support_background_report.py`
- `README.md`
- `docs/project_map.md`
- `docs/theory/boundary_condition_task_audit.md`
- `docs/theory/boundary_conditions_summary.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/theory/current_mixed_weak_theory_note.tex`
- `CHANGELOG.md`

- Added a separate active full-state axisymmetric simple-support background module with state `[T_s, T_sn, M_s, u_r, u_z, varphi]`.
- Implemented fixed-load solves first and then a continuation wrapper on top, without relabeling the older 5-state `F_min` fallback.
- Added dedicated task wrappers and a compact report path that prints the imposed BCs, the successful load range, and the current failure point near `4.33 MPa`.
- Updated the repository documentation so it now distinguishes the new full-state background path from the still-hybrid mixed-weak scan workflow.

## 2026-03-20 - Add pilot 07 for the axisymmetric simple-support background

Affected files:
- `proof_pilots/pilot_07_axisymmetric_simple_support_background/pilot_07_axisymmetric_simple_support_background.md`
- `proof_pilots/pilot_07_axisymmetric_simple_support_background/background_problem_statement.md`
- `proof_pilots/pilot_07_axisymmetric_simple_support_background/numerical_diagnostic.py`
- `proof_pilots/pilot_07_axisymmetric_simple_support_background/implementation_note.md`
- `docs/theory/current_theory_verification_map.md`
- `CHANGELOG.md`

- Added a dedicated diagnostic pilot for the current axisymmetric simple-support background bottleneck.
- Recorded the repository-level problem statement and the minimum next implementation step without changing solver mathematics.
- Added a runnable numerical diagnostic that distinguishes the active 5-state `F_min` fallback from the intended 6-state simple-support background and localizes the current continuation failure band.
- Refined the verification-map wording for the strategy-level bottleneck claim V-ST1.

## 2026-03-20 - Audit boundary-condition task separation

Affected files:
- `docs/theory/boundary_condition_task_audit.md`
- `docs/theory/boundary_conditions_summary.md`
- `README.md`
- `docs/project_map.md`
- `docs/theory/current_mixed_weak_theory_note.tex`
- `CHANGELOG.md`

- Added a compact audit note that separates the moving-clamp/sliding-clamp line, the current hybrid mixed-weak scan/testbench path, and the full simple-support background task.
- Added a boundary-condition summary table for `подвижная заделка` versus `подвижный шарнир / simple support`.
- Clarified in the README and project map that the current active mixed-weak scans still reuse the older `F_min` background and should not be read as a clean final simple-support solver path.
- Added a short boundary-condition-scope clarification to the supervisor-facing mixed-weak theory note.

## 2026-03-20 - Polish supervisor-facing wording in mixed-weak theory note

Affected files:
- `docs/theory/current_mixed_weak_theory_note.tex`
- `CHANGELOG.md`

- Tightened the wording of the supervisor-facing mixed-weak theory note without changing the mathematics, claim statuses, or verification boundary.
- Removed a few remaining repository-internal phrases so the note reads more cleanly as a standalone discussion document.
- Kept the explicit distinction between locally verified components and still-open points.

## 2026-03-20 - Refresh mixed-weak theory note after pilots 01-06b

Affected files:
- `docs/theory/current_mixed_weak_theory_note.tex`
- `AGENTS.md`
- `docs/theory/AGENTS.md`
- `CHANGELOG.md`

- Rewrote the supervisor-facing mixed-weak theory note so it reflects the current repository-level structure after pilots 01-06b, including the boundary-pair logic, channel independence, two-mode center family, `B_mix` construction rule, working `sigma_min(B_mix)` criterion, and the repository-level closed `G_ps` statement.
- Kept the note explicit about verification boundaries and remaining open points, including the still-open full shell theory, final closed mixed BVP, and final physical simple-support load.
- Refined the AGENTS maintenance policy so future theory-note updates are expected when proof pilots materially change central claim statuses or when an important open block receives a repository-level closed statement.

## 2026-03-20 - Add pilot 06b for closed G_ps statement

Affected files:
- `proof_pilots/pilot_06b_gps_closed_statement/gps_closed_statement.md`
- `proof_pilots/pilot_06b_gps_closed_statement/formula_check.py`
- `proof_pilots/pilot_06b_gps_closed_statement/note_for_theory_note.md`
- `docs/theory/current_theory_verification_map.md`
- `CHANGELOG.md`

- Added a compact repository-level closed statement of the active mixed-weak prestress/load block `G_ps`, aligned to the current code and theory documents.
- Added a formula check that verifies the consolidated statement against both active mixed-weak solver cores and confirms bilinearity in the current mixed trial/test slots.
- Refined the V-S1 wording in the verification map to record the closed repository-level `G_ps` statement more precisely, while keeping the claim at a clarified-and-still-partial status.
- Added a short optional paragraph for possible later insertion into the supervisor-facing mixed-weak theory note.

## 2026-03-20 - Add pilot 06 for G_ps as mixed-weak block

Affected files:
- `proof_pilots/pilot_06_gps_mixed_weak_block/pilot_06_gps_mixed_weak_block.md`
- `proof_pilots/pilot_06_gps_mixed_weak_block/structure_check.md`
- `proof_pilots/pilot_06_gps_mixed_weak_block/cas_check.py`
- `docs/theory/current_theory_verification_map.md`
- `CHANGELOG.md`

- Added a dedicated V-S1 proof pilot that isolates the current repository-level statement of the mixed weak prestress/load block `G_ps`.
- Added a compact structure note separating repository facts, current interpretation, and remaining ambiguity around the active `G_ps` statement.
- Added a SymPy-based structural check showing that the live solver-level forcing block is bilinear in the current mixed trial/test slots and is not naturally a scalar closure `G(U)` of the displacement/rotation slot alone.
- Refined V-S1 in the verification map to a clarified-and-still-partial status, without promoting it to a full article-level proof.

## 2026-03-20 - Add pilot 05 for sigma_min(B_mix) as working criterion

Affected files:
- `proof_pilots/pilot_05_sigma_min_working_criterion/pilot_05_sigma_min_working_criterion.md`
- `proof_pilots/pilot_05_sigma_min_working_criterion/numerical_check.py`
- `docs/theory/current_theory_verification_map.md`
- `CHANGELOG.md`

- Added a dedicated V-N1 proof pilot for the current mixed-weak working criterion `sigma_min(B_mix(q)) = 0`.
- Added a numerical check that uses the live broad/fine/adaptive/targeted mixed-weak scan workflow together with the current resolution-study path.
- Recorded that the current repository supports `sigma_min(B_mix)` as a tightened working exploratory criterion within the present testbench boundary, without promoting it to a final theorem of the physical problem.
- Kept this pilot numerical-only because an abstract Lean rank-loss lemma would not materially verify the repository-level workflow claim.

## 2026-03-20 - Add pilot 04 for B_mix from regular modes

Affected files:
- `proof_pilots/pilot_04_bmix_from_regular_modes/pilot_04_bmix_from_regular_modes.md`
- `proof_pilots/pilot_04_bmix_from_regular_modes/numerical_check.py`
- `proof_pilots/pilot_04_bmix_from_regular_modes/lean/BmixFromRegularModes.lean`
- `docs/theory/current_theory_verification_map.md`
- `CHANGELOG.md`

- Added a dedicated V-S5 proof pilot for the current repository rule that `B_mix` is built from the center-regular mode pair.
- Added a numerical comparison between the live `V_reg`-based `B_mix` construction and a raw smallest-singular-vector surrogate pair, showing that the raw pair violates the active center constraints and changes the construction in the current repository sense.
- Added a minimal Lean file for the abstract admissibility logic behind using the regular pair rather than a non-admissible surrogate pair.
- Tightened the V-S5 verification-map wording without upgrading the claim beyond the current surrogate/testbench boundary.

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
