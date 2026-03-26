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

### V-N1. `sigma_min(B_mix(q)) = 0` is the current working criterion

- ID: `V-N1`
- Claim / Hypothesis:
  `sigma_min(B_mix(q)) = 0` is the correct **working** spectral criterion for
  the present mixed-weak branch.
- Type: `numerical`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` sections 2.2.2 and 2.3;
  `docs/assumptions/assumptions.md` A7;
  `docs/journal/project_journal_updated14.md` sections 4 and 10.
- Current status: `partially confirmed, tightened by pilot 05`
- What counts as verification:
  live computability of `sigma_min(B_mix)` on the active q-range, reproducible
  refined minima under the current fine/adaptive/targeted scan workflow,
  moderate resolution robustness in the present testbench, and repository-level
  comparison evidence that this picture differs from the rejected old
  reduced/full architecture.
- Verification method:
  numerical testbench, project-state comparison.
- Verification boundary:
  working criterion inside the current mixed-weak exploratory/testbench branch
  only; the pilot does not prove the final closed mixed BVP criterion or the
  final physical simple-support critical load.
- Next action:
  keep this tightened working-criterion status, but continue linking the
  testbench spectral signal to the final mixed BVP before promoting stronger
  claims.

### V-N2. Current candidate load `n=13`, `qРІвЂ°в‚¬3.79..3.80 MPa`

- ID: `V-N2`
- Claim / Hypothesis:
  The present best mixed-weak candidate is
  `n = 13`, `q РІвЂ°в‚¬ 3.79..3.80 MPa`, with the nearest competitor near
  `n = 14`, `q РІвЂ°в‚¬ 4.28 MPa`.
- Type: `numerical`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` sections 2.3 and 3.1;
  `docs/assumptions/assumptions.md` A8;
  `docs/journal/project_journal_updated14.md` section 10.
- Current status: `exploratory`
- What counts as verification:
  reproducible localization under resolution/fine/adaptive/targeted scans and a
  clear statement of what the result does and does not mean.
- Verification method:
  numerical testbench.
- Verification boundary:
  exploratory mixed-weak candidate only; not validated as the final physical
  `simple support` critical load.
- Next action:
  keep the candidate archived, but do not promote it until the background and
  critical problem are fully consistent.

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

### V-I2. The current exploratory candidate is limited by problem consistency

- ID: `V-I2`
- Claim / Hypothesis:
  The main reason the current `3.79..3.80 MPa` candidate cannot be treated as a
  final `simple support` result is inconsistency between the axisymmetric
  background and the critical problem setup.
- Type: `interpretation`
- Source file(s):
  `docs/theory/vyvod_uravneniy_updated17.md` sections 2.4 and 3.1;
  `docs/assumptions/assumptions.md` A8 and A9.
- Current status: `partially confirmed`
- What counts as verification:
  direct architecture analysis showing that the earlier simple-support result
  did not come from a fully consistent full problem.
- Verification method:
  manual derivation, project-state analysis.
- Verification boundary:
  interpretation inside the current repository architecture; not yet a complete
  rebuilt solver proof.
- Next action:
  keep this limitation explicit in every summary of the candidate load.

### V-ST1. Main open problem is the axisymmetric simple-support background

- ID: `V-ST1`
- Claim / Hypothesis:
  The main remaining bottleneck is the axisymmetric simple-support background
  solver, not the existence of the mixed-weak critical structure itself.
