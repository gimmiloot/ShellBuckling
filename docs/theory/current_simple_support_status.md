# Current Simple-Support Operational Status

## Scope
This file is the canonical operational snapshot for the separate active 6-state
axisymmetric `simple support` background path.

It is intentionally short and operational. It does not replace:

- `docs/theory/current_simple_support_object_glossary.md` for stable object
  definitions and notation;
- `docs/theory/current_theory_verification_map.md` for claim-status tracking;
- `docs/theory/current_simple_support_final_audit_note.md` for the final
  audit-style closure reading of the current clean theorem-facing line;
- `docs/theory/current_simple_support_criterion_rebuild_note.md` for the
  current criterion-facing rebuild target, working-order reading, and
  `R1 / R2 / R3` source-of-truth interpretation;
- `docs/theory/current_simple_support_closed_line_index.md` for the frozen-line
  archive/index view and archive reading order;
- `docs/theory/current_mixed_weak_theory_note.tex` for compact scientific
  discussion;
- `docs/theory/vyvod_uravneniy_updated17.md` for derivation work;
- `docs/journal/project_journal_updated14.md` for project-stage discussion.

## Active 6-State Path
The active full-state simple-support background path is:

- core module: `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`
- state: `[T_s, T_sn, M_s, u_r, u_z, varphi]`
- BC set: center `T_sn(x0)=0`, `u_r(x0)=0`, `varphi(x0)=0`; edge `T_s(1)=0`,
  `M_s(1)=0`, `u_z(1)=0`

This path is separate from the preserved hybrid mixed-weak scans. Those older
scan tasks still use the reduced `F_min` background and should not be read as
the fully consistent simple-support solver path. A new clean standalone
critical-search program now also exists:

- core module: `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`
- task wrapper: `tasks/run_full_simple_support_critical_search.py`
- background continuation bridge: `src/shell_buckling/mixed_weak/simple_support_high_load_background_continuation.py`
- critical-layer boundary rows: `[u_n(1), varphi(1), T_s(1), S(1), H(1)]`

This new path reconnects the mixed-weak criticality layer to the honest full-
state simple-support background without reusing the older `F_min` line.


## Current Theorem-Facing Criterion Status
For operational reading on the current clean branch:

- use `A_ls` as the current selected reduced family;
- use `L_red` as the main theorem-facing reduced object;
- keep `B_red` / `B_mix` as exploratory descendants rather than proved
  replacements for `L_red`;
- use `docs/theory/current_simple_support_criterion_rebuild_note.md` as the
  current source-of-truth note for the rebuild target and for the
  `R1 / R2 / R3` reading;
- use `docs/theory/current_simple_support_criterion_bridge_note.md` for the
  current interpretation language;
- use `docs/theory/current_simple_support_object_glossary.md` for stable object
  definitions.

## Current Selection-Authority Status
The current clean hierarchy should now be read in the order

```text
clean path / equations / BC meaning
    -> selected-family construction
    -> canonical rebasing
    -> boundary descendants
    -> stacked diagnostics
    -> criterion authority.
```

On that hierarchy, the clean path itself is not the present bottleneck: the
audited boundary rows, center constraints, and rebasing identities stay clean.
The recipe-dependent layer is the selected-family rule that chooses the 2D span
inside the constrained fiber before rebasing. The current Tikhonov/KKT selector

```text
min ||A_int c||^2 + reg ||c||^2  subject to C_center c = d
```

is exact as a description of the current repo-selected family, but it is not
yet criterion-authoritative. Canonical rebasing

```text
V_adm = V_reg (C_amp V_reg)^(-1)
```

fixes coordinates on a chosen span; it does not make nearby chosen spans
coincide. So `B_red`, `B_mix`, and `rho_R2` must currently be read only as
descendants/diagnostics on the selected family, not as criterion-authoritative
outputs.

### Current selector-authority requirements

A future criterion-authoritative selector on the present clean branch would
need all of the following.

- structural/invariance requirements:
  preserve the clean amplitude/regularity constraints, remain compatible with
  the object hierarchy `A_ls -> L_red -> B_red -> B_mix`, and stay invariant
  under harmless representative/basis-choice changes of one fixed family;
- numerical robustness requirements:
  remain materially stable under small admissible regularization changes,
  avoid dependence on arbitrary cutoff tuning, and not change the qualitative
  near-pair `n=7` / `n=8` reading under nearby admissible selector choices on
  the checked settings;
- theorem-facing authority requirements:
  come from a theorem-facing weak/KKT or local-to-global selected-family
  principle that explains why one chosen 2D span is privileged inside the clean
  constrained fiber, rather than only from a numerical recipe;
- convenience-only properties that are not enough by themselves:
  small `C_amp V_adm - I` / `C_reg V_adm`, moderate `cond(G_amp)`, one calm
  window, or an attractive winner order.

Already closed or partially supported:

- the clean path, center constraints, and rebasing identities remain
  internally consistent;
- harmless representative changes are mostly washed out by canonical rebasing
  on the current audits;
- canonical rebasing is a valid post-selection coordinate fix on a chosen span.

Still open and now the true bottleneck:

- stability of the chosen span under nearby admissible selector choices such as
  small `reg` or cutoff changes;
- a theorem-facing reason why one selected family should be privileged;
- selector robustness strong enough not to change the qualitative near-pair
  `n=7` / `n=8` reading.

### Candidate theorem-facing selector principles now on the table

- weak/KKT-selected global family principle:
  structurally the closest to the live architecture and therefore the most
  natural promising candidate, but only if reformulated as a genuine
  theorem-facing weak/interior selection rule rather than as the current
  Tikhonov recipe;
- local-to-global selected-family principle:
  also promising in principle, but presently blocked because the repo does not
  yet close an intrinsic local selected object with a canonical global lift;
- trace-plane-first principle:
  compatible as a partial ingredient because the selected trace plane is closed,
  but not sufficient by itself because the trace data does not yet determine a
  unique privileged global family;
- variational/minimal-energy selector principle:
  currently unsupported on the present repo boundary because no canonically
  justified energy/coercivity functional has yet been derived for this role;
- no justified selector yet:
  this remains the correct current conservative status language until one of the
  theorem-facing principles above is actually derived and checked against the
  selector-authority requirements.

### Weak/KKT route: current surrogate versus theorem-facing target

- current live surrogate:
  for the two amplitude right-hand sides `d_1 = [1,0,0,0]`,
  `d_2 = [0,1,0,0]`, the code solves
  `min ||A_int c||^2 + reg ||c||^2` subject to `C_center c = d_j`,
  normalizes each solution, orthogonalizes the second against the first, forms
  `V_reg = [c_1, c_2]`, and only then canonically rebases to
  `V_adm = V_reg (C_amp V_reg)^(-1)`;
- what that surrogate captures correctly:
  hard center/amplitude constraints together with an interior weak-residual
  preference for low-`A_int` representatives;
- what a genuine weak/KKT selector principle would need instead:
  a theorem-facing selected-representative map from amplitude data to a
  privileged global 2D family that is justified by a canonical weak/interior
  optimality statement and does not rely on arbitrary `reg`, cutoff, or
  normalization/orthogonalization choices;
