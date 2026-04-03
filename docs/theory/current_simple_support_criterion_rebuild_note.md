# Criterion Rebuild Note For Clean Full `simple support / подвижный шарнир`

This note is a criterion-facing audit/rebuild pass after the frozen theorem
line. It does not reopen that line, does not add new theorem-step names, and
does not try again to prove or refute admissibility of `c_temp` or `z_temp`.

Stable object names remain centralized in
`docs/theory/current_simple_support_object_glossary.md`.

## Working Role Of This Note

For the clean full `simple support / подвижный шарнир` criterion-rebuild
branch, this note is the current criterion-facing source-of-truth and
working-order entry point.

Use the following working order:

1. `docs/theory/current_simple_support_criterion_rebuild_note.md`
2. `docs/theory/current_simple_support_status.md`
3. `docs/theory/current_simple_support_object_glossary.md`
4. `docs/theory/current_simple_support_criterion_bridge_note.md`
5. `docs/theory/current_simple_support_final_audit_note.md`
6. `docs/theory/current_simple_support_closed_line_index.md` as archive/frozen-line navigation only

## Criterion Object Hierarchy

For theorem-facing authority on the current clean branch, read the main
criterion objects in the order

```text
L_red > B_red > B_mix.
```

That means:

- `L_red` is the main theorem-facing reduced object on the selected family;
- `B_red` is a boundary descendant on that same selected family;
- `B_mix` is the live basis-level boundary descendant used operationally in the
  current clean search code.

This hierarchy is about criterion authority, not about changing solver
behavior.

## Fixed Background For This Pass

Use the following as fixed project state:

- the old theorem line is frozen/saturated;
- it did not validate the current criterion;
- it did not refute the current criterion either;
- it produced reusable negative knowledge:
  the current criterion still lacks theorem-facing authority to exclude the
  explicit membrane candidate;
- the final sharpened unresolved endpoint is the residual-direction question
  for `z_temp`;
- continuing the same line without genuinely new continuum/equation-level input
  is not the present task.

## Part A. Exact Reconstruction Of The Current Criterion

### A1. What the live clean code currently uses operationally

On the active clean search path, the operational critical-load object is still
the boundary descendant

```text
B_mix,n(q) = B_full,n(q) V_reg,n(q),
```

with the three stored metrics

```text
sigma_raw      = sigma_min(B_mix),
sigma_bal      = sigma_min(diag(1,1,1,2(1+nu),C_twist) B_mix),
sigma_bal_noH  = sigma_min((diag(...) B_mix) without the H-row).
```

Operational mode/load choice in the live clean search is then:

- per mode, choose the best point by minimizing `sigma_bal`;
- across modes, choose the best point again by minimizing `sigma_bal`.

So the raw live selector is still a balanced boundary-only minimum on `B_mix`,
not a direct theorem-facing kernel test on `L_red`.

### A2. What selected family is actually being used

The selected two-mode span is not a raw smallest-singular-vector surrogate.
It is built from the exact center map

```text
C_center(c)
 = [u_s/x^n,
    varphi/x^(n-1),
    u_n/x^n + (lambda_c/n) varphi/x^(n-1),
    psi/x^(n-1) - lambda_c varphi/x^(n-1)] at x = x0,
```

by two constrained KKT/least-squares solves:

```text
c1 = argmin ||A_int c||^2 + reg ||c||^2  subject to C_center c = [1,0,0,0],
c2 = argmin ||A_int c||^2 + reg ||c||^2  subject to C_center c = [0,1,0,0],
```

followed by orthogonalization. The resulting basis columns form `V_reg`.

The live clean code therefore uses the current global weak/KKT-selected
center-regular two-mode family operationally, but in the raw basis `V_reg`.
The theory-facing canonical rebasing is

```text
V_adm = V_reg G_amp^(-1),
```

so the exact selected family is

```text
A_ls = im(V_adm) = im(M_amp).
```

### A2b. What is recipe-dependent and what rebasing does not fix

The current clean selection story splits into four layers:

- amplitude constraints:
  `C_center c = [a_1, a_2, 0, 0]` is fixed by the clean architecture;
- interior weak/KKT selection:
  choosing one 2D span inside that constrained fiber by minimizing
  `||A_int c||^2 + reg ||c||^2`;
- regularization artifact:
  the specific `reg` value, and any nearby pseudoinverse / truncation rule, are
  selector choices rather than theorem-facing consequences of the clean path
  alone;
- post-selection rebasing:
  `V_adm = V_reg G_amp^(-1)` is canonical only after a span has already been
  chosen.

So the current recipe-dependent layer is the selector that chooses `im(V_reg)`
inside the constrained fiber, not the later rebasing. The selected-family
sensitivity audit shows that harmless representative changes are mostly washed
out by canonical rebasing, but nearby `reg` changes are not. The later
selection-rule audit sharpens the same conclusion: the current Tikhonov rule is
too recipe-sensitive for criterion authority, while the apparently stable
truncated-SVD alternative is still cutoff-dependent enough that it should not
yet be promoted.

### A2c. Requirements for a criterion-authoritative selector

A selector should be called criterion-authoritative on the present clean branch
only if requirements of four different kinds are met.

Structural/invariance requirements:

- it must preserve the fixed clean amplitude/regularity constraints
  `C_center c = [a_1, a_2, 0, 0]`;
- it must remain compatible with the object hierarchy
  `A_ls -> L_red -> B_red -> B_mix`, so descendants are not silently promoted
  above the reduced operator;
- it must be invariant under harmless representative-choice, normalization, and
  orthogonalization changes that do not alter the underlying selected span;
- canonical rebasing must not be the only reason the output looks stable: the
  chosen span itself must be stable, not only its coordinates after rebasing.

Numerical robustness requirements:

- the selected span should not drift materially under small admissible
  Tikhonov-style `reg` changes;
- the selected span should not depend qualitatively on arbitrary SVD cutoff
  tuning;
- nearby admissible selector choices should not change the qualitative
  near-pair `n=7` / `n=8` reading on the checked dense windows/settings.

Theorem-facing authority requirements:

- the selector should come from a theorem-facing weak/KKT principle, or from a
  local-to-global selected-family theorem, rather than only from a numerical
  recipe;
- it should explain why one 2D span is privileged inside the clean constrained
  fiber;
- it should remain compatible with `L_red` as the main criterion-facing object,
  not replace that hierarchy by a boundary-only or tuning-based rule.

Convenience-only properties that are not enough by themselves:

- small identity residuals `C_amp V_adm - I` and `C_reg V_adm`;
- moderate `cond(G_amp)`;
- a numerically calm or visually appealing local window;
- a winner ordering that happens to look plausible.

### A2d. Current selector assessment against those requirements

Current Tikhonov/KKT selector:

- passes / partially supports:
  the clean amplitude constraints, the current object hierarchy, the clean
  rebasing identities, and near-invariance under harmless representation
  changes after rebasing;
- fails:
  stability under small admissible `reg` changes, theorem-facing derivation of
  a privileged selector, and qualitative near-pair robustness strong enough for
  criterion authority.

Current truncated-SVD alternative:

- passes / partially supports:
  the same clean identities and, on some checked settings, a numerically calmer
  selected-family reading than the Tikhonov ladder;
- fails:
  cutoff independence, theorem-facing derivation of a privileged selector, and
  enough cross-rule agreement to justify promotion as the new baseline.

Canonical rebasing:

- passes / partially supports:
  exact coordinate normalization on a chosen span and numerical washing-out of
  harmless representative changes;
- does not supply criterion authority by itself:
  it is a post-selection step, so it cannot by itself turn a nearby
  recipe-dependent selected span into a canonical selector.

### A2e. Candidate theorem-facing selector principles now on the table

The current repo evidence leaves several candidate selector-principle programs
on the table. None is yet closed enough to promote.

Read against the requirement list in A2c, the weak/KKT and local-to-global
routes are the only candidates that presently look capable in principle of
satisfying both the structural/hierarchy conditions and the theorem-facing
authority condition. The trace-plane-first route presently looks insufficient by
itself, the variational/minimal-energy route remains more speculative because no
canonical functional is yet available, and `no justified selector yet` is the
current conservative fallback rather than a selector principle that could be
promoted.

1. Weak/KKT-selected global family principle

- privileged object:
  a theorem-facing globally selected 2D family inside the clean constrained
  fiber, justified by a genuine weak/interior optimality rule;
- why it is relevant:
  it is the closest conceptual upgrade of the current live architecture, which
  already chooses a family through an interior weak residual;
- evidence that supports it:
  the current clean hierarchy already separates amplitude constraints, interior
  selection, and post-selection rebasing; harmless representation changes are
  mostly washed out; `L_red` is already the main object on a fixed selected
  family;
- evidence that does not yet support it:
  the current Tikhonov rule is still `reg`-sensitive, so the numerical recipe
  is not yet a theorem-facing selector;
- next bottleneck:
  formulate and justify a weak/KKT principle that privileges one span
  independently of the present tuning recipe, and check that it satisfies the
  selector-authority requirements;
- current read:
  promising and structurally compatible, but requires new theorem work.

2. Local-to-global selected-family principle

- privileged object:
  a global selected family canonically lifted from the correct local selected
  object or selected shadow/quotient object;
- why it is relevant:
  the clean branch already has strong local checked data and an explicit
  bridge question between local selected information and the global reduced
  operator story;
- evidence that supports it:
  the selected trace plane is closed, the local quotient boundary is explicit,
  and the project already tracks the bridge from local data back to `A_ls` and
  `L_red`;
- evidence that does not yet support it:
  no intrinsic higher-order local selector beyond the checked quotient is
  closed, and no canonical lift theorem is available;
- next bottleneck:
  close a genuinely selected local object and prove that it lifts uniquely to a
  privileged global family;
- current read:
  promising but currently unsupported beyond structural compatibility.

3. Trace-plane-first principle

- privileged object:
  a selector fixed first at the selected trace/amplitude plane and then lifted
  canonically to a global family;
- why it is relevant:
  the leading trace plane is one of the cleanest currently closed pieces of the
  branch;
- evidence that supports it:
  `J_0 = C_center` and `J_0(A_ls) = im(D_amp)` are already closed on the
  current repo-selected family;
- evidence that does not yet support it:
  the trace plane alone does not yet determine a unique privileged global span;
  many global families can share the same leading trace data;
- next bottleneck:
  derive a theorem that turns selected trace data into a unique canonical
  global lift rather than only a family overclass;
- current read:
  useful ingredient, but mismatched as a standalone selector principle.