- Type: `strategy`
- Source file(s):
  `docs/assumptions/assumptions.md` A12;
  `docs/theory/vyvod_uravneniy_updated17.md` sections 2.4 and 3.1;
  `proof_pilots/pilot_07_axisymmetric_simple_support_background/pilot_07_axisymmetric_simple_support_background.md`;
  `proof_pilots/pilot_08_simple_support_background_stabilization/pilot_08_simple_support_background_stabilization.md`;
  `proof_pilots/pilot_09_simple_support_local_branch_following/pilot_09_simple_support_local_branch_following.md`;
  `proof_pilots/pilot_10_high_load_simple_support_continuation/pilot_10_high_load_simple_support_continuation.md`;
  `proof_pilots/pilot_10_high_load_simple_support_continuation/branch_diagnostics.md`;
  `proof_pilots/pilot_11_shallow_vs_nonshallow_barrier_comparison/comparison_problem_statement.md`;
  `proof_pilots/pilot_12_high_load_branch_extension/pilot_12_high_load_branch_extension.md`;
  `proof_pilots/pilot_12_high_load_branch_extension/branch_consistency_check.md`;
  `proof_pilots/pilot_13_shallow_nonshallow_divergence_source/pilot_13_shallow_nonshallow_divergence_source.md`;
  `proof_pilots/pilot_15_shallow_bc_equivalence_audit/bc_equivalence_audit.md`;
  `proof_pilots/pilot_16_shallow_simple_support_comparator/shallow_problem_statement.md`;
  `proof_pilots/pilot_17_shallow_vs_nonshallow_simple_support_divergence/pilot_17_shallow_vs_nonshallow_simple_support_divergence.md`;
  `proof_pilots/pilot_18_revised_analytic_barrier_diagnosis/pilot_18_revised_analytic_barrier_diagnosis.md`;
  `proof_pilots/pilot_18_revised_analytic_barrier_diagnosis/edge_layer_scaling.md`;
  `proof_pilots/pilot_18_revised_analytic_barrier_diagnosis/jacobian_conditioning_check.py`;
  `proof_pilots/pilot_18_revised_analytic_barrier_diagnosis/term_balance_check.py`;
  `proof_pilots/pilot_19_edge_stretched_simple_support_continuation/comparison_note.md`;
  `proof_pilots/pilot_20_method_sweep_for_simple_support_ceiling/pilot_20_method_sweep_for_simple_support_ceiling.md`;
  `proof_pilots/pilot_20_method_sweep_for_simple_support_ceiling/method_comparison_table.md`;
  `proof_pilots/pilot_20_method_sweep_for_simple_support_ceiling/method_sweep.py`;
  `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/pilot_21_u_z_scaled_arc_like_continuation.md`;
  `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/u_z_scaled_arc_like_continuation.py`;
  `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/u_z_scaled_arc_like_results.json`;
  `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/continuation_runtime.py`;
  `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_u_z_scaled_arc_like_continuation.py`;
  `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/confirm_u_z_scaled_arc_like_continuation.py`;
  `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_continuation_workflow.md`;
  `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/fast_progress.json`;
  `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/confirm_results.json`;
  `proof_pilots/pilot_22_exact_load_shallow_vs_current_simple_support_comparison/compare_exact_loads.py`;
  `proof_pilots/pilot_22_exact_load_shallow_vs_current_simple_support_comparison/pilot_22_exact_load_shallow_vs_current_simple_support_comparison.md`;
  `proof_pilots/pilot_22_exact_load_shallow_vs_current_simple_support_comparison/comparison_results.json`;
  `docs/theory/current_simple_support_status.md`;
  `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`.
- Current status: `strategy only`
- Operational pointer:
  The live operational snapshot for this separate 6-state path is maintained in
  `docs/theory/current_simple_support_status.md`.
- What counts as verification:
  not a theorem; it is supported only insofar as current evidence points to the
  background as the dominant unresolved node. A separate active full-state
  simple-support background path exists, its live 6-state BC function matches
  the intended simple-support BC set, and its active equations match the
  supporting 6-state non-shallow block. On the old single-domain rescue-local
  workflow, `4.3434 MPa` remains reproducible while `4.3440 MPa` remains the
  first persistent failure with tiny BC residuals and strong right-edge
  concentration. Pilot 15 then showed that the old shallow comparison path was
  not BC-equivalent to simple support, pilot 16 built the strongest currently
  justified shallow simple-support comparator, and pilot 17 revisited the
  divergence sweep in that corrected BC setting. In the corrected simple-support
  comparison, the mapped mismatch is small at low load, first crosses the
  `0.05` bulk-rel-L2 threshold in any variable at `2.0 MPa` (`Phi0'`), becomes
  clearly overall visible at `3.0 MPa` (`theta0'` and `Phi0'`), grows with
  load, and remains smooth through the available high-load range rather than as
  a new barrier-localized qualitative jump. Pilot 18 adds a revised analytic
  diagnosis: a coarse discretized BVP Jacobian in the `4.3400..4.3434 MPa` band
  remains severely ill-conditioned but shows no collapsing near-zero-singular-
  value trend, while the right-edge term balance stays smooth and is dominated
  by the geometric hoop term `u_r/x` inside `T_theta`, by the `T_sn -> M_s ->
  varphi` coupling chain, and by a large `u_z` response with only moderate
  trig-gap corrections. Pilot 19 then shows that simple edge-focused mesh
  changes alone do not move the ceiling materially. Pilot 20 sharpens the
  numerical reading further: predictor-only and pseudo-arclength-like changes
  help only modestly, while an equation-preserving state-representation change
  (`u_z`-scaled solve) moves the bounded ceiling to `4.3520 MPa` without a
  bounded failure being hit in the packaged ladder. Pilot 21 then consolidates
  the practical continuation strategy: the exact pilot-20 `u_z`-scaled path,
  augmented only by auxiliary arc-like step adaptation, reproduces `4.3520 MPa`
  and carries the bounded staged ladder through `4.3550`, `4.3600`, `4.3700`,
  and `4.3800 MPa` with reproducible stage retests and no bounded failure in
  the packaged ladder. A newer checkpointed fast/confirm layer now reuses the
  same equations, BCs, and scaled continuation kernel in a more operational
  form: the first from-scratch fast run reaches `4.3900 MPa`, later resume runs
  carry the stored path first through `4.5000 MPa` and then onward through
  `4.6000`, `4.7000`, `4.8000`, `4.9000`, `5.0000`, `5.2000`, `5.4000`,
  `5.6000`, `5.8000`, `6.0000`, `6.5000`, `7.0000`, `8.0000`, `9.0000`, and
  `10.0000 MPa` without a bounded failure event in the saved ladder. A
  dedicated `4.4000 MPa` milestone audit repeats the same accepted seed in two
  independent pointwise confirm passes, stays `near_reproducible`, shows no
  branch-jump suspicion, and does not hit a short failure probe through
  `4.4100 MPa`, but still leaves `strict_reproducible = false`. New sparse
  confirms at `7.0000` and `10.0000 MPa` also keep the same accepted seed, show
  no branch-jump suspicion, and do not hit short first-failure probes through
  `10.0200 MPa`, but their repeat drift remains in the same smooth
  `2.85e-5..3.30e-5` max-relative-L2 band and still fails the current
  `near_reproducible` threshold even while remaining `M_s`-dominated and much
  smaller than the ordinary adjacent-step branch drift. Because the strict gate
  is still inherited from pilot 12 as `1e-7 / 1e-6`, the present
  `strict_reproducible = false` signal is now better read as an explicit open
  audit-policy / metric issue than as evidence that the branch has physically
  ended or jumped. The fast runner also no longer needs to inherit the old
  pilot-21 internal `0.0025 MPa` step cap: that bound remains part of the
  historical audited pilot artifact only, while the operational fast layer now
  uses its own runtime-controlled min/max/growth/shrink policy plus explicit
  milestone retention. A new exact-load comparison pilot then reuses the
  pilot-16 shallow simple-support comparator together with the same
  `arrays_nepol_sin(...)` mapping logic already used in pilot 17 at `4.0`,
  `7.0`, and `10.0 MPa`: the mismatch is already moderately visible at
  `4.0 MPa`, becomes clearly visible at `7.0 MPa`, stays clearly visible at
  `10.0 MPa`, and remains dominated by right-edge differences while still
  staying smooth through the available high-load range rather than producing a
  new barrier-localized qualitative jump. These newer `4.4000..10.0000 MPa`
  values are still operational continuation evidence rather than the current
  canonical audited ceiling, so the bottleneck remains on the numerical side
  and now more specifically on formulation / conditioning sensitivity plus
  confirm-policy sensitivity rather than on a simple raw-mesh limit or a
  verified physical end of branch. The active mixed-weak scans still use the
  reduced 5-state `F_min` background.
