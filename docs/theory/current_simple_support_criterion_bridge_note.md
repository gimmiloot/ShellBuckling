# Criterion Bridge Note For Clean Full `simple support / подвижный шарнир`

This note stabilizes the repo-facing criterion language after the current local
Outcome-B stopping point. It is a status/interpretation memo, not a new theorem
about final physical criticality.

For the current rebuild/source-of-truth reading of the criterion story, pair
this note with
`docs/theory/current_simple_support_criterion_rebuild_note.md`, which now
records the explicit `R1 / R2 / R3` rebuild options and the current preferred
target.

## What Is Already Closed

- `A_ls` is best read as the global weak/KKT-selected family used by the current
  clean reduced architecture.
- `L_red` remains the main theorem-facing reduced object:
  `L_red,n(q) = [A_int,n(q); B_full,n(q)] V_adm,n(q)`.
- The selected leading trace plane is closed:
  `J_0 = C_center`, `J_0(A_ls) = im(D_amp)`.
- On the current checked higher-order local boundary, the strongest local
  theorem-facing object closes only as the quotient
  `im(D_rich,eta^corr) / span(g_mem)`.

## What Is Not Closed

- No final physical criticality theorem for the clean full
  `simple support / подвижный шарнир` problem is closed here.
- No theorem equating boundary-only degeneration with the full reduced-kernel
  question for `L_red` is closed here.
- No criterion-authoritative selection rule for the current reduced family is
  closed here.
- No nearby alternative selection rule is yet licensed here as a justified
  promoted baseline.
- No intrinsic higher-order local selector has been identified beyond the
  checked quotient boundary.
- No final physical candidate load/mode is determined here.

## How To Read The Objects

### `A_ls`

Theorem-facing role:
- the current repo-selected reduced family;
- the global weak/KKT-selected family, not the raw unrestricted local
  center-regular family.

Operational role:
- the family actually used by the live clean reduced search and by the current
  reduced-coordinate objects.

Do not read it as:
- the whole raw local regular family;
- a canonical or criterion-authoritative selected family;
- a statement that `A_full^th = A_ls` has already been proved.

### `L_red`

Theorem-facing role:
- the main reduced operator for the current nontrivial-kernel question.

Operational role:
- the clean reduced object that carries both interior and boundary information.

Do not read it as:
- already interchangeable with a boundary-only matrix;
- already equivalent to raw `sigma_min(B_mix) = 0`.

### `B_red`

Theorem-facing role:
- boundary descendant of the clean reduced family:
  `B_red,n(q) = B_full,n(q) V_adm,n(q)`.

Operational role:
- a useful boundary-only companion object on the same selected reduced family.

Do not read it as:
- a proved theorem-level substitute for the full stacked `L_red`.

### `B_mix`

Theorem-facing role:
- a boundary-only coordinate presentation on the selected reduced family:
  `B_mix,n(q) = B_red,n(q) G_amp,n(q)`.

Operational role:
- the current raw working / exploratory diagnostic object, including
  `sigma_min(B_mix)`.

Do not read it as:
- a closed final criterion for physical criticality;
- a silent replacement for the full reduced-kernel question on `L_red`.

## Selection-Authority Language

The current clean hierarchy should now be read in the order

```text
clean path / equations / BC meaning
    -> selected-family construction
    -> canonical rebasing
    -> boundary descendants
    -> stacked diagnostics
    -> criterion authority.
```

On that hierarchy:

- the clean path itself is not the present bottleneck; the audited boundary
  rows, center constraints, and rebasing identities stay internally
  consistent;
- the recipe-dependent layer is the selected-family rule that chooses one 2D
  span inside the constrained fiber before rebasing;
- canonical rebasing
  `V_adm = V_reg (C_amp V_reg)^(-1)` is canonical only after a span has already
  been chosen, so it does not force nearby chosen spans to coincide;
- harmless representative changes are mostly washed out by canonical rebasing,
  but nearby selection-rule changes are not;
- the current Tikhonov-selected family is therefore not
  criterion-authoritative;
- the apparently more stable truncated-SVD alternative is still cutoff-
  dependent enough that it should not yet be promoted;
- `B_red`, `B_mix`, and `rho_R2` must therefore be read only as
  reduced-family descendants / comparative diagnostics on a
  selection-layer-unresolved branch.