- exact missing step:
  replace the current recipe-level constrained Tikhonov solve by a closed
  theorem-facing weak/KKT selection principle that proves why one selected span
  is privileged inside the clean constrained fiber.

### Weak/KKT theorem-readiness verdict

- candidate theorem target:
  for fixed `(n,q)`, a theorem-facing selected-representative map
  `a -> c_weak(a)` from amplitude data `a in R^2` (equivalently the selected
  trace plane `im(D_amp)`) into a theorem-facing clean constrained class,
  with image a privileged 2D family;
- already precise enough:
  the code-level ambient class `X_trial`, the explicit center maps
  `C_center = [C_amp; C_reg]`, the explicit numerical constrained class
  `W_reg = {c in X_trial : C_reg c = 0}`, the current repo-selected family
  `A_repo = im(V_adm)`, and the reduced-object hierarchy
  `A_ls -> L_red -> B_red -> B_mix`;
- still not precise enough:
  the exact theorem-facing constrained class into which `c_weak(a)` should
  land is not yet independently closed, and the canonical weak/interior
  optimality principle selecting `c_weak(a)` is not yet identified;
- likely failure points if proof work started immediately:
  uniqueness/canonicity would still be underdetermined, trace data would still
  not determine a unique global family, and the present Tikhonov surrogate
  would still lack a theorem-facing convergence/consistency link;
- readiness verdict:
  `B. almost ready, but one or two lower-level clarifications should be done
  first`;
- exact prerequisites before proof work:
  first close the theorem-facing constrained class on which the weak selector is
  supposed to act; then state the canonical weak/interior optimality condition
  that would define `c_weak(a)` without arbitrary `reg`/cutoff choices.

### Theorem-facing constrained-class verdict for `A_con^th`

- primary natural candidate:
  the selected-trace constrained slice of the intended full theorem-facing
  admissible class, meaning
  `A_con^th,n(q) = {c in A_full^th,n(q) : J_0(c) in im(D_amp,n(q))}`
  or, fiberwise,
  `{c in A_full^th,n(q) : J_0(c) = D_amp a}`;
- secondary plausible candidate:
  a theorem-facing selected overclass closer to `A_ls`, such as the current
  structural candidate class `A_sel^{th,cand}` above the repo-selected family
  or a future local-to-global selected lift class;
- what is ruled out as the default codomain:
  the raw code-level spaces `X_trial,n`, `W_reg,n(q)`, and the exact numerical
  selected family `A_repo,n(q) = A_ls,n(q)` are not themselves the intended
  theorem-facing codomain;
- final codomain verdict:
  `B. A_con^th is narrowed to a short list of 2 plausible candidates`;
- exact block on fixing it more sharply:
  the full theorem-facing admissible/constrained class is not yet packaged as an
  independently closed continuum object, while the selected-overclass route is
  still blocked by the absence of a closed intrinsic local selected object with
  a canonical global lift.

### Preferred codomain route for the weak/KKT target

- route preference verdict:
  `A. Prefer the selected-trace constrained slice of the full admissible class
  as the main codomain target`;
- why this route is currently preferred:
  it keeps the weak/KKT geometry sharp by treating `S_weak,n,q` as a selector
  acting on a larger clean constrained fiber with fixed selected trace
  `J_0(c) = D_amp a`, rather than presupposing a partly selected codomain in
  advance;
- why the selected-overclass route is not the preferred codomain here:
  it remains a live neighboring theorem program, but it currently looks more
  like an alternative selected-object/lift story than the ambient codomain for
  a weak/interior selector;
- exact next bottleneck implied by this choice:
  package the intended full theorem-facing admissible class sharply enough that
  the selected-trace constrained slice becomes a clean codomain, then state the
  canonical weak/interior optimality rule on that codomain.

### Ambient full admissible/constrained class verdict for `A_full^th`

- preferred current meaning:
  the full clean admissible / center-regular tangent class of the continuous
  mixed problem on the present branch, read as the ambient theorem-facing class
  on which the finite leading-center trace `J_0` should be well-defined and on
  which the selected-trace slice
  `{c in A_full^th,n(q) : J_0(c) in im(D_amp,n(q))}`
  should make sense;
- what it is not:
  it is not the weighted-trial coefficient universe `X_trial,n`, not the
  explicit ansatz-level center-regular coefficient space `W_reg,n(q)`, not the
  exact repo-selected family `A_repo,n(q) = A_ls,n(q)`, and not the selected
  trace plane `im(D_amp,n(q))` by itself;
- what is already explicit:
  the current mixed equations, the clean boundary-condition meaning, the
  ansatz-level scaling orders, the explicit weighted-trial surrogates
  `X_trial,n` and `W_reg,n(q)`, and the exact selected-family trace identity
  `J_0(A_ls) = im(D_amp)`;
- what remains only surrogate-level:
  the weighted-trial/coefficient spaces are still only finite-dimensional
  numerical surrogates for the ambient continuum class, and the current exact
  trace map `J_0 = C_center` is closed only on the repository-selected /
  weighted-ansatz boundary;
- final ambient-class verdict:
  `B. A_full^th is narrowed substantially but still not sharp enough`;
- exact remaining obstacle:
  the repository still lacks an independently packaged continuum/local
  definition of the full admissible center-regular class with its higher-order
  formal continuation/completeness and theorem-facing trace regularity stated
  sharply enough to serve as the ambient codomain source for the preferred
  weak/KKT slice.

### Continuum/local class-plus-trace packaging verdict

- packaged current read:
  `A_full^th,n(q)` should now be read as the ambient continuum/local clean
  admissible / center-regular tangent class, while `J_0` should be read as the
  theorem-facing finite leading-center jet map on that class, retaining the two
  leading amplitudes together with the two leading regularity-defect rows;
- what is exact already on the weighted-ansatz / selected-family boundary:
  `J_0 = C_center`, `J_0(A_ls) = im(D_amp)`, and `J_0|_{A_ls}` is an exact
  bijection onto the selected trace plane;
- what still needs theorem-facing upgrade:
  the branch still needs a continuum/local statement that every
  `c in A_full^th,n(q)` carries a well-defined finite leading-center jet in the
  same 4D trace space, with enough local continuation/completeness and trace
  regularity that slicing by `J_0(c) in im(D_amp,n(q))` is cleanly meaningful;
- final packaging verdict:
  `B. the preferred codomain is much sharper, but one explicit continuum/local
  trace-regularity gap still remains`.

### `J_0` theorem-facing extension verdict

- what is exact only on the weighted-ansatz / selected-family boundary:
  `J_0 = C_center`, `J_0(A_ls) = im(D_amp)`, and the exact bijection
  `J_0|_{A_ls} : A_ls -> im(D_amp)`;
- intended theorem-facing meaning on `A_full^th,n(q)`:
  `J_0` should be the finite leading-center jet on the ambient clean
  admissible / center-regular class, retaining the two leading amplitudes and
  the two leading regularity-defect rows in the same 4D trace space used on the
  current selected-family boundary;