4. Variational/minimal-energy selector principle

- privileged object:
  a family singled out by a canonically justified energy, coercivity, or
  reduced functional;
- why it might be relevant:
  it could provide the kind of theorem-facing authority and invariance that the
  recipe-based Tikhonov norm currently lacks;
- evidence that supports it:
  the present solver already uses a minimization-style rule, so a truly
  canonical variational principle would conceptually fit the architecture;
- evidence that does not yet support it:
  no canonically justified energy/coercivity functional has yet been derived
  for the selector role on this clean boundary;
- next bottleneck:
  derive and justify an actual canonical functional and show that its minimizer
  determines a privileged 2D family;
- current read:
  currently unsupported and more speculative than the weak/KKT or
  local-to-global routes.

5. No justified selector yet

- privileged object:
  none at present; this is the conservative status-only fallback position;
- why it is relevant:
  it matches the current audit evidence and prevents the repo from overclaiming
  criterion authority before a selector principle is genuinely derived;
- evidence that supports it:
  the present selector-authority requirements are explicit, while the checked
  Tikhonov and truncated-SVD rules both fail them in different ways;
- evidence that does not yet support promotion beyond fallback:
  it does not itself produce a privileged reduced family;
- next bottleneck:
  choose and develop one theorem-facing selector principle, or remain on this
  conservative language;
- current read:
  this is the correct current source-of-truth position.

### A2f. Weak/KKT route: current numerical surrogate versus genuine theorem-facing target

The current weak/KKT-like selector in the live code can now be written
explicitly.

For the two center-amplitude right-hand sides

```text
d_1 = [1,0,0,0],    d_2 = [0,1,0,0],
```

the repository solves, separately for `j = 1, 2`,

```text
min_c  ||A_int c||^2 + reg ||c||^2
subject to
      C_center c = d_j.
```

Equivalently, it solves the KKT block system

```text
[A_int^T A_int + reg I   C_center^T] [c_j ]   [0  ]
[C_center                0         ] [mu_j] = [d_j].
```

After that, the current recipe still performs two extra numerical choices:

- normalize each constrained solution `c_j / ||c_j||`;
- orthogonalize the second constrained solution against the first.

Only then does it form

```text
V_reg = [c_1, c_2],
V_adm = V_reg (C_amp V_reg)^(-1).
```

So the current live selector splits into four pieces:

- hard constraints:
  `C_center c = d_j`;
- weak/interior flavor:
  preference for small `||A_int c||`;
- recipe-level artifact:
  the Euclidean coefficient penalty `reg ||c||^2`, the chosen `reg`, and the
  later normalization / orthogonalization order;
- post-selection rebasing:
  `V_adm = V_reg (C_amp V_reg)^(-1)`.

What the current recipe captures correctly:

- the selected family should live inside the clean constrained fiber;
- the selector should privilege representatives that are weakly favorable in
  the interior, not merely convenient boundary traces;
- the selected family should remain compatible with `L_red` as the main reduced
  criterion-facing object.

What it does not yet justify:

- why the Euclidean `reg ||c||^2` term is canonically the right weak selector;
- why the chosen `reg` value does not matter in the delicate settings;
- why solving separately for `d_1`, `d_2` and then normalizing /
  orthogonalizing is the theorem-facing way to select the span;
- why the resulting span should be privileged beyond one numerical recipe.

A genuine theorem-facing weak/KKT selector principle would need to say
something stronger:

- for each admissible leading amplitude datum `a in R^2`, there exists a
  canonically selected weak/interior representative
  `c_weak(a)` in the clean constrained class;
- the selected map `a -> c_weak(a)` defines one privileged 2D family
  `A_weak = {c_weak(a)}` inside the clean constrained fiber;
- that family is invariant under harmless representation changes and does not
  depend on arbitrary `reg`, cutoff, or normalization choices;
- the family is justified by a theorem-facing weak/interior optimality
  statement rather than by a tuning-dependent numerical surrogate.

So the weak/KKT route does not ask merely for a nicer recipe. It asks for a new
theorem-facing selected-representative principle.

Exact next bottleneck on that route:

- identify the correct theorem-facing global constrained class on which the
  weak selector should act;
- identify the canonical weak/interior optimality statement or functional;
- prove existence/uniqueness/canonicity of the selected representative
  `c_weak(a)` for each amplitude datum;
- prove that the resulting 2D span is stable enough to satisfy the
  selector-authority requirements;
- only then reinterpret the present Tikhonov selector, if possible, as a
  numerical surrogate/approximation of that theorem-facing weak/KKT family.

### A2g. Weak/KKT theorem-readiness checklist and verdict

Current candidate theorem target:

- for fixed `(n,q)`, define a theorem-facing selected-representative map
  `S_weak,n,q : R^2 -> A_con^th,n(q)`;
- equivalently, read the domain as the selected trace plane `im(D_amp,n(q))`;
- require `J_0(S_weak(a)) = D_amp a` in the intended theorem-facing sense;
- require the image
  `A_weak,n(q) := im(S_weak,n,q)`
  to be one privileged 2D selected family inside the clean constrained class.

Current constrained-class picture:

- already explicit numerically:
  the weighted trial coefficient space
  `X_trial,n = R^N`,
  the explicit center matrix `C_center = [C_amp; C_reg]`,
  the code-level center-regular class
  `W_reg,n(q) = {c in X_trial,n : C_reg,n(q) c = 0}`,
  and the current repo-selected family
  `A_repo,n(q) = im(V_adm,n(q))`;
- intended theorem-facing target:
  a clean admissible / center-regular constrained class
  `A_con^th,n(q)` inside the intended clean tangent universe
  `A_full^th,n(q)`;
- still only implicit/schematic:
  the repo does not yet package `A_con^th,n(q)` as an independently closed
  continuum object strong enough to serve as the codomain of `S_weak,n,q`.

Exact weak/interior principle still missing:

- the current surrogate uses
  `||A_int c||^2 + reg ||c||^2`;
- what is still not specified theorem-facingly is the canonical weak/interior
  stationarity, variational, or optimality statement that should single out
  `S_weak,n,q(a)`;
- so the theorem target is still missing the very rule that would replace
  arbitrary `reg`, cutoff, normalization, and orthogonalization choices.

Authority properties that the theorem would need:

- existence of `S_weak,n,q(a)` for every admissible amplitude datum `a`;
- uniqueness/canonicity of the selected representative;
- exact image a privileged 2D family, not just an arbitrary set of good
  representatives;
- invariance under harmless representation choices;
- independence from arbitrary regularization/cutoff tuning;
- compatibility with the hierarchy
  `A_ls -> L_red -> B_red -> B_mix`;
- selector stability strong enough not to alter the qualitative near-pair
  reading under nearby admissible choices.

Failure map / unresolved prerequisites:

- constrained-class failure:
  `A_con^th,n(q)` is not yet independently closed sharply enough, so the
  codomain of the theorem target is still schematic;
- weak-principle failure:
  no canonical weak/interior optimality principle has yet been identified, so
  the theorem does not yet know what property characterizes `S_weak,n,q(a)`;
- uniqueness failure:
  without that principle, uniqueness/canonicity is not yet well-posed;
- trace-lift failure:
  the selected trace data is closed, but by itself it still does not determine
  a unique global family;
- surrogate-link failure:
  there is not yet a theorem saying the present Tikhonov rule converges to or
  approximates the theorem-facing weak selector;
- authority failure:
  even after choosing a selector, criterion authority would still need the
  selector-authority properties above.

Readiness verdict:

- `B. almost ready, but one or two lower-level clarifications should be done first.`

Reason:

- the candidate theorem route is now specified well enough to identify the
  right proof *kind*, but not yet sharply enough to start the proof itself;
- the two prerequisite clarifications are:
  1. close the theorem-facing constrained class
     `A_con^th,n(q)` on which the selector should act;
  2. identify the canonical weak/interior optimality statement that defines
     `S_weak,n,q(a)` without arbitrary tuning choices.

After those two clarifications, a real proof attempt would become the right
next step.

### A2h. Clarifying the theorem-facing constrained class `A_con^th,n(q)`

Candidate codomain meanings currently on the table:

1. `A_con^th,n(q) = A_full^th,n(q)`:

- what its elements would be:
  the full theorem-facing clean admissible / center-regular tangent objects on
  the present clean branch;
- how it differs from nearby repo objects:
  it is not the weighted trial coefficient space `X_trial,n = R^N`, not the
  numerical center-regular slice
  `W_reg,n(q) = {c in X_trial,n : C_reg,n(q) c = 0}`, and not the exact current
  selected family `A_repo,n(q) = A_ls,n(q) = im(V_adm,n(q))`;
- current support:
  this is the most natural ambient theorem-facing class if one wants the weak
  selector to choose representatives inside the full clean admissible fiber;
- current obstacle:
  `A_full^th,n(q)` is still not packaged sharply enough on the present repo
  boundary to serve directly as the fixed codomain of `S_weak,n,q`.

2. `A_con^th,n(q)` as a selected-trace constrained slice of the full class:

- what its elements would be:
  theorem-facing global clean admissible objects in the full class whose
  selected leading-center trace lands in the already closed plane
  `im(D_amp,n(q))`, or fiberwise in the affine slice
  `J_0(c) = D_amp a`;
- how it differs from nearby objects:
  unlike `X_trial` and `W_reg`, this is meant to be a continuum
  theorem-facing constrained class; unlike `A_repo = A_ls`, it is not already
  the numerically selected 2D family, but the larger clean constrained fiber in
  which a theorem-facing selector would pick one privileged representative for
  each amplitude datum;
- current support:
  this is the most natural codomain for a future weak/KKT map
  `S_weak,n,q`, because the domain is already read as amplitude data or,
  equivalently, the selected trace plane `im(D_amp)`;
- current obstacle:
  it still inherits the unresolved packaging of `A_full^th,n(q)` itself.

3. `A_con^th,n(q)` as a theorem-facing selected overclass:

- what its elements would be:
  theorem-facing selected clean objects above the exact repo-selected family,
  closer in meaning to the current selected-family object `A_ls` than to the
  raw full admissible class;
- the nearest current named candidate:
  `A_sel^{th,cand}`, the strongest currently justified theorem-facing candidate
  class above the exact repository-selected family;
- how it differs from nearby objects:
  it is broader than the exact numerical family `A_repo = A_ls`, but already
  narrower and more selected than the raw full admissible class;
