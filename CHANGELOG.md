# CHANGELOG

## 2026-04-01 - Phase 3 workflow/output layering cleanup

Affected files:
- .gitignore
- proof_pilots/README.md
- proof_pilots/pilot_18_revised_analytic_barrier_diagnosis/artifacts/README.md
- proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/artifacts/README.md
- tasks/README.md
- output/README.md
- CHANGELOG.md

- Added lightweight role/index files for `proof_pilots/`, `tasks/`, and `output/` to separate source material from generated artifacts without moving path-coupled historical files.
- Added forward-looking `artifacts/` boundaries for the artifact-heavy pilot 18 and pilot 21 directories while keeping the existing root artifact paths intact for compatibility.
- Unignored and tracked `output/README.md` so the output tree now has a repository-visible classification of curated exports versus runtime validation trees.
- Cleaned generated `__pycache__` directories only in repository-controlled source/task/pilot locations; solver logic, equations, and boundary-condition meaning were unchanged.

## 2026-04-01 - Phase 2 mixed-weak internal code extraction layer

Affected files:
- src/shell_buckling/mixed_weak/_core_reduction.py
- src/shell_buckling/mixed_weak/_core_solver_common.py
- src/shell_buckling/mixed_weak/solver_patched_core.py
- src/shell_buckling/mixed_weak/solver_simple_support_core.py
- src/shell_buckling/mixed_weak/boundary_matrix_scan.py
- src/shell_buckling/mixed_weak/boundary_matrix_targeted_scan.py
- src/shell_buckling/mixed_weak/full_simple_support_critical_search.py
- CHANGELOG.md

- Extracted shared boundary/reduction helpers into `_core_reduction.py` and rewired the boundary-matrix scan/search modules through thin local wrappers.
- Moved the common mixed-weak solver implementation into `_core_solver_common.py` and converted `solver_patched_core.py` / `solver_simple_support_core.py` into wrapper-preserving public modules.
- Preserved public entry-point paths and wrapper behavior while keeping the existing variant split in the second boundary row (`varphi(1)` vs `M_s(1)`).
- Kept scientific meaning unchanged: no equations, boundary-condition meaning, numerical retuning, or intended solver behavior were changed.

## 2026-04-01 - Docs-only Phase 1 role split for clean full simple support

Affected files:
- docs/theory/current_simple_support_object_glossary.md
- docs/theory/current_simple_support_status.md
- docs/theory/current_simple_support_final_audit_note.md
- docs/theory/current_simple_support_closed_line_index.md
- docs/theory/current_simple_support_theorem_roadmap.md
- docs/theory/current_theory_verification_map.md
- docs/project_map.md
- CHANGELOG.md

- Added a canonical glossary for stable clean full simple-support object names and source-of-truth references.
- Trimmed the operational status page back to active-path reading plus a frozen-line pointer, instead of replaying the frozen theorem history there.
- Trimmed the theorem roadmap to active forward-looking use, with the frozen-line replay now pointed to the final audit note and closed-line index.
- Kept the verification map as the authoritative claim registry while replacing part of the repeated frozen-line narrative with references to the glossary and archive docs.
- Trimmed the project map back toward a repository-role map instead of a second theorem-history/status memo.
- Kept scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, or theorem status were upgraded.

## 2026-04-01 - Freeze and index the closed clean full simple support theorem line

Affected files:
- docs/theory/current_simple_support_final_audit_note.md
- docs/theory/current_simple_support_closed_line_index.md
- docs/theory/current_simple_support_status.md
- docs/journal/project_journal_updated14.md
- CHANGELOG.md

- Synced the final freeze of the old clean full simple support / Р С—Р С•Р Т‘Р Р†Р С‘Р В¶Р Р…РЎвЂ№Р в„– РЎв‚¬Р В°РЎР‚Р Р…Р С‘РЎР‚ theorem-facing line.
- Recorded that the old line is frozen, did not validate the current criterion, and did not refute it either.
- Recorded the exact final sharpened admissibility-side boundary as the residual-direction question z_temp in A_adm^th,n(q) intersect ker(C_center,n(q)) ?.
- Added a short closed-line archive/index note with reusable results and an ordered source-of-truth reading list for future criterion reformulation work.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, clean standalone full simple support / Р С—Р С•Р Т‘Р Р†Р С‘Р В¶Р Р…РЎвЂ№Р в„– РЎв‚¬Р В°РЎР‚Р Р…Р С‘РЎР‚ path, or hybrid F_min reuse policy were changed.

## 2026-04-01 - Reduce the explicit affine-line admissibility fork to the single residual direction z_temp

Affected files:
- docs/theory/current_simple_support_theorem_roadmap.md
- docs/theory/current_theory_verification_map.md
- CHANGELOG.md

- Recorded the final line-level sharpening for the explicit affine line c_sel + span(z_temp,n(q;s_mem)).
- Used the already closed inclusion A_sel^repo subseteq A_sel^{th,cand} subseteq A_adm^th together with the tangent-space meaning of A_adm^th to reduce the line fork to one residual-direction question: whether z_temp itself belongs to A_adm^th,n(q) intersect ker(C_center,n(q)).
- Recorded the exact equivalence: line-level collapse to c_sel is equivalent to span(z_temp) intersect A_adm^th = {0}, while any nonzero theorem-facing admissible point on that line is equivalent to admissibility of z_temp itself.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, clean standalone full simple support / Р С—Р С•Р Т‘Р Р†Р С‘Р В¶Р Р…РЎвЂ№Р в„– РЎв‚¬Р В°РЎР‚Р Р…Р С‘РЎР‚ path, or hybrid F_min reuse policy were changed.
## 2026-04-01 - Sharpen the c_temp admissibility fork to an explicit positive-fiber-excess point on the fixed fiber

Affected files:
- docs/theory/current_simple_support_theorem_roadmap.md
- docs/theory/current_theory_verification_map.md
- CHANGELOG.md

- Recorded that the explicit candidate c_temp = c_sel + z_temp,n(q;s_mem) is not only an off-selected point of the fixed same-trace center-regular fiber, but an explicit positive-fiber-excess point there.
- Used the already closed weighted-ansatz fiber-excess identity to state Delta_H,n,q(c_temp) = z_temp^T H_n,q z_temp > 0 on the current repository boundary.
- Sharpened the admissibility-side question accordingly: decide whether theorem-facing admissibility contains that explicit positive-fiber-excess point on the affine line c_sel + span(z_temp), or collapses on that line to the unique selected H_n,q-minimal representative.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, clean standalone full simple support / Р С—Р С•Р Т‘Р Р†Р С‘Р В¶Р Р…РЎвЂ№Р в„– РЎв‚¬Р В°РЎР‚Р Р…Р С‘РЎР‚ path, or hybrid F_min reuse policy were changed.
## 2026-04-01 - Sharpen the admissibility-side one-point gap to the fixed same-trace center-regular fiber

Affected files:
- docs/theory/current_simple_support_theorem_roadmap.md
- docs/theory/current_theory_verification_map.md
- CHANGELOG.md

- Recorded a sharper admissibility-side reading for the explicit point c_temp := c_sel + z_temp,n(q;s_mem).
- Fixed that the remaining Z_adm(c_temp) gap is not extension across a generic off-selected weighted-trial point: c_temp already lies in the same fixed ansatz-level center-regular fiber as c_sel, so the unresolved step is continuum realization of one explicit off-selected point of that fiber.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, clean standalone full simple support / Р С—Р С•Р Т‘Р Р†Р С‘Р В¶Р Р…РЎвЂ№Р в„– РЎв‚¬Р В°РЎР‚Р Р…Р С‘РЎР‚ path, or hybrid F_min reuse policy were changed.
## 2026-04-01 - Add the final audit note for the current clean full simple support / Р С—Р С•Р Т‘Р Р†Р С‘Р В¶Р Р…РЎвЂ№Р в„– РЎв‚¬Р В°РЎР‚Р Р…Р С‘РЎР‚ theorem path

Affected files:
- docs/theory/current_simple_support_final_audit_note.md
- docs/theory/current_simple_support_status.md
- docs/theory/current_simple_support_theorem_roadmap.md
- docs/theory/current_theory_verification_map.md
- docs/project_map.md
- CHANGELOG.md

- Added a short final audit-style note freezing the old clean theorem-step line as saturated on the present repository boundary.
- Recorded that the current criterion is still not theorem-secured enough to exclude the explicit membrane candidate.
- Recorded the exact remaining admissibility-side target as the one-point extension theorem for c_temp := c_sel + z_temp,n(q;s_mem), extending the closed selected-family coefficient identification beyond A_repo = A_ls to this explicit off-selected weighted-trial point.
- Synced cross-references from the current status, theorem roadmap, verification map, and project map to the final audit note.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, clean standalone full simple support / Р С—Р С•Р Т‘Р Р†Р С‘Р В¶Р Р…РЎвЂ№Р в„– РЎв‚¬Р В°РЎР‚Р Р…Р С‘РЎР‚ path, or hybrid F_min reuse policy were changed.

## 2026-04-01 - Sharpen the one-point closure branch for the explicit membrane candidate on the clean full `simple support / Р С—Р С•Р Т‘Р Р†Р С‘Р В¶Р Р…РЎвЂ№Р в„– РЎв‚¬Р В°РЎР‚Р Р…Р С‘РЎР‚` path

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Split the earlier generic one-point upgrade language into two sharper closure theorems for the explicit point `c_temp := c_sel + z_temp,n(q;s_mem)`.
- Recorded that `Z_adm(c_temp)` is the one-point continuum-realization theorem for the explicit weighted-trial point.
- Recorded that `Z_chk(c_temp,c_sel)` is the one-point checked-local shadow existence theorem for `c_temp` on the fixed equal-trace selected class of `c_sel`, with overlap/common-chart compatibility no longer treated as an independent bottleneck after such a shadow exists.
- Sharpened the admissibility side further: the exact missing theorem for `Z_adm(c_temp)` is not the whole global losslessness statement `A_repo = A_full^th`, but a one-point extension of the already closed selected-family coefficient map `a -> V_adm,n(q) a` from `A_repo = A_ls` to the explicit off-selected weighted-trial point `c_temp`.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, clean standalone full `simple support / Р С—Р С•Р Т‘Р Р†Р С‘Р В¶Р Р…РЎвЂ№Р в„– РЎв‚¬Р В°РЎР‚Р Р…Р С‘РЎР‚` path, or hybrid `F_min` reuse policy were changed.
## 2026-04-01 - Freeze the old theorem-step line at the one-point object-closure boundary on the clean full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path

Affected files:
- `docs/theory/current_simple_support_status.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Synced the clean `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` status after the one-point audit: the older `T3...` style line is now recorded as saturated as far as the current clean repository boundary allows.
- Recorded explicitly that the current theorem-facing objects are still not closed enough to decide the one-point question for `c_temp := c_sel + z_temp,n(q;s_mem)`.
- Opened the new active one-point closure branch `Z_adm(c_temp)` / `Z_chk(c_temp,c_sel)` without introducing another theorem-step sub-chain.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, clean standalone full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path, or hybrid `F_min` reuse policy were changed.

## 2026-04-01 - Isolate the exact promotion failure for the explicit weighted-ansatz membrane template on the clean full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Recorded the exact next obstruction after the explicit weighted-ansatz membrane template is built: the extension fails at the theorem-facing admissibility / `Pair_chk` upgrade, not at low-order jet realizability.
- Recorded the conditional sharpening that if the explicit template did admit a checked-local shadow in a common corrected chart, then the membrane deviation would already be nonzero on the current physical clean regime because the visible membrane direction is the `U1` direction and `U1 = alpha s_mem` with `alpha != 0`.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, clean standalone full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path, or hybrid `F_min` reuse policy were changed.
## 2026-04-01 - Add an explicit weighted-ansatz residual template realizing the membrane-nullmode jet on the clean full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` residual fiber

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Recorded an explicit current weighted-ansatz same-trace residual coefficient template with only `u_s,k=1,2`, `v,k=1,2`, and `T_s,k=1,2` nonzero.
- Showed exactly that this template lies in `ker(C_center)` and has extracted low-order jet equal to `s_mem g_mem^aug,n(q)`.
- Therefore the current clean weighted-ansatz / coefficient architecture does not itself obstruct global realization of the membrane-nullmode jet on the residual fiber.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, clean standalone full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` search path, or hybrid `F_min` reuse policy were changed.

## 2026-04-01 - Add the low-order membrane-nullmode obstruction on the residual fiber for the clean full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Added a genuinely new residual-fiber restriction: any nonzero checked-local pair-definable membrane-visible residual must have augmented local jet in the one-dimensional membrane-nullmode line `span(g_mem^aug,n(q))`.
- Recorded the explicit low-order coefficient equations `U1 = alpha T1`, `V1 = beta T1`, `N1 = P1 = Y1 = 0`, with `T1 != 0`, together with checked next-layer closure to zero.
- Sharpened the remaining bottleneck accordingly: the true missing input is now a global checked-local coefficient-extraction theorem on `R_res,n(q) = A_adm^th,n(q) intersect ker(C_center,n(q))` deciding whether a given residual realizes that exact augmented membrane-nullmode jet.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, clean standalone full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` search path, or hybrid `F_min` reuse policy were changed.