- Verification method:
  project-state analysis, numerical testbench.
- Verification boundary:
  not a theorem, only a current research strategy.
- Next action:
  keep the separate full 6-state simple-support background path, use the
  pilot-21 `u_z`-scaled continuation with auxiliary arc-like step adaptation as
  the current high-load workflow, split it operationally into a checkpointed
  fast runner plus a milestone confirm runner, keep the `4.3434 / 4.3440 MPa`
  pair explicit as the canonical old-path anchor/failure reference, keep the
  audited `4.3800 MPa` pilot-21 ceiling explicit even when newer fast-run
  checkpoints move higher, treat the strict-threshold policy itself as an open
  method question before promoting higher loads to audited status, use the fast
  runner's explicit runtime-controlled step limits rather than the historical
  pilot cap for future operational climbing, stop spending time on simple
  edge-mesh concentration alone, and use the pilot-16/pilot-17 BC-aligned
  shallow comparator plus the pilot-18 diagnosis before considering any
  reconnection to the mixed-weak scans.

### V-ST2. Stabilize the background before promoting `q_cr`

- ID: `V-ST2`
- Claim / Hypothesis:
  The correct project strategy is to stabilize the axisymmetric background
  before returning to final claims about `q_cr`.
- Type: `strategy`
- Source file(s):
  `docs/assumptions/assumptions.md` A14;
  `docs/theory/vyvod_uravneniy_updated17.md` section 3.1.
- Current status: `strategy only`
- What counts as verification:
  none in theorem form; this is an organizational consequence of the current
  dependency structure.
- Verification method:
  project-state analysis.
- Verification boundary:
  not a theorem, only a strategy-level rule for the next project step.
- Next action:
  keep separate from structural or numerical claims in reports.

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
- the use of `B_mix` as the current exploratory criterion.

Most urgent items to verify next:

- the bridge from the current testbench criterion to a fully consistent
  simple-support problem.
- the gap between the current reduced center ansatz and a fuller shell-center
  derivation.

Most valuable next proof pilots:

1. A pilot that isolates the current `B_mix` construction rule from the two
   central modes and checks its rows symbolically/numerically.
2. A pilot for the current prestress/load block boundary between what is already
   structurally fixed and what is still only a working formula package.
3. A proof-oriented check comparing the current reduced center ansatz against
   broader regular mixed extensions, if that boundary becomes verification
   critical.



