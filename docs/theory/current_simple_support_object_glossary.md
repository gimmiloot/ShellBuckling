# Current Object Glossary For Clean Full `simple support / подвижный шарнир`

This file is the canonical glossary for stable object names repeatedly used in
the clean full `simple support / подвижный шарнир` theory/status documents.

It is a role/notation guide only. It does not reopen the frozen theorem line,
does not add new mathematical claims, and does not replace the derivation
source, verification map, or frozen-line archive.

## How To Read This File

For each object below, keep the following split in mind:

- short definition: the most compact current repository reading;
- current status: whether the object is closed, structural only, or still not
  fully theorem-facing on the current clean boundary;
- source-of-truth files: where the object is actually developed or frozen.

## `A_ls`

- Short definition:
  current selected reduced family on the live clean repository boundary.
  On that boundary,
  `A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q))`.
- Current status:
  closed enough on the current repository-selected boundary; do not read it as
  the whole full theorem-facing admissible space.
- Source-of-truth file(s):
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/theory/current_theory_verification_map.md`.

## `A_repo`

- Short definition:
  current repository-selected admissible family used on the weighted-ansatz
  clean boundary. In the current clean branch it is the same selected family as
  `A_ls`.
- Current status:
  closed enough on the repository boundary, but not the same thing as the full
  theorem-facing continuum admissible class.
- Source-of-truth file(s):
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/theory/current_theory_verification_map.md`.

## `A_full^th`

- Short definition:
  intended ambient theorem-facing full admissible / center-regular clean
  tangent class for the current mixed problem. In the current weak/KKT codomain
  discussion this is the ambient continuum class from which the selected-trace
  slice defining `A_con^th` should be taken.
- Current status:
  narrowed substantially but still not closed sharply enough. It should not be
  read as the same thing as the finite-dimensional ansatz spaces, the exact
  repo-selected family, or the selected trace plane alone. It is the ambient
  class on which the theorem-facing finite trace `J_0` still needs a full
  continuum/local upgrade.
- Source-of-truth file(s):
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_theory_verification_map.md`.

## `A_adm^th`

- Short definition:
  intended theorem-facing admissible clean tangent space for the linearized
  clean mixed problem. In the present criterion-facing codomain discussion this
  is the same intended ambient role that is being denoted by `A_full^th`, with
  `A_adm^th` retained when the emphasis is specifically on admissibility /
  residual-direction questions.
- Current status:
  still not closed enough on the current clean repository boundary to decide
  the frozen residual-direction question for `z_temp`, and still not packaged
  sharply enough to close the preferred weak/KKT codomain source.
- Source-of-truth file(s):
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/theory/current_simple_support_final_audit_note.md`;
  `docs/theory/current_theory_verification_map.md`.

## `A_con^th`

- Short definition:
  intended theorem-facing constrained codomain for the future weak/KKT
  selected-representative map
  `S_weak,n,q : R^2 -> A_con^th,n(q)`.
  The current preferred reading is the selected-trace constrained slice of the
  intended full admissible clean tangent class, rather than a codomain already
  built from a selected-overclass object.
- Current status:
  narrowed and route-preferred, but still not closed sharply enough to start a
  proof attempt. The selected-overclass / local-to-global route remains a live
  neighboring theorem program rather than the preferred current codomain.
- Source-of-truth file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`.

## `A_sel^{th,cand}`

- Short definition:
  strongest currently justified theorem-facing candidate class above the exact
  repository-selected family, defined by the selected leading trace and
  checked-local quotient shadows.
- Current status:
  structural theorem-facing candidate class only; not a proof that it equals
  `A_adm^th`.
- Source-of-truth file(s):
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`;
  `docs/theory/current_theory_verification_map.md`.

## `J_0`

- Short definition:
  selected leading trace map on the clean branch. On the current repository
  boundary, `J_0 = C_center`. In the current weak/KKT codomain discussion its
  intended theorem-facing role is the finite leading-center jet on
  `A_full^th`.
- Current status:
  closed enough on the selected-family boundary, including
  `J_0(A_ls) = im(D_amp)`, but not yet upgraded to a finished theorem-facing
  trace-regularity statement on all of `A_full^th`. The remaining gap is now
  best read as one precise local/trace extension task rather than a broad
  selector-level ambiguity, and that task is now sharp enough to state as a
  direct theorem target. A direct proof attempt does not yet close it, but it
  reduces the gap further to one explicit ambient finite-jet extraction lemma
  for the current `J_0` coordinates on `A_full^th`.