## 2026-04-01 - Reduce the extrinsic admissible-lift branch to the residual-fiber pair-definability / membrane-visibility question on the clean full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Recorded the exact intersection law `X_sel,n(q) intersect ker(C_center,n(q)) = {0}` following from `C_center,n(q) P_sel,n(q) = I_4`.
- Used that law to show that for every repo-selected basepoint `c_sel in A_ls,n(q)` and every nonzero same-trace residual direction `z in A_adm^th,n(q) intersect ker(C_center,n(q))`, the point `c_sel + z` is automatically outside `X_sel,n(q)`.
- Sharpened the extrinsic admissible-lift branch accordingly: outside-`X_sel` is no longer an independent condition, so the true remaining bottleneck is now a global-to-local theorem on the residual fiber deciding checked-local pair-definability and membrane visibility.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, clean standalone full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` search path, or hybrid `F_min` reuse policy were changed.
## 2026-04-01 - Add the first admissible-lift obstruction inside the global selected full-center lift on the clean full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended the post-`T3v` branch into the admissible-lift question without introducing another reformulation-only theorem step.
- Recorded the first exact obstruction on that branch: no nonzero same-trace admissible global lift can occur inside the current global selected full-center lift `X_sel = im(P_sel)`, because `C_center|_(X_sel)` is bijective with inverse `P_sel`.
- Added the equivalent candidate-class consequence `A_sel^{th,cand} intersect X_sel = A_ls`, so any future admissible-lift construction must lie outside the current KKT-selected architecture.
- Synced the theorem roadmap, verification map, and project journal so the next bottleneck is now the existence or impossibility of admissible candidate-class points outside `X_sel` that still realize the membrane direction.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, clean standalone full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` search path, or hybrid `F_min` reuse policy were changed.


## 2026-04-01 - Sharpen the T3u pairwise scalar-difference question into the T3v representative-sensitive rigidity obstruction on the clean full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 25 from the `T3u` pairwise scalar-difference-image stage into the `T3v` representative-sensitive rigidity stage.
- Recorded the conservative `Outcome B` result: pairwise scalar-difference collapse `Omega_sigma,n(q; c_sel) = {0}` is not yet proved, but the exact missing ingredient is now isolated more sharply as one representative-sensitive rigidity law on the exact admissible pair domain `Pair_sigma,n(q; c_sel)`.
- Recorded the sharper structural relation `Sigma_sigma,n(q; c_sel) subseteq Omega_sigma,n(q; c_sel) subseteq Sigma_sigma,n(q; c_sel) - Sigma_sigma,n(q; c_sel)` and the exact nonzero-pairwise template in one fixed quotient fiber.
- Synced the theorem roadmap, verification map, and project journal so the next bottleneck is now the `T3v` representative-sensitive rigidity / pairwise scalar-difference-collapse theorem rather than only the `T3u` pairwise-image wording.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, clean standalone full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` search path, or hybrid `F_min` reuse policy were changed.

## 2026-03-30 - Reduce the T3t scalar-image question to a T3u exact pairwise scalar-difference obstruction on the clean full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 25 from the `T3t` scalar defect-image stage into the `T3u` scalar-image-collapse stage.
- Recorded the conservative `Outcome B` result: scalar-image collapse `Sigma_sigma,n(q; c_sel) = {0}` is not yet proved, but it is now reduced further to vanishing of the exact pairwise scalar-difference image `Omega_sigma,n(q; c_sel)` on the same exact admissible pair domain.
- Synced the theorem roadmap, verification map, and project journal so the next bottleneck is now the `T3u` pairwise scalar-difference vanishing theorem rather than only the scalar-image-collapse wording.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, broad scans, or hybrid `F_min` reuse policy were changed.

## 2026-03-30 - Reduce the T3s global pointwise-defect question to a T3t exact defect-set / scalar-image obstruction on the clean full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 25 from the `T3s` chart-invariant global pointwise-defect stage into the `T3t` exact global defect-set emptiness stage.
- Recorded the conservative `Outcome B` result: emptiness of `N_sigma,n(q; c_sel)` is not yet proved, but it is now reduced further to the exact scalar defect-image collapse condition `Sigma_sigma,n(q; c_sel) = {0}` on the same full exact domain.
- Synced the theorem roadmap, verification map, and project journal so the next bottleneck is now the `T3t` defect-set emptiness / scalar-image-collapse theorem rather than only the global pointwise-vanishing wording.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, broad scans, or hybrid `F_min` reuse policy were changed.

## 2026-03-30 - Reduce the T3r pointwise-law question to a T3s chart-invariant global defect-map obstruction on the exact checked-local domain for clean simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 25 from the `T3r` patchwise pointwise-law stage into the `T3s` chart-invariant global pointwise-defect stage.
- Recorded the exact descent of the patchwise basepoint-relative membrane difference `Delta_rep,U^pt` to the chart-invariant global map `Delta_rep^pt : D_sigma -> span(e_mem)` with `Delta_rep^pt = sigma_chk e_mem`.
- Recorded the sharpest current obstruction theorem: current theorem-facing invariants still force only codomain containment in `span(e_mem)` plus basepoint normalization at `z = 0`, not vanishing on the full exact domain.
- Recorded the exact remaining bottleneck as emptiness of the pointwise nonzero set `N_sigma,n(q; c_sel)` on `D_sigma,n(q; c_sel)`.
- Synced the theorem roadmap, verification map, and project journal so the next bottleneck is now the `T3s` global pointwise-vanishing theorem rather than a patch-indexed pointwise law.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, or theorem-level status of `B_red` / `B_mix` were changed.


## 2026-03-30 - Reduce the T3q representative-law question to a T3r pointwise basepoint-relative obstruction on exact checked-local patches for clean simple support

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 25 from the `T3q` patchwise representative-law obstruction stage into the `T3r` pointwise basepoint-relative representative-law stage.
- Recorded the exact pointwise basepoint-relative checked-local representative difference `Delta_rep,U^pt,n(q; c_sel)(z) = chi_chk,U(c_sel + z) - chi_chk,U(c_sel) = sigma_chk(z) e_mem` on every exact admissible residual-generated checked-local patch.
- Recorded the strongest current sharpening: the pairwise patchwise representative law `Rep_U` is exactly equivalent to pointwise vanishing of that basepoint-relative membrane deviation, so failure of `Rep_U` is already equivalent to one exact nonzero patch point.
- Recorded the sharpest current obstruction theorem: on the checked local boundary all currently justified theorem-facing invariants still force only membrane-line containment of that pointwise difference and do not by themselves force its vanishing.
- Synced the theorem roadmap, verification map, and project journal so the next bottleneck is now the `T3r` pointwise basepoint-relative vanishing theorem on the full exact admissible patch cover.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, active standalone clean `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path, or theorem-level status of `B_red` / `B_mix` were changed.

## 2026-03-30 - Reduce the T3p singletonity question to a T3q representative-law obstruction on exact membrane-fiber patches for clean simple support

Affected files:
- proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md
- docs/theory/current_simple_support_theorem_roadmap.md
- docs/theory/current_theory_verification_map.md
- docs/journal/project_journal_updated14.md
- CHANGELOG.md

- Extended pilot 25 from the T3p membrane-fiber singleton stage into the T3q representative-law obstruction stage.
- Recorded the exact patchwise representative law Rep_U,n(q; c_sel) and the exact equivalence between Rep_U, vanishing of sigma_chk, constancy of s_U, and singletonity of the checked-local patch image in the fixed membrane fiber.
- Recorded the sharpest current obstruction theorem: on the checked local boundary all currently justified theorem-facing invariants remain quotient-final, so they still force only fiber containment and do not by themselves force singletonity.
- Recorded the exact next bottleneck: derive one representative-sensitive law on the exact admissible residual-generated patch cover, or explicitly realize an admissible non-singleton patch.
- Synced the theorem roadmap, verification map, and project journal so the next bottleneck is now the T3q patchwise representative-law theorem rather than a generic singletonity question.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, active standalone clean simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ path, or theorem-level status of B_red / B_mix were changed.
## 2026-03-29 - Reduce the T3p membrane-selector question to a membrane-fiber singleton obstruction on exact checked-local patches for clean simple support

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 25 from the `T3o` patchwise-constancy stage into the `T3p` membrane-fiber singleton stage.
- Recorded the exact checked-local patch image `Im_chk,U,n(q; c_sel)` and the equivalent membrane-fiber image `S_U,n(q; c_sel)` on every exact admissible residual-generated checked-local patch.
- Recorded the sharpest current reduction: after `T3o`, vanishing of `sigma_chk`, constancy of `s_U`, singletonity of `S_U`, and singletonity of `Im_chk,U` in the fixed membrane fiber are all equivalent.
- Recorded the exact remaining bottleneck: current theorem-facing constraints force only containment in the fixed membrane fiber above `(a_sel, b_sel)`, not singletonity of that image, so the remaining open question is now a precise membrane-fiber singleton theorem on the exact patches.
- Synced the theorem roadmap, verification map, and project journal so the next bottleneck is now to prove or refute singletonity of the exact checked-local patch image on every exact admissible residual-generated patch.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, active standalone clean `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path, or theorem-level status of `B_red` / `B_mix` were changed.

## 2026-03-29 - Reduce the T3o membrane-selector question to an exact patchwise constancy obstruction after automatic overlap compatibility for clean simple support

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 25 from the T3n local-coboundary stage into the T3o patchwise-constancy stage and recorded the exact admissible residual-generated checked-local patch family `D_sigma^U,n(q; c_sel)`.
- Recorded the strongest current sharpening: under quotient-preserving chart changes the local membrane coordinates on one fixed equal-trace class differ only by a z-independent constant, so overlap compatibility is automatic.
- Recorded the exact remaining bottleneck: global vanishing of `sigma_chk,n(q; c_sel)(z)` is now equivalent to constancy of the local membrane coordinate on any exact admissible residual-generated checked-local patch cover, and the only unresolved issue is patchwise constancy itself.
- Synced the theorem roadmap, verification map, and project journal so the next bottleneck is now to prove or refute patchwise constancy of `s_U` on the full exact admissible residual-generated checked-local patch cover.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, active standalone clean `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path, or theorem-level status of `B_red` / `B_mix` were changed.

## 2026-03-29 - Reduce the T3n membrane-selector question to an exact patchwise membrane-constancy / uniqueness-in-class obstruction theorem for clean simple support

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 25 from the T3m selector-cocycle stage into the T3n uniqueness stage and recorded the exact checked-local definability subdomain `D_sigma,n(q; c_sel)` as the domain on which uniqueness is actually tested.
- Recorded the strongest current selector-level reduction: on every common corrected-chart patch the membrane selector is locally a coboundary `sigma_chk = s_U - s_U(0)`, so vanishing is exactly equivalent to patchwise constancy of the local membrane coordinate.
- Recorded the sharpest honest obstruction now available: current theorem-facing constraints still determine only the quotient coordinates `(a, b)` and do not yet force constancy of `s_U`; an explicit admissible nonzero example is still not constructed, but any patch point with `s_U(z) != s_U(0)` is now the exact nonvanishing template.
- Synced the theorem roadmap, verification map, and project journal so the next bottleneck is now to prove or refute patchwise membrane constancy on the exact admissible residual-generated checked-local pair patches, equivalently prove or refute `sigma_chk,n(q; c_sel)(z) = 0` on all of `D_sigma,n(q; c_sel)`.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, active standalone clean `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path, or theorem-level status of `B_red` / `B_mix` were changed.

## 2026-03-29 - Reduce the T3m membrane-selector question to an exact cocycle / obstruction theorem for clean simple support

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 25 from the T3l pairwise membrane-difference stage into the T3m membrane-selector stage and recorded the exact residual-generated selector domain `D_sigma,n(q; c_sel)`.
- Recorded the strongest current selector-level theorem: the basepoint-relative membrane selector `sigma_chk` is now packaged as the exact chart-invariant membrane cocycle on equal-trace checked-local pairs, with normalization, antisymmetry, and cocycle laws.
- Recorded the sharpest honest obstruction now available: current checked-local selected invariants still factor only through the membrane quotient, so they do not yet force `sigma_chk,n(q; c_sel)(z) = 0`; an admissible nonvanishing pair is not yet constructed, but the exact nonvanishing template is now isolated.
- Synced the theorem roadmap, verification map, and project journal so the next bottleneck is now to prove or refute that the exact admissible residual-generated checked-local pair domain meets each equal-trace membrane quotient class only in the repo-selected representative.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, active standalone clean `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path, or theorem-level status of `B_red` / `B_mix` were changed.

