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
  and the canonical projection `Pi_eta_to_J0`, and returning on the
  weighted-trial overlap to the exact current ansatz-boundary trace
  `J_0 = C_center`;
- verdict:
  `B. the ambient local-system / jet-lift lemma is reduced to one smaller
  explicit punctured-neighborhood richer-jet lift-existence lemma.`

## Cleaned Next Local Target

- cleaned proof-line implication:
  `richer-jet lift + regular-singular convergence + overlap compatibility
  => J_0^th well-defined`;
- what overlap compatibility means here:
  agreement with the exact ansatz-boundary trace `J_0 = C_center` and
  compatibility with the canonical return map `Pi_eta_to_J0` on the weighted-
  trial overlap;
- next active theorem target:
  prove the punctured-neighborhood richer-jet lift-existence lemma already in
  that cleaned form, so overlap compatibility is part of the setup rather than
  an afterthought added after the lift and convergence steps.

## Direct Theorem-Attempt Outcome For The Cleaned Richer-Jet Lift-Existence Lemma

- theorem-attempt result:
  not fully proved at the current repo level;
- what becomes formal once the current richer chart exists:
  extension of `W_c`,
  canonical return through `Pi_eta_to_J0`,
  and the overlap-compatibility clause with `J_0 = C_center`;
- exact first unresolved point:
  every `c in A_full^th` should admit punctured-neighborhood first post-leading
  chart data realizing `Xi_rich^(1,eta)` and, when needed, `Xi_rich^(1+,eta)`,
  so that those already-formal projection and overlap clauses can even be
  stated theorem-facingly;
- theorem-facing role of the Step-1 blocker:
  keep punctured-neighborhood local-representative existence as a separate
  local regularity / continuation lemma for members of `A_full^th`, rather
  than redefining `A_full^th` to include it by fiat or promoting it to a
  standing extra assumption;
- direct theorem-attempt outcome for that isolated Step-1 target:
  not fully proved at the current repo level, but reduced further to one
  smaller explicit ambient punctured-local-representative existence lemma,
  because the scaling-class read of the four channels and the checked richer-
  chart language are no longer the first blockers once such a representative
  exists;
- theorem-facing representation read for the ambient-to-local blocker:
  keep `A_full^th` as an ambient class, but state the local realization step as
  an existential representation / witness relation between `c in A_full^th`
  and a punctured near-center clean mixed germ, rather than as an identity of
  `A_full^th` with germ classes or as a canonical realization map;
- exact predicate style now preferred for that relation:
  use a hybrid witness predicate `Rep_loc^{n,q}(c,G)`, requiring that `G` be a
  genuine punctured near-center clean mixed germ in the current mixed
  variables, that it serve as the theorem-facing local witness for `c`, and
  that on the exact weighted-ansatz / selected-family boundary this witness
  relation normalize to agreement with the exact finite trace
  `J_0 = C_center`;
- next local theorem target in that language:
  for every `c in A_full^th,n(q)`, there exist `\delta > 0` and a punctured
  near-center clean mixed germ `G` on `(0,\delta)` such that
  `Rep_loc^{n,q}(c,G)`;
- direct theorem-attempt outcome in that language:
  still open at the current repo level;
  once the hybrid predicate `Rep_loc^{n,q}(c,G)` is fixed, the first
  unresolved step is existence of a punctured near-center clean mixed germ
  witness itself for arbitrary ambient `c in A_full^th,n(q)`;
- source-principle verdict behind that blocker:
  the next theorem should be a separate ambient punctured-neighborhood local
  clean mixed continuation theorem for members of `A_full^th`, from which the
  witness-germ existence statement follows by taking the punctured local germ;
  a full local solution-family theorem is stronger than currently needed, and a
  weak-to-local realization theorem is not the best-supported route on the
  present repo boundary;
- direct theorem-attempt outcome for that source theorem:
  still open at the current repo level;
  once such a punctured near-center local continuation exists, the current
  clean mixed-state, local-equation, and scaling-order clauses are no longer
  the first blockers, so the first unresolved smaller lemma is local
  continuation existence itself for arbitrary ambient `c in A_full^th,n(q)`;