- current support:
  this route matches the current evidence that the selected trace plane
  `J_0(A_ls) = im(D_amp)` is closed and that the best theorem-facing comparison
  object is now likely to be selected rather than fully raw;
- current obstacle:
  `A_sel^{th,cand}` is still only a structural candidate class, not yet a
  closed intrinsic codomain licensed as the exact target of the weak selector.

4. `A_con^th,n(q)` as a local-to-global lifted selected class:

- what its elements would be:
  global clean objects obtained as the canonical lifts of a genuinely closed
  local selected object or selected trace object;
- how it differs from nearby objects:
  it is not merely the trace plane `im(D_amp)` itself, but the global class
  determined by such local selected data;
- current support:
  the selected trace plane is already closed and so this route remains a live
  structural possibility;
- current obstacle:
  there is still no closed intrinsic local selected object with a canonical
  global lift, so this route cannot yet fix the codomain sharply.

Conservative fallback candidate:

- `A_con^th,n(q)` still not fixed:
  this remains the correct fallback language if one insists that only a fully
  closed theorem-facing codomain may be named;
- why that fallback is no longer the whole story:
  the current repo evidence narrows the field more than that, because the raw
  code-level spaces and the exact repo-selected family are already ruled out as
  the intended codomain.

Best current codomain verdict:

- `B. A_con^th,n(q)` is narrowed to a short list of 2 plausible candidates:
  1. primarily, the selected-trace constrained slice of the full theorem-facing
     clean admissible class;
  2. secondarily, a theorem-facing selected overclass closer to `A_ls`, with
     `A_sel^{th,cand}` the nearest current structural placeholder;
- why not `A` fixed sharply:
  the first route still depends on a not-yet-independently-closed ambient full
  admissible class, while the second route still depends on a not-yet-closed
  intrinsic selected local/global object;
- why not `C` still fully schematic:
  the codomain can already be narrowed away from `X_trial`, `W_reg`, the exact
  numerical family `A_repo = A_ls`, and the trace plane alone.

### A2i. Choosing the preferred codomain route for `A_con^th,n(q)`

The two live codomain routes should now be compared as follows.

Route 1: selected-trace constrained slice of the full admissible class

- what this codomain contains:
  theorem-facing global clean admissible objects in the intended full class
  whose selected leading-center trace lies in `im(D_amp,n(q))`, or fiberwise
  satisfies `J_0(c) = D_amp a`;
- relation to the main nearby objects:
  it is a constrained slice inside `A_full^th,n(q)`, it contains the
  amplitude/trace fiber in which a selector should choose one privileged
  representative, it is larger than `A_ls = A_repo`, and it uses
  `im(D_amp,n(q))` as the fixed trace datum rather than as the whole codomain;
- why it is attractive:
  this route is the closest theorem-facing analogue of the current live KKT
  geometry, where fixed center/amplitude data leave a large fiber and the weak
  solve selects one representative from that fiber;
- what already supports it:
  the source-of-truth code path, the pilot-23 affine-fiber reading, and the
  exact trace identity `J_0(A_ls) = im(D_amp)` all fit this ambient-fiber then
  selected-representative picture;
- what still blocks it:
  the ambient full theorem-facing admissible/constrained class is not yet
  packaged sharply enough on the present branch, so the slice cannot yet be
  written as a fully closed codomain.

Route 2: theorem-facing selected overclass / local-to-global selected class

- what this codomain contains:
  theorem-facing selected clean objects above the exact repo-selected family,
  with `A_sel^{th,cand}` the nearest current structural placeholder and a
  future local-to-global selected lift class the stronger version;
- relation to the main nearby objects:
  it lies closer to `A_ls = A_repo` than to the full admissible class, uses the
  selected trace plane `im(D_amp)` as part of a selected-object story, and
  would make the codomain itself already partly selected before the weak/KKT
  selector acts;
- why it is attractive:
  it matches the current evidence that the selected trace plane is closed and
  that a raw unrestricted local comparison object is likely too broad;
- what already supports it:
  `A_sel^{th,cand}`, `J_0(A_ls) = im(D_amp)`, and the local-to-global menu from
  pilot 23 all keep this route live as a plausible theorem program;
- what still blocks it:
  there is still no closed intrinsic local selected object with a canonical
  global lift, so this route currently depends on a stronger unresolved
  selected-object theorem than the weak/KKT codomain choice itself.

Comparison as future weak/KKT targets:

- closeness to the live weak/KKT route:
  Route 1 is closer, because the present surrogate already acts by selecting an
  `H`-minimal representative inside a larger fixed-center fiber;
- compatibility with the hierarchy `A_ls -> L_red -> B_red -> B_mix`:
  both routes can feed that hierarchy, but Route 1 preserves the clean split
  between ambient codomain and selected image more directly;
- dependence on unresolved ambient objects:
  Route 1 depends on sharpening `A_full^th`, but does not require a separate
  intrinsic selected local object first;
- dependence on unresolved local selected objects / lifts:
  Route 2 depends essentially on exactly that still-missing local selected
  object and canonical lift;
- support for a future selector-authority theorem:
  Route 1 is more direct, because it frames the theorem as existence,
  uniqueness, and canonicity of one weak-selected representative inside a
  larger admissible constrained fiber, rather than baking selectedness into the
  codomain itself.

Route-preference verdict:

- `A. Prefer the selected-trace constrained slice of the full admissible class
  as the main codomain target for the future weak/KKT selector.`

Justification:

- this route best matches the current live KKT architecture and keeps the weak
  selector theorem conceptually sharp: the codomain should be the ambient clean
  constrained fiber with fixed selected trace, while the selected 2D family is
  the image produced by the theorem rather than built into the codomain in
  advance;
- the selected-overclass / local-to-global route remains live, but it now reads
  better as a neighboring theorem program or possible later comparison theorem
  than as the primary codomain of `S_weak,n,q`.

Exact next bottleneck implied by that choice:

- sharpen the intended full theorem-facing admissible/constrained class enough
  to make the selected-trace slice
  `{c in A_full^th,n(q) : J_0(c) = D_amp a}`
  a clean codomain, and only then formulate the canonical weak/interior
  optimality statement on that codomain.

### A2j. Clarifying the ambient full admissible/constrained class `A_full^th,n(q)`

The preferred codomain route now pushes the next clarification one layer
upward: the ambient full class itself.

Candidate ambient meanings currently visible in the repo:

1. `A_full^th,n(q)` as the full clean admissible / center-regular tangent class
   of the continuous mixed problem

- what its elements are supposed to be:
  theorem-facing global clean tangent objects in the current mixed variables
  satisfying the clean mixed equations, the current clean simple-support
  boundary-condition meaning, and the center regularity/admissibility
  conditions needed for a finite selected leading-center trace;
- how it differs from nearby explicit objects:
  it is not the coefficient universe `X_trial,n = R^N`, not the ansatz-level
  center-regular slice `W_reg,n(q) = {c in X_trial,n : C_reg,n(q) c = 0}`,
  not the exact selected family `A_repo = A_ls`, and not the selected trace
  plane `im(D_amp)`;
- what is already explicit:
  the branch already fixes the governing mixed equations, the boundary meaning,
  the principal scaling orders, and the exact selected trace plane on `A_ls`;
- what is still only implicit:
  the full continuum/local admissible class itself is not yet packaged as an
  independently closed object with its higher-order formal continuation and
  theorem-facing trace regularity written sharply enough.

2. Weighted-trial / coefficient surrogate class

- what its elements are:
  the explicit finite-dimensional coefficient vectors in
  `X_trial,n = R^N`, together with the largest explicit ansatz-level
  center-regular slice `W_reg,n(q)`;
- why it is useful:
  this is the strongest current exact numerical container for the live
  assembly, center constraints, and KKT-selected family;
- why it is not the intended ambient class:
  it is discretization-dependent, basis-dependent, and finite-dimensional, so
  it cannot by itself serve as the theorem-facing ambient full admissible class
  for the weak/KKT program.

3. Selected-trace-compatible ambient reading already implicit in the repo

- what its elements are supposed to be:
  full clean admissible / center-regular continuum objects for which the
  finite leading-center trace `J_0` is meaningful and whose selected-trace
  slice against `im(D_amp)` can be formed;
- why this is the strongest current narrowed reading:
  the source-of-truth files already close `J_0 = C_center` and
  `J_0(A_ls) = im(D_amp)` on the weighted-ansatz selected boundary, so any
  ambient class serving the preferred codomain route must at least support that
  trace/slicing language in theorem-facing form;
- what is still missing:
  the repo has not yet closed the continuum theorem saying exactly on which
  full admissible class that same finite trace is defined and sufficiently
  stable for the codomain slice.

4. Conservative fallback: `A_full^th,n(q)` still schematic

- why this fallback remains available:
  the article-level local formal-completeness packaging is still unfinished,
  and the current exact `J_0` trace map is still closed only on the
  weighted-ansatz/repo-selected side;
- why it is no longer the best current read:
  the repo evidence now narrows the intended ambient role much more than a
  purely schematic placeholder, because the continuous ambient class must at
  least be a clean admissible / center-regular class compatible with the
  selected-trace slicing route.

Minimum structure the ambient class must carry:

- it must be a theorem-facing class for the current clean mixed equations and
  the current clean boundary-condition meaning;
- it must encode the center regularity/admissibility conditions that distinguish
  the ambient full class from raw trial coefficients;
- it must support a finite leading-center trace map `J_0` strong enough that
  slicing by `J_0(c) = D_amp a` is meaningful;
- it must be broad enough that the future weak/KKT selector chooses a
  representative from a larger admissible constrained fiber, rather than merely
  reparametrizing `A_ls`;
- it must remain compatible with the current criterion-facing hierarchy
  `A_ls -> L_red -> B_red -> B_mix`.

Ambient-class verdict:

- `B. A_full^th,n(q)` is narrowed substantially but still not sharp enough.

Justification:

- the current best source-of-truth reading is now clear enough to say that
  `A_full^th` should mean the full clean admissible / center-regular tangent
  class of the continuous mixed problem, not any of the finite-dimensional
  surrogates and not the already selected family;
- but it is still not closed sharply enough, because the repo does not yet
  package the full continuum/local class together with its higher-order formal
  continuation/completeness and theorem-facing `J_0` trace regularity strongly
  enough for the preferred codomain slice
  `{c in A_full^th,n(q) : J_0(c) = D_amp a}`
  to be written as a finished theorem-facing codomain.

Exact remaining obstacle:

- the missing step is not more selector tuning. It is a continuum/local
  packaging step: close the full admissible center-regular class and its trace
  regularity sharply enough that the selected-trace slice inside `A_full^th`
  becomes a clean theorem-facing codomain for the weak/KKT route.

### A2k. Continuum/local class-plus-trace packaging for `A_full^th,n(q)` and `J_0`

The preferred codomain route can now be packaged more sharply by pairing the
ambient class with the finite trace it needs.

Ambient class package:

- intended ambient object:
  `A_full^th,n(q)` should be the full continuum/local clean admissible /
  center-regular tangent class for the current mixed equations and the current
  clean simple-support boundary meaning;
- its role:
  this is the ambient theorem-facing class before any weak/KKT selection is
  imposed, and the future selector should choose one representative from a
  larger constrained fiber inside this class;
- what it excludes:
  it should not be read as `X_trial,n`, not as `W_reg,n(q)`, not as the exact
  repo-selected family `A_repo = A_ls`, and not as the selected trace plane.

Trace package:

- intended theorem-facing trace object:
  `J_0` should be the finite leading-center jet map on `A_full^th,n(q)`,
  retaining the two leading amplitudes and the two leading regularity-defect
  rows in one 4D trace object;
- current exact weighted-ansatz realization:
  on the present repository boundary this same finite trace is represented
  exactly by `J_0 = C_center`;
- why this is the right trace role:
  `J_amp` keeps only amplitudes, while `J_0` also remembers the leading
  regularity-defect rows that distinguish raw center data from the selected
  regularity-zero slice.

What is already closed only on the weighted-ansatz / selected-family side:

- `J_0 = C_center` is exact as a finite leading-center-jet extractor on the
  weighted-trial boundary;
- `J_0(A_ls) = im(D_amp)` is exact and basis-independent on the current
  selected family;
- `J_0|_{A_ls}` is bijective with inverse given by the selected lift.

What still must be upgraded to the continuum/local level:

- the repo still lacks the theorem-facing statement that the same finite
  leading-center jet is well-defined on all of `A_full^th,n(q)`;
- equivalently, it is not yet closed on which ambient admissible class the
  finite trace `J_0(c)` exists with enough regularity for the selected-trace
  slice
  `{c in A_full^th,n(q) : J_0(c) in im(D_amp,n(q))}`
  to be a clean codomain;
- this upgrade depends on a higher-order local continuation/completeness layer,
  because without that layer the continuum/local class-plus-trace package is
  still only exact on the weighted-ansatz boundary.

Main remaining gap after this pass:

- the dominant remaining obstacle is one combined continuum/local
  trace-regularity gap:
  extend the current exact finite trace `J_0 = C_center` from the
  weighted-ansatz / selected-family side to the full ambient class
  `A_full^th,n(q)` with enough local continuation/completeness to make the
  selected-trace slice cleanly meaningful.

Codomain-readiness verdict after this packaging pass:

- `B. the preferred codomain is much sharper, but one explicit continuum/local
  trace-regularity gap still remains.`

Justification:

- `A_full^th` and `J_0` can now be read together rather than separately:
  the ambient object is the full clean admissible / center-regular tangent
  class, and the trace object is the finite leading-center jet that should cut
  out the preferred selected-trace slice;
- but the current exact trace identities are still closed only on the
  weighted-ansatz / selected-family boundary, not yet on the full continuum
  ambient class, so the codomain is not proof-ready until that one combined
  trace/local upgrade is closed.

### A2l. `J_0` theorem-facing extension / trace-regularity task

Current exact closure that should not be overstated:

- on the weighted-ansatz / selected-family boundary one has the exact finite
  trace map `J_0 = C_center`;
- on that same boundary one has the exact identity
  `J_0(A_ls) = im(D_amp)`;
- and the restriction `J_0|_{A_ls}` is an exact bijection with inverse given by
  the selected lift.

Intended theorem-facing extension:

- on the ambient continuum/local class `A_full^th,n(q)`, `J_0` should mean the
  finite leading-center jet that keeps the same four coordinates already
  visible on the weighted ansatz:
  the two leading amplitudes and the two leading regularity-defect rows;
- equivalently, the theorem-facing extension should reduce to `C_center` on the
  current weighted-trial boundary, while being defined intrinsically on all of
  `A_full^th,n(q)`.

What is still missing:

- a theorem-facing statement that every
  `c in A_full^th,n(q)` admits those same four leading-center quantities in a
  well-defined finite trace;
- the local continuation/completeness input needed to ensure that the ambient
  admissible / center-regular class really has enough near-center structure for
  that trace to exist and be stable;
- therefore also the ambient selected-trace codomain statement
  `{c in A_full^th,n(q) : J_0(c) in im(D_amp,n(q))}`.

Best current read of the remaining obstacle:

- this is no longer a broad selector-level ambiguity;
- it is also not merely a notation/definition gap, because the trace extension
  depends on local continuation/completeness strong enough to justify those
  four leading-center quantities on the ambient class;
- the remaining obstacle is best read as one combined local/trace theorem task:
  extend the exact finite leading-center jet `J_0 = C_center` from the current
  weighted-ansatz / selected-family boundary to all of `A_full^th,n(q)` with
  enough local continuation/completeness and trace regularity that slicing by
  `J_0(c) in im(D_amp,n(q))` becomes cleanly meaningful.

`J_0`-gap verdict:

- `B. the J_0 gap is narrowed to one precise local/trace theorem task.`

Justification:

- the finite trace itself is no longer vague: the repo now has a stable
  candidate meaning for `J_0`, and the exact selected-family identities already
  say what the trace must look like on the current operational boundary;
- what is still missing is a single theorem-facing upgrade carrying that same
  finite trace from the weighted-ansatz / selected-family side to the full
  ambient class `A_full^th,n(q)`, and that upgrade necessarily bundles trace
  existence with the local continuation/completeness that supports it.

### A2m. Sharp formulation of the remaining `J_0` local/trace theorem task

The next theorem-facing task can now be stated sharply enough to stand on its
own as the next direct theorem target.

Candidate theorem statement:

- for each fixed `(n,q)`, there exists a theorem-facing finite leading-center
  jet map
  `J_0^th,n,q : A_full^th,n(q) -> R^4`
  such that for every
  `c in A_full^th,n(q)`,
  the four leading-center quantities
  `(U0, P0, N0 + (lambda_c / n) P0, Y0 - lambda_c P0)` are well-defined and
  determine `J_0^th,n,q(c)`;
- on the overlap with the current weighted-trial boundary, this theorem-facing
  map agrees with the exact operational trace
  `J_0 = C_center`;
- consequently, the preferred codomain
  `A_con^th,n(q) = {c in A_full^th,n(q) : J_0^th,n,q(c) in im(D_amp,n(q))}`
  is a cleanly defined theorem-facing class.

Hypotheses that must be explicit in that task:

- ambient class hypothesis:
  `A_full^th,n(q)` is the intended clean admissible / center-regular tangent
  class for the current mixed equations and the current clean simple-support
  boundary meaning;
- local scaling hypothesis:
  members of `A_full^th,n(q)` admit the current near-center scaling orders used
  throughout the clean branch;
- finite-jet existence hypothesis:
  the leading coefficients `U0, N0, P0, Y0` exist and are uniquely determined
  for each `c in A_full^th,n(q)`;
- compatibility hypothesis:
  those leading coefficients satisfy the same trace normalization convention as
  the current `J_0 = C_center` story, so no alternative richer-local chart is
  silently substituted;
- local continuation/completeness hypothesis:
  the ambient class has enough local continuation/completeness that the finite
  leading-center jet is stable under the current continuous mixed equations and
  is not merely an ansatz artifact.

Exact conclusion needed for the weak/KKT codomain:

- existence and well-definedness of `J_0^th,n,q` on all of `A_full^th,n(q)`;
- agreement with `C_center` on the current weighted-trial overlap;
- preservation of the current selected-trace coordinates, so the meaning of
  `im(D_amp,n(q))` is unchanged;
- enough regularity to make the slice
  `J_0^th,n,q(c) in im(D_amp,n(q))`
  meaningful as a theorem-facing codomain condition.

Role of local continuation / completeness:

- it is not an optional side remark;
- it is the ingredient that turns the four leading-center quantities from an
  ansatz-level exact trace into a theorem-facing trace on the whole ambient
  class;
- for that reason the current best read is that local continuation/completeness
  belongs inside the proof burden of this `J_0` theorem task, not as an
  unrelated later add-on.

What this theorem would solve, and what it would not:

- it would solve the codomain-meaning problem for the preferred weak/KKT route;
- it would not yet prove the weak/KKT selected-representative theorem;
- it would not yet prove selector authority or losslessness of `A_ls`;
- it would not by itself reopen or settle the frozen theorem line.

Sharpness verdict:

- `A. the remaining J_0 task is now sharp enough for a direct theorem attempt.`

Justification:

- the task now has a clear domain (`A_full^th,n(q)`), a clear target (`R^4`),
  explicit trace coordinates, an explicit compatibility requirement with
  `C_center`, and an explicit codomain consequence for
  `{c : J_0(c) in im(D_amp)}`;
- what remains hard is proof difficulty, not statement ambiguity.

### A2n. Direct proof attempt for the remaining `J_0` local/trace theorem

Theorem attempted in theorem-style form:

- fix `(n,q)`;
- domain:
  `A_full^th,n(q)`, the intended ambient clean admissible / center-regular
  tangent class;
- codomain:
  `R^4`;
- map to define:
  `J_0^th,n,q(c) := [U0, P0, N0 + (lambda_c / n) P0, Y0 - lambda_c P0]`,
  where `(U0, N0, P0, Y0)` are the leading-center coefficients of `c` in the
  current near-center scaling orders;
- desired conclusion:
  `J_0^th,n,q` is well-defined on all of `A_full^th,n(q)`, agrees with
  `C_center` on the weighted-trial overlap, and therefore makes
  `A_con^th,n(q) = {c in A_full^th,n(q) : J_0^th,n,q(c) in im(D_amp,n(q))}`
  a clean theorem-facing codomain.

Proof-attempt breakdown:

1. Compatibility with the current ansatz-level trace on the weighted-trial
   overlap:

- this part is already closed at the current repo level;
- by the exact weighted-ansatz trace theorem,
  `J_0 = C_center`, `J_0(A_ls) = im(D_amp)`, and `J_0|_{A_ls}` is bijective
  onto `im(D_amp)`;
- so if `J_0^th,n,q` were already defined on `A_full^th,n(q)` and restricted to
  the current weighted-trial overlap, the required compatibility clause would
  be exact and not merely heuristic.