- exact remaining gap:
  the branch still lacks the theorem-facing extension statement that every
  ambient object `c in A_full^th,n(q)` has such a well-defined finite trace
  with enough local continuation/completeness and trace regularity for the
  slice `J_0(c) in im(D_amp,n(q))` to be cleanly meaningful;
- final `J_0`-gap verdict:
  `B. the J_0 gap is narrowed to one precise local/trace theorem task`.

### Sharp `J_0` local/trace theorem task now on deck

- candidate theorem target:
  for fixed `(n,q)`, define a theorem-facing finite leading-center jet map
  `J_0^th,n,q : A_full^th,n(q) -> R^4`
  by the current four coordinates
  `[U0, P0, N0 + (lambda_c / n) P0, Y0 - lambda_c P0]`;
- hypotheses the theorem would need:
  `c in A_full^th,n(q)` solves the current clean mixed equations in the
  intended ambient admissible / center-regular class, has the current near-
  center scaling orders, and admits enough local continuation/completeness that
  those four leading-center quantities exist uniquely and depend only on `c`;
- conclusion the theorem would need:
  `J_0^th,n,q(c)` is well-defined on all of `A_full^th,n(q)`, agrees with the
  current exact `C_center` trace on the weighted-trial overlap, and makes the
  selected-trace slice
  `{c in A_full^th,n(q) : J_0^th,n,q(c) in im(D_amp,n(q))}`
  cleanly meaningful;
- what this would solve and not solve:
  it would close the codomain meaning for the future weak/KKT selector, but it
  would still not by itself prove the weak/KKT selector theorem, criterion
  authority, or `A_full^th = A_ls`;
- sharpness verdict:
  `A. the remaining J_0 task is now sharp enough for a direct theorem attempt`
  on that local/trace theorem alone.

### Direct proof-attempt outcome for the `J_0` local/trace theorem

- theorem attempted:
  for fixed `(n,q)`, define
  `J_0^th,n,q : A_full^th,n(q) -> R^4`
  by the current four coordinates
  `[U0, P0, N0 + (lambda_c / n) P0, Y0 - lambda_c P0]`,
  and prove that it is well-defined on all of `A_full^th,n(q)`, agrees with
  `C_center` on the weighted-trial overlap, and makes
  `{c in A_full^th,n(q) : J_0^th,n,q(c) in im(D_amp,n(q))}`
  meaningful;
- what is already closed enough to use:
  the exact ansatz-level trace theorem
  `J_0 = C_center`, `J_0(A_ls) = im(D_amp)`, and `J_0|_{A_ls}` bijective onto
  `im(D_amp)`, together with the leading local symbolic recovery of
  `im(D_amp)` in the same `J_0` coordinates;
- exact first unresolved lemma:
  prove that every ambient object `c in A_full^th,n(q)` admits a unique
  current-normalized leading-center quadruple `(U0, N0, P0, Y0)` in the
  current near-center scaling class, compatible with the continuous mixed
  equations and agreeing with the exact weighted-trial trace `C_center` on the
  overlap where both are defined;
- why this is the first blocker:
  without that ambient finite-jet extraction lemma, the map `J_0^th,n,q`
  cannot yet be defined on the whole domain `A_full^th,n(q)`, so the global
  uniqueness clause and the codomain slice on `A_full^th,n(q)` do not yet
  start;
- outcome verdict:
  `B. the theorem is not fully proved, but the proof attempt reduces it to one
  smaller explicit local/trace lemma task`;
- nature of the obstruction:
  still local/trace in nature, centered on ambient finite-jet
  existence/uniqueness plus trace regularity; it does not reopen the selector
  layer or the codomain-route choice.

### Direct theorem-attempt outcome for the ambient finite-jet extraction lemma

- lemma attempted:
  for every `c in A_full^th,n(q)`, there exists a unique current-normalized
  leading-center quadruple `(U0, N0, P0, Y0)` compatible with the clean mixed
  equations, such that
  `[U0, P0, N0 + (lambda_c / n) P0, Y0 - lambda_c P0]`
  is well-defined and agrees with `C_center` on the weighted-trial overlap;
- what closes conditionally once those four coefficients exist:
  uniqueness of the normalized quadruple is formal inside the current scaling
  class, the leading mixed-equation compatibility block gives
  `n N0 + lambda_c P0 = 0` and `n N0 + Y0 = 0`, and the overlap agreement with
  `C_center` is already exact on the current weighted-ansatz boundary;
- exact first unresolved sublemma:
  prove that every ambient object `c in A_full^th,n(q)` admits the four
  current-normalized leading coefficients `(U0, N0, P0, Y0)` in the current
  near-center scaling class for the channels `(u_s, u_n, varphi, psi)`,
  before imposing the already known leading mixed-equation relations between
  them;
- why this is smaller than the previous blocker:
  the old blocker bundled coefficient extraction, equation compatibility, and
  overlap agreement together, while the present proof attempt shows that only
  the ambient coefficient-extraction step is still genuinely open;
- verdict:
  `B. the lemma is not proved, but it is reduced to one smaller explicit
  sublemma`;
- nature of the residual gap:
  still local/trace in nature and now sharper than a full finite-jet theorem:
  it is an ambient leading-coefficient extraction / normalization question, not
  a selector or codomain-choice ambiguity.

### Direct theorem-attempt outcome for the ambient leading-coefficient extraction / normalization sublemma

- sublemma attempted:
  for fixed `(n,q)`, every `c in A_full^th,n(q)` admits the four
  current-normalized leading coefficients `(U0, N0, P0, Y0)` for the channels
  `(u_s, u_n, varphi, psi)` in the current near-center scaling class;
- what already closes once the one-term asymptotics exist:
  uniqueness of `(U0, N0, P0, Y0)` inside the current normalization is formal,
  the weighted-trial overlap still agrees with `C_center`, and the already
  checked leading mixed-equation block can then act on those coefficients;
- exact first unresolved sub-sublemma:
  prove that every ambient object `c in A_full^th,n(q)` admits the one-term
  current-normalized asymptotics
  `u_s = U0 x^n + o(x^n)`,
  `u_n = N0 x^n + o(x^n)`,
  `varphi = P0 x^(n-1) + o(x^(n-1))`,
  `psi = Y0 x^(n-1) + o(x^(n-1))`
  in the current center-trace convention;
- why this is smaller than the previous blocker:
  the previous sublemma asked already for extracted coefficients, while the
  present proof attempt shows that extraction/normalization would be automatic
  once this ambient one-term asymptotic existence statement were available;
- verdict:
  `B. the sublemma is not proved, but it is reduced to one smaller explicit
  asymptotic-existence sub-sublemma`;
- nature of the residual gap:
  still purely local/trace in nature, now at the level of ambient one-term
  asymptotic existence in the current scaling class.

### Direct theorem-attempt outcome for the ambient one-term asymptotic existence sub-sublemma