- source-mechanism verdict behind that smaller lemma:
  the next proof should be a direct continuation theorem from the ambient clean
  admissible / center-regular compatibility package itself;
  the repo does not support reading `A_full^th` as already locally realized on
  punctured intervals, does not support a weak-to-local extraction theorem as
  the preferred route here, and does not currently identify a further missing
  ambient premise that must be added before the theorem can start;
- Assumption LC (working physical assumption):
  for fixed `(n,q)`, every `c in A_full^th,n(q)` admits `\delta > 0` and a
  punctured near-center clean mixed continuation on `(0,\delta)` in the
  current mixed variables, satisfying the current local clean mixed equations
  and the intended near-center scaling orders there;
- how to read it:
  this is not proved theorem-facingly on the current branch and does not close
  the strict ambient-to-local theorem line;
  it is introduced only to stop repeated repackaging of the same closure
  barrier, so later witness-germ, chart-realization, richer-jet, and local
  `J_0` steps should now be read conditionally under Assumption LC unless the
  closure theorem is proved independently;
- conditional witness-germ consequence under LC:
  the existential witness-germ lemma is then closed conditionally on the
  current branch reading:
  Assumption LC provides a punctured near-center clean mixed continuation,
  taking its punctured local germ gives `G`, and the current `Rep_loc^{n,q}`
  schema reads that germ as the theorem-facing local witness for `c`;
  this conditional closure does not discharge LC and does not alter the still-
  open strict ambient-to-local theorem line;