## Selector-Authority Requirements

A future promoted selector would need:

- structural/invariance requirements:
  compatibility with the fixed clean constraints and with the object hierarchy
  `A_ls -> L_red -> B_red -> B_mix`, together with invariance under harmless
  representative-choice changes;
- numerical robustness requirements:
  no material drift under small admissible `reg` changes, no qualitative
  dependence on arbitrary cutoff tuning, and no qualitative near-pair
  `n=7` / `n=8` reading change under nearby admissible selector choices;
- theorem-facing authority requirements:
  a theorem-facing reason why one chosen span is privileged inside the clean
  constrained fiber, not just a numerically convenient recipe;
- convenience-only properties that are not enough by themselves:
  small rebasing residuals, moderate `cond(G_amp)`, or one visually calm local
  window.

Current read of the existing pieces:

- the current Tikhonov selector fails the small-`reg` robustness and
  theorem-facing authority requirements;
- the current truncated-SVD alternative fails the cutoff-independence and
  theorem-facing authority requirements;
- canonical rebasing is a necessary post-selection normalization, not an
  authoritative selector by itself.

## Theorem-Facing Selector-Principle Candidates

- weak/KKT-selected global family:
  the most structurally compatible candidate with the current live architecture,
  but only if upgraded from the present numerical recipe to a theorem-facing
  weak/interior selection principle;
- local-to-global selected-family:
  also structurally compatible, but still blocked by the lack of a closed
  intrinsic local selected object with a canonical global lift;
- trace-plane-first:
  useful as an ingredient because the selected trace plane is closed, but not
  enough by itself because that trace data does not yet determine a unique
  privileged global family;
- variational/minimal-energy:
  conceptually possible, but currently unsupported because no canonical
  selector-energy/coercivity principle has yet been derived on this branch;
- no justified selector yet:
  this remains the correct current fallback position until one theorem-facing
  selector principle is actually derived and checked.

## Weak/KKT Route In Current Repo Language

- current Tikhonov surrogate:
  solve
  `min ||A_int c||^2 + reg ||c||^2` subject to `C_center c = d_j`
  for the two amplitude directions, then normalize, orthogonalize, and only
  afterward canonically rebase;
- what is genuinely weak/KKT-like there:
  the selector is trying to privilege representatives by an interior weak
  residual criterion, not by boundary data alone;
- what is still only recipe-level:
  the Euclidean `reg ||c||^2` term, the chosen `reg`, the separate right-hand-
  side solve, and the later normalization / orthogonalization choices;
- target theorem-facing upgrade:
  a canonical weak/interior selected-representative map that privileges one 2D
  span without relying on those arbitrary tuning choices;
- exact current missing step:
  no theorem-facing weak/KKT selector principle has yet been proved that turns
  the present surrogate into a justified privileged selected family.

## Weak/KKT Readiness Verdict

- candidate theorem target:
  a selected-representative map from amplitude data / selected trace data to a
  privileged 2D family inside a theorem-facing clean constrained class;
- what is already sharp enough:
  the code-level constrained recipe, the selected trace/amplitude data, and the
  reduced-object hierarchy;
- what is still underdetermined one layer lower:
  the exact theorem-facing constrained class and the canonical weak/interior
  optimality statement;
- readiness verdict:
  `B. almost ready, but one or two lower-level clarifications should be done first`;
- those prerequisites are exactly:
  close the theorem-facing constrained class, then specify the canonical
  weak/interior selector principle on it.

## Clarifying `A_con^th`

- what it is not:
  the intended theorem-facing codomain is not the raw coefficient space
  `X_trial`, not the code-level center-regular slice `W_reg`, and not the exact
  current numerical family `A_repo = A_ls`;
- primary natural candidate:
  the selected-trace constrained slice of the intended full theorem-facing
  admissible class, meaning the clean global admissible objects whose selected
  leading trace lies in `im(D_amp)` or, fiberwise, equals `D_amp a`;
- secondary plausible candidate:
  a theorem-facing selected overclass closer to `A_ls`, with the current
  structural placeholder `A_sel^{th,cand}` the nearest named candidate on the
  repo boundary;