2. Codomain consequence once the map exists:

- this part is formal once the previous clause is available;
- if `J_0^th,n,q : A_full^th,n(q) -> R^4` is well-defined and `im(D_amp,n(q))`
  remains the already closed selected trace plane, then the slice
  `J_0^th,n,q(c) in im(D_amp,n(q))`
  is a meaningful codomain condition.

3. Existence / well-definedness of the four leading-center quantities on
   `A_full^th,n(q)`:

- the proof attempt stops here first;
- the repo does not yet contain a closed theorem that every
  `c in A_full^th,n(q)` admits a unique current-normalized leading-center
  quadruple `(U0, N0, P0, Y0)` in the current scaling class;
- what is closed instead is narrower:
  the exact weighted-ansatz trace extractor on the current selected family, the
  symbolic leading local relations in the same `J_0` coordinates, and the
  richer-trace reconciliation back to those coordinates;
- none of those statements yet upgrades ambient `A_full^th,n(q)` objects to a
  finished theorem-facing finite-jet extraction theorem.

4. Uniqueness of the four leading-center quantities:

- this is not reached as a separate closed step;
- it is bundled with the same missing ambient finite-jet extraction theorem,
  because uniqueness is only meaningful after existence and current-normalized
  identification on `A_full^th,n(q)` are available.

Exact first blocking lemma:

- Ambient finite-jet extraction lemma for the current `J_0` coordinates:
  for every `c in A_full^th,n(q)`, there exists a unique quadruple
  `(U0, N0, P0, Y0)` in the current near-center scaling class such that
  the four coordinates
  `[U0, P0, N0 + (lambda_c / n) P0, Y0 - lambda_c P0]`
  are well-defined, depend only on `c`, are compatible with the current clean
  mixed equations, and agree with `C_center c` on the weighted-trial overlap.

Why this lemma blocks the theorem:

- without it, the ambient map `J_0^th,n,q` is not yet defined on all of
  `A_full^th,n(q)`;
- so the proof does not yet reach a theorem-facing statement of the selected-
  trace slice on the preferred codomain;
- this is still a local/trace obstruction, not a return to selector-level
  ambiguity.

Proof-attempt verdict:

- `B. the theorem is not fully proved, but the proof attempt reduces it to one
  smaller explicit local/trace lemma task.`

Conservative conclusion:

- the direct proof attempt does not close the `J_0` theorem at the current repo
  level;
- but it does sharpen the exact first unresolved step to the ambient finite-jet
  extraction lemma above;
- so the remaining gap is now below the level of theorem-task formulation and
  above the level of selector ambiguity.

### A2o. Direct theorem attempt for the ambient finite-jet extraction lemma

Lemma attempted in theorem-style form:

- fix `(n,q)`;
- domain:
  `A_full^th,n(q)`;
- claim:
  every `c in A_full^th,n(q)` admits a unique current-normalized leading-center
  quadruple `(U0, N0, P0, Y0)` such that
  `[U0, P0, N0 + (lambda_c / n) P0, Y0 - lambda_c P0]`
  is well-defined, compatible with the clean mixed equations, and agrees with
  `C_center` on the weighted-trial overlap.

Proof-attempt breakdown:

1. Agreement with `C_center` on the weighted-trial overlap:

- already closed;
- this is exactly the current weighted-ansatz trace theorem
  `J_0 = C_center` on the present repository boundary.

2. Compatibility with the clean mixed equations:

- closed conditionally on existence of the four leading coefficients;
- at the selected leading-center level the current symbolic local block yields
  `n N0 + lambda_c P0 = 0` and `n N0 + Y0 = 0`,
  hence the two regularity-defect rows are exactly the ones already used in the
  current `J_0` coordinates;
- so compatibility is not the first unresolved point once the coefficients are
  available.

3. Uniqueness of the normalized quadruple:

- also not the first unresolved point;
- once the four leading coefficients exist in the current near-center scaling
  class for `(u_s, u_n, varphi, psi)`, uniqueness of those leading coefficients
  is formal in that normalization.

4. Existence of the four current-normalized leading coefficients on
   `A_full^th,n(q)`:

- the proof stops here first;
- the repo still does not close the ambient statement that every
  `c in A_full^th,n(q)` actually admits those four leading coefficients in the
  current trace convention, prior to imposing the already checked leading local
  relations.

Exact first unresolved sublemma:

- Ambient leading-coefficient extraction / normalization sublemma:
  every `c in A_full^th,n(q)` admits current-normalized leading coefficients
  for the channels `(u_s, u_n, varphi, psi)` in the current near-center
  scaling class, so that `(U0, N0, P0, Y0)` exists before one asks for the
  mixed-equation relations among them.

Why this is the first true blocker:

- the previous finite-jet lemma bundled four things together;
- the present proof attempt shows that overlap agreement with `C_center`,
  equation compatibility at leading order, and uniqueness inside the chosen
  normalization are not the first failing steps;
- the first failure is simpler: the ambient theorem-facing extraction of the
  four current-normalized leading coefficients themselves.

Proof-attempt verdict:

- `B. the lemma is not proved, but it is reduced to one smaller explicit
  sublemma.`

Conservative conclusion:

- the ambient finite-jet extraction lemma is still open at the current repo
  level;
- but its first unresolved step is now sharper than before:
  not full finite-jet extraction with all properties at once, but the ambient
  leading-coefficient extraction / normalization sublemma above;
- this remains a local/trace problem and does not reopen the selector layer.

### A2p. Direct theorem attempt for the ambient leading-coefficient extraction / normalization sublemma

Sublemma attempted in theorem-style form:

- fix `(n,q)`;
- domain:
  `A_full^th,n(q)`;
- channels:
  `(u_s, u_n, varphi, psi)`;
- current normalization/scaling statement to prove:
  every `c in A_full^th,n(q)` admits
  `u_s = U0 x^n + o(x^n)`,
  `u_n = N0 x^n + o(x^n)`,
  `varphi = P0 x^(n-1) + o(x^(n-1))`,
  `psi = Y0 x^(n-1) + o(x^(n-1))`
  in the current center-trace convention;
- desired conclusion:
  the four current-normalized leading coefficients `(U0, N0, P0, Y0)` exist
  for every ambient object before one imposes the already known leading
  mixed-equation relations among them.

Proof-attempt breakdown:

1. Uniqueness under the chosen normalization:

- closed conditionally once the one-term asymptotics above exist;
- the coefficients are then uniquely determined as the leading coefficients in
  those four fixed orders.

2. Relation to the already exact weighted-ansatz overlap:

- already closed once again;
- on the weighted-trial overlap the current exact `C_center` map already
  extracts precisely those same four leading coefficients in the current trace
  convention.

3. Compatibility with the ambient admissible / center-regular class:

- not the first blocker once the one-term asymptotics exist;
- the principal-part analysis and the checked local leading block already match
  the same scaling orders and the same `J_0` coordinates used on the weighted-
  ansatz side;
- so compatibility is not where the proof stops first.

4. Existence of the one-term current-normalized asymptotics on all of
   `A_full^th,n(q)`:

- the proof stops here first;
- the repo currently has the principal-part scaling orders and the local
  leading symbolic family, but it still does not close the ambient theorem that
  every `c in A_full^th,n(q)` actually admits those one-term asymptotics in the
  current trace convention.

Exact first unresolved sub-sublemma:

- Ambient one-term asymptotic existence sub-sublemma:
  every `c in A_full^th,n(q)` satisfies
  `u_s = U0 x^n + o(x^n)`,
  `u_n = N0 x^n + o(x^n)`,
  `varphi = P0 x^(n-1) + o(x^(n-1))`,
  `psi = Y0 x^(n-1) + o(x^(n-1))`
  for some coefficients `(U0, N0, P0, Y0)` in the current center-trace
  normalization.

Why this is the first true blocker:

- once those one-term asymptotics exist, coefficient extraction itself is
  immediate;
- uniqueness in the chosen normalization is then formal;
- the weighted-ansatz overlap and later leading-equation compatibility are
  already aligned with the same trace convention;
- so the direct theorem attempt stops first at ambient one-term asymptotic
  existence, not at a larger selector or codomain question.

Proof-attempt verdict:

- `B. the sublemma is not proved, but it is reduced to one smaller explicit
  asymptotic-existence sub-sublemma.`

Conservative conclusion:

- the ambient leading-coefficient extraction / normalization sublemma is still
  open at the current repo level;
- but its first unresolved step is now one level narrower:
  the ambient one-term asymptotic existence statement in the current scaling
  class for `(u_s, u_n, varphi, psi)`;
- this remains a narrow local/trace obstruction.

### A2q. Direct theorem attempt for the ambient one-term asymptotic existence sub-sublemma

Sub-sublemma attempted in theorem-style form:

- fix `(n,q)`;
- domain:
  `A_full^th,n(q)`;
- channels:
  `(u_s, u_n, varphi, psi)`;
- current scaling/normalization:
  `u_s, u_n` are read in the `x^n` normalization and
  `varphi, psi` in the `x^(n-1)` normalization;
- claim to prove:
  every `c in A_full^th,n(q)` admits one-term asymptotics
  `u_s = U0 x^n + o(x^n)`,
  `u_n = N0 x^n + o(x^n)`,
  `varphi = P0 x^(n-1) + o(x^(n-1))`,
  `psi = Y0 x^(n-1) + o(x^(n-1))`
  in the current center-trace convention.

Proof-attempt breakdown:

1. Relation to the ambient admissible / center-regular class:

- partially closed at the order level;
- the principal-part analysis and the current local principal model already
  support the scaling orders
  `u_s, u_n = O(x^n)` and `varphi, psi = O(x^(n-1))`;
- so the first unresolved point is no longer which exponents the current clean
  branch uses.

2. Relation to the already exact weighted-ansatz overlap:

- closed once more;
- on the weighted-trial boundary the exact `C_center` trace already uses the
  same normalized channel convention.

3. Uniqueness once those one-term asymptotics exist:

- formal;
- once the four one-term asymptotics exist, the coefficients
  `(U0, N0, P0, Y0)` are uniquely determined as the corresponding leading
  coefficients in the fixed normalization.

4. Existence of the one-term asymptotics themselves:

- the proof stops here first;
- the repo supports the order bounds, but it still does not close the ambient
  theorem that the four normalized channel quotients actually have finite
  limits on all of `A_full^th,n(q)`.

Exact first unresolved sub-sub-sublemma:

- Ambient normalized-limit existence sub-sub-sublemma:
  every `c in A_full^th,n(q)` satisfies that the four normalized quotients
  `u_s / x^n`,
  `u_n / x^n`,
  `varphi / x^(n-1)`,
  `psi / x^(n-1)`
  admit finite limits in the current center-trace normalization.

Why this is the first true blocker:

- if those four normalized limits existed, the one-term asymptotics would
  follow immediately by definition;
- the scaling orders themselves are already the supported current ones;
- the weighted-ansatz overlap and the later `J_0`-coordinate extraction are
  already aligned with the same normalization;
- so the direct theorem attempt stops first at normalized-limit existence, not
  at a broader asymptotic or selector-level ambiguity.

Proof-attempt verdict:

- `B. the sub-sublemma is not proved, but it is reduced to one smaller explicit
  normalized-limit sub-sub-sublemma.`

Conservative conclusion:

- the ambient one-term asymptotic existence sub-sublemma is still open at the
  current repo level;
- but its first unresolved step is now even narrower:
  finite existence of the four normalized channel limits in the current
  scaling/trace convention;
- this remains a narrow local/trace obstruction.

### A2r. Direct theorem attempt for the ambient normalized-limit existence sub-sub-sublemma

Sub-sub-sublemma attempted in theorem-style form:

- fix `(n,q)`;
- domain:
  `A_full^th,n(q)`;
- normalized channels:
  `u_s / x^n`,
  `u_n / x^n`,
  `varphi / x^(n-1)`,
  `psi / x^(n-1)`;
- current center-trace normalization:
  the same four renormalized quantities used by the current `J_0`-coordinate
  convention;
- claim to prove:
  every `c in A_full^th,n(q)` has finite limits of those four normalized
  channels as `x -> 0`.

Proof-attempt breakdown:

1. Boundedness from the current scaling orders:

- closed at the current repo level;
- the principal-part analysis already supports
  `u_s, u_n = O(x^n)` and `varphi, psi = O(x^(n-1))`;
- therefore the four normalized quotients are already bounded in the current
  scaling class.

2. Relation to the ambient admissible / center-regular class:

- partially closed in the same boundedness sense;
- the present theorem-facing reading of `A_full^th,n(q)` already requires the
  current center-regular scaling orders, so the normalized quotients are
  meaningful on the punctured near-center domain.

3. Relation to the principal/local analysis already in the repo:

- closed only at order level;
- the local principal model fixes the exponents and the current renormalized
  channels, but it does not yet prove that those bounded quotients converge for
  every ambient admissible object.

4. Relation to the exact weighted-ansatz overlap:

- closed once more;
- on the weighted-trial boundary the same normalized quantities are exactly the
  `C_center` / `J_0` coordinates already checked symbolically.

Exact first unresolved sub-sub-sub-sublemma:

- Ambient normalized-quotient convergence sub-sub-sub-sublemma:
  every `c in A_full^th,n(q)` satisfies that the bounded renormalized channels
  `x^(-n) u_s`,
  `x^(-n) u_n`,
  `x^(1-n) varphi`,
  `x^(1-n) psi`
  converge as `x -> 0`, equivalently admit continuous extension to the center
  in the present trace normalization.

Why this is the first true blocker:

- boundedness of those four renormalized channels is already supplied by the
  current scaling analysis;
- the weighted-ansatz overlap already identifies the same quantities with the
  exact `C_center` trace on the repo boundary;
- so the direct theorem attempt no longer stops at the whole limit statement,
  but specifically at the convergence / continuous-extension step for those
  already-bounded quotients.

Proof-attempt verdict:

- `B. the sub-sub-sublemma is not proved, but it is reduced to one smaller
  explicit normalized-quotient convergence sub-sub-sub-sublemma.`

Conservative conclusion:

- the ambient normalized-limit existence sub-sub-sublemma is still open at the
  current repo level;
- but the boundedness part is no longer the blocker;
- the first unresolved point is now convergence of the already-bounded
  renormalized center channels in the current trace convention;
- this remains a narrow local/trace obstruction.

### A2s. Direct theorem attempt for the ambient normalized-quotient convergence sub-sub-sub-sublemma

Sub-sub-sub-sublemma attempted in theorem-style form:

- fix `(n,q)`;
- domain:
  `A_full^th,n(q)`;
- renormalized channels:
  `x^(-n) u_s`,
  `x^(-n) u_n`,
  `x^(1-n) varphi`,
  `x^(1-n) psi`;
- current center-trace normalization:
  the same renormalized channel chart used by the present `J_0` coordinates;
- claim to prove:
  every `c in A_full^th,n(q)` makes those four renormalized channels converge
  as `x -> 0`, equivalently extend continuously to the center.

Proof-attempt breakdown by route:

1. Derivative / integrability route:

- blocked first;
- the repo does not yet contain theorem-facing derivative identities or
  integrability estimates for
  `d/dx [x^(-n) u_s]`,
  `d/dx [x^(-n) u_n]`,
  `d/dx [x^(1-n) varphi]`,
  `d/dx [x^(1-n) psi]`
  on arbitrary ambient objects in `A_full^th,n(q)`;
- so this route does not presently upgrade boundedness to a Cauchy property.

2. Regular-singular system route:

- gets furthest;
- the current principal-part model and checked recurrence layers already show
  that the clean branch is naturally organized in these renormalized
  near-center variables;
- the missing step is no longer the choice of variables or exponents, but the
  ambient theorem-facing statement that these renormalized channels satisfy a
  closed local regular-singular continuation / recurrence strong enough to
  force convergence of bounded solutions.

3. Compactness / continuity route:

- also blocked;
- the repo does not yet have a stronger local continuation/completeness theorem
  on `A_full^th,n(q)` that would upgrade boundedness alone to convergence by an
  abstract compactness argument.

4. Relation to the exact weighted-ansatz overlap:

- still closed;
- on the weighted-trial boundary the same renormalized quantities are exactly
  the current `C_center` / `J_0` coordinates.

Which route gets furthest:

- the regular-singular system route gets furthest;
- it matches the already checked local recurrence material and identifies the
  smallest structural theorem that would imply convergence.

Exact first unresolved sub-sub-sub-sub-sublemma:

- Ambient renormalized regular-singular limit sub-sub-sub-sub-sublemma:
  for every `c in A_full^th,n(q)`, the renormalized channel vector
  `W_c(x) = [x^(-n) u_s, x^(-n) u_n, x^(1-n) varphi, x^(1-n) psi]`
  satisfies a theorem-facing near-center regular-singular local system /
  continuation statement strong enough that boundedness of `W_c` implies
  convergence of `W_c(x)` as `x -> 0`.

Why this is the first true blocker:

- route 1 fails because derivative-integrability of the renormalized channels
  has not been derived;
- route 3 fails because no stronger ambient compactness/completeness theorem is
  yet available;
- route 2 reaches a sharper structural target, but still needs the ambient
  local system / continuation theorem that turns the checked recurrence picture
  into actual limit existence for arbitrary `c in A_full^th,n(q)`.

Proof-attempt verdict:

- `B. the sub-sub-sub-sublemma is not proved, but it is reduced to one smaller
  explicit renormalized regular-singular limit sub-sub-sub-sub-sublemma.`

Conservative conclusion:

- the ambient normalized-quotient convergence sub-sub-sub-sublemma is still
  open at the current repo level;
- the regular-singular route is the only one that gets materially further with
  current repo evidence;
- the first unresolved point is now an ambient renormalized local-system /
  continuation lemma, not the scaling orders or boundedness;
- this remains a narrow local/trace obstruction.

### A2t. Direct theorem attempt for the ambient renormalized regular-singular limit sub-sub-sub-sub-sublemma

Lemma attempted in theorem-style form:

- fix `(n,q)`;
- domain:
  `A_full^th,n(q)`;
- renormalized vector:
  `W_c(x) = [x^(-n) u_s, x^(-n) u_n, x^(1-n) varphi, x^(1-n) psi]`;
- regular-singular route:
  use the current richer local jet / recurrence picture
  `Xi_rich^(1,eta)`, `Xi_rich^(1+,eta)` together with the canonical projection
  `Pi_eta_to_J0`;
- claim to prove:
  every ambient object `c in A_full^th,n(q)` satisfies a theorem-facing
  punctured-neighborhood regular-singular continuation statement for `W_c`
  strong enough that boundedness of `W_c` implies convergence as `x -> 0`.

Proof-attempt breakdown:

1. Connection to the current renormalized variables:

- closed on the current repo boundary;
- the center-trace normalization already uses exactly these renormalized
  quantities through `C_center` / `J_0`.

2. Formal regular-singular picture:

- partially closed;
- the principal center model and the checked richer-jet recurrence calculations
  show that the local picture is naturally organized in renormalized variables,
  and they provide the checked finite-order candidate structure behind the
  sought local theorem.

3. Ambient derivation of a punctured-neighborhood local system:

- blocked first;
- the repo does not yet prove that every ambient object `c in A_full^th,n(q)`
  lifts from those checked jet identities to a genuine punctured-neighborhood
  renormalized local state satisfying a closed theorem-facing regular-singular
  system.

4. Regular-singular classification and bounded-solution convergence inside that system:

- not the first blocker;
- those questions only become theorem-facing after the ambient local system has
  been derived.

5. Return to the current center-trace normalization:

- formally aligned once more;
- the projection `Pi_eta_to_J0` is exact on the checked richer trace charts, so
  any ambient theorem built through that route would return to the present
  `J_0 = C_center` coordinates canonically.

Which exact regular-singular route gets used:

- the richer-jet / recurrence route is the only route used here;
- more precisely, the theorem attempt passes through the checked truncated jet
  `Xi_rich^(1,eta)`, its augmented version `Xi_rich^(1+,eta)`, and the exact
  projection `Pi_eta_to_J0`, not through derivative-integrability or abstract
  compactness.

Exact first unresolved sub-sub-sub-sub-sub-sublemma:

- Ambient renormalized local-system derivation / jet-lift
  sub-sub-sub-sub-sub-sublemma:
  for every `c in A_full^th,n(q)`, there exists a punctured near-center local
  state extending
  `W_c(x) = [x^(-n) u_s, x^(-n) u_n, x^(1-n) varphi, x^(1-n) psi]`
  by the first post-leading variables of the current richer jet, and that
  extended state satisfies a closed theorem-facing near-center
  regular-singular system whose leading structure agrees with the checked
  principal-part / recurrence model.

Why this is the first true blocker:

- the current repo already has the correct renormalized variables and the
  formal finite-order recurrence picture;