- sub-sublemma attempted:
  for fixed `(n,q)`, every `c in A_full^th,n(q)` admits the one-term
  current-normalized asymptotics
  `u_s = U0 x^n + o(x^n)`,
  `u_n = N0 x^n + o(x^n)`,
  `varphi = P0 x^(n-1) + o(x^(n-1))`,
  `psi = Y0 x^(n-1) + o(x^(n-1))`
  in the current center-trace normalization;
- what already closes once the normalized limits exist:
  the one-term asymptotics follow immediately, extraction of
  `(U0, N0, P0, Y0)` is automatic, uniqueness is formal, and the overlap with
  `C_center` remains exact on the weighted-trial boundary;
- what is already supported before that point:
  the principal-part analysis fixes the current scaling orders
  `u_s, u_n = O(x^n)` and `varphi, psi = O(x^(n-1))`, so the first unresolved
  point is no longer the choice of exponents themselves;
- exact first unresolved sub-sub-sublemma:
  prove that every ambient object `c in A_full^th,n(q)` has finite
  current-normalized channel limits
  `lim x^(-n) u_s`,
  `lim x^(-n) u_n`,
  `lim x^(1-n) varphi`,
  `lim x^(1-n) psi`
  in the present center-trace convention;
- why this is smaller than the previous blocker:
  the previous sub-sublemma asked already for one-term asymptotics, while the
  present proof attempt shows that the still-missing ingredient is even more
  primitive: existence of the four normalized limits themselves;
- verdict:
  `B. the sub-sublemma is not proved, but it is reduced to one smaller
  explicit normalized-limit sub-sub-sublemma`;
- nature of the residual gap:
  still purely local/trace in nature, now at the level of ambient
  normalized-limit existence in the current scaling orders.

### Direct theorem-attempt outcome for the ambient normalized-limit existence sub-sub-sublemma

- sub-sub-sublemma attempted:
  for fixed `(n,q)`, every `c in A_full^th,n(q)` has finite current-normalized
  channel limits
  `lim x^(-n) u_s`,
  `lim x^(-n) u_n`,
  `lim x^(1-n) varphi`,
  `lim x^(1-n) psi`
  in the present center-trace convention;
- what is already supported before the limit step:
  the principal-part scaling analysis already gives
  `u_s, u_n = O(x^n)` and `varphi, psi = O(x^(n-1))`, so the four normalized
  quotients are already known to be bounded in the current scaling class;
- what also remains aligned:
  on the weighted-trial overlap the same normalized quantities are exactly the
  `C_center` / `J_0` coordinates already used on the selected-family boundary;
- exact first unresolved sub-sub-sub-sublemma:
  prove that for every ambient object `c in A_full^th,n(q)`, the bounded
  renormalized channels
  `x^(-n) u_s`,
  `x^(-n) u_n`,
  `x^(1-n) varphi`,
  `x^(1-n) psi`
  actually converge as `x -> 0`, equivalently extend continuously to the center
  in the present trace normalization;
- why this is smaller than the previous blocker:
  the previous sub-sub-sublemma asked for finite normalized limits as a whole,
  while the present proof attempt shows that the boundedness half is already
  supported by the current scaling analysis and only the convergence /
  continuous-extension half remains open;
- verdict:
  `B. the sub-sub-sublemma is not proved, but it is reduced to one smaller
  explicit normalized-quotient convergence sub-sub-sub-sublemma`;
- nature of the residual gap:
  still purely local/trace in nature, now at the level of convergence of the
  already-bounded renormalized center channels.

### Direct theorem-attempt outcome for the ambient normalized-quotient convergence sub-sub-sub-sublemma

- sub-sub-sub-sublemma attempted:
  for fixed `(n,q)`, every `c in A_full^th,n(q)` satisfies that the bounded
  renormalized channels
  `x^(-n) u_s`,
  `x^(-n) u_n`,
  `x^(1-n) varphi`,
  `x^(1-n) psi`
  converge as `x -> 0`, equivalently extend continuously to the center, in the
  present center-trace convention;
- route 1, derivative / integrability:
  does not close at the current repo level;
  no theorem-facing derivative bounds or integrable-derivative statement for
  the four renormalized channels has yet been derived on ambient
  `A_full^th,n(q)` objects;
- route 2, regular-singular system:
  gets furthest;
  the principal center model and the checked recurrence layers strongly support
  that these renormalized channels are the right near-center variables, but the
  repo still lacks the theorem-facing ambient statement that they satisfy a
  closed renormalized local system / recurrence strong enough to force
  convergence of bounded solutions;
- route 3, compactness / continuity:
  does not close at the current repo level;
  there is no stronger ambient local continuation/completeness theorem beyond
  the current scaling bounds that would upgrade boundedness to convergence by a
  compactness argument alone;
- exact first unresolved sub-sub-sub-sub-sublemma:
  prove an ambient renormalized regular-singular limit lemma:
  for every `c in A_full^th,n(q)`, the renormalized channel vector
  `W_c(x) = [x^(-n) u_s, x^(-n) u_n, x^(1-n) varphi, x^(1-n) psi]`
  satisfies a theorem-facing near-center local system / recurrence on which the
  present boundedness of `W_c` implies convergence of `W_c(x)` as `x -> 0`;
- why this is smaller than the previous blocker:
  the previous sub-sub-sub-sublemma asked directly for convergence of the four
  renormalized channels, while the present proof attempt shows that the route
  with the most traction is narrower and structural:
  a renormalized regular-singular continuation statement that forces limit
  existence for bounded ambient solutions;
- verdict:
  `B. the sub-sub-sub-sublemma is not proved, but it is reduced to one smaller
  explicit renormalized regular-singular limit sub-sub-sub-sub-sublemma`;
- nature of the residual gap:
  still purely local/trace in nature, now at the level of regular-singular
  limit existence / local continuation for the renormalized center channels.

### Direct theorem-attempt outcome for the ambient renormalized regular-singular limit sub-sub-sub-sub-sublemma

- lemma attempted:
  for fixed `(n,q)`, every `c in A_full^th,n(q)` should determine the
  renormalized channel vector
  `W_c(x) = [x^(-n) u_s, x^(-n) u_n, x^(1-n) varphi, x^(1-n) psi]`
  on a punctured near-center neighborhood, with a theorem-facing
  regular-singular local continuation statement strong enough that boundedness
  of `W_c` implies convergence of `W_c(x)` as `x -> 0`;
- exact regular-singular route used:
  the current richer-jet / recurrence route through
  `Xi_rich^(1,eta)`, `Xi_rich^(1+,eta)`, and the canonical projection
  `Pi_eta_to_J0`;
- what is already closed on that route:
  the renormalized variables are the correct current center-trace coordinates,
  the checked recurrence layers organize the formal local picture in those
  variables, and the projection back to current `J_0 = C_center` coordinates is
  exact on the checked richer trace charts;
- exact first unresolved sub-sub-sub-sub-sub-sublemma:
  prove an ambient renormalized local-system derivation / jet-lift lemma:
  every `c in A_full^th,n(q)` admits a punctured near-center renormalized local
  state extending `W_c` by the first post-leading variables of the current
  richer jet, and that state satisfies a closed theorem-facing near-center
  regular-singular system whose leading structure matches the checked
  recurrence/principal-part model;