## 2026-03-29 - Reduce the T3l checked-local bridge question to a chart-invariant pairwise membrane-difference object for clean simple support

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 25 from the T3k raw-shadow obstruction stage into the T3l pairwise bridge stage and recorded the theorem-facing equal-trace checked-local representative-difference object `Delta_rep,chk,n(q; c, c_ref) in span(e_mem)`.
- Recorded the sharpest current theorem-facing reduction: raw same-trace shadows still collapse, but the pairwise membrane difference between equal-trace checked-local representatives is chart-invariant under quotient-preserving chart changes and is equivalently encoded by the scalar selector `sigma_chk,n(q; c, c_ref)`.
- Synced the theorem roadmap, verification map, and project journal so the next bottleneck is now to prove or refute vanishing of `sigma_chk,n(q; c_sel)(z)` on the exact admissible residual-generated checked-local pair domain.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, active standalone clean `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path, or theorem-level status of `B_red` / `B_mix` were changed.

## 2026-03-29 - Reduce the T3k global-shadow question to an exact zero-quotient obstruction for raw same-trace shadows in clean simple support

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 25 from the T3j local-extractor stage into the T3k global-shadow stage and recorded the exact obstruction theorem: on `D_res,n(q) subset ker(J_0,n(q))`, any compatible raw shadow map `Sh_chk,n(q)` into `Xi_sel,corr^(1,eta),n(q)` already collapses to the zero quotient class.
- Recorded the sharpest current theorem-facing reduction: any such raw shadow map must factor through the membrane line `span(g_mem,n(q))`, equivalently through a scalar membrane-selector candidate `sigma_chk,n(q)`, so a raw factorization `Phi_chk = q_coeff o chi_chk,vis o Sh_chk` would be identically zero.
- Synced the theorem roadmap, verification map, and project journal so the next bottleneck is now a theorem-facing basepoint-relative checked-local representative-difference object on ambient candidate-class pairs before quotient collapse, or a direct vanishing theorem for the same-trace membrane selector.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, active standalone clean `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path, or theorem-level status of `B_red` / `B_mix` were changed.

## 2026-03-29 - Reduce the T3j checked-local coefficient-extraction question to an explicit local extractor plus one missing global shadow bridge for clean simple support

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 25 from the T3i projected-map injectivity stage into the T3j checked-local coefficient-extraction stage and recorded the explicit visible-chart local extractor `chi_chk,vis,n(q)` on `Xi_sel,corr^(1,eta),n(q) = im(D_rich,eta^corr,n(q))`.
- Recorded the sharpest current theorem-facing reduction: the full 3-coordinate local extractor is chart-dependent, but its projection `q_coeff o chi_chk,vis,n(q)` is chart-invariant and factors exactly through `Pi_eta_to_J0` on the checked local corrected family.
- Synced the theorem roadmap, verification map, and project journal so the next bottleneck is now the global checked-local shadow bridge `Sh_chk,n(q) : D_res,n(q) -> Xi_sel,corr^(1,eta),n(q)`, not the absence of a local checked extractor itself.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, active standalone clean `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path, or theorem-level status of `B_red` / `B_mix` were changed.

## 2026-03-29 - Reduce the T3i injectivity question to one exact missing global checked-local extraction operator for clean simple support

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 25 from the T3h membrane-lift kernel/preimage package into the T3i projected-map injectivity stage and isolated the exact projected lift map `Phi_chk,n(q; c_sel) = q_coeff o delta_chk,n(q; c_sel)` on the admissible same-trace residual domain.
- Recorded the sharpest current theorem-facing reduction: `ker(Phi_chk) = Lift_mem = R_inv`, so injectivity would close the zero-excess gap, but the repo still does not package the explicit global checked local coefficient-extraction operator `chi_chk,n(q)` that would turn this into a closed linear rank/nullity theorem.
- Synced the theorem roadmap, verification map, and project journal so the next bottleneck is now operator-level control/construction of `chi_chk,n(q)` on `A_adm^th,n(q) intersect ker(C_center,n(q))`.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, active standalone clean `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path, or theorem-level status of `B_red` / `B_mix` were changed.

## 2026-03-29 - Reduce the T3h membrane-lift gap to the exact kernel of the checked local lift map for clean simple support

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 25 from the T3g residual-class lift stage into the T3h global membrane-lift stage and wrote the exact corrected local quotient map `q_coeff = [[1,0,0],[0,1,0]]`, its membrane kernel `ker(q_coeff) = span(e_mem)`, and the corresponding global lift class `Lift_mem,n(q; c_sel)`.
- Recorded the sharpest current theorem-facing reduction: the remaining zero-excess / reverse-inclusion gap is now exactly the kernel of `q_coeff o delta_chk,n(q; c_sel)` on admissible same-trace global residuals, not merely a residual class named abstractly.
- Synced the theorem roadmap, verification map, and project journal so the next bottleneck is now to control the checked local lift-difference map `delta_chk` well enough to decide whether that kernel is trivial.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, active standalone clean `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path, or theorem-level status of `B_red` / `B_mix` were changed.

## 2026-03-29 - Reduce the T3g zero-excess gap to the exact residual-lift class for clean simple support

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 25 from the T3f shadow-only obstruction into the T3g residual-class lift stage and introduced the exact same-trace residual class `R_same,n(q) = ker(C_center,n(q)) = ker(J_0,n(q))` together with the exact quotient-invisible admissible lift class `R_inv,n(q; c_sel)`.
- Recorded the sharpest current theorem-facing reduction: the remaining zero-excess / reverse-inclusion question is now exactly whether `R_inv,n(q; c_sel) = {0}` for every repo-selected representative, equivalently whether the local membrane-kernel line `span(g_mem,n(q))` has any nonzero admissible global lift inside `ker(C_center,n(q))`.
- Synced the theorem roadmap, verification map, and project journal so the next bottleneck is no longer a generic shadow-only obstruction but the exact residual-lift triviality problem on the current repository/theory boundary.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, active standalone clean `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path, or theorem-level status of `B_red` / `B_mix` were changed.

