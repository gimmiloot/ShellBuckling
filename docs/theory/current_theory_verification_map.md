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