- why this is the first true blocker:
  before this ambient local-system / jet-lift statement is available, the
  checked recurrence remains only a formal finite-order jet calculation rather
  than a theorem on arbitrary ambient objects;
  so the proof stops before regular-singular classification or bounded-solution
  convergence inside a closed ambient system can even be applied;
- verdict:
  `B. the lemma is not proved, but it is reduced to one smaller explicit
  ambient renormalized local-system / jet-lift sub-sub-sub-sub-sub-sublemma`;
- nature of the residual gap:
  still purely local/trace in nature, now primarily at the level of deriving
  the ambient punctured-neighborhood renormalized regular-singular system
  itself, inseparable from the needed local continuation/completeness input.

### Direct theorem-attempt outcome for the ambient punctured-neighborhood renormalized local-system / jet-lift lemma

- lemma attempted:
  for fixed `(n,q)`, every `c in A_full^th,n(q)` admits a punctured near-center
  local state extending
  `W_c(x) = [x^(-n) u_s, x^(-n) u_n, x^(1-n) varphi, x^(1-n) psi]`
  by the first post-leading variables of the current richer jet, and that
  extended state satisfies a closed theorem-facing near-center regular-singular
  system whose leading structure agrees with the checked principal-part /
  recurrence model;
- what is already aligned:
  the richer-jet route
  `Xi_rich^(1,eta)`, `Xi_rich^(1+,eta)`, `Pi_eta_to_J0`
  identifies the correct formal post-leading variables and their projection back
  to the present `J_0 = C_center` coordinates;
- exact first unresolved smaller lemma:
  prove an ambient punctured-neighborhood richer-jet lift existence lemma:
  for every `c in A_full^th,n(q)`, there exists a punctured near-center local
  lift realizing the first post-leading richer-jet variables corresponding to
  `Xi_rich^(1,eta)` (and, when the membrane direction is kept explicit,
  `Xi_rich^(1+,eta)`), compatible with the renormalized vector `W_c(x)`,
  with the canonical projection `Pi_eta_to_J0`, and with the exact
  ansatz-boundary trace `J_0 = C_center` on the weighted-trial overlap whenever
  both descriptions are defined;
- why this is the first true blocker:
  before such a lift exists for arbitrary ambient objects, the current richer
  jet remains only a formal checked jet chart rather than a theorem-facing
  punctured-neighborhood state;
  so derivation of a closed ambient local system and its later regular-singular
  consequences cannot yet be applied;
- verdict:
  `B. the lemma is not proved, but it is reduced to one smaller explicit
  punctured-neighborhood richer-jet lift-existence lemma`;
- nature of the residual gap:
  still purely local/trace in nature, now first at the level of punctured-
  neighborhood lift existence rather than closure or convergence inside an
  already-derived local system.

### Targeted CAS+Lean back-verification of the current proof line

- scope of this pass:
  only the current load-bearing theorem line around
  `J_0 = C_center`, `J_0(A_ls) = im(D_amp)`, the richer-jet projection
  `Pi_eta_to_J0`, and the present local/trace reduction chain;
- CAS/code re-checks that are now reconfirmed:
  the live code-level `C_center` map sees exactly the four `k = 0` ansatz
  columns for `u_s`, `u_n`, `varphi`, `psi`;
  in those coordinates the exact current `J_0` trace is
  `[U0, P0, N0 + (lambda_c / n) P0, Y0 - lambda_c P0]`,
  with determinant `-1` on the four leading-center coordinates;
  the selected leading local relations still send this trace exactly to
  `im(D_amp)`;
  the richer-chart projection `Pi_eta_to_J0` is algebraically exact and
  satisfies
  `Pi_eta_to_J0(im(D_rich,eta)) = im(D_amp)`;
  the first checked post-leading recurrence is still an exact direct product
  over `(U0, P0)` and the membrane nullmode still kills every checked residual
  row after substitution;
- proof-skeleton audit result:
  the abstract implications
  `normalized limits => one-term asymptotics`,
  `one-term asymptotics => formal coefficient extraction`,
  and
  `J_0^th well-defined => selected-trace slice meaningful`
  are clean;
  the first step that needs one extra explicit premise is
  `richer-jet lift + regular-singular convergence => J_0^th well-defined`;
- exact extra premise now made explicit:
  one must also require overlap compatibility of the ambient richer-jet lift
  with the current exact `J_0 = C_center` coordinates on the weighted-trial /
  selected-family boundary, equivalently a theorem-facing compatibility of the
  ambient lift with the canonical projection back to the current `J_0` trace;
- status consequence:
  no currently closed ansatz-boundary identity is downgraded;
  but future proof-skeleton statements on this branch should no longer treat
  `richer-jet lift + regular-singular convergence`
  by itself as sufficient for
  `J_0^th` well-definedness;
  the compatibility / projection clause should be stated explicitly.

### Next active local theorem target after proof-line cleanup

- corrected next target:
  prove the ambient punctured-neighborhood richer-jet lift-existence lemma in
  the cleaned theorem-line form:
  for every `c in A_full^th,n(q)`, there exists a punctured near-center richer-
  jet lift realizing the first post-leading variables of
  `Xi_rich^(1,eta)` and, when needed, `Xi_rich^(1+,eta)`, extending the
  renormalized vector
  `W_c(x) = [x^(-n) u_s, x^(-n) u_n, x^(1-n) varphi, x^(1-n) psi]`,
  and returning compatibly to the current exact `J_0 = C_center` trace via the
  canonical projection `Pi_eta_to_J0` on the weighted-trial overlap;
- why this is the right next theorem target:
  this packages overlap compatibility into the theorem setup itself, so the
  later implication
  `richer-jet lift + regular-singular convergence + overlap compatibility
  => J_0^th well-defined`
  no longer hides an extra premise in the middle of the proof line;
- current reading:
  no theorem-facing `J_0` closure should be claimed from a richer-jet lift /
  convergence statement that omits this overlap-compatibility clause.

### Direct proof-attempt outcome for the cleaned ambient punctured-neighborhood richer-jet lift-existence lemma

- lemma attempted:
  for fixed `(n,q)`, every `c in A_full^th,n(q)` should admit a punctured near-
  center richer-jet lift realizing the first post-leading variables of
  `Xi_rich^(1,eta)` and, when needed, `Xi_rich^(1+,eta)`, extending
  `W_c(x) = [x^(-n) u_s, x^(-n) u_n, x^(1-n) varphi, x^(1-n) psi]`,
  compatible with `Pi_eta_to_J0`, and overlap-compatible with the exact
  ansatz-boundary trace `J_0 = C_center`;
- what already closes once such a richer chart is realized:
  extension of `W_c` is then built into the chart data,
  compatibility with `Pi_eta_to_J0` is exact by the current richer-chart
  projection formula,
  overlap return to `J_0 = C_center` is then a formal compatibility clause on
  the weighted-trial overlap,
  and the later regular-singular step can be posed on that lifted state;