- conditional chart-realization consequence under LC:
  the chart-realization lemma is not yet fully closed even under LC, but it is
  reduced:
  Step 1 is now supplied conditionally by LC, while compatibility with
  `Pi_eta_to_J0` and overlap return to `J_0 = C_center` are already formal once
  the richer chart exists;
  the first remaining conditional blocker is realization of
  `Xi_rich^(1,eta)` and, when needed, `Xi_rich^(1+,eta)` as actual punctured
  local chart data on the witness germ;
  more sharply, the remaining conditional blocker is recurrence-to-local
  realization on that witness germ: promotion of the checked first post-
  leading recurrence variables to actual punctured local chart data;
  for the reduced first post-leading slots `U1, N1, P1, Y1` alone, the first
  exact reduced blocker is one extra near-center asymptotic order for the
  renormalized witness-germ channels, strong enough to define those four
  coefficients as actual punctured local quantities;
  once that reduced extraction statement is available in the weaker asymptotic
  form `f(x) = f0 + x f1 + o(x)` or equivalent, recurrence-side agreement is no
  longer the first blocker;
  more sharply still, once the reduced renormalized remainder system is fixed,
  the first exact reduced blocker is first post-leading control of the
  auxiliary renormalized source remainders `Q_s` and `Q_\varphi`;
  after that, remainder control for `(R_s, R_n, R_\varphi)` is triangular and
  `R_\psi` follows algebraically, so coefficient extraction / recurrence-side
  agreement is no longer the first blocker;
  but a structural diagnostic shows that the reduced four-channel problem is
  not actually closed as written:
  `Q_s` depends on the membrane auxiliary block through `T_s` and `v`, and
  `Q_\varphi` depends on the bending/shear auxiliary block through `M_s` and
  its companion local propagation;
  so the next theorem-facing target should lift the reduced line back to the
  smallest fuller local mixed block carrying
  `(u_s, u_n, v, \varphi, \psi, T_s, Q_s, M_s)` in renormalized form;
  a further structural closure check then shows that `H^{ren}` and
  `\chi^{ren}` themselves do not force new local unknowns, because they can be
  eliminated using the existing flexural equations and algebraic identities;
  but the proposed 8-channel fuller block is still not a genuinely closed
  first-order system, because the membrane side still depends on an explicit
  `S^{ren}`-level variable;
  so the true minimal first-order repair is the 9-channel block
  `(U,N,V,P,Y,T,Q,M,S^{ren})`;
  a direct theorem attempt on that 9-channel block still does not close the
  conditional first post-leading asymptotic theorem, but it sharpens the first
  blocker further:
  once the 9-channel block is written as a first-order renormalized local
  system with preserved compatibility, the leading layer and the formal first
  post-leading coefficient system are no longer the first blockers on the
  current branch reading;
  the first exact analytic blocker is regular-singular remainder control on the
  actual punctured local witness germ, strong enough to conclude
  `f(x) = f0 + x f1 + o(x)` for each of the 9 channels;
  a further remainder-derivation check sharpens this again:
  for the actual witness-germ system, `U`, `N`, and derived `Y` reduce to
  `O(x)` under the current background expansions and LC scaling orders, while
  `V`, `P`, and `Q` are only plausibly `O(x)` because their exact coefficient
  corrections / elimination formulas are not yet packaged sharply enough;
  the first exact obstruction sits in the `T`, `M`, and `S^{ren}` rows, where
  the richer-local C3c audit still leaves low-order curvature-coupled terms not
  reduced to `O(x)`;
  so the remainder problem is not yet blocked first by resonance, but by a
  mismatch between the actual local witness-germ equations and the currently
  chosen principal operator `A_0` in those rows;
  a sharper principal-operator correction diagnostic then separates those rows:
  the `T` row really does need a principal correction from
  `-(s_0 c_0 / r_0^2) M_\theta`, and the `S^{ren}` row really does need a
  principal correction from `\kappa_{\theta 0}\chi`;
  but the `M` row low-order structure is already represented by the current
  principal operator, so no extra principal correction is presently forced
  there;
  the corrected principal operator should therefore modify the `T` and
  `S^{ren}` rows, not enlarge the state and not change the principal `M` row;
  after that correction, no row is currently known to leave a non-`O(x)`
  remainder;
  the supported `O(x)` rows are `U`, `N`, `V`, and derived `Y`, while the
  `P`, `T`, `Q`, `M`, and `S^{ren}` rows remain only plausibly `O(x)` because
  their corrected remainders still depend on theorem-facing control of the
  actual-to-principal elimination errors for `M_\theta^{ren}`, `H^{ren}`, and
  `\chi^{ren}`;
  so the next blocker is no longer another principal-operator correction, but
  the exact theorem-facing `O(x)` control of those elimination errors on the
  punctured witness germ;
  a direct elimination-error derivation then sharpens this again:
  `\Delta H^{ren}` is no longer a first blocker, because on the current branch
  reading it reduces explicitly to
  `[\;n(\lambda_{s0}-\lambda_c) P - n x \kappa_{s0} U\;] / C_{tw}` once the
  actual `Y` row is read through the actual `N` row and preserved
  compatibility, so it is supported as `O(x)`;
  `\Delta \chi^{ren}` likewise is no longer an independent first blocker,
  because after substituting that `\Delta H^{ren}` formula together with the
  actual `P`, `Y`, and `U` rows it reduces to
  `n \Delta M_\theta^{ren} + O(x)` on the current branch reading;
  so the exact first blocker after the corrected-principal split is now the
  theorem-facing `O(x)` control of `\Delta M_\theta^{ren}` itself, which
  remains only plausible at the current repo level because the exact actual
  coefficient package in the corrected circumferential / twist-shear block is
  still not article-level fixed sharply enough;
  more sharply, the current branch reading already identifies the exact needed
  coefficient form:
  `M_\theta^{ren,0} = \nu M + (P + nY)/\Lambda`, while the actual
  circumferential / twist-shear package can now be reconstructed more
  explicitly as
  `M_\theta^{ren,act}
   = \nu M
   + [c_0 / (\Lambda \lambda_{\theta 0})] P
   + [n / (\Lambda \lambda_{\theta 0})] Y
   - [s_0 c_0 / (\Lambda \lambda_{\theta 0}^2)] U
   - [s_0^2 / (\Lambda \lambda_{\theta 0}^2)] N`,
  with the `U`-term already harmless because its coefficient is `O(x)`;
  hence
  `\Delta M_\theta^{ren}
   = (a_P(x) - 1/\Lambda) P + (a_Y(x) - n/\Lambda) Y + a_N(x) N`,
  with
  `a_P(x) = c_0 / (\Lambda \lambda_{\theta 0})`,
  `a_Y(x) = n / (\Lambda \lambda_{\theta 0})`,
  `a_N(x) = - s_0^2 / (\Lambda \lambda_{\theta 0}^2)`;
  here `a_N(x)` is already supported as `O(x^2)`, so the exact first missing
  ingredient is now narrower:
  theorem-facing near-center fixation of the `\lambda_{\theta 0}`
  normalization inside the `P`- and `Y`-coefficients, sharp enough to justify
  `c_0/\lambda_{\theta 0} - 1 = O(x)` and `1/\lambda_{\theta 0} - 1 = O(x)` in
  the same local normalization as the corrected-principal model;
  a further normalization-consistency check then shows that current repo
  material still mixes two distinct normalizations at exactly this point:
  the frozen principal-center line uses `\lambda_{\theta 0} \to 1`, the richer
  intrinsic center expansion uses `\lambda_{\theta 0} = \lambda_c + O(x^2)`,
  and the current clean theorem-facing trace convention only fixes
  `\lambda_{\theta 0}(x_0) = 1` at the selected `x_0`-trace layer;
  therefore the repo does not yet theorem-facingly decide whether the
  principal/model `P`- and `Y`-coefficients in `M_\theta^{ren}` should be
  compared against `1/\Lambda, n/\Lambda` or against
  `1/(\Lambda \lambda_c), n/(\Lambda \lambda_c)`;
  the normalization map is now:
  `A. intrinsic center normalization`:
  punctured `x \to 0` local geometry with
  `c_0 = 1 + O(x^2)` and `\lambda_{\theta 0} = \lambda_c + O(x^2)`;
  `B. frozen principal-center normalization`:
  helper/principal simplification with
  `c_0 \to 1` and `\lambda_{\theta 0} \to 1`;
  `C. selected x_0`-trace normalization:
  criterion/trace convention with `\lambda_{\theta 0}(x_0) = 1`;
  the `x_0`-trace normalization belongs to the criterion/trace layer and must
  not be silently substituted for the local punctured-center normalization in
  the theorem-facing principal `M_\theta^{ren}` comparison unless an explicit
  bridge lemma is stated;
  the current theorem-facing decision for the local punctured `x \to 0` line is
  therefore:
  use the intrinsic punctured-center normalization as the master local
  normalization, because it is the one naturally attached to the witness germ
  and to the active renormalized circumferential / twist-shear reconstruction;
  do not read the frozen helper normalization as the final local theorem-facing
  choice, and do not read the selected `x_0`-trace normalization as governing
  the local principal `P`- and `Y`-coefficients;
  accordingly, the candidate local principal/model package is
  `M_\theta^{ren,0,loc} = \nu M + (P + nY)/(\Lambda \lambda_c)`;
  but the criterion-facing selected-family comparison still lives on the
  separate `x_0`-trace layer, so an explicit theorem-to-criterion bridge lemma
  is required later and is not yet available on the current branch reading;
  after that intrinsic-local choice, the `M_\theta^{ren}` comparison itself is
  no longer the first unresolved coefficient block:
  one has
  `\Delta M_\theta^{ren}
   = [\,(c_0/\lambda_{\theta 0}) - (1/\lambda_c)\,] P / \Lambda
   + n[\,(1/\lambda_{\theta 0}) - (1/\lambda_c)\,] Y / \Lambda
   - [s_0 c_0 / (\Lambda \lambda_{\theta 0}^2)] U
   - [s_0^2 / (\Lambda \lambda_{\theta 0}^2)] N`,
  and the current intrinsic center expansions now support
  `c_0/\lambda_{\theta 0} - 1/\lambda_c = O(x^2)`,
  `1/\lambda_{\theta 0} - 1/\lambda_c = O(x^2)`,
  the `U`-coefficient as `O(x)`, and the `N`-coefficient as `O(x^2)`;
  since the renormalized channels are bounded in the LC scaling class, this
  supports `\Delta M_\theta^{ren} = O(x)` on the intrinsic local line;
  hence the earlier elimination-error obstruction is no longer first on the
  corrected 9-channel system, and the next blocker becomes the regular-
  singular first-correction argument itself;
  the earlier normalization-consistency issue now survives only as a separate
  theorem-to-criterion bridge question between the intrinsic punctured-center
  local line and the selected `x_0`-trace layer, rather than as the current
  blocker for the local `M_\theta^{ren}` coefficient comparison itself;