- but it still does not upgrade that picture to a theorem on arbitrary ambient
  `A_full^th,n(q)` objects on a punctured neighborhood;
- so the proof stops first at derivation of the ambient local system itself,
  inseparable from the needed local continuation/completeness step;
- regular-singular classification and bounded-solution convergence are not yet
  the first unresolved point.

Proof-attempt verdict:

- `B. the lemma is not proved, but it is reduced to one smaller explicit
  ambient renormalized local-system / jet-lift
  sub-sub-sub-sub-sub-sublemma.`

Conservative conclusion:

- the ambient renormalized regular-singular limit lemma is still open at the
  current repo level;
- the richer-jet regular-singular route remains the correct route to pursue;
- but the first unresolved point is now sharper still:
  derivation of the ambient punctured-neighborhood renormalized local system
  itself;
- this remains a narrow local/trace obstruction and does not reopen selector
  authority, codomain choice, or clean-path consistency.

### A2u. Direct theorem attempt for the ambient punctured-neighborhood renormalized local-system / jet-lift lemma

Lemma attempted in theorem-style form:

- fix `(n,q)`;
- domain:
  `A_full^th,n(q)`;
- renormalized vector:
  `W_c(x) = [x^(-n) u_s, x^(-n) u_n, x^(1-n) varphi, x^(1-n) psi]`;
- richer-jet extension variables:
  the first post-leading variables of the current richer charts
  `Xi_rich^(1,eta)` and, when the membrane direction is kept explicit,
  `Xi_rich^(1+,eta)`;
- claim to prove:
  every ambient object `c in A_full^th,n(q)` admits a punctured near-center
  local lift extending `W_c` by those richer-jet variables, and that lifted
  state satisfies a closed near-center regular-singular system whose leading
  structure agrees with the checked principal-part / recurrence model.

Proof-attempt breakdown:

1. Compatibility of the richer-jet variables with the present trace language:

- closed at the formal checked level;
- `Xi_rich^(1,eta)`, `Xi_rich^(1+,eta)`, and `Pi_eta_to_J0` already identify
  the intended post-leading variables and their canonical return to the present
  `J_0 = C_center` coordinates on the weighted-trial overlap;
- this exact overlap return must now be kept explicit in the theorem setup:
  no future theorem-line statement should read
  `richer-jet lift + regular-singular convergence`
  as sufficient by itself for `J_0^th` well-definedness.

2. Agreement of the leading structure with the checked recurrence model:

- formally closed once the richer-jet lift exists;
- the checked recurrence calculations already provide the target leading
  structure that such an ambient local state would need to match.

3. Existence of a punctured-neighborhood richer-jet lift for arbitrary ambient objects:

- blocked first;
- the repo still does not prove that every `c in A_full^th,n(q)` admits an
  actual punctured-neighborhood local lift realizing those first post-leading
  richer-jet variables rather than only a formal checked jet chart.

4. Derivation of the closed near-center regular-singular local system:

- not the first blocker;
- this comes only after the richer-jet lift exists as a theorem-facing ambient
  local state.

5. Feedback to the already isolated convergence step:

- formal once more;
- if the punctured-neighborhood richer-jet lift, its overlap compatibility with
  `J_0 = C_center` / `Pi_eta_to_J0`, and its closed local system existed, then
  one could return to the previously isolated bounded-solution convergence step
  inside that ambient system.

Exact first unresolved smaller lemma:

- Ambient punctured-neighborhood richer-jet lift-existence lemma:
  for every `c in A_full^th,n(q)`, there exists a punctured near-center local
  lift realizing the first post-leading richer-jet variables corresponding to
  `Xi_rich^(1,eta)` and, when needed, `Xi_rich^(1+,eta)`, compatibly with the
  renormalized vector `W_c(x)`, the canonical projection `Pi_eta_to_J0`, and
  the exact ansatz-boundary trace `J_0 = C_center` on the weighted-trial
  overlap whenever both descriptions are defined.

Why this is the first true blocker:

- the current repo already has the formal richer-jet coordinates and the
  checked recurrence structure;
- but it still does not upgrade them to a theorem on arbitrary ambient
  `A_full^th,n(q)` objects on a punctured neighborhood;
- so the proof stops before closure of the ambient regular-singular local
  system itself;
- the first missing step is punctured-neighborhood lift existence, not yet
  system closure or bounded-solution convergence.

Proof-attempt verdict:

- `B. the lemma is not proved, but it is reduced to one smaller explicit
  punctured-neighborhood richer-jet lift-existence lemma.`

Conservative conclusion:

- the ambient punctured-neighborhood renormalized local-system / jet-lift lemma
  is still open at the current repo level;
- the exact first unresolved point is now punctured-neighborhood richer-jet
  lift existence for arbitrary ambient objects;
- this remains a narrow local/trace obstruction and does not reopen selector
  authority, codomain choice, or clean-path consistency.
- the cleaned theorem-line reading from this point onward is:
  `richer-jet lift + regular-singular convergence + overlap compatibility
  => J_0^th well-defined`,
  with overlap compatibility built into the next active local theorem target
  rather than added later by hand.

### A2o. Direct proof attempt for the cleaned punctured-neighborhood richer-jet lift-existence lemma

Lemma attempted in theorem-style form:

- claim to prove:
  every ambient object `c in A_full^th,n(q)` admits a punctured near-center
  richer-jet lift realizing the first post-leading variables of
  `Xi_rich^(1,eta)` and, when needed, `Xi_rich^(1+,eta)`, extending `W_c`,
  compatible with `Pi_eta_to_J0`, and overlap-compatible with the exact
  ansatz-boundary trace `J_0 = C_center`.

Proof-attempt breakdown:

1. Extension of `W_c` once the current richer chart exists:

- formal;
- the first four slots of the richer chart are exactly the current normalized
  leading data together with the explicit defect coordinates, so once the chart
  is realized the extension of `W_c` is built in.

2. Compatibility with `Pi_eta_to_J0`:

- formal;
- the projection formula is exact on `Xi_rich^(1,eta)` and `Xi_rich^(1+,eta)`,
  so once the richer chart exists the canonical return to current `J_0`
  coordinates is immediate.

3. Overlap compatibility with `J_0 = C_center`:

- not the first blocker;
- once the richer chart exists and the canonical projection is available, the
  remaining overlap clause is exactly that the projected trace agrees with the
  already closed ansatz-boundary trace on the weighted-trial overlap;
- the targeted CAS+Lean back-verification already isolated this as an explicit
  premise, not as a new symbolic identity.

4. Existence of the punctured-neighborhood richer chart itself:

- blocked first;
- the repo still does not prove that every `c in A_full^th,n(q)` admits the
  first post-leading chart realization needed to speak theorem-facingly about
  `Xi_rich^(1,eta)` or `Xi_rich^(1+,eta)` on a punctured neighborhood.

5. Feedback to the later regular-singular step:

- formal once more;
- after such a chart is realized, the later regular-singular continuation /
  convergence step can be posed on that lifted state with the overlap clause
  already built in.

Exact first unresolved smaller lemma:

- Ambient punctured-neighborhood first post-leading chart-realization lemma:
  for every `c in A_full^th,n(q)`, there exists punctured near-center first
  post-leading chart data realizing `Xi_rich^(1,eta)` and, when needed,
  `Xi_rich^(1+,eta)`, extending the renormalized vector `W_c(x)`, so that
  `Pi_eta_to_J0` and the overlap return to `J_0 = C_center` are meaningful.

Why this is the first true blocker:

- the current repo already closes the exact richer-chart projection identities;
- it already isolates overlap compatibility as an explicit clause rather than a
  hidden symbolic issue;
- so the proof no longer stops at the projection or overlap steps themselves;
- it stops first at realizing the current richer chart for arbitrary ambient
  objects on a punctured neighborhood.

Proof-attempt verdict:

- `B. the lemma is not fully proved, but it is reduced to one smaller explicit
  local chart-realization lemma.`

Conservative conclusion:

- the cleaned punctured-neighborhood richer-jet lift-existence lemma is still
  open at the current repo level;
- the exact first unresolved point is now punctured-neighborhood first post-
  leading chart realization for arbitrary ambient objects;
- the Step-1 punctured local representative should presently be read as a
  separate local regularity / continuation lemma for ambient objects in
  `A_full^th,n(q)`, not as a silent strengthening of the meaning of
  `A_full^th,n(q)` itself and not as a standing extra assumption;
- a direct theorem-attempt pass on that isolated Step-1 target does not yet
  prove it, but reduces it further to one smaller explicit ambient punctured-
  local-representative existence lemma:
  once such a representative exists, the current scaling-class read already
  makes `W_c` meaningful and the checked richer-chart identities already make
  `Xi_rich^(1,eta)` / `Xi_rich^(1+,eta)` theorem-facingly meaningful;
- the next ambient-to-local step should presently be phrased through a weaker
  representation / witness relation between `c in A_full^th,n(q)` and a
  punctured near-center clean mixed germ, not by redefining `A_full^th,n(q)` as
  a germ quotient and not by demanding a canonical realization map at this
  stage;
- the exact predicate should presently be packaged as a hybrid witness relation
  `Rep_loc^{n,q}(c,G)`:
  `G` is a genuine punctured near-center clean mixed germ in the current mixed
  variables, it is admitted as the theorem-facing local witness for the ambient
  object `c`, and on the exact weighted-ansatz / selected-family boundary the
  relation is normalized by agreement with the exact finite leading-center
  trace `J_0 = C_center`;
- the next exact local lemma in that language is existential:
  for every `c in A_full^th,n(q)`, there exist `\delta > 0` and a punctured
  near-center clean mixed germ `G` on `(0,\delta)` such that
  `Rep_loc^{n,q}(c,G)`;
- a direct theorem-attempt pass on that existential witness lemma still does
  not prove it, but now the first unresolved step is sharper:
  the statement is well-posed in the `Rep_loc^{n,q}(c,G)` language, yet the
  repo still does not produce a punctured near-center clean mixed germ witness
  for arbitrary `c in A_full^th,n(q)`;
- the correct source principle behind that blocker should presently be read as
  a separate ambient punctured-neighborhood local clean mixed continuation
  theorem for `A_full^th,n(q)` objects:
  produce an actual punctured near-center clean mixed state first, then obtain
  the witness-germ statement by passing to its germ and applying
  `Rep_loc^{n,q}(c,G)`;
- this source theorem is narrower than a full article-level local solution-
  family derivation, better supported than a weak-to-local realization theorem
  on current repo material, and not yet already packaged as a closed theorem in
  the current pilots;