- why the local-to-global route is not yet enough to fix it:
  the selected trace plane is closed, but there is still no closed intrinsic
  local selected object with a canonical global lift;
- codomain verdict:
  `B. A_con^th` is narrowed to a short list of 2 plausible candidates rather
  than fixed sharply;
- exact remaining block:
  the ambient full admissible class is not yet independently packaged sharply
  enough, and the selected-overclass route is not yet closed intrinsically
  enough to settle the codomain uniquely.

## Preferred Codomain Route For The Weak/KKT Target

- preferred route:
  the selected-trace constrained slice of the intended full theorem-facing
  admissible class;
- why it wins the current comparison:
  it is the closest theorem-facing analogue of the live constrained-fiber plus
  weak-selection geometry, and it keeps the selected 2D family as the image of
  the theorem rather than part of the codomain definition;
- why the selected-overclass route stays secondary:
  it remains a live neighboring theorem program, but it still depends on a
  stronger unresolved local selected-object / canonical-lift story;
- exact next bottleneck after this preference:
  sharpen the ambient full admissible class enough to define the selected-trace
  constrained slice cleanly, then formulate the canonical weak/interior
  selector principle on that codomain.

## Ambient `A_full^th` Read

- preferred current meaning:
  the full clean admissible / center-regular tangent class of the continuous
  mixed problem, treated as the ambient theorem-facing class above `A_ls` and
  above the selected trace plane;
- what it is not:
  not `X_trial`, not `W_reg`, not `A_repo = A_ls`, and not `im(D_amp)` alone;
- why it is still not closed sharply:
  the repo still lacks a finished continuum/local packaging of that full class
  with higher-order formal continuation/completeness and theorem-facing trace
  regularity strong enough to define the selected-trace slice cleanly;
- ambient-class verdict:
  `B. A_full^th` is narrowed substantially but still not sharp enough.

## Class-Plus-Trace Packaging Read

- paired theorem-facing package:
  `A_full^th` is the ambient continuum/local clean admissible class and `J_0`
  is the finite leading-center jet that should live on that class;
- what is already exact:
  on the weighted-ansatz / selected-family boundary, `J_0 = C_center`,
  `J_0(A_ls) = im(D_amp)`, and `J_0|_{A_ls}` is exact;
- what still blocks proof-readiness:
  the branch still needs one continuum/local trace-regularity upgrade carrying
  that same finite trace cleanly to all of `A_full^th`;
- readiness verdict:
  `B. much sharper, but one explicit continuum/local trace-regularity gap still remains.`

## `J_0` Extension Gap

- exact current closure:
  on the weighted-ansatz / selected-family boundary,
  `J_0 = C_center`, `J_0(A_ls) = im(D_amp)`, and `J_0|_{A_ls}` is exact;
- intended ambient meaning:
  on `A_full^th`, `J_0` should be the same finite leading-center jet, keeping
  the two amplitudes and two regularity-defect rows in one 4D trace object;
- exact remaining theorem task:
  prove the theorem-facing extension of that finite trace from the current
  ansatz boundary to all of `A_full^th`, together with the local
  continuation/completeness needed for the slice `J_0(c) in im(D_amp)` to make
  sense;
- verdict:
  `B. the J_0 gap is narrowed to one precise local/trace theorem task.`

## Sharp `J_0` Theorem Task

- target:
  define a theorem-facing finite leading-center jet
  `J_0^th : A_full^th -> R^4` with the same four coordinates already used by
  the exact `C_center` trace;
- hypotheses:
  ambient admissible / center-regular objects in `A_full^th` must admit the
  current near-center scaling orders and enough local
  continuation/completeness that those four leading-center quantities exist
  uniquely;
- conclusion:
  `J_0^th` is well-defined on all of `A_full^th`, agrees with `C_center` on the
  weighted-trial overlap, and makes the slice `J_0(c) in im(D_amp)` meaningful;
- sharpness verdict:
  `A. the remaining J_0 task is now sharp enough for a direct theorem attempt.`

## Direct Proof-Attempt Outcome For `J_0`

- theorem-attempt result:
  not fully proved at the current repo level;
- exact first blocking lemma:
  every `c in A_full^th` should admit a unique current-normalized leading-center
  quadruple `(U0, N0, P0, Y0)` compatible with the continuous mixed equations
  and agreeing with `C_center` on the weighted-trial overlap;