- Source-of-truth file(s):
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_theory_verification_map.md`.

## `C_center`

- Short definition:
  exact center map collecting the clean center amplitude and center regularity
  constraints.
- Current status:
  closed enough on the current weighted-ansatz clean boundary and used as the
  operational center/trace object.
- Source-of-truth file(s):
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`;
  `docs/theory/current_theory_verification_map.md`.

## `V_adm`

- Short definition:
  selected reduced lift matrix obtained from the regular span `V_reg` by
  amplitude normalization.
- Current status:
  closed enough on the current repository-selected boundary as the exact map
  generating `A_ls`.
- Source-of-truth file(s):
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`.

## `L_red`

- Short definition:
  main theorem-facing reduced operator on the current clean branch:
  `L_red,n(q) = [A_int,n(q); B_full,n(q)] V_adm,n(q)`.
- Current status:
  still the correct theorem-facing reduced object; boundary descendants remain
  exploratory diagnostics rather than proved replacements.
- Source-of-truth file(s):
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `proof_pilots/pilot_24_t3a_selected_kernel_bridge/pilot_24_t3a_selected_kernel_bridge.md`;
  `docs/theory/current_theory_verification_map.md`.

## `B_red`

- Short definition:
  boundary descendant of the clean reduced family:
  `B_red,n(q) = B_full,n(q) V_adm,n(q)`.
- Current status:
  useful reduced boundary object, but not a theorem-level substitute for
  `L_red`.
- Source-of-truth file(s):
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_simple_support_theorem_roadmap.md`.

## `B_mix`

- Short definition:
  boundary-only coordinate presentation on the selected reduced family:
  `B_mix,n(q) = B_red,n(q) G_amp,n(q)`.
- Current status:
  exploratory/diagnostic criterion object only; not a closed final criticality
  theorem.
- Source-of-truth file(s):
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_theory_verification_map.md`.

## `P_sel`

- Short definition:
  selected full-center lift map on the selected architecture, with
  `X_sel,n(q) = im(P_sel,n(q))`.
- Current status:
  closed enough on the selected-architecture obstruction layer, including
  `C_center,n(q) P_sel,n(q) = I_4`.
- Source-of-truth file(s):
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`;
  `docs/theory/current_theory_verification_map.md`.

## `Pair_chk`

- Short definition:
  structurally defined checked-local equal-trace pair domain used for
  representative-sensitive pair comparisons on the clean branch.
- Current status:
  structurally defined, but concrete one-point membership is not fully closed on
  the present repository boundary for the explicit candidate side of the frozen
  line.
- Source-of-truth file(s):
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/current_simple_support_status.md`.

## `c_sel`

- Short definition:
  fixed repo-selected basepoint in `A_ls,n(q)` used as the selected reference
  point on the current clean branch.
- Current status:
  stable operational/theorem-facing reference object on the selected-family
  side.
- Source-of-truth file(s):
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`;
  `docs/theory/current_simple_support_final_audit_note.md`.

## `z_temp`

- Short definition:
  explicit weighted-ansatz membrane residual direction isolated on the frozen
  clean branch.
- Current status:
  closed enough as a repository-boundary residual direction, but not proved
  theorem-facing admissible in `A_adm^th`.
- Source-of-truth file(s):
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`;
  `docs/theory/current_simple_support_final_audit_note.md`;
  `docs/theory/current_simple_support_closed_line_index.md`.

## `c_temp`

- Short definition:
  explicit affine-point candidate built from the selected basepoint and the
  residual direction:
  `c_temp := c_sel + z_temp,n(q;s_mem)`.
- Current status:
  central frozen candidate of the old line; not excluded by current
  theorem-facing authority, but not proved theorem-facing admissible either.
- Source-of-truth file(s):
  `docs/theory/current_simple_support_final_audit_note.md`;
  `docs/theory/current_simple_support_closed_line_index.md`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.

## `X_sel`

- Short definition:
  selected full-center lift architecture generated by `P_sel`:
  `X_sel,n(q) = im(P_sel,n(q))`.
- Current status:
  closed enough on the selected-architecture obstruction layer; the frozen line
  already excludes nonzero same-trace admissible membrane lifts inside this
  selected architecture.
- Source-of-truth file(s):
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`;
  `docs/theory/current_theory_verification_map.md`.

## Frozen-Line Endpoint Convention

- Final unresolved admissibility-side boundary:
  `z_temp,n(q;s_mem) in A_adm^th,n(q) intersect ker(C_center,n(q)) ?`
- Archive layer:
  `docs/theory/current_simple_support_final_audit_note.md`
  and
  `docs/theory/current_simple_support_closed_line_index.md`
- Live claim registry:
  `docs/theory/current_theory_verification_map.md`
