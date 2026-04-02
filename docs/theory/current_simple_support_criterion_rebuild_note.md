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