- why that is the first block:
  without this ambient finite-jet extraction result, `J_0^th` is not yet
  defined on all of `A_full^th`, so the selected-trace slice on the preferred
  codomain is not yet theorem-facingly available;
- verdict:
  `B. the direct proof attempt reduces the theorem to one smaller explicit
  local/trace lemma task.`

## Direct Theorem-Attempt Outcome For The Ambient Finite-Jet Lemma

- theorem-attempt result:
  not fully proved at the current repo level;
- what already closes once the coefficients exist:
  overlap agreement with `C_center`, leading mixed-equation compatibility, and
  uniqueness inside the current normalization;
- exact first unresolved sublemma:
  every `c in A_full^th` should admit the four current-normalized leading
  coefficients `(U0, N0, P0, Y0)` for `(u_s, u_n, varphi, psi)` in the current
  near-center scaling class;
- verdict:
  `B. the ambient finite-jet lemma is reduced to one smaller explicit
  coefficient-extraction sublemma.`

## Direct Theorem-Attempt Outcome For The Ambient Leading-Coefficient Sublemma

- theorem-attempt result:
  not fully proved at the current repo level;
- what already closes once the one-term asymptotics exist:
  uniqueness in the chosen normalization, overlap agreement with `C_center`,
  and later use of the leading mixed-equation block;
- exact first unresolved sub-sublemma:
  every `c in A_full^th` should admit one-term current-normalized asymptotics
  for `(u_s, u_n, varphi, psi)` in the present scaling orders;
- verdict:
  `B. the leading-coefficient sublemma is reduced to one smaller explicit
  asymptotic-existence sub-sublemma.`

## Direct Theorem-Attempt Outcome For The Ambient One-Term Asymptotic Sub-Sublemma

- theorem-attempt result:
  not fully proved at the current repo level;
- what already closes once normalized limits exist:
  one-term asymptotics themselves, coefficient extraction, uniqueness in the
  chosen normalization, and overlap agreement with `C_center`;
- exact first unresolved sub-sub-sublemma:
  every `c in A_full^th` should admit finite normalized channel limits
  `u_s/x^n`, `u_n/x^n`, `varphi/x^(n-1)`, `psi/x^(n-1)` in the present trace
  convention;
- verdict:
  `B. the asymptotic-existence sub-sublemma is reduced to one smaller explicit
  normalized-limit sub-sub-sublemma.`

## Direct Theorem-Attempt Outcome For The Ambient Normalized-Limit Sub-Sub-Sublemma

- theorem-attempt result:
  not fully proved at the current repo level;
- what is already closed:
  the current scaling analysis already gives bounded normalized channels
  `u_s/x^n`, `u_n/x^n`, `varphi/x^(n-1)`, `psi/x^(n-1)`;
- what remains the first unresolved point:
  every `c in A_full^th` should satisfy convergence of those already-bounded
  renormalized channels as `x -> 0`, equivalently continuous extension to the
  center in the present trace convention;
- verdict:
  `B. the normalized-limit sub-sub-sublemma is reduced to one smaller explicit
  normalized-quotient convergence sub-sub-sub-sublemma.`

## Direct Theorem-Attempt Outcome For The Ambient Normalized-Quotient Convergence Sub-Sub-Sub-Sublemma

- theorem-attempt result:
  not fully proved at the current repo level;
- route comparison:
  derivative/integrability and compactness/continuity do not close on the
  present repo material, while the regular-singular route gets furthest;
- exact first unresolved point:
  every `c in A_full^th` should satisfy a theorem-facing renormalized local
  regular-singular continuation statement for
  `[x^(-n) u_s, x^(-n) u_n, x^(1-n) varphi, x^(1-n) psi]` strong enough that
  boundedness forces convergence as `x -> 0`;
- verdict:
  `B. the normalized-quotient convergence sub-sub-sub-sublemma is reduced to
  one smaller explicit renormalized regular-singular limit sub-sub-sub-sub-sublemma.`

## Direct Theorem-Attempt Outcome For The Ambient Renormalized Regular-Singular Limit Sub-Sub-Sub-Sub-Sublemma

- theorem-attempt result:
  not fully proved at the current repo level;