## 2026-03-29 - Sharpen the T3f zero-excess gap to a shadow-only obstruction and conditional positive-excess template

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 25 from the T3e zero-excess criterion into the T3f stage and recorded the sharpest current theorem-facing obstruction: the checked local quotient condition is representative-lossy and adds no closed representative-level control beyond the selected shadow coordinates.
- Added the exact conditional counterexample template: if a nonzero admissible same-trace, quotient-invisible fiber residual exists, then it produces `Delta_H(c) > 0` immediately and breaks reverse inclusion on the current repository boundary.
- Refined the theorem roadmap, verification map, and project journal so the next bottleneck is no longer just Р Р†Р вЂљРЎС™prove `Delta_H = 0`Р Р†Р вЂљРЎСљ: it is now to prove or refute survival of a same-trace, quotient-invisible admissible fiber residual.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, active standalone clean `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path, or theorem-level status of `B_red` / `B_mix` were changed.

## 2026-03-29 - Isolate the T3e zero fiber-excess / selected-minimality obstruction above the T3d representative-law boundary

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 25 from the T3d representative-law note into the T3e fiberwise `H = A_int^T A_int + reg I` minimality stage and recorded the sharpest current theorem: every candidate-class element admits the exact same-trace decomposition `c = P_sel J_0(c) + z`, and the remaining bridge is exactly vanishing of the nonnegative fiber-excess functional `Delta_H(c) = z^T H z`.
- Refined the theorem roadmap, verification map, and project journal so the active bottleneck is no longer only the abstract representative law or vector orthogonality statement: the exact missing bridge is now zero fiber excess on the candidate class `A_sel^{th,cand}`.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, active standalone clean simple-support path, or theorem-level status of `B_red` / `B_mix` were changed.

## 2026-03-29 - Isolate the T3d representative-law / selected-minimality obstruction above the T3c comparison boundary

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 25 from the T3c comparison note into the T3d representative-law stage and recorded the sharpest current theorem: on the present repo-selected boundary the reverse inclusion target `c = P_sel J_0(c)` is equivalent to fiberwise `H = A_int^T A_int + reg I` minimality / orthogonality in the fixed-trace fiber.
- Refined the theorem roadmap, verification map, and project journal so the active bottleneck is no longer just a generic reverse-inclusion problem: the exact missing bridge is now the implication from shadow-compatible candidate-class membership to the global weak/KKT-selected `H`-minimal representative law.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, active standalone clean simple-support path, or theorem-level status of `B_red` / `B_mix` were changed.

## 2026-03-29 - Isolate the T3c comparison boundary between the exact repo-selected family and the stronger candidate class

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended the pilot-25 theorem note from the T3b candidate-class step into the T3c comparison/losslessness stage, and recorded the strongest current theorem as exact inclusion `A_sel^repo subseteq A_sel^{th,cand}` together with the exact reduction of the reverse inclusion to the missing selected-representative theorem `c = P_sel J_0(c)` for shadow-compatible admissible perturbations.
- Refined the theorem roadmap, verification map, and project journal so the active bottleneck is no longer Р Р†Р вЂљРЎС™define a stronger class at allР Р†Р вЂљРЎСљ: the stronger candidate class is already in place, and the current open theorem is now the exact comparison/losslessness step deciding whether the candidate class is already exhausted by the exact global weak/KKT-selected family.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, active standalone clean simple-support path, or theorem-level status of `B_red` / `B_mix` were changed.

## 2026-03-29 - Define the T3b shadow-compatible selected-class candidate above the closed T3a repo-selected bridge

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended the dedicated `T3b` proof-pilot note from a pure staging/obstruction memo into a concrete candidate-class package: trace-only and quotient-only readings are recorded as insufficient by themselves, while the strongest current theorem-facing candidate is now the shadow-compatible class `A_sel^{th,cand}` defined by the simultaneous selected-trace condition `J_0(c) in im(D_amp)` and checked local quotient compatibility `Q_chk(c) in im(D_rich,eta^corr) / span(g_mem)`.
- Refined the theorem roadmap, verification map, and project journal so `T3b` is no longer recorded only as an open class-definition bottleneck: the stronger theorem-facing class is now constructed at the candidate level, the strongest current comparison is the conservative inclusion `A_sel^repo subseteq A_sel^{th,cand}`, and the single remaining bottleneck is the exact comparison/losslessness theorem deciding whether the repo-selected family already exhausts that candidate class.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, active standalone clean simple-support path, or theorem-level status of `B_red` / `B_mix` were changed.

## 2026-03-29 - Open the T3b selected-class upgrade / obstruction stage above the closed T3a repo-selected bridge

Affected files:
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Added a dedicated `T3b` proof-pilot note that separates the exact current repository-selected class `A_sel^repo = A_ls = im(V_adm) = im(M_amp)` from the stronger theorem-facing selected/admissible class needed for full `T3`, and packages the next stage as a selected-class upgrade / obstruction problem rather than as another kernel-transfer note on the same repo boundary.
- Refined the theorem roadmap so `T3a` remains the closed enough finite-dimensional bridge on the current repo-selected class, while `T3b` is now recorded as the next theorem-facing stage: determine the exact relation between `A_sel^repo` and the stronger class seen so far only through the selected trace plane `im(D_amp)` and the checked local Outcome-B quotient object.
- Added a new verification-map entry for `T3b` and updated the project journal so the main bottleneck is now stated explicitly as the exact theorem-level construction/definition of the stronger selected class beyond its currently closed trace/quotient shadows.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, active standalone clean simple-support path, or theorem-level status of `B_red` / `B_mix` were changed.

## 2026-03-29 - Tighten and close enough the T3a finite-dimensional selected-kernel bridge package for clean simple support

Affected files:
- `proof_pilots/pilot_24_t3a_selected_kernel_bridge/pilot_24_t3a_selected_kernel_bridge.md`
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Tightened the dedicated proof-pilot note so it now states the exact `T3a` theorem target on the current repository-selected family `A_sel^repo = A_ls = im(V_adm) = im(M_amp)`, packages the explicit lemma split `T3a-L1`--`T3a-L5`, separates exact algebra from representative live shell checks, and adds the Lean-facing abstraction target without reopening the frozen local Outcome-B branch.
- Refined the theorem roadmap so `T3` remains the broader bridge program while `T3a` is now recorded as packaged and closed enough on the current repository-selected boundary, with the explicit caution that `B_red` / `B_mix` remain descendants only.
- Updated the verification map and project journal so they now record that the finite-dimensional selected-kernel bridge is closed enough on the current repo-selected boundary and that the remaining open work belongs to the broader long-term `T3`, not to a missing shell-specific ingredient inside `T3a`.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, clean solver behavior, candidate-load interpretation, or active standalone clean simple-support path were changed.



## 2026-03-27 - Sync criterion-planning docs after the non-decisive clean simple support pilot sequence

Affected files:
- `docs/theory/current_theory_verification_map.md`
- `docs/project_map.md`
- `CHANGELOG.md`

- Updated the verification map so it now reflects the live clean `simple support` competition set `n=4,6,7,8`, treats raw `sigma_min(B_mix)` explicitly as the current baseline rather than as a closed final criterion, and records that the main unresolved bottleneck has shifted from background reach to theorem-level criterion closure.
- Updated the project map so it now lists the clean criterion-diagnostic runners `run_simple_support_criterion_pilot_ac.py`, `run_simple_support_criterion_pilot_d.py`, and `run_simple_support_criterion_pilot_e.py`, and states that the next planned stage is a more theoretical criterion rework rather than another broad scan.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, or active clean `simple support` architecture were changed.


## 2026-03-27 - Add clean full simple support criterion pilot E and record that it remains non-decisive

Affected files:
- `docs/theory/current_simple_support_status.md`
- `docs/journal/project_journal_updated14.md`
- `tasks/run_simple_support_criterion_pilot_e.py`
- `CHANGELOG.md`

- Added `tasks/run_simple_support_criterion_pilot_e.py`, a non-invasive helper runner that keeps the main clean solver unchanged while evaluating an energy-like reduced-coercivity surrogate on the current competition set `n=4,6,7,8`.
- Ran the new pilot on broad/focused local windows and included targeted discretization checks for `n=6` and `n=8`, saving machine-readable summaries under `output/clean_full_simple_support/criterion_pilot_e_*.{json,csv}`.
- Updated the operational status and journal notes so they now record explicitly that `D` was useful but not decisive, that the first light `E` pilot gives interior-distributed reduced-coercivity signals without changing equations or BC meaning, and that `E` still does not settle the `n=6` versus `n=8` competition strongly enough to replace the conservative operational memory.
- Kept the scientific meaning unchanged: the main clean solver path, equations, honest background BC set, and critical boundary rows are unchanged; the E pilot is a diagnostic add-on and does not reconnect the old hybrid `F_min` path.

## 2026-03-27 - Add clean full simple support criterion pilot D and refresh post-A+C status

Affected files:
- `docs/theory/current_simple_support_status.md`
- `docs/journal/project_journal_updated14.md`
- `tasks/run_simple_support_criterion_pilot_d.py`
- `CHANGELOG.md`

- Added `tasks/run_simple_support_criterion_pilot_d.py`, a non-invasive helper runner that keeps the main clean solver unchanged while evaluating a local tangent-bundle restricted operator diagnostic on the current competition set `n=4,6,7,8`.
- Ran the new pilot on broad/focused local windows and included targeted discretization checks for `n=6` and `n=8`, saving machine-readable summaries under `output/clean_full_simple_support/criterion_pilot_d_*.{json,csv}`.
- Updated the operational status and journal notes so they now record explicitly that `A + C` did not materially improve discrimination, that the first light `D` pilot gives interior-dominated local signals without changing equations or BC meaning, and that `E` remains the explicit fallback / next heavier layer if `D` is not refined further.
- Kept the scientific meaning unchanged: the main clean solver path, equations, honest background BC set, and critical boundary rows are unchanged; the D pilot is a diagnostic add-on and does not reconnect the old hybrid `F_min` path.

## 2026-03-27 - Add clean full simple support criterion pilot A+C and refresh competition-memory docs

Affected files:
- `docs/theory/current_simple_support_status.md`
- `docs/journal/project_journal_updated14.md`
- `tasks/run_simple_support_criterion_pilot_ac.py`
- `CHANGELOG.md`

- Refreshed the canonical clean simple-support status snapshot so it now records the current clean competition picture around the exploratory `n=6` supported candidate near `17.6 MPa`, the `n=8` unstable rival, the `n=7` raw-but-unsupported reserve dips, the weak `n=4` control reading, and the shift of the unresolved bottleneck from background reach to criterion discrimination.
- Added a project-level journal update that fixes the next preferred strategy as the lighter criterion pilot `A + C`, while explicitly preserving `D` and then possibly `E` as fallback directions if the lighter pilot does not materially improve candidate discrimination or stability.
- Added `tasks/run_simple_support_criterion_pilot_ac.py`, a non-invasive helper runner that keeps the main clean solver unchanged while evaluating branch-aware local-valley descriptors together with an augmented / bordered solvability diagnostic on the current competition set `n=4,6,7,8`.
- Kept the scientific meaning unchanged: the pilot reuses the same clean simple-support equations, the same background BC set, and the same critical boundary rows, and it does not reconnect the old hybrid `F_min` path.

## 2026-03-26 - Upgrade the clean full simple-support search to the proven high-load background path

Affected files:
- `src/shell_buckling/mixed_weak/simple_support_high_load_background_continuation.py`
- `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`
- `docs/theory/current_simple_support_status.md`
- `docs/project_map.md`
- `CHANGELOG.md`

- Added a new reusable `src/...` bridge that lets the standalone clean full simple-support critical-search program reuse the proven honest high-load background continuation discipline from the separate pilot-21 path without shelling out to the old pilot runner and without falling back to the hybrid `F_min` background.
- Split the clean background handling into a directly solved low-load band plus high-load continuation from retained honest checkpoints using the same `u_z`-scaled secant solve and runtime-controlled step adaptation that had already been demonstrated separately on the active 6-state simple-support path.
- Re-ran the clean standalone `0..15 MPa` mixed-weak search for modes `n=2..6`; the honest background now stays converged through the full scheduled band, so the clean program genuinely probes the FEM-oriented `12..14 MPa` region instead of stalling near the earlier implementation loss at `4.3..4.5 MPa`.
- Narrow local refinements now place the main clean target-band candidates near `11.8 MPa` for `n=3`, `13.95 MPa` for `n=5`, and `14.25 MPa` for `n=6`, while keeping the language conservative: these are still exploratory clean-program candidates rather than final physical critical-load claims.


## 2026-03-26 - Run the first clean full simple-support critical-search campaign

Affected files:
- `docs/theory/current_simple_support_status.md`
- `CHANGELOG.md`

- Ran the first standalone clean full simple-support critical-search campaign with `tasks/run_full_simple_support_critical_search.py` on the honest 6-state background and the patched critical rows `[u_n(1), varphi(1), T_s(1), S(1), H(1)]` for modes `n=2..6`.
- The moderate `0..15 MPa` campaign did not reach the expected `12..14 MPa` band because the clean program lost the honest background at `4.5 MPa`; narrow local refinements then pushed the same clean path only to about `4.3246 MPa` before another background failure near `4.3276 MPa`.
- Recorded the current exploratory clean-program candidate loads as approximately `4.3215 MPa` (`n=2`), `4.3215 MPa` (`n=3`), `2.9 MPa` (`n=4`), `1.84 MPa` (`n=5`, but more oscillatory / sensitive), and `4.3154 MPa` (`n=6`), with the present unresolved bottleneck reading as honest-background continuation rather than a verified critical region near `12..14 MPa`.
- Kept the scientific language conservative: no equations or BC meanings changed, the old hybrid path was not reused for this campaign, and the reported loads remain exploratory numerical candidates rather than final physical critical loads.


## 2026-03-26 - Add standalone clean full simple-support critical-search program

Affected files:
- `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`
- `tasks/run_full_simple_support_critical_search.py`
- `docs/project_map.md`
- `docs/theory/boundary_condition_task_audit.md`
- `docs/theory/boundary_conditions_summary.md`
- `docs/theory/current_simple_support_status.md`
- `CHANGELOG.md`

- Added a new standalone reusable core module and task wrapper for the full hinged/simple-support critical-load search, keeping it in `src/...` and `tasks/...` instead of treating it as a pilot-only script.
- Reconnected the mixed-weak critical layer to the honest 6-state axisymmetric simple-support background, while keeping the preserved hybrid `F_min`-backed scan paths unchanged for comparison and diagnostics.
- Fixed the clean critical-layer boundary reading for the new program to `[u_n(1), varphi(1), T_s(1), S(1), H(1)]`, and set the first-pass default circumferential range explicitly to `n=2..6` with no automatic legacy `13/14` targeted windows.
- Updated the project map, BC audit, BC summary, and current simple-support status page so the repository now classifies the new path as the preferred clean full simple-support critical-search program while preserving the older hybrid scans.

## 2026-03-26 - Add validated-operational-milestone policy for post-audited simple-support loads

Affected files:
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/continuation_runtime.py`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_continuation_workflow.md`
- `docs/theory/current_simple_support_status.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/theory/current_mixed_weak_theory_note.tex`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Introduced an explicit intermediate reporting class `validated operational milestone` for the separate 6-state simple-support path so high-load same-branch points do not have to be described either as generic operational evidence or as audited ceiling replacements.
- Kept the audited-ceiling meaning unchanged: the canonical pilot-21 audited ceiling remains `4.3800 MPa`, and promotion beyond it still requires explicit strict audit closure under the current standard.
- Reclassified the already documented `4.4000 MPa`, `7.0000 MPa`, and `10.0000 MPa` points as validated operational milestones on the basis of their stored same-seed, no-branch-jump, smooth-repeat-drift, sane-BC, unchanged-gradient-order, and short-probe-no-failure evidence.
- Updated the pilot-21 runtime policy and workflow note so future confirm summaries use the new status class, and made the next `10 -> 15 MPa` confirm-critical retention schedule explicit at `11.0`, `12.0`, `12.5`, `13.0`, `13.5`, `14.0`, and `15.0 MPa`.
- Recorded explicitly that this is a reporting / project-discipline change only: equations, simple-support BCs, mixed-weak scans, and the current numerical-vs-physical barrier reading are unchanged.

## 2026-03-26 - Extend pilot-21 operational continuation to 10 MPa and add exact-load shallow-vs-current plots

Affected files:
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/fast_progress.json`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/confirm_results.json`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_continuation_workflow.md`
- `proof_pilots/pilot_22_exact_load_shallow_vs_current_simple_support_comparison/compare_exact_loads.py`
- `proof_pilots/pilot_22_exact_load_shallow_vs_current_simple_support_comparison/pilot_22_exact_load_shallow_vs_current_simple_support_comparison.md`
- `proof_pilots/pilot_22_exact_load_shallow_vs_current_simple_support_comparison/comparison_results.json`
- `proof_pilots/pilot_22_exact_load_shallow_vs_current_simple_support_comparison/figures/current_vs_shallow_exact_4.0_mpa.png`
- `proof_pilots/pilot_22_exact_load_shallow_vs_current_simple_support_comparison/figures/current_vs_shallow_exact_7.0_mpa.png`
- `proof_pilots/pilot_22_exact_load_shallow_vs_current_simple_support_comparison/figures/current_vs_shallow_exact_10.0_mpa.png`
- `docs/theory/current_simple_support_status.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/project_map.md`
- `CHANGELOG.md`