- exact first unresolved smaller lemma:
  prove an ambient punctured-neighborhood first post-leading chart-realization
  lemma:
  every `c in A_full^th,n(q)` admits punctured near-center first post-leading
  chart data realizing `Xi_rich^(1,eta)` and, when needed, `Xi_rich^(1+,eta)`,
  extending `W_c`, so that the canonical projection `Pi_eta_to_J0` and the
  overlap return to `J_0 = C_center` are meaningful;
- why this is smaller than the cleaned target lemma:
  the cleaned target bundled chart realization together with projection and
  overlap consequences, while the present proof attempt shows that those latter
  parts are already formal once the current richer chart itself is realized for
  an arbitrary ambient object;
- verdict:
  `B. the lemma is not fully proved, but it is reduced to one smaller explicit
  local chart-realization lemma`;
- nature of the residual gap:
  still purely local/trace in nature, now at the level of punctured-
  neighborhood first post-leading chart realization for ambient objects, not at
  the level of the projection or overlap clauses themselves.

## Frozen Theorem-Line Note
The older theorem-facing line is frozen and should not be continued in the same
style from this operational status page.

Operationally, the only reading needed here is:

- the frozen line did not validate the current criterion;
- it did not refute the current criterion either;
- the current criterion still does not have theorem-facing authority to exclude
  the explicit membrane candidate on the present clean boundary.

For the frozen-line conclusion, exact final unresolved endpoint, and reusable
results, see:

- `docs/theory/current_simple_support_final_audit_note.md`
- `docs/theory/current_simple_support_closed_line_index.md`
- `docs/theory/current_simple_support_object_glossary.md`

Read `docs/theory/current_simple_support_closed_line_index.md` as archive /
frozen-line navigation, not as the primary working-order entry point for the
current criterion-facing branch.

For the current live criterion-facing working order, start from:

1. `docs/theory/current_simple_support_status.md`
2. `docs/theory/current_simple_support_object_glossary.md`
3. `docs/theory/current_simple_support_final_audit_note.md`
4. `docs/theory/current_simple_support_criterion_rebuild_note.md`
5. `docs/theory/current_simple_support_criterion_bridge_note.md`
6. `docs/theory/current_theory_verification_map.md`

## First Clean Full Critical-Search Campaign
The first full exploratory run of the standalone clean simple-support critical
search is still kept in memory as an implementation baseline:

- runner: `tasks/run_full_simple_support_critical_search.py`
- honest background BC set: center `T_sn(x0)=0`, `u_r(x0)=0`, `varphi(x0)=0`;
  edge `T_s(1)=0`, `M_s(1)=0`, `u_z(1)=0`
- critical rows: `[u_n(1), varphi(1), T_s(1), S(1), H(1)]`
- first mode range: `n=2..6`

That first clean campaign used the right formulation but not yet the proven
high-load continuation discipline of the separate honest background path:

- the initial moderate scan on `0..15 MPa` with 31 load points succeeded only
  through `4.0 MPa` and then lost the background at `4.5 MPa`;
- a narrow upper-edge refinement on `3.0..4.4 MPa` pushed the clean program to
  `4.3 MPa` and then lost the background at `4.4 MPa`;
- a second upper-edge refinement on `4.30..4.343 MPa` reached `4.3246 MPa` and
  then failed at `4.3276 MPa`.

This earlier `4.32..4.5 MPa` clean-program loss should now be read only as a
superseded continuation bottleneck inside the first standalone implementation.
It is not evidence that the honest full-state simple-support background
physically ends there.

## High-Load-Enabled Clean Critical Search
The clean standalone search now also reuses the proven honest high-load
background-following discipline through:

- reusable bridge: `src/shell_buckling/mixed_weak/simple_support_high_load_background_continuation.py`
- same equations and same honest simple-support BC set as the active 6-state
  background path;
- exact retained high-load checkpoints from the separate pilot-21 background
  path where they already exist;
- the same `u_z`-scaled secant continuation attempts and runtime-controlled
  bounded step adaptation above the directly solved low-load band;
- no fallback to the old hybrid `F_min` background line.

With that upgrade the clean standalone `0..15 MPa` search for `n=2..6` now
succeeds through the full scheduled band with no background failure:

- successful background solves: `31 / 31`;
- highest reached clean-program load: `15.0 MPa`;
- first background failure in the scheduled clean run: not reached;
- the clean program now genuinely probes the FEM-oriented `12..14 MPa` region.

Current exploratory mode-by-mode reading from the clean program is now broader:

- `n=4`: weak control-mode interior minimum remains near `11.1 MPa`; this mode
  is still kept in the competition set because of the older FEM-oriented prior,
  not because the clean broad scan now makes it numerically strong;
- `n=6`: current leading supported clean candidate is an interior minimum near
  `17.6 MPa`; it remains exploratory and not yet a final physical claim, but it
  is still the strongest current candidate that has survived the clean
  competition workflow with at least moderate stability support;
- `n=8`: main unstable rival now sits near `17.8 MPa`; on some local windows it
  can beat `n=6` in raw `sigma_bal`, but its advantage remains sensitive to the
  exact local window and selected discretization;
- `n=7`: reserve mode can produce very sharp raw dips near `17.2..17.4 MPa`,
  including raw `sigma_bal` values below the current supported candidate, but
  these sharp dips have not yet shown acceptable robustness and should stay
  classified as raw-but-unsupported reserve readings;
- `n=14`: reserve mode also produces an interior point above the older
  `18 MPa` broad ceiling neighborhood, near `19.3 MPa`, but it has not yet
  upgraded into a stable real competitor;
- the earlier `n=5` / `n=6` target-band reading near `13.95..14.25 MPa`
  remains part of the project memory, but it is no longer the full current
  clean competition reading.

So the unresolved bottleneck is no longer honest-background reach. It is now
criterion discrimination / candidate selection inside the clean full
simple-support search: how to separate supported interior valleys from raw
window-sensitive sharp dips. The leading supported reading is presently `n=6`
near `17.6 MPa`; `n=8` remains the main unstable rival; `n=7` remains a raw
reserve dip without acceptable robustness; `n=4` remains a weak control mode.
None of these values is yet a final physical critical-load claim.

The later `A + C` criterion pilot did not materially improve this competition
picture: branch-aware descriptors were useful mainly negatively, while the
augmented / bordered solvability reading stayed boundary-led and unstable. A
first light `D` pilot on the same clean architecture then gave interior-
dominated local signals for `n=6`, `n=7`, and `n=8`, no longer read `n=7` as
the single strongest point-like dip, and placed `n=8` first in the focused
baseline D ranking; however, it did not settle the `n=6` versus `n=8`
competition robustly enough to replace the conservative supported-candidate
operational memory. A first light `E` pilot has now also been checked on the
same clean architecture: it uses an energy-like reduced-coercivity surrogate
based on the local tangent bundle plus an amplitude norm built from current
strain / curvature channels. This `E` reading is much more interpretable than
the raw boundary-only metric and stays interior-distributed on the checked
windows, but it still places `n=8` first in the focused baseline E ranking,
keeps `n=7` competitive, and therefore also does not yet settle the
competition strongly enough to replace the current conservative operational
memory.