- exact regular-singular route used:
  the current richer-jet / recurrence route
  `Xi_rich^(1,eta) -> Xi_rich^(1+,eta) -> Pi_eta_to_J0`;
- exact first unresolved point:
  every `c in A_full^th` should admit an ambient punctured-neighborhood
  renormalized local-system / jet-lift statement extending
  `[x^(-n) u_s, x^(-n) u_n, x^(1-n) varphi, x^(1-n) psi]`
  to a closed regular-singular local state whose leading structure matches the
  checked recurrence model;
- verdict:
  `B. the renormalized regular-singular limit sub-sub-sub-sub-sublemma is
  reduced to one smaller explicit ambient renormalized local-system / jet-lift
  sub-sub-sub-sub-sub-sublemma.`

## Direct Theorem-Attempt Outcome For The Ambient Punctured-Neighborhood Renormalized Local-System / Jet-Lift Lemma

- theorem-attempt result:
  not fully proved at the current repo level;
- exact first unresolved point:
  every `c in A_full^th` should admit a punctured-neighborhood richer-jet lift
  realizing the first post-leading variables of `Xi_rich^(1,eta)` and, when
  needed, `Xi_rich^(1+,eta)`, compatibly with
  `[x^(-n) u_s, x^(-n) u_n, x^(1-n) varphi, x^(1-n) psi]`
  and the canonical projection `Pi_eta_to_J0`;
- verdict:
  `B. the ambient local-system / jet-lift lemma is reduced to one smaller
  explicit punctured-neighborhood richer-jet lift-existence lemma.`

## How To Read Candidate Labels

- `supported candidate`
  the strongest current clean candidate with some robustness/support on the
  active criterion workflow, but not a final physical critical mode.
- `unstable rival`
  a serious competitor that can look stronger in some windows or surrogate
  readings, but remains too sensitive or insufficiently stabilized to replace
  the current supported reading.
- `reserve dip`
  a sharp raw dip that is not yet robust enough to promote.
- `control mode`
  a retained comparison mode used to keep the competition picture calibrated,
  not a leading supported candidate.

Current selected-family competition language:
- `n=7` and `n=8` form a near-degenerate selected-family pair on the present
  clean branch;
- `rho_R2` on the current selected family often leans mildly toward `n=8`, but
  that reading is not stable enough to resolve the pair under nearby
  discretization or selection-rule changes;
- `n=6` stays below both in the checked stacked reading and is kept only as a
  lower comparison control, not as the active unresolved pair.

Current selection-authority / `R2` language:
- `rho_R2` is a comparative stacked diagnostic on a chosen selected family, not
  a promoted main working criterion;
- pair-resolution metrics do not resolve the near-degenerate `n=7` / `n=8`
  pair on one fixed selected family;
- selected-family sensitivity and selection-rule audits show that the current
  Tikhonov-selected family is too recipe-sensitive for criterion authority;
- the seemingly stable truncated-SVD alternative is still cutoff-dependent
  enough that it should not yet be promoted;
- the current bottleneck is therefore the unresolved authority of the
  selected-family rule itself, not only the ranking of `n=7` against `n=8`.
- any future promoted criterion on this branch now needs a selector satisfying
  the explicit selector-authority requirements above.
- the next theorem/status choice is therefore whether to develop the weak/KKT
  route, the local-to-global route, some future genuine variational route, or
  to remain on the conservative `no justified selector yet` language.

None of these labels implies a final physical critical-load claim.

## Project Strategy After Outcome B

- The local theorem-facing branch is frozen for now at Outcome B on the current
  checked boundary.
- This is a project-strategy stopping point, not a mathematical impossibility
  claim.
- The next active path is selection-authority clarification above the current
  criterion story, not a new winner search.
- The current source-of-truth rebuild reading is recorded separately in
  `docs/theory/current_simple_support_criterion_rebuild_note.md`.
- Do not reopen the same checked local branch unless a genuinely new
  theorem-facing idea appears.
- The next bridge question is how the checked local quotient result should be
  read together with `A_ls`, `L_red`, `B_red`, and `B_mix` together with an
  explicit selection-authority question, without overclaiming final physical
  criticality.
- The current theorem program above that frozen boundary is recorded in
  `docs/theory/current_simple_support_theorem_roadmap.md`.