- Continued the separate pilot-21 fast `u_z`-scaled + auxiliary arc-like path from `6.0000 MPa` through retained exact targets `6.5000`, `7.0000`, `8.0000`, `9.0000`, and `10.0000 MPa` without replaying the branch from scratch and without hitting a bounded failure event in the saved fast ladder.
- Ran sparse confirms at `7.0000` and `10.0000 MPa`; both kept the same accepted seed, showed no branch-jump suspicion, stayed classified as operational continuation evidence, and did not hit short probe failures through `10.0200 MPa`, while `strict_reproducible` and `near_reproducible` both remained false under the current policy.
- Added a new exact-load comparison pilot that reuses the pilot-16 shallow simple-support solver together with the existing `arrays_nepol_sin(...)` mapping from the current 6-state path to plot `theta`, `theta'`, `Phi`, and `Phi'` at exact loads `4.0`, `7.0`, and `10.0 MPa`.
- Recorded that the exact-load shallow-vs-current mismatch is already moderately visible at `4.0 MPa`, becomes clearly visible at `7.0 MPa`, stays clearly visible at `10.0 MPa`, and remains dominated by right-edge differences while still staying smooth through the available high-load range rather than showing a new barrier-localized jump.
- Refreshed the pilot-21 workflow note, the current simple-support operational status page, the verification-map strategy note, and the project map so they now reflect operational continuation evidence through `10.0000 MPa`, sparse confirms through `10.0200 MPa`, and the new exact-load comparison pilot without promoting any post-`4.3800 MPa` load to audited-ceiling language.

## 2026-03-26 - Generalize runtime-cache policy and harden pilot-21 bootstrap-anchor repair

