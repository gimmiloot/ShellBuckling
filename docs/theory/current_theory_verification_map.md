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
  `docs/journal/project_journal_updated14.md` sections 12.3-12.4;
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
  `docs/journal/project_journal_updated14.md` section 12.4.
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
- the use of raw `B_mix` as the current baseline criterion together with the
  clean `n = 4, 6, 7, 8` competition set as the live operational benchmark.

Most urgent items to verify next:

- the exact theorem-level operator or quadratic-form object whose degeneration
  should define criticality on the admissible clean `simple support`
  center-regular space;
- the reduction of that object from the full linearized mixed BVP to the actual
  reduced admissible coordinates used by the clean solver;
- the precise reason why `n = 6`, `n = 7`, and `n = 8` separate differently
  under the raw boundary-only reading and the lighter diagnostic pilots.

Most valuable next proof pilots:

1. A derivation/CAS pilot that isolates the full tangent mixed operator of the
   clean `simple support` problem and its reduction to admissible
   center-regular coordinates.
2. A proof-oriented pilot that compares candidate spectral, generalized, and
   quadratic-form criteria on that reduced object and records exactly where
   equivalence holds or fails.
3. A small numerical verification pilot that compares the new theorem-level
   criterion against the raw `B_mix` baseline on `n = 4, 6, 7, 8` without a new
   broad search.