A first focused robustness pass for the first practical stacked `R2` reading
`rho_R2` has now also been checked on dense local windows for `n=6`, `n=7`,
and `n=8` under small `m_basis` / `n_collocation` variations. In that pass,
`rho_R2` keeps `n=8` ahead of `n=7` in five of the six checked settings and
keeps `n=6` below both in all six, but the combined finer setting
`m_basis = 7`, `n_collocation = 140` flips the top two with only a small
`n=7`-vs-`n=8` gap. The flip does not align with worsening winner
`cond(G_amp)`: the lowest- and highest-winner-conditioning settings still keep
`n=8` first. So `rho_R2` is informative and keeps `n=7` as a competitive
second in R2 language, but it is not yet robust enough to replace the current
conservative operational memory or to promote `rho_R2` to the new main working
criterion.

Later selected-family sensitivity and selection-rule audits sharpen the same
reading further. Harmless representative/basis changes are mostly washed out by
canonical rebasing, but nearby changes of the selection rule are not. In
particular, the current Tikhonov-selected family is too recipe-sensitive for
criterion authority, while the seemingly more stable truncated-SVD alternative
is still cutoff-dependent enough that it should not yet be promoted. So the
current `n=7` / `n=8` picture should now be read as a near-degenerate
selected-family reading on a selection-layer-unresolved branch: `rho_R2` stays a
comparative stacked diagnostic, not a criterion-authoritative winner rule.

## Current Reproducible Loads
Several load markers should now be kept separate:

- old-path reproducible anchor load: `4.3434 MPa`
- old-path first persistent failure load: `4.3440 MPa`
- best bounded method-sweep ceiling from pilot 20: `4.3520 MPa` (`u_z_scaled_state`)
- best bounded staged continuation ceiling from pilot 21: `4.3800 MPa` (`u_z`-scaled continuation + auxiliary arc-like step adaptation)
- strongest post-audited validated operational milestone: `4.4000 MPa` (same accepted seed, repeated pointwise confirm, `near_reproducible = true`, no branch-jump suspicion, short probe through `4.4100 MPa`, but `strict_reproducible = false`)
- higher validated operational milestones from the fast/confirm workflow: `7.0000 MPa` and `10.0000 MPa` (same accepted seed, no branch-jump suspicion, smooth repeat drift smaller than adjacent-step drift, short confirm probes through `7.0080` and `10.0200 MPa`, `strict_reproducible = false`, `near_reproducible = false`)
- current clean full simple-support critical-search broad compatible scan reach: `18.0000 MPa` with `38 / 38` scheduled background points on the clean compatible load ladder
- selected local competition / reserve windows have also been checked up to `22.0000 MPa` with retained-checkpoint-seeded clean helper continuation using the same equations and BC set; these local checks have not yet established a deeper supported candidate above `18 MPa`
- current fast-engine highest stored accepted load: `10.0000 MPa` (`fast_u_z_scaled_arc_like_continuation.py`), still kept separate from the canonical audited ceiling language
- best bounded staged continuation first failure in the audited pilot-21 ladder: not reached
- current short confirm probes above the newer fast-engine checkpoints: no failure reached through `4.4100 MPa` from the dedicated `4.4000 MPa` audit and through `10.0200 MPa` from the sparse `7.0000 / 10.0000 MPa` confirms

The `4.3434 / 4.3440 MPa` pair is still the canonical old-path reference for
the original single-domain rescue-local continuation workflow. The `4.3520 MPa`
value remains the bounded pilot-20 method ceiling for the standalone
`u_z`-scaled solve. The `4.3800 MPa` value remains the current audited
pilot-21 continuation ceiling on the same 6-state equations and BC set. The
`4.4000 MPa`, `7.0000 MPa`, and `10.0000 MPa` points should now be read as
validated operational milestones: they have dedicated milestone confirms with
strong same-branch indicators and successful short probes, but they do not have
strict audit closure and therefore do not replace the canonical audited
ceiling. Intermediate accepted points on the fast/resumable path remain
operational continuation evidence unless they are explicitly rechecked. None of
these values is a final physical critical load claim.

## Current Milestone / Audit Policy
The confirm language is now explicit and split into same-branch indicators plus
a three-level reporting ladder.

Same-branch indicators:

- same accepted seed;
- no `branch_jump_suspicion` in the continuity check;
- repeat drift remains smooth across checked milestones;
- repeat drift remains smaller than an ordinary adjacent continuation step;
- strongest gradient ordering remains `u_z > varphi > T_s`;
- BC residuals remain sane.

Promotion policy:

- `strict_reproducible`
  same-load repeat solve closes under the inherited pilot-12 gate
  `1e-7 / 1e-6` in max-relative-L2 / max-relative-max;
- `near_reproducible`
  same-load repeat solve keeps the same accepted seed and closes under the
  relaxed fast-workflow gate `2e-5 / 2e-4`;
- `operational continuation evidence`
  accepted fast-run continuation result without dedicated milestone validation;
- `validated operational milestone`
  dedicated milestone confirm keeps the same accepted seed, stays free of
  `branch_jump_suspicion`, keeps repeat drift smooth and smaller than an
  ordinary adjacent continuation step, preserves the current strongest
  gradient ordering and BC sanity checks, and records a short confirm probe
  without failure. `strict_reproducible` is not required; `near_reproducible`
  is supportive but not mandatory if the repeat drift still looks like a small
  smooth same-branch drift;
- `audited ceiling`
  promotion above the current audited ceiling still requires explicit milestone
  audit closure under the stricter current standard, including
  `strict_reproducible`.

This reporting change is about project discipline, not changed equations or BCs.
It keeps the status language conservative while preventing high-load same-branch
points from getting stuck between overly weak generic operational wording and
overly strong audited-ceiling wording. Loads above `4.3800 MPa` are still not
promoted silently, and the current `strict_reproducible = false` signal remains
an explicit open audit-policy issue rather than a silent branch-loss claim.

Milestone retention is also explicit in the fast workflow. By default the
retained confirmable milestone schedule includes:

- `4.3520 MPa`;
- `4.3800 MPa`;
- `4.4000 MPa`;
- the `0.5 MPa` round grid;
- the next `10 -> 15 MPa` confirm-critical schedule `11.0`, `12.0`, `12.5`,
  `13.0`, `13.5`, `14.0`, `15.0 MPa`;
- the current bootstrap/target loads;
- any extra user-requested `--milestone-load-mpa` values that are actually
  reached.

## Current Barrier Interpretation
The current reading is still mainly numerical, but now more sharply numerical
formulation / conditioning dominated:

- the old single-domain path still reaches a reproducible `4.3434 MPa` anchor
  and still fails first at `4.3440 MPa` with very small BC residuals;
- pilot 18 still shows no clear near-fold / collapsing-singular-value signal;
- pilot 19 showed that simple right-edge mesh concentration alone does not move
  the ceiling materially;