- a direct theorem-attempt pass on that source theorem still does not prove it,
  but sharpens the first unresolved step further:
  once a punctured near-center local continuation in the current mixed
  variables exists, the clean mixed-state, local-equation, and scaling-order
  clauses are no longer the first blockers, so the remaining gap is local
  continuation existence itself for arbitrary `c in A_full^th,n(q)`;
- the best-supported source mechanism behind that remaining gap is still a
  separate direct continuation theorem from the present ambient clean
  admissible / center-regular compatibility package:
  not an interpretation of `A_full^th,n(q)` as already made of punctured local
  states, not a weak-to-local extraction theorem, and not a newly missing
  ambient hypothesis that must first be added;
- this remains a narrow local/trace obstruction and does not reopen selector
  authority, codomain choice, or clean-path consistency.

### A3. What is closed enough theorem-facing

The following criterion-facing blocks are currently closed enough to use:

- `A_ls` as the current repo-selected reduced family;
- `J_0 = C_center` and `J_0(A_ls) = im(D_amp)`;
- `L_red,n(q) = [A_int,n(q); B_full,n(q)] V_adm,n(q)` as the main
  theorem-facing reduced object;
- the finite-dimensional selected-family bridge on the current repo-selected
  class:
  `ker(L_red) <-> A_ls ∩ ker(L_full)`.

This is enough to say that the right theorem-facing criticality question on the
current selected family is the nontrivial-kernel question for `L_red`, not a
boundary descendant alone.

### A4. What still depends on the too-strong reading

The following parts are not currently licensed theorem-facing conclusions:

- reading `sigma_min(B_mix)=0` or small `sigma_bal` as already equivalent to the
  nontrivial-kernel question for `L_red`;
- reading the current repo-selected family `A_ls` as already lossless for the
  full admissible clean tangent space;
- reading the current Tikhonov/KKT selector as already canonical or
  criterion-authoritative;
- reading the current truncated-SVD alternative as an already justified promoted
  baseline;
- reading the selected trace plus checked-local quotient data as already enough
  to force the selected representative;
- excluding the explicit membrane competitor from the criterion story.

### A5. What is descendant, diagnostic, or surrogate rather than the true criterion object

The true criterion-facing object is `L_red` on the selected family. By
contrast:

- `B_red` and `B_mix` are boundary descendants on that same selected family;
- `sigma_raw`, `sigma_bal`, and `sigma_bal_noH` are operational boundary-only
  diagnostics derived from `B_mix`;
- the `A + C`, `D`, and `E` pilots are surrogates/diagnostics, not the true
  criterion object;
- the support labels `supported candidate`, `unstable rival`, `reserve dip`,
  and `control mode` are reporting/ranking language layered on top of those
  diagnostics;
- the checked-local ingredients
  `J_0(c) in im(D_amp)` and
  `Q_chk(c) in im(D_rich,eta^corr) / span(g_mem)`
  define the strongest current overclass above `A_ls`, but they do not by
  themselves choose the critical load or wave number.

### A6. Current wave-number choice logic

There are presently three different wave-number choice layers:

- live code:
  choose the cross-mode winner by the smallest `sigma_bal`;
- operational clean project memory:
  keep `n=6` near `17.6 MPa` as the leading supported candidate,
  `n=8` as the main unstable rival,
  `n=7` as a raw reserve dip,
  and `n=4` as a control mode;
- theorem-facing layer:
  no closed theorem currently turns either of the two layers above into a final
  physical wave-number selection rule.

## Part B. Exact Failure Mode Of The Old Strong Reading

The old strong reading can be stated sharply as follows:

- the live boundary-only degeneration on `B_mix` was being treated as if it
  already captured the relevant criticality of the clean full problem;
- equivalently, the current selected trace and checked-local selected shadows
  were being read as if they already fixed the representative inside the same
  equal-trace class;
- therefore the explicit membrane competitor could be treated as excluded and
  the current load/mode ranking could be promoted toward a theorem-facing
  criticality reading.

What is now known to be too strong is the middle step.

The frozen line did not close any theorem implying that every theorem-facing
same-trace candidate must equal the selected representative

```text
c_sel = P_sel J_0(c),
```

or equivalently that the fiber excess vanishes automatically.

So the exact failed dependency is:

```text
selected trace + checked-local quotient compatibility
    => selected representative uniqueness
    => membrane-channel exclusion
```

The first implication is not secured on the present boundary. Once that fails,
the current criterion loses theorem-facing authority to exclude the explicit
membrane candidate, and the boundary-only ranking can no longer be read as an
exclusive final criticality criterion.

## Part C. Rebuilt Criterion Candidates

### Candidate R1. Supported Boundary-Diagnostic Criterion

Exact statement:

- for each mode `n`, define the working clean candidate load by a robust local
  minimum of the balanced boundary metric `sigma_bal(B_mix,n(q))`;
- report the winner only through the current support labels
  (`supported`, `unstable rival`, `reserve`, `control mode`).

Core object:

- `B_mix` and its balanced singular metric `sigma_bal`.

Assumptions:

- the current clean search windows and robustness checks are the admissible
  operational filter;
- no theorem-level promotion beyond that filter is attempted.

Current theorem-facing authority:

- numerical/operational only.

Suitability:

- provisional computation only: yes;
- theorem-facing development: no;
- comparison against the shallow-method result: yes, but only as exploratory
  comparison memory.

### Candidate R2. Selected-Class Reduced-Kernel Criterion With Explicit Membrane Caveat

Exact statement:

- for fixed clean `(n,q)`, selected-class criticality is read through

```text
exists 0 != a in R^2 : L_red,n(q) a = 0,
```

  equivalently

```text
exists 0 != c in A_ls,n(q) : L_full,n(q) c = 0;
```

- `B_red` and `B_mix` are used only as descendants/locators on the same
  selected family;
- any chosen `(n,q)` is reported as a selected-class critical candidate, not as
  a final physical one, because the membrane competitor is unresolved rather
  than excluded.

Core object:

- `L_red` on `A_ls = im(V_adm)`.

Assumptions:

- the selected-family reading of `A_ls`;
- the current finite-dimensional bridge from `L_red` to `A_ls ∩ ker(L_full)`;
- no claim that `A_ls` already equals the full theorem-facing admissible class;
- no claim that `B_mix` already replaces `L_red`;
- no claim that the explicit membrane competitor is excluded.

Current theorem-facing authority:

- strongest current reduced-object formulation on the presently chosen family;
- not yet criterion-authoritative for final clean criticality, because the
  selection rule choosing that family is itself unresolved.

Suitability:

- provisional computation only: yes;
- theorem-facing development: yes;
- comparison against the shallow-method result: yes, with the explicit reading
  "selected-class comparison, not final physical equivalence."

Current first practical `rho_R2` status:

- the first focused stacked `rho_R2` robustness pass on dense `n=6,7,8`
  windows keeps `n=8` ahead of `n=7` in five of six checked discretization
  settings and keeps `n=6` below both in all six;
- the combined finer setting `m_basis = 7`, `n_collocation = 140` flips the
  top two, with `n=7` beating `n=8` by only a small margin;
- this flip does not line up with worsening winner `cond(G_amp)`, so the
  instability is not well explained as a simple conditioning-spike winner;
- later selected-family sensitivity checks show that harmless representation
  changes are mostly washed out by canonical rebasing, but nearby selector
  changes are not;
- the later selection-rule audit then shows that the current Tikhonov-selected
  family is too recipe-sensitive for criterion authority, while the seemingly
  stable truncated-SVD alternative is still cutoff-dependent enough that it
  should not yet be promoted;
- therefore `rho_R2` is a useful comparative stacked diagnostic on the current
  selected family, but the present bottleneck is now the unresolved authority of
  the selection rule itself, not only pointwise `n=7` / `n=8` ranking on one
  fixed family.

### Candidate R3. Ambiguity-Aware Broadened Criterion

Exact statement:

- keep Candidate R2 as the selected-class baseline;
- in addition, keep an explicit unresolved competitor layer above the selected
  representative, i.e. do not collapse the criterion output to one winner while
  the membrane channel is still not excluded by theorem-facing authority;
- until that ambiguity is resolved, report a candidate set or ambiguity flag
  rather than a unique final physical `q_cr / n_cr`.

Core object:

- `L_red` on `A_ls`, together with an unresolved overclass above the selected
  representative.

Assumptions:

- the frozen negative knowledge is retained as active caution;
- the membrane channel is unresolved rather than silently absent.

Current theorem-facing authority:

- interpretation/strategy only.

Suitability:

- provisional computation only: yes, if ambiguity-aware reporting is desired;
- theorem-facing development: yes;
- comparison against the shallow-method result: yes, as a comparison envelope
  rather than a single-value claim.

## Part D. Recommended Next Criterion Path

The best next working target remains **Candidate R2**, but only as the current
theorem-facing diagnostic baseline on a fixed selected family, not as a
criterion-authoritative final selector.

Why this is still the right reduced-object target:

- it is anchored on the strongest currently licensed theorem-facing object,
  `L_red`;
- it stops overreading `B_mix` while still keeping `B_mix` useful as a locator;
- it keeps mathematical honesty by refusing to treat the membrane candidate as
  already excluded.

Why it still cannot be promoted further yet:

- the current Tikhonov-selected family is too recipe-sensitive for criterion
  authority;
- the apparently more stable truncated-SVD alternative is still cutoff-
  dependent enough that it is not yet a justified promoted baseline;
- so the present bottleneck is no longer only `n=7` versus `n=8` ranking, but
  the unresolved authority of the selected-family rule itself.

Exact next checks needed after this rebuild:

1. keep `L_red`-based and `rho_R2`-based readings only as diagnostics on an
   explicitly chosen family;
2. isolate what would actually make a selection rule criterion-authoritative on
   the present clean boundary;
3. decide whether that authority would have to come from a theorem-facing
   weak/KKT rule, a local-to-global selected-family theorem, or some other
   construction;
4. return to winner-search language only after the selection-authority layer is
   no longer open.

## Why This Pass Is Genuinely New

This pass does not replay the frozen theorem line.

It changes the criterion-facing organization itself:

- it separates the live boundary-only selector from the theorem-facing reduced
  object;
- it separates descendants/diagnostics/surrogates from the actual criterion
  target;
- it isolates the exact failed dependency in the old strong reading;
- it proposes explicit rebuilt criterion formulations and chooses one concrete
  next working target.
