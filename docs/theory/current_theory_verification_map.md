# Current Theory Verification Map

## 1. Introduction

This map is for verification of the **current mixed-weak project theory** only.
It does **not** attempt to re-derive the whole shell theory from zero and does
not restart from Chernykh or other classical sources.

Its purpose is narrower:

- separate the accepted working basis of the current mixed-weak branch from the
  claims that still need checking;
- distinguish structural, formula-level, numerical, interpretation, and
  strategy-level items;
- record which kinds of checks belong to CAS, Lean, numerical testbench work,
  or manual derivation.

The goal is repository-level verification discipline, not a replacement for the
main theory document.

Stable object definitions repeatedly used in the clean full
`simple support / подвижный шарнир` branch are centralized in
`docs/theory/current_simple_support_object_glossary.md`.

## 2. Verification Boundary

This map starts from the point where the project has already accepted the
following as the working object of the current stage:

- the old reduced/full architecture is rejected as the main path after explicit
  negative tests;
- the current object of study is the mixed-weak branch;
- the current theory is read through
  `docs/theory/vyvod_uravneniy_updated17.md`,
  `docs/assumptions/assumptions.md`, and
  `docs/journal/project_journal_updated14.md`.

Outside scope for this map:

- full re-derivation of general shell theory from the literature;
- proving the whole corrected geometry from zero in one closed text;
- claiming final physical validation of the current candidate loads;
- treating project strategy as theorem-level mathematics.

## 2a. Verification-Method Policy

Use proof tooling by role:

- manual derivation:
  continuum/local analytical statements, near-center asymptotics, theorem
  framing, and analytical meaning;
- CAS:
  symbolic algebra, elimination, recurrence manipulations, principal-part
  reductions, boundary-pair algebra, and exact formula checks;
- Lean:
  abstract logical closure once the statement is sharp enough, including
  witness structure, uniqueness structure, implication chains, and proof
  skeleton checks;
- numerical testbench:
  diagnostics, robustness checks, and counterexample hunting only; not theorem
  closure.

Practical order:

- sharpen the statement manually first;
- then check symbolic transitions with CAS;
- then use Lean if the statement is stable enough for proof-skeleton closure;
- use numerics only as diagnostic support.

Method boundary:

- a claim should not be treated as stronger merely because it was tested
  numerically or manipulated successfully in CAS;
- Lean should be used to validate proof skeletons and hidden assumptions, not
  to replace theorem framing.

## 3. Accepted Working Base

The items below are treated as the **accepted working basis for the current
verification round**. This means they are the starting point of current checks,
not that every one of them is already article-level proven.

- The old reduced/full architecture is treated as an exhausted main path for
  this project stage.
- Corrected kinematics and the corrected circumferential bending block are
  treated as the retained base of the mixed-weak branch.
- The current mixed-weak unknown/resultant set
  `U = (u_s, u_n, v, varphi, psi)` and
  `P = (T_s, T_theta, S, Q_s, M_s, M_theta, H, chi)`
  is treated as the active operator class of the project.
- Verification begins from the mixed-weak weak-form / boundary-matrix
  formulation already recorded in the repository, not from an attempt to
  reconstruct all earlier theory.
- Current numerical candidate loads are accepted only as exploratory mixed-weak
  outputs unless stronger verification is added.

## 4. Structured Claim Map

### V-B1. Corrected base retained for the current branch

- ID: `V-B1`
- Claim / Hypothesis:
  Corrected kinematics and corrected circumferential bending are the accepted
  base blocks of the current mixed-weak branch.
- Type: `base`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` sections 1.2.2-1.2.3;
  `docs/assumptions/assumptions.md` A3.
- Current status: `accepted base`
- What counts as verification:
  No internal contradiction inside the current mixed-weak derivations and
  testbench branches; explicit note that these blocks are retained on purpose.
- Verification method:
  manual derivation, literature alignment, project-state consistency.
- Verification boundary:
  accepted as the starting basis of the current mixed-weak version only; not a
  full from-zero proof of shell theory.
- Next action:
  keep as base; do not silently upgrade to a fully closed derivation.

### V-S1. Mixed weak-form replaces scalar-potential closure

- ID: `V-S1`
- Claim / Hypothesis:
  The current branch must be formulated as a mixed weak-form with a bilinear
  prestress/load block `G_ps`, rather than by forcing everything into a single
  scalar potential closure.
- Type: `structural`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` sections 1.4-1.5;
  `docs/assumptions/assumptions.md` A5;
  `docs/journal/project_journal_updated14.md` sections 5.1 and 5.3.
- Current status: `clarified and still partial`
- What counts as verification:
  a compact repository-level closed statement
  `G_ps,n^repo(X, Xhat; q) ~ int [hat(T_s) g_s + hat(Q_s) g_n + hat(M_s) g_m] dx`
  with sign fixed by `A_n = K_n - G_ps,n + B_partial,n`, together with
  structural/CAS confirmation that `g_s`, `g_n`, and `g_m` match the live
  solver cores and that the block depends on the stress-like variable `T_s` and
  on independent mixed test slots, so it does not collapse to `G(U)` of the
  `U` slot alone.
- Verification method:
  manual derivation, project-state alignment, CAS structure check.
- Verification boundary:
  within the current mixed-weak repository theory and active solver/testbench
  reconstruction only; not a full article-level derivation of `G_ps` and not a
  proof that every possible scalar reformulation is impossible.
- Next action:
  derive the article-level full `G_ps` formula from this repository-level closed
  statement and freeze the final boundary between `G_ps` and the remaining
  background-dependent operator pieces.

### V-S2. Boundary conjugate pairs and natural BC logic

- ID: `V-S2`
- Claim / Hypothesis:
  The right-boundary conjugate pairs are
  `(T_s, u_s)`, `(Q_s, u_n)`, `(S, v)`, `(M_s, varphi)`, `(H, psi)`, and under
  the current testbench essential conditions `u_n(1)=0`, `varphi(1)=0` the
  natural conditions reduce to `T_s(1)=0`, `S(1)=0`, `H(1)=0`.
- Type: `structural`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.4;
  `docs/journal/project_journal_updated14.md` section 4;
  `proof_pilots/pilot_01_boundary_pairs/pilot_01_boundary_pairs.md`.
- Current status: `proven in pilot`
- What counts as verification:
  the reduced free-variation boundary form isolates exactly the coefficients
  `T_s`, `S`, and `H`.
- Verification method:
  CAS, Lean.
- Verification boundary:
  proven in proof pilot 01 only for the reduced boundary-pair step; not a proof
  of the whole weak-form derivation.
- Next action:
  keep this step as closed locally and reuse it in later pilots.

### V-S3. Independent circumferential channels `(v,S)` and `(psi,H,chi)`

- ID: `V-S3`
- Claim / Hypothesis:
  The current operator class contains structurally independent circumferential
  channels `(v,S)` and `(psi,H,chi)` and should not collapse back to the old
  closure logic.
- Type: `structural`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` sections 1.2.1 and 2.2.1;
  `docs/assumptions/assumptions.md` A4;
  `docs/journal/project_journal_updated14.md` sections 3.2, 4, and 10.3;
  `proof_pilots/pilot_02_independent_channels/pilot_02_independent_channels.md`.
- Current status: `proven in pilot`
- What counts as verification:
  explicit witness states where the `S`-channel is active while `H = chi = 0`,
  and psi-side witness states where `S = 0` while `H` or `chi` is active.
- Verification method:
  CAS, Lean.
- Verification boundary:
  proven in proof pilot 02 only as structural independence within the current
  formulas and abstract witness logic; not a full derivation of the operator
  class from general shell theory.
- Next action:
  preserve this as a closed local check and use it when reviewing future
  formula changes.

### V-F1. Current formulas for `S`, `H`, and `chi` respect the channel split

- ID: `V-F1`
- Claim / Hypothesis:
  The active mixed-weak reconstruction formulas for `S`, `H`, and `chi` are
  compatible with the intended channel separation of the current branch.
- Type: `formula`
- Source file(s):
  `src/shell_buckling/mixed_weak/solver_simple_support_core.py`;
  `src/shell_buckling/mixed_weak/solver_patched_core.py`;
  `proof_pilots/pilot_02_independent_channels/cas_check.py`.
- Current status: `proven in pilot`
- What counts as verification:
  exact source-formula match plus symbolic checks showing:
  `S` has zero dependence on twist/shear variables,
  `H` has zero dependence on `v`-channel variables, and
  `chi` does not require the `v`-channel to be active in the witness tests.
- Verification method:
  CAS.
- Verification boundary:
  within the current active formulas only; not a proof that these formulas are
  uniquely correct in the full theory.
- Next action:
  add similar formula guards if more mixed-weak channels become verification
  critical.

### V-S4. Two-dimensional central regular family

- ID: `V-S4`
- Claim / Hypothesis:
  The current mixed-weak class has a two-dimensional physical regular family at
  the center.
- Type: `structural`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` sections 1.6 and 2.2.1;
  `docs/assumptions/assumptions.md` A6;
  `docs/journal/project_journal_updated14.md` sections 3.4 and 4;
  `proof_pilots/pilot_03_central_regular_family/pilot_03_central_regular_family.md`.
- Current status: `partially confirmed, tightened by pilot 03`
- What counts as verification:
  principal-part scaling, reduced center nullity `2` in the current ansatz,
  successful construction of two center-regular modes in the current testbench
  logic, and a typechecked abstract implication from two-mode parameterization
  to two-dimensionality.
- Verification method:
  manual derivation, dedicated CAS reduction, numerical testbench, Lean
  abstraction.
- Verification boundary:
  within the current mixed-weak principal-part analysis, reduced center ansatz,
  and surrogate/testbench mode construction; Lean closes only the abstract
  mode-count step and does not prove the full shell-center derivation or
  uniqueness of every regular mixed extension.
- Next action:
  keep V-S4 at this tightened pilot-backed status, but do not upgrade it beyond
  the current ansatz/testbench boundary without a fuller center derivation.

### V-S5. `B_mix` must be built from two central regular modes

- ID: `V-S5`
- Claim / Hypothesis:
  The current boundary matrix must be assembled from two central regular modes,
  not from a global surrogate interior nullspace.
- Type: `structural`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` sections 2.2.1 and 2.2.2;
  `docs/journal/project_journal_updated14.md` sections 6.2-6.3 and 9;
  `proof_pilots/pilot_04_bmix_from_regular_modes/pilot_04_bmix_from_regular_modes.md`.
- Current status: `partially confirmed, tightened by pilot 04`
- What counts as verification:
  the live `v2` workflow must explicitly form `B_mix = B_full @ V_reg` from the
  two center-regular modes, and a raw surrogate-direction comparison must show
  that the unconstrained smallest-right-singular-vector pair violates the
  active center constraints and changes the construction in the current
  repository sense.
- Verification method:
  numerical testbench, Lean abstraction.
- Verification boundary:
  only at the surrogate/testbench builder level so far; Lean closes only the
  abstract admissibility logic and does not prove the final shell BVP or a
  final closed solver implementation.
- Next action:
  keep V-S5 at this tightened pilot-backed status and re-check it whenever the
  boundary-matrix builder changes.

### V-S6. The clean `simple support` theorem-level target object is the full reduced tangent operator

- ID: `V-S6`
- Claim / Hypothesis:
  On the active clean standalone `simple support` path, the theorem-level
  criticality object should be the full linearized mixed operator with interior
  residual block plus boundary rows
  `[u_n(1), varphi(1), T_s(1), S(1), H(1)]`, reduced to the admissible
  center-regular space, rather than the boundary-only object alone.
- Type: `structural`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.7;
  `docs/assumptions/assumptions.md` A16;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`.
- Current status: `frozen as the current target object, not yet proved`
- What counts as verification:
  an explicit repository-level derivation of the full stacked operator,
  an explicit split of the center rows into free amplitudes and true regularity
  constraints, and a reduced operator definition that is basis-clean on the
  same two-dimensional admissible family.
- Verification method:
  manual derivation, CAS, numerical representative check, Lean abstraction
  target.
- Verification boundary:
  repository-level target freeze only; not yet a proof of the final shell BVP,
  not yet a proof of exact kernel equivalence, and not yet a proof that the
  boundary-only object is sufficient.
- Next action:
  prove the kernel-equivalence step from the admissible full operator to the
  reduced operator, and only then decide whether a further collapse to a
  boundary-only criterion is justified.

### V-F2. Current reduced tangent operator candidate from the live clean objects

- ID: `V-F2`
- Claim / Hypothesis:
  With the live clean objects
  `L_full = [A_int; B_full]`, `C_center = [C_amp; C_reg]`,
  `G_amp = C_amp V_reg`, and `V_adm = V_reg G_amp^(-1)`, the preferred reduced
  operator candidate is
  `L_red = [A_int; B_full] V_adm`, while
  `B_red = B_full V_adm` and the current raw baseline satisfies
  `B_mix = B_red G_amp`.
- Type: `formula`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.7;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/reduction_check.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`.
- Current status: `formula-level target derived and partially checked`
- What counts as verification:
  CAS confirmation of the block identities used in the stacked reduction,
  live representative checks that `C_reg V_reg ≈ 0`,
  `det(C_amp V_reg) != 0`, `C_center V_adm ≈ [[I_2],[0]]`,
  and `B_mix ≈ B_red G_amp`.
- Verification method:
  manual derivation, CAS, numerical representative check.
- Verification boundary:
  current finite-dimensional clean architecture only; this does not yet prove
  the exact continuum reduction, exact vanishing of `A_int V_adm`, or final
  equivalence of kernels.
- Next action:
  isolate the exact C3 kernel-equivalence statement and decide in C4 whether a
  genuine quadratic-form object exists beyond the current reduced stacked
  operator and its Gram surrogate.

### V-S7. On the current reduced family, `ker(L_red)` is exactly the restricted admissible kernel of the full clean operator

- ID: `V-S7`
- Claim / Hypothesis:
  Let `A_repo = im(V_adm)` be the current chosen two-dimensional reduced family
  in the clean standalone `simple support` architecture. Then the map
  `a -> c = V_adm a` identifies `ker(L_red)` exactly with
  `A_repo ∩ ker(L_full)`, where `L_full = [A_int; B_full]` and
  `L_red = L_full V_adm`.
- Type: `structural`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.8;
  `docs/assumptions/assumptions.md` A16;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/reduction_check.py`.
- Current status: `closed at the finite-dimensional restricted-family level`
- What counts as verification:
  an explicit proof that `C_amp V_adm = I_2` and `C_reg V_adm = 0` make
  `a -> V_adm a` a bijection from `R^2` onto `A_repo`, together with the exact
  identity `L_red = L_full V_adm`.
- Verification method:
  manual derivation, CAS, numerical representative check, Lean abstraction
  target.
- Verification boundary:
  this does not yet prove that `A_repo` equals the full exact clean admissible
  center-regular tangent space; it closes only the current repository-level
  reduction on the chosen two-dimensional family.
- Next action:
  formalize the abstract finite-dimensional bijection in Lean, then decide
  whether the restriction to `A_repo` is lossless for the full clean problem.

### V-F3. The reduced clean kernel question is basis-independent, and `B_red` / `B_mix` differ only by reduced coordinates

- ID: `V-F3`
- Claim / Hypothesis:
  For any invertible reduced coordinate change `T`, replacing `V_adm` by
  `V_adm T` leaves `im(V_adm)` unchanged and gives
  `L_full(V_adm T) = L_red T`, `B_full(V_adm T) = B_red T`. Also, with
  `G_amp = C_amp V_reg`, one has `V_reg = V_adm G_amp` and
  `B_mix = B_red G_amp`, so `ker(B_mix) = G_amp^(-1)(ker(B_red))` whenever
  `det(G_amp) != 0`.
- Type: `formula`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.8;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/reduction_check.py`.
- Current status: `formula-level closed on the current reduced family`
- What counts as verification:
  CAS confirmation of the right-multiplication identities and live checks that
  `det(G_amp) != 0`, `V_reg ≈ V_adm G_amp`,
  `L_full V_reg ≈ L_red G_amp`, and `B_mix ≈ B_red G_amp`.
- Verification method:
  manual derivation, CAS, numerical representative check.
- Verification boundary:
  this is a coordinate-equivalence statement only; it does not prove
  `ker(L_red) <-> ker(B_red)` and does not justify replacing the interior block
  by boundary rows alone.
- Next action:
  keep this as the basis-clean coordinate layer and isolate separately the
  additional theorem that would be needed for a boundary-only collapse.

### V-S8. The current `A_repo = im(V_adm)` is exactly the KKT-selected two-parameter family of the weighted trial ansatz

- ID: `V-S8`
- Claim / Hypothesis:
  Inside the current weighted polynomial trial ansatz, the current repository
  family `A_repo = im(V_adm)` is exactly the image of the amplitude-to-
  coefficient map produced by the constrained regularized least-squares KKT
  problem with free center amplitudes and zero regularity rows. In that sense,
  the current reduction is lossless relative to the present selected ansatz-
  level family.
- Type: `structural`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.9;
  `docs/assumptions/assumptions.md` A17;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/reduction_check.py`;
  `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`;
  `src/shell_buckling/mixed_weak/solver_patched_core.py`.
- Current status: `closed at the current weighted-ansatz / selected-family level`
- What counts as verification:
  an explicit derivation of the leading center block from the weighted basis,
  an explicit definition of the KKT-selected amplitude family, and a check that
  the canonical `V_adm` span coincides with that family on representative live
  clean objects.
- Verification method:
  manual derivation, CAS, numerical representative check.
- Verification boundary:
  this does not prove that the selected family already equals the full theorem-
  facing clean admissible tangent space of the continuous problem; it closes
  only the exact current ansatz-level family used by the repository.
- Next action:
  isolate the separate continuum/completeness theorem that would be needed to
  upgrade this ansatz-level equality to theorem-level losslessness.

### V-F4. `C_reg = 0` alone leaves a much larger trial coefficient space than `A_repo`

- ID: `V-F4`
- Claim / Hypothesis:
  In the current `48`-unknown weighted trial basis (`m_basis = 6`), the
  center-regular constraint block has rank `2`, so `ker(C_reg)` is
  `46`-dimensional, while `ker(C_center)` is `44`-dimensional. Therefore the
  current reduced family `A_repo` cannot be identified with the whole
  coefficient-level center-regular trial space from the existing center
  constraints alone.
- Type: `formula`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.9;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/reduction_check.py`;
  `src/shell_buckling/mixed_weak/solver_patched_core.py`.
- Current status: `formula-level closed on the active trial basis`
- What counts as verification:
  exact derivation of the four-by-four leading center block from the weighted
  basis together with live rank/dimension checks on the active representative
  clean points.
- Verification method:
  manual derivation, CAS, numerical representative check.
- Verification boundary:
  this is a statement about the current weighted trial basis only; it does not
  by itself determine the dimension of the full continuum admissible clean
  tangent space.
- Next action:
  keep this as the explicit reason why continuum losslessness still requires an
  additional theorem beyond the current center constraints and selected-family
  construction.

### V-S9. The singular leading center block is two-parameter in the current principal center model

- ID: `V-S9`
- Claim / Hypothesis:
  In the current principal center model extracted from the live mixed
  equations, the singular leading center block is parameterized by the same
  amplitudes used by the current repository reduction, namely
  `(u_s/x^n, varphi/x^(n-1))`, and determines the accompanying leading
  relations for `u_n`, `psi`, `M_s`, and one `T_s` relation.
- Type: `structural`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.10;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `src/shell_buckling/mixed_weak/solver_patched_core.py`.
- Current status: `closed at the singular leading-block level`
- What counts as verification:
  symbolic extraction of the leading singular block from the current mixed
  equations and explicit solution of the leading center relations for
  `u_n`, `psi`, and `M_s` in terms of the two free amplitudes.
- Verification method:
  manual derivation, CAS.
- Verification boundary:
  this is not yet a full local formal family of the fully frozen principal
  model; it is only the singular leading-block compatibility statement.
- Next action:
  compare that singular leading block with the full frozen-principal layer
  equations instead of promoting it directly to continuum completeness.

### V-F5. The full frozen principal leading layer is generically zero under nonresonance

- ID: `V-F5`
- Claim / Hypothesis:
  Once the full frozen principal leading layer is assembled from
  `R_us`, `R_un`, `R_Ts`, `R_gtheta`, `R_phi`, `R_Ms`, and `R_v`, its exact
  determinant is generically nonzero, so the leading coefficient layer
  `U0, N0, V0, P0, Y0, T0, M0` is forced to zero under nonresonance.
- Type: `formula`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.10;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`.
- Current status: `closed for the fully frozen principal leading layer`
- What counts as verification:
  a CAS derivation of the exact membrane and flexural leading determinants and
  of the combined leading determinant in the frozen principal model.
- Verification method:
  CAS, manual derivation.
- Verification boundary:
  this is a formula-level statement only for the fully frozen principal model;
  it does not disprove the existence of a richer continuum local family once the
  omitted finite center coefficients are restored.
- Next action:
  inspect the next and subsequent frozen-principal layers instead of reading the
  singular leading-block amplitudes as a completed local family.

### V-F6. After the zero leading layer, the frozen principal recurrence shows a one-parameter next membrane mode and a zero checked second layer

- ID: `V-F6`
- Claim / Hypothesis:
  After the leading frozen-principal layer is zero, the next coefficient layer
  has full rank `7` and nullity `1`: it leaves one membrane parameter `T1`
  free, forces `N1 = P1 = Y1 = M1 = Q0 = 0`, and determines `U1` and `V1`
  from `T1`; after substituting that mode, the checked second layer is again
  uniquely zero under nonresonance.
- Type: `formula`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.10;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status: `closed through the checked finite orders of the fully frozen principal model`
- What counts as verification:
  a CAS derivation of the next-layer rank/nullspace, the explicit membrane
  nullvector and flexural determinant, and the invertible checked second-layer
  system after substituting the generic next membrane mode.
- Verification method:
  CAS, manual derivation, representative live clean evaluation of the derived
  determinant factors.
- Verification boundary:
  this is still a finite-order result for the fully frozen principal model; it
  does not yet identify the full theorem-facing clean local family.
- Next action:
  restore the first omitted finite center coefficients / forcing terms of the
  clean mixed equations and derive the richer regular-singular recurrence there.


### V-F7. The first restored finite center coefficients do not change the low-order obstruction layer

- ID: `V-F7`
- Claim / Hypothesis:
  After restoring the first honest finite center coefficients of the clean
  background, the richer local model still leaves the same low-order
  `P0`-obstruction in `R_Ts`, `R_Ms`, and `R_v`: the restored corrections start
  only at `O(x^2)` / `O(x^3)`, while the decisive obstruction sits at
  `x^(n-3)`, so the checked low-order formulas remain the same as in the
  constant-finite model.
- Type: `formula`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.10.7;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status: `closed for the first restored finite-center layer`
- What counts as verification:
  explicit order counting showing that the restored terms cannot enter the same
  obstruction layer, symbolic formulas for the unchanged low-order rows after
  substituting the singular relations, and representative live clean evaluation
  that `K = kappa_s0(x0)` and the derived obstruction factors stay far from
  zero on the active competition set.
- Verification method:
  manual derivation, CAS, representative live clean evaluation.
- Verification boundary:
  this is still not a theorem-level description of the final local clean family;
  it only shows that the first `O(x^2)` / `O(x^3)` background corrections are
  insufficient to restore the expected two-amplitude continuation.
- Next action:
  identify a local ingredient that can act at the same lowest obstruction
  orders, or reconsider the exact theorem-facing local comparison object before
  trying to prove `A_full^th = A_ls`.

### V-S10. `A_ls` is a KKT-selected `H`-minimal section of a much larger amplitude fiber, not merely a chart for center regularity

- ID: `V-S10`
- Claim / Hypothesis:
  For the live clean construction, fixing amplitudes
  `a = (u_s/x^n, varphi/x^(n-1))` defines the affine weighted-trial fiber
  `F(a) = {c : C_center c = [a1, a2, 0, 0]}`. The current family
  `A_ls = im(M_amp) = im(V_adm)` is the image of the unique minimizer of
  `||A_int c||^2 + reg ||c||^2` on that fiber. Equivalently, with
  `H = A_int^T A_int + reg I`, the selected map satisfies
  `H M_amp + C_center^T Lambda = 0` and is `H`-orthogonal to
  `ker(C_center)`. So `A_ls` already carries a global weak/interior selection
  layer and is not merely the full unrestricted local center-regular family.
- Type: `structural`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.10.8;
  `docs/assumptions/assumptions.md` A18;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`;
  `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`.
- Current status: `closed at the current weighted-ansatz / global-KKT level`
- What counts as verification:
  explicit code inspection of the KKT solve defining `M_amp`, representative
  checks that the current amplitude fiber still has large dimension while the
  selected family is 2D, representative checks of KKT stationarity / fiber
  orthogonality, and a check that near-center-only surrogate objectives do not
  reproduce the same selected map.
- Verification method:
  structural code inspection, linear algebra check, representative live clean
  evaluation.
- Verification boundary:
  this still does not provide a purely local theorem-facing selected object for
  the continuous clean problem. It only closes the meaning of `A_ls` inside the
  current live clean architecture and shows why comparing it directly to the
  raw unrestricted local center-regular family is likely mismatched.
- Next action:
  identify the correct selected local/germ comparison object for `A_ls`, or
  prove a global-to-local theorem showing that the center traces of the
  globally weak-selected family are the right theorem-facing comparison partner.

### V-S11. The best current theorem-facing local selected object is the local trace of the global KKT-selected family, while an intrinsic local selector remains open

- ID: `V-S11`
- Claim / Hypothesis:
  After the object-selection step and C3e, the best exact faithful local
  comparison object currently visible in the repository is not the raw local
  center-regular family `A_reg^loc`, but the extrinsic trace object
  `A_sel,trace^loc = J_0(A_ls)`, where `A_ls` is the global KKT-selected family
  already used by the clean code. What remains open is an intrinsic local
  characterization of that same object inside `A_reg^loc`, for example via a
  canonical local weak/KKT-type selection rule.
- Type: `structural`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.10.9;
  `docs/assumptions/assumptions.md` A19;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`.
- Current status: `partially delimited; exact extrinsic candidate identified, intrinsic local selector still open`
- What counts as verification:
  an explicit theorem-facing decomposition of the live clean family into the
  selected 4D center-data lift plus its regularity-zero amplitude slice,
  explicit distinction between what the center constraints fix and what the
  global minimization fixes, and representative checks that naive near-center
  surrogate objectives do not reproduce the same selected family.
- Verification method:
  structural code inspection, linear algebra check, representative live clean
  evaluation, prior CAS/local obstruction check.
- Verification boundary:
  this does not yet prove that `J_0(A_ls)` has a canonical intrinsic local weak
  description, and it does not prove `A_full^th = A_ls`. It only sharpens the
  theorem-facing object: compare against a selected local trace, not against the
  unrestricted local center-regular family by default.
- Next action:
  prove a global-to-local trace theorem for `A_ls`, or derive an intrinsic local
  selected-object theorem that identifies the same trace inside `A_reg^loc`.

### V-S12. The best current theorem-facing trace map is the finite leading-center jet `J_0 = C_center`, and on `A_ls` its image is the basis-independent 2D selected trace plane `im(D_amp)`

- ID: `V-S12`
- Claim / Hypothesis:
  On the current clean weighted-trial boundary, the best theorem-facing meaning
  of `J_0` is the finite leading-center jet map `J_0(c) = C_center c`, not a
  full higher-order local germ extractor. This map is exact at the current
  ansatz level because evaluation at `x0` kills all `k > 0` trial columns and
  leaves an invertible 4x4 center block on the `k = 0` columns of
  `(u_s, u_n, varphi, psi)`. For the selected family
  `A_ls = im(P_sel D_amp)`, one then has exactly
  `J_0(A_ls) = im(D_amp)`, and the restriction `J_0|_{A_ls}` is a basis-
  independent bijection onto that 2D plane with inverse given by the selected
  lift `P_sel` on `im(D_amp)`.
- Type: `structural`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.10.10;
  `docs/assumptions/assumptions.md` A20;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/reduction_check.py`;
  `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`;
  `src/shell_buckling/mixed_weak/solver_patched_core.py`.
- Current status: `closed at the current weighted-ansatz / leading-center-jet level`
- What counts as verification:
  explicit code inspection showing what `C_center` extracts, exact confirmation
  that only the four `k = 0` center columns survive and form an invertible
  center block, explicit KKT/lift identities for `P_sel`, representative checks
  that `C_center P_sel ≈ I_4`, `C_center M_amp ≈ D_amp`, reconstruction from
  selected trace works, and basis changes inside `A_ls` preserve the same trace
  plane.
- Verification method:
  structural code inspection, linear algebra check, representative live clean
  evaluation, symbolic center-block check.
- Verification boundary:
  this does not identify a higher-order intrinsic local selector and does not
  prove a full continuum local germ theorem. It closes only the exact finite
  leading-center trace layer currently available in the repository.
- Next action:
  compare the continuous/local selected object against this selected leading-
  center trace plane, or derive an intrinsic local theorem that recovers the
  same trace plane from the full local selected family.
### V-N1. `sigma_min(B_mix(q)) = 0` is the current raw working criterion

- ID: `V-N1`
- Claim / Hypothesis:
  `sigma_min(B_mix(q)) = 0` is the correct **raw working** spectral criterion
  and baseline comparison reading for the present mixed-weak branch on the
  active clean `simple support` path.
- Type: `numerical`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` sections 2.2.2 and 2.3;
  `docs/assumptions/assumptions.md` A7;
  `docs/theory/current_simple_support_status.md`;
  `docs/journal/project_journal_updated14.md` sections 12.3-12.4.
- Current status: `partially confirmed as a raw baseline, but non-decisive`
- What counts as verification:
  live computability of `sigma_min(B_mix)` on the active clean q-ranges,
  reproducible refined minima under the current local-window workflow, moderate
  nearby discretization robustness in the present testbench, and explicit use
  of this reading as the reference baseline when comparing lighter diagnostic
  pilots.
- Verification method:
  numerical testbench, project-state comparison.
- Verification boundary:
  working baseline inside the current mixed-weak exploratory/testbench branch
  only; it is not yet the theorem-level criterion of the final mixed BVP and it
  does not by itself settle the final physical `simple support` critical load.
- Next action:
  keep this criterion as the raw reference reading, but derive a stronger
  theorem-level criticality object before promoting stronger mode-selection or
  `q_cr` claims.

### V-N2. Current operational clean `simple support` competition reading

- ID: `V-N2`
- Claim / Hypothesis:
  On the active clean standalone `simple support` path, the current operational
  reading is: `n = 6`, `q ~ 17.6 MPa` as the best supported candidate,
  `n = 8` as the main rival, `n = 7` as a persistent reserve/raw competitor,
  and `n = 4` as the control mode.
- Type: `numerical`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/journal/project_journal_updated14.md` sections 12.3-12.4;
  `tasks/run_full_simple_support_critical_search.py`.
- Current status: `exploratory operational reading`
- What counts as verification:
  reproducible local-window comparisons on the clean path, limited nearby
  discretization checks, and explicit separation between supported candidate,
  methodological rival, reserve/raw competitor, and control mode.
- Verification method:
  numerical testbench, project-state comparison.
- Verification boundary:
  operational reading inside the current clean search only; not a validated
  final physical critical load and not a theorem-level proof of mode selection.
- Next action:
  keep this clean competition set as the live benchmark for criterion rework,
  while leaving the older hybrid candidate memories archived for historical
  comparison only.

### V-I1. Mixed-weak branch gives a qualitatively new picture

- ID: `V-I1`
- Claim / Hypothesis:
  The mixed-weak branch has produced a qualitatively new numerical picture
  relative to the rejected reduced/full architecture.
- Type: `interpretation`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` sections 2.3 and 3.1;
  `docs/journal/project_journal_updated14.md` sections 1, 9, and 10.3;
  `docs/assumptions/assumptions.md` A1, A2, A7, A8.
- Current status: `partially confirmed`
- What counts as verification:
  explicit comparison with old negative branches and stable evidence that the
  new criterion is not collapsing back to the old behavior.
- Verification method:
  numerical testbench, project-state comparison.
- Verification boundary:
  interpretation of current project evidence, not a theorem about all possible
  future variants.
- Next action:
  retain the comparison baseline so the qualitative shift remains reproducible.

### V-I2. Current operational candidates are limited mainly by criterion closure

- ID: `V-I2`
- Claim / Hypothesis:
  Even on the active clean standalone `simple support` path, the current
  operational candidates cannot be treated as final because the theorem-level
  criticality object linking the admissible mixed problem to mode selection is
  still not closed.
- Type: `interpretation`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/journal/project_journal_updated14.md` sections 12.3-12.4.
- Current status: `partially confirmed`
- What counts as verification:
  explicit evidence that the raw `sigma_min(B_mix)` reading and the lighter
  `A + C`, `D`, and `E` pilots improve diagnostics only partially and do not
  robustly settle the `n = 6` versus `n = 8` competition.
- Verification method:
  project-state analysis, numerical testbench.
- Verification boundary:
  interpretation of the current clean-path evidence only; not yet a theorem
  about the final mixed BVP.
- Next action:
  keep this limitation explicit in every summary of the present candidate loads
  and treat criterion rework as the next theory task.

### V-ST1. Main open problem on the clean standalone `simple support` path is theorem-level criterion closure

- ID: `V-ST1`
- Claim / Hypothesis:
  On the active clean standalone `simple support` path, the main remaining
  bottleneck is no longer basic background reach but the absence of a
  theorem-level criticality object that links the full linearized mixed BVP to
  stable mode selection on the admissible center-regular space.
- Type: `strategy`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/journal/project_journal_updated14.md` sections 12.3-12.5;
  `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`;
  `tasks/run_simple_support_criterion_pilot_d.py`;
  `tasks/run_simple_support_criterion_pilot_e.py`.
- Current status: `strategy only`
- Operational pointer:
  The live operational snapshot for this clean path is maintained in
  `docs/theory/current_simple_support_status.md`.
- What counts as verification:
  not a theorem; it is supported only insofar as the honest clean background
  path now already reaches the active competition region, while the completed
  `A + C`, `D`, and `E` pilots remain diagnostically useful but non-decisive
  for mode selection on the local competition set `n = 4, 6, 7, 8`.
- Verification method:
  project-state analysis, numerical testbench.
- Verification boundary:
  not a theorem, only a current research strategy.
- Next action:
  move from cheap pilot iteration to a theorem-level criterion rework on the
  clean architecture before promoting stronger `q_cr` claims or launching a new
  broad scan.

### V-ST2. Next correct project step is criterion-theory rework before stronger `q_cr` claims

- ID: `V-ST2`
- Claim / Hypothesis:
  The correct current project strategy is to derive and verify a stronger
  criterion object before returning to stronger claims about `q_cr` on the full
  `simple support` problem.
- Type: `strategy`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/journal/project_journal_updated14.md` sections 12.4-12.5.
- Current status: `strategy only`
- What counts as verification:
  none in theorem form; this is an organizational consequence of the present
  dependency structure and of the completed non-decisive pilot sequence.
- Verification method:
  project-state analysis.
- Verification boundary:
  not a theorem, only a strategy-level rule for the next project step.
- Next action:
  keep this separate from structural or formula-level claims and schedule the
  rework through explicit manual/CAS/Lean checkpoints rather than as unchecked
  prose.

## 5. Existing Proof Pilots Already Integrated

- Proof pilot 01 supports `V-S2`:
  it verifies the reduced right-boundary free-variation step and the extraction
  of the natural conditions `T_s(1)=0`, `S(1)=0`, `H(1)=0`.
- Proof pilot 02 supports `V-S3` and `V-F1`:
  it verifies structural separation of `(v,S)` and `(psi,H,chi)` in the current
  formulas and proves the abstract witness-based non-collapse logic in Lean.
- Proof pilot 03 supports `V-S4`:
  it combines CAS, numerical, and Lean checks for the current reduced center
  ansatz and the `v2` center-mode workflow, tightening the current
  two-dimensional-center-family claim within the repository boundary.
- Proof pilot 04 supports `V-S5`:
  it checks that the live `B_mix` builders use the constrained center-regular
  pair rather than raw surrogate kernel directions and adds the matching
  abstract admissibility logic in Lean.
- Proof pilot 05 supports `V-N1`:
  it checks that `sigma_min(B_mix)` is computable in the live mixed-weak scan
  workflow, stays usable across the current broad/fine/adaptive/targeted and
  resolution-study paths, and remains only a tightened working criterion inside
  the repository boundary.
- Proof pilot 06 supports `V-S1`:
  it isolates the current repository-level `G_ps` statement and CAS-checks that
  the active solver-level forcing block is mixed-slot bilinear rather than a
  closure `G(U)` of the `U` slot alone, while keeping the claim explicitly
  partial.
- Proof pilot 06b supports `V-S1`:
  it consolidates the current repository-level closed statement
  `G_ps^repo ~ int [hat(T_s) g_s + hat(Q_s) g_n + hat(M_s) g_m] dx` and
  formula-checks it against both active solver cores without upgrading the claim
  beyond the current repository boundary.
- Proof pilot 23 supports `V-S6` and `V-F2`:
  it freezes the clean full reduced tangent target object from the live clean
  architecture, CAS-checks the stacked reduction identities, and numerically
  checks the current admissible rebasing
  `V_adm = V_reg (C_amp V_reg)^(-1)` on representative clean competition
  points.

These pilots close only local steps. They do **not** prove the whole mixed-weak
theory.

## 6. Hypotheses Handling in This Repository

The repository uses several different kinds of hypotheses, and they should not
be mixed together.

### 6.1. Accepted working base

These are accepted as the starting basis of the current verification round even
if they are not yet fully article-level proven:

- corrected base blocks of the mixed-weak branch;
- the mixed-weak operator class itself;
- rejection of the old reduced/full architecture as the main path;
- the rule that current candidate loads remain exploratory unless stronger
  verification is added.

### 6.2. Testable structural and formula claims

These are claims that can in principle be tightened by local proof work:

- boundary conjugate-pair and natural-BC logic;
- independence of circumferential channels;
- formula-level channel reconstruction checks;
- dimensionality and mode-construction logic near the center.

These are the best candidates for CAS and Lean pilots.

### 6.3. Numerical hypotheses and claims

These require numerical testbench evidence rather than symbolic proof:

- whether `B_mix` built from the current pipeline remains nondegenerate;
- whether `sigma_min(B_mix(q))` behaves as the intended working criterion;
- where the current exploratory minima sit in pressure/mode space.

These should stay labeled as exploratory, partially confirmed, or testbench-only
unless the numerical boundary conditions and background are fully consistent.

### 6.4. Interpretation and strategy items

These are not theorems and should never be reported as if they were:

- that the mixed-weak branch already provides the right physical explanation;
- that the main remaining bottleneck is specifically the simple-support
  background;
- that the project should delay final `q_cr` claims until that background is
  stabilized.

They may still be sensible and well-supported, but they remain interpretation or
strategy rather than proof.

## 7. Final Summary

Relatively solid inside the current repository boundary:

- the accepted working base of the mixed-weak branch;
- the local right-boundary reduction and natural BC logic;
- structural independence of the circumferential channels in the current
  formulas;
- the pilot-backed two-dimensional center-regular family logic of the current
  reduced ansatz and `v2` workflow;
- the pilot-backed rule that the current `B_mix` builders use the
  center-regular mode pair rather than raw surrogate directions;
- the explicit target-object freeze
  “full admissible operator -> reduced tangent operator `L_red`” for the clean
  `simple support` rework;
- the exact finite-dimensional C3 statement
  `ker(L_red) <-> im(V_adm) ∩ ker(L_full)` on the current chosen reduced
  family;
- basis-independence of the reduced kernel question on that same family and the
  coordinate-equivalence `B_mix = B_red G_amp`;
- the exact ansatz-level characterization of the current selected reduced
  family `A_repo = im(V_adm)` as the KKT-selected amplitude family inside the
  weighted trial construction;
- the sharper structural meaning of that family: `A_ls` is the `H`-minimal
  KKT-selected section of a much larger amplitude fiber, not merely a chart for
  raw center regularity;
- the singular leading-block center relations in the current principal center
  model and their agreement with the amplitudes used by `A_ls`;
- the finite-order frozen-principal obstruction pattern: zero full leading
  layer, one-parameter next membrane mode, and zero checked second layer;
- the use of raw `B_mix` as the current baseline criterion together with the
  clean `n = 4, 6, 7, 8` competition set as the live operational benchmark.

Most urgent items to verify next:

- identify a theorem-facing selected local object `A_sel^loc`, or prove a
  global-to-local statement showing that the center traces of the globally
  weak-selected family are the right comparison partner for `im(V_adm)`;
- only after that, prove or disprove that this selected local/germ object
  matches the current selected family `im(V_adm)` rather than comparing
  `im(V_adm)` directly to the raw unrestricted local center-regular family;
- whether and when the reduced stacked operator can be replaced by the
  boundary-only object `B_red` / the raw baseline `B_mix`;
- whether a genuine quadratic-form object exists on the reduced admissible
  space, rather than only the current stacked-operator / Gram surrogate;
- the precise reason why `n = 6`, `n = 7`, and `n = 8` separate differently
  under the raw boundary-only reading and the lighter diagnostic pilots.

Most valuable next proof pilots:

1. A Lean-oriented abstraction pilot that formalizes the singular leading-data
   space, the KKT-selected amplitude family, and the already-closed reduced-
   family kernel equivalence.
2. A theorem-oriented object-selection pilot that derives a selected local
   family or proves a global-to-local comparison object matching the current
   weak/KKT-selected family.
3. A completeness step that compares that selected local/germ family to the
   global weighted-ansatz/KKT construction.
4. A C4 pilot that compares candidate spectral, generalized, and quadratic-form
   criteria on `L_red` and records exactly where equivalence holds or fails.


### V-S13. At the current theorem-facing leading-center-jet layer, the continuum/local selected trace equals `im(D_amp)` when written in the same coordinates as `J_0 = C_center`

- ID: `V-S13`
- Claim / Hypothesis:
  The current theorem-facing local comparison object for the selected trace
  stage is the leading-center trace written in the same coordinates as the live
  exact trace map `J_0 = C_center`, namely
  `[U0, P0, N0 + (lambda_c / n) P0, Y0 - lambda_c P0]`. On that coordinate
  choice, the singular local compatibility equations
  `n N0 + lambda_c P0 = 0` and `n N0 + Y0 = 0` imply
  `[U0, P0, N0 + (lambda_c / n) P0, Y0 - lambda_c P0] = D_amp [U0, P0]`, so
  the continuum/local selected leading-center trace plane is exactly
  `im(D_amp)`.
- Type: `formula-level claim`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.10.11;
  `docs/assumptions/assumptions.md` A21;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`;
  `src/shell_buckling/mixed_weak/solver_patched_core.py`.
- Current status: `closed at the leading-center-jet / current J_0-coordinate level`
- What counts as verification:
  symbolic derivation of the selected leading local relations, explicit recovery
  of the trace vector as `D_amp [U0, P0]`, structural inspection that the live
  clean background uses `lambda_theta0 = r0 / x`, and explicit confirmation on
  the representative clean path that the truncated background BCs give
  `u_r(x0) = 0` and therefore `lambda_theta0(x0) = 1` at the current selected
  `x0`-trace layer.
- Verification method:
  CAS, structural code inspection, representative live clean evaluation.
- Verification boundary:
  this does not yet produce a full intrinsic higher-order local selected family.
  It closes only the selected leading-center trace plane in the current
  theorem-facing coordinates. If one changes the fourth local trace coordinate,
  the exact equality with `im(D_amp)` is no longer automatic.
- Next action:
  prove a higher-order intrinsic local selected-family theorem preserving this
  same trace plane, or explicitly reconcile the current `J_0` coordinates with
  any alternative richer-local trace normalization.


### V-S14. Richer local trace charts are reconciled with `J_0` by an explicit projection, and the invariant selected object is a 2D lifted plane projecting to `im(D_amp)`

- ID: `V-S14`
- Claim / Hypothesis:
  Let the richer local trace chart be written as
  `Xi_rich^(1,eta) = [U0, P0, Delta_un^(0), Delta_psi,eta^(0), U1, N1, P1, Y1]`
  with `Delta_un^(0) = N0 + (lambda_c / n) P0` and
  `Delta_psi,eta^(0) = Y0 - eta P0`. Then there is an explicit triangular
  projection `Pi_eta_to_J0` sending
  `[U0, P0, Delta_un^(0), Delta_psi,eta^(0), U1, N1, P1, Y1]` to
  `[U0, P0, Delta_un^(0), Delta_psi,eta^(0) + (eta - lambda_c) P0]`, i.e. to
  the canonical current `J_0` trace. Under the current local selected leading
  relations, the selected object inside the richer trace is the 2D lifted plane
  `im(D_rich,eta)`, and `Pi_eta_to_J0(im(D_rich,eta)) = im(D_amp)` exactly.
- Type: `formula-level claim`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.10.12;
  `docs/assumptions/assumptions.md` A22;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status: `closed at the trace-reconciliation / truncated-jet level`
- What counts as verification:
  symbolic derivation of the projection identity, symbolic construction of the
  lifted plane `im(D_rich,eta)`, symbolic proof that its projection equals
  `im(D_amp)`, and representative live clean checks that the special case
  `eta = 1` indeed gives a small but nonzero lifted fourth component on the
  active clean path.
- Verification method:
  CAS, structural code inspection, limited representative live clean evaluation.
- Verification boundary:
  this does not yet produce a full higher-order selected-family theorem. It
  closes only the trace-normalization reconciliation and identifies the
  invariant object that the higher-order theorem should preserve.
- Next action:
  formulate and prove a higher-order theorem for a 2D lifted selected family in
  the richer trace space whose canonical `J_0` projection remains `im(D_amp)`.


### V-S15. The first checked post-leading recurrence preserves a corrected one-parameter membrane thickening, not the raw 2D lifted plane

- ID: `V-S15`
- Claim / Hypothesis:
  Let
  `Xi_rich^(1,eta) = [U0, P0, Delta_un^(0), Delta_psi,eta^(0), U1, N1, P1, Y1]`
  and let `im(D_rich,eta)` be the lifted 2D selected plane from C3h. Then at the
  first checked post-leading recurrence the equations are exactly independent of
  the leading selected amplitudes `(U0, P0)`. Under the same nonresonance
  assumption as the checked frozen-principal recurrence, the flexural
  post-leading coefficients satisfy `N1 = P1 = Y1 = M1 = Q0c = 0`, while the
  membrane sector leaves one free parameter `T1` with
  `U1 = alpha*T1`, `V1 = beta*T1`. Therefore raw `im(D_rich,eta)` is not
  exactly preserved; the smallest corrected object is a one-parameter membrane
  thickening over that lifted plane, and its canonical `J_0` projection is still
  exactly `im(D_amp)`.
- Type: `formula-level claim`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.10.13;
  `docs/assumptions/assumptions.md` A23;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status: `closed at the first checked post-leading recurrence level`
- What counts as verification:
  symbolic derivation of the first post-leading recurrence restricted to the
  selected leading trace, symbolic proof that its Jacobian with respect to
  `(U0, P0)` is zero, symbolic solution of the flexural and membrane blocks,
  symbolic construction of the corrected visible and augmented selected objects,
  symbolic proof that their canonical `J_0` projection remains `im(D_amp)`, and
  limited representative live clean checks that the membrane-mode visibility
  coefficient is nonzero on the active clean path.
- Verification method:
  CAS, structural code inspection, limited representative live clean evaluation.
- Verification boundary:
  this is not an all-orders theorem. It closes only the first corrected
  higher-order selected object and leaves open the intrinsic higher-order rule
  that should select, normalize, or quotient out the membrane thickening
  direction.
- Next action:
  formulate the intrinsic higher-order theorem for the corrected lifted family,
  or identify the canonical local normalization that removes the extra membrane
  parameter without changing the canonical `J_0` projection.


### V-S16. The membrane thickening direction is currently canonical only as a quotient kernel, not as a canonically normalized removable mode

- ID: `V-S16`
- Claim / Hypothesis:
  Let the corrected higher-order selected family from C3i be written as the 3D
  family `im(D_rich,eta^corr)` in the visible richer jet, or equivalently as the
  coefficient-faithful 3D family `im(D_rich,eta^aug)` in the augmented jet.
  Then the canonical `J_0` projection has exact one-dimensional kernel equal to
  the membrane thickening line. The next checked recurrence layer does not kill
  that line. Moreover there is a whole two-parameter family of 2D sections of
  the corrected 3D family, each projecting isomorphically to `im(D_amp)`, so no
  canonical normalized 2D section is selected by the current checked local data.
  Therefore the best current theorem-facing local object is the quotient of the
  corrected 3D family by the membrane line.
- Type: `formula-level claim`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.10.14;
  `docs/assumptions/assumptions.md` A24;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status: `closed at the quotient / first higher-order kernel level`
- What counts as verification:
  symbolic computation of the canonical projection on the corrected 3D family,
  symbolic computation of its one-dimensional kernel, symbolic proof that the
  kernel generator is killed by the projection, symbolic construction of the
  family of all 2D sections and proof that each section projects to `im(D_amp)`,
  together with the already checked second-layer fact that the membrane line is
  not killed at the next checked order.
- Verification method:
  CAS, structural inspection of the local recurrence, limited representative
  live clean evaluation inherited from C3i.
- Verification boundary:
  this does not prove a gauge symmetry and does not prove that the quotient has a
  unique distinguished representative. It identifies only the current canonical
  quotient object.
- Next action:
  derive the intrinsic higher-order rule that either canonically selects a
  representative of this quotient class or proves that the quotient itself is
  the final local selected object.


### V-S17. No intrinsic canonical higher-order representative is currently justified beyond the membrane quotient

- ID: `V-S17`
- Claim / Hypothesis:
  Let the corrected checked-order local selected family be the 3D family
  `im(D_rich,eta^corr)` in the visible richer jet, or equivalently the
  coefficient-faithful augmented family `im(D_rich,eta^aug)`. Then on the
  current checked local boundary no intrinsic local rule among the tested
  candidates canonically selects one representative of each quotient class
  modulo the membrane line. In particular, the next checked local compatibility
  layer does not distinguish representatives, checked local residual
  minimization also does not distinguish them, chart conditions such as
  `U1 = 0` are chart-dependent section choices, and orthogonality / minimal-norm
  rules depend on an extra metric choice. Therefore the strongest current
  theorem-facing local object remains the quotient
  `im(D_rich,eta^corr) / span(g_mem)`.
- Type: `formula-level claim`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.10.15;
  `docs/assumptions/assumptions.md` A25;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status: `closed on the current checked local quotient boundary`
- What counts as verification:
  symbolic proof that the next checked local compatibility layer does not
  distinguish representatives inside the membrane-thickened corrected family,
  symbolic proof that the checked residual vanishes along the membrane line,
  symbolic construction of quotient-preserving chart changes showing that
  `U1 = 0` is only a section choice, symbolic derivation of the metric-dependent
  orthogonality selector, and structural confirmation that the current global
  KKT metric has not yet been localized intrinsically.
- Verification method:
  CAS, structural inspection of the local recurrence and global KKT setup.
- Verification boundary:
  this does not prove that no future intrinsic selector exists. It proves only
  that none of the currently justified checked local rules canonically select a
  representative beyond the membrane quotient.
- Next action:
  derive an intrinsic higher-order selector that canonically represents each
  membrane-quotient class, or elevate the quotient itself to the final local
  theorem-facing selected object.


### V-S18. On the current checked local boundary the membrane quotient is the final theorem-facing local selected object

- ID: `V-S18`
- Claim / Hypothesis:
  Let the corrected checked-order local selected family be the 3D family
  `im(D_rich,eta^corr)` in the visible richer jet, or equivalently the
  coefficient-faithful augmented family `im(D_rich,eta^aug)`. Then on the
  current checked local boundary the quotient
  `im(D_rich,eta^corr) / span(g_mem)` is the final local theorem-facing selected
  object. More precisely: every currently justified local selected invariant
  factors through the quotient map to the two quotient coordinates, no checked
  local condition distinguishes representatives inside one quotient class, and
  any canonical comparison to the already closed global selected trace must
  therefore pass through this quotient object.
- Type: `formula-level claim`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.10.16;
  `docs/assumptions/assumptions.md` A26;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status: `closed on the current checked local boundary`
- What counts as verification:
  symbolic proof that the canonical `J_0` trace on the corrected 3D family is
  exactly `D_amp` composed with the quotient map `(a, b, s) -> (a, b)`,
  symbolic proof that the checked local residual vanishes identically on the
  corrected family, symbolic confirmation that the next checked local
  compatibility layer contributes no representative-level invariant, together
  with the already checked failure of the strongest plausible intrinsic
  selectors.
- Verification method:
  CAS, structural inspection of the local recurrence and global KKT setup.
- Verification boundary:
  this is a boundary-scoped finality theorem. It does not prove that no future
  unchecked higher-order intrinsic selector could ever appear. It proves only
  that none is currently justified on the checked local boundary and that the
  quotient is therefore the final local theorem-facing object there.
- Next action:
  either lift this boundary-scoped quotient theorem to a stronger higher-order
  theorem, or derive a genuinely new intrinsic selector beyond the current
  checked local boundary.

### V-S19. `T3a` target: finite-dimensional selected-class criticality on the current clean repository boundary should be read through `ker(L_red)`, not through a boundary descendant alone

- ID: `V-S19`
- Claim / Hypothesis:
  For fixed clean `(n, q)`, let
  `L_full,n(q) = [A_int,n(q); B_full,n(q)]`,
  let the current selected repository class be
  `A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q))`
  on the weighted-ansatz boundary, and let
  `L_red,n(q) = L_full,n(q) V_adm,n(q)`.
  Then the correct theorem-facing bridge target is:
  selected-class criticality on the current repository boundary should be read
  through the exact nontrivial-kernel question
  `exists 0 != c in A_sel^repo,n(q) : L_full,n(q) c = 0`
  if and only if
  `exists 0 != a in R^2 : L_red,n(q) a = 0`,
  while `B_red` / `B_mix` remain descendants on the same selected family rather
  than theorem-level replacements for the full stacked operator.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/vyvod_uravneniy_updated17.md` sections 1.8-1.10;
  `proof_pilots/pilot_24_t3a_selected_kernel_bridge/pilot_24_t3a_selected_kernel_bridge.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/reduction_check.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`.
- Current status: `packaged and closed enough on the finite-dimensional selected-family boundary`
- What counts as verification:
  a clean `T3a` theorem package that explicitly combines:
  exact selected-family reading `A_sel^repo = A_ls = im(V_adm) = im(M_amp)`,
  exact reduced-object identity `L_red = L_full V_adm`,
  exact finite-dimensional bijection `R^2 <-> A_sel^repo`,
  exact restricted-kernel bridge on that class,
  the Outcome-B local quotient result only as a compatibility/support layer,
  and the explicit caution that `B_red` / `B_mix` do not yet collapse the
  problem to a boundary-only criterion.
- Verification method:
  manual derivation, CAS, code inspection, Lean abstraction for the
  finite-dimensional bridge.
- Verification boundary:
  repository-level selected-class theorem only; not yet a final physical shell
  theorem, not yet a proof that the current selected class is the full exact
  continuum admissible clean tangent space, and not yet a proof that
  boundary-only degeneration is equivalent to the full reduced-kernel problem.
- Next action:
  keep `V-S19` as the closed enough repository-selected `T3a` bridge layer,
  optionally formalize the abstract finite-dimensional bijection/kernel step in
  Lean, and keep the broader long-term `T3` question open beyond the current
  repository-selected family.

### V-S20. `T3b` implementation: the strongest current theorem-facing class above `A_sel^repo` is the shadow-compatible candidate `A_sel^{th,cand}`

- ID: `V-S20`
- Claim / Hypothesis:
  Let
  `A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q))`
  be the current repository-selected family closed by `T3a`.
  Define the strongest currently justified theorem-facing candidate above that
  family by
  `A_sel^{th,cand},n(q)
   := { c : J_0(c) in im(D_amp,n(q))
        and Q_chk(c) in im(D_rich,eta^corr,n(q)) / span(g_mem,n(q)) }`,
  where `Q_chk(c)` denotes the checked local quotient shadow of the current
  richer local germ of `c` whenever that checked local shadow is defined on the
  current boundary.
  Then the implemented `T3b` step is:
  the stronger theorem-facing selected-class target is now constructed at the
  candidate level through the simultaneous selected-trace and checked-quotient
  conditions, with the conservative relation
  `A_sel^repo,n(q) subseteq A_sel^{th,cand},n(q)`.
  The remaining open theorem is the exact comparison/losslessness statement
  deciding whether `A_sel^repo` already exhausts `A_sel^{th,cand}` strongly
  enough to upgrade the selected-class kernel reading beyond `T3a`.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/vyvod_uravneniy_updated17.md` sections `1.9`-`1.10.16`;
  `docs/assumptions/assumptions.md` entries `A17`-`A20`, `A24`-`A26`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_24_t3a_selected_kernel_bridge/pilot_24_t3a_selected_kernel_bridge.md`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `candidate class defined; exact comparison/losslessness theorem with A_sel^repo still open`
- What counts as verification:
  a clean `T3b` package that explicitly records:
  the exact current repository-selected family `A_sel^repo`,
  the new shadow-compatible candidate class `A_sel^{th,cand}`,
  the selected trace condition `J_0(c) in im(D_amp)`,
  the checked local quotient condition
  `Q_chk(c) in im(D_rich,eta^corr) / span(g_mem)`,
  the conservative inclusion `A_sel^repo subseteq A_sel^{th,cand}`,
  and the exact missing comparison/losslessness ingredient still needed to
  upgrade the selected-class kernel reading beyond `T3a`.
- Verification method:
  manual derivation, CAS, code inspection, Lean abstraction only for the
  conditional finite-dimensional comparison template once the class relation is
  explicit.
- Verification boundary:
  this is not yet full `T3`, not a final physical shell theorem, not a proof
  that `A_sel^repo = A_sel^{th,cand}`, not a proof that
  `A_sel^{th,cand}` is already the final intrinsic stronger class, and not a
  proof that boundary-only descendants replace the full reduced-kernel
  question.
- Next action:
  keep `V-S19` as the closed enough repo-selected bridge layer, keep the new
  `V-S20` candidate-class package as the next theorem-facing step above it, and
  isolate the single main bottleneck as the exact comparison/losslessness
  theorem between `A_sel^repo` and `A_sel^{th,cand}`.

### V-S21. `T3c` implementation: the strongest current comparison theorem is exact inclusion `A_sel^repo subseteq A_sel^{th,cand}`, and the reverse inclusion is reduced to the selected-representative law

- ID: `V-S21`
- Claim / Hypothesis:
  Let
  `A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q))`
  be the exact repo-selected family, and let
  `A_sel^{th,cand},n(q)`
  be the shadow-compatible candidate class from `V-S20`.
  Then the strongest currently justified comparison theorem on the current
  repository/theory boundary is:
  `A_sel^repo,n(q) subseteq A_sel^{th,cand},n(q)`,
  while the reverse inclusion is reduced exactly to the selected-representative
  theorem
  `c = P_sel,n(q) J_0(c)` for every `c in A_sel^{th,cand},n(q)`.
  The exact obstruction is that the candidate conditions control only the
  already closed selected trace and checked quotient shadows, whereas the
  current repo-selected family is the unique global weak/KKT-selected
  `H_n,q`-minimal section of a much larger fixed-center fiber.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.8`-`1.10.16`;
  `docs/assumptions/assumptions.md` entries `A18`-`A20`, `A26`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `Outcome B: exact inclusion closed enough; reverse inclusion reduced to one exact missing theorem`
- What counts as verification:
  a clean `T3c` package that explicitly records:
  the exact inclusion `A_sel^repo subseteq A_sel^{th,cand}`,
  the selected-trace bijection on `A_sel^repo` with inverse `P_sel`,
  the quotient-factorization statement showing that current local selected
  invariants carry no representative-level data beyond the two quotient
  coordinates,
  and the exact reduction of the remaining gap to the theorem
  `c = P_sel J_0(c)` for `c in A_sel^{th,cand}`.
- Verification method:
  manual derivation, CAS/theory reuse for the local quotient factorization,
  code inspection, representative live clean evaluation for the global
  fiber/KKT-selected section side.
- Verification boundary:
  this is not yet full `T3`, not a final physical shell theorem, not a proof
  that `A_sel^repo = A_sel^{th,cand}`, and not a proved non-equality theorem
  either. It is the strongest current inclusion-plus-obstruction theorem on the
  present repository/theory boundary.
- Next action:
  prove or refute the selected-representative theorem
  `c = P_sel J_0(c)` for `c in A_sel^{th,cand}`, i.e. decide whether the
  candidate class is already exhausted by the exact repo-selected family.

### V-S22. `T3d` implementation: on the current repo-selected boundary the representative law is equivalent to fiberwise `H_n,q`-minimality / `H_n,q`-orthogonality, and current candidate-class membership does not yet imply that law

- ID: `V-S22`
- Claim / Hypothesis:
  Let
  `A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q))`
  be the exact repo-selected family, and let
  `A_sel^{th,cand},n(q)`
  be the shadow-compatible candidate class. For `c in A_sel^{th,cand},n(q)`,
  define the exact repo-selected representative with the same selected trace by
  `c_sel := P_sel,n(q) J_0(c)`.
  Then on the current repo-selected boundary:
  `c = c_sel` is equivalent to fiberwise
  `H_n,q`-orthogonality
  `z^T H_n,q c = 0` for every `z in ker(C_center,n(q))`,
  equivalently to `c` being the unique `H_n,q`-minimal point in its
  fixed-trace fiber.
  The current candidate-class conditions force only the selected trace shadow
  and checked local quotient compatibility, while the checked local quotient
  theorem remains representative-lossy. Therefore the exact remaining
  obstruction is the missing bridge from candidate-class membership to this
  global weak/KKT-selected `H_n,q`-minimality law.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.8`-`1.10.16`;
  `docs/assumptions/assumptions.md` entries `A18`-`A20`, `A26`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `Outcome B: exact representative-law criterion isolated; candidate-class membership does not yet imply it`
- What counts as verification:
  a clean `T3d` package that explicitly records:
  the same-trace fiber relation between `c` and `P_sel J_0(c)`,
  the equivalence between the representative law and fiberwise
  `H_n,q`-orthogonality / minimality,
  the representative-lossiness of the checked local quotient theorem,
  and the exact counter-condition
  `exists z in ker(C_center) : z^T H_n,q c != 0` as the failure mode for the
  representative law.
- Verification method:
  manual derivation, code inspection, representative live clean evaluation for
  the global fiber/KKT-selected section side, CAS/theory reuse for the local
  quotient factorization side.
- Verification boundary:
  this is not yet full `T3`, not a final physical shell theorem, not a proof
  that every candidate-class element is already `H_n,q`-minimal, and not a
  constructed counterexample either. It is the strongest current
  representative-law / obstruction theorem on the present repository boundary.
- Next action:
  prove or refute the bridge from candidate-class membership to fiberwise
  `H_n,q`-orthogonality / minimality, equivalently prove or refute
  `c = P_sel J_0(c)` for every `c in A_sel^{th,cand}`.

### V-S23. `T3e` implementation: the remaining bridge is exactly vanishing of the nonnegative fiber-excess functional `Delta_H,n,q(c)`

- ID: `V-S23`
- Claim / Hypothesis:
  Let
  `A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q))`
  be the exact repo-selected family, and let
  `A_sel^{th,cand},n(q)`
  be the shadow-compatible candidate class. For `c in A_sel^{th,cand},n(q)`,
  define
  `c_sel := P_sel,n(q) J_0(c)`
  and
  `z := c - c_sel`.
  Then on the current repo-selected boundary:
  `z in ker(C_center,n(q))`,
  `z^T H_n,q c_sel = 0`,
  and therefore
  `c^T H_n,q c = c_sel^T H_n,q c_sel + z^T H_n,q z`.
  Equivalently, with
  `Delta_H,n,q(c) := (c - P_sel,n(q) J_0(c))^T H_n,q (c - P_sel,n(q) J_0(c))`,
  one has
  `Delta_H,n,q(c) >= 0`,
  with equality if and only if
  `c = P_sel,n(q) J_0(c)`,
  equivalently if and only if `c` is the unique `H_n,q`-minimal point in its
  fixed-trace fiber.
  The current candidate-class conditions still force only the selected trace
  shadow and checked local quotient compatibility, while the checked local
  quotient theorem remains representative-lossy. Therefore the exact remaining
  obstruction is now the missing bridge from candidate-class membership to
  `Delta_H,n,q(c) = 0`.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.8`-`1.10.16`;
  `docs/assumptions/assumptions.md` entries `A18`-`A20`, `A26`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `Outcome B: exact fiber-excess criterion isolated; candidate-class membership does not yet imply its vanishing`
- What counts as verification:
  a clean `T3e` package that explicitly records:
  the fixed-trace decomposition
  `c = P_sel J_0(c) + z`,
  the orthogonality relation
  `z^T H_n,q P_sel J_0(c) = 0`,
  the exact fiber-excess identity
  `c^T H_n,q c = c_sel^T H_n,q c_sel + Delta_H,n,q(c)`,
  the equivalence
  `Delta_H,n,q(c) = 0 <-> c = P_sel J_0(c)`,
  and the exact counter-condition
  `Delta_H,n,q(c) > 0`
  as the failure mode for the reverse inclusion.
- Verification method:
  manual derivation, code inspection, representative live clean evaluation for
  the global fiber/KKT-selected section side, CAS/theory reuse for the local
  quotient factorization side.
- Verification boundary:
  this is not yet full `T3`, not a final physical shell theorem, not a proof
  that every candidate-class element has zero fiber excess, and not a
  constructed counterexample either. It is the strongest current zero-excess /
  obstruction theorem on the present repository boundary.
- Next action:
  prove or refute the bridge from candidate-class membership to
  `Delta_H,n,q(c) = 0`, equivalently prove or refute vanishing of the
  same-trace fiber excess for every `c in A_sel^{th,cand}`.

### V-S24. `T3f` implementation: the current shadow conditions are representative-lossy, and any nonzero admissible same-trace, quotient-invisible fiber residual is an exact counterexample template

- ID: `V-S24`
- Claim / Hypothesis:
  Keep
  `A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q))`
  as the exact repo-selected family, and let
  `A_sel^{th,cand},n(q)`
  be the shadow-compatible candidate class. For
  `c in A_sel^{th,cand},n(q)`,
  let
  `c_sel := P_sel,n(q) J_0(c)`
  and
  `z := c - c_sel`.
  Then the exact fiber-excess identity from `V-S23` gives
  `Delta_H,n,q(c) = z^T H_n,q z`.
  On the checked local boundary, however, every currently justified local
  selected invariant factors through the quotient coordinates and does not
  distinguish representatives inside one quotient class. Therefore the current
  candidate-class conditions force only the selected trace shadow together with
  quotient-object compatibility, and do not yet impose any closed
  representative-level condition implying `z = 0` or `Delta_H,n,q(c) = 0`.
  More sharply: if there exist
  `c_sel in A_sel^repo,n(q)`
  and
  `0 != z in A_adm^th,n(q) intersect ker(C_center,n(q))`
  such that
  `Q_chk(c_sel + z) in im(D_rich,eta^corr,n(q)) / span(g_mem,n(q))`,
  then
  `c := c_sel + z`
  lies in `A_sel^{th,cand},n(q)` and satisfies
  `Delta_H,n,q(c) = z^T H_n,q z > 0`.
  So any such `z` is an exact counterexample template to reverse inclusion /
  losslessness on the current repository boundary.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.8`-`1.10.16`;
  `docs/assumptions/assumptions.md` entries `A18`-`A20`, `A26`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `Outcome B: exact shadow-only obstruction isolated; the conditional counterexample template is written, but existence or impossibility of such a residual is still open`
- What counts as verification:
  a clean `T3f` package that explicitly records:
  the exact decomposition
  `c = P_sel J_0(c) + z`,
  the exact identity
  `Delta_H,n,q(c) = z^T H_n,q z`,
  the local quotient-factorization statement that currently justified local
  selected invariants carry no representative-level data beyond the quotient
  coordinates, and the exact template
  `0 != z in A_adm^th intersect ker(C_center)`
  with quotient-compatible shadow
  `=> Delta_H,n,q(c_sel + z) > 0`.
- Verification method:
  manual derivation, code inspection, representative live clean evaluation for
  the global selection side, CAS/theory reuse for the quotient-lossiness side.
- Verification boundary:
  this is not yet full `T3`, not a final physical shell theorem, not a proof
  that a positive-excess example exists, and not a proof that it cannot exist.
  It is the sharpest current obstruction theorem on the present repository
  boundary.
- Next action:
  prove or refute that no nonzero admissible same-trace, quotient-invisible
  fiber residual survives, equivalently prove or refute
  `Delta_H,n,q(c) = 0` for every `c in A_sel^{th,cand}`.

### V-S25. `T3g` implementation: the remaining zero-excess gap is exactly the residual-lift class `R_inv,n(q; c_sel)`

- ID: `V-S25`
- Claim / Hypothesis:
  For fixed clean `(n, q)`, keep
  `A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q))`
  and let
  `c_sel in A_sel^repo,n(q)`.
  Define the exact same-trace residual class
  `R_same,n(q) := ker(C_center,n(q)) = ker(J_0,n(q))`
  and the exact quotient-invisible admissible lift class
  `R_inv,n(q; c_sel)
   := { z in A_adm^th,n(q) intersect R_same,n(q)
        : Q_chk(c_sel + z) = Q_chk(c_sel) }`
  whenever the checked local quotient shadow is defined on the current checked
  boundary. Then:
  1. `z in R_same,n(q)` means exactly that `c_sel + z` has the same selected
     leading trace as `c_sel`;
  2. `z in R_inv,n(q; c_sel)` means exactly that `c_sel + z` is invisible to
     the currently closed quotient-level selected invariants on that checked
     boundary;
  3. the remaining reverse-inclusion / zero-excess question is now exactly
     whether `R_inv,n(q; c_sel) = {0}` for every repo-selected representative
     `c_sel`;
  4. equivalently, the unresolved object is whether the local membrane-kernel
     line `span(g_mem,n(q))`, which is the exact quotient kernel on the checked
     local boundary, has a nonzero admissible global lift inside
     `ker(C_center,n(q))`;
  5. if such a nonzero lift exists, then it yields a candidate-class element
     with the same selected trace and positive excess
     `Delta_H,n,q(c_sel + z) = z^T H_n,q z > 0`;
     if no such lift exists, then `Delta_H,n,q(c) = 0` holds on the whole
     candidate class.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.8`-`1.10.16`;
  `docs/assumptions/assumptions.md` entries `A18`-`A20`, `A26`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `Outcome B: the existence/impossibility question is reduced exactly to triviality or nontriviality of the lift class R_inv,n(q; c_sel); no impossibility theorem and no explicit nonzero lift are yet closed`
- What counts as verification:
  a clean `T3g` package that explicitly records:
  the exact classes
  `R_same,n(q) = ker(C_center,n(q)) = ker(J_0,n(q))`
  and
  `R_inv,n(q; c_sel)`,
  the fact that quotient-invisibility on the checked local boundary is carried
  by the local membrane-kernel direction `span(g_mem,n(q))`,
  the exact equivalence
  `R_inv,n(q; c_sel) = {0} for all c_sel in A_sel^repo,n(q)
   iff Delta_H,n,q(c) = 0 for all c in A_sel^{th,cand},n(q)`,
  and the sharpened obstruction theorem that the whole remaining gap is the
  admissible global lift problem for that quotient kernel.
- Verification method:
  manual derivation, code inspection, representative live clean evaluation for
  the global KKT-selected section side, CAS/theory reuse for the local quotient
  kernel and quotient-factorization side.
- Verification boundary:
  this is not yet full `T3`, not a final physical shell theorem, not an
  impossibility theorem for nonzero residuals, and not an explicit constructed
  residual either. It is the sharpest current theorem-facing reduction of the
  zero-excess gap on the present repository boundary.
- Next action:
  prove or refute that the local membrane-kernel line `span(g_mem,n(q))` has
  no nonzero admissible global lift inside `ker(C_center,n(q))`, equivalently
  prove or refute `R_inv,n(q; c_sel) = {0}` for every
  `c_sel in A_sel^repo,n(q)`.

### V-S26. `T3h` implementation: the exact global membrane-lift class is the kernel of the checked local quotient map on admissible same-trace residuals

- ID: `V-S26`
- Claim / Hypothesis:
  For fixed clean `(n, q)`, keep
  `A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q))`
  and let
  `c_sel in A_sel^repo,n(q)`.
  Let
  `R_same,n(q) := ker(C_center,n(q)) = ker(J_0,n(q))`.
  On the current checked local boundary, let the corrected local coefficient
  quotient map be
  `q_coeff = [[1,0,0],[0,1,0]]`
  with
  `ker(q_coeff) = span(e_mem)`
  and
  `g_mem,n(q) = D_rich,eta^corr,n(q) e_mem`.
  Whenever the checked local shadows of `c_sel + z` and `c_sel` are defined in
  a common corrected chart, let
  `delta_chk,n(q; c_sel)(z)`
  denote the checked local coefficient difference in that chart. Define
  `Lift_mem,n(q; c_sel)
   := { z in A_adm^th,n(q) intersect R_same,n(q)
        : delta_chk,n(q; c_sel)(z) in span(e_mem) }`.
  Then:
  1. `Lift_mem,n(q; c_sel) = R_inv,n(q; c_sel)`;
  2. equivalently, on the current linear tangent boundary,
     `Lift_mem,n(q; c_sel)
      = ker(q_coeff o delta_chk,n(q; c_sel)
            |_(A_adm^th,n(q) intersect ker(C_center,n(q))))`;
  3. hence triviality/nontriviality of the remaining zero-excess gap is now the
     exact kernel question for the checked local lift map, not merely a named
     residual-class question in ambient prose.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.14`-`1.10.16`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `Outcome B: the lift problem is now reduced exactly to the kernel of q_coeff o delta_chk on the admissible same-trace global residual space; no impossibility theorem and no explicit nonzero lift are yet closed`
- What counts as verification:
  a clean `T3h` package that explicitly records:
  the exact local quotient map
  `q_coeff = [[1,0,0],[0,1,0]]`,
  the exact local membrane-kernel line
  `ker(q_coeff) = span(e_mem)` and its jet image `span(g_mem)`,
  the exact checked local coefficient-difference map
  `delta_chk,n(q; c_sel)`,
  the exact global lift class
  `Lift_mem,n(q; c_sel)`,
  and the exact reformulation
  `Lift_mem = R_inv = ker(q_coeff o delta_chk)`.
- Verification method:
  manual derivation, code inspection, representative helper evaluation for the
  closed local quotient-kernel side and the closed global selected-fiber side.
- Verification boundary:
  this is not yet full `T3`, not a final physical shell theorem, not an
  impossibility theorem for nonzero global lifts, and not an explicit
  constructed lift either. It is the sharpest current local-to-global kernel
  reduction of the remaining zero-excess gap on the present repository
  boundary.
- Next action:
  construct or control `delta_chk,n(q; c_sel)` on
  `A_adm^th,n(q) intersect ker(C_center,n(q))`
  well enough to decide whether
  `ker(q_coeff o delta_chk,n(q; c_sel)) = {0}` for every
  `c_sel in A_sel^repo,n(q)`.

### V-S27. `T3i` implementation: injectivity is reduced to one exact missing global checked-local extraction operator

- ID: `V-S27`
- Claim / Hypothesis:
  For fixed clean `(n, q)`, let
  `D_res,n(q) := A_adm^th,n(q) intersect ker(C_center,n(q))`
  and, on the checked boundary,
  `D_res,chk,n(q; c_sel)
   := { z in D_res,n(q) : delta_chk,n(q; c_sel)(z) is defined }`.
  Define
  `Phi_chk,n(q; c_sel) := q_coeff o delta_chk,n(q; c_sel)`.
  Then:
  1. `ker(Phi_chk,n(q; c_sel)) = Lift_mem,n(q; c_sel) = R_inv,n(q; c_sel)`;
  2. `q_coeff` is exactly linear and quotient-preserving-chart invariant on the
     checked local boundary;
  3. by definition `delta_chk,n(q; c_sel)` is affine in the base point;
  4. if an explicit global checked local coefficient-extraction operator
     `chi_chk,n(q)` existed on `D_res,n(q)`, then
     `delta_chk,n(q; c_sel)(z) = chi_chk,n(q)(z)`,
     so the kernel question would become a genuine linear injectivity/rank
     theorem for `q_coeff o chi_chk,n(q)` on `D_res,n(q)`;
  5. the current repository does not yet package such an operator, so the
     injectivity question is not yet a closed global rank/nullspace theorem.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.14`-`1.10.16`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `Outcome D: the exact missing ingredient is now isolated as a global checked local coefficient-extraction operator chi_chk,n(q) on the admissible same-trace residual domain`
- What counts as verification:
  a clean `T3i` package that explicitly records:
  the exact domains `D_res` and `D_res,chk`,
  the projected map `Phi_chk = q_coeff o delta_chk`,
  the exact identity `ker(Phi_chk) = Lift_mem = R_inv`,
  the chart-invariance of `q_coeff`,
  and the exact conditional reduction from `delta_chk` to a fixed linear global
  operator `chi_chk`.
- Verification method:
  code inspection, manual derivation, representative helper evaluation for the
  local quotient-map invariance side, and repository search for `delta_chk` /
  `chi_chk`.
- Verification boundary:
  this is not yet full `T3`, not a final physical shell theorem, not an
  injectivity theorem for `Phi_chk`, and not an explicit nonzero kernel element
  either. It is the sharpest current operator-level obstruction theorem on the
  present repository boundary.
- Next action:
  construct or control an explicit global checked local coefficient-extraction
  operator `chi_chk,n(q)` on
  `D_res,n(q) = A_adm^th,n(q) intersect ker(C_center,n(q))`
  strongly enough that the kernel of `q_coeff o chi_chk,n(q)` can be decided.

### V-S28. `T3j` implementation: the local checked extractor is explicit, and the remaining gap is the global shadow bridge

- ID: `V-S28`
- Claim / Hypothesis:
  For fixed clean `(n, q)`:
  1. the visible checked local corrected family is
     `Xi_sel,corr^(1,eta),n(q) = im(D_rich,eta^corr,n(q))`;
  2. there is an explicit linear visible-chart extractor
     `chi_chk,vis,n(q) := L_vis,n(q)|_(Xi_sel,corr^(1,eta),n(q))`
     with `L_vis,n(q) D_rich,eta^corr,n(q) = I_3`;
  3. under quotient-preserving chart changes the full 3-coordinate extractor is
     chart-dependent, but
     `q_coeff o chi_chk,(ell1,ell2),n(q)
      = q_coeff o chi_chk,vis,n(q)`;
  4. on `Xi_sel,corr^(1,eta),n(q)`,
     `q_coeff o chi_chk,vis,n(q) = L_amp o Pi_eta_to_J0`;
  5. therefore the projected checked local coefficient extractor is already
     canonical on the checked local corrected family;
  6. what is still missing is a global checked-local shadow map
     `Sh_chk,n(q) : D_res,n(q) -> Xi_sel,corr^(1,eta),n(q)`,
     or an equivalent exact control theorem, from which a theorem-facing global
     operator `chi_chk,n(q)` on `D_res,n(q)` could be composed.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.14`-`1.10.16`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `Outcome D: the strongest current result is a partial construction on the strict checked local corrected-family domain together with an exact obstruction to extending it to a theorem-facing global operator on D_res,n(q)`
- What counts as verification:
  a clean `T3j` package that explicitly records:
  the local corrected-family extractor `chi_chk,vis`,
  its chart-transformation law,
  the projected invariance under `q_coeff`,
  the exact factorization through `Pi_eta_to_J0`,
  and the remaining missing global shadow map `Sh_chk`.
- Verification method:
  CAS, code inspection, manual derivation, and repository search for a global
  checked-local shadow operator.
- Verification boundary:
  this is not yet full `T3`, not a final physical shell theorem, not a closed
  global operator theorem on `D_res,n(q)`, and not yet the injectivity theorem
  for `q_coeff o chi_chk,n(q)`. It is the sharpest current separation between
  the already available local extractor and the still-missing global bridge.
- Next action:
  construct or control a global checked-local shadow map
  `Sh_chk,n(q) : D_res,n(q) -> Xi_sel,corr^(1,eta),n(q)`
  strongly enough that
  `chi_chk,n(q) := chi_chk,vis,n(q) o Sh_chk,n(q)`
  is well-defined and the kernel of `q_coeff o chi_chk,n(q)` can be decided.

### V-S29. `T3k` implementation: any compatible raw same-trace shadow already collapses to the zero quotient class

- ID: `V-S29`
- Claim / Hypothesis:
  For fixed clean `(n, q)`:
  1. on `Xi_sel,corr^(1,eta),n(q)` one has
     `q_coeff o chi_chk,vis,n(q) = L_amp o Pi_eta_to_J0`;
  2. `D_res,n(q) = A_adm^th,n(q) intersect ker(C_center,n(q))
                   subset ker(J_0,n(q))`;
  3. therefore any theorem-facing checked-local shadow map
     `Sh_chk,n(q) : D_res,n(q) -> Xi_sel,corr^(1,eta),n(q)`
     compatible with the current quotient reading must satisfy
     `q_coeff o chi_chk,vis,n(q) o Sh_chk,n(q) = 0`;
  4. equivalently, any such raw shadow map must land in
     `span(g_mem,n(q))` and is only a scalar membrane-selector candidate
     `sigma_chk,n(q)`;
  5. so a raw basepoint-independent factorization
     `Phi_chk = q_coeff o chi_chk,vis o Sh_chk`
     on `D_res,n(q)` would be identically zero and cannot be the correct
     remaining nontrivial global bridge.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.14`-`1.10.16`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `Outcome C: the raw same-trace shadow-map target is now ruled out as the correct nontrivial bridge on the current boundary; the exact remaining issue is a basepoint-relative representative-difference object or a theorem killing the membrane selector`
- What counts as verification:
  a clean `T3k` package that explicitly records:
  the factorization `q_coeff o chi_chk,vis = L_amp o Pi_eta_to_J0`,
  the inclusion `D_res subset ker(J_0)`,
  the membrane-line factorization of any compatible raw shadow map,
  and the resulting impossibility of a nontrivial raw factorization of `Phi_chk`
  through `q_coeff o chi_chk,vis o Sh_chk`.
- Verification method:
  CAS, code inspection, manual derivation, and reuse of the closed quotient
  finality theorem from pilot 23.
- Verification boundary:
  this is not yet full `T3`, not a final physical shell theorem, not the final
  injectivity theorem, and not yet a construction of the correct basepoint-
  relative global object. It is an exact obstruction theorem for the raw same-
  trace shadow-map target.
- Next action:
  construct or control a theorem-facing basepoint-relative checked-local
  representative-difference object on ambient candidate-class pairs before
  quotient collapse, or prove directly that the admissible same-trace membrane
  selector vanishes on
  `A_adm^th,n(q) intersect ker(C_center,n(q))`.

### V-S30. `T3l` implementation: the correct surviving checked-local bridge object is the pairwise membrane-difference on equal-trace pairs

- ID: `V-S30`
- Claim / Hypothesis:
  For fixed clean `(n, q)`:
  1. the raw same-trace shadow on
     `D_res,n(q) = A_adm^th,n(q) intersect ker(C_center,n(q))`
     already collapses to the zero quotient class;
  2. on the equal-trace checked-local pair domain `Pair_chk,n(q)`, if
     `chi_chk,chart,n(q)(c) = (a,b,s)^T` and
     `chi_chk,chart,n(q)(c_ref) = (a_ref,b_ref,s_ref)^T`, then
     `a = a_ref`, `b = b_ref`, and the difference is
     `(0,0,s-s_ref)^T in span(e_mem)`;
  3. under every quotient-preserving chart change this difference is unchanged;
  4. therefore there is a well-defined theorem-facing pair object
     `Delta_rep,chk,n(q; c, c_ref) in span(e_mem)`,
     equivalently a unique scalar selector
     `sigma_chk,n(q; c, c_ref)` with
     `Delta_rep,chk = sigma_chk e_mem`;
  5. on the residual-generated pair domain this yields the basepoint-relative
     membrane selector `sigma_chk,n(q; c_sel)(z)`;
  6. the next nontrivial theorem is now vanishing/nonvanishing of this pairwise
     object, not existence of a raw same-trace shadow map.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.14`-`1.10.16`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `Outcome A: the correct basepoint-relative checked-local bridge object is now constructed at the structural level; vanishing of the induced selector remains open`
- What counts as verification:
  a clean `T3l` package that explicitly records:
  the raw same-trace zero-collapse,
  the invariance of equal-trace pairwise membrane difference under
  quotient-preserving chart changes,
  the theorem-facing pair object `Delta_rep,chk`,
  the equivalent scalar selector `sigma_chk`,
  and the reduction of the next theorem to vanishing/nonvanishing of that
  selector.
- Verification method:
  CAS, code inspection, manual derivation.
- Verification boundary:
  this is not yet full `T3`, not a final physical shell theorem, not a
  vanishing theorem for `sigma_chk`, and not yet the final injectivity theorem.
  It is the sharpest current construction of the surviving nontrivial
  checked-local bridge object below the full theorem.
- Next action:
  prove or refute that the basepoint-relative membrane selector
  `sigma_chk,n(q; c_sel)(z)` vanishes on the exact admissible residual-generated
  checked-local pair domain.

### V-S31. `T3m` implementation: the basepoint-relative membrane selector is the exact surviving membrane cocycle, but vanishing is still obstructed

- ID: `V-S31`
- Claim / Hypothesis:
  For fixed clean `(n, q)` and fixed repo-selected basepoint `c_sel`:
  1. the exact residual-generated selector domain is
     `D_sigma,n(q; c_sel) := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
     (c_sel + z, c_sel) in Pair_chk,n(q) }`;
  2. on this domain the basepoint-relative selector
     `sigma_chk,n(q; c_sel)(z) := sigma_chk,n(q; c_sel + z, c_sel)` is
     well-defined;
  3. on the equal-trace checked-local pair domain the selector is a
     chart-invariant membrane cocycle with
     `sigma_chk(c, c) = 0`,
     `sigma_chk(c, c_ref) = -sigma_chk(c_ref, c)`,
     and
     `sigma_chk(c_1, c_3) = sigma_chk(c_1, c_2) + sigma_chk(c_2, c_3)`;
  4. vanishing of `sigma_chk,n(q; c_sel)(z)` is equivalent to vanishing of the
     pairwise representative-difference object
     `Delta_rep,chk,n(q; c_sel + z, c_sel)`;
  5. the current theorem-facing admissibility / selected-trace structure still
     forces only equality of the quotient coordinates `(a, b)`, not vanishing
     of the membrane cocycle;
  6. therefore current checked-local selected invariants do not yet force
     `sigma_chk = 0`, and any admissible residual-generated pair with common
     corrected-chart coordinates `(a, b, s_sel + delta)` and `(a, b, s_sel)`
     and `delta != 0` gives the exact nonvanishing template
     `sigma_chk = delta != 0`.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `Outcome B: the selector structure now closes as an exact cocycle / obstruction theorem, but vanishing and explicit nonvanishing on the exact admissible pair domain are both still open`
- What counts as verification:
  a clean `T3m` package that explicitly records:
  the exact domain `D_sigma,n(q; c_sel)`,
  the chart-invariant cocycle laws for `sigma_chk`,
  the equivalence between vanishing of `sigma_chk` and vanishing of
  `Delta_rep,chk`,
  and the exact obstruction theorem showing that current checked-local
  selected invariants still factor only through the membrane quotient.
- Verification method:
  CAS, code inspection, manual derivation.
- Verification boundary:
  this is not yet full `T3`, not a vanishing theorem for `sigma_chk`, not an
  explicit admissible nonzero counterexample, and not a final physical shell
  theorem.
  It is the sharpest current selector-level reduction of the remaining
  checked-local membrane-difference gap.
- Next action:
  prove or refute that the exact admissible residual-generated checked-local
  pair domain meets each equal-trace membrane quotient class only in the
  repo-selected representative, equivalently that
  `sigma_chk,n(q; c_sel)(z) = 0` on all of `D_sigma,n(q; c_sel)`.

### V-S32. `T3n` implementation: selector vanishing is exactly patchwise membrane constancy on the admissible checked-local pair domain

- ID: `V-S32`
- Claim / Hypothesis:
  For fixed clean `(n, q)` and fixed repo-selected basepoint `c_sel`:
  1. uniqueness is tested on the exact checked-local definability subdomain
     `D_sigma,n(q; c_sel) := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
     (c_sel + z, c_sel) in Pair_chk,n(q) }`, not on the whole residual space by
     default;
  2. on this domain, uniqueness in the equal-trace membrane quotient class is
     equivalent to vanishing of
     `sigma_chk,n(q; c_sel)(z)`;
  3. on every common corrected-chart patch `D_sigma^U,n(q; c_sel)`, there is a
     local membrane coordinate `s_U` such that
     `sigma_chk,n(q; c_sel)(z) = s_U(z) - s_U(0)`;
  4. therefore selector vanishing is exactly equivalent to patchwise constancy
     of the local membrane coordinate on the exact admissible residual-
     generated checked-local pair patches;
  5. the current theorem-facing candidate/admissibility structure still forces
     only the quotient coordinates `(a, b)` and does not yet force that
     constancy;
  6. any patch containing one point with `s_U(z) != s_U(0)` yields an exact
     nonvanishing template for `sigma_chk`.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `Outcome B: the remaining selector-vanishing question is now reduced to an exact patchwise membrane-constancy / uniqueness-in-class obstruction theorem`
- What counts as verification:
  a clean `T3n` package that explicitly records:
  the exact uniqueness domain,
  the equivalence between uniqueness-in-class and selector vanishing,
  the local-coboundary formula `sigma_chk = s_U - s_U(0)`,
  and the exact obstruction that current theorem-facing constraints still do
  not force constancy of `s_U`.
- Verification method:
  CAS, code inspection, manual derivation.
- Verification boundary:
  this is not yet full `T3`, not a vanishing theorem on the full exact domain,
  not an explicit admissible nonzero counterexample, and not a final physical
  shell theorem.
  It is the sharpest current reduction of the membrane-selector problem to an
  exact local constancy question on the checked-local admissible pair patches.
- Next action:
  prove or refute patchwise constancy of the local membrane coordinate on every
  exact admissible residual-generated checked-local pair patch, equivalently
  prove or refute that `sigma_chk,n(q; c_sel)(z) = 0` on all of
  `D_sigma,n(q; c_sel)`.

### V-S33. `T3o` implementation: overlap compatibility is automatic, so the only remaining issue is patchwise membrane constancy itself

- ID: `V-S33`
- Claim / Hypothesis:
  For fixed clean `(n, q)` and fixed repo-selected basepoint `c_sel`:
  1. the exact admissible residual-generated checked-local patches are
     `D_sigma^U,n(q; c_sel) subseteq D_sigma,n(q; c_sel)`, where a common
     corrected chart `U` represents both `c_sel + z` and `c_sel`;
  2. on every such patch,
     `sigma_chk,n(q; c_sel)(z) = s_U(z) - s_U(0)`;
  3. if two quotient-preserving corrected charts `U, V` overlap on the same
     fixed equal-trace class, then
     `s_V(z) = s_U(z) - ell1 a_sel - ell2 b_sel`
     for constants `ell1, ell2` coming from the chart transition and fixed
     trace coordinates `(a_sel, b_sel)` of the class;
  4. therefore constancy of the local membrane coordinate is automatically
     equivalent across overlaps, and global vanishing of `sigma_chk` is
     equivalent to patchwise constancy on any exact admissible residual-
     generated patch cover;
  5. the only remaining obstruction is now patchwise nonconstancy itself, not
     overlap/gluing compatibility.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `Outcome B: overlap compatibility is now closed as automatic, but patchwise constancy of the local membrane coordinate is still open`
- What counts as verification:
  a clean `T3o` package that explicitly records:
  the exact patch family `D_sigma^U,n(q; c_sel)`,
  the local-coboundary formula on each patch,
  the constant-shift overlap law under quotient-preserving chart changes,
  and the reduction of the remaining question to patchwise constancy itself.
- Verification method:
  CAS, code inspection, manual derivation.
- Verification boundary:
  this is not yet full `T3`, not a global vanishing theorem on the full exact
  domain, not an explicit admissible nonconstant patch, and not a final
  physical shell theorem.
  It is the sharpest current reduction of the selector problem after removing
  overlap/gluing as an independent bottleneck.
- Next action:
  prove or refute constancy of `s_U` on the full exact admissible residual-
  generated checked-local patch cover, equivalently prove or refute that
  `sigma_chk,n(q; c_sel)(z) = 0` on all of `D_sigma,n(q; c_sel)`.

### V-S34. `T3p` implementation: the remaining issue is singletonity of the exact patch image inside the fixed membrane fiber

- ID: `V-S34`
- Claim / Hypothesis:
  For fixed clean `(n, q)` and fixed repo-selected basepoint `c_sel`:
  1. for every exact admissible residual-generated checked-local patch
     `D_sigma^U,n(q; c_sel)`, the checked-local image
     `Im_chk,U,n(q; c_sel)
      := { chi_chk,U,n(q)(c_sel + z) : z in D_sigma^U,n(q; c_sel) }`
     satisfies
     `Im_chk,U,n(q; c_sel) subseteq { (a_sel, b_sel, s)^T : s in R }`;
  2. equivalently the patch carries a membrane-fiber image
     `S_U,n(q; c_sel) := { s_U(z) : z in D_sigma^U,n(q; c_sel) }`;
  3. patchwise constancy of `s_U`, vanishing of `sigma_chk` on the patch, and
     singletonity of `Im_chk,U` / `S_U` are exact equivalent formulations;
  4. by the already closed `T3o` overlap law, singletonity is cover-invariant;
  5. current theorem-facing constraints still determine only the quotient base
     point `(a_sel, b_sel)`, so they currently prove only fiber containment and
     not fiber singletonity.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `Outcome B: the remaining selector question is reduced to the singletonity of the exact checked-local patch image in the fixed membrane fiber, but singletonity is not yet proved`
- What counts as verification:
  a clean `T3p` package that explicitly records:
  the exact checked-local patch image `Im_chk,U`,
  the membrane-fiber image `S_U`,
  the equivalence between selector vanishing, patchwise constancy, and
  singletonity,
  and the exact obstruction that current theorem-facing constraints still force
  only fiber containment.
- Verification method:
  CAS, code inspection, manual derivation.
- Verification boundary:
  this is not yet full `T3`, not a constancy theorem on the full exact domain,
  not an explicit admissible nonsingleton patch, and not a final physical shell
  theorem.
  It is the sharpest current reduction after `T3o`: the unresolved freedom is
  now isolated as a possible nonsingleton subset of the fixed membrane fiber on
  each exact patch.
- Next action:
  prove or refute that the membrane-fiber image is a singleton on every exact
  admissible residual-generated checked-local patch, equivalently prove or
  refute that `sigma_chk,n(q; c_sel)(z) = 0` on all of
  `D_sigma,n(q; c_sel)`.


### V-S35. T3q implementation: current theorem-facing constraints remain quotient-final on the exact patches, so singletonity is equivalent to one missing representative law inside the fixed membrane fiber

- ID: V-S35
- Claim / Hypothesis:
  For fixed clean (n, q) and fixed repo-selected basepoint c_sel:
  1. on every exact admissible residual-generated checked-local patch
     D_sigma^U,n(q; c_sel), singletonity of Im_chk,U,n(q; c_sel) in the
     fixed membrane fiber is exactly equivalent to one patchwise
     representative law Rep_U,n(q; c_sel);
  2. Rep_U, vanishing of sigma_chk on that patch, constancy of s_U on
     that patch, and singletonity of S_U are exact equivalent formulations;
  3. all currently justified checked-local invariants on the present checked
     boundary still factor through the quotient map (a, b, s) -> (a, b) or
     are blind along the membrane line;
  4. therefore current theorem-facing constraints still force only fiber
     containment and do not force singletonity by themselves;
  5. the exact missing ingredient is now one representative-sensitive law on
     the exact admissible patch domain, not another quotient-final theorem.
- Type: structural claim
- Source file(s):
  docs/theory/current_simple_support_theorem_roadmap.md;
  proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md;
  proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md.
- Current status: Outcome B: singletonity is still open, but the remaining gap is now isolated as one missing representative law inside the fixed membrane fiber on each exact patch
- What counts as verification:
  a clean T3q package that explicitly records:
  the patchwise representative law Rep_U,
  the equivalence between Rep_U, selector vanishing, patchwise constancy,
  and membrane-fiber singletonity,
  the exact quotient-finality obstruction,
  and the sharpened next bottleneck as a representative-sensitive theorem.
- Verification method:
  CAS, code inspection, manual derivation.
- Verification boundary:
  this is not yet full T3, not a singletonity theorem on the full exact
  domain, not an explicit admissible non-singleton realization, and not a
  final physical shell theorem.
  It is the sharpest current reduction after T3p: the unresolved gap is no
  longer just "prove singletonity", but "derive one representative-sensitive
  law that is not already contained in the quotient-final checked-local
  package".
- Next action:
  prove or refute the patchwise representative law Rep_U,n(q; c_sel) on
  every exact admissible residual-generated checked-local patch, equivalently
  prove or refute singletonity of the exact checked-local patch image in the
  fixed membrane fiber, equivalently prove or refute that
  sigma_chk,n(q; c_sel)(z) = 0 on all of D_sigma,n(q; c_sel).

### V-S36. `T3r` implementation: the patchwise representative law reduces exactly to one pointwise basepoint-relative membrane-deviation law on each exact patch

- ID: `V-S36`
- Claim / Hypothesis:
  For fixed clean `(n, q)` and fixed repo-selected basepoint `c_sel`:
  1. on every exact admissible residual-generated checked-local patch
     `D_sigma^U,n(q; c_sel)`, the pairwise representative law
     `Rep_U,n(q; c_sel)` is exactly equivalent to the pointwise basepoint law
     `chi_chk,U,n(q)(c_sel + z) = chi_chk,U,n(q)(c_sel)` for every `z` on that
     patch;
  2. equivalently the pointwise basepoint-relative representative difference
     `Delta_rep,U^pt,n(q; c_sel)(z)
      := chi_chk,U,n(q)(c_sel + z) - chi_chk,U,n(q)(c_sel)`
     satisfies
     `Delta_rep,U^pt = sigma_chk e_mem` and takes values in `span(e_mem)`;
  3. current theorem-facing admissibility / candidate constraints still force
     only the fixed quotient coordinates `(a_sel, b_sel)` and therefore only
     `Delta_rep,U^pt(z) in span(e_mem)`, not its vanishing;
  4. failure of `Rep_U` on an exact patch is therefore exactly equivalent to
     existence of one patch point `z_*` with
     `Delta_rep,U^pt,n(q; c_sel)(z_*) != 0`,
     equivalently `sigma_chk,n(q; c_sel)(z_*) != 0`;
  5. the exact remaining bottleneck is now one pointwise vanishing theorem on
     the full exact admissible patch cover, not another quotient-final theorem.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `Outcome B: the patchwise representative law is still open, but it is now reduced exactly to pointwise vanishing of the basepoint-relative membrane deviation on each exact patch`
- What counts as verification:
  a clean `T3r` package that explicitly records:
  the pointwise basepoint-relative representative difference `Delta_rep,U^pt`,
  the equivalence between `Rep_U`, pointwise basepoint vanishing,
  selector vanishing, and singletonity,
  the exact obstruction that current theorem-facing constraints still force
  only membrane-line containment of that difference,
  and the sharpened one-point nonvanishing template.
- Verification method:
  CAS, code inspection, manual derivation.
- Verification boundary:
  this is not yet full `T3`, not a representative-law theorem on the full exact
  domain, not an explicit admissible nonzero realization, and not a final
  physical shell theorem.
  It is the sharpest current reduction after `T3q`: the unresolved gap is now
  not merely pairwise equality on a patch, but pointwise vanishing of the exact
  basepoint-relative membrane deviation.
- Next action:
  prove or refute the pointwise basepoint-relative law
  `chi_chk,U,n(q)(c_sel + z) = chi_chk,U,n(q)(c_sel)` on every exact
  admissible residual-generated checked-local patch, equivalently prove or
  refute that `sigma_chk,n(q; c_sel)(z) = 0` on all of
  `D_sigma,n(q; c_sel)`.


### V-S37. `T3s` implementation: the patchwise pointwise membrane-deviation law descends to a chart-invariant exact global pointwise defect map on `D_sigma`

- ID: `V-S37`
- Claim / Hypothesis:
  For fixed clean `(n, q)` and fixed repo-selected basepoint `c_sel`:
  1. the patchwise pointwise-difference objects
     `Delta_rep,U^pt,n(q; c_sel)(z)` glue on overlaps and define one exact
     chart-invariant map
     `Delta_rep^pt,n(q; c_sel) : D_sigma,n(q; c_sel) -> span(e_mem)`;
  2. for every `z in D_sigma,n(q; c_sel)` one has
     `Delta_rep^pt,n(q; c_sel)(z) = sigma_chk,n(q; c_sel)(z) e_mem` and
     `Delta_rep^pt,n(q; c_sel)(0) = 0`;
  3. global pointwise vanishing of `Delta_rep^pt` on `D_sigma,n(q; c_sel)` is
     exactly equivalent to global vanishing of `sigma_chk`, to `Rep_U` on every
     exact patch, and to patchwise constancy / singletonity on every exact
     admissible residual-generated checked-local patch;
  4. current theorem-facing admissibility / candidate constraints still force
     only codomain containment in `span(e_mem)` plus the basepoint
     normalization at `0`, not vanishing at an arbitrary point;
  5. the remaining obstruction is now the exact pointwise nonzero set
     `N_sigma,n(q; c_sel)
      := { z in D_sigma,n(q; c_sel) :
           Delta_rep^pt,n(q; c_sel)(z) != 0 }`.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `Outcome B: the pointwise law is still open, but it is now packaged as a chart-invariant exact global defect map whose nonzero set is the remaining obstruction`
- What counts as verification:
  a clean `T3s` package that explicitly records:
  the descent `Delta_rep,U^pt -> Delta_rep^pt`,
  the identity `Delta_rep^pt = sigma_chk e_mem`,
  the exact equivalence with `Rep_U` / singletonity / constancy,
  the codomain-plus-normalization obstruction theorem,
  and the exact nonzero-set formulation.
- Verification method:
  CAS, code inspection, manual derivation.
- Verification boundary:
  this is not yet full `T3`, not a global vanishing theorem on the full exact
  domain, not an explicit admissible nonzero realization, and not a final
  physical shell theorem.
  It is the sharpest current reduction after `T3r`: the unresolved gap is now
  not merely patchwise pointwise equality, but emptiness of one exact chart-
  invariant global pointwise nonzero set on `D_sigma,n(q; c_sel)`.
- Next action:
  prove or refute that `N_sigma,n(q; c_sel) = emptyset`, equivalently prove or
  refute that `Delta_rep^pt,n(q; c_sel)(z) = 0` for every
  `z in D_sigma,n(q; c_sel)`.

### V-S38. `T3t` implementation: emptiness of the exact global nonzero defect set is equivalent to collapse of one scalar defect image on `D_sigma`

- ID: `V-S38`
- Claim / Hypothesis:
  For fixed clean `(n, q)` and fixed repo-selected basepoint `c_sel`:
  1. on the exact admissible residual-generated domain `D_sigma,n(q; c_sel)`,
     the chart-invariant global pointwise defect map `Delta_rep^pt,n(q; c_sel)`
     determines the exact nonzero set
     `N_sigma,n(q; c_sel)
      := { z in D_sigma,n(q; c_sel) :
           Delta_rep^pt,n(q; c_sel)(z) != 0 }`;
  2. the same exact data determine the scalar defect image
     `Sigma_sigma,n(q; c_sel)
      := { sigma_chk,n(q; c_sel)(z) : z in D_sigma,n(q; c_sel) }`;
  3. emptiness of `N_sigma,n(q; c_sel)` is exactly equivalent to collapse of
     that image to `{0}`;
  4. pairwise representative-sensitive differences factor through scalar defect
     value differences;
  5. current theorem-facing admissibility / candidate constraints still force
     only `0 in Sigma_sigma,n(q; c_sel)`, not `Sigma_sigma,n(q; c_sel) = {0}`.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `Outcome B: emptiness of the defect set is still open, but it is now reduced further to the exact scalar defect-image collapse condition on the same full exact domain`
- What counts as verification:
  a clean `T3t` package that explicitly records:
  the exact defect set `N_sigma`;
  the exact scalar defect image `Sigma_sigma`;
  the equivalence `N_sigma = emptyset` iff `Sigma_sigma = {0}`;
  the pairwise factorization through scalar defect-value differences;
  and the exact obstruction that current theorem-facing constraints still force
  only `0 in Sigma_sigma`.
- Verification method:
  CAS, code inspection, manual derivation.
- Verification boundary:
  this is not yet full `T3`, not an emptiness theorem on the full exact domain,
  not an explicit admissible nonzero realization, and not a final physical
  shell theorem.
  It is the sharpest current reduction after `T3s`: the unresolved gap is now
  not merely global vanishing of a defect map, but collapse of its exact scalar
  image to `{0}`, equivalently emptiness of the exact nonzero defect set.
- Next action:
  prove or refute that `Sigma_sigma,n(q; c_sel) = {0}`, equivalently prove or
  refute that `N_sigma,n(q; c_sel) = emptyset` on the full exact domain
  `D_sigma,n(q; c_sel)`.

### V-S39. `T3u` implementation: scalar-image collapse is equivalent to vanishing of the exact pairwise scalar-difference image on the admissible exact pair domain

- ID: `V-S39`
- Claim / Hypothesis:
  For fixed clean `(n, q)` and fixed repo-selected basepoint `c_sel`:
  1. the exact scalar selector `sigma_chk,n(q; c_sel)` on
     `D_sigma,n(q; c_sel)` determines the exact scalar image `Sigma_sigma`, the
     exact defect set `N_sigma`, and the exact pairwise scalar-difference image
     `Omega_sigma,n(q; c_sel)`;
  2. scalar-image collapse is exactly equivalent to vanishing of that pairwise
     scalar-difference image:
     `Sigma_sigma,n(q; c_sel) = {0}` iff `Omega_sigma,n(q; c_sel) = {0}`;
  3. all surviving exact pairwise representative-sensitive differences factor
     through `Omega_sigma e_mem`;
  4. the scalar cocycle package gives normalization at `0`, antisymmetry, and
     additivity where the exact admissible pairs compose;
  5. current theorem-facing admissibility / candidate constraints still force
     only that scalar cocycle package, not `Omega_sigma = {0}`.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `Outcome B: scalar-image collapse is still open, but it is now reduced further to vanishing of the exact pairwise scalar-difference image on the same exact admissible pair domain`
- What counts as verification:
  a clean `T3u` package that explicitly records:
  the scalar selector `sigma_chk` on `D_sigma`;
  the exact scalar image `Sigma_sigma`;
  the exact defect set `N_sigma`;
  the exact pairwise scalar-difference image `Omega_sigma`;
  the equivalence `Sigma_sigma = {0}` iff `Omega_sigma = {0}`;
  and the exact obstruction that current theorem-facing constraints still force
  only the scalar cocycle package.
- Verification method:
  CAS, code inspection, manual derivation.
- Verification boundary:
  this is not yet full `T3`, not a scalar-image collapse theorem on the full
  exact domain, not an explicit admissible nonzero-scalar realization, and not
  a final physical shell theorem.
  It is the sharpest current reduction after `T3t`: the unresolved gap is now
  not merely collapse of the scalar image, but vanishing of the exact pairwise
  scalar-difference image that governs all surviving representative-sensitive
  pairwise differences.
- Next action:
  prove or refute that `Omega_sigma,n(q; c_sel) = {0}`, equivalently prove or
  refute that `Sigma_sigma,n(q; c_sel) = {0}` on the full exact admissible pair
  domain.
### V-S40. `T3v` implementation: pairwise scalar-difference collapse is still open, but the exact missing ingredient is now one representative-sensitive rigidity law on the admissible pair domain

- ID: `V-S40`
- Claim / Hypothesis:
  For fixed clean `(n, q)` and fixed repo-selected basepoint `c_sel`:
  1. define the exact admissible pair domain
     `Pair_sigma,n(q; c_sel)
      := { (z_1, z_2) in D_sigma,n(q; c_sel)^2 :
           (c_sel + z_1, c_sel + z_2) in Pair_chk,n(q) }`;
  2. define the exact pairwise scalar-difference image
     `Omega_sigma,n(q; c_sel)
      := { sigma_chk,n(q; c_sel)(z_1) - sigma_chk,n(q; c_sel)(z_2) :
           (z_1, z_2) in Pair_sigma,n(q; c_sel) }`;
  3. then `Omega_sigma` is chart-invariant and satisfies the exact inclusions
     `Sigma_sigma,n(q; c_sel) subseteq Omega_sigma,n(q; c_sel)
      subseteq Sigma_sigma,n(q; c_sel) - Sigma_sigma,n(q; c_sel)`;
  4. pairwise scalar-difference collapse is therefore exactly equivalent to
     scalar-image collapse, defect-set emptiness, selector vanishing, global
     pointwise-defect vanishing, and `Rep_U` on every exact patch;
  5. current theorem-facing admissibility / candidate constraints remain
     quotient-final on the checked boundary: they fix the quotient coordinates
     `(a_sel, b_sel)` and the scalar cocycle package, but do not force equality
     of membrane coordinates inside the fixed quotient fiber;
  6. so the exact remaining missing ingredient is one representative-sensitive
     rigidity law forbidding an exact admissible pair
     `(z_1, z_2) in Pair_sigma,n(q; c_sel)` with
     `chi_chk,chart(c_sel + z_i) = (a_sel, b_sel, s_i)^T` and `s_1 != s_2`.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `Outcome B: pairwise scalar-difference collapse is still open, but the exact missing ingredient is now isolated as one representative-sensitive rigidity law on the full exact admissible pair domain`
- What counts as verification:
  a clean `T3v` package that explicitly records:
  the exact pair domain `Pair_sigma`;
  the exact pairwise scalar-difference image `Omega_sigma`;
  the sharp relation `Sigma_sigma subseteq Omega_sigma subseteq Sigma_sigma - Sigma_sigma`;
  the equivalence between collapse of `Omega_sigma` and collapse of `Sigma_sigma`;
  and the exact obstruction that current theorem-facing constraints still do not
  force equality of membrane representatives inside the fixed quotient fiber.
- Verification method:
  manual derivation, CAS, code inspection.
- Verification boundary:
  this is not yet full `T3`, not a pairwise-collapse theorem on the full exact
  domain, not an explicit admissible nonzero-pair realization, and not a final
  physical shell theorem.
  It is the sharpest current reduction after `T3u`: the unresolved gap is now
  not merely vanishing of one exact pairwise scalar-difference image, but one
  specific representative-sensitive rigidity law invisible to the current
  quotient-final constraints.
- Next action:
  prove or refute that there do not exist exact admissible pair data
  `(z_1, z_2) in Pair_sigma,n(q; c_sel)` with the same quotient coordinates
  `(a_sel, b_sel)` and different membrane coordinates `s_1 != s_2`,
  equivalently prove or refute that `Omega_sigma,n(q; c_sel) = {0}` on the full
  exact admissible pair domain.

### V-S41. Admissible-lift branch: no nonzero same-trace admissible lift can live inside the global selected full-center lift `X_sel`

- ID: `V-S41`
- Claim / Hypothesis:
  For fixed clean `(n, q)`, let
  `X_sel,n(q) := im(P_sel,n(q))` with `C_center,n(q) P_sel,n(q) = I_4`.
  Then:
  1. the restricted map `C_center|_(X_sel,n(q)) : X_sel,n(q) -> R^4` is
     bijective, with inverse `P_sel,n(q)`;
  2. for every repo-selected basepoint `c_sel in A_sel^repo,n(q) = A_ls,n(q)`,
     the selected-architecture lift class
     `Lift_mem^sel,n(q; c_sel)
      := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
           c_sel + z in X_sel,n(q),
           (c_sel + z, c_sel) in Pair_chk,n(q) }`
     satisfies
     `Lift_mem^sel,n(q; c_sel) = {0}`;
  3. equivalently,
     `A_sel^{th,cand},n(q) intersect X_sel,n(q) = A_ls,n(q)`.
  So any nonzero admissible global lift of the local membrane mode, if it
  exists at all, must lie outside the current KKT-selected full-center lift.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `docs/theory/vyvod_uravneniy_updated17.md` section 1.10.9;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `closed enough on the selected-architecture obstruction layer`
- What counts as verification:
  explicit use of the exact identity `C_center P_sel = I_4`, the definition
  `X_sel = im(P_sel)`, the same-trace condition `z in ker(C_center)`, and the
  candidate-class trace condition `J_0(c) in im(D_amp)`.
- Verification method:
  manual derivation, code inspection, theorem reuse from the selected-lift
  package.
- Verification boundary:
  this does not yet prove that the full admissible lift class is empty inside
  all of `A_adm^th,n(q)`. It proves only that no nonzero same-trace admissible
  lift can occur inside the current global selected full-center lift `X_sel`.
- Next action:
  decide whether there exist candidate-class points in
  `A_sel^{th,cand},n(q) \ X_sel,n(q)` whose same-trace residual is still
  checked-local pair-definable and membrane-visible.
### V-S42. Extrinsic admissible-lift branch: after the `X_sel` obstruction, extrinsicness is automatic for every nonzero same-trace residual, so the true missing input is a residual-fiber pair-definability / membrane-visibility theorem

- ID: `V-S42`
- Claim / Hypothesis:
  For fixed clean `(n, q)`, one has the exact intersection law
  `X_sel,n(q) intersect ker(C_center,n(q)) = {0}`.
  Hence for every repo-selected basepoint `c_sel in A_ls,n(q) subset X_sel,n(q)`
  and every nonzero residual direction
  `0 != z in A_adm^th,n(q) intersect ker(C_center,n(q))`,
  one automatically has `c_sel + z notin X_sel,n(q)`.
  Therefore the extrinsic admissible-lift question is no longer an `X_sel`
  question at all: it is exactly whether the residual fiber
  `A_adm^th,n(q) intersect ker(C_center,n(q))` contains a nonzero direction that
  is checked-local pair-definable with `c_sel` and carries nonzero
  representative-sensitive membrane deviation.
- Type: `structural claim`
- Source file(s):
  `docs/theory/current_simple_support_theorem_roadmap.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `closed enough as a residual-fiber reduction / blocking-condition statement`
- What counts as verification:
  explicit use of `C_center P_sel = I_4`, the identity `X_sel = im(P_sel)`, the
  same-trace condition `z in ker(C_center)`, and the already closed inclusion
  `A_ls subset X_sel`.
- Verification method:
  manual derivation, code inspection, theorem reuse from the selected-lift package.
- Verification boundary:
  this does not yet construct an extrinsic admissible lift and does not yet
  prove that none exists in all of `A_adm^th,n(q) intersect ker(C_center,n(q))`.
  It removes only one remaining false degree of freedom: outside-`X_sel` is now
  automatic for every nonzero same-trace residual, so the true missing input is
  a global-to-local theorem deciding pair-definability and membrane visibility
  on the residual fiber itself.
- Next action:
  derive an exact coefficient-level or operator-level criterion on
  `A_adm^th,n(q) intersect ker(C_center,n(q))` that decides which nonzero
  residual directions are checked-local pair-definable with `c_sel` and whether
  they produce nonzero membrane deviation.
### V-S43. Residual-fiber branch: any checked-local membrane-visible candidate residual must satisfy the exact augmented membrane-nullmode equations

- ID: `V-S43`
- Claim / Hypothesis:
  Under the same checked local nonresonance regime already used in pilot 23,
  let
  `R_res,n(q) := A_adm^th,n(q) intersect ker(C_center,n(q))`.
  If
  `0 != z in R_res,n(q)`
  satisfies `(c_sel + z, c_sel) in Pair_chk,n(q)` and carries nonzero
  representative-sensitive membrane deviation, then in any common coefficient-
  faithful augmented corrected checked-local chart its residual jet lies in
  `span(g_mem^aug,n(q))`, where
  `g_mem^aug,n(q) = [0,0,0,0,alpha,0,0,0,beta,1]`.
  Equivalently the first checked nontrivial augmented coefficients obey
  `U1 = alpha T1`, `V1 = beta T1`, `N1 = P1 = Y1 = 0`, with `T1 != 0`, and the
  checked next layer closes uniquely to zero.
- Type: `formula-level claim`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` sections 1.10.13-1.10.14;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `closed enough as a necessary low-order obstruction on the residual fiber`
- What counts as verification:
  explicit reuse of the local first post-leading membrane-nullmode formulas,
  the coefficient-faithful augmented membrane vector `g_mem^aug`, the checked
  next-layer closure, and the same-trace / pair-definability interpretation on
  the residual fiber.
- Verification method:
  manual derivation, CAS/theory reuse from pilot 23, code inspection.
- Verification boundary:
  this does not yet construct a nonzero residual-fiber lift and does not yet
  prove that none exists globally. It proves only that any such candidate must
  satisfy one explicit low-order membrane-nullmode equation family, so the true
  remaining missing input is a global coefficient-extraction theorem on
  `R_res,n(q)` deciding whether that local jet is realized.
- Next action:
  derive an exact residual-fiber coefficient extractor or equivalent operator-
  level criterion deciding when `z in R_res,n(q)` has augmented checked-local
  jet in `span(g_mem^aug,n(q))`.
### V-S44. Residual-fiber branch: the current weighted trial ansatz explicitly realizes the membrane-nullmode jet on `ker(C_center)`

- ID: `V-S44`
- Claim / Hypothesis:
  On the current clean weighted-ansatz repository boundary, let `L := 1 - x0`
  and fix `s_mem != 0`. Define a trial coefficient vector with only
  `u_s,k=1,2`, `v,k=1,2`, and `T_s,k=1,2` nonzero,
  equal respectively to
  `(-L alpha s_mem, -(L^2/x0) alpha s_mem)`,
  `(-L beta s_mem,  -(L^2/x0) beta s_mem)`,
  `(-L s_mem,       -(L^2/x0) s_mem)`.
  Then this vector lies in `ker(C_center,n(q))` and its extracted low-order
  center jet is exactly `s_mem g_mem^aug,n(q)`.
- Type: `formula-level claim`
- Source file(s):
  `src/shell_buckling/mixed_weak/solver_patched_core.py`;
  `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`;
  `docs/theory/vyvod_uravneniy_updated17.md` sections 1.10.13-1.10.14;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `closed enough on the current weighted-ansatz repository boundary`
- What counts as verification:
  explicit use of the basis form `x^p t^k`, the exact center map `C_center`, and
  direct coefficient expansion showing the leading local jet equals
  `s_mem g_mem^aug,n(q)`.
- Verification method:
  manual derivation, code inspection.
- Verification boundary:
  this is a current weighted-ansatz / repository-boundary realization result. It
  does not yet prove the full continuum theorem that an exact admissible nonzero
  membrane-visible lift exists in all of `A_adm^th,n(q)`.
- Next action:
  decide whether the theorem-facing admissible / pair-definable class upgrades
  this explicit weighted-ansatz template into a true exact admissible lift, or
  whether an additional admissibility theorem blocks that upgrade.
### V-S45. Explicit weighted-ansatz membrane template: the remaining extension failure is exactly the admissibility / `Pair_chk` upgrade

- ID: `V-S45`
- Claim / Hypothesis:
  Keep the explicit weighted-ansatz residual template `z_temp,n(q; s_mem)` with
  `s_mem != 0`. On the current exact repository boundary, the extension attempt
  to a genuine admissible checked-local lift fails exactly at the theorem-facing
  admissibility / shadow upgrade: the repository does not yet promote this
  explicit weighted trial vector to an independently closed element of
  `A_adm^th,n(q)`, and does not yet package a checked-local shadow theorem strong
  enough to conclude `(c_sel + z_temp, c_sel) in Pair_chk,n(q)`.
  Conditional on such a shadow upgrade, the final membrane deviation would be
  nonzero rather than zero, because the visible membrane generator is the `U1`
  direction and the template has `U1 = alpha s_mem` with `alpha != 0` on the
  physical clean regime already checked in pilot 23.
- Type: `structural/formal claim`
- Source file(s):
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`.
- Current status: `closed enough on the present repository boundary`
- Interpretation:
  this is the object-closure boundary at which the older `T3...` style chain
  saturates on the present clean repository boundary; the current criterion is
  still not theorem-facing enough to exclude the explicit membrane candidate.
- What counts as verification:
  explicit use of the already closed template existence on `X_trial intersect ker(C_center)`,
  the pilot-23 statement that `A_full^th` is not yet an independently closed
  continuum object on the repository boundary, the current absence of a global
  checked-local shadow theorem on raw residuals, and the nonvanishing of the
  visible membrane coefficient `U1 = alpha s_mem` in the physical regime.
- Verification method:
  manual derivation, code inspection, pilot/theory cross-read.
- Verification boundary:
  this is not a proof that the explicit template is impossible in the full
  continuum admissible problem. It is a proof that the current exact repository
  boundary does not yet extend it past the admissibility / `Pair_chk` upgrade.
- Next action:
  keep this entry as the authoritative claim-registry endpoint of the frozen
  line, but do not replay the full frozen narrative here.
  Use:
  `docs/theory/current_simple_support_object_glossary.md`
  for stable object definitions,
  `docs/theory/current_simple_support_final_audit_note.md`
  for the frozen-line conclusion, and
  `docs/theory/current_simple_support_closed_line_index.md`
  for the archive/index reading.
  Any future theorem return on this topic should bring genuinely new continuum
  / equation-level admissibility input aimed directly at the frozen
  residual-direction boundary
  `z_temp in A_adm^th,n(q) intersect ker(C_center,n(q)) ?`,
  rather than continue the old chain by reformulation.

### V-S46. Selection-rule authority for the current reduced family remains open

- ID: `V-S46`
- Claim / Hypothesis:
  On the present clean full simple-support branch, the current repo-selected
  reduced family `A_ls = im(V_adm) = im(M_amp)` should be treated as
  selection-rule-dependent rather than criterion-authoritative. Representation-
  only changes of one fixed family are mostly washed out by canonical rebasing,
  but nearby changes of the actual selector (for example Tikhonov `reg` or SVD
  truncation) can move the chosen span and the resulting `n=7` / `n=8` stacked
  reading materially while preserving the clean identities
  `C_amp V_adm ~= I` and `C_reg V_adm ~= 0`. So the current bottleneck is the
  unresolved authority of the selected-family rule itself, not only metric
  choice on one fixed selected family.
- Type: `interpretation claim`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `tasks/run_simple_support_selected_family_sensitivity.py`;
  `tasks/run_simple_support_selection_rule_audit.py`;
  `output/clean_full_simple_support/selected_family_sensitivity_summary.json`;
  `output/clean_full_simple_support/selection_rule_audit_summary.json`.
- Current status: `open bottleneck / negative authority conclusion recorded`
- What counts as verification:
  explicit evidence that representation variants leave the rebased selected-
  family reading nearly unchanged, while nearby selector variants produce
  materially different projectors and `n=7` / `n=8` readouts on the delicate
  settings without breaking the clean center/rebasing identities.
- Verification method:
  numerical audit, code inspection, manual theory/status synthesis.
- Verification boundary:
  this is not a proof that no canonical selector exists. It records only that
  the current Tikhonov rule is too recipe-sensitive for criterion authority and
  that the present truncated-SVD alternative is still cutoff-dependent enough
  that it should not yet be promoted.
- Next action:
  derive a theorem-facing canonical selector, or prove that criterion authority
  can be formulated without privileging one nearby selected-family recipe.

### V-S47. Criterion-authoritative selector requirements are explicit, but no checked selector currently satisfies them

- ID: `V-S47`
- Claim / Hypothesis:
  On the present clean full simple-support branch, a selector should be treated
  as criterion-authoritative only if it satisfies four kinds of requirements:
  structural/invariance requirements, numerical robustness requirements,
  theorem-facing authority requirements, and compatibility with the current
  `L_red -> B_red -> B_mix` object hierarchy. Convenience-only properties such
  as small rebasing residuals, moderate `cond(G_amp)`, or one calm local window
  are not sufficient by themselves. On the current checked repository boundary,
  the Tikhonov selector fails the small-`reg` robustness / theorem-authority
  requirements, the truncated-SVD alternative fails cutoff-independence /
  theorem-authority requirements, and canonical rebasing is only a
  post-selection normalization step.
- Type: `interpretation claim`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `output/clean_full_simple_support/selected_family_sensitivity_summary.json`;
  `output/clean_full_simple_support/selection_rule_audit_summary.json`.
- Current status: `requirements explicit / no closed selector yet`
- What counts as verification:
  an explicit source-of-truth requirement list together with numerical evidence
  that representation-only changes are mostly washed out, while nearby selector
  changes can still move the selected span and the delicate `n=7` / `n=8`
  readout materially.
- Verification method:
  numerical audit, code inspection, manual theory/status synthesis.
- Verification boundary:
  this does not prove that no canonical selector exists. It records only the
  present requirement list and the negative conclusion that no currently checked
  selector satisfies it well enough for criterion authority.
- Next action:
  either derive a theorem-facing selector meeting these requirements, or show
  that criterion authority can be formulated without promoting one selector to a
  privileged theorem-facing role.

### V-S48. Candidate theorem-facing selector principles are now explicit, but no selector principle is yet closed

- ID: `V-S48`
- Claim / Hypothesis:
  On the present clean full simple-support branch, the plausible theorem-facing
  selector-principle candidates now on the table are:
  a genuine weak/KKT-selected global family principle, a local-to-global
  selected-family principle, a trace-plane-first principle, a genuinely
  variational/minimal-energy selector principle, and the conservative fallback
  position `no justified selector yet`. Of these, the weak/KKT and
  local-to-global routes are the most structurally compatible with the present
  repo evidence, the trace-plane-first route is at best a partial ingredient,
  the variational/minimal-energy route is currently unsupported, and no
  selector principle is yet closed strongly enough to license a privileged
  selected family.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `output/clean_full_simple_support/selected_family_sensitivity_summary.json`;
  `output/clean_full_simple_support/selection_rule_audit_summary.json`.
- Current status: `candidate principles enumerated / none closed`
- What counts as verification:
  an explicit source-of-truth comparison showing, for each candidate principle,
  what privileged object it would single out, what current repo evidence
  supports it, what evidence does not yet support it, and what next theorem or
  status step would still be required.
- Verification method:
  numerical audit reuse, code inspection, manual theory/status synthesis.
- Verification boundary:
  this does not prove that any of these selector principles is correct. It only
  records the current theorem/status menu and the present evidence-based
  classification of those options.
- Next action:
  decide whether the next theorem-facing program should target the weak/KKT
  route, the local-to-global route, a new genuine variational route, or remain
  temporarily on the conservative `no justified selector yet` position.

### V-S49. Genuine weak/KKT selector principle is now formulated as a theorem-facing target, while the current Tikhonov rule remains only a surrogate

- ID: `V-S49`
- Claim / Hypothesis:
  On the present clean full simple-support branch, the current live
  Tikhonov/KKT-like selector should be read only as a numerical surrogate for a
  possible theorem-facing weak/interior selector route. The live surrogate
  solves
  `min ||A_int c||^2 + reg ||c||^2` subject to `C_center c = d_j`,
  separately for the two amplitude directions, then normalizes and
  orthogonalizes before rebasing. A genuine weak/KKT selector principle would
  need instead a canonically justified selected-representative map from
  amplitude data to one privileged 2D span, independent of arbitrary `reg`,
  cutoff, and normalization choices.
- Type: `strategy-level hypothesis`
- Source file(s):
  `src/shell_buckling/mixed_weak/_core_reduction.py`;
  `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`;
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `output/clean_full_simple_support/selected_family_sensitivity_summary.json`;
  `output/clean_full_simple_support/selection_rule_audit_summary.json`.
- Current status: `weak/KKT target formulated / not closed`
- What counts as verification:
  an explicit source-of-truth separation between the current recipe-level
  constrained Tikhonov solve and the stronger theorem-facing weak/KKT selector
  principle it would need to approximate.
- Verification method:
  code inspection, numerical audit reuse, manual theory/status synthesis.
- Verification boundary:
  this does not prove that the weak/KKT route succeeds. It records only that
  this route is the most natural next theorem-facing selector program and that
  the present Tikhonov rule is not itself the theorem.
- Next action:
  define the correct theorem-facing constrained class and the canonical
  weak/interior optimality statement, then prove existence, uniqueness, and
  canonicity of the selected weak family.

### V-S50. Weak/KKT theorem target readiness has been assessed: almost ready, but prerequisite clarification is still needed

- ID: `V-S50`
- Claim / Hypothesis:
  The weak/KKT selector route on the present clean full simple-support branch
  is now specified well enough to identify the correct next theorem program,
  but not yet well enough to start a clean proof attempt immediately. The
  remaining prerequisite clarifications are:
  1. close the theorem-facing constrained class on which the selected weak map
     should act;
  2. identify the canonical weak/interior optimality statement that should
     define the selected representative.
- Type: `strategy-level hypothesis`
- Source file(s):
  `src/shell_buckling/mixed_weak/_core_reduction.py`;
  `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`.
- Current status: `almost ready / prerequisite clarification needed`
- What counts as verification:
  an explicit readiness checklist that identifies the candidate theorem target,
  the exact unresolved underdeterminations, the authority proof obligations, and
  the prerequisite clarifications needed before proof work starts.
- Verification method:
  code inspection, numerical audit reuse, manual theory/status synthesis.
- Verification boundary:
  this is not a proof that the weak/KKT route succeeds, and it is not yet a
  readiness claim for a finished proof start. It records only that the next
  step should still be one short clarification layer below a proof attempt.
- Next action:
  clarify the theorem-facing constrained class and the canonical weak/interior
  principle first; then reassess proof readiness.

### V-S51. The theorem-facing constrained class `A_con^th,n(q)` has been narrowed but not fixed

- ID: `V-S51`
- Claim / Hypothesis:
  On the present clean full simple-support branch, the intended theorem-facing
  constrained codomain for a future weak/KKT selected-representative map is no
  longer completely schematic, but it is not yet fixed sharply either. The
  current repo evidence narrows `A_con^th,n(q)` to two plausible candidates:
  1. the selected-trace constrained slice of the intended full theorem-facing
     admissible class;
  2. a theorem-facing selected overclass closer to `A_ls`, with
     `A_sel^{th,cand}` the nearest current structural placeholder.
  The raw code-level spaces `X_trial,n`, `W_reg,n(q)`, the exact numerical
  selected family `A_repo,n(q) = A_ls,n(q)`, and the selected trace plane alone
  should not be read as the intended theorem-facing codomain.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_simple_support_object_glossary.md`;
  `docs/theory/current_theory_verification_map.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status: `narrowed to two plausible candidates / not fixed`
- What counts as verification:
  a source-of-truth clarification that distinguishes the intended
  theorem-facing codomain from the code-level coefficient classes, the exact
  numerical selected family, and the trace plane alone, while identifying the
  precise remaining ambiguity.
- Verification method:
  code inspection, theory/status synthesis, existing pilot/object-glossary
  comparison.
- Verification boundary:
  this does not prove that either narrowed candidate is the correct codomain.
  It only records that the codomain question is now better constrained than a
  fully schematic placeholder, while still not closed enough for proof work to
  start without one more clarification layer.
- Next action:
  decide whether the theorem-facing codomain should be fixed through the full
  admissible-class route or through a genuinely closed selected-overclass /
  local-to-global route; then return to the weak/KKT readiness question.

### V-S52. For the weak/KKT route, the preferred codomain target is now the selected-trace constrained slice of the full admissible class

- ID: `V-S52`
- Claim / Hypothesis:
  On the present clean full simple-support branch, the preferred theorem-facing
  codomain target for the future weak/KKT selected-representative map is now
  the selected-trace constrained slice of the intended full admissible class,
  not the selected-overclass / local-to-global route. The selected-overclass
  route remains live, but it is currently better read as a neighboring theorem
  program than as the primary codomain of `S_weak,n,q`.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_simple_support_object_glossary.md`;
  `docs/theory/current_theory_verification_map.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status: `preferred codomain route chosen / not closed`
- What counts as verification:
  a source-of-truth comparison showing why the selected-trace constrained slice
  is the closer theorem-facing analogue of the live weak/KKT geometry and why
  the selected-overclass route should currently be treated as a secondary
  neighboring program.
- Verification method:
  code inspection, pilot interpretation reuse, manual theory/status synthesis.
- Verification boundary:
  this does not prove that the preferred route is already closed as a theorem.
  It records only the current route choice for the next clarification step on
  the weak/KKT program.
- Next action:
  sharpen the ambient full admissible/constrained class enough to define the
  selected-trace slice cleanly, then formulate the canonical weak/interior
  optimality statement on that preferred codomain.

### V-S53. The ambient full admissible/constrained class `A_full^th,n(q)` is now narrowed substantially, but still not closed sharply enough

- ID: `V-S53`
- Claim / Hypothesis:
  On the present clean full simple-support branch, the intended ambient class
  `A_full^th,n(q)` for the preferred weak/KKT codomain route should now be read
  as the full clean admissible / center-regular tangent class of the continuous
  mixed problem, not as the weighted-trial coefficient universe, not as the
  ansatz-level center-regular coefficient slice, not as the exact repo-selected
  family, and not as the selected trace plane alone. This narrows the ambient
  object substantially, but it does not yet close it sharply enough, because
  the repo still lacks a finished continuum/local packaging of that full class
  together with higher-order formal continuation/completeness and theorem-facing
  trace regularity strong enough for the selected-trace slice to be a finished
  codomain.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_simple_support_object_glossary.md`;
  `docs/theory/current_theory_verification_map.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `src/shell_buckling/mixed_weak/_core_reduction.py`;
  `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`.
- Current status: `ambient class narrowed substantially / still not sharp enough`
- What counts as verification:
  a source-of-truth clarification that separates the intended ambient continuum
  class from the explicit weighted-trial/coefficient surrogates and from the
  exact selected family, while naming the exact missing continuum/local
  packaging step.
- Verification method:
  code inspection, pilot interpretation reuse, manual theory/status synthesis.
- Verification boundary:
  this does not prove that `A_full^th,n(q)` is already closed. It records only
  the strongest current ambient-class reading and the remaining obstacle that
  still blocks the preferred weak/KKT codomain from becoming a finished
  theorem-facing object.
- Next action:
  package the full admissible / center-regular continuum class and its
  theorem-facing trace regularity sharply enough that the selected-trace slice
  inside `A_full^th,n(q)` becomes a clean codomain source.

### V-S54. The preferred weak/KKT codomain is now packaged as an ambient-class-plus-trace pair, but one explicit continuum/local trace-regularity gap remains

- ID: `V-S54`
- Claim / Hypothesis:
  On the present clean full simple-support branch, the preferred weak/KKT
  codomain can now be read more sharply as the pair
  `(A_full^th,n(q), J_0)`, where `A_full^th,n(q)` is the full clean admissible /
  center-regular tangent class and `J_0` is the finite leading-center jet used
  to define the slice
  `{c in A_full^th,n(q) : J_0(c) in im(D_amp,n(q))}`.
  The exact map `J_0 = C_center` and the identity
  `J_0(A_ls) = im(D_amp)` are already closed on the weighted-ansatz /
  selected-family boundary, but not yet on all of `A_full^th,n(q)`. So the
  remaining bottleneck is one explicit continuum/local trace-regularity gap,
  tied to the missing higher-order local continuation/completeness packaging.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_simple_support_object_glossary.md`;
  `docs/theory/current_theory_verification_map.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `src/shell_buckling/mixed_weak/_core_reduction.py`;
  `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`.
- Current status: `class-plus-trace package sharp / one trace-local gap remains`
- What counts as verification:
  a source-of-truth clarification that packages the preferred codomain as the
  ambient class together with the finite trace needed to define the selected
  slice, and that names the exact remaining continuum/local upgrade.
- Verification method:
  code inspection, pilot interpretation reuse, manual theory/status synthesis.
- Verification boundary:
  this does not prove that the preferred codomain is already proof-ready. It
  records only that the remaining obstacle has been reduced to one explicit
  continuum/local trace-regularity gap.
- Next action:
  close the theorem-facing extension of the finite leading-center trace `J_0`
  to the full ambient class `A_full^th,n(q)`, together with the local
  continuation/completeness needed for that extension to support the selected-
  trace slice cleanly.

### V-S55. The `J_0` theorem-facing extension gap is now narrowed to one precise local/trace theorem task

- ID: `V-S55`
- Claim / Hypothesis:
  On the present clean full simple-support branch, the remaining `J_0` blocker
  for the preferred weak/KKT codomain is no longer best read as a broad open
  selector ambiguity. It is now narrowed to one precise theorem-facing task:
  extend the current exact finite leading-center jet
  `J_0 = C_center` from the weighted-ansatz / selected-family boundary to the
  full ambient class `A_full^th,n(q)`, with enough local
  continuation/completeness and trace regularity that the slice
  `{c in A_full^th,n(q) : J_0(c) in im(D_amp,n(q))}` is cleanly meaningful.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_simple_support_object_glossary.md`;
  `docs/theory/current_theory_verification_map.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `src/shell_buckling/mixed_weak/_core_reduction.py`;
  `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`.
- Current status: `narrowed to one precise local/trace theorem task`
- What counts as verification:
  a source-of-truth clarification that separates the exact ansatz-level closure
  from the intended ambient-class extension and formulates the remaining gap as
  one explicit theorem-facing trace/local extension task.
- Verification method:
  code inspection, pilot interpretation reuse, manual theory/status synthesis.
- Verification boundary:
  this does not prove that the `J_0` extension is already closed. It records
  only that the remaining blocker has now been sharpened to one explicit local
  trace-extension task.
- Next action:
  formulate and eventually prove the theorem-facing extension of the finite
  leading-center jet `J_0` to `A_full^th,n(q)` together with the local
  continuation/completeness needed for that extension.

### V-S56. The remaining `J_0` local/trace theorem task is now formulated sharply enough for a direct theorem attempt

- ID: `V-S56`
- Claim / Hypothesis:
  On the present clean full simple-support branch, the remaining `J_0`
  blocker for the preferred weak/KKT codomain can now be formulated as one
  sharp theorem-facing task: for fixed `(n,q)`, define a finite leading-center
  jet
  `J_0^th,n,q : A_full^th,n(q) -> R^4`
  on the ambient admissible / center-regular class, with the same four
  coordinates already used by the exact ansatz-level trace, prove that it is
  well-defined under the current local continuation/completeness hypotheses,
  and prove that it agrees with `C_center` on the weighted-trial overlap so
  that the slice
  `{c in A_full^th,n(q) : J_0^th,n,q(c) in im(D_amp,n(q))}`
  is meaningful.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_simple_support_object_glossary.md`;
  `docs/theory/current_theory_verification_map.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `src/shell_buckling/mixed_weak/_core_reduction.py`;
  `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`.
- Current status: `sharp enough for direct theorem attempt`
- What counts as verification:
  a source-of-truth statement of the exact theorem target, its hypotheses, and
  its intended codomain-level conclusion, with the statement ambiguity reduced
  below the level of “what theorem are we trying to prove?”
- Verification method:
  code inspection, pilot interpretation reuse, manual theory/status synthesis.
- Verification boundary:
  this does not prove the theorem itself. It records only that the remaining
  `J_0` task now appears sharp enough to be attacked directly as a theorem.
- Next action:
  either begin the direct theorem attempt for this `J_0` local/trace task, or
  run one final proof-readiness recheck focused only on the explicit
  hypotheses.

### V-S57. A direct proof attempt for the remaining `J_0` local/trace theorem reduces it to one explicit ambient finite-jet extraction lemma

- ID: `V-S57`
- Claim / Hypothesis:
  On the present clean full simple-support branch, a direct proof attempt for
  the theorem-facing map
  `J_0^th,n,q : A_full^th,n(q) -> R^4`
  does not yet prove the full theorem, but it does identify the first blocking
  lemma sharply: every ambient object `c in A_full^th,n(q)` should admit a
  unique current-normalized leading-center quadruple `(U0, N0, P0, Y0)` whose
  induced four coordinates
  `[U0, P0, N0 + (lambda_c / n) P0, Y0 - lambda_c P0]`
  are well-defined, depend only on `c`, satisfy the current clean mixed local
  compatibility requirements, and agree with `C_center c` on the weighted-trial
  overlap. Until that ambient finite-jet extraction lemma is closed, the map
  `J_0^th,n,q` is not yet available on all of `A_full^th,n(q)`.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_simple_support_object_glossary.md`;
  `docs/theory/current_theory_verification_map.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`.
- Current status: `direct proof attempt made / reduced to first explicit local-trace lemma`
- What counts as verification:
  a theorem-facing proof of ambient finite-jet existence, uniqueness, current-
  normalization compatibility, and weighted-overlap agreement for the current
  `J_0` coordinates on `A_full^th,n(q)`.
- Verification method:
  manual proof attempt, reuse of already closed ansatz-level trace theorem,
  reuse of leading local symbolic trace identities, theory/status synthesis.
- Verification boundary:
  this does not prove the `J_0` theorem itself, and it does not reopen the
  selector problem. It records only that the direct theorem attempt stops first
  at one explicit local/trace lemma.
- Next action:
  prove the ambient finite-jet extraction lemma for the current `J_0`
  coordinates, or if needed sharpen only the hypothesis-level statement of
  `A_full^th,n(q)` enough for that lemma to be well-posed.

### V-S58. A direct theorem attempt for the ambient finite-jet extraction lemma reduces it further to ambient leading-coefficient extraction in the current normalization

- ID: `V-S58`
- Claim / Hypothesis:
  On the present clean full simple-support branch, a direct theorem attempt for
  the ambient finite-jet extraction lemma does not yet prove the whole lemma,
  but it does show that the first unresolved step is even narrower: one still
  needs a theorem-facing statement that every `c in A_full^th,n(q)` admits the
  four current-normalized leading coefficients `(U0, N0, P0, Y0)` for the
  channels `(u_s, u_n, varphi, psi)` in the current near-center scaling class.
  Once those coefficients exist, the current repo already has the needed
  overlap agreement with `C_center`, the leading mixed-equation compatibility
  relations, and uniqueness inside that normalization.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status: `direct lemma attempt made / reduced to ambient leading-coefficient extraction sublemma`
- What counts as verification:
  a theorem-facing proof that ambient admissible / center-regular objects in
  `A_full^th,n(q)` admit the four current-normalized leading coefficients in
  the current trace convention before the leading mixed-equation relations are
  imposed.
- Verification method:
  manual theorem attempt, reuse of the exact weighted-ansatz trace theorem,
  reuse of the already closed leading local symbolic block, theory/status
  synthesis.
- Verification boundary:
  this does not prove the ambient finite-jet lemma. It records only that its
  first unresolved step is now reduced to ambient leading-coefficient
  extraction rather than the full bundle of jet properties.
- Next action:
  prove the ambient leading-coefficient extraction / normalization sublemma for
  the current `J_0` coordinates, or sharpen `A_full^th,n(q)` only to the extent
  needed to make that sublemma formally well-posed.

### V-S59. A direct theorem attempt for the ambient leading-coefficient extraction sublemma reduces it further to ambient one-term asymptotic existence in the current scaling class

- ID: `V-S59`
- Claim / Hypothesis:
  On the present clean full simple-support branch, a direct theorem attempt for
  the ambient leading-coefficient extraction / normalization sublemma does not
  yet prove that sublemma, but it does show that the first unresolved step is
  smaller still: one needs a theorem-facing statement that every
  `c in A_full^th,n(q)` admits one-term current-normalized asymptotics for the
  four channels `(u_s, u_n, varphi, psi)` in the present near-center scaling
  orders. Once those one-term asymptotics exist, extraction of
  `(U0, N0, P0, Y0)` is immediate, uniqueness in the chosen normalization is
  formal, and the overlap with `C_center` remains exact on the weighted-trial
  boundary.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status: `direct sublemma attempt made / reduced to ambient one-term asymptotic existence`
- What counts as verification:
  a theorem-facing proof that ambient admissible / center-regular objects in
  `A_full^th,n(q)` admit one-term asymptotics
  `u_s = U0 x^n + o(x^n)`,
  `u_n = N0 x^n + o(x^n)`,
  `varphi = P0 x^(n-1) + o(x^(n-1))`,
  `psi = Y0 x^(n-1) + o(x^(n-1))`
  in the current center-trace normalization.
- Verification method:
  manual theorem attempt, reuse of the principal-part scaling analysis, reuse
  of the exact weighted-ansatz trace theorem, theory/status synthesis.
- Verification boundary:
  this does not prove the leading-coefficient extraction sublemma. It records
  only that the first unresolved step is now ambient one-term asymptotic
  existence rather than extraction/normalization itself.
- Next action:
  prove the ambient one-term asymptotic existence sub-sublemma for the four
  current `J_0` channels, or sharpen `A_full^th,n(q)` only enough to make that
  asymptotic statement formally well-posed.

### V-S60. A direct theorem attempt for the ambient one-term asymptotic existence sub-sublemma reduces it further to normalized-limit existence in the current scaling convention

- ID: `V-S60`
- Claim / Hypothesis:
  On the present clean full simple-support branch, a direct theorem attempt for
  the ambient one-term asymptotic existence sub-sublemma does not yet prove
  that sub-sublemma, but it shows that the first unresolved step is narrower
  still: one needs a theorem-facing statement that every
  `c in A_full^th,n(q)` has finite normalized channel limits
  `u_s/x^n`, `u_n/x^n`, `varphi/x^(n-1)`, and `psi/x^(n-1)` in the current
  center-trace normalization. The current repo already supports the scaling
  orders themselves, so the first unresolved point is no longer the exponents
  but the existence of the corresponding normalized limits.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status: `direct sub-sublemma attempt made / reduced to normalized-limit existence`
- What counts as verification:
  a theorem-facing proof that ambient admissible / center-regular objects in
  `A_full^th,n(q)` have finite normalized limits for the four current `J_0`
  channels in the present scaling convention.
- Verification method:
  manual theorem attempt, reuse of the principal-part scaling analysis, reuse
  of the exact weighted-ansatz trace convention, theory/status synthesis.
- Verification boundary:
  this does not prove the one-term asymptotic existence sub-sublemma. It
  records only that the first unresolved step is now normalized-limit
  existence rather than the one-term asymptotic statement as a whole.
- Next action:
  prove the ambient normalized-limit existence sub-sub-sublemma for the four
  current `J_0` channels, or sharpen `A_full^th,n(q)` only enough to make that
  limit statement formally well-posed.

### V-S61. A direct theorem attempt for the ambient normalized-limit existence sub-sub-sublemma reduces it further to convergence of the already-bounded normalized channels

- ID: `V-S61`
- Claim / Hypothesis:
  On the present clean full simple-support branch, a direct theorem attempt for
  the ambient normalized-limit existence sub-sub-sublemma does not yet prove
  that sub-sub-sublemma, but it shows that the first unresolved step is
  narrower still: the current repo already supports boundedness of
  `u_s/x^n`, `u_n/x^n`, `varphi/x^(n-1)`, and `psi/x^(n-1)` through the checked
  scaling orders, so the remaining open point is convergence of those
  already-bounded renormalized channels as `x -> 0`, equivalently continuous
  extension of them to the center in the present trace normalization.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status:
  `direct sub-sub-sublemma attempt made / reduced to normalized-quotient convergence`
- What counts as verification:
  a theorem-facing proof that for every ambient admissible / center-regular
  object in `A_full^th,n(q)`, the bounded renormalized channels
  `u_s/x^n`, `u_n/x^n`, `varphi/x^(n-1)`, and `psi/x^(n-1)` converge as
  `x -> 0` in the current center-trace normalization.
- Verification method:
  manual theorem attempt, reuse of the principal-part scaling analysis, reuse
  of the exact weighted-ansatz trace convention, theory/status synthesis.
- Verification boundary:
  this does not prove the normalized-limit existence sub-sub-sublemma. It
  records only that boundedness is already supported and that the first open
  point is now convergence / continuous extension of the normalized channels.
- Next action:
  prove the ambient normalized-quotient convergence sub-sub-sub-sublemma for
  the four current `J_0` channels, or sharpen `A_full^th,n(q)` only enough to
  make that convergence statement formally well-posed.

### V-S62. A direct theorem attempt for the ambient normalized-quotient convergence sub-sub-sub-sublemma reduces it further to a renormalized regular-singular limit lemma

- ID: `V-S62`
- Claim / Hypothesis:
  On the present clean full simple-support branch, a direct theorem attempt for
  the ambient normalized-quotient convergence sub-sub-sub-sublemma does not yet
  prove that sub-sub-sub-sublemma, but it shows that the regular-singular route
  gets furthest: the current repo already supports the scaling orders and hence
  boundedness of the renormalized channels, while derivative/integrability and
  compactness routes are not yet closed. The first unresolved step is now an
  ambient renormalized local-system / continuation statement ensuring that the
  renormalized vector
  `[x^(-n) u_s, x^(-n) u_n, x^(1-n) varphi, x^(1-n) psi]`
  satisfies a near-center regular-singular law strong enough that boundedness
  forces convergence as `x -> 0`.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status:
  `direct sub-sub-sub-sublemma attempt made / reduced to renormalized regular-singular limit`
- What counts as verification:
  a theorem-facing proof that for every ambient admissible / center-regular
  object in `A_full^th,n(q)`, the renormalized channel vector satisfies a
  near-center regular-singular local system / continuation statement from which
  convergence of the bounded renormalized channels follows.
- Verification method:
  manual theorem attempt, reuse of the principal-part scaling analysis, reuse
  of the checked local recurrence structure, theory/status synthesis.
- Verification boundary:
  this does not prove the normalized-quotient convergence sub-sub-sub-sublemma.
  It records only that the regular-singular route is the strongest current
  route and that the first open point is now the ambient renormalized limit
  theorem behind that route.
- Next action:
  prove the ambient renormalized regular-singular limit
  sub-sub-sub-sub-sublemma for the four current `J_0` channels, or sharpen
  `A_full^th,n(q)` only enough to make that local-system statement formally
  well-posed.

### V-S63. A direct theorem attempt for the ambient renormalized regular-singular limit lemma reduces it further to ambient local-system derivation in the richer jet variables

- ID: `V-S63`
- Claim / Hypothesis:
  On the present clean full simple-support branch, a direct theorem attempt for
  the ambient renormalized regular-singular limit
  sub-sub-sub-sub-sublemma does not yet prove that lemma, but it shows that the
  first unresolved step is narrower still: the checked richer-jet recurrence
  picture
  `Xi_rich^(1,eta)`, `Xi_rich^(1+,eta)`, together with the exact projection
  `Pi_eta_to_J0`, already identifies the formal renormalized variables and the
  candidate regular-singular structure, but the repo still lacks a theorem-
  facing derivation that every ambient
  `c in A_full^th,n(q)` admits a punctured-neighborhood renormalized local
  state satisfying a closed near-center regular-singular system whose leading
  structure matches that checked model.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status:
  `direct sub-sub-sub-sub-sublemma attempt made / reduced to ambient renormalized local-system derivation`
- What counts as verification:
  a theorem-facing proof that every ambient admissible / center-regular object
  in `A_full^th,n(q)` lifts to a punctured-neighborhood renormalized local
  state in the current richer jet variables, satisfying a closed
  regular-singular system compatible with the checked principal-part /
  recurrence model.
- Verification method:
  manual theorem attempt, reuse of the principal-part scaling analysis, reuse
  of the checked richer-jet recurrence structure, theory/status synthesis.
- Verification boundary:
  this does not prove the ambient renormalized regular-singular limit lemma. It
  records only that the first open point is now derivation of the ambient local
  system itself, prior to bounded-solution convergence inside that system.
- Next action:
  prove the ambient renormalized local-system / jet-lift
  sub-sub-sub-sub-sub-sublemma for the current richer jet variables, or sharpen
  `A_full^th,n(q)` only enough to make that punctured-neighborhood statement
  formally well-posed.

### V-S64. A direct theorem attempt for the ambient renormalized local-system / jet-lift lemma reduces it further to punctured-neighborhood richer-jet lift existence

- ID: `V-S64`
- Claim / Hypothesis:
  On the present clean full simple-support branch, a direct theorem attempt for
  the ambient punctured-neighborhood renormalized local-system / jet-lift
  sub-sub-sub-sub-sub-sublemma does not yet prove that lemma, but it shows that
  the first unresolved step is narrower still: the checked richer-jet charts
  `Xi_rich^(1,eta)` and `Xi_rich^(1+,eta)` together with the exact projection
  `Pi_eta_to_J0` already identify the formal post-leading variables and their
  canonical return to current `J_0` coordinates, but the repo still lacks a
  theorem-facing statement that every ambient `c in A_full^th,n(q)` admits a
  punctured-neighborhood local lift realizing those richer-jet variables in a
  way that is also overlap-compatible with the exact ansatz-boundary trace
  `J_0 = C_center`.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status:
  `direct sub-sub-sub-sub-sub-sublemma attempt made / reduced to punctured-neighborhood richer-jet lift existence`
- What counts as verification:
  a theorem-facing proof that every ambient admissible / center-regular object
  in `A_full^th,n(q)` admits a punctured-neighborhood local lift realizing the
  first post-leading richer-jet variables compatible with the renormalized
  vector `W_c(x)`, the exact projection `Pi_eta_to_J0`, and the exact
  ansatz-boundary trace `J_0 = C_center` on the weighted-trial overlap whenever
  both descriptions are defined.
- Verification method:
  manual theorem attempt, reuse of the principal-part scaling analysis, reuse
  of the checked richer-jet chart / recurrence structure, theory/status
  synthesis.
- Verification boundary:
  this does not prove the ambient renormalized local-system / jet-lift lemma.
  It records only that the first open point is now existence of the punctured-
  neighborhood richer-jet lift itself, prior to closure of the ambient local
  system built on that lift.
- Next action:
  prove the punctured-neighborhood richer-jet lift-existence lemma for the
  current richer jet variables together with the needed overlap-compatibility
  clause, or sharpen `A_full^th,n(q)` only enough to make that local lift
  statement formally well-posed.

### V-S65. Targeted CAS+Lean back-verification confirms the current ansatz-boundary identities and exposes one explicit hidden premise in the proof skeleton

- ID: `V-S65`
- Claim / Hypothesis:
  On the present clean full simple-support branch, a targeted back-verification
  pass using live code inspection, CAS checks, and a small Lean proof-skeleton
  experiment reconfirms the current exact ansatz-boundary identities
  `J_0 = C_center`,
  `J_0(A_ls) = im(D_amp)`,
  the projection identities for `Pi_eta_to_J0`,
  and the checked first post-leading recurrence identities, while also showing
  that the abstract implication
  `richer-jet lift + regular-singular convergence => J_0^th well-defined`
  still needs one explicit extra premise:
  compatibility of the ambient lift with the current exact `J_0 = C_center`
  coordinates on the weighted-trial overlap.
- Type: `structural/formal claim`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `src/shell_buckling/mixed_weak/_core_reduction.py`;
  `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`.
- Current status:
  `targeted CAS+Lean back-verification completed / one hidden premise exposed`
- What counts as verification:
  1. live-code confirmation that `C_center` uses exactly the four `k = 0`
     ansatz columns and implements the current `J_0` coordinates;
  2. CAS confirmation of the exact current trace coordinates, the
     `Pi_eta_to_J0` identities, and the checked first post-leading recurrence
     identities used in the present proof line;
  3. Lean-style logical confirmation that steps
     `normalized limits => one-term asymptotics`,
     `one-term asymptotics => formal coefficient extraction`,
     and
     `J_0^th well-defined => selected-trace slice meaningful`
     compose cleanly, while the richer-jet step requires the explicit overlap-
     compatibility premise.
- Verification method:
  manual derivation framing, CAS, Lean proof-skeleton check, live-code audit.
- Verification boundary:
  this does not prove the ambient richer-jet lift-existence lemma, the ambient
  regular-singular limit theorem, or the weak/KKT selector theorem.
  It only reconfirms the currently exact formula-level identities and sharpens
  the abstract proof skeleton by making the compatibility premise explicit.
- Next action:
  keep the current formula-level identities at their present status, and state
  the richer-jet implication in future theorem work as
  `richer-jet lift + regular-singular convergence + overlap compatibility
  => J_0^th well-defined`,
  where overlap compatibility means agreement with the exact ansatz-boundary
  trace `J_0 = C_center` and compatibility with the canonical
  `Pi_eta_to_J0` projection on the weighted-trial overlap.

### V-S66. A direct proof attempt for the cleaned punctured-neighborhood richer-jet lift-existence lemma reduces it further to punctured-neighborhood first post-leading chart realization

- ID: `V-S66`
- Claim / Hypothesis:
  On the present clean full simple-support branch, a direct proof attempt for
  the cleaned ambient punctured-neighborhood richer-jet lift-existence lemma
  does not yet prove that lemma, but it shows that the first unresolved step is
  narrower still: once the current richer chart is realized for an ambient
  object, extension of `W_c`, compatibility with `Pi_eta_to_J0`, and the
  cleaned overlap-compatibility clause with `J_0 = C_center` are already formal.
  The first open point is therefore realization of the first post-leading chart
  itself on a punctured neighborhood for arbitrary ambient objects in
  `A_full^th,n(q)`.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`.
- Current status:
  `direct cleaned-lemma attempt made / reduced to punctured-neighborhood first post-leading chart realization`
- What counts as verification:
  a theorem-facing proof that every ambient admissible / center-regular object
  in `A_full^th,n(q)` admits punctured-neighborhood first post-leading chart
  data realizing `Xi_rich^(1,eta)` and, when needed, `Xi_rich^(1+,eta)`,
  extending `W_c`, so that the exact projection `Pi_eta_to_J0` and the
  overlap return to `J_0 = C_center` are meaningful.
- Verification method:
  manual theorem attempt, reuse of the checked richer-jet chart identities,
  reuse of the exact overlap-trace closure already recorded for `J_0 = C_center`,
  theory/status synthesis.
- Verification boundary:
  this does not prove the cleaned richer-jet lift-existence lemma. It records
  only that projection compatibility and overlap compatibility are no longer the
  first open steps once the chart exists, and that the first unresolved point
  is realization of the first post-leading richer chart itself.
- Next action:
  prove the punctured-neighborhood first post-leading chart-realization lemma
  for arbitrary ambient objects, or sharpen `A_full^th,n(q)` only enough to
  make that chart-realization statement formally well-posed.

### V-S67. The Step-1 blocker for the chart-realization line is best read as a separate punctured-local-representative existence lemma

- ID: `V-S67`
- Claim / Hypothesis:
  On the present clean full simple-support branch, the Step-1 blocker isolated
  by the current chart-realization proof line should presently be read as a
  separate local regularity / continuation lemma for ambient objects
  `c in A_full^th,n(q)`: each such object should admit a punctured near-center
  local representative with enough structure to define
  `(u_s, u_n, varphi, psi)` and support the first post-leading richer chart.
  This should not be folded silently into the definition of `A_full^th,n(q)`,
  because that ambient class is still recorded as not independently closed
  sharply enough, and it should not be promoted to a standing extra assumption,
  because that would hide the exact local theorem gap now isolated by the
  chart-realization line.
- Type: `structural/formal claim`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_simple_support_object_glossary.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/current_simple_support_chart_realization_proof_draft.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status:
  `theorem-facing role clarified / separate local representative lemma preferred`
- What counts as verification:
  a source-of-truth clarification that keeps `A_full^th,n(q)` as the intended
  ambient admissible / center-regular class while treating punctured near-
  center local-representative existence as its own local theorem task for
  members of that class, rather than as a hidden definition change or a
  standing extra assumption.
- Verification method:
  theory/status synthesis, pilot interpretation reuse, manual theorem-structure
  audit.
- Verification boundary:
  this does not prove punctured-local-representative existence. It records only
  the current theorem-facing role of that blocker in the clean chart-
  realization line.
- Next action:
  formulate and prove the explicit punctured-local-representative existence
  lemma for `c in A_full^th,n(q)`, or sharpen `A_full^th,n(q)` only enough to
  make that lemma formally well-posed.

### V-S68. A direct theorem attempt for the isolated Step-1 lemma reduces it further to ambient punctured-local-representative existence

- ID: `V-S68`
- Claim / Hypothesis:
  On the present clean full simple-support branch, a direct theorem attempt for
  the isolated Step-1 lemma does not yet prove that every
  `c in A_full^th,n(q)` admits a punctured near-center local representative
  with enough structure to define `W_c` and make the first richer-chart
  language meaningful. But it does show that the current scaling-class read and
  the checked richer-chart identities are no longer the first blockers once a
  punctured local representative exists. The first unresolved step is therefore
  smaller still: existence of the punctured-local representative itself for the
  ambient object.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/current_simple_support_chart_realization_proof_draft.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status:
  `direct Step-1 attempt made / reduced to ambient punctured-local-representative existence`
- What counts as verification:
  a theorem-facing proof that every ambient admissible / center-regular object
  `c in A_full^th,n(q)` admits some `delta > 0` and a punctured-neighborhood
  local representative on `(0,delta)` carrying the current mixed channels
  `(u_s, u_n, varphi, psi)`. Once that representative exists, the current
  scaling-class read already makes `W_c` meaningful and the checked truncated
  richer-chart objects `Xi_rich^(1,eta)`, `Xi_rich^(1+,eta)`, together with
  `Pi_eta_to_J0`, are already available as the theorem-facing Step-1 chart
  language.
- Verification method:
  manual theorem attempt, reuse of the current scaling-order read of
  `A_full^th,n(q)`, reuse of the checked richer-jet chart identities,
  theory/status synthesis.
- Verification boundary:
  this does not prove punctured-local-representative existence. It records only
  that the scaling-class clause and the richer-chart-language clause are not
  the first unresolved pieces once a punctured local representative exists.
- Next action:
  prove the ambient punctured-local-representative existence lemma for
  `c in A_full^th,n(q)`, or sharpen `A_full^th,n(q)` only enough to make that
  existence statement formally well-posed.

### V-S69. The ambient-to-local step should presently be phrased as a representation / witness relation, not as a germ-identity or canonical realization map

- ID: `V-S69`
- Claim / Hypothesis:
  On the present clean full simple-support branch, the theorem-facing relation
  between an ambient object `c in A_full^th,n(q)` and a punctured near-center
  clean mixed germ should presently be read as a weaker representation /
  witness relation. This is stronger than leaving the link informal, but weaker
  than identifying `A_full^th,n(q)` with an equivalence class of local germs
  and weaker than demanding a canonical realization map. The current next local
  theorem target should therefore assert existence of a witness local germ for
  each ambient object, not uniqueness or canonicity of a realization map.
- Type: `structural/formal claim`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/current_simple_support_object_glossary.md`;
  `docs/theory/current_simple_support_chart_realization_proof_draft.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status:
  `representation relation clarified / witness-style next lemma preferred`
- What counts as verification:
  a source-of-truth clarification that keeps `A_full^th,n(q)` as the ambient
  admissible / center-regular class, rejects silent redefinition of that class
  as a local-germ quotient, avoids introducing a stronger canonical realization
  map than is currently justified, and states the next local theorem target in
  existential witness form.
- Verification method:
  theory/status synthesis, pilot interpretation reuse, manual theorem-structure
  audit.
- Verification boundary:
  this does not prove ambient-to-local realization. It records only the current
  theorem-facing form that the realization statement should take.
- Next action:
  formulate and prove the existential ambient-to-local witness lemma: for every
  `c in A_full^th,n(q)`, there exists a punctured near-center clean mixed germ
  representing `c`.

### V-S70. The ambient-to-local witness relation should presently be packaged as a hybrid predicate `Rep_loc^{n,q}(c,G)`

- ID: `V-S70`
- Claim / Hypothesis:
  On the present clean full simple-support branch, the theorem-facing meaning
  of “`G` represents `c`” should presently be packaged as a hybrid witness
  predicate `Rep_loc^{n,q}(c,G)` between `c in A_full^th,n(q)` and punctured
  near-center clean mixed germs `G`. The predicate should require:
  1. `G` is a genuine punctured near-center clean mixed germ on some
     `(0,\delta)` in the current mixed variables, satisfying the current local
     clean mixed equations and near-center scaling orders there;
  2. `G` is admitted as the theorem-facing local witness for the ambient object
     `c` for the local near-center statements currently under consideration on
     this branch;
  3. on the exact weighted-ansatz / selected-family boundary, the witness
     relation is normalized by agreement with the exact finite leading-center
     trace `J_0 = C_center`.
  This is stronger than a trace-only predicate, but weaker than identifying
  `A_full^th,n(q)` with local-germ equivalence classes and weaker than
  demanding a canonical realization map.
- Type: `structural/formal claim`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/current_simple_support_object_glossary.md`;
  `docs/theory/current_simple_support_chart_realization_proof_draft.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status:
  `representation predicate sharpened / hybrid witness schema preferred`
- What counts as verification:
  a source-of-truth clarification that fixes the meaning of “`G` represents
  `c`” sharply enough that the existential witness lemma
  “for every `c in A_full^th,n(q)`, there exist `\delta > 0` and a punctured
  near-center clean mixed germ `G` on `(0,\delta)` such that
  `Rep_loc^{n,q}(c,G)`”
  is mathematically well-posed, while still avoiding germ-quotient semantics
  and avoiding a canonical realization map.
- Verification method:
  theory/status synthesis, pilot interpretation reuse, manual theorem-structure
  audit.
- Verification boundary:
  this does not prove that a witness germ exists for every
  `c in A_full^th,n(q)`. It records only the preferred predicate schema for the
  ambient-to-local witness relation.
- Next action:
  attempt the existential witness lemma in the sharpened form:
  for every `c in A_full^th,n(q)`, there exist `\delta > 0` and a punctured
  near-center clean mixed germ `G` on `(0,\delta)` such that
  `Rep_loc^{n,q}(c,G)`.

### V-S71. A direct theorem attempt for the existential ambient-to-local witness lemma is now blocked at witness-germ existence itself

- ID: `V-S71`
- Claim / Hypothesis:
  On the present clean full simple-support branch, once the theorem-facing
  representation predicate has been sharpened to `Rep_loc^{n,q}(c,G)`, the
  existential witness lemma
  “for every `c in A_full^th,n(q)`, there exist `\delta > 0` and a punctured
  near-center clean mixed germ `G` on `(0,\delta)` such that
  `Rep_loc^{n,q}(c,G)`”
  becomes mathematically well-posed. But a direct theorem attempt still does
  not prove it, because the repo does not yet provide a theorem-facing
  ambient-to-local extraction that produces such a punctured near-center clean
  mixed germ witness for arbitrary `c in A_full^th,n(q)`. So the first
  unresolved step is now witness-germ existence itself.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/current_simple_support_object_glossary.md`;
  `docs/theory/current_simple_support_chart_realization_proof_draft.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status:
  `direct witness-lemma attempt made / blocked at witness-germ existence`
- What counts as verification:
  a theorem-facing proof that for every `c in A_full^th,n(q)`, there exist
  `\delta > 0` and a punctured near-center clean mixed germ `G` on
  `(0,\delta)` such that `Rep_loc^{n,q}(c,G)`.
- Verification method:
  manual theorem attempt, reuse of the sharpened representation-predicate
  schema, pilot interpretation reuse, minimal theory/status audit.
- Verification boundary:
  this does not prove existence of the witness germ. It records only that the
  first unresolved step, after fixing the predicate, is production of the
  punctured near-center clean mixed germ witness itself.
- Next action:
  prove the witness-germ existence lemma for arbitrary `c in A_full^th,n(q)`,
  or isolate the exact ambient-to-local extraction principle needed to produce
  that witness.

### V-S72. The source principle behind witness-germ existence should presently be a punctured-neighborhood local clean mixed continuation theorem

- ID: `V-S72`
- Claim / Hypothesis:
  On the present clean full simple-support branch, the correct next source
  theorem behind witness-germ existence is a separate ambient punctured-
  neighborhood local clean mixed continuation theorem for objects
  `c in A_full^th,n(q)`. It should assert existence of an actual punctured
  near-center clean mixed state in the current mixed variables, satisfying the
  current local clean mixed equations and near-center scaling orders, and
  serving as a theorem-facing local continuation of `c`. The existential
  witness-germ lemma should then follow by passing to the germ of that local
  state and applying the already sharpened predicate `Rep_loc^{n,q}(c,G)`.
  This source theorem is narrower than a full article-level local solution-
  family derivation, better supported than a weak-to-local realization theorem
  on the current repo material, and not already closed implicitly in the
  current pilots.
- Type: `structural/formal claim`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/current_simple_support_object_glossary.md`;
  `docs/theory/current_simple_support_chart_realization_proof_draft.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status:
  `source theorem clarified / punctured local clean mixed continuation preferred`
- What counts as verification:
  a theorem-facing proof that for every `c in A_full^th,n(q)`, there exist
  `\delta > 0` and a genuine punctured near-center clean mixed state on
  `(0,\delta)` in the current mixed variables, satisfying the current local
  clean mixed equations and near-center scaling orders there, and serving as a
  local continuation of `c`.
- Verification method:
  theory/status synthesis, pilot interpretation reuse, manual theorem-structure
  audit.
- Verification boundary:
  this does not yet prove the local clean mixed continuation theorem. It fixes
  only which source principle should be pursued next behind witness-germ
  existence.
- Next action:
  attempt the ambient punctured-neighborhood local clean mixed continuation
  theorem, then derive the existential witness-germ lemma as its corollary via
  `Rep_loc^{n,q}(c,G)`.

### V-S73. A direct theorem attempt for the ambient punctured-neighborhood local clean mixed continuation theorem is now blocked at local continuation existence itself

- ID: `V-S73`
- Claim / Hypothesis:
  On the present clean full simple-support branch, a direct theorem attempt for
  the ambient punctured-neighborhood local clean mixed continuation theorem
  does not yet prove that every `c in A_full^th,n(q)` admits such a local
  continuation. But it does show that once a punctured near-center local
  continuation of `c` in the current mixed variables exists, the genuine clean
  mixed-state status, satisfaction of the current local clean mixed equations,
  and the current near-center scaling-order clauses are no longer the first
  blockers on the present repo reading. The first unresolved smaller step is
  therefore local continuation existence itself for arbitrary ambient
  `c in A_full^th,n(q)`.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/current_simple_support_object_glossary.md`;
  `docs/theory/current_simple_support_chart_realization_proof_draft.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status:
  `direct source-theorem attempt made / blocked at local continuation existence`
- What counts as verification:
  a theorem-facing proof that for every `c in A_full^th,n(q)`, there exist
  `\delta > 0` and a punctured near-center local continuation of `c` in the
  current mixed variables on `(0,\delta)`.
- Verification method:
  manual theorem attempt, reuse of the current ambient-equation and scaling
  assumptions, pilot interpretation reuse, minimal theory/status audit.
- Verification boundary:
  this does not prove local continuation existence. It records only that the
  other clauses of the source theorem are not the first unresolved pieces once
  such a continuation exists.
- Next action:
  prove the ambient punctured-neighborhood local continuation existence lemma
  for arbitrary `c in A_full^th,n(q)`, then recover the full source theorem and
  the witness-germ corollary.

### V-S74. The source mechanism behind local continuation existence should presently be a direct continuation theorem from the ambient compatibility package

- ID: `V-S74`
- Claim / Hypothesis:
  On the present clean full simple-support branch, the best-supported mechanism
  behind ambient punctured-neighborhood local continuation existence is a
  separate direct continuation theorem from the current ambient clean
  admissible / center-regular compatibility package for
  `c in A_full^th,n(q)`. This is better supported than reading `A_full^th,n(q)`
  as already locally realized on punctured intervals, better supported than a
  weak-to-local extraction theorem on the present repo boundary, and better
  supported than introducing a new extra ambient hypothesis before the theorem
  can start.
- Type: `structural/formal claim`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_rebuild_note.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/current_simple_support_object_glossary.md`;
  `docs/theory/current_simple_support_chart_realization_proof_draft.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status:
  `source mechanism clarified / direct continuation theorem preferred`
- What counts as verification:
  a source-of-truth clarification that the next theorem should directly prove
  punctured local continuation from the current ambient compatibility package
  on `A_full^th,n(q)`, rather than relying on away-from-center identification,
  weak-to-local extraction, or an added ambient premise.
- Verification method:
  theory/status synthesis, pilot interpretation reuse, manual theorem-structure
  audit.
- Verification boundary:
  this does not prove local continuation existence. It fixes only which
  theorem-facing mechanism should be pursued next behind that existence claim.
- Next action:
  attempt the direct ambient compatibility-to-punctured-local-continuation
  theorem for `A_full^th,n(q)`.

### V-S75. Assumption LC is an explicit unproved working assumption separating the strict closure line from the conditional local/chart line

- ID: `V-S75`
- Claim / Hypothesis:
  On the present clean full simple-support branch, introduce the following
  working physical assumption:
  for fixed `(n,q)`, every `c in A_full^th,n(q)` admits `\delta > 0` and a
  punctured near-center clean mixed continuation on `(0,\delta)` in the
  current mixed variables, satisfying the current local clean mixed equations
  and the intended near-center scaling orders there.
  This is not a proved theorem-facing result on the branch. It is introduced
  only to stop further repeated reformulation of the same ambient-to-local
  closure barrier. Under Assumption LC, later witness-germ, chart-realization,
  richer-jet, and theorem-facing local-`J_0` steps may proceed conditionally.
  Without it, the strict theorem line remains open at the local-continuation
  closure barrier recorded in `V-S73`.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/assumptions/assumptions.md`;
  `docs/theory/current_simple_support_chart_realization_proof_draft.md`.
- Current status:
  `explicit working assumption introduced / not proved`
- What counts as verification:
  a theorem-facing proof of the ambient punctured-neighborhood local
  continuation existence lemma for arbitrary `c in A_full^th,n(q)`, so that
  Assumption LC can be discharged rather than used as a standing conditional
  premise.
- Verification method:
  manual theorem attempt; later, if the statement stabilizes, CAS/Lean support
  may be used on subordinate symbolic/logical pieces.
- Verification boundary:
  this does not prove Assumption LC. It records only the strict/conditional
  split: the strict theorem line remains blocked at the closure barrier, while
  the later local/chart line may proceed conditionally under LC.
- Next action:
  either prove the strict ambient punctured-neighborhood local continuation
  existence lemma, or continue the local witness/chart program explicitly under
  Assumption LC.

### V-S76. Conditional on Assumption LC, the ambient-to-local witness-germ lemma is closed on the current branch reading

- ID: `V-S76`
- Claim / Hypothesis:
  On the present clean full simple-support branch, conditional on Assumption
  LC, the ambient-to-local witness-germ lemma is closed:
  for fixed `(n,q)` and every `c in A_full^th,n(q)`, there exist `\delta > 0`
  and a punctured near-center clean mixed germ `G` on `(0,\delta)` such that
  `Rep_loc^{n,q}(c,G)`.
- Type: `structural/formal claim`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/assumptions/assumptions.md`;
  `docs/theory/current_simple_support_chart_realization_proof_draft.md`;
  `docs/theory/current_simple_support_object_glossary.md`.
- Current status:
  `closed conditionally under LC / strict line still open`
- What counts as verification:
  a theorem-facing derivation that Assumption LC supplies a punctured near-
  center clean mixed continuation, that passing to its punctured local germ is
  legitimate, and that the current `Rep_loc^{n,q}(c,G)` schema then reads that
  germ as the theorem-facing local witness for `c`.
- Verification method:
  manual theorem attempt under the explicit working assumption LC.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict ambient-to-
  local continuation theorem. It closes only the conditional witness-germ
  lemma under LC.
- Next action:
  continue the local chart / richer-jet line conditionally under LC, or return
  to the strict closure theorem if the assumption is to be discharged.

### V-S77. Conditional on Assumption LC, the chart-realization lemma is reduced to realization of the first post-leading richer variables on the witness germ

- ID: `V-S77`
- Claim / Hypothesis:
  On the present clean full simple-support branch, conditional on Assumption
  LC, the chart-realization line no longer blocks at punctured local
  representative existence. Under LC, punctured local continuation and the
  witness-germ lemma are available. Once the first post-leading richer chart is
  realized on that witness germ, compatibility with `Pi_eta_to_J0` and overlap
  return to `J_0 = C_center` are already formal on the current branch reading.
  The first remaining conditional blocker is therefore realization of
  `Xi_rich^(1,eta)` and, when needed, `Xi_rich^(1+,eta)` as actual punctured
  local chart data on the witness germ, not merely as formal recurrence
  coefficients.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/assumptions/assumptions.md`;
  `docs/theory/current_simple_support_chart_realization_proof_draft.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.
- Current status:
  `reduced conditionally under LC / first blocker is richer-variable realization`
- What counts as verification:
  a theorem-facing conditional proof that for fixed `(n,q)` and every
  `c in A_full^th,n(q)`, Assumption LC implies existence of punctured near-
  center first post-leading chart data realizing `Xi_rich^(1,eta)` and, when
  needed, `Xi_rich^(1+,eta)`, extending the punctured local witness germ.
- Verification method:
  manual theorem attempt under Assumption LC, reuse of the current exact
  `Pi_eta_to_J0` and overlap-compatibility identities.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only the first remaining
  blocker on the conditional local chart line.
- Next action:
  attempt the conditional first post-leading richer-variable realization lemma
  on the punctured local witness germ under Assumption LC.

### V-S78. Conditional on Assumption LC, the first exact blocker in the chart-realization line is recurrence-to-local realization on the witness germ

- ID: `V-S78`
- Claim / Hypothesis:
  On the present clean full simple-support branch, conditional on Assumption
  LC, the chart-realization line is reduced one step further. The remaining
  blocker is not punctured local existence and not the formal projection /
  overlap clauses. It is recurrence-to-local realization on the punctured local
  witness germ itself: promotion of the checked first post-leading richer
  variables underlying `Xi_rich^(1,eta)` and, when needed, `Xi_rich^(1+,eta)`
  from formal checked recurrence data to actual punctured local chart data on
  that germ.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/assumptions/assumptions.md`;
  `docs/theory/current_simple_support_chart_realization_proof_draft.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`.
- Current status:
  `reduced conditionally under LC / blocker sharpened to recurrence-to-local realization`
- What counts as verification:
  a theorem-facing conditional proof that the checked first post-leading
  recurrence variables can be realized as actual punctured local chart data on
  the punctured local witness germ supplied by Assumption LC.
- Verification method:
  manual theorem attempt under Assumption LC, reuse of the checked recurrence
  model, minimal pilot/theory audit.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only the sharpened first
  blocker on the conditional chart-realization line.
- Next action:
  attempt the conditional recurrence-to-local realization lemma on the
  punctured local witness germ under Assumption LC.

### V-S79. Conditional on Assumption LC, the reduced first post-leading extraction lemma is blocked first at one extra asymptotic order for the renormalized witness-germ channels

- ID: `V-S79`
- Claim / Hypothesis:
  On the present clean full simple-support branch, if one restricts the
  conditional chart-realization line to the reduced first post-leading slots
  `U1, N1, P1, Y1` underlying `Xi_rich^(1,eta)`, the first exact reduced
  blocker is no longer the whole recurrence-to-local bridge at once. It is one
  extra near-center asymptotic order for the renormalized witness-germ
  channels, sufficient to define those four coefficients as actual punctured
  local quantities. Once such extraction is available in the weak asymptotic
  form `f(x) = f0 + x f1 + o(x)` or an equivalent first post-leading statement,
  agreement with the checked recurrence-side variables is no longer the first
  blocker on the current branch reading.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_richer_variable_realization_draft.md`;
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/assumptions/assumptions.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`.
- Current status:
  `reduced conditionally under LC / first reduced blocker is extra asymptotic order`
- What counts as verification:
  a theorem-facing conditional proof that the punctured local witness germ
  supplied by Assumption LC admits one extra near-center asymptotic order for
  the renormalized channels, enough to define `U1, N1, P1, Y1` as actual
  punctured local first post-leading coefficients and then compare them with
  the checked recurrence-side variables.
- Verification method:
  manual theorem attempt under Assumption LC, reuse of the checked first
  post-leading recurrence model, minimal pilot/theory audit.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only the sharpened reduced
  blocker on the conditional chart-realization line.
- Next action:
  attempt the conditional extra-asymptotic-order lemma for the renormalized
  punctured witness-germ channels under Assumption LC.

### V-S80. Conditional on Assumption LC, the reduced first-order remainder-control lemma is blocked first at source-remainder control for `Q_s` and `Q_\varphi`

- ID: `V-S80`
- Claim / Hypothesis:
  On the present clean full simple-support branch, once the reduced
  renormalized witness-germ remainder system is fixed, a direct theorem attempt
  for the reduced first-order remainder-control lemma does not yet prove the
  desired asymptotics
  `S = U0 + xU1 + o(x)`, `N = N0 + xN1 + o(x)`,
  `P = P0 + xP1 + o(x)`, `Y = Y0 + xY1 + o(x)`.
  But it does reduce the first exact reduced blocker further:
  the missing step is first post-leading control of the auxiliary renormalized
  source remainders `Q_s` and `Q_\varphi`.
  Once that source-remainder control is available, the reduced remainder system
  is triangular in `(R_s, R_n, R_\varphi)` and `R_\psi` follows algebraically,
  so coefficient extraction / recurrence-side identification is no longer the
  first blocker on the current branch reading.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_reduced_renormalized_system_draft.md`;
  `docs/theory/current_simple_support_richer_variable_realization_draft.md`;
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/assumptions/assumptions.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`.
- Current status:
  `reduced conditionally under LC / first reduced blocker is source-remainder control`
- What counts as verification:
  a theorem-facing conditional proof that the auxiliary renormalized source
  remainders `Q_s` and `Q_\varphi` admit first post-leading control strong
  enough to drive the reduced remainder system to
  `R_s = xU1 + o(x)`, `R_n = xN1 + o(x)`, `R_\varphi = xP1 + o(x)`,
  `R_\psi = xY1 + o(x)`.
- Verification method:
  manual theorem attempt under Assumption LC, reuse of the reduced
  renormalized local system draft and the checked first post-leading recurrence
  model.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only the sharpened reduced
  blocker on the conditional chart-realization line.
- Next action:
  attempt the conditional source-remainder control lemma for `Q_s` and
  `Q_\varphi` under Assumption LC.

### V-S81. Conditional on Assumption LC, the reduced first post-leading asymptotic problem is not structurally closed and must be lifted to the smallest fuller local mixed block

- ID: `V-S81`
- Claim / Hypothesis:
  On the present clean full simple-support branch, a structural diagnostic of
  the reduced renormalized witness-germ system shows that the reduced
  four-channel first post-leading asymptotic problem is not closed as written.
  The auxiliary source remainder `Q_s` is not controlled by the reduced
  witness-germ channels alone because it depends on the membrane auxiliary
  block through `T_s` and `v`. The auxiliary source remainder `Q_\varphi` is
  not controlled by the reduced witness-germ channels alone because it depends
  on the bending/shear auxiliary block through `M_s` and its companion local
  propagation. Therefore the reduced first post-leading problem must be lifted
  to the smallest fuller local mixed block carrying
  `(u_s, u_n, v, \varphi, \psi, T_s, Q_s, M_s)` in renormalized form if one
  wants theorem-facing first post-leading closure.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_reduced_renormalized_system_draft.md`;
  `docs/theory/current_simple_support_richer_variable_realization_draft.md`;
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/assumptions/assumptions.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`.
- Current status:
  `structural verdict: reduced line not closed / lift to fuller mixed block required`
- What counts as verification:
  a theorem-facing conditional derivation that either closes the reduced source
  remainders from reduced data alone, or proves the lifted first post-leading
  asymptotic closure theorem on the smallest fuller renormalized local mixed
  block.
- Verification method:
  manual structural diagnostic under Assumption LC, reuse of the constitutive
  dependencies and the checked local recurrence model.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only the structural verdict
  that the reduced line is not closed as written.
- Next action:
  formulate and attempt the conditional first post-leading asymptotic closure
  theorem on the smallest fuller renormalized local mixed block carrying
  `(u_s, u_n, v, \varphi, \psi, T_s, Q_s, M_s)`.

### V-S82. Conditional on Assumption LC, the proposed 8-channel fuller renormalized block is not yet a closed first-order system, but one extra `S^{ren}`-level variable is enough

- ID: `V-S82`
- Claim / Hypothesis:
  On the present clean full simple-support branch, a structural closure check
  of the proposed fuller renormalized local mixed block shows:
  `H^{ren}` is eliminable without adding a new local unknown, and
  `\chi^{ren}` is likewise eliminable after substituting the first-order
  relations already present in the flexural block. So no extra `H`-level or
  `\chi`-level state variable is needed. However, the proposed 8-channel block
  `(U,N,V,P,Y,T,Q,M)` is still not a genuinely closed first-order local
  renormalized system, because the membrane side still depends on an explicit
  `S^{ren}`-level quantity and otherwise hides second-order dependence through
  `v`. Therefore the true minimal first-order repair is to add one extra
  `S^{ren}`-level variable, yielding the minimal enlarged block
  `(U,N,V,P,Y,T,Q,M,S^{ren})`.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_fuller_renormalized_block_draft.md`;
  `docs/theory/current_simple_support_reduced_renormalized_system_draft.md`;
  `docs/theory/current_simple_support_richer_variable_realization_draft.md`;
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/assumptions/assumptions.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`.
- Current status:
  `structural verdict: 8-channel block not first-order closed / one extra S-level variable suffices`
- What counts as verification:
  a theorem-facing conditional derivation of a genuinely first-order local
  renormalized system on the minimal enlarged block
  `(U,N,V,P,Y,T,Q,M,S^{ren})`, together with proof that `H^{ren}` and
  `\chi^{ren}` are eliminable from it without enlarging the state further.
- Verification method:
  manual structural diagnostic under Assumption LC, reuse of the checked local
  recurrence model and the fuller-block draft.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only the sharpened
  structural verdict for the conditional fuller local line.
- Next action:
  formulate the minimal 9-channel first-order renormalized local mixed block
  carrying `(U,N,V,P,Y,T,Q,M,S^{ren})`, then attempt conditional first
  post-leading asymptotic closure on that block.

### V-S83. Conditional on Assumption LC, the direct 9-channel first post-leading asymptotic theorem is reduced to regular-singular remainder control on the actual witness germ

- ID: `V-S83`
- Claim / Hypothesis:
  On the present clean full simple-support branch, a direct theorem attempt for
  first post-leading asymptotic closure on the minimal 9-channel first-order
  renormalized local mixed block
  `(U,N,V,P,Y,T,Q,M,S^{ren})` does not yet prove the desired expansions
  `f(x) = f_0 + x f_1 + o(x)` for each channel. But once the 9-channel block
  is written in first-order renormalized form with preserved compatibility
  `Y + nN = 0`, the leading layer and the formal first post-leading linear
  coefficient system are no longer the first blockers on the current branch
  reading; the checked recurrence-side local model already supports that formal
  coefficient system. The first exact analytic blocker is instead regular-
  singular remainder control on the actual punctured local witness germ:
  proving that the renormalized 9-channel witness-germ system matches the
  checked principal local model with sufficiently strong `O(x)` remainder
  control to conclude `f(x) = f_0 + x f_1 + o(x)` for each channel.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_minimal_9channel_block_draft.md`;
  `docs/theory/current_simple_support_fuller_renormalized_block_draft.md`;
  `docs/theory/current_simple_support_reduced_renormalized_system_draft.md`;
  `docs/theory/current_simple_support_richer_variable_realization_draft.md`;
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/assumptions/assumptions.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`.
- Current status:
  `reduced conditionally under LC / first analytic blocker is regular-singular remainder control`
- What counts as verification:
  a theorem-facing conditional proof that the actual punctured local witness
  germ admits a renormalized 9-channel remainder system of regular-singular
  type with strong enough `O(x)` coefficient/source control to imply
  `f(x) = f_0 + x f_1 + o(x)` for each of the 9 channels.
- Verification method:
  manual theorem attempt under Assumption LC, reuse of the checked recurrence-
  side local model and the minimal 9-channel block draft.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only the sharpened
  analytic blocker on the conditional local chart line.
- Next action:
  attempt the conditional regular-singular remainder-control lemma on the
  minimal 9-channel renormalized local mixed block under Assumption LC.

### V-S84. Conditional on Assumption LC, the explicit 9-channel remainder derivation shows that `R(x)=O(x)` is not yet justified because the `T`, `M`, and `S^{ren}` rows still mismatch the chosen principal operator

- ID: `V-S84`
- Claim / Hypothesis:
  On the present clean full simple-support branch, write the minimal
  renormalized witness-germ system in the form
  `x Z'(x) = A_0 Z(x) + R(x)` for
  `Z = (U,N,V,P,Y,T,Q,M,S^{ren})`.
  Then the current repo material does not yet justify a theorem-facing
  `R(x) = O(x)` bound on the actual punctured local witness germ.
  Under the current background expansions and LC scaling orders, the `U`, `N`,
  and derived `Y` rows reduce to `O(x)`. The `V`, `P`, and `Q` rows are only
  plausibly `O(x)` because their exact witness-germ coefficient corrections and
  elimination formulas are not yet packaged sharply enough theorem-facingly.
  The first exact obstruction lies in the `T`, `M`, and `S^{ren}` rows:
  the richer-local C3c audit still exhibits low-order curvature-coupled terms
  such as the `-(s_0 c_0 / r_0^2) M_\theta` contribution in the `T_s` row and
  the `\kappa_{\theta 0}\chi` contribution in the `S` row, and current repo
  material does not reduce those to `O(x)` relative to the chosen principal
  operator `A_0`. So the first analytic blocker is a mismatch between the
  actual witness-germ equations and the currently chosen principal model in
  those rows, rather than resonance of the formal first post-leading system.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_minimal_9channel_block_draft.md`;
  `docs/theory/current_simple_support_fuller_renormalized_block_draft.md`;
  `docs/theory/current_simple_support_reduced_renormalized_system_draft.md`;
  `docs/theory/current_simple_support_richer_variable_realization_draft.md`;
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/assumptions/assumptions.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`.
- Current status:
  `reduced conditionally under LC / first explicit remainder obstruction is T-M-S mismatch with A_0`
- What counts as verification:
  a theorem-facing conditional derivation that either:
  1. proves the `T`, `M`, and `S^{ren}` witness-germ remainder terms are in
     fact `O(x)` relative to the current `A_0`, or
  2. identifies and justifies a corrected principal operator that absorbs those
     low-order curvature-coupled terms and restores an `O(x)` remainder bound.
- Verification method:
  manual remainder derivation under Assumption LC, reuse of the richer-local
  C3c audit and the minimal 9-channel block draft.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only the sharpened
  remainder-level blocker on the conditional local chart line.
- Next action:
  isolate the actual `T`, `M`, and `S^{ren}` witness-germ rows more sharply and
  decide whether their low-order curvature-coupled terms should be proved
  negligible or instead absorbed into a corrected principal operator.

### V-S85. Conditional on Assumption LC, the principal operator must be corrected in the `T` and `S^{ren}` rows, while the `M` row is already principal on the current branch reading

- ID: `V-S85`
- Claim / Hypothesis:
  On the present clean full simple-support branch, a sharper principal-operator
  diagnostic of the 9-channel witness-germ system shows:
  the `T` row contains a genuinely principal curvature-coupled term
  `-(s_0 c_0 / r_0^2) M_\theta`, and the `S^{ren}` row contains a genuinely
  principal curvature-coupled term `\kappa_{\theta 0}\chi`. These terms are
  not removed by any currently available cancellation and therefore should be
  absorbed into a corrected principal operator `A_0^{corr}`.
  By contrast, the `M` row low-order structure
  `M_s' + a_0 M_s - a_0 M_\theta + (n/x) H` is already the principal part
  currently encoded in the 9-channel `M` row, while the `-Q_s` contribution is
  one order lower after renormalization. So the current evidence does not force
  an additional principal correction in the `M` row.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_minimal_9channel_block_draft.md`;
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`.
- Current status:
  `structural verdict: current A_0 is wrong in T/S rows / M row already principal`
- What counts as verification:
  a theorem-facing conditional formulation of a corrected principal operator
  `A_0^{corr}` that modifies the `T` and `S^{ren}` rows by the non-negligible
  curvature-coupled terms, followed by a renewed remainder split against
  `A_0^{corr}`.
- Verification method:
  manual principal-operator diagnostic under Assumption LC, reuse of the richer
  local C3c audit and the 9-channel block draft.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only the sharpened verdict
  about where the principal operator must be corrected on the conditional local
  line.
- Next action:
  formulate the corrected principal operator `A_0^{corr}` for the 9-channel
  block by modifying the `T` and `S^{ren}` rows, then redo the renormalized
  remainder split against `A_0^{corr}`.

### V-S86. Conditional on Assumption LC, after correcting the `T` and `S^{ren}` rows the first blocker is no longer principal-operator choice, but theorem-facing `O(x)` control of the elimination errors for `M_\theta^{ren}`, `H^{ren}`, and `\chi^{ren}`

- ID: `V-S86`
- Claim / Hypothesis:
  On the present clean full simple-support branch, once the corrected principal
  operator `A_0^{corr}` is used for the minimal 9-channel block, no row is
  currently known to leave a non-`O(x)` remainder. The `U`, `N`, `V`, and
  derived `Y` rows are supported as `O(x)` on the current branch reading.
  The `P`, `T`, `Q`, `M`, and `S^{ren}` rows are only plausibly `O(x)` because
  their corrected remainders still depend on theorem-facing control of the
  actual-to-principal elimination errors for `M_\theta^{ren}`, `H^{ren}`, and
  `\chi^{ren}` on the punctured witness germ. Therefore the first blocker
  after principal correction is no longer another defect of the principal
  operator itself, but insufficient theorem-facing justification that those
  elimination errors are `O(x)`.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_minimal_9channel_block_draft.md`;
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / first blocker after correction is elimination-error O(x) control`
- What counts as verification:
  a theorem-facing conditional derivation that the actual-to-principal
  corrections in `M_\theta^{ren}`, `H^{ren}`, and `\chi^{ren}` are `O(x)` on
  the punctured local witness germ, strong enough to make all corrected
  remainder rows `O(x)`.
- Verification method:
  manual corrected-remainder derivation under Assumption LC, reuse of the
  corrected 9-channel principal operator and the richer-local C3c audit.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only the sharpened blocker
  after the principal-operator correction on the conditional local line.
- Next action:
  isolate and prove the `O(x)` control of the actual-to-principal elimination
  errors for `M_\theta^{ren}`, `H^{ren}`, and `\chi^{ren}` on the punctured
  witness germ.

### V-S87. Conditional on Assumption LC, the elimination-error derivation reduces the first blocker further to theorem-facing `O(x)` control of `\Delta M_\theta^{ren}` itself

- ID: `V-S87`
- Claim / Hypothesis:
  On the present clean full simple-support branch, after the corrected
  principal operator `A_0^{corr}` is fixed, a direct elimination-error
  derivation sharpens the blocker further.
  The actual-to-principal twist-moment error `\Delta H^{ren}` reduces
  explicitly on the current branch reading to
  `[\;n(\lambda_{s0}-\lambda_c) P - n x \kappa_{s0} U\;] / C_{tw}` once the
  actual `Y` row is read through the actual `N` row together with preserved
  compatibility `Y + nN = 0`; under the recorded background expansions and LC
  scaling orders this is supported as `O(x)`.
  The actual-to-principal shear error `\Delta \chi^{ren}` then reduces on the
  current branch reading to `n \Delta M_\theta^{ren} + O(x)` after
  substituting that explicit `\Delta H^{ren}` formula together with the actual
  `P`, `Y`, and `U` rows.
  Therefore the first blocker after the corrected-principal split is no longer
  the whole triple
  `(\Delta M_\theta^{ren}, \Delta H^{ren}, \Delta \chi^{ren})`, but the
  theorem-facing `O(x)` control of `\Delta M_\theta^{ren}` itself.
  At the current repo level that control remains only plausible, because the
  exact actual coefficient package in the corrected circumferential /
  twist-shear block is still not article-level fixed sharply enough for a
  closed theorem-facing `O(x)` statement.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_minimal_9channel_block_draft.md`;
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / first blocker after elimination-error derivation is Delta M_theta O(x) control`
- What counts as verification:
  a theorem-facing conditional derivation that the actual-to-principal
  circumferential-bending error `\Delta M_\theta^{ren}` is `O(x)` on the
  punctured witness germ; once that is available, the present branch reading
  already makes `\Delta H^{ren}` supported as `O(x)` and makes
  `\Delta \chi^{ren}` downstream of `\Delta M_\theta^{ren}` up to `O(x)`.
- Verification method:
  manual elimination-error derivation under Assumption LC, reuse of the
  corrected 9-channel principal operator, the current 9-channel draft, and the
  richer-local C3c audit.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only the sharpened blocker
  after splitting the three elimination errors more explicitly on the
  conditional local line.
- Next action:
  isolate and prove theorem-facing `O(x)` control of `\Delta M_\theta^{ren}`
  on the punctured witness germ.

### V-S88. Conditional on Assumption LC, the exact missing ingredient behind `\Delta M_\theta^{ren} = O(x)` is article-level fixation and near-center expansion of the actual circumferential / twist-shear coefficient package

- ID: `V-S88`
- Claim / Hypothesis:
  On the present clean full simple-support branch, after the elimination-error
  split is reduced to the single target `\Delta M_\theta^{ren}`, the current
  branch reading already identifies the exact coefficient form needed for a
  theorem-facing `O(x)` statement.
  The corrected-principal model uses
  `M_\theta^{ren,0} = \nu M + (P + nY)/\Lambda`.
  The active circumferential / twist-shear formulas already reconstruct the
  actual renormalized package more explicitly as
  `M_\theta^{ren,act}
   = \nu M
   + [c_0 / (\Lambda \lambda_{\theta 0})] P
   + [n / (\Lambda \lambda_{\theta 0})] Y
   - [s_0 c_0 / (\Lambda \lambda_{\theta 0}^2)] U
   - [s_0^2 / (\Lambda \lambda_{\theta 0}^2)] N`,
  with the `U`-term already harmless on the current branch reading because its
  coefficient is `O(x)`.
  Therefore
  `\Delta M_\theta^{ren}
   = (a_P(x) - 1/\Lambda) P + (a_Y(x) - n/\Lambda) Y + a_N(x) N`.
  Here
  `a_P(x) = c_0 / (\Lambda \lambda_{\theta 0})`,
  `a_Y(x) = n / (\Lambda \lambda_{\theta 0})`,
  `a_N(x) = - s_0^2 / (\Lambda \lambda_{\theta 0}^2)`.
  Since `s_0 = Kx + O(x^3)`, the `N`-coefficient is already supported as
  `O(x^2)` on the current branch reading.
  So the exact missing ingredient is now narrower than fixation of the whole
  coefficient package: it is theorem-facing near-center fixation of the
  `\lambda_{\theta 0}` normalization inside the actual `P`- and `Y`-
  coefficients, sharp enough to justify
  `c_0/\lambda_{\theta 0} - 1 = O(x)` and `1/\lambda_{\theta 0} - 1 = O(x)` in
  the same local normalization as the corrected-principal model.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_minimal_9channel_block_draft.md`;
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / exact missing ingredient is lambda_theta0-normalization control in the P-Y coefficients`
- What counts as verification:
  a theorem-facing conditional derivation that fixes the actual
  `\lambda_{\theta 0}` normalization in the corrected circumferential /
  twist-shear block sharply enough to prove
  `c_0/\lambda_{\theta 0} - 1 = O(x)` and `1/\lambda_{\theta 0} - 1 = O(x)` on
  the punctured witness germ; once that is available, the current branch
  reading already makes the `U`-term harmless and makes
  `a_N(x) = - s_0^2 / (\Lambda \lambda_{\theta 0}^2)` supported as `O(x^2)`.
- Verification method:
  manual coefficient-package derivation under Assumption LC, reuse of the
  corrected circumferential bending block, the current twist-shear channel
  notation, and the corrected-principal 9-channel line.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only the sharpened
  identification of what is still missing behind the conditional
  `\Delta M_\theta^{ren}` target.
- Next action:
  fix theorem-facingly the near-center `\lambda_{\theta 0}` normalization in
  the actual circumferential / twist-shear block, then re-check the `P`- and
  `Y`-coefficient errors in `\Delta M_\theta^{ren}`.

### V-S89. Conditional on Assumption LC, the principal `P`/`Y` normalization in `M_\theta^{ren}` is still ambiguous between the intrinsic `x \to 0` center line and the selected `x_0`-trace line

- ID: `V-S89`
- Claim / Hypothesis:
  On the present clean full simple-support branch, a normalization-consistency
  check of the `P`- and `Y`-coefficients in `M_\theta^{ren}` shows that
  current repo material does not yet theorem-facingly identify a unique
  principal comparison package. The frozen principal-center line uses
  `c_0 \to 1` and `\lambda_{\theta 0} \to 1`; the richer intrinsic center
  expansion uses `c_0 = 1 + O(x^2)` and
  `\lambda_{\theta 0} = \lambda_c + O(x^2)`; and the theorem-facing clean
  trace convention fixes only `\lambda_{\theta 0}(x_0) = 1` at the selected
  `x_0`-trace layer. Therefore current repo material does not yet decide
  theorem-facingly whether the principal/model `P`- and `Y`-coefficients in
  `M_\theta^{ren}` should remain `1/\Lambda, n/\Lambda` or instead carry the
  intrinsic-center factors `1/(\Lambda \lambda_c), n/(\Lambda \lambda_c)`.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `undecided conditionally under LC / normalization mismatch between intrinsic center and x0-trace lines not yet reconciled`
- What counts as verification:
  a theorem-facing conditional normalization-consistency derivation that
  identifies which normalization governs the punctured witness-germ principal
  `P`/`Y` comparison in `M_\theta^{ren}`:
  either the intrinsic `x \to 0` center package with
  `\lambda_{\theta 0} = \lambda_c + O(x^2)`, or the separately selected
  `x_0`-trace package with `\lambda_{\theta 0}(x_0) = 1`;
  only after that is fixed can the `P`- and `Y`-coefficient errors in
  `\Delta M_\theta^{ren}` be stated against a uniquely chosen principal model.
- Verification method:
  manual source-formula comparison and normalization tracking across the active
  circumferential / twist-shear reconstruction, the richer intrinsic center
  expansion, and the selected theorem-facing `x_0`-trace convention.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It only records the sharpened fact
  that the remaining `P`/`Y` issue is not yet a pure `O(x)` coefficient
  estimate because the principal normalization itself is still ambiguous at the
  current theorem-facing repo level.
- Next action:
  formulate a theorem-facing normalization-consistency lemma reconciling the
  punctured `x \to 0` intrinsic center normalization with the selected
  `x_0`-trace normalization, then re-check whether the principal/model
  `P`/`Y` coefficients in `M_\theta^{ren}` should be
  `1/\Lambda, n/\Lambda` or `1/(\Lambda \lambda_c), n/(\Lambda \lambda_c)`.

### V-S90. Conditional on Assumption LC, the current blocker can be organized as a three-line normalization map, and the exact unresolved theorem-facing choice is which line governs the principal `P`/`Y` coefficients in `M_\theta^{ren,0}`

- ID: `V-S90`
- Claim / Hypothesis:
  On the present clean full simple-support branch, the remaining
  normalization-consistency blocker is best organized by a three-line map:
  `A. intrinsic center normalization`:
  the punctured `x \to 0` local geometry line with
  `c_0 = 1 + O(x^2)` and `\lambda_{\theta 0} = \lambda_c + O(x^2)`;
  `B. frozen principal-center normalization`:
  the helper/principal simplification line with
  `c_0 \to 1` and `\lambda_{\theta 0} \to 1`;
  `C. selected x_0`-trace normalization:
  the criterion/selected-family/trace-side convention with
  `\lambda_{\theta 0}(x_0) = 1`.
  The theorem-facing unresolved choice is then:
  for the principal/model comparison in `M_\theta^{ren}`, should the `P`- and
  `Y`-coefficients be governed by the intrinsic punctured-center line, which
  suggests `1/(\Lambda \lambda_c), n/(\Lambda \lambda_c)`, by an explicitly
  gauge-fixed local normalization with `\lambda_c = 1`, or by a theorem-facing
  bridge from the selected `x_0`-trace line?
  The selected `x_0`-trace normalization belongs to the criterion/trace layer
  and must not be silently substituted for the local punctured-center
  normalization in the principal operator unless such a bridge lemma is stated.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `docs/theory/current_simple_support_minimal_9channel_block_draft.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `undecided conditionally under LC / current blocker organized as normalization-map choice, not yet as a closed coefficient estimate`
- What counts as verification:
  a theorem-facing conditional statement that fixes which one of the three
  normalization lines governs the principal `P`/`Y` coefficients in
  `M_\theta^{ren,0}`, and if the selected `x_0`-trace line is used, states the
  explicit bridge from that trace layer to the local punctured-center theorem
  line.
- Verification method:
  manual normalization tracking across the intrinsic center expansion, the
  helper-level principal model, the active circumferential / twist-shear
  reconstruction, and the selected `x_0`-trace convention.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only the sharpened fact
  that the remaining issue is now an unresolved normalization-map choice.
- Next action:
  decide theorem-facingly which normalization line governs the principal `P`-
  and `Y`-coefficients in `M_\theta^{ren,0}`, then only after that reopen the
  corresponding coefficient-error estimate in `\Delta M_\theta^{ren}`.

### V-S91. Conditional on Assumption LC, the intrinsic punctured-center normalization should be used as the master normalization for the local `x \to 0` theorem line, while the selected `x_0`-trace normalization remains a separate criterion-side layer that still needs an explicit bridge

- ID: `V-S91`
- Claim / Hypothesis:
  On the present clean full simple-support branch, the master theorem-facing
  normalization for the punctured local `x \to 0` line should be the intrinsic
  punctured-center normalization, not the frozen helper normalization and not
  the selected `x_0`-trace normalization.
  The reason is structural:
  the local theorem line is posed on the punctured witness germ itself;
  the active renormalized circumferential / twist-shear reconstruction is
  naturally expressed in the intrinsic center variables with
  `\lambda_{\theta 0} = \lambda_c + O(x^2)`;
  the repo does not currently contain a separate theorem-facing gauge-fixing
  strong enough to justify setting `\lambda_c = 1` on that local line; and the
  selected `x_0`-trace normalization belongs to the criterion/trace layer,
  where current repo material only fixes `\lambda_{\theta 0}(x_0) = 1` and
  explicitly warns that this does not yet determine a full intrinsic
  `x \to 0` selector.
  Therefore the candidate local principal/model package is
  `M_\theta^{ren,0,loc} = \nu M + (P + nY)/(\Lambda \lambda_c)`,
  while a separate theorem-to-criterion bridge to the selected `x_0`-trace
  layer must still be stated explicitly later.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `docs/theory/current_simple_support_minimal_9channel_block_draft.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `chosen conditionally under LC / intrinsic center normalization is the master local line, separate x0-trace bridge still required`
- What counts as verification:
  1. a theorem-facing conditional rewrite of the local principal/model
     comparison using
     `M_\theta^{ren,0,loc} = \nu M + (P + nY)/(\Lambda \lambda_c)`,
     followed by the corresponding re-check of `\Delta M_\theta^{ren}` on the
     punctured witness germ;
  2. a separate theorem-to-criterion bridge statement relating that intrinsic
     local normalization to the selected `x_0`-trace normalization when the
     local line is projected back to the criterion/trace layer.
- Verification method:
  manual normalization decision based on the current witness-germ framing, the
  active circumferential / twist-shear reconstruction, and the explicit trace-
  layer warning already recorded on the branch.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It only fixes the current master
  normalization for the conditional local theorem line and keeps the criterion-
  side bridge as a separate unresolved task.
- Next action:
  rewrite the local `\Delta M_\theta^{ren}` comparison against
  `M_\theta^{ren,0,loc} = \nu M + (P + nY)/(\Lambda \lambda_c)`, and state
  separately the needed theorem-to-criterion bridge to the selected
  `x_0`-trace layer.

### V-S92. Conditional on Assumption LC, after switching to the intrinsic local principal package one has `\Delta M_\theta^{ren} = O(x)` on the current branch reading, so the elimination-error blocker is no longer first on the corrected 9-channel system

- ID: `V-S92`
- Claim / Hypothesis:
  On the present clean full simple-support branch, work on the punctured local
  witness germ in the intrinsic center normalization and compare
  `M_\theta^{ren,act}` against
  `M_\theta^{ren,0,loc} = \nu M + (P + nY)/(\Lambda \lambda_c)`.
  Then
  `\Delta M_\theta^{ren}
   = [\,(c_0/\lambda_{\theta 0}) - (1/\lambda_c)\,] P / \Lambda
   + n[\,(1/\lambda_{\theta 0}) - (1/\lambda_c)\,] Y / \Lambda
   - [s_0 c_0 / (\Lambda \lambda_{\theta 0}^2)] U
   - [s_0^2 / (\Lambda \lambda_{\theta 0}^2)] N`.
  Using the current intrinsic-center expansions
  `c_0 = 1 + O(x^2)`,
  `\lambda_{\theta 0} = \lambda_c + O(x^2)`,
  `s_0 = Kx + O(x^3)`,
  one gets on the current branch reading
  `c_0/\lambda_{\theta 0} - 1/\lambda_c = O(x^2)`,
  `1/\lambda_{\theta 0} - 1/\lambda_c = O(x^2)`,
  the `U`-coefficient as `O(x)`, and the `N`-coefficient as `O(x^2)`.
  Since the renormalized channels are bounded in the LC scaling class, this
  supports `\Delta M_\theta^{ren} = O(x)` on the intrinsic local line.
  Therefore, together with the already recorded
  `\Delta H^{ren} = O(x)` and
  `\Delta \chi^{ren} = n \Delta M_\theta^{ren} + O(x)`, the corrected
  elimination errors are no longer the first blocker on the corrected
  9-channel system; the next blocker becomes the regular-singular first-
  correction argument itself.
- Type: `formula-level claim`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `docs/theory/current_simple_support_minimal_9channel_block_draft.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `supported conditionally under LC / intrinsic-local Delta M_theta is O(x), elimination-error blocker removed`
- What counts as verification:
  a theorem-facing conditional rewrite of the corrected 9-channel remainder
  system using the intrinsic local principal package
  `M_\theta^{ren,0,loc} = \nu M + (P + nY)/(\Lambda \lambda_c)`, followed by a
  regular-singular first-correction argument proving
  `Z(x) = Z_0 + x Z_1 + o(x)` for the corrected 9-channel state.
- Verification method:
  manual intrinsic-local coefficient derivation under Assumption LC, using the
  active circumferential / twist-shear reconstruction and the recorded
  intrinsic center expansions.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict
  ambient-to-local continuation theorem, and does not itself prove first
  post-leading asymptotic closure. It only records that the earlier
  `\Delta M_\theta^{ren}` elimination-error blocker is no longer first once the
  intrinsic local normalization is used.
- Next action:
  rewrite the corrected 9-channel remainder split entirely against
  `M_\theta^{ren,0,loc} = \nu M + (P + nY)/(\Lambda \lambda_c)` and attempt the
  regular-singular first-correction step itself.

### V-S93. Conditional on Assumption LC, a direct theorem attempt for the corrected intrinsic-local 9-channel first-correction step is reduced to the no-log spectral lemma for the bounded compatibility-preserving sector of `A_{0,loc}^{corr}`

- ID: `V-S93`
- Claim / Hypothesis:
  On the present clean full simple-support branch, rewrite the corrected
  intrinsic-local 9-channel witness-germ system in the form
  `x Z'(x) = A_{0,loc}^{corr} Z(x) + R_{loc}(x)` with preserved compatibility
  `Y + nN = 0`.
  After the intrinsic-local principal choice, the corrected remainder split is
  no longer blocked first by source packaging, normalization choice, or the
  `M_\theta^{ren}` elimination-error target:
  the current branch reading now supports `\Delta M_\theta^{ren} = O(x)`,
  together with the already recorded `\Delta H^{ren} = O(x)` and
  `\Delta \chi^{ren} = n \Delta M_\theta^{ren} + O(x)`.
  But a direct theorem attempt for first post-leading closure on this corrected
  intrinsic-local system still does not yet prove
  `Z(x) = Z_0 + x Z_1 + o(x)`.
  The first exact analytic blocker is now the theorem-facing regular-singular
  first-correction argument itself.
  More sharply, the proof no longer fails first at leading-state extraction,
  the formal first post-leading coefficient system, or the corrected
  intrinsic-local `O(x)` remainder split.
  It fails first at the missing no-log spectral lemma for the bounded
  compatibility-preserving sector of the corrected intrinsic-local operator
  `A_{0,loc}^{corr}`, namely the statement that every bounded witness-germ
  solution satisfying the preserved compatibility relation admits the affine
  first correction with no logarithmic or other additional bounded
  first-correction terms.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/current_simple_support_minimal_9channel_block_draft.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / exact first blocker is the no-log spectral lemma for the bounded compatibility-preserving sector`
- What counts as verification:
  a theorem-facing conditional proof that every bounded solution of the
  corrected intrinsic-local regular-singular system
  `x Z'(x) = A_{0,loc}^{corr} Z(x) + O(x)` in the compatibility-preserving
  sector `Y + nN = 0` admits
  `Z(x) = Z_0 + x Z_1 + o(x)`,
  with no logarithmic or other additional bounded first-correction terms.
- Verification method:
  manual regular-singular analysis of the corrected intrinsic-local operator,
  reuse of the corrected remainder split and the existing formal first post-
  leading coefficient structure.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only that the old
  structural / normalization / elimination-error block chain has been cleared
  on the current conditional local line, and that the next blocker is now the
  final regular-singular first-correction step itself.
- Next action:
  formulate and prove the no-log spectral lemma for the bounded
  compatibility-preserving sector of `A_{0,loc}^{corr}`, then use it to close
  the first post-leading affine expansion
  `Z(x) = Z_0 + x Z_1 + o(x)`.

### V-S94. Conditional on Assumption LC, the checked bounded compatibility-preserving sector of `A_{0,loc}^{corr}` does not currently exhibit a log-producing Jordan degeneracy; the next blocker is the bounded-solution / variation-of-constants step

- ID: `V-S94`
- Claim / Hypothesis:
  On the present clean full simple-support branch, consider the corrected
  intrinsic-local regular-singular system
  `x Z'(x) = A_{0,loc}^{corr} Z(x) + O(x)` in the bounded
  compatibility-preserving sector `Y + nN = 0`.
  The checked spectral picture currently supported by the repo is:
  1. bounded leading states lie in the compatibility-preserving kernel of the
     corrected intrinsic-local principal operator;
  2. at the first post-leading checked layer, the recurrence leaves exactly
     one genuine membrane `x`-mode parameter `T1`, with
     `U1 = \alpha T1`, `V1 = \beta T1`, while the flexural coefficients are
     uniquely zero under the same nonresonance condition as before;
  3. the resonance denominator `(n-2)(n+1)` is nonzero on the current
     physical branch `n > 2`;
  4. once that genuine membrane mode is admitted, the next checked layer
     closes uniquely to zero.
  Therefore the current checked spectral data do not exhibit a bounded
  log-producing Jordan direction in the compatibility-preserving sector.
  The remaining open point is not another spectral repair, but the theorem-
  facing argument that converts this checked spectral picture together with the
  corrected `O(x)` remainder split into the affine expansion
  `Z(x) = Z_0 + x Z_1 + o(x)`.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/current_simple_support_minimal_9channel_block_draft.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `supported conditionally under LC / no checked bounded-sector log-producing Jordan degeneracy, next blocker is bounded-solution step`
- What counts as verification:
  1. a theorem-facing derivation that the bounded compatibility-preserving
     sector of `A_{0,loc}^{corr}` has no logarithmic first-correction mode;
  2. a theorem-facing bounded-solution / variation-of-constants lemma turning
     `x Z'(x) = A_{0,loc}^{corr} Z(x) + O(x)` into
     `Z(x) = Z_0 + x Z_1 + o(x)` on that sector.
- Verification method:
  manual spectral audit of the checked first and second post-leading
  recurrences, together with manual regular-singular analysis of the corrected
  intrinsic-local operator.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only that, on the current
  branch reading, the checked spectral obstruction is no longer first.
- Next action:
  prove the bounded-solution / variation-of-constants lemma for the corrected
  intrinsic-local regular-singular system on the compatibility-preserving
  bounded sector.

### V-S95. Conditional on Assumption LC, the first exact blocker inside the bounded-solution step is the compatibility-preserving projector / variation-of-constants lemma that extracts `Z_0` and keeps `W = (Z-Z_0)/x` bounded

- ID: `V-S95`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  Let
  `Z = (U,N,V,P,Y,T,Q,M,S^{ren})`
  be a bounded corrected intrinsic-local witness-germ solution on `(0,\delta)`
  satisfying the preserved compatibility relation `Y + nN = 0`, and suppose
  the corrected intrinsic-local system has already been rewritten as
  `x Z'(x) = A_{0,loc}^{corr} Z(x) + x b(x)` with `b` bounded.
  The operator used in the attempted regular-singular proof is the frozen
  corrected intrinsic-local 9-channel principal matrix, restricted to the
  compatibility-preserving sector.
  On the current branch reading, the checked recurrence-side spectral picture
  already supports the following heuristic decomposition of the bounded sector:
  bounded leading states should lie in
  `\ker A_{0,loc}^{corr}`,
  the only checked bounded first-correction mode is the genuine membrane
  `x`-mode in
  `\ker(A_{0,loc}^{corr} - I)`,
  and no checked bounded log-producing Jordan direction is currently visible.
  If that decomposition were available theorem-facingly together with a
  spectral gap
  `\Re \sigma(A_{0,loc}^{corr}|_{E_{>1}}) > 1`
  on the remaining bounded sector, then the standard variation-of-constants
  argument would yield
  `Z(x) = Z_0 + x Z_1 + o(x)`.
  But the proof still fails one step earlier:
  the repo does not yet contain the needed compatibility-preserving projector /
  dichotomy lemma proving from boundedness alone that
  `Z - Z_0 = O(x)` for some
  `Z_0 \in \ker A_{0,loc}^{corr}`
  and that the transformed unknown
  `W(x) = (Z(x) - Z_0)/x`
  stays bounded.
  Equivalently, the exact first blocker inside the bounded-solution step is
  the missing theorem-facing exclusion of hidden bounded non-affine
  first-correction behavior on that sector.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/current_simple_support_minimal_9channel_block_draft.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / exact first blocker inside bounded-solution step is the compatibility-preserving projector-dichotomy lemma`
- What counts as verification:
  a theorem-facing proof on the bounded compatibility-preserving sector of the
  corrected intrinsic-local operator that every bounded solution of
  `x Z'(x) = A_{0,loc}^{corr} Z(x) + x b(x)` admits
  `Z_0 \in \ker A_{0,loc}^{corr}` with `Z - Z_0 = O(x)`,
  that `W = (Z-Z_0)/x` remains bounded and has leading state in
  `\ker(A_{0,loc}^{corr} - I)`,
  and therefore that
  `Z(x) = Z_0 + x Z_1 + o(x)`
  with no hidden bounded non-affine first correction.
- Verification method:
  manual regular-singular / variation-of-constants proof attempt using the
  corrected intrinsic-local remainder split together with the checked membrane
  `x`-mode and no-log spectral evidence.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only the sharper location
  of the first missing lemma inside the already isolated bounded-solution
  step.
- Next action:
  formulate and prove the compatibility-preserving projector /
  variation-of-constants lemma for `A_{0,loc}^{corr}` on the bounded sector,
  strong enough to extract `Z_0`, control `W = (Z-Z_0)/x`, and exclude hidden
  bounded non-affine corrections.

### V-S96. Conditional on Assumption LC, a matrix/projector audit reduces the projector lemma further to a missing direct-sum / spectral-gap theorem for `A_{comp} := A_{0,loc}^{corr}|_{E_{comp}}`

- ID: `V-S96`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  Let
  `E_{comp} = {Z = (U,N,V,P,Y,T,Q,M,S^{ren}) : Y + nN = 0}`.
  Since the principal `N` and `Y` rows satisfy
  `x(Y+nN)' = -n(Y+nN)`,
  this compatibility subspace is invariant for the corrected intrinsic-local
  principal flow and therefore for the restricted operator
  `A_{comp} := A_{0,loc}^{corr}|_{E_{comp}}`.
  In the reduced coordinates
  `(U,N,V,P,T,Q,M,S^{ren})`
  with `Y = -nN`, the matrix/projector target is to identify the bounded
  generalized-eigenspace of `A_{comp}`.
  The current checked repo evidence supports the following candidate low
  spectral picture on that restricted space:
  1. the already closed selected leading trace plane gives the candidate
     `0`-eigenspace block `E_0`;
  2. the checked first post-leading membrane mode gives the candidate
     `1`-eigenspace block `E_1`;
  3. the checked second layer does not exhibit a Jordan continuation of that
     membrane `1`-mode.
  But this is still not a theorem-facing direct-sum theorem for the actual
  restricted matrix.
  The repo does not yet prove that the bounded sector of `A_{comp}` is exactly
  `E_{bd} = E_0 \oplus E_1 \oplus E_{>1}`,
  with no extra bounded spectrum `0 < \Re \lambda < 1`,
  no Jordan block at `0` or `1`, and
  `\Re \sigma(A_{comp}|_{E_{>1}}) > 1`.
  Therefore the exact first matrix-level blocker is now sharper than a later
  variation-of-constants estimate:
  before constructing the needed projectors, one still needs the restricted
  direct-sum / spectral-gap theorem for `A_{comp}` itself.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/current_simple_support_minimal_9channel_block_draft.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / exact first matrix-level blocker is the restricted direct-sum and spectral-gap theorem for A_comp`
- What counts as verification:
  a theorem-facing derivation of the restricted matrix
  `A_{comp} := A_{0,loc}^{corr}|_{E_{comp}}` proving all of:
  1. `E_0 = \ker A_{comp}` is exactly the compatibility-preserving leading
     block already seen in the selected leading trace;
  2. `E_1 = \ker(A_{comp} - I)` is exactly the genuine membrane `x`-mode and is
     semisimple;
  3. there is no additional bounded spectrum with
     `0 < \Re \lambda < 1`;
  4. the remaining restricted spectrum satisfies
     `\Re \sigma(A_{comp}|_{E_{>1}}) > 1`.
  Only after that can one define the projectors needed to prove
  `Z_0 \in \ker A_{comp}`, `Z - Z_0 = O(x)`, boundedness of
  `W = (Z-Z_0)/x`, and the affine first correction.
- Verification method:
  manual matrix/projector audit using the exact compatibility relation, the
  selected leading-trace recovery, the checked first post-leading membrane
  mode, and the checked second-layer closure.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only the sharper
  matrix-level location of the first missing theorem inside the already
  isolated bounded-solution step.
- Next action:
  formulate the explicit restricted operator
  `A_{comp} := A_{0,loc}^{corr}|_{E_{comp}}`,
  identify its low spectral blocks theorem-facingly, prove the direct-sum /
  spectral-gap statement, and only then return to the final projector /
  variation-of-constants estimate.

### V-S97. Conditional on Assumption LC, an explicit-matrix packaging pass fixes the corrected `T` row and writes the full restricted 8x8 matrix `A_{comp}` theorem-facingly

- ID: `V-S97`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  On the compatibility-preserving slice
  `E_{comp} = {Y + nN = 0}`,
  use the reduced coordinates
  `(U,N,V,P,T,Q,M,S^{ren})`
  with `Y = -nN`.
  Then the intrinsic-local principal package already determines explicitly:
  `T_{\theta,comp}^{ren} = \nu T + U + nV`,
  `M_{\theta,comp}^{ren,0,loc}
   = \nu M + (P - n^2 N)/(\Lambda \lambda_c)`,
  `H_{comp}^{ren,0,loc}
   = n[\,2N + (\lambda_c - 1)P\,]/C_{tw}`,
  and
  `\chi_{comp}^{ren,0,loc}
   = n M_{\theta,comp}^{ren,0,loc}
   + n[(\lambda_c + 1)P
   - (\lambda_c - 1)\Lambda(M - \nu M_{\theta,comp}^{ren,0,loc})]/C_{tw}`.
  Therefore the restricted `U`, `N`, `V`, `P`, `Q`, `M` rows and the
  `\kappa_{\theta 0}\chi` contribution in the `S^{ren}` row are already
  writable explicitly on `E_{comp}`.
  The corrected `T` row is now fixed as well:
  in the live corrected `T_s` source,
  `-(s_0 c_0 / r_0^2) M_\theta`,
  the intrinsic-local center expansions
  `s_0 = Kx + O(x^3)`,
  `c_0 = 1 + O(x^2)`,
  `r_0 = \lambda_c x + O(x^3)`
  give
  `s_0 c_0 / r_0^2 = K / (\lambda_c^2 x) + O(x)`,
  so after moving that source from the residual side to the evolution equation
  and renormalizing, the constant corrected principal term is
  `+(K/\lambda_c^2) M_\theta^{ren,0,loc}`;
  hence
  `c_T^{loc} = K/\lambda_c^2`,
  and the corrected `T` row on `E_{comp}` becomes
  `xT'
   = U
   - [K n^2 / (\Lambda \lambda_c^3)] N
   + nV
   + [K / (\Lambda \lambda_c^3)] P
   + (\nu - n)T
   + [K \nu / \lambda_c^2] M
   - n S^{ren}`.
  Therefore the full restricted constant 8x8 matrix
  `A_{comp} := A_{0,loc}^{corr}|_{E_{comp}}`
  is theorem-facingly fixed in the coordinates
  `(U,N,V,P,T,Q,M,S^{ren})` as
  `A_{comp} =`
  \[
  \begin{pmatrix}
  -(n+\nu) & 0 & -n\nu & 0 & 1-\nu^2 & 0 & 0 & 0 \\
  0 & -n & 0 & -\lambda_c & 0 & 0 & 0 & 0 \\
  n & 0 & -(n-1) & 0 & 0 & 0 & 0 & 2(1+\nu) \\
  0 & \nu n^2/\lambda_c & 0 & -(n-1)-\nu/\lambda_c & 0 & 0 & \Lambda(1-\nu^2) & 0 \\
  1 & -K n^2/(\Lambda \lambda_c^3) & n & K/(\Lambda \lambda_c^3) & \nu-n & 0 & K\nu/\lambda_c^2 & -n \\
  0 &
    n^4\!\left[\frac{1}{\Lambda \lambda_c} + \frac{\nu(\lambda_c-1)}{\lambda_c C_{tw}}\right] &
    0 &
    -n^2\!\left[\frac{1}{\Lambda \lambda_c} + \frac{\lambda_c+1}{C_{tw}} + \frac{\nu(\lambda_c-1)}{\lambda_c C_{tw}}\right] &
    0 & -(n-1) &
    -n^2\!\left[\nu - \frac{(\lambda_c-1)\Lambda(1-\nu^2)}{C_{tw}}\right] &
    0 \\
  0 &
    -n^2\!\left[\frac{1}{\Lambda \lambda_c} + \frac{2}{C_{tw}}\right] &
    0 &
    \frac{1}{\Lambda \lambda_c} - \frac{n^2(\lambda_c-1)}{C_{tw}} &
    0 & 0 &
    \nu - n + 1 &
    0 \\
  n &
    K n^3\!\left[\frac{1}{\Lambda \lambda_c^2} + \frac{\nu(\lambda_c-1)}{\lambda_c^2 C_{tw}}\right] &
    n^2 &
    -K n\!\left[\frac{1}{\Lambda \lambda_c^2} + \frac{\lambda_c+1}{\lambda_c C_{tw}} + \frac{\nu(\lambda_c-1)}{\lambda_c^2 C_{tw}}\right] &
    n\nu & 0 &
    -\frac{K n}{\lambda_c}\!\left[\nu - \frac{(\lambda_c-1)\Lambda(1-\nu^2)}{C_{tw}}\right] &
    -(n+1)
  \end{pmatrix}.
  \]
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/current_simple_support_minimal_9channel_block_draft.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `supported conditionally under LC / full explicit 8x8 restricted matrix packaged`
- What counts as verification:
  the theorem-facing derivation above:
  explicit intrinsic-local renormalization of the corrected `T`-row source,
  extraction of `c_T^{loc} = K/\lambda_c^2`,
  and explicit writing of the full reduced constant 8x8 matrix
  `A_{comp}` in the coordinates `(U,N,V,P,T,Q,M,S^{ren})`.
- Verification method:
  manual restricted-matrix derivation using the minimal 9-channel block, the
  intrinsic-local principal package, the corrected-principal `T`/`S^{ren}`
  diagnostic, and the live surrogate source formulas.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only that the full matrix
  `A_{comp}` is now fixed theorem-facingly enough that the next remaining
  local question is the genuine restricted spectral audit.
- Next action:
  perform the restricted spectral-gap / direct-sum audit for `A_{comp}`:
  identify `\ker A_{comp}` and `\ker(A_{comp}-I)`, prove semisimplicity at `0`
  and `1`, and exclude spectrum with `0 < \Re \lambda < 1`.

### V-S98. Conditional on Assumption LC, after explicit packaging of `A_{comp}` the exact next blocker is the genuine restricted spectral audit of that 8x8 matrix

- ID: `V-S98`
- Claim / Hypothesis:
  On the present clean full simple-support branch, once the corrected `T` row
  is frozen and the full constant 8x8 restricted matrix
  `A_{comp} := A_{0,loc}^{corr}|_{E_{comp}}`
  is written explicitly, the matrix-packaging blocker is removed.
  The exact next theorem-facing target is now the restricted spectral audit of
  that explicit matrix:
  1. identify `\ker A_{comp}` theorem-facingly;
  2. identify `\ker(A_{comp}-I)` theorem-facingly;
  3. exclude Jordan blocks at `0` and `1`;
  4. exclude any spectrum with `0 < \Re \lambda < 1`.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/current_simple_support_minimal_9channel_block_draft.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / next blocker is the explicit restricted spectral-gap and semisimplicity audit`
- What counts as verification:
  a theorem-facing spectral audit of the explicit 8x8 matrix `A_{comp}` proving
  the direct-sum decomposition of its bounded sector into
  `\ker A_{comp} \oplus \ker(A_{comp}-I) \oplus E_{>1}`,
  with no Jordan blocks at `0` or `1` and no spectrum with
  `0 < \Re \lambda < 1`.
- Verification method:
  manual matrix-spectrum analysis of the explicit restricted matrix,
  using the checked membrane `x`-mode and checked second-layer closure as
  support but not as a substitute for the actual theorem-facing matrix proof.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only the exact next local
  theorem-facing target after the explicit matrix packaging step.
- Next action:
  perform the restricted spectrum / semisimplicity audit on the explicit matrix
  `A_{comp}` itself.

### V-S99. Conditional on Assumption LC, the explicit `8 \times 8` spectral audit reduces the bounded-sector question to the `3 \times 3` flexural block `G_{flex}`, while the membrane block and the `Q` scalar are already fully audited

- ID: `V-S99`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  Take the explicit restricted matrix
  `A_{comp} := A_{0,loc}^{corr}|_{E_{comp}}`
  already written in the coordinates `(U,N,V,P,T,Q,M,S^{ren})`.
  After permuting the coordinates to
  `(N,P,M,Q,U,V,T,S^{ren})`,
  that matrix is block lower triangular with diagonal blocks
  \[
  G_{flex}
  =
  \begin{pmatrix}
  -n & -\lambda_c & 0 \\
  \nu n^2/\lambda_c & -(n-1)-\nu/\lambda_c & \Lambda(1-\nu^2) \\
  -n^2\!\left[\frac{1}{\Lambda \lambda_c} + \frac{2}{C_{tw}}\right] &
  \frac{1}{\Lambda \lambda_c} - \frac{n^2(\lambda_c-1)}{C_{tw}} &
  \nu - n + 1
  \end{pmatrix},
  \]
  the scalar `Q` eigenvalue `-(n-1)`, and
  \[
  B_{mem}
  =
  \begin{pmatrix}
  -(n+\nu) & -n\nu & 1-\nu^2 & 0 \\
  n & -(n-1) & 0 & 2(1+\nu) \\
  1 & n & \nu-n & -n \\
  n & n^2 & n\nu & -(n+1)
  \end{pmatrix}.
  \]
  A direct determinant computation for the membrane block gives
  \[
  \det(B_{mem} - \lambda I)
  =
  (\lambda-1)(\lambda+1)(\lambda+2n-1)(\lambda+2n+1).
  \]
  Therefore the membrane spectrum is exactly
  `{1,-1,1-2n,-(2n+1)}`, the membrane `\lambda=1` mode is simple and
  semisimple, and the membrane block has no spectrum with
  `0 < \Re \lambda < 1`.
  Together with the scalar `Q` eigenvalue `-(n-1)`, this proves that every
  remaining bounded-sector uncertainty for the full `8 \times 8` matrix is
  concentrated entirely in `G_{flex}`.
  In particular:
  1. the checked membrane `x`-mode is now theorem-facingly matched by the
     explicit membrane eigenvalue `\lambda=1`;
  2. the current checked absence of a membrane-side Jordan continuation is
     consistent with the explicit distinct membrane eigenvalues;
  3. if the expected leading `\lambda=0` block exists for the explicit local
     operator, it must come from `G_{flex}` alone.
  So the full direct-sum / spectral-gap theorem is still open, but no longer
  at the level of the whole `8 \times 8` matrix:
  the exact remaining spectral task is now the theorem-facing audit of the
  flexural block `G_{flex}` itself.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/current_simple_support_minimal_9channel_block_draft.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / membrane block and Q scalar fully audited, exact remaining spectral blocker is the 3x3 flexural block G_flex`
- What counts as verification:
  a theorem-facing flexural spectral audit proving all remaining points for
  `G_{flex}`:
  1. compute `\ker G_{flex}` and match it to the expected leading
     `\lambda=0` block, if nontrivial;
  2. prove `1 \notin \sigma(G_{flex})`;
  3. exclude any spectrum with `0 < \Re \lambda < 1`;
  4. if `0 \in \sigma(G_{flex})`, prove semisimplicity at `\lambda=0`.
  Since the membrane block and the scalar `Q` eigenvalue are already explicit,
  those four flexural items are now exactly equivalent to the remaining bounded-
  sector theorem for the full `A_{comp}`.
- Verification method:
  manual block-triangular spectral reduction of the explicit `8 \times 8`
  matrix, direct determinant computation for the membrane block, and
  comparison with the checked first and second post-leading recurrence picture.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only that the `8 \times 8`
  spectral audit now reduces the open low-spectrum question to the explicit
  flexural block `G_{flex}`.
- Next action:
  audit the flexural block `G_{flex}` theorem-facingly:
  compute `\ker G_{flex}`, prove `1 \notin \sigma(G_{flex})`, and exclude
  `0 < \Re \lambda < 1`.

### V-S100. Conditional on Assumption LC, the flexural block `G_{flex}` now has explicit determinant and characteristic-polynomial packaging; the exact remaining blocker is the sign/factorization analysis of that cubic

- ID: `V-S100`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  Take the flexural block
  \[
  G_{flex}
  =
  \begin{pmatrix}
  -n & -\lambda_c & 0 \\
  \nu n^2/\lambda_c & -(n-1)-\nu/\lambda_c & \Lambda(1-\nu^2) \\
  -n^2\!\left[\frac{1}{\Lambda \lambda_c} + \frac{2}{C_{tw}}\right] &
  \frac{1}{\Lambda \lambda_c} - \frac{n^2(\lambda_c-1)}{C_{tw}} &
  \nu - n + 1
  \end{pmatrix}
  \]
  already extracted from the explicit restricted matrix `A_{comp}`.
  Since `\Lambda = (1-\nu) C_{tw}`, the similarity scaling
  `\widetilde G_{flex}
   = \operatorname{diag}(1,1,\Lambda)\, G_{flex}\,
     \operatorname{diag}(1,1,\Lambda)^{-1}`
  removes `\Lambda` from the third column and yields
  \[
  \widetilde G_{flex}
  =
  \begin{pmatrix}
  -n & -\lambda_c & 0 \\
  \nu n^2/\lambda_c & -(n-1)-\nu/\lambda_c & 1-\nu^2 \\
  -n^2\!\left[\frac{1}{\lambda_c} + 2(1-\nu)\right] &
  \frac{1}{\lambda_c} - n^2(1-\nu)(\lambda_c-1) &
  \nu - n + 1
  \end{pmatrix},
  \]
  which has the same spectrum as `G_{flex}`.
  Writing `c_\nu := (1-\nu)^2(1+\nu)`, one gets the explicit cubic
  \[
  \chi_{flex}(\lambda)
  :=
  \det(\widetilde G_{flex} - \lambda I)
  =
  -(n+\lambda)\Bigl(
    (n-1+\lambda)^2
    - \frac{\nu(\lambda_c-1)}{\lambda_c}(n-1+\lambda)
    - \frac{1}{\lambda_c}
    + n^2 c_\nu (\lambda_c-1)
  \Bigr)
  +
  n^2\Bigl(
    1 - \nu(n-1+\lambda) + 2\lambda_c c_\nu
  \Bigr).
  \]
  Therefore
  \[
  \lambda_c \det G_{flex}
  =
  n^2(2-n)c_\nu \lambda_c^2
  +
  n\Bigl(
    n^2 c_\nu - n^2 + 3n - 1 - \nu (n-1)^2
  \Bigr)\lambda_c
  +
  n\bigl(1-\nu(n-1)\bigr),
  \]
  and
  \[
  \lambda_c \det(G_{flex}-I)
  =
  -n^2(n-1)c_\nu \lambda_c^2
  +
  \Bigl(
    n^2(n+1)c_\nu - n\bigl(n^2(1+\nu)-\nu(n+1)\bigr)
  \Bigr)\lambda_c
  -
  (n+1)(n\nu-1).
  \]
  The theorem-facing parameter regime currently recorded on this clean branch
  is only the coarse positivity package
  `\lambda_c > 0`, `\nu > 0`, active nonshallow clean modes `n \ge 4`,
  `C_{tw} = 12(1+\nu)\mu^2 > 0`, and
  `\Lambda = 12(1-\nu^2)\mu^2 = (1-\nu)C_{tw}`;
  the repo does not yet record a sharper branch inequality linking
  `\lambda_c` to `(n,\nu)` strongly enough to decide those two quadratic tests
  or the Hurwitz determinants of `\chi_{flex}`.
  So the flexural spectral audit is no longer blocked by missing determinant or
  characteristic-polynomial packaging:
  `\lambda=0` and `\lambda=1` reduce to explicit quadratic conditions in
  `\lambda_c`, and the exclusion of `0 < \Re \lambda < 1` reduces to a
  sign/factorization / Hurwitz analysis of the same explicit cubic.
  But the repo still does not contain that last parameter-aware sign analysis,
  and the older frozen-principal flexural determinants from the checked
  recurrence line do not directly close the corrected-cubic argument for this
  `G_{flex}`.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/current_simple_support_minimal_9channel_block_draft.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / determinant and cubic packaging closed, exact remaining blocker is parameter-aware sign analysis of chi_flex`
- What counts as verification:
  a theorem-facing analysis of the explicit cubic `\chi_{flex}` proving all
  remaining flexural spectral points:
  1. whether the current clean branch really satisfies `\det G_{flex} = 0`;
  2. `\det(G_{flex}-I) \neq 0`;
  3. no root of `\chi_{flex}` lies in `0 < \Re \lambda < 1`;
  4. if `0` is a root, then it is simple / semisimple;
  5. and this analysis must use only the parameter inequalities actually fixed
     theorem-facingly on the clean branch.
- Verification method:
  manual determinant and characteristic-polynomial derivation from the explicit
  flexural matrix, together with comparison against the older frozen-principal
  recurrence determinants to identify exactly what they do and do not prove for
  the corrected intrinsic-local cubic.
- Verification boundary:
  this does not prove Assumption LC and does not close the strict
  ambient-to-local continuation theorem. It records only that the flexural
  audit is now reduced from "package the matrix" to "analyze the explicit cubic
  `\chi_{flex}`".
- Next action:
  perform the sign/factorization / Hurwitz audit of the explicit cubic
  `\chi_{flex}` and decide the `\lambda=0`, `\lambda=1`, and
  `0 < \Re \lambda < 1` questions directly from that polynomial.

### V-S101. Conditional on Assumption LC, the currently recorded `\lambda_c` facts are not yet strong enough for the flexural Hurwitz step; the missing ingredient should remain an open theorem target, not a new standing assumption

- ID: `V-S101`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  On the present clean branch, the theorem-facing `\lambda_c` package already
  recorded in the repo consists of:
  the intrinsic-center identities
  `\lambda_c = \lambda_{s0}(0) = \lambda_{\theta 0}(0)`,
  `\lambda_{\theta 0} = \lambda_c + O(x^2)`,
  `r_0 = \lambda_c x + O(x^3)`,
  the coarse positivity `\lambda_c > 0`, and the separate selected trace-layer
  convention `\lambda_{\theta 0}(x_0) = 1`.
  These data are enough to package the corrected local operator and the
  flexural cubic `\chi_{flex}`, but they are not enough to decide the signs of
  `\det G_{flex}`, `\det(G_{flex}-I)`, or the Hurwitz determinants of
  `\chi_{flex}`.
  The stronger branch reading that representative active clean selected points
  have `\lambda_c = \lambda_{s0}(x_0)` slightly above `1` remains only
  live-check / pilot evidence.
  Therefore the exact missing ingredient is a theorem-facing intrinsic
  clean-branch inequality package for `\lambda_c` relative to `(n,\nu)`;
  on the current branch reading this should remain an open theorem target
  rather than be promoted to a new standing assumption parallel to
  Assumption LC.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `docs/theory/current_simple_support_minimal_9channel_block_draft.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / theorem-facing lambda_c package too weak for Hurwitz, exact missing ingredient is an intrinsic clean-branch inequality package for lambda_c`
- What counts as verification:
  a theorem-facing derivation, from the clean background/local equations rather
  than representative live checks alone, of branch inequalities for
  `\lambda_c` strong enough to decide:
  1. whether `\det G_{flex}` vanishes on the current branch;
  2. whether `\det(G_{flex}-I)` stays nonzero;
  3. the Hurwitz sign conditions for `\chi_{flex}`.
- Verification method:
  manual theorem-facing audit of all currently recorded `\lambda_c` facts,
  together with explicit separation of intrinsic-center statements,
  selected-trace statements, and pilot/live-check statements.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, and does not justify adding a new narrow `\lambda_c` assumption.
  It records only that the currently available `\lambda_c` facts are
  insufficient for the flexural sign/Hurwitz step.
- Next action:
  derive or identify an intrinsic clean-branch inequality package for
  `\lambda_c` relative to `(n,\nu)` from the clean background/local equations;
  if that still fails, then reassess whether a separate narrow working
  assumption is scientifically justified.

### V-S102. Conditional on Assumption LC, the origin chain of `\lambda_c` is now identified: it is the common center stretch of the clean axisymmetric background branch, and the exact next missing ingredient is a clean-background branch law for that quantity

- ID: `V-S102`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  On the current clean branch, `\lambda_c` is not introduced first through the
  local flexural matrix; it comes from the clean axisymmetric background
  itself.
  In the live background package one has
  `e_{\theta 0} = (r_0-x)/x`,
  `e_{s0} = (1-\nu^2)T_{s0} - \nu e_{\theta 0}`,
  `\lambda_{s0} = 1 + e_{s0}`,
  `\lambda_{\theta 0} = r_0/x`,
  and `r_0' = (1+e_{s0}) c_0`.
  The intrinsic-center expansion used on the local theorem line then records
  `\lambda_{s0}(0) = \lambda_{\theta 0}(0) = \lambda_c`,
  `\lambda_{s0} = \lambda_c + O(x^2)`,
  `\lambda_{\theta 0} = \lambda_c + O(x^2)`,
  `r_0 = \lambda_c x + O(x^3)`.
  Thus `\lambda_c` is the common center stretch carried by the clean
  axisymmetric background branch itself, not a removable local normalization
  parameter.
  The checked honest background recurrence fixes the later center coefficients
  `Ts2, U3, K3, Ms2, Q3`, but the repo does not yet contain a theorem-facing
  branch law or inequality fixing `\lambda_c` itself strongly enough for the
  flexural quadratic tests or Hurwitz minors.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / origin chain of lambda_c identified, exact missing ingredient is a clean-background branch law for the common center stretch`
- What counts as verification:
  a theorem-facing derivation from the clean axisymmetric background equations,
  rather than from local spectral packaging or representative live checks
  alone, of inequalities or interval control for the common center stretch
  `\lambda_c` strong enough to decide:
  1. whether `\det G_{flex}` vanishes on the branch;
  2. whether `\det(G_{flex}-I)` stays nonzero;
  3. the Hurwitz sign conditions for `\chi_{flex}`.
- Verification method:
  manual audit of the live clean background definitions, the intrinsic-center
  expansion, and the current checked recurrence bookkeeping to separate what is
  determined by the local recurrence from what still belongs to the clean
  background branch itself.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, and does not yet derive any nontrivial interval or monotonicity law for
  `\lambda_c`.
- Next action:
  attack the clean background directly and derive a theorem-facing branch law,
  interval control, or monotonicity statement for the common center stretch
  `\lambda_c`; further local flexural algebra is no longer the first missing
  step.

### V-S103. Conditional on Assumption LC, the clean background leading center system closes algebraically to two free coefficients; the first remaining Hurwitz blocker is still sharper branch control of `T_{s0}(0)` / `\lambda_c`

- ID: `V-S103`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  On the current clean branch, the live background definitions give
  `e_{\theta 0} = (r_0-x)/x`,
  `e_{s0} = (1-\nu^2)T_{s0} - \nu e_{\theta 0}`,
  `\lambda_{s0} = 1 + e_{s0}`,
  `\lambda_{\theta 0} = r_0/x`,
  and the intrinsic-center expansion records
  `\lambda_{s0}(0) = \lambda_{\theta 0}(0) = \lambda_c`.
  Therefore
  `e_{\theta 0}(0) = \lambda_c - 1`,
  `e_{s0}(0) = (1-\nu^2)T_{s0}(0) - \nu(\lambda_c - 1)`,
  and
  `\lambda_c = 1 + e_{s0}(0)`.
  Substituting and solving gives
  `(1+\nu)(\lambda_c - 1) = (1-\nu^2)T_{s0}(0)`,
  hence exactly
  `\lambda_c - 1 = (1-\nu)T_{s0}(0)`.
  So the missing clean-background branch law for `\lambda_c` is now
  equivalently a theorem-facing sign/interval theorem for the center
  meridional background quantity `T_{s0}(0)`.
  But the repo still does not record theorem-facing sign, interval, or
  monotonicity control for `T_{s0}(0)` itself.
  More explicitly, the currently recorded clean background package is
  `T_{s0}'
   = -T_{s0}/r_0 + (c_0/r_0)T_{\theta 0} - \varphi_0' Q_0`,
  with
  `T_{\theta 0} = \nu T_{s0} + e_{\theta 0}`,
  `e_{\theta 0} = (r_0-x)/x`,
  `e_{s0} = (1-\nu^2)T_{s0} - \nu e_{\theta 0}`,
  `r_0' = (1+e_{s0})c_0`,
  and clean BCs
  `T_{s0}(1)=0`, `\varphi_0(1)=0`, `Q_0(x_0)=0`, `r_0(x_0)=x_0`,
  `\varphi_0(x_0)=0`.
  Center regularity cancels the singular `1/r_0` term and yields
  `T_{\theta 0}(0)=T_{s0}(0)`, but the repo still contains no theorem-facing
  comparison principle, sign-preserving lemma, monotonicity theorem, or center
  evaluation formula propagating this ODE/BC package to a sign or interval law
  for `T_{s0}(0)`.
  A direct center expansion of the same ODE package now gives one additional
  exact coefficient identity:
  with
  `Q_0(x)=Q_1 x + O(x^3)`,
  `s_0 = Kx + O(x^3)`,
  `r_0 = \lambda_c x + O(x^3)`,
  `T_{\theta 0}(x)=T_{s0}(0)+O(x^2)`,
  and the current theorem-facing background expansion
  `\varphi_0'(x)=K+O(x^2)`,
  the `Q_0` equation yields
  `Q_1 = K T_{s0}(0) - [\lambda_c/(\lambda_c+1)]\bar q`,
  equivalently
  `Q_1 = K(\lambda_c-1)/(1-\nu) - [\lambda_c/(\lambda_c+1)]\bar q`.
  This must be kept distinct from the older checked frozen-principal
  recurrence statement `Q_1 = 0`: that earlier identity belongs to a different
  fully frozen principal layer and does not by itself determine the present
  live-background center coefficient in the theorem-facing ODE package.
  So positive branch load contributes a negative term to `Q_1`, but the repo
  still does not contain theorem-facing sign control for `K` or `T_{s0}(0)`,
  and the current center expansion only implies `T_{s0}'(0)=0` rather than a
  local monotonicity law.
  A still narrower clean-background center pass uses the same recorded
  first-omitted-coefficient package, which fixes `Ms2`, so at the order needed
  here one may read
  `M_{s0}(x)=M_{s0}(0)+O(x^2)`.
  Then the clean moment equation
  `M_{s0}'
   = -M_{s0}/r_0 + (c_0/r_0)M_{\theta 0} + Q_0`
  cannot carry an admissible `x^{-1}` term, hence exact center regularity
  forces
  `M_{\theta 0}(0)=M_{s0}(0)`.
  Feeding that into
  `\varphi_0' = \Lambda(M_{s0} - \nu M_{\theta 0})`
  and using `\varphi_0'(x)=K+O(x^2)` gives
  `K = \Lambda(1-\nu) M_{s0}(0)`.
  Therefore the whole leading center package is already
  `\lambda_c = 1 + (1-\nu)T_{s0}(0)`,
  `K = \Lambda(1-\nu)M_{s0}(0)`,
  `Q_1 = K T_{s0}(0) - [\lambda_c/(\lambda_c+1)]\bar q`;
  equivalently, the four quantities
  `(T_{s0}(0), K, Q_1, M_{s0}(0))`
  reduce at leading order to two free coefficients, for example
  `(T_{s0}(0), M_{s0}(0))`.
  Since the branch already records `\lambda_c > 0`, this gives the coarse
  one-sided bound
  `T_{s0}(0) > -1/(1-\nu)`;
  since `\Lambda = 12(1-\nu^2)\mu^2 > 0`, it also gives the exact sign linkage
  `\operatorname{sign} K = \operatorname{sign} M_{s0}(0)`.
  But this is still not enough to sign `T_{s0}(0)`, exclude
  `T_{s0}(0)=0`, or sign `Q_1`;
  indeed `T_{s0}(0)=0` remains compatible with the current leading center
  system and would give `\lambda_c = 1`, `Q_1 = -\bar q/2`.
  So the first remaining Hurwitz-relevant blocker is no longer an independent
  center-curvature variable `K`, but sharper branch control of `T_{s0}(0)`,
  equivalently of `\lambda_c`, beyond the coarse lower bound above; if one also
  wants a sign law for `Q_1`, one further needs sign/control of the product
  `M_{s0}(0)T_{s0}(0)`.
  More sharply, the current clean `T_{s0}` equation does not yet produce a
  scalar one-sided derivative inequality:
  \[
  T_{s0}'
  =
  \frac{\nu c_0 - 1}{r_0} T_{s0}
  +
  \frac{c_0}{r_0} e_{\theta 0}
  -
  \varphi_0' Q_0,
  \]
  and the current theorem-facing branch record gives no sign control for the
  coefficient `(\nu c_0 - 1)/r_0`, none for `e_{\theta 0}`, and none for the
  product `\varphi_0' Q_0`.
  So integrating from the edge condition `T_{s0}(1)=0` yields only a
  sign-indefinite integral identity, not a comparison formula.
  In particular, the present theorem-facing ODE/BC package gives no
  contradiction for `T_{s0}(0)=0`, and no contradiction for the whole negative
  range allowed by the coarse lower bound
  `-1/(1-\nu) < T_{s0}(0) < 0`.
  The exact first missing ingredient is therefore most honestly a theorem-
  facing coupled comparison / integral / monotonicity theorem for the clean
  background system that propagates the split BC package to the center value
  `T_{s0}(0)`.
  A still narrower coupled pass now shows that exact weighted identities do
  exist:
  \[
  (r_0 T_{s0})' = c_0 T_{\theta 0} - \varphi_0' r_0 Q_0,\qquad
  (r_0 Q_0)' = s_0 T_{\theta 0} + \varphi_0' r_0 T_{s0} - \bar q r_0,\qquad
  (r_0 M_{s0})' = c_0 M_{\theta 0} + r_0 Q_0.
  \]
  More sharply, with
  `A := c_0 T_{s0} + s_0 Q_0`,
  `B := -s_0 T_{s0} + c_0 Q_0`,
  the first two equations rotate exactly to
  \[
  A' + A/r_0 = T_{\theta 0}/r_0 - s_0 \bar q,\qquad
  B' + B/r_0 = -c_0 \bar q.
  \]
  Because the current BC package gives
  `\varphi_0(x_0)=\varphi_0(1)=0`, `Q_0(x_0)=0`, `T_{s0}(1)=0`,
  one has
  `A(x_0)=T_{s0}(0)`, `A(1)=0`, `B(x_0)=0`, `B(1)=Q_0(1)`.
  So with the positive integrating factor
  `\mu(x):=\exp(\int_{x_0}^x ds/r_0(s))`
  the coupled system yields the exact integral identities
  \[
  Q_0(1)
  =
  -\mu(1)^{-1}\bar q \int_{x_0}^1 \mu(\xi)c_0(\xi)\,d\xi,
  \]
  \[
  T_{s0}(0)
  =
  -\int_{x_0}^1 \mu(\xi)
   \Bigl[\frac{T_{\theta 0}(\xi)}{r_0(\xi)} - s_0(\xi)\bar q\Bigr]\,d\xi.
  \]
  These identities are theorem-facingly sharper than the scalar `T_{s0}`
  equation alone, but they still do not sign `T_{s0}(0)`:
  the `B` identity still needs a sign law for `c_0=\cos\varphi_0`, and the
  `A` identity still needs sign/control of the whole kernel
  `T_{\theta 0}/r_0 - s_0 \bar q`.
  The current theorem-facing kernel-sign package is only local / endpoint-level:
  from `\varphi_0(x_0)=\varphi_0(1)=0` one gets
  `c_0(x_0)=c_0(1)=1`, `s_0(x_0)=s_0(1)=0`;
  from the recorded center expansions
  `c_0 = 1 + O(x^2)`,
  `s_0 = Kx + O(x^3)`,
  `T_{\theta 0}(x)=T_{s0}(0)+O(x^2)`
  one gets local near-center positivity of `c_0`, but no theorem-facing sign
  of `s_0` because `K` is not signed.
  By continuity and `c_0(1)=1`, one also gets positivity of `c_0` on some
  sufficiently small right-edge interval.
  Moreover the same clean background equation gives the exact integral
  representation
  `\varphi_0(x)
   = \Lambda \int_{x_0}^x [M_{s0}(\xi)-\nu M_{\theta 0}(\xi)]\, d\xi`,
  so `\varphi_0(1)=0` also forces the exact cancellation identity
  `\int_{x_0}^1 [M_{s0}(\xi)-\nu M_{\theta 0}(\xi)]\, d\xi = 0`.
  Since the clean branch is at least `C^1` on `[x_0,1]`, Rolle's theorem
  therefore yields at least one interior point `x_*` with
  `\varphi_0'(x_*)=0`, equivalently `M_{s0}(x_*) = \nu M_{\theta 0}(x_*)`.
  So a literal global one-sign theorem for `\varphi_0'` cannot be the right
  next target unless one also proves `\varphi_0 \equiv 0` on `[x_0,1]`, which
  the current repo does not.
  But the repo still has no theorem-facing range-preservation theorem for
  `\varphi_0`,
  so it does not exclude interior sign changes of `\varphi_0` and therefore
  does not prove global positivity of `c_0`.
  Likewise it still has no one-sided control of
  `e_{\theta 0} = (r_0-x)/x`, hence no one-sided estimate for
  `T_{\theta 0} = \nu T_{s0} + e_{\theta 0}`.
  So the exact first coupled-background obstruction is now naturally split:
  1. first, a theorem-facing global range-preservation / turning-angle bound
     for `\varphi_0` strong enough to keep `|\varphi_0| < \pi/2` and promote
     local `c_0 > 0` to the whole interval;
  2. second, a theorem-facing one-sided estimate for `e_{\theta 0}` or
     directly for `T_{\theta 0}` strong enough to sign the `A`-kernel.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / leading center package closes to two free coefficients and gives a coarse lower bound for T_s0(0); exact rotated coupled integral identities are available; local/endpoint kernel facts for c0 are available; the phi0 equation gives an exact integral representation and forces at least one interior stationary point, so a literal one-sign theorem for phi0' is not the right next target; but no global range-preservation theorem for phi0 and no one-sided control of T_theta0 are yet available; the first remaining Hurwitz blocker is still sharper branch control of T_s0(0)/lambda_c`
- What counts as verification:
  a theorem-facing clean-background argument proving any one of the following,
  strong enough to feed the flexural quadratic/Hurwitz step:
  1. sign of `T_{s0}(0)`;
  2. sharper interval control on `T_{s0}(0)` or `\lambda_c` beyond the coarse
     lower bound `T_{s0}(0) > -1/(1-\nu)`;
  3. sign/control of the product `M_{s0}(0)T_{s0}(0)`, equivalently of the
     center contribution `K T_{s0}(0)`;
  4. monotonicity or branch-law information determining `T_{s0}(0)` on the
     active clean branch;
  5. or a coupled comparison / integral theorem for the clean background ODE/BC
     package strong enough to propagate the split boundary data to the center;
  6. concretely, sign / interval control of `c_0`, `s_0`, and `T_{\theta 0}`
     strong enough to sign the exact rotated kernels above;
  7. more sharply, a global range-preservation / turning-angle bound for
     `\varphi_0` strong enough to show `|\varphi_0| < \pi/2`, together with a
     one-sided estimate for `e_{\theta 0}` / `T_{\theta 0}`.
- Verification method:
  manual derivation from the recorded clean background constitutive chain and
  intrinsic-center identities, together with an audit of whether the repo
  already contains sign/interval information for the center meridional
  background quantity.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, and does not yet reopen the flexural Hurwitz step by itself; it only
  closes the leading center algebra to two free coefficients and adds the
  coarse consequences `T_{s0}(0) > -1/(1-\nu)` and
  `\operatorname{sign} K = \operatorname{sign} M_{s0}(0)`;
  the branch still lacks the sharper intrinsic control of `T_{s0}(0)` /
  `\lambda_c` needed for the flexural quadratic/Hurwitz step, and the current
  ODE/BC package still does not furnish a sign-definite coupled comparison
  mechanism for `T_{s0}` beyond local/endpoint positivity of `c_0`; in
  particular, it does not yet give a global range-preservation theorem for
  `\varphi_0`, only the exact integral representation and the existence of an
  interior stationary point.
- Next action:
  attack the clean axisymmetric background directly and prove a coupled
  comparison / integral / monotonicity theorem for the clean ODE/BC package,
  strong enough to control `T_{s0}(0)` or `\lambda_c` beyond the current coarse
  lower bound; under the physical-semantic screen and the sharper reduced
  identity recorded below, the default next subtarget is no longer the
  separate split
  "first prove a global range-preservation theorem for `\varphi_0`, then prove
  a one-sided estimate for `e_{\theta 0}` / `T_{\theta 0}`";
  that remains only a stronger sufficient route in principle.
  The honest default next target is now the weaker direct estimate on the
  combined reduced kernel `F_T`, or one layer higher a proof of `H \ge 0`
  together with the weighted domination estimate on `(Hs_0)^+`.
  If the goal is to sign `Q_1` as well, add control of the product
  `M_{s0}(0)T_{s0}(0)`.
  The flexural Hurwitz step should not be reopened before that stronger
  background control is available.

### V-S104. On the clean full simple-support branch, future theorem-facing blocker promotion must pass a physical-semantic screening rule before acceptance as the next strict or LC-conditional target

- ID: `V-S104`
- Claim / Hypothesis:
  Fix `(n,q)`.
  Before accepting any new theorem-facing target, blocker, lemma, or
  spectral/geometric claim on the clean full `J_0` branch, one must first apply
  a physical-semantic screening rule on both the strict line and the line
  conditional on Assumption LC.
  That screen should:
  1. classify each relevant variable as geometric, force/stress/moment,
     kinematic, normalization/gauge/trace-layer, or purely algebraic/helper;
  2. classify the proposed claim as local identity, global sign claim, global
     monotonicity claim, interval/range bound, normalization statement,
     spectral statement, or a claim only on an explicitly restricted geometry
     class;
  3. reject default promotion of claims that are too strong for the variable
     semantics, too geometry-dependent for the stated branch class, or stronger
     than the current proof step actually needs;
  4. prefer the weakest claim that is sufficient for the current theorem-facing
     step.
  Operationally, if a proposed claim fails this screen, the pass must say so
  explicitly, state whether it is too strong, too geometry-dependent, or not
  actually needed, and replace it by a weaker or better-targeted claim rather
  than silently continuing with the failed claim as the next blocker.
  Current audit on the active clean branch:
  the exact center/background identities
  `\lambda_c - 1 = (1-\nu)T_{s0}(0)`,
  `K = \Lambda(1-\nu)M_{s0}(0)`,
  `Q_1 = K T_{s0}(0) - [\lambda_c/(\lambda_c+1)]\bar q`,
  and the reduction to two free center coefficients do pass this screen;
  the earlier target "global sign / no-turning theorem for `\varphi_0`" does
  not pass as a default theorem-facing target on the general shell-of-
  revolution branch without an explicit no-overturning geometry class, because
  it is stronger than the immediate need `c_0 > 0` and more geometry-dependent
  than the present background step requires.
- Type: `interpretation claim`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `adopted as methodological gate / future clean-branch blocker promotion must pass the physical-semantic screen on both the strict and LC-conditional lines`
- What counts as verification:
  1. future theorem/status passes explicitly record the physical class of the
     key variables, the strength class of the proposed claim, and the
     sufficiency decision before promoting a new blocker/target;
  2. if a proposed claim fails the screen, the pass says so explicitly and
     replaces it rather than silently continuing with it;
  3. the currently accepted clean-branch center/background identities remain
     coherent under the same audit.
- Verification method:
  manual repo-facing audit of the active theory docs and of the theorem-facing
  blocker language used on the clean branch.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, does not change equations, BCs, solver behavior, or assumptions, and
  does not by itself prove any new mathematical theorem; it only governs how
  future theorem-facing targets/blockers are screened before promotion.
- Next action:
  apply this screen in future theorem-facing clean-branch passes.
  On the current background route, do not re-promote a global sign /
  no-turning theorem for `\varphi_0` by default;
  either state an explicit restricted no-overturning geometry class, or seek a
  weaker coupled / range-preservation estimate that is sufficient for the
  rotated kernel step.

### V-S105. Conditional on Assumption LC, the exact eta-weighted reduced identity for `T_{s0}(0)` isolates a minimal sufficient combined kernel package; stronger separate sign targets are no longer the default next move under the physical-semantic screen

- ID: `V-S105`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  On the current clean branch, start from the exact rotated identities
  `A' + A/r_0 = T_{\theta 0}/r_0 - s_0 \bar q`,
  `B' + B/r_0 = -c_0 \bar q`,
  and the exact `B` formula
  `B(x) = -\mu(x)^{-1}\bar q \int_{x_0}^x \mu(\xi)c_0(\xi)\, d\xi`,
  where
  `\mu(x) := \exp(\int_{x_0}^x ds/r_0(s)) > 0`.
  Rewriting the `A` equation as
  `A' + [(1-\nu c_0)/r_0]A = e_{\theta 0}/r_0 - \bar q s_0 - \nu s_0 B/r_0`
  and introducing
  `\eta(x) := \exp(\int_{x_0}^x (1-\nu c_0(s))/r_0(s)\, ds) > 0`,
  one gets the exact reduced identity
  `T_{s0}(0) = -\int_{x_0}^1 \eta(\xi) F_T(\xi)\, d\xi`,
  where
  `F_T(\xi)
   := e_{\theta 0}(\xi)/r_0(\xi)
      - \bar q s_0(\xi) H(\xi)`,
  `H(\xi)
   := 1 - \nu J(\xi)/(r_0(\xi)\mu(\xi))`,
  and
  `J(\xi) := \int_{x_0}^{\xi} \mu(\tau)c_0(\tau)\, d\tau`.
  Because `\eta > 0`, the truly minimal sufficient package is now direct
  sign/interval control of the single combined kernel `F_T`:
  `F_T \ge 0` a.e. gives `T_{s0}(0) \le 0`,
  `F_T \le 0` a.e. gives `T_{s0}(0) \ge 0`,
  and bounds `a \le F_T \le b` give
  `-b\int_{x_0}^1 \eta \le T_{s0}(0) \le -a\int_{x_0}^1 \eta`.
  Under the physical-semantic screen this is sharper than the earlier default
  route that separately targeted a global angle-range theorem for `\varphi_0`
  and then a sign theorem for `e_{\theta 0}` / `T_{\theta 0}`:
  those remain stronger sufficient routes in principle, but they are not the
  minimal default target anymore.
  One structured but still screening-compatible sufficient package for the
  upper bound `T_{s0}(0) \le 0` is:
  `H \ge 0`
  together with the weighted domination
  `\int_{x_0}^1 \eta(\xi)e_{\theta 0}(\xi)/r_0(\xi)\, d\xi
   \ge
   \bar q \int_{x_0}^1 \eta(\xi)(H(\xi)s_0(\xi))^+\, d\xi`.
  This avoids requiring global sign theorems for all of `c_0`, `s_0`, and
  `e_{\theta 0}`.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / exact eta-weighted T_s0(0) identity isolates the combined kernel F_T as the minimal sufficient target; currently available are only mu,eta positivity, exact trig bounds, and local/endpoint c0 positivity; sign/range control of H, one-sided control of e_theta0/r0, and the weighted domination estimate remain open`
- What counts as verification:
  a theorem-facing proof of at least one of the following:
  1. `F_T \ge 0` a.e. or `F_T \le 0` a.e.;
  2. interval bounds `a \le F_T \le b` strong enough to bound `T_{s0}(0)`;
  3. the structured sufficient package
     `H \ge 0` together with
     `\int \eta e_{\theta 0}/r_0
      \ge
      \bar q \int \eta (Hs_0)^+`;
  4. any equally narrow direct weighted estimate on the combined kernel
     `F_T` that yields a one-sided sign/interval law for `T_{s0}(0)`.
- Verification method:
  manual theorem-facing reduction of the exact rotated integral identities,
  followed by the physical-semantic screen to isolate the weakest sufficient
  kernel package rather than stronger separate sign claims.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, does not change equations, BCs, solver behavior, or assumptions, and
  does not yet reopen the flexural Hurwitz step by itself; it only sharpens
  the LC-conditional background blocker from a broad coupled-sign problem to a
  minimal combined-kernel estimate.
- Next action:
  do not default to separate global sign/range theorems for `\varphi_0`,
  `s_0`, and `e_{\theta 0}`.
  Instead, attack the weakest sufficient object:
  a direct sign/interval estimate on `F_T`, or one layer higher
  `H \ge 0` plus the weighted domination estimate above.

### V-S106. Conditional on Assumption LC, the auxiliary kernel factor `H` closes to an exact weighted first-order identity; it gives local positivity near `x_0` and a clean sufficient source condition for global positivity, but by itself still does not control `F_T`

- ID: `V-S106`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  Define
  `J(x) := \int_{x_0}^x \mu(t)c_0(t)\, dt`
  and
  `H(x) := 1 - \nu J(x)/(r_0(x)\mu(x))`,
  where
  `\mu(x) := \exp(\int_{x_0}^x ds/r_0(s)) > 0`.
  Then the exact theorem-facing identities are:
  `H(x_0)=1`,
  `J'(x)=\mu(x)c_0(x)`,
  `\mu'(x)=\mu(x)/r_0(x)`,
  `(r_0\mu(H-1))' = -\nu \mu c_0`,
  equivalently
  `(r_0\mu H)' = \mu(r_0' + 1 - \nu c_0)`,
  and therefore
  `H'
   = (r_0' + 1 - \nu c_0)/r_0 - ((r_0'+1)/r_0)H`.
  Because `r_0(x_0)=x_0`, `\mu(x_0)=1`, `c_0(x_0)=1`, and `H(x_0)=1`,
  the exact initial slope is
  `H'(x_0) = -\nu/x_0 < 0`.
  Hence `H` is theorem-facingly positive on some sufficiently small right-
  neighborhood of `x_0`.
  The same identities show two clean sufficient routes in principle:
  if `c_0 \ge 0` on the whole interval then `H \le 1`,
  and if `r_0' + 1 - \nu c_0 \ge 0` on the whole interval then `H > 0`.
  But none of those global sign conditions is yet theorem-facingly available on
  the present branch record.
  Therefore `H` does now have an exact theorem-facing equation and a local
  positivity consequence, but `H`-control alone still does not sign
  `F_T = e_{\theta 0}/r_0 - \bar q s_0 H`, because neither `s_0` nor
  `e_{\theta 0}/r_0` is currently signed.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `supported conditionally under LC / exact H-equation closes; H(x0)=1 and H'(x0)=-nu/x0 give local positivity near x0; global sign/range control of H is still open; H-control alone does not yet sign F_T`
- What counts as verification:
  a theorem-facing proof of at least one of the following:
  1. a global sign/range law for `H`, such as `H > 0` or `0 \le H \le 1`;
  2. the clean sufficient source-level condition
     `r_0' + 1 - \nu c_0 \ge 0`;
  3. a direct combined estimate showing how the available `H` control feeds
     the sign of `F_T`.
- Verification method:
  manual differentiation and exact weighted reformulation of the reduced kernel
  factor, followed by a conservative sign audit under the physical-semantic
  screening rule.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, does not change equations, BCs, solver behavior, or assumptions, and
  does not yet reopen the flexural Hurwitz step by itself; it only sharpens the
  auxiliary-kernel side of the LC-conditional background reduction.
- Next action:
  do not promote stronger separate global sign theorems for `\varphi_0` or
  `s_0` by default.
  If one insists on an `H`-first route, attack the weakest clean sufficient
  source-level condition `r_0' + 1 - \nu c_0 \ge 0`;
  otherwise keep the honest default target at the combined-kernel level,
  namely a direct one-sided estimate on `F_T` or on the weighted positive part
  of `H s_0`.

### V-S107. Conditional on Assumption LC, the rewritten combined kernel `F_T = 1/x - 1/r_0 - \bar q s_0 H` isolates the honest minimal sufficient packages as geometry-versus-coupling dominance estimates, while separate global sign targets remain stronger than necessary

- ID: `V-S107`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  On the current clean branch, rewrite the active reduced kernel as
  `F_T(x) = 1/x - 1/r_0(x) - \bar q s_0(x)H(x)`.
  Since `x>0` on `[x_0,1]` and the current reduction uses `r_0>0`, one has
  the exact identity
  `1/x - 1/r_0 = (r_0-x)/(x r_0) = e_{\theta 0}/r_0`,
  hence
  `\operatorname{sign}(1/x - 1/r_0) = \operatorname{sign}(r_0-x)`.
  Therefore the direct geometry/coupling balance is now explicit.
  Strong but easy pointwise sufficient packages are:
  `r_0 \ge x` together with `s_0 H \le 0` implies `F_T \ge 0`,
  and
  `r_0 \le x` together with `s_0 H \ge 0` implies `F_T \le 0`.
  Under the physical-semantic screen those are stronger than the default next
  need.
  The weaker direct pointwise sufficient packages are:
  `r_0 - x \ge \bar q\,x r_0 (s_0 H)^+` a.e. implies `F_T \ge 0` a.e.,
  and
  `x - r_0 \ge \bar q\,x r_0 (-s_0 H)^+` a.e. implies `F_T \le 0` a.e.
  Because `\eta>0`, the corresponding weighted sufficient packages are:
  `\int_{x_0}^1 \eta(x)(r_0(x)-x)/(x r_0(x))\, dx
   \ge
   \bar q \int_{x_0}^1 \eta(x)(s_0(x)H(x))^+\, dx`
  for `T_{s0}(0) \le 0`,
  and
  `\int_{x_0}^1 \eta(x)(x-r_0(x))/(x r_0(x))\, dx
   \ge
   \bar q \int_{x_0}^1 \eta(x)(-s_0(x)H(x))^+\, dx`
  for `T_{s0}(0) \ge 0`.
  These are the honest minimal sufficient packages extracted from the rewritten
  `F_T` form.
  What is currently available theorem-facingly is still only the endpoint
  information
  `r_0(x_0)=x_0`, `s_0(x_0)=0`, `H(x_0)=1`, hence `F_T(x_0)=0`,
  together with the earlier local positivity of `H` near `x_0`;
  the repo does not yet give a global sign or interval law for `r_0-x`,
  a sign/size law for `s_0 H`, or a direct weighted dominance estimate between
  those two terms.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / rewritten F_T isolates the honest minimal sufficient packages as geometry-defect versus coupling dominance; only endpoint vanishing and local H positivity are currently available; global sign/size control of r0-x, s0H, and their weighted dominance remain open`
- What counts as verification:
  a theorem-facing proof of at least one of the following:
  1. `r_0 - x \ge \bar q\,x r_0 (s_0 H)^+` a.e.;
  2. `x - r_0 \ge \bar q\,x r_0 (-s_0 H)^+` a.e.;
  3. the corresponding `\eta`-weighted integral dominance for the sign of
     `T_{s0}(0)`;
  4. any equally narrow pointwise or weighted dominance estimate that signs or
     bounds `F_T` directly.
- Verification method:
  manual algebraic rewrite of the exact reduced kernel and a conservative
  theorem-facing audit under the physical-semantic screening rule.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, does not change equations, BCs, solver behavior, or assumptions, and
  does not yet reopen the flexural Hurwitz step; it only sharpens the active
  LC-conditional blocker from a generic combined-kernel estimate to the
  explicit geometry-versus-coupling dominance problem.
- Next action:
  do not promote stronger default targets such as global sign theorems for
  `\varphi_0`, `s_0`, or `e_{\theta 0}`.
  Attack the weakest sufficient object instead:
  a direct pointwise or `\eta`-weighted dominance estimate between
  `(r_0-x)/(x r_0)` and the positive part of `s_0 H`.

### V-S108. Conditional on Assumption LC, the weighted dominance target for the rewritten kernel is sharply isolated, but the present clean ODE/BC package still provides no theorem-facing route to it

- ID: `V-S108`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  On the current clean branch, keep the exact weighted target
  `\int_{x_0}^1 \eta(x)(r_0(x)-x)/(x r_0(x))\, dx
   \ge
   \bar q \int_{x_0}^1 \eta(x)(s_0(x)H(x))^+\, dx`
  as the default next sufficient route for `T_{s0}(0) \le 0`.
  A narrower theorem-facing audit shows that the present clean ODE/BC package
  does not yet yield a natural comparison path to that target:
  1. differentiating the active weight
     `\eta' = \eta(1-\nu c_0)/r_0`
     does not by itself convert the geometry term into a coercive derivative;
  2. rewriting the geometry defect as
     `(r_0-x)/(x r_0) = e_{\theta 0}/r_0`
     or via
     `r_0' = (1+e_{s0})c_0`,
     `e_{s0} = (1-\nu^2)T_{s0} - \nu e_{\theta 0}`,
     stays exact but does not produce a sign-closing weighted identity;
  3. rewriting the coupling factor through
     `H = 1 - \nu J/(r_0\mu)`,
     `J' = \mu c_0`,
     `(r_0\mu(H-1))' = -\nu \mu c_0`
     likewise stays exact but does not yield a weighted upper bound for
     `\int \eta(s_0 H)^+`;
  4. no exact cancellation identity linking those two weighted terms is
     currently theorem-facingly available in the branch record.
  Under the physical-semantic screen, stronger fallback targets such as global
  sign theorems for `\varphi_0`, `s_0`, or `e_{\theta 0}`, or the stronger
  pointwise dominance packages, are therefore rejected as default next moves
  because they are stronger than the active weighted need.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / the eta-weighted dominance target is sharply isolated and remains useful, but the current clean ODE/BC package yields no theorem-facing weighted route to it beyond the exact identity for T_s0(0); the first missing ingredient is a new eta-weighted comparison/cancellation estimate`
- What counts as verification:
  a theorem-facing proof of at least one of the following:
  1. a weighted lower bound for
     `\int_{x_0}^1 \eta(x)(r_0(x)-x)/(x r_0(x))\, dx`;
  2. a weighted upper bound for
     `\int_{x_0}^1 \eta(x)(s_0(x)H(x))^+\, dx`;
  3. a direct weighted cancellation/comparison identity linking those two
     integrals strongly enough to sign or bound `T_{s0}(0)`;
  4. any equally narrow theorem-facing weighted estimate on the rewritten
     kernel `F_T` that yields a one-sided sign/interval law for `T_{s0}(0)`.
- Verification method:
  manual weighted audit of the exact reduced kernel, exact differentiation of
  the available weight and auxiliary factors, and conservative blocker
  selection under the physical-semantic screening rule.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, does not change equations, BCs, solver behavior, or assumptions, and
  does not yet reopen the flexural Hurwitz step; it only sharpens the active
  LC-conditional blocker from a weighted sufficient package to the more
  specific missing weighted comparison/cancellation ingredient behind it.
- Next action:
  do not default back to stronger pointwise or global-sign targets.
  Attack the weakest missing object instead:
  a new theorem-facing `\eta`-weighted comparison / cancellation estimate,
  most naturally a weighted lower bound for the geometry-defect integral or a
  weighted upper bound for the coupling integral `\int \eta(s_0 H)^+`.

### V-S109. Conditional on Assumption LC, the natural first-order multiplier / auxiliary-combination routes beyond `A,B,\mu,\eta,H` appear exhausted: the remaining step requires a genuinely non-first-order background input

- ID: `V-S109`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  On the current clean branch, audit the natural first-order multiplier and
  auxiliary-combination routes suggested by the exact background package beyond
  the already tested `A,B,\mu,\eta,H` framework.
  The conservative theorem-facing classification is:
  1. other linear combinations of `(T_{s0},Q_0)` designed to remove the
     `\varphi_0'` skew-coupling are not genuinely new:
     the cancellation transport is already solved by the `\varphi_0`-rotation,
     so any such route is equivalent to `(A,B)` up to a constant invertible
     post-combination;
  2. adjoint-style scalar multipliers applied after that reduction are also
     not genuinely new:
     they reproduce the same scalar integrating-factor structure, hence only
     `\mu` and `\eta` up to nonzero constants;
  3. weighted raw channel identities such as
     `(r_0T_{s0})'`, `(r_0Q_0)'`, `(r_0M_{s0})'`
     are already the pre-rotated source identities behind the current route;
  4. combinations involving `M_{s0}`, `\varphi_0`, `c_0`, `s_0`, or
     `e_{\theta 0}` do not presently add a new comparison structure:
     they reintroduce the same unresolved kernels
     `(r_0-x)/(x r_0)`, `s_0H`, `c_0`, or `\varphi_0'`
     without new sign/coercivity input or stronger boundary leverage.
  Under the physical-semantic screen, stronger or more arbitrary first-order
  recombinations are therefore not the honest default next target.
  At this reduction level, the current clean background package is effectively
  exhausted.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / no genuinely new natural first-order multiplier route beyond A,B,mu,eta,H is currently visible; candidate routes are equivalent or no stronger; the first missing ingredient is now a genuinely non-first-order background input`
- What counts as verification:
  a theorem-facing proof of at least one of the following:
  1. a genuinely new natural first-order combination that is not equivalent to
     the present rotated/integrating-factor route and yields a strictly
     stronger comparison/cancellation identity for `T_{s0}(0)`;
  2. a genuinely non-first-order background theorem, branch law, or geometric
     restriction strong enough to prove one of the weighted bounds isolated in
     `V-S108`;
  3. an exact adjoint/fundamental-matrix argument showing that the current
     first-order reduction is canonical up to equivalence.
- Verification method:
  manual audit of the exact first-order subsystem, conservative classification
  of natural multiplier candidates under the physical-semantic screening rule,
  and comparison against the already closed `A,B,\mu,\eta,H` framework.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, does not change equations, BCs, solver behavior, or assumptions, and
  does not yet reopen the flexural Hurwitz step; it only sharpens the blocker
  diagnosis from "missing weighted dominance route" to
  "first-order multiplier search appears exhausted, so the next input must be
  genuinely non-first-order".
- Next action:
  do not keep promoting additional first-order recombinations by default.
  Either produce a genuinely non-equivalent first-order canonical argument, or
  move to a non-first-order background input: most naturally a higher-order or
  branch-level theorem proving one of the weighted bounds isolated in `V-S108`.

### V-S110. Conditional on Assumption LC, the minimal genuinely non-first-order next input is a global background integral theorem for the active weighted dominance, not a higher-order local jet theorem, a broader branch-law theorem, or a new geometry-class restriction

- ID: `V-S110`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  After `V-S109`, the plausible genuinely non-first-order classes are:
  1. a higher-order background expansion theorem;
  2. a branch-level comparison / monotonicity / interval law for
     `T_{s0}(0)` or `\lambda_c`;
  3. a global background integral theorem not reducible to first-order
     multipliers;
  4. an explicit restricted geometry-class theorem.
  The conservative theorem-facing choice is now:
  class (3) is the minimal honest default next input.
  It is preferred because it targets exactly the already isolated weighted need
  behind the active reduced kernel
  `F_T = (r_0-x)/(x r_0) - \bar q s_0 H`
  without inflating the theorem statement.
  More concretely, the default next target should be a theorem-facing proof of
  `\int_{x_0}^1 \eta(x)(r_0(x)-x)/(x r_0(x))\, dx
   \ge
   \bar q \int_{x_0}^1 \eta(x)(s_0(x)H(x))^+\, dx`,
  or of an equally weak one-sided variant sufficient to sign or bound
  `T_{s0}(0)`.
  The other classes are not the default next target:
  1. a higher-order background expansion theorem is plausible in principle but
     too local by itself to control the already global weighted integral unless
     it is supplemented by an additional localization/globalization theorem;
  2. a branch-level interval law for `T_{s0}(0)` or `\lambda_c` would indeed be
     sufficient, but it is broader than the current kernel-level need and so is
     stronger than necessary at this stage;
  3. an explicit restricted geometry subclass would change the intended
     theorem statement / geometry class and therefore fails the
     physical-semantic screen as a default move unless later shown unavoidable.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / the minimal genuinely non-first-order next input is now clear: a global background integral theorem proving the active weighted dominance or an equally weak one-sided variant; higher-order local jets, broader branch laws, and restricted geometry subclasses are all reserve alternatives, not the default next move`
- What counts as verification:
  a theorem-facing proof of at least one of the following:
  1. the direct weighted dominance
     `\int_{x_0}^1 \eta(r_0-x)/(x r_0)
      \ge
      \bar q \int_{x_0}^1 \eta(s_0 H)^+`;
  2. an equally weak global integral comparison/cancellation law sufficient to
     sign or bound `T_{s0}(0)`;
  3. an exact theorem-facing reduction showing that such a global background
     integral theorem is equivalent to the desired sign/interval control of
     `T_{s0}(0)` on the current branch.
- Verification method:
  manual strategy audit of the active reduced kernel, conservative comparison of
  plausible non-first-order input classes under the physical-semantic
  screening rule, and theorem-facing selection of the weakest sufficient class.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, does not change equations, BCs, solver behavior, or assumptions, and
  does not yet reopen the flexural Hurwitz step; it only chooses the minimal
  non-first-order direction in which the LC-conditional proof line should now
  continue.
- Next action:
  pursue the global background integral theorem route first.
  Do not default instead to higher-order local jet theorems, broader branch-law
  theorems for `T_{s0}(0)` / `\lambda_c`, or restricted geometry subclasses
  unless the chosen integral route later proves genuinely insufficient.

### V-S111. Conditional on Assumption LC, an adjoint / Green-type route is presently reserve only: the reduced scalar adjoint is already exhausted by the `eta` identity, while a genuinely new full-BVP adjoint would require a canonical linearized background BVP not yet fixed theorem-facingly

- ID: `V-S111`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  On the current clean branch, consider possible adjoint / Green-type routes
  for the target functional
  `\ell(Y) := T_{s0}(x_0)`,
  where
  `Y := (T_{s0},Q_0,M_{s0},r_0,\varphi_0)`
  solves the nonlinear background BVP
  `Y' = F(x,Y;q)`,
  with active BCs
  `T_{s0}(1)=0`,
  `\varphi_0(1)=0`,
  `Q_0(x_0)=0`,
  `r_0(x_0)=x_0`,
  `\varphi_0(x_0)=0`.
  The theorem-facing audit is:
  1. at the reduced scalar level, the adjoint/integrating-factor route is not
     genuinely new, because the already recorded
     `T_{s0}(0) = -\int_{x_0}^1 \eta F_T`
     is precisely the existing adjoint/Green-style representation of the
     reduced first-order transport equation;
  2. a genuinely new adjoint / Green representation would have to be organized
     around a canonical linearized background BVP
     `\delta Y' = D_YF(x,Y_*(x);q)\,\delta Y + \cdots`
     on the active branch;
  3. the repo does not yet fix such a theorem-facing linearized background BVP
     for the clean axisymmetric background step, and that route would
     naturally represent variations of `\ell`, not the nonlinear quantity
     `\ell(Y_*)` itself.
  Therefore an adjoint / Green route is plausible in principle but not the
  minimal honest next input on the current record.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / adjoint-Green route audited; reduced-scalar adjoint is equivalent to the current eta identity, while a genuinely new full-BVP adjoint would require a canonical theorem-facing linearized background BVP not yet fixed; so this route is reserve, not default`
- What counts as verification:
  a theorem-facing proof of at least one of the following:
  1. a canonical clean-background linearized BVP whose adjoint represents the
     target functional or its required one-sided estimate in a form not
     equivalent to the present `\eta` identity;
  2. an exact theorem-facing argument that the full-BVP adjoint route collapses
     canonically to the current reduced identity, proving no extra strength is
     available there;
  3. a Green-type kernel formula with genuinely new sign/coercivity structure
     beyond the already isolated weighted dominance problem.
- Verification method:
  manual audit of the nonlinear background operator, its BC package, the target
  endpoint functional, and the relation between reduced scalar adjoint
  identities and possible full-BVP adjoint representations.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, does not change equations, BCs, solver behavior, or assumptions, and
  does not yet reopen the flexural Hurwitz step; it only classifies the
  adjoint/Green option as a reserve non-first-order mechanism rather than the
  minimal next theorem-facing target.
- Next action:
  keep the default next move at the global background integral-theorem level.
  Do not escalate first to a full adjoint/Green setup unless a canonical
  linearized background BVP is fixed and the reduced integral route is shown to
  be genuinely insufficient.

### V-S112. Conditional on Assumption LC, the direct weighted-integral split into `I_geom` and `I_coup` is sharp: on the preferred `LC-only` line the geometry term remains the more natural next subtarget, while on the fallback line `LC + LC-HM` the geometry endpoint is closed and the coupling term becomes the next blocker

- ID: `V-S112`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  Keep the active weighted dominance target in the split form
  `I_{geom} \ge \bar q I_{coup}`,
  where
  `I_{geom} := \int_{x_0}^1 \eta(x)(r_0(x)-x)/(x r_0(x))\, dx`
  and
  `I_{coup} := \int_{x_0}^1 \eta(x)(s_0(x)H(x))^+\, dx`.
  The direct theorem-facing audit is:
  1. for `I_{geom}`, the exact rewrites
     `(r_0-x)/(x r_0) = e_{\theta 0}/r_0 = 1/x - 1/r_0`
     and the background equations
     `r_0' = (1+e_{s0})c_0`,
     `e_{s0} = (1-\nu^2)T_{s0} - \nu e_{\theta 0}`
     remain exact but do not yet yield a theorem-facing lower bound after
     integration, because they reintroduce the unresolved quantities
     `T_{s0}` and `c_0`;
  2. for `I_{coup}`, the exact `H,J,\mu,\eta` structure yields
     `((\eta J)/\mu)' = \eta c_0 H`,
     so the current package naturally controls the weighted quantity
     `\int \eta c_0 H`, not the active positive part
     `\int \eta(s_0 H)^+`;
  3. together with the available bound `|s_0| \le 1`, this gives only soft
     estimates through `|H|`, not a theorem-facing upper bound for `I_{coup}`.
  Therefore the direct integral split is sharp but still open.
  The route split should now be read explicitly:
  on the preferred `LC-only` line, the geometry side remains the more natural
  next subtarget;
  on the fallback line conditional on `LC + LC-HM`, the geometry-side endpoint
  `I_{geom}=D(1)` is closed by assumption, so the next actual blocker is the
  missing theorem-facing upper bound for `I_{coup}`.
  Under the physical-semantic screen, stronger global sign theorems for
  `\varphi_0`, `s_0`, or `e_{\theta 0}`, and broader branch-law theorems, are
  still stronger than necessary here.
  The more natural default next subtarget is now the geometry side:
  derive a theorem-facing lower bound for `I_{geom}`.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `LC-only: the direct integral split is explicit and sharp; no theorem-facing lower bound for I_geom or upper bound for I_coup is yet closed at this level, and because the coupling side currently controls eta c0 H rather than eta(s0 H)^+, the geometry side remains the more natural next default subtarget / LC+HM: the geometry endpoint I_geom=D(1) is closed by fallback assumption, so the next blocker is the still-open coupling-side upper bound for I_coup`
- What counts as verification:
  a theorem-facing proof of at least one of the following:
  1. a lower bound for
     `I_{geom} = \int_{x_0}^1 \eta(r_0-x)/(x r_0)`;
  2. an upper bound for
     `I_{coup} = \int_{x_0}^1 \eta(s_0 H)^+`;
  3. an equally weak one-sided integral inequality sufficient to sign or bound
     `T_{s0}(x_0)`;
  4. an exact theorem-facing argument showing that a lower bound for
     `I_{geom}` is the truly minimal next subtarget among those options.
- Verification method:
  manual direct-integral audit of the active dominance inequality, exact
  rewrites of the geometry and coupling integrands, and conservative blocker
  selection under the physical-semantic screening rule.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, does not change equations, BCs, solver behavior, or assumptions, and
  does not yet reopen the flexural Hurwitz step; it only sharpens the active
  integral-theorem target by splitting it into the geometry and coupling
  subtargets and selecting the more natural next one.
- Next action:
  keep the route split explicit:
  on the preferred `LC-only` line, pursue a theorem-facing lower bound for
  `I_{geom}` first;
  on the fallback line conditional on `LC + LC-HM`, treat `I_{geom}=D(1)` as
  already closed by assumption and move next to the coupling side, namely an
  upper bound for `I_{coup}` or an equally weak control converting the exact
  information on `\eta c_0 H` into control of `\eta(s_0 H)^+`.

### V-S113. Conditional on Assumption LC, the geometry integral `I_geom` does admit a direct positive-kernel representation; the lower-bound problem reduces to the source term `c_0-1+(1-\nu^2)T_{s0}c_0`

- ID: `V-S113`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  On the current clean branch, define
  `e_{\theta 0} := (r_0-x)/x`,
  so
  `I_{geom} = \int_{x_0}^1 \eta(x)e_{\theta 0}(x)/r_0(x)\, dx`.
  Then the exact background kinematics give
  `r_0 = x(1+e_{\theta 0})`,
  `r_0' = (1+e_{s0})c_0`,
  `e_{s0} = (1-\nu^2)T_{s0} - \nu e_{\theta 0}`,
  hence the exact linear geometry equation
  `x e_{\theta 0}' + (1+\nu c_0)e_{\theta 0}
   = c_0 - 1 + (1-\nu^2)T_{s0}c_0`.
  Because the active BC package includes `r_0(x_0)=x_0`, one has
  `e_{\theta 0}(x_0)=0`.
  Therefore, with the positive integrating factor
  `\rho(x) := x \exp(\int_{x_0}^x \nu c_0(s)/s\, ds) > 0`,
  one gets the exact Volterra representation
  `e_{\theta 0}(x)
   = \rho(x)^{-1}\int_{x_0}^x \rho(\xi)
     [c_0(\xi)-1+(1-\nu^2)T_{s0}(\xi)c_0(\xi)]/\xi\, d\xi`.
  Substituting this into `I_{geom}` and applying Fubini gives
  `I_{geom}
   = \int_{x_0}^1 K_{geom}(\xi)
     [c_0(\xi)-1+(1-\nu^2)T_{s0}(\xi)c_0(\xi)]/\xi\, d\xi`,
  where
  `K_{geom}(\xi)
   := \rho(\xi)\int_{\xi}^1 \eta(x)/(r_0(x)\rho(x))\, dx \ge 0`,
  with `K_{geom}(\xi)>0` for `\xi<1` and `K_{geom}(1)=0`.
  So a genuine geometry-side lower-bound route exists:
  a lower bound for `I_{geom}` is reduced to a one-sided estimate on the
  source term `c_0-1+(1-\nu^2)T_{s0}c_0` under a positive kernel.
  This is sharper than the earlier raw rewrites
  `e_{\theta 0}/r_0 = 1/x - 1/r_0`.
  It is still not closed, because the exact negative term
  `c_0-1 = -(1-c_0) \le 0` is explicit, while the compensating lower bound on
  `(1-\nu^2)T_{s0}c_0` is not yet theorem-facingly available.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / a direct geometry-side positive-kernel route for I_geom is now visible; the remaining obstacle is the lack of a theorem-facing lower bound on the source term c0-1+(1-nu^2)T_s0 c0`
- What counts as verification:
  a theorem-facing proof of at least one of the following:
  1. a lower bound on the source term
     `c_0-1+(1-\nu^2)T_{s0}c_0`
     strong enough to give a lower bound for `I_{geom}`;
  2. an equivalent one-sided lower bound for `I_{geom}` obtained from the same
     positive-kernel representation;
  3. a reduction showing that the minimal remaining geometry-side blocker is
     exactly the source-term estimate above.
- Verification method:
  manual geometry-side reduction of the exact background kinematics to a linear
  equation for `e_{\theta 0}`, followed by an integrating-factor / Fubini
  representation with positive kernel and a conservative source-term audit.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, does not change equations, BCs, solver behavior, or assumptions, and
  does not yet reopen the flexural Hurwitz step; it only sharpens the geometry
  subtarget from a raw lower-bound search on `I_{geom}` to the explicit
  source-term lower-bound problem above.
- Next action:
  pursue a theorem-facing lower bound for the source term
  `c_0-1+(1-\nu^2)T_{s0}c_0` under the positive kernel `K_{geom}/x`.
  Do not default instead to stronger global sign theorems for `\varphi_0` or
  `e_{\theta 0}`, or to broader branch-law theorems, unless this sharper
  geometry-side route later proves insufficient.

### V-S114. Conditional on Assumption LC, the raw split `S = -(1-c_0) + (1-\nu^2)T_{s0}c_0` is the best active source form for the geometry-side lower-bound problem; the rewrite `S = r_0' - 1 + \nu c_0 e_{\theta 0}` is exact but currently only cosmetic

- ID: `V-S114`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  Keep the geometry-side source term
  `S := c_0 - 1 + (1-\nu^2)T_{s0}c_0`.
  The exact theorem-facing rewrites currently available are:
  1. the raw split
     `S = -(1-c_0) + (1-\nu^2)T_{s0}c_0`;
  2. using
     `(1-\nu^2)T_{s0} = e_{s0} + \nu e_{\theta 0}`
     and
     `r_0' = (1+e_{s0})c_0`,
     the exact kinematic form
     `S = r_0' - 1 + \nu c_0 e_{\theta 0}
        = r_0' - 1 + \nu c_0(r_0-x)/x`;
  3. the half-angle refinement of the negative part
     `c_0 - 1 = -2\sin^2(\varphi_0/2)`.
  The conservative theorem-facing comparison is:
  the raw split is the best active lower-bound form.
  It is preferred because it isolates the already explicit loss term
  `1-c_0 \ge 0`, so the remaining burden is concentrated on the compensating
  positive candidate `(1-\nu^2)T_{s0}c_0`.
  By contrast, the rewrite
  `S = r_0' - 1 + \nu c_0 e_{\theta 0}`
  is exact but currently less suitable as the active form:
  it replaces the explicit negative piece `c_0-1` by two terms of unresolved
  sign and therefore mainly repackages the same lower-bound difficulty.
  The half-angle formula is exact but only sharpens the already known negative
  part and does not by itself improve the missing lower bound on the
  compensating term.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / the source-term lower-bound problem is now best read in the raw split S = -(1-c0) + (1-nu^2)T_s0 c0; the kinematic rewrite through r0'-1 + nu c0 e_theta0 is exact but does not currently improve the comparison structure`
- What counts as verification:
  a theorem-facing proof of at least one of the following:
  1. a lower bound on `(1-\nu^2)T_{s0}c_0` strong enough, under `K_{geom}/x`,
     to dominate `1-c_0`;
  2. an equivalent one-sided lower bound for the raw source form `S`;
  3. an exact theorem-facing argument that the kinematic form
     `r_0' - 1 + \nu c_0 e_{\theta 0}` does not produce a stronger lower-bound
     route than the raw split.
- Verification method:
  manual audit of the exact source-term algebra and conservative comparison of
  the available source-level rewrites under the physical-semantic screening
  rule.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, does not change equations, BCs, solver behavior, or assumptions, and
  does not yet reopen the flexural Hurwitz step; it only chooses the best
  current source-level form in which the geometry-side lower-bound problem
  should now be attacked.
- Next action:
  keep the raw split
  `S = -(1-c_0) + (1-\nu^2)T_{s0}c_0`
  as the active source form and pursue a lower bound on the compensating term
  `(1-\nu^2)T_{s0}c_0` under the positive kernel.
  Do not default instead to stronger global sign theorems or to the kinematic
  rewrite unless the raw split later proves genuinely insufficient.

### V-S115. Conditional on Assumption LC, the weighted compensating term is the exact active comparison object: `I_geom = J_comp - J_loss`, but no theorem-facing lower bound for `J_comp` is yet available

- ID: `V-S115`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  On the current clean branch, define
  `J_{comp}
   := \int_{x_0}^1 [K_{geom}(x)/x](1-\nu^2)T_{s0}(x)c_0(x)\, dx`
  and
  `J_{loss}
   := \int_{x_0}^1 [K_{geom}(x)/x](1-c_0(x))\, dx`.
  Since
  `S = -(1-c_0) + (1-\nu^2)T_{s0}c_0`,
  the positive-kernel representation of `I_{geom}` becomes exactly
  `I_{geom} = J_{comp} - J_{loss}`.
  Therefore the desired comparison
  `J_{comp} \ge J_{loss}`
  is equivalent to `I_{geom} \ge 0`.
  The exact compensating-term rewrites currently available are:
  1. the raw product `(1-\nu^2)T_{s0}c_0`;
  2. `c_0 e_{s0} + \nu c_0 e_{\theta 0}`;
  3. `r_0' - c_0 + \nu c_0 e_{\theta 0}`.
  The conservative theorem-facing audit is:
  these are exact but none yet yields a one-sided lower bound for `J_{comp}`
  after weighting by `K_{geom}/x`.
  Multiplying the `T_{s0}` equation by `c_0`, or re-expressing `T_{s0}` via
  the rotated variables `(A,B)`, does not presently improve the comparison
  structure; it mainly repackages the same unresolved sign difficulty.
  Under the physical-semantic screen, broader global sign theorems for
  `\varphi_0`, `c_0`, or `e_{\theta 0}`, and broader branch-law theorems, are
  stronger than necessary here.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / the weighted compensating term is now the exact active comparison object, but no theorem-facing lower bound for J_comp is yet available; the desired comparison J_comp >= J_loss remains open`
- What counts as verification:
  a theorem-facing proof of at least one of the following:
  1. a lower bound for `J_{comp}` strong enough to imply `J_{comp} \ge J_{loss}`;
  2. a direct weighted comparison `J_{comp} \ge J_{loss}`;
  3. an equally weak one-sided integral estimate sufficient to conclude
     `I_{geom} \ge 0`.
- Verification method:
  manual audit of the weighted compensating term under the positive kernel,
  comparison of the exact available rewrites, and conservative lower-bound
  diagnosis under the physical-semantic screening rule.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, does not change equations, BCs, solver behavior, or assumptions, and
  does not yet reopen the flexural Hurwitz step; it only sharpens the geometry
  blocker from a source-form question to the exact weighted comparison object
  `J_{comp} \ge J_{loss}`.
- Next action:
  keep the default next target at the direct weighted comparison
  `J_{comp} \ge J_{loss}`.
  Do not default instead to stronger global sign theorems or broader branch-law
  theorems unless this exact weighted comparison route later proves
  insufficient.

### V-S116. Conditional on Assumption LC, the cumulative comparison functional `D(y)` has an exact evolution identity, but no theorem-facing comparison law is yet available

- ID: `V-S116`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  Define
  `D(y)
   := \int_{x_0}^y [K_{geom}(x)/x]
      ((1-\nu^2)T_{s0}(x)c_0(x) - (1-c_0(x)))\, dx`.
  Then the exact theorem-facing facts already available are:
  1. `D(x_0)=0` and `D(1)=I_{geom}`;
  2. the exact differential law
     `D'(y) = [K_{geom}(y)/y]S(y)`;
  3. using
     `y e_{\theta 0}' + (1+\nu c_0)e_{\theta 0} = S`
     and
     `K_{geom}' = K_{geom}(1+\nu c_0)/y - \eta/r_0`,
     the equivalent exact cumulative identity
     `D'(y) = (K_{geom}e_{\theta 0})'(y) + \eta(y)e_{\theta 0}(y)/r_0(y)`,
     hence
     `D(y)
      = K_{geom}(y)e_{\theta 0}(y)
      + \int_{x_0}^y \eta(x)e_{\theta 0}(x)/r_0(x)\, dx`.
  So `D` is a genuine cumulative object, not a cosmetic renaming.
  However, no theorem-facing comparison law is yet available:
  the current package still does not sign the right-hand side above, and any
  monotonicity or positivity theorem for `D` would require a one-sided
  estimate on `e_{\theta 0}` or on the source term `S`.
  Under the physical-semantic screen, a global sign theorem for
  `e_{\theta 0}` is stronger than the default next need.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / D(y) has an exact cumulative identity, but no theorem-facing monotonicity or comparison law is yet available; the remaining blocker is a weaker one-sided estimate on the right-hand side rather than a new reformulation of D`
- What counts as verification:
  a theorem-facing proof of at least one of the following:
  1. a one-sided differential inequality for `D(y)`;
  2. a one-sided estimate on
     `K_{geom}(y)e_{\theta 0}(y)
      + \int_{x_0}^y \eta e_{\theta 0}/r_0`
     strong enough to conclude `D(1)\ge 0`;
  3. an equally weak cumulative comparison law implying `J_{comp}\ge J_{loss}`.
- Verification method:
  manual cumulative-functional audit of the exact weighted comparison object,
  exact differentiation of `D` and `K_{geom}`, and conservative comparison-law
  diagnosis under the physical-semantic screening rule.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, does not change equations, BCs, solver behavior, or assumptions, and
  does not yet reopen the flexural Hurwitz step; it only sharpens the weighted
  comparison step from a static integral inequality to an exact cumulative law
  whose missing ingredient is now explicit.
- Next action:
  keep the default next move at the weakest cumulative target:
  a one-sided estimate on the exact right-hand side
  `K_{geom}(y)e_{\theta 0}(y) + \int_{x_0}^y \eta e_{\theta 0}/r_0`
  strong enough to imply `D(1)\ge 0`.
  Do not default instead to broader global sign theorems or branch-law
  theorems unless this cumulative route later proves genuinely insufficient.

### V-S117. Conditional on Assumption LC, the physically meaningful cumulative object behind `D(y)` is the circumferential stretch defect `e_{\theta 0} = \lambda_{\theta 0}-1`; the current package gives only the weak admissibility floor `\lambda_{\theta 0}>0`, which is too weak by itself to sign `D`

- ID: `V-S117`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  On the active clean branch,
  `e_{\theta 0} := (r_0-x)/x`
  is the circumferential strain / circumferential-stretch defect, with
  `\lambda_{\theta 0} := r_0/x = 1 + e_{\theta 0}`.
  The current theorem-facing facts already available are:
  1. `e_{\theta 0}(x_0)=0` and `\lambda_{\theta 0}(x_0)=1`, because
     `r_0(x_0)=x_0`;
  2. because `x>0` on `[x_0,1]` and the current reduction is written on the
     clean branch with `r_0>0`, the weak admissibility floor
     `\lambda_{\theta 0}>0`, equivalently `e_{\theta 0}>-1`, is available on
     the current branch package;
  3. the cumulative identity for `D` may therefore be rewritten exactly as
     `D(y)
      = K_{geom}(y)(\lambda_{\theta 0}(y)-1)
      + \int_{x_0}^y [\eta(x)/x](1-\lambda_{\theta 0}(x)^{-1})\, dx`.
  This is a genuine physical reformulation of the same cumulative comparison
  problem. However, the presently available admissibility floor is still too
  weak to sign `D` or to prove `D(1)\ge 0`: positivity of
  `\lambda_{\theta 0}` alone only gives `e_{\theta 0}>-1`, while the kernel
  `1-\lambda_{\theta 0}^{-1}` remains unbounded below as
  `\lambda_{\theta 0}\downarrow 0`.
  Under the physical-semantic screen, a global sign theorem for
  `e_{\theta 0}` or for `\lambda_{\theta 0}-1` is stronger than the default
  need. The honest next physical target is instead a weaker admissibility or
  cumulative lower bound for `\lambda_{\theta 0}` strong enough to lower-bound
  the right-hand side above.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / the physically meaningful cumulative object is now clearly lambda_theta0 = 1 + e_theta0, but the current theorem-facing control stops at the weak admissibility floor lambda_theta0 > 0; this is too weak by itself to sign D(1)`
- What counts as verification:
  a theorem-facing proof of at least one of the following:
  1. a quantitative lower bound for `\lambda_{\theta 0}` on the clean branch
     strong enough to imply a lower bound for
     `\int_{x_0}^1 [\eta(x)/x](1-\lambda_{\theta 0}(x)^{-1})\, dx`;
  2. a direct cumulative lower bound for
     `K_{geom}(y)(\lambda_{\theta 0}(y)-1)
      + \int_{x_0}^y [\eta(x)/x](1-\lambda_{\theta 0}(x)^{-1})\, dx`;
  3. an equally weak admissibility theorem for the circumferential stretch
     sufficient to conclude `D(1)\ge 0`.
- Verification method:
  manual physical-semantic audit of the exact cumulative identity for `D`,
  exact rewrite through the circumferential stretch
  `\lambda_{\theta 0}=r_0/x`, and conservative admissibility-based blocker
  selection.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, does not change equations, BCs, solver behavior, or assumptions, and
  does not yet reopen the flexural Hurwitz step; it only sharpens the
  cumulative geometry blocker from a generic one-sided estimate on
  `e_{\theta 0}` to the weaker physical target of admissibility-level control
  on `\lambda_{\theta 0}`.
- Next action:
  keep the default next move at the weakest physical cumulative target:
  prove a weak admissibility theorem or cumulative lower bound for the
  circumferential stretch `\lambda_{\theta 0}` strong enough to lower-bound
  `K_{geom}(y)(\lambda_{\theta 0}(y)-1)
   + \int_{x_0}^y [\eta(x)/x](1-\lambda_{\theta 0}(x)^{-1})\, dx`.
  Do not default instead to stronger global sign theorems for
  `\varphi_0`, `c_0`, or `e_{\theta 0}`, or to broader branch-law theorems,
  unless this weaker admissibility route later proves genuinely insufficient.

### V-S118. Conditional on Assumption LC, the endpoint quantity `D(1)` reduces exactly to a weighted harmonic-mean test for the circumferential stretch; among pure pointwise lower bounds, `\lambda_{\theta 0}\ge 1` is the weakest sufficient one

- ID: `V-S118`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  Because
  `K_{geom}(1)
   = \rho(1)\int_1^1 \eta(x)/(r_0(x)\rho(x))\, dx = 0`,
  the exact cumulative identity from `V-S116` simplifies at the active
  endpoint to
  `D(1)=I_{geom}
   = \int_{x_0}^1 [\eta(x)/x](1-\lambda_{\theta 0}(x)^{-1})\, dx`.
  Hence:
  1. since `1-\lambda^{-1}` is strictly increasing on `(0,\infty)`,
     every pointwise lower bound
     `\lambda_{\theta 0}(x)\ge \lambda_* > 0`
     yields the exact consequence
     `D(1)\ge W_\eta(1-\lambda_*^{-1})`,
     where `W_\eta := \int_{x_0}^1 \eta(x)/x\, dx > 0`;
  2. among pure pointwise lower bounds, the weakest sufficient one is exactly
     `\lambda_{\theta 0}\ge 1`;
  3. any weaker uniform floor
     `\lambda_{\theta 0}\ge \lambda_*` with `0<\lambda_*<1`,
     equivalently `\lambda_{\theta 0}\ge 1-\delta` with `\delta>0`,
     is not sufficient by itself;
  4. a weaker cumulative sufficient package is the weighted harmonic-mean
     condition
     `\int_{x_0}^1 [\eta(x)/(x\lambda_{\theta 0}(x))]\, dx
      \le \int_{x_0}^1 \eta(x)/x\, dx`,
     equivalently
     `H_{\eta/x}(\lambda_{\theta 0}) \ge 1`.
  This is strictly weaker than pointwise `\lambda_{\theta 0}\ge 1` and is the
  best currently visible admissibility-type sufficient package for `D(1)\ge 0`.
  The current theorem-facing package, however, still supplies only the weak
  floor `\lambda_{\theta 0}>0`; no theorem-facing route to the weighted
  harmonic-mean bound is yet available from the present clean ODE/BC record.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / the exact endpoint test for D(1) is now a weighted harmonic-mean condition on lambda_theta0; this is weaker than pointwise lambda_theta0 >= 1, but the current theorem-facing package does not yet support it`
- What counts as verification:
  a theorem-facing proof of at least one of the following:
  1. the weighted harmonic-mean inequality
     `\int_{x_0}^1 [\eta/(x\lambda_{\theta 0})]
      \le \int_{x_0}^1 \eta/x`;
  2. an equally weak cumulative admissibility theorem implying the same;
  3. a pointwise lower bound `\lambda_{\theta 0}\ge 1` on the active clean
     branch, if the weaker harmonic-mean route later proves inaccessible.
- Verification method:
  manual endpoint specialization of the exact cumulative identity for `D`,
  monotonicity audit of the kernel `1-\lambda^{-1}`, and conservative
  sufficient-condition selection under the physical-semantic screening rule.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, does not change equations, BCs, solver behavior, or assumptions, and
  does not yet reopen the flexural Hurwitz step; it only sharpens the active
  physical admissibility target for the geometry-side step from a generic lower
  bound on `\lambda_{\theta 0}` to the precise weighted harmonic-mean
  condition above.
- Next action:
  keep the default next move at the weakest sufficient endpoint target:
  prove the weighted harmonic-mean bound
  `\int_{x_0}^1 [\eta/(x\lambda_{\theta 0})]
   \le \int_{x_0}^1 \eta/x`.
  Do not default instead to the stronger pointwise condition
  `\lambda_{\theta 0}\ge 1`, or to broader global sign / branch-law theorems,
  unless this weaker cumulative admissibility route later proves genuinely
  insufficient.

### V-S119. Conditional on Assumption LC, the weighted harmonic-mean inequality is the exact active endpoint target; the first theorem-facing obstruction is the missing comparison law for the inverse stretch `u=\lambda_{\theta 0}^{-1}` against the comparator `1`

- ID: `V-S119`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  Define `u := \lambda_{\theta 0}^{-1}` on the active clean branch.
  Then the exact geometry equation
  `x e_{\theta 0}' + (1+\nu c_0)e_{\theta 0} = S`,
  with `e_{\theta 0} = \lambda_{\theta 0}-1`,
  is equivalent to the exact inverse-stretch Riccati equation
  `x u' = (1+\nu c_0)u - (1+\nu c_0 + S)u^2`,
  with `u(x_0)=1`.
  The active endpoint target from `V-S118` is therefore exactly
  `\int_{x_0}^1 [\eta(x)/x]u(x)\, dx \le \int_{x_0}^1 \eta(x)/x\, dx`.
  The natural comparator is `u \equiv 1`, but the comparator defect is exactly
  `-S`: evaluating the right-hand side of the `u`-equation at `u=1` gives
  `-S`.
  Therefore the first theorem-facing obstruction to deriving the weighted
  harmonic-mean inequality from the present clean ODE/BC package is now sharp:
  the repo does not yet provide a one-sided comparison law for `u` against `1`,
  because the sign of the source term `S` remains unresolved on the current
  branch package.
  The theorem/status split should now be read explicitly:
  on the preferred `LC-only` line, this weighted harmonic-mean inequality
  remains the active endpoint target to be derived through one-sided control on
  `S`;
  on the fallback line conditional on `LC + LC-HM` (with `LC-HM` registered in
  `docs/assumptions/assumptions.md`), the same endpoint condition is assumed
  and the geometry-side endpoint `D(1)\ge 0` is therefore closed by fallback.
  Under the physical-semantic screen, stronger fallback routes such as pointwise
  `\lambda_{\theta 0}\ge 1`, global sign theorems for
  `\varphi_0`, `c_0`, or `e_{\theta 0}`, or broader branch-law theorems are
  still stronger than the active need.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `LC-only: the weighted harmonic-mean inequality is still the exact active endpoint target, but the current theorem-facing package lacks the one-sided comparison law for u=lambda_theta0^{-1} against the comparator 1 because the sign of S is unresolved / LC+HM: the geometry-side endpoint D(1)>=0 is closed by fallback assumption, and this fallback closure does not replace the preferred LC-only theorem route`
- What counts as verification:
  a theorem-facing proof of at least one of the following:
  1. a one-sided comparison theorem placing `u` below `1` in the weighted
     sense needed for
     `\int [\eta/x]u \le \int \eta/x`;
  2. a direct weighted upper bound on `u=\lambda_{\theta 0}^{-1}` implying the
     harmonic-mean inequality;
  3. a theorem-facing proof that no such comparison can be derived from the
     current package alone, in which case the harmonic-mean inequality itself
     should be adopted as the minimal fallback assumption rather than replaced
     by stronger pointwise or angle-sign assumptions.
- Verification method:
  manual reduction of the exact geometry equation to the inverse-stretch
  Riccati form, exact identification of the comparator defect at `u=1`, and
  conservative blocker selection under the physical-semantic screening rule.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, does not change equations, BCs, solver behavior, or assumptions, and
  does not yet reopen the flexural Hurwitz step; it only sharpens the active
  endpoint admissibility target by isolating the exact comparison-theoretic
  obstruction in the inverse-stretch equation.
- Next action:
  keep the default next move on the `LC-only` line at the weakest exact
  endpoint target:
  derive a theorem-facing weighted upper bound on
  `u=\lambda_{\theta 0}^{-1}` sufficient for
  `\int [\eta/x]u \le \int \eta/x`;
  if that still cannot be obtained from the clean ODE/BC package, then the
  fallback line conditional on `LC + LC-HM` may treat the weighted
  harmonic-mean inequality as assumed, thereby closing the geometry-side
  endpoint `D(1)\ge 0` by fallback rather than by theorem.
  Do not default instead to stronger pointwise, angle-sign, or branch-law
  assumptions unless this weaker route later proves genuinely insufficient.

### V-S120. Conditional on Assumption LC, the scalar Riccati comparison problem sharpens the sufficient-control hierarchy on `S`: `S\ge 0` is the weakest pure pointwise barrier condition for `u\le 1`, while the weaker endpoint-only condition `\int (K_{geom}/x)S \ge 0` is already equivalent to the target `D(1)\ge 0`

- ID: `V-S120`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  Keep the exact inverse-stretch Riccati equation
  `x u' = (1+\nu c_0)u - (1+\nu c_0 + S)u^2`,
  with `u(x_0)=1`,
  and define the comparison variable `w := 1-u`.
  Then the exact comparison equation is
  `x w' = S - (1+\nu c_0+2S)w + (1+\nu c_0+S)w^2`,
  with `w(x_0)=0`.
  Hence:
  1. among pure state-independent pointwise conditions on `S` alone,
     `S\ge 0` is the weakest sufficient one for using `u\equiv 1` as a global
     barrier, because at every contact point with `w=0` one has `x w' = S`;
     thus `S\ge 0` would force `w\ge 0`, equivalently `u\le 1`, hence
     `D(1)\ge 0`;
  2. any weaker state-independent pointwise floor on `S` allowing `S<0`
     somewhere is not by itself sufficient to preserve the barrier at a
     contact point;
  3. a weaker endpoint-only sufficient package is
     `\int_{x_0}^1 [K_{geom}(x)/x]S(x)\, dx \ge 0`,
     but this is already exactly equivalent to `D(1)\ge 0`, so it does not
     produce a genuinely simpler target.
  Therefore the current theorem-facing obstruction is now sharper:
  the repo does not yet provide one-sided control on `S` strong enough to feed
  either the pure pointwise barrier route or a genuinely weaker comparison
  theorem for `u`.
  Under the physical-semantic screen, stronger fallback routes such as global
  sign theorems for `\varphi_0`, `c_0`, `e_{\theta 0}`, pointwise
  `\lambda_{\theta 0}\ge 1`, or broader branch-law theorems remain stronger
  than the active need.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / the Riccati comparison frame now shows that S>=0 is the weakest pure pointwise barrier condition for u<=1, but the current package does not yet support S>=0 or a genuinely weaker comparison theorem; the weighted endpoint condition ∫(K_geom/x)S>=0 is weaker but equivalent to the target`
- What counts as verification:
  a theorem-facing proof of at least one of the following:
  1. `S\ge 0` on the active clean branch;
  2. a genuinely weaker comparison theorem for `u` using one-sided control on
     `S` that is sufficient for `D(1)\ge 0`;
  3. a theorem-facing proof that no such weaker comparison can be derived from
     the current package, in which case the weighted harmonic-mean inequality
     should remain the minimal fallback assumption.
- Verification method:
  manual scalar-comparison reduction of the exact inverse-stretch Riccati
  equation, exact derivation of the `w=1-u` comparison equation, and
  conservative sufficient-condition audit under the physical-semantic
  screening rule.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, does not change equations, BCs, solver behavior, or assumptions, and
  does not yet reopen the flexural Hurwitz step; it only sharpens the scalar
  comparison problem by separating the weakest pure pointwise sufficient
  control on `S` from the weaker but target-equivalent endpoint condition.
- Next action:
  keep the default next move at the weakest exact endpoint target:
  if a theorem-facing route to one-sided control on `S` still does not emerge,
  keep the weighted harmonic-mean inequality itself as the minimal fallback
  assumption rather than replacing it by the stronger pointwise condition
  `S\ge 0`.
  Do not default instead to stronger global sign, pointwise-stretch, or
  branch-law assumptions unless this weaker route later proves genuinely
  insufficient.

### V-S121. Conditional on Assumption LC, the physical audit of `S` leaves `S\ge 0` as the only clearly formulated physically meaningful sufficient control on `S` itself; weaker sufficient controls are either trajectory-dependent, require contact localization, or are already target-equivalent

- ID: `V-S121`
- Claim / Hypothesis:
  Fix `(n,q)` and assume Assumption LC.
  The exact source term
  `S = c_0 - 1 + (1-\nu^2)T_{s0}c_0`
  is best read in the split form
  `S = -(1-c_0) + (1-\nu^2)T_{s0}c_0`.
  Here
  `c_0-1 = -2\sin^2(\varphi_0/2)\le 0`
  is the exact geometric turning/projection loss, while
  `(1-\nu^2)T_{s0}c_0`
  is the meridional constitutive compensation.
  In the scalar comparison equation for `w:=1-u`,
  `x w' = S - (1+\nu c_0+2S)w + (1+\nu c_0+S)w^2`,
  this yields the following sufficient-control hierarchy:
  1. `S\ge 0` is the weakest pure state-independent pointwise sufficient
     condition on `S` itself;
  2. any weaker state-independent pointwise floor on `S` allowing `S<0`
     somewhere, including `S\ge -\varepsilon`, is not by itself sufficient;
  3. weaker sufficient packages do exist in principle, but they are not yet
     sharp theorem-facing targets:
     positivity of `S` on a decisive subregion would require a first-contact
     localization theorem;
     a trajectory-dependent bound such as `S\ge -A(x)w` depends on the unknown
     comparison trajectory;
     and the endpoint condition
     `\int_{x_0}^1 [K_{geom}(x)/x]S(x)\, dx \ge 0`
     is already exactly equivalent to `D(1)\ge 0`.
  Therefore, at the current theorem-facing level, `S\ge 0` remains the only
  clearly formulated physically meaningful sufficient control on `S` itself.
  No weaker non-equivalent one-sided control is yet sharp on the current clean
  branch record.
- Type: `strategy-level hypothesis`
- Source file(s):
  `docs/theory/current_simple_support_status.md`;
  `docs/theory/current_simple_support_criterion_bridge_note.md`;
  `docs/theory/current_theory_verification_map.md`;
  `docs/theory/vyvod_uravneniy_updated17.md`;
  `src/shell_buckling/mixed_weak/_core_solver_common.py`;
  `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`;
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
  `docs/assumptions/assumptions.md`.
- Current status:
  `reduced conditionally under LC / the physical audit of S does not yet reveal a weaker non-equivalent theorem-facing sufficient control; S>=0 remains the only clearly formulated physically meaningful sufficient control on S itself`
- What counts as verification:
  a theorem-facing proof of at least one of the following:
  1. `S\ge 0` on the active clean branch;
  2. a first-contact localization theorem together with `S\ge 0` on the
     decisive subregion;
  3. a genuinely weaker comparison theorem using trajectory-dependent
     one-sided control on `S`;
  4. a theorem-facing proof that none of those weaker non-equivalent routes can
     be derived from the current clean package, in which case the weighted
     harmonic-mean inequality should remain the minimal fallback assumption.
- Verification method:
  manual physical-semantic audit of the split source term `S`, exact analysis
  of the scalar comparison equation for `w=1-u`, and conservative comparison of
  weaker sufficient packages under the physical-semantic screening rule.
- Verification boundary:
  this does not prove Assumption LC, does not close the strict continuation
  line, does not change equations, BCs, solver behavior, or assumptions, and
  does not yet reopen the flexural Hurwitz step; it only sharpens the source-
  term strategy by separating the physically meaningful sufficient control
  `S\ge 0` from weaker but currently ungrounded or target-equivalent variants.
- Next action:
  absent a theorem-facing contact-localization or trajectory-dependent
  comparison theorem, do not silently replace the weighted harmonic-mean target
  by ad hoc weaker-looking source conditions.
  Keep the weighted harmonic-mean inequality as the minimal fallback
  assumption, not a stronger pointwise or angle-sign statement.