- pilot 20 showed that predictor-only changes help only modestly, while an
  unchanged-equation state representation change (`u_z`-scaled solve) moves the
  bounded ceiling to `4.3520 MPa`;
- pilot 21 then turned that into one main audited high-load workflow: the exact
  `u_z`-scaled continuation path plus auxiliary arc-like step adaptation
  reproduced `4.3520 MPa` and carried the bounded staged ladder through
  `4.3550`, `4.3600`, `4.3700`, and `4.3800 MPa` with reproducible stage
  retests and no bounded failure in the packaged ladder;
- the fast/confirm operational split reuses the same equations and BCs, adds
  checkpoint/resume, and now carries the stored path through `4.4200`,
  `4.4400`, `4.4600`, `4.4800`, `4.5000`, `4.6000`, `4.7000`, `4.8000`,
  `4.9000`, `5.0000`, `5.2000`, `5.4000`, `5.6000`, `5.8000`, `6.0000`,
  `6.5000`, `7.0000`, `8.0000`, `9.0000`, and `10.0000 MPa` without a bounded
  failure event in the saved fast ladder;
- a stricter dedicated audit at `4.4000 MPa` repeats the same accepted seed in
  two independent pointwise confirm passes, stays `near_reproducible`, shows no
  branch-jump suspicion, and does not hit a short failure probe through
  `4.4100 MPa`; under the new reporting policy this closes `4.4000 MPa` as a
  validated operational milestone, but it still does not satisfy the stricter
  `strict_reproducible` gate and therefore does not replace the audited ceiling;
- sparse confirms at `7.0000` and `10.0000 MPa` keep the same accepted
  seed, show no branch-jump suspicion, and do not hit short failure probes
  through `10.0200 MPa`; their repeat drift stays in the same smooth
  `2.85e-5..3.30e-5` max-relative-L2 band and still fails the current
  `near_reproducible` threshold even while remaining much smaller than an
  ordinary adjacent continuation step, so under the new reporting policy they
  also qualify as validated operational milestones rather than as audited
  ceiling replacements;
- after the clean standalone critical-search path was upgraded to reuse the
  same high-load continuation discipline, the honest background also stays
  alive through the clean `0..15 MPa` mixed-weak search; this confirms that the
  earlier standalone `4.32..4.5 MPa` loss was a solver-workflow bottleneck,
  not evidence of a physical end of the honest background branch;
- the repeat drift is smooth and currently dominated by `M_s`, while the
  strongest gradient ordering inside the accepted branch still remains `u_z`,
  then `varphi`, then `T_s`;
- the current `strict_reproducible` gate is still inherited from the older
  pilot-12 threshold pair `1e-7 / 1e-6`, so the remaining strict-false signal
  presently reads more like an open audit-policy / metric issue than like
  evidence of branch loss.

So the barrier still reads as numerical rather than as a verified physical fold,
and the newer data sharpen that reading toward solver formulation / conditioning
plus confirm-policy sensitivity rather than toward a verified physical end of
branch.

## Shallow / Non-Shallow Comparison Status
The shallow-comparison picture is now sharper but still conservative:

- the old shallow comparison path was BC-mismatched for simple support;
- pilot 16 built the strongest current BC-aligned shallow simple-support
  comparator;
- pilot 17 showed that the corrected shallow/non-shallow mismatch becomes
  clearly visible around `2..3 MPa`, grows with load, and stays smooth through
  the available high-load range;
- a new exact-load comparison pilot at `4.0`, `7.0`, and `10.0 MPa` reuses the
  same corrected shallow comparator and the same mapped `arrays_nepol_sin(...)`
  logic from the current 6-state system: the mismatch is already moderately
  visible at `4.0 MPa`, becomes clearly visible at `7.0 MPa`, stays clearly
  visible at `10.0 MPa`, and remains dominated by right-edge differences rather
  than by a special new jump localized exactly at the old `4.3434..4.3440 MPa`
  ceiling band.

## Current Next Step
The preferred next move is no longer deeper continuation of the same checked
local theorem branch. That branch is frozen for now at Outcome B on its current
checked boundary.

Operationally, the clean full `simple support / РїРѕРґРІРёР¶РЅС‹Р№ С€Р°СЂРЅРёСЂ` workflow still
keeps the same high-load discipline:

- use `u_z`-scaled continuation with auxiliary arc-like step adaptation as the
  default high-load path for the separate 6-state background family;
- use `fast_u_z_scaled_arc_like_continuation.py` for resumable upward progress
  and `confirm_u_z_scaled_arc_like_continuation.py` only at milestone or audit
  loads;
- keep the clean standalone search `tasks/run_full_simple_support_critical_search.py`
  as the preferred clean mixed-weak search, and keep the preserved hybrid scan
  wrappers only as legacy/exploratory testbenches;
- keep candidate loads reported conservatively as exploratory, supported,
  unstable-rival, or reserve readings rather than as final physical critical
  loads.

The theorem-facing next move is now selection-authority clarification above the
current criterion story, not a new numerical winner search:

- keep `A_ls` as the current repo-selected family, but not as a
  criterion-authoritative family;
- keep `L_red` as the main reduced theorem-facing operator on a fixed selected
  family;
- read `B_red`, `B_mix`, and `rho_R2` as descendants / comparative diagnostics
  on that selected family, not as already proved full replacements for `L_red`;
- use the local Outcome-B quotient result as a caution layer when interpreting
  clean candidate loads and modes;
- treat the current Tikhonov/KKT selector as one exploratory selection rule,
  not as a justified privileged rule;
- do not promote the current truncated-SVD alternative yet, because its
  apparent stability is still cutoff-dependent on the delicate settings;
- prefer a bridge from the checked local quotient theorem back to the global
  reduced criterion story together with an explicit selection-authority question
  over deeper continuation of the same local branch.

## Canonical Runnable Entry Points
Baseline, report, and clean critical-search entry points:

- `tasks/run_axisymmetric_simple_support_background.py`
- `tasks/run_axisymmetric_simple_support_background_report.py`
- `tasks/run_axisymmetric_simple_support_local_branch_following.py`
- `tasks/run_full_simple_support_critical_search.py`

Canonical bounded high-load / diagnosis scripts:

- `proof_pilots/pilot_12_high_load_branch_extension/numerical_extension.py`
- `proof_pilots/pilot_18_revised_analytic_barrier_diagnosis/jacobian_conditioning_check.py`
- `proof_pilots/pilot_18_revised_analytic_barrier_diagnosis/term_balance_check.py`
- `proof_pilots/pilot_19_edge_stretched_simple_support_continuation/edge_stretched_continuation.py`
- `proof_pilots/pilot_20_method_sweep_for_simple_support_ceiling/method_sweep.py`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/u_z_scaled_arc_like_continuation.py`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_u_z_scaled_arc_like_continuation.py`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/confirm_u_z_scaled_arc_like_continuation.py`

For comparison context only, not as the canonical simple-support background
solver path:

- `experiments/supporting/run_supporting_dimensionless_comparison.py`
- `experiments/supporting/run_supporting_determinant_comparison.py`