Affected files:
- `AGENTS.md`
- `.gitignore`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/continuation_runtime.py`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_u_z_scaled_arc_like_continuation.py`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_continuation_workflow.md`
- `README.md`
- `docs/project_map.md`
- `CHANGELOG.md`

- Added a repo-wide rule that mass runtime artifacts such as checkpoints, append-only progress logs, ad hoc confirm dumps, and temporary resume caches are local runtime cache by default, while compact summaries and deliberately curated exports remain the normal tracked artifacts.
- Generalized `.gitignore` from pilot-21-specific cache paths to the reusable `proof_pilots/*/fast_run/` cache layout without hiding compact tracked summaries such as `confirm_results.json`.
- Hardened the pilot-21 fast-run bootstrap-anchor repair path so copied or legacy run directories can recover the named `bootstrap_previous` / `scaled_anchor` pointers from disk before falling back to an expensive rebuild, and stale `bootstrap_older_checkpoint` metadata is normalized away explicitly.
- Made the next planned `6 -> 10 MPa` confirm-critical milestones `6.5`, `7.0`, `8.0`, `9.0`, and `10.0 MPa` explicit in the runtime checkpoint policy so pruning does not silently drop them once they are reached.
- Refreshed the operational workflow docs to describe the repo-wide cache convention, the repaired bootstrap-anchor behavior, and the explicit long-climb milestone-retention schedule.

## 2026-03-26 - Remove the hidden fast-run step cap and formalize pilot-21 audit policy

Affected files:
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/continuation_runtime.py`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_u_z_scaled_arc_like_continuation.py`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/confirm_u_z_scaled_arc_like_continuation.py`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_continuation_workflow.md`
- `docs/theory/current_simple_support_status.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/theory/current_mixed_weak_theory_note.tex`
- `README.md`
- `docs/project_map.md`
- `CHANGELOG.md`

- Removed the hidden fast-run dependence on the historical pilot-21 `MAX_STEP_MPA = 0.0025` controller cap by moving the operational step-growth / conditioning-shrink policy into the pilot-21 runtime layer, while leaving the bounded historical pilot script unchanged as the audited artifact.
- Added explicit runtime-controlled fast-step parameters (`min`, `max`, `success_growth`, `conditioning_shrink`, `failure_shrink`) plus explicit milestone retention controls (`milestone_grid_mpa`, repeated `--milestone-load-mpa`) so the fast runner now respects user-configured step limits and preserves confirm-critical loads intentionally.
- Formalized the pilot-21 audit policy by separating same-branch indicators from promotion language, keeping the inherited `strict_reproducible` thresholds explicit as an open audit-policy issue rather than a silent branch-loss interpretation.
- Updated the confirm runner to report same-branch indicators, promotion-policy classification, and an adaptive high-load probe step, while keeping confirm cheap and milestone-focused.
- Ran a short ignored validation campaign from `6.0000` to `6.0200 MPa` with `--max-step-mpa 0.0050`: the accepted steps reached `0.003375`, `0.00455625`, and `0.0050 MPa`, so the fast layer now genuinely exceeds the old hidden `0.0025 MPa` cap without breaking resume, pruning, or confirm mode.

## 2026-03-26 - Add rolling+milestones checkpoint retention and untrack pilot-21 runtime cache

Affected files:
- `.gitignore`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/continuation_runtime.py`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_u_z_scaled_arc_like_continuation.py`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/confirm_u_z_scaled_arc_like_continuation.py`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_continuation_workflow.md`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/fast_progress.json`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/progress_log.jsonl`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/checkpoints/*`
- `README.md`
- `docs/project_map.md`
- `CHANGELOG.md`

- Added explicit checkpoint retention modes `all`, `rolling`, `milestones`, and `rolling+milestones`, with `rolling+milestones` as the default operational policy for the pilot-21 fast continuation runner.
- Made the default policy retain only the bootstrap anchor files, the active resume pair, milestone-context checkpoints, a bounded rolling history, and any failure/suspicious context instead of keeping every accepted-step checkpoint.
- Updated the confirm runner so it fails explicitly when a requested load was pruned from the local cache, rather than assuming every historical checkpoint is always retained.
- Marked the pilot-21 runtime checkpoint directory and append-only progress log as local cache in `.gitignore`, kept `fast_progress.json` and `confirm_results.json` as the tracked summaries, and removed the previously tracked runtime cache files from the git index.
- Validated the new default policy with a no-op prune refresh on the canonical `fast_run` directory and a separate ignored resume test in `output/`, where a pruned copy resumed from `6.0000` to `6.0050 MPa` and then reopened cleanly as a no-op run.

## 2026-03-26 - Extend fast simple-support continuation to 6.0000 MPa and diagnose strict reproducibility drift

Affected files:
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/fast_progress.json`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/progress_log.jsonl`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/confirm_results.json`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/confirm_5p0000_5p5000_6p0000_milestones.json`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_continuation_workflow.md`
- `docs/theory/current_simple_support_status.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/theory/current_mixed_weak_theory_note.tex`
- `docs/journal/project_journal_updated14.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/assumptions/assumptions.md`
- `CHANGELOG.md`

- Resumed the stored pilot-21 fast path from `4.5000 MPa` to `6.0000 MPa` without replaying the lower ladder, without changing the 6-state equations or the simple-support BC set, and without hitting a bounded failure event in the saved fast ladder.
- Ran sparse milestone confirms at `5.0000`, `5.5000`, and `6.0000 MPa`; all three kept the same accepted seed, showed no branch-jump suspicion, and did not hit short failure probes through `6.0040 MPa`, while `strict_reproducible` stayed false throughout and `near_reproducible` turned false above `5.0 MPa` because the repeat drift gradually exceeded the current threshold.
- Recorded a targeted diagnosis that the remaining `strict_reproducible = false` signal is presently dominated by the inherited pilot-12 threshold policy (`1e-7 / 1e-6`) rather than by clear branch loss: the observed repeat drift stays smooth, same-seed, and much smaller than the ordinary adjacent-step continuation drift.
- Refreshed the pilot-21 workflow note and the key status/theory/project-memory documents so they now keep the audited `4.3800 MPa` ceiling explicit, keep `4.4000 MPa` as the strongest non-promoted milestone point, and record operational continuation evidence through `6.0000 MPa` plus short confirm probes through `6.0040 MPa`.

## 2026-03-26 - Audit 4.4000 milestone and extend fast continuation to 4.5000

Affected files:
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/fast_progress.json`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/progress_log.jsonl`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/confirm_results.json`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/confirm_4p4000_audit_pass1.json`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/confirm_4p4000_audit_pass2.json`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/confirm_4p4600_4p5000_milestones.json`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_continuation_workflow.md`
- `docs/theory/current_simple_support_status.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/theory/current_mixed_weak_theory_note.tex`
- `docs/journal/project_journal_updated14.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/assumptions/assumptions.md`
- `CHANGELOG.md`

- Ran a stricter dedicated milestone audit at `4.4000 MPa`: two independent pointwise confirm passes stayed `near_reproducible` on the same accepted seed, showed no branch-jump suspicion, and did not hit a short failure probe through `4.4100 MPa`, but `strict_reproducible` still remained false.
- Resumed the stored fast pilot-21 path through `4.4200`, `4.4400`, `4.4600`, `4.4800`, and `4.5000 MPa` without replaying the lower ladder, without changing the 6-state equations or the simple-support BC set, and without recording a bounded failure event in the saved fast ladder.
- Ran sparse milestone confirms at `4.4600 MPa` and `4.5000 MPa`; both stayed `near_reproducible`, showed no branch-jump suspicion, and did not hit short failure probes through `4.4640 MPa` and `4.5040 MPa`, so the newer loads remain operational continuation evidence rather than a new canonical audited ceiling.
- Refreshed the pilot-21 workflow note and the key status/theory/project-memory documents so they now distinguish the audited pilot-21 `4.3800 MPa` ceiling from the stronger-but-still-non-audited `4.4000 MPa` milestone audit and the newer operational continuation evidence through `4.5000 MPa`.

## 2026-03-26 - Add pilot 21 fast checkpointed continuation layer and full simple-support status sync

Affected files:
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/continuation_runtime.py`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_u_z_scaled_arc_like_continuation.py`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/confirm_u_z_scaled_arc_like_continuation.py`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_continuation_workflow.md`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/pilot_21_u_z_scaled_arc_like_continuation.md`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/fast_progress.json`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/progress_log.jsonl`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/confirm_results.json`
- `docs/theory/current_simple_support_status.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/theory/current_mixed_weak_theory_note.tex`
- `README.md`
- `docs/project_map.md`
- `docs/journal/project_journal_updated14.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/assumptions/assumptions.md`
- `CHANGELOG.md`

- Added a reusable pilot-21 runtime layer with checkpoint I/O, a fast resumable continuation runner, and a separate confirm runner, while keeping the same 6-state equations and the same simple-support BC set unchanged.
- Ran a first from-scratch fast continuation from the current audited pilot-21 path to `4.3900 MPa`, then resumed the stored path to `4.4000 MPa` without replaying the full ladder, and kept the confirm logic pointwise instead of repeating a broad pilot audit.
- Recorded that the milestone confirm at `4.4000 MPa` remains `near_reproducible` with the same accepted seed, shows no branch-jump suspicion, and does not hit a short first-failure probe through `4.4040 MPa`; this is still operational continuation evidence, not a new canonical audited ceiling or a final physical critical load claim.
- Synchronized the key status/theory/project-memory documents so they now consistently distinguish the old-path `4.3434 / 4.3440 MPa` pair, the pilot-20 `4.3520 MPa` ceiling, the audited pilot-21 `4.3800 MPa` ceiling, and the newer fast-run checkpoints above that audited level.
## 2026-03-26 - Add pilot 21 u_z-scaled arc-like continuation and refresh simple-support status

Affected files:
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/pilot_21_u_z_scaled_arc_like_continuation.md`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/u_z_scaled_arc_like_continuation.py`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/u_z_scaled_arc_like_results.json`
- `docs/theory/current_simple_support_status.md`
- `docs/theory/current_theory_verification_map.md`
- `CHANGELOG.md`

- Added a dedicated pilot-21 package that stops treating arc-like control as a separate competing method and instead uses the exact pilot-20 `u_z`-scaled path as the main continuation formulation with bounded arc-like step adaptation layered on top.
- Ran the staged ladder through `4.3520`, `4.3550`, `4.3600`, `4.3700`, and `4.3800 MPa`, recording reproducible stage retests at every planned target and no bounded failure inside the packaged ladder while keeping the 6-state equations and simple-support BC set unchanged.
- Updated the canonical simple-support status and verification map so they now distinguish the old-path `4.3434 / 4.3440 MPa` anchor/failure pair, the pilot-20 standalone `4.3520 MPa` method ceiling, and the new pilot-21 bounded continuation ceiling `4.3800 MPa` without promoting any of them to a final physical critical load.

## 2026-03-25 - Add pilot 20 simple-support method sweep and update ceiling status

Affected files:
- `proof_pilots/pilot_20_method_sweep_for_simple_support_ceiling/pilot_20_method_sweep_for_simple_support_ceiling.md`
- `proof_pilots/pilot_20_method_sweep_for_simple_support_ceiling/method_sweep.py`
- `proof_pilots/pilot_20_method_sweep_for_simple_support_ceiling/method_sweep_results.json`
- `proof_pilots/pilot_20_method_sweep_for_simple_support_ceiling/method_comparison_table.md`
- `docs/theory/current_simple_support_status.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/theory/current_mixed_weak_theory_note.tex`
- `CHANGELOG.md`

- Added a bounded pilot-20 method sweep that keeps the active 6-state simple-support equations and BCs fixed while comparing the old continuation path, a stronger predictor bundle, an arc-like step-control surrogate, a `u_z`-scaled state representation, and a packaged bulk/right-edge domain-split prototype.
- Ran the sweep and recorded that the old single-domain path still stops at the reproducible `4.3434 / 4.3440 MPa` ceiling/failure pair, while the best bounded packaged result comes from the unchanged-equation `u_z`-scaled solve, which reaches `4.3520 MPa` without a bounded failure being hit in the pilot-20 ladder.
- Updated the canonical simple-support status and the compact theory / verification notes so they now reflect the sharper interpretation that the present ceiling remains mainly numerical but is more sensitive to formulation and conditioning than to simple right-edge mesh concentration alone.

## 2026-03-25 - Add canonical simple-support status page and conservative documentation deduplication

Affected files:
- `README.md`
- `docs/project_map.md`
- `docs/project_layering_refactor_note.md`
- `docs/theory/current_simple_support_status.md`
- `docs/theory/current_mixed_weak_theory_note.tex`
- `docs/theory/current_theory_verification_map.md`
- `docs/theory/boundary_condition_task_audit.md`
- `docs/theory/boundary_conditions_summary.md`
- `tasks/run_mixed_weak_boundary_matrix_scan.py`
- `tasks/run_mixed_weak_targeted_scan.py`
- `CHANGELOG.md`

- Added `docs/theory/current_simple_support_status.md` as the canonical operational status page for the separate active 6-state simple-support background path, including the active module, reproducible `4.3434 MPa` anchor, persistent `4.3440 MPa` failure, current barrier reading, shallow/non-shallow status, next step, and canonical runnable entry points.
- Reduced duplicated simple-support status text across README, project map, BC audit/summary notes, and the compact theory note by replacing stale repeated operational blurbs with short role-appropriate pointers to the new canonical status page.
- Added `docs/project_layering_refactor_note.md` and refreshed nearby script/document wording so the active mixed-weak `F_min` testbench path, the separate 6-state simple-support path, the supporting moving-clamp/sliding-clamp path, and the old-vs-new shallow-comparator situation are easier to distinguish without moving code.

## 2026-03-25 - Add pilot 19 edge-stretched simple-support continuation comparison

Affected files:
- `proof_pilots/pilot_19_edge_stretched_simple_support_continuation/pilot_19_edge_stretched_simple_support_continuation.md`
- `proof_pilots/pilot_19_edge_stretched_simple_support_continuation/edge_stretched_continuation.py`
- `proof_pilots/pilot_19_edge_stretched_simple_support_continuation/edge_stretched_results.json`
- `proof_pilots/pilot_19_edge_stretched_simple_support_continuation/comparison_note.md`
- `CHANGELOG.md`

- Added a dedicated pilot-19 package that keeps the active 6-state simple-support equations and BCs unchanged while testing two edge-aware right-edge mesh representations against the current documented pilot-12 continuation ceiling.
- Ran the bounded comparison and recorded that the best usable edge-aware path `edge_power_tail` still reaches `4.3434 MPa` and still fails first at `4.3440 MPa`, with small BC residuals and strong right-edge concentration, so no material upward ceiling shift was observed.
- Recorded that the more aggressive two-zone ultra-edge mesh does not produce a usable continuation path in the bounded pilot-19 run because the anchor ramp already fails by mesh-node exhaustion.

## 2026-03-22 - Translate supervisor theory note into Russian and make Russian maintenance explicit

Affected files:
- `docs/theory/current_mixed_weak_theory_note.tex`
- `AGENTS.md`
- `docs/theory/AGENTS.md`
- `CHANGELOG.md`

- Rewrote the supervisor-facing mixed-weak theory note into Russian while preserving the mathematics, notation, status distinctions, and the current repository-level caveats.
- Kept the simple-support status aligned with the current repository record, including the separate 6-state background path, the reproducible `4.3434 MPa` anchor, the persistent `4.3440 MPa` staged failure, the mainly numerical right-edge-layer bottleneck reading, and the corrected shallow/non-shallow mismatch onset around `2..3 MPa` without a special ceiling-localized jump.
- Made the AGENTS guidance explicit that `docs/theory/current_mixed_weak_theory_note.tex` should be written and maintained in Russian for supervisor-facing use, without changing notation, formulas, or claim-status semantics.

## 2026-03-21 - Add pilot 18 revised analytic barrier diagnosis and refresh theory-facing simple-support status

Affected files:
- `docs/theory/current_mixed_weak_theory_note.tex`
- `docs/theory/current_theory_verification_map.md`
- `proof_pilots/pilot_18_revised_analytic_barrier_diagnosis/pilot_18_revised_analytic_barrier_diagnosis.md`
- `proof_pilots/pilot_18_revised_analytic_barrier_diagnosis/barrier_problem_statement.md`
- `proof_pilots/pilot_18_revised_analytic_barrier_diagnosis/edge_layer_scaling.md`
- `proof_pilots/pilot_18_revised_analytic_barrier_diagnosis/analysis_common.py`
- `proof_pilots/pilot_18_revised_analytic_barrier_diagnosis/jacobian_conditioning_check.py`
- `proof_pilots/pilot_18_revised_analytic_barrier_diagnosis/term_balance_check.py`
- `proof_pilots/pilot_18_revised_analytic_barrier_diagnosis/branch_state_cache.npz`
- `proof_pilots/pilot_18_revised_analytic_barrier_diagnosis/branch_state_cache.json`
- `proof_pilots/pilot_18_revised_analytic_barrier_diagnosis/jacobian_conditioning_results.json`
- `proof_pilots/pilot_18_revised_analytic_barrier_diagnosis/term_balance_results.json`
- `CHANGELOG.md`

- Updated the supervisor-facing mixed-weak theory note so the simple-support discussion now reflects the reproducible `4.3434 MPa` anchor, the persistent `4.3440 MPa` failure, the BC-corrected shallow comparator history, the corrected `2..3 MPa` mismatch onset, and the still-open final shell / mixed-BVP / physical-load status.
- Added a dedicated pilot-18 analytic diagnosis package with a compact problem statement, a heuristic edge-layer note, a shared branch-cache helper, and two runnable diagnostics for Jacobian conditioning and term-balance structure near the current ceiling.
- Ran the new diagnostics and recorded that the coarse Jacobian remains severely ill-conditioned but shows no collapsing near-zero-singular-value trend, while the right-edge term balance stays smooth and is dominated by the geometric hoop contribution `u_r/x`, the `T_sn -> M_s -> varphi` chain, and a large `u_z` response with only moderate trig-gap corrections.

## 2026-03-21 - Add pilot 17 corrected shallow-vs-non-shallow simple-support divergence sweep

Affected files:
- `proof_pilots/pilot_17_shallow_vs_nonshallow_simple_support_divergence/pilot_17_shallow_vs_nonshallow_simple_support_divergence.md`
- `proof_pilots/pilot_17_shallow_vs_nonshallow_simple_support_divergence/comparison_problem_statement.md`
- `proof_pilots/pilot_17_shallow_vs_nonshallow_simple_support_divergence/numerical_comparison.py`
- `proof_pilots/pilot_17_shallow_vs_nonshallow_simple_support_divergence/term_attribution.py`
- `proof_pilots/pilot_17_shallow_vs_nonshallow_simple_support_divergence/comparison_results.json`
- `proof_pilots/pilot_17_shallow_vs_nonshallow_simple_support_divergence/comparison_cache.npz`
- `proof_pilots/pilot_17_shallow_vs_nonshallow_simple_support_divergence/term_attribution_results.json`
- `docs/theory/current_theory_verification_map.md`
- `CHANGELOG.md`

- Added a dedicated pilot-17 sweep that compares the active 6-state non-shallow simple-support branch against the new pilot-16 shallow simple-support comparator rather than the older BC-mismatched shallow path.
- Ran the bounded corrected sweep from `0.02 MPa` to `4.3434 MPa` and recorded that the mismatch is small at low load, first becomes clearly visible in any variable at `2.0 MPa`, becomes clearly overall visible at `3.0 MPa`, and then grows with load.
- Added a matching term-attribution pass showing that geometric hoop terms remain structurally large, while the growth of the corrected mismatch correlates most strongly with the `theta0` / `theta0'` trigonometric and cosine-factor corrections; the available high-load range stays smooth rather than showing a new barrier-localized qualitative jump.

## 2026-03-21 - Add pilot 16 shallow simple-support comparator

Affected files:
- `proof_pilots/pilot_16_shallow_simple_support_comparator/pilot_16_shallow_simple_support_comparator.md`
- `proof_pilots/pilot_16_shallow_simple_support_comparator/shallow_problem_statement.md`
- `proof_pilots/pilot_16_shallow_simple_support_comparator/shallow_bc_derivation_check.py`
- `proof_pilots/pilot_16_shallow_simple_support_comparator/shallow_simple_support_solver.py`
- `CHANGELOG.md`

- Added a dedicated pilot-16 shallow simple-support comparator instead of reusing the older shallow moving-clamp/sliding-clamp comparison path.
- Recorded the compact repository-level shallow simple-support BC set `theta0(x0)=0`, `Phi0(x0)=0`, `Phi0(1)=0`, `theta0'(1)+nu*theta0(1)=0`, with the force BC exact under the live mapping and the moment BC derived from the shallow limit of the exact shell mapping.
- Ran the structural BC derivation check and the new shallow simple-support continuation solver, which converged through the verification ladder up to `4.3434 MPa`.

## 2026-03-21 - Add pilot 15 shallow BC equivalence audit

Affected files:
- `proof_pilots/pilot_15_shallow_bc_equivalence_audit/pilot_15_shallow_bc_equivalence_audit.md`
- `proof_pilots/pilot_15_shallow_bc_equivalence_audit/bc_equivalence_audit.md`
- `proof_pilots/pilot_15_shallow_bc_equivalence_audit/symbolic_bc_mapping_check.py`
- `proof_pilots/pilot_15_shallow_bc_equivalence_audit/recommendation_note.md`
- `CHANGELOG.md`

- Added a dedicated pilot-15 audit to check whether the repository's current shallow comparison path uses BCs that are physically equivalent to the active 6-state non-shallow simple-support branch.
- Recorded the exact live BC vectors from the shallow supporting path, the supporting 6-state non-shallow comparison path, and the active 6-state simple-support background path.
- Added a structural mapping check showing that the shallow path aligns with the moving-clamp / sliding-clamp edge type through `varphi(1)=0`, not with the simple-support edge condition `M_s(1)=0`.

## 2026-03-21 - Add pilot 13 shallow-vs-non-shallow divergence source sweep and attribution

Affected files:
- `proof_pilots/pilot_13_shallow_nonshallow_divergence_source/pilot_13_shallow_nonshallow_divergence_source.md`
- `proof_pilots/pilot_13_shallow_nonshallow_divergence_source/load_sweep_comparison.py`
- `proof_pilots/pilot_13_shallow_nonshallow_divergence_source/term_attribution.py`
- `proof_pilots/pilot_13_shallow_nonshallow_divergence_source/load_sweep_results.json`
- `proof_pilots/pilot_13_shallow_nonshallow_divergence_source/load_sweep_cache.npz`
- `proof_pilots/pilot_13_shallow_nonshallow_divergence_source/term_attribution_results.json`
- `docs/theory/current_theory_verification_map.md`
- `CHANGELOG.md`

- Added a dedicated pilot-13 load sweep that compares the repository's shallow path against the mapped active 6-state non-shallow simple-support branch from `0.02 MPa` up to the reproducible `4.3434 MPa` high-load anchor.
- Ran the bounded sweep and recorded that the mapped shallow/non-shallow mismatch is already clearly present at the first sampled low load, remains right-edge dominated overall, and does not grow toward the `4.3434 MPa` continuation barrier.
- Added a term-attribution pass using the current repository formulas and recorded that the explicit small-angle / radius corrections in the `theta0` and `theta0'` mappings stay tiny at low load, while larger geometric contributions such as `ur/x` are present from the start, so the early mismatch is not explained by a new high-load-only non-shallow correction.


## 2026-03-21 - Add pilot 12 staged branch extension above the reproducible 4.3434 MPa simple-support point

Affected files:
- `proof_pilots/pilot_12_high_load_branch_extension/pilot_12_high_load_branch_extension.md`
- `proof_pilots/pilot_12_high_load_branch_extension/numerical_extension.py`
- `proof_pilots/pilot_12_high_load_branch_extension/branch_consistency_check.md`
- `proof_pilots/pilot_12_high_load_branch_extension/extension_results.json`
- `docs/theory/current_theory_verification_map.md`
- `CHANGELOG.md`

- Added a dedicated pilot-12 branch-extension workflow that reboots the validated high-load 6-state simple-support branch, repeats `4.3434 MPa` from the same predecessor pair, and then attempts a staged ladder above that point with continuity and branch-jump diagnostics.
- Ran the bounded extension script and confirmed that `4.3434 MPa` is reproducible on the same `secant_profile_mesh` strategy, with the repeated same-load retests converging to the same saved solution and no branch-jump signal.
- Recorded that the first new ladder step `4.3440 MPa` still fails for all tried seeds by mesh-node exhaustion with tiny BC residuals and strong right-edge concentration, so the branch anchor is now reproducible but the ceiling has not yet moved beyond 4.35 MPa.

## 2026-03-21 - Add pilot 11 shallow-vs-non-shallow barrier comparison near the simple-support high-load barrier

Affected files:
- `proof_pilots/pilot_11_shallow_vs_nonshallow_barrier_comparison/pilot_11_shallow_vs_nonshallow_barrier_comparison.md`
- `proof_pilots/pilot_11_shallow_vs_nonshallow_barrier_comparison/comparison_problem_statement.md`
- `proof_pilots/pilot_11_shallow_vs_nonshallow_barrier_comparison/numerical_comparison.py`
- `proof_pilots/pilot_11_shallow_vs_nonshallow_barrier_comparison/comparison_results.json`
- `CHANGELOG.md`

- Added a bounded pilot-11 comparison between the active 6-state simple-support branch and the repository's existing shallow comparison path using the live non-shallow-to-shallow mapping formulas already present in the supporting scripts.
- Ran the comparison near the current high-load barrier neighborhood and recorded that the bounded pilot-11 run reaches `4.3434 MPa` on the non-shallow branch after two mesh-pressure failures on raw-mesh seeds and a successful `secant_profile_mesh` rescue.
- Recorded that the mapped non-shallow vs shallow mismatch is already present below the barrier and changes only weakly from `4.3400` to `4.3434 MPa`, so the shallow comparison is informative but not a clean same-branch barrier detector by itself.

## 2026-03-21 - Add pilot 10 staged high-load continuation campaign for the 6-state simple-support background

Affected files:
- `proof_pilots/pilot_10_high_load_simple_support_continuation/pilot_10_high_load_simple_support_continuation.md`
- `proof_pilots/pilot_10_high_load_simple_support_continuation/continuation_campaign.py`
- `proof_pilots/pilot_10_high_load_simple_support_continuation/branch_diagnostics.md`
- `proof_pilots/pilot_10_high_load_simple_support_continuation/campaign_results.json`
- `docs/theory/current_theory_verification_map.md`
- `CHANGELOG.md`

- Added a new pilot-10 continuation campaign for the active 6-state simple-support background with staged band runs, bounded runtime budgets, and incremental JSON progress logging.
- Kept the same 6-state equations and simple-support BC set, but rebuilt the campaign around the validated high-load local branch rather than a smoother alternative branch.
- Added a concise branch-diagnostics note recording the bounded `4.34..4.50 MPa` band result and the finer rescue-local refinement that reaches about `4.3433 MPa` before `4.3434 MPa` remains unresolved by mesh-node exhaustion.
- Tightened the verification-map wording for V-ST1 without changing its status from `strategy only`.

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
- Added a boundary-condition summary table for `Р В Р’В Р РЋРІР‚вЂќР В Р’В Р РЋРІР‚СћР В Р’В Р СћРІР‚ВР В Р’В Р В РІР‚В Р В Р’В Р РЋРІР‚ВР В Р’В Р вЂ™Р’В¶Р В Р’В Р В РІР‚В¦Р В Р’В Р вЂ™Р’В°Р В Р Р‹Р В Р РЏ Р В Р’В Р вЂ™Р’В·Р В Р’В Р вЂ™Р’В°Р В Р’В Р СћРІР‚ВР В Р’В Р вЂ™Р’ВµР В Р’В Р вЂ™Р’В»Р В Р’В Р РЋРІР‚СњР В Р’В Р вЂ™Р’В°` versus `Р В Р’В Р РЋРІР‚вЂќР В Р’В Р РЋРІР‚СћР В Р’В Р СћРІР‚ВР В Р’В Р В РІР‚В Р В Р’В Р РЋРІР‚ВР В Р’В Р вЂ™Р’В¶Р В Р’В Р В РІР‚В¦Р В Р Р‹Р Р†Р вЂљРІвЂћвЂ“Р В Р’В Р Р†РІР‚С›РІР‚вЂњ Р В Р Р‹Р Р†РІР‚С™Р’В¬Р В Р’В Р вЂ™Р’В°Р В Р Р‹Р В РІР‚С™Р В Р’В Р В РІР‚В¦Р В Р’В Р РЋРІР‚ВР В Р Р‹Р В РІР‚С™ / simple support`.
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






















## 2026-03-27 - Freeze the clean `simple support` theorem target and derive the reduced tangent operator candidate

Affected files:
- `docs/theory/current_theory_verification_map.md`
- `docs/assumptions/assumptions.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/journal/project_journal_updated14.md`
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/reduction_check.py`
- `CHANGELOG.md`

- Froze the clean theorem-facing C1 target on the active `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` path: the full stacked linearized mixed object is now recorded explicitly as the preferred theorem-level target, while raw `B_mix` is kept only as the current boundary-only baseline.
- Added proof pilot 23 with a live/CAS check of the current reduction layer: it splits `C_center` into amplitude and true regularity rows, rebases the current `V_reg` span to canonical reduced coordinates, and derives the preferred reduced tangent candidate `L_red = [A_int; B_full] V_adm`.
- Updated the verification map, assumptions register, theory derivation file, and project journal so the next proof obligations are now explicit: C3 kernel-equivalence for the clean reduced object and C4 the decision whether a genuine quadratic-form / second-variation object exists.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, broad scans, or hybrid `F_min` reuse policy were changed.

## 2026-03-27 - Close the restricted C3 kernel-equivalence statement for the clean reduced family

- Affected files:
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/reduction_check.py`
- `docs/theory/current_theory_verification_map.md`
- `docs/assumptions/assumptions.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 23 from C1/C2 into C3 by making the exact restricted statement explicit: on the current chosen reduced family `A_repo = im(V_adm)`, the coordinate map `a -> V_adm a` identifies `ker(L_red)` with `A_repo Р Р†РІвЂљВ¬Р’В© ker(L_full)`.
- Added the matching basis-change and boundary-descendant logic: right multiplication by an invertible reduced-coordinate matrix leaves the reduced-kernel question unchanged, and `B_mix = B_red G_amp` is now recorded explicitly as a coordinate change on the same family rather than as a new theorem-level object.
- Updated the verification map, assumptions register, theory derivation file, and project journal to separate what is now closed at the finite-dimensional reduced-family level from what remains open: losslessness of the restriction to `im(V_adm)`, any collapse `ker(L_red) <-> ker(B_red) / ker(B_mix)`, and the later C4 quadratic-form decision.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, broad scans, or hybrid `F_min` reuse policy were changed.

## 2026-03-27 - Delimit C3b losslessness: exact current KKT family closed, continuum equality still open

- Affected files:
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/reduction_check.py`
- `docs/theory/current_theory_verification_map.md`
- `docs/assumptions/assumptions.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended pilot 23 into C3b by separating three layers explicitly: the theorem-facing full admissible clean tangent space, the large weighted-trial coefficient space satisfying `C_reg = 0`, and the exact current KKT-selected two-parameter family actually used by `V_reg` / `V_adm`.
- Added a sharper center-space derivation: in the current weighted basis only the `k = 0` coefficients contribute to the leading center block, the leading regular data is exactly two-parameter, but `C_reg = 0` alone still leaves a much larger coefficient space, so the present reduction cannot be declared continuum-lossless from center constraints alone.
- Recorded the new ansatz-level closure: `A_repo = im(V_adm)` is now identified exactly with the current constrained least-squares amplitude family inside the weighted trial construction, while equality to the full theorem-facing clean admissible tangent space remains explicitly open.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, broad scans, or hybrid `F_min` reuse policy were changed.

## 2026-03-27 - Derive the continuum/local leading family and isolate the higher-order completeness gap

- Affected files:
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`
- `docs/theory/current_theory_verification_map.md`
- `docs/assumptions/assumptions.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Added a dedicated continuum/local helper for the next theorem-facing step after C3b: it extracts the current principal center block from the live mixed equations, derives the two-parameter leading clean center-regular family symbolically, and records the exact leading relations for `u_n`, `psi`, and `M_s`.
- Recorded the stronger but still conservative closure boundary: the current repository now matches the continuum/local family at leading center order, not just at the weighted-trial ansatz level, but this still does not prove `A_full^th = A_ls`.
- Isolated the exact new gap explicitly in the theory docs: the frozen principal truncation does not yet close the full higher-order local formal family, so the next theorem-facing step is a regular-singular center recurrence/completeness derivation rather than a criterion rewrite.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, broad scans, or hybrid `F_min` reuse policy were changed.

## 2026-03-27 - Derive the finite-order frozen-principal recurrence pattern for clean `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ`

- Affected files:
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/assumptions/assumptions.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Replaced the earlier vague higher-order gap wording with an explicit finite-order frozen-principal recurrence result: the singular leading block stays two-parameter, the full frozen-principal leading layer is generically zero, the next checked layer leaves one membrane parameter, and the checked second layer is again uniquely zero.
- Updated pilot 23 and the theory-facing docs so this finite-order obstruction is recorded conservatively as a formula-level result for the fully frozen principal model only, without upgrading it to theorem-level continuum completeness.
- Clarified the next proof-oriented step: restore the first omitted finite center coefficients / forcing terms of the clean mixed equations and derive the richer regular-singular local recurrence there.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, broad scans, or hybrid `F_min` reuse policy were changed.

## 2026-03-27 - Check the richer first-finite center layer for clean `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ`

- Affected files:
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/assumptions/assumptions.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Added the C3c theory-facing check for the richer local center model with the first omitted honest finite background terms, and recorded the exact restored center-term orders used in that layer.
- Closed a sharper negative boundary than before: these first `O(x^2)` / `O(x^3)` center corrections do not change the same low-order obstruction layer in `R_Ts`, `R_Ms`, and `R_v`, so the checked richer local model still forces the `P0` branch to vanish generically on the active clean path.
- Updated the pilot note, derivation file, verification map, assumptions register, and project journal conservatively so this is tracked as a formula-level obstruction result for the first restored finite-center layer only, not as theorem-level closure of `A_full^th = A_ls`.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, broad scans, or hybrid `F_min` reuse policy were changed.

## 2026-03-28 - Identify the selected-object boundary for the clean full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` local comparison task

- Affected files:
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/assumptions/assumptions.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Added a dedicated pilot-23 helper that makes the live clean meaning of `A_ls` explicit as the unique KKT-selected `H = A_int^T A_int + reg I`-minimal section of the fixed-amplitude fiber `C_center c = [a1, a2, 0, 0]`, and checks representative clean points on the active standalone path.
- Recorded the new conservative theorem-facing clarification: direct comparison of `A_ls` with the full unrestricted local center-regular family is now likely too broad or mismatched, because the current selected family already carries a global weak/interior optimality layer.
- Updated the theory derivation file, verification map, assumptions register, project journal, and pilot note so the next proof obligation is now sharper: identify the correct selected local/germ comparison object or prove a global-to-local theorem for the globally weak-selected family, rather than blindly extending the same unrestricted local expansion.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, broad scans, or hybrid `F_min` reuse policy were changed.

## 2026-03-28 - Delimit the local selected object for the clean full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` C3e step

- Affected files:
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/assumptions/assumptions.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended the pilot-23 selection helper so the live clean family is now read through the full selected 4D center-data lift `P_sel`, its regularity-zero amplitude slice, and the explicit separation between the large fixed-center fiber and the unique global weak/KKT-selected representative.
- Recorded the sharper C3e theorem-facing result conservatively: the best exact current local comparison object is the local trace of the globally selected family `A_ls`, while a canonical intrinsic local weak-selected object inside the raw local center-regular family is still open.
- Updated the pilot note, derivation file, verification map, assumptions register, and project journal so the next proof obligation is now stated as a global-to-local trace theorem or an intrinsic selected-object theorem, not as blind completeness against the unrestricted local family.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, broad scans, or hybrid `F_min` reuse policy were changed.

## 2026-03-28 - Characterize the selected global-to-local trace object for the clean full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` C3f step

- Affected files:
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/assumptions/assumptions.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended the pilot-23 selection helper so the current selected family is now also checked through its finite leading-center trace layer: exact active center columns, the invertible center block, reconstruction from selected trace, and coordinate-change invariance of the selected trace plane.
- Recorded the sharper C3f theorem-facing result conservatively: the best current meaning of `J_0` is the finite leading-center jet `J_0 = C_center`, and on the current weighted-ansatz boundary the selected trace object is exactly the basis-independent 2D plane `J_0(A_ls) = im(D_amp)`.
- Updated the pilot note, derivation file, verification map, assumptions register, and project journal so the next proof obligation is now framed as comparing the continuum/local selected object against this selected leading-center trace plane, or recovering the same plane from an intrinsic local selected theorem.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, broad scans, or hybrid `F_min` reuse policy were changed.


## 2026-03-28 - Recover the selected leading-center trace plane on the continuum/local side for the clean full `simple support` C3g step

- Affected files:
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/assumptions/assumptions.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended the local symbolic helper so it now checks the current live clean `x0`-trace convention, confirms on representative clean backgrounds that `u_r(x0) = 0` implies `lambda_theta0(x0) = 1` at the selected trace layer, and derives the leading local selected trace in the same coordinates as `J_0 = C_center`.
- Recorded the C3g theorem-facing result conservatively: at the leading-center-jet level the continuum/local selected trace plane equals `im(D_amp)` when written in the current `J_0` coordinates, while a full intrinsic higher-order local selector remains open.
- Updated the pilot note, derivation file, verification map, assumptions register, and project journal so the next proof obligation is now a higher-order intrinsic selected-family theorem or an explicit trace-reconciliation theorem, not a return to the raw unrestricted local family.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, broad scans, or hybrid `F_min` reuse policy were changed.


## 2026-03-28 - Reconcile richer local trace charts with the canonical selected trace for the clean full `simple support` C3h step

- Affected files:
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/assumptions/assumptions.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended the local symbolic helper so it now treats the richer local trace as a normalization-dependent truncated jet with explicit parameter `eta`, derives the projection `Pi_eta_to_J0`, and checks that the selected richer object is a lifted 2D plane whose canonical `J_0` projection is exactly `im(D_amp)`.
- Recorded the C3h theorem-facing result conservatively: the invariant object for future higher-order work is not a chart-dependent zero-defect slice, but a lifted selected family in richer trace space projecting to the already closed selected plane `im(D_amp)`.
- Updated the pilot note, derivation file, verification map, assumptions register, and project journal so the next proof obligation is now a higher-order preservation theorem for this lifted richer object rather than another comparison against raw unrestricted local families.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, broad scans, or hybrid `F_min` reuse policy were changed.


## 2026-03-28 - Derive the first higher-order preservation statement for the clean full `simple support` C3i step

- Affected files:
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/assumptions/assumptions.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended the local symbolic helper so it now derives the first checked
  post-leading recurrence over the lifted selected trace, proves exact
  independence from the selected leading amplitudes `(U0, P0)`, solves the
  post-leading flexural block, and identifies the remaining one-parameter
  membrane nullmode.
- Recorded the C3i theorem-facing result conservatively: the raw lifted 2D plane
  `im(D_rich,eta)` is not exactly preserved at the first checked post-leading
  order; the smallest corrected higher-order selected object is a one-parameter
  membrane thickening whose canonical `J_0` projection still equals `im(D_amp)`.
- Updated the pilot note, derivation file, verification map, assumptions
  register, and project journal so the next proof obligation is now to select,
  normalize, or quotient out this membrane thickening direction rather than to
  force the richer post-leading family back into the old 2D chart.
- Kept the scientific meaning unchanged: no equations, boundary-condition
  meaning, solver behavior, broad scans, or hybrid `F_min` reuse policy were
  changed.


## 2026-03-28 - Identify the quotient treatment of the membrane thickening direction for the clean full `simple support` C3j step

- Affected files:
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/assumptions/assumptions.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended the local symbolic helper so it now computes the kernel of the
  canonical `J_0` projection on the corrected higher-order selected family,
  identifies the exact membrane generator in both the visible and coefficient-
  faithful augmented jets, and constructs the whole family of 2D sections that
  still project to `im(D_amp)`.
- Recorded the C3j theorem-facing result conservatively: no canonical local 2D
  normalization is currently justified, and the best current local selected
  object is the quotient of the corrected 3D higher-order family by the membrane
  thickening line.
- Updated the pilot note, derivation file, verification map, assumptions
  register, and project journal so the next proof obligation is now to derive an
  intrinsic higher-order rule selecting a representative of that quotient class,
  or to show that the quotient itself is the final local selected object.
- Kept the scientific meaning unchanged: no equations, boundary-condition
  meaning, solver behavior, broad scans, or hybrid `F_min` reuse policy were
  changed.


## 2026-03-28 - Strengthen the membrane-quotient theorem for the clean full `simple support` C3k step

- Affected files:
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/assumptions/assumptions.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended the symbolic local helper so it now tests candidate canonical
  selectors for the membrane-thickened corrected local family: next checked
  compatibility, checked local residual minimization, chart normalization, and
  metric orthogonality / minimal norm.
- Recorded the conservative C3k theorem-facing result: no intrinsic canonical
  higher-order representative is currently justified on the checked local
  boundary, and the strongest current local selected object remains the membrane
  quotient class.
- Updated the pilot note, derivation file, verification map, assumptions
  register, and project journal so the next proof obligation is now either to
  derive an intrinsic higher-order selector or to prove that the quotient itself
  is the final local selected object.
- Kept the scientific meaning unchanged: no equations, boundary-condition
  meaning, solver behavior, broad scans, or hybrid `F_min` reuse policy were
  changed.


## 2026-03-28 - Close the local A/B/C fork as Outcome B for the clean full `simple support` C3l step

- Affected files:
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/assumptions/assumptions.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Extended the symbolic helper with a boundary-scoped fork-decision report that
  checks exact factorization of the canonical `J_0` trace through the membrane
  quotient, records that the checked local residual vanishes identically on the
  corrected family, and confirms that the next checked local compatibility layer
  adds no representative-level invariant.
- Recorded the conservative C3l theorem-facing result: on the current checked
  local boundary the quotient object is the final local theorem-facing selected
  object, because no intrinsic selector is justified there and every currently
  checked local selected invariant factors through the quotient.
- Updated the pilot note, derivation file, verification map, assumptions
  register, and project journal so the next proof obligation is now either to
  lift this boundary-scoped quotient theorem to a stronger higher-order theorem,
  or to derive genuinely new local information beyond the current checked
  boundary.
- Kept the scientific meaning unchanged: no equations, boundary-condition
  meaning, solver behavior, broad scans, or hybrid `F_min` reuse policy were
  changed.

## 2026-03-28 - Sync criterion-facing docs after the clean full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` Outcome-B local stopping point

Affected files:
- `docs/theory/current_simple_support_status.md`
- `docs/project_map.md`
- `docs/theory/current_mixed_weak_theory_note.tex`
- `CHANGELOG.md`

- Audited the operational status page, project map, and supervisor-facing mixed-weak note against the post-C3k/C3l clean full `simple support / Р В РЎвЂ”Р В РЎвЂўР В РўвЂР В Р вЂ Р В РЎвЂР В Р’В¶Р В Р вЂ¦Р РЋРІР‚в„–Р В РІвЂћвЂ“ Р РЋРІвЂљВ¬Р В Р’В°Р РЋР вЂљР В Р вЂ¦Р В РЎвЂР РЋР вЂљ` theorem-facing state.
- Updated the status page so it now records the local Outcome-B stopping point, treats the higher-order local selected object as a quotient on the checked boundary, and redirects the next active move from deeper local continuation to criterion-level synthesis / interpretation.
- Updated the project map so it now marks pilot 23 as the active theorem-facing branch with a current stopping point at Outcome B and identifies the next active theory direction as criterion-level synthesis linking the local quotient result back to `A_ls`, `L_red`, `B_red`, and `B_mix`.
- Updated the compact supervisor note conservatively so it now reflects the active clean path, the theorem-facing role of `L_red` versus the boundary-only `B_red` / `B_mix` objects, the quotient-based local conclusion on the checked boundary, and the resulting caution that raw `sigma_min(B_mix)` remains exploratory rather than a closed final physical criterion.
- Kept the scientific meaning unchanged: no equations, boundary-condition meaning, solver behavior, broad scans, or hybrid `F_min` reuse policy were changed.

## 2026-03-28 - Record the quotient-aware return from local Outcome B to criterion interpretation

Affected files:
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Added a short project-level journal note freezing the checked local theorem branch at Outcome B for now as a strategy decision, not as a global impossibility claim.
- Recorded the quotient-aware criterion reading explicitly: `A_ls` stays the global weak/KKT-selected family, `L_red` stays the main theorem-facing reduced object, `B_red` / `B_mix` stay boundary-only companions, and the current `n=6` / `n=8` / `n=7` / `n=4` clean competition language remains operational rather than final physical criticality.

## 2026-03-28 - Add a repo-facing criterion bridge memo after Outcome B

Affected files:
- `docs/theory/current_simple_support_criterion_bridge_note.md`
- `docs/theory/current_simple_support_status.md`
- `docs/project_map.md`
- `CHANGELOG.md`

- Added a compact bridge memo under `docs/theory/` that stabilizes the post-Outcome-B interpretation language for `A_ls`, `L_red`, `B_red`, `B_mix`, and the current clean candidate labels.
- Added minimal cross-references from the simple-support status page and project map so the memo can be cited directly without reopening the checked local theorem branch.

## 2026-03-28 - Add the theorem roadmap above the frozen local Outcome-B boundary

Affected files:
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_simple_support_criterion_bridge_note.md`
- `docs/project_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Added a compact theorem-program note under `docs/theory/` that starts from the bridge note plus Outcome B and organizes the next theorem-facing agenda as `T1`--`T5`, with `T3` explicitly identified as the global selected-kernel bridge theorem for `L_red`.
- Added minimal cross-references from the bridge note, project map, and project journal so the roadmap can be cited without overloading the status page or reopening the same checked local branch.

## 2026-03-28 - Open the T3 implementation stage as a selected-kernel bridge program

Affected files:
- `docs/theory/current_simple_support_theorem_roadmap.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/journal/project_journal_updated14.md`
- `CHANGELOG.md`

- Refined the theorem roadmap so `T3` now has an exact repository-level target: on the current selected class `A_sel^repo = A_ls = im(V_adm) = im(M_amp)`, selected-class criticality should be read through the nontrivial-kernel question for `L_red = [A_int; B_full] V_adm`, not through a boundary descendant alone.
- Added an explicit `T3-L1`--`T3-L5` bridge-lemma decomposition, identified the main remaining gap as packaging those pieces into one selected-class bridge theorem, and recorded the Lean/CAS/manual split for the next proof implementation step.
- Added a new verification-map entry for the T3-stage theorem target and a short journal note marking the start of the T3 proof-organization stage above the frozen local Outcome-B boundary.