- direct theorem-attempt read after the intrinsic-local correction:
  on the current branch reading the corrected intrinsic-local system may now be
  read as
  `x Z'(x) = A_{0,loc}^{corr} Z(x) + R_{loc}(x)`
  with preserved compatibility `Y + nN = 0` and corrected elimination errors
  already reduced to `O(x)`;
  so the line is no longer blocked first by source packaging, principal-model
  choice, or the `M_\theta^{ren}` comparison;
  the first exact blocker is now the theorem-facing regular-singular first-
  correction argument itself;
  more sharply, the proof no longer breaks first at leading-state extraction,
  the formal first post-leading coefficient system, or the corrected
  intrinsic-local `O(x)` remainder split;
  it breaks first at the missing no-log spectral lemma for the bounded
  compatibility-preserving sector of `A_{0,loc}^{corr}`, i.e. the missing
  theorem-facing statement that every bounded witness-germ solution satisfying
  `Y + nN = 0` has the affine first correction
  `Z(x) = Z_0 + x Z_1 + o(x)` with no logarithmic or other additional bounded
  first-correction terms;
  a narrower spectral audit now indicates that this is no longer blocked first
  by a visible Jordan-type degeneracy on the checked principal model:
  once the preserved compatibility relation `Y + nN = 0` is imposed, the
  first checked post-leading layer leaves exactly one genuine membrane
  `x`-direction `(U1, V1, T1) = T1 (\alpha, \beta, 1)`, the flexural
  coefficients are killed under the same nonresonance condition, and after
  admitting that membrane mode the next checked layer closes uniquely to zero;
  so the checked spectral picture does not currently support a bounded
  logarithmic first-correction mode in the compatibility-preserving sector,
  and the next blocker is the theorem-facing bounded-solution /
  variation-of-constants step rather than further spectral repair;
  a narrower proof pass now makes that remaining step more explicit:
  for fixed `(n,q)` under Assumption LC, if the bounded corrected intrinsic-
  local witness-germ state
  `Z = (U,N,V,P,Y,T,Q,M,S^{ren})` satisfies
  `x Z'(x) = A_{0,loc}^{corr} Z(x) + x b(x)` with bounded `b` and preserved
  compatibility `Y + nN = 0`, then the exact operator entering the regular-
  singular argument is the restriction of the frozen corrected intrinsic-local
  9-channel principal matrix to that compatibility-preserving sector;
  the attempted proof would close once one had a theorem-facing bounded-sector
  decomposition into the leading kernel, the genuine membrane `x`-mode, and a
  remainder sector with spectral gap `\Re \lambda > 1`, because then
  variation-of-constants would give a leading limit `Z_0`, bounded
  `W = (Z - Z_0)/x`, and hence
  `Z(x) = Z_0 + x Z_1 + o(x)`;
  the first exact missing ingredient is therefore no longer another spectral
  repair, but the compatibility-preserving projector / bounded-solution lemma
  itself: a theorem-facing proof that boundedness already implies
  `Z - Z_0 = O(x)` and rules out hidden bounded non-affine corrections on that
  sector;
  a narrower matrix/projector read sharpens this once more:
  the exact compatibility-preserving space is
  `E_{comp} = {Z : Y + nN = 0}`,
  equivalently the 8-dimensional reduced coordinate space with `Y = -nN`, and
  it is invariant because the principal `N`/`Y` rows give
  `x(Y+nN)' = -n(Y+nN)`;
  on the current branch reading the selected leading trace plane is the
  current candidate `0`-eigenspace block and the checked membrane `x`-mode is
  the current candidate `1`-eigenspace block, with no visible checked Jordan
  continuation of that membrane mode at the next layer;
  but the repo still lacks the theorem-facing restricted-spectrum statement for
  `A_{comp} := A_{0,loc}^{corr}|_{E_{comp}}` proving that the whole bounded
  sector is exactly
  `E_0 \oplus E_1 \oplus E_{>1}`
  with no extra bounded spectrum `0 < \Re \lambda < 1`;
  a narrower explicit-matrix packaging pass now closes that row-level blocker:
  using
  `s_0 = Kx + O(x^3)`,
  `c_0 = 1 + O(x^2)`,
  `r_0 = \lambda_c x + O(x^3)`,
  the structural principal source
  `-(s_0 c_0 / r_0^2) M_\theta`
  becomes, after moving it from the residual side to the evolution equation
  and then performing intrinsic-local renormalization, the constant corrected
  term
  `+(K/\lambda_c^2) M_\theta^{ren,0,loc}` in the `T` row, so
  `c_T^{loc} = K/\lambda_c^2`;
  together with the already explicit compatibility-slice packages
  `T_{\theta,comp}^{ren}`,
  `M_{\theta,comp}^{ren,0,loc}`,
  `H_{comp}^{ren,0,loc}`,
  and `\chi_{comp}^{ren,0,loc}`, this fixes the full restricted 8x8 constant
  matrix `A_{comp}` theorem-facingly on the present branch reading;
  the exact next blocker is therefore no longer matrix packaging, but the
  actual restricted spectral-gap / direct-sum audit for `A_{comp}` itself:
  identify the `0`- and `1`-blocks theorem-facingly, exclude Jordan defects at
  `0` and `1`, and exclude any spectrum with `0 < \Re \lambda < 1`;
  a narrower spectral audit now sharpens this further:
  after reordering the coordinates to `(N,P,M,Q,U,V,T,S^{ren})`, the explicit
  matrix `A_{comp}` is block lower triangular with diagonal blocks
  `G_{flex}`, the scalar `-(n-1)`, and `B_{mem}`;
  the membrane block is
  \[
  B_{mem}
  =
  \begin{pmatrix}
  -(n+\nu) & -n\nu & 1-\nu^2 & 0 \\
  n & -(n-1) & 0 & 2(1+\nu) \\
  1 & n & \nu-n & -n \\
  n & n^2 & n\nu & -(n+1)
  \end{pmatrix},
  \]
  and a direct determinant computation gives
  `\det(B_{mem} - \lambda I)
   = (\lambda-1)(\lambda+1)(\lambda+2n-1)(\lambda+2n+1)`;
  hence the membrane spectrum is exactly
  `{1,-1,1-2n,-(2n+1)}`, the membrane `\lambda=1` mode is simple and
  semisimple, and no membrane or `Q` eigenvalue contributes to
  `0 < \Re \lambda < 1`;
  this matches the checked recurrence-side membrane nullmode
  `(U1,V1,T1) = T1(\alpha,\beta,1)` and adds the corresponding
  `S_1 = -nT_1/(n-2)`;
  therefore the full bounded-sector theorem has not yet been proved, but the
  entire remaining low-spectrum question is now concentrated in the flexural
  `3 \times 3` block
  \[
  G_{flex}
  =
  \begin{pmatrix}
  -n & -\lambda_c & 0 \\
  \nu n^2/\lambda_c & -(n-1)-\nu/\lambda_c & \Lambda(1-\nu^2) \\
  -n^2\!\left[\frac{1}{\Lambda \lambda_c} + \frac{2}{C_{tw}}\right] &
  \frac{1}{\Lambda \lambda_c} - \frac{n^2(\lambda_c-1)}{C_{tw}} &
  \nu - n + 1
  \end{pmatrix};
  \]
  the exact first remaining spectral blocker is now the theorem-facing flexural
  audit of `G_{flex}` itself:
  determine `\ker G_{flex}`, prove `1 \notin \sigma(G_{flex})`, and exclude
  `0 < \Re \lambda < 1` inside `\sigma(G_{flex})`;
- verdict:
  `B. the cleaned richer-jet lift-existence lemma is reduced to one smaller
  explicit punctured-neighborhood first post-leading chart-realization lemma.`

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
