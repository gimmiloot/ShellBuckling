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

### A3. What is closed enough theorem-facing

The following criterion-facing blocks are currently closed enough to use:

- `A_ls` as the current selected reduced family;
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

- strongest current criterion-facing formulation available in the repository.

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
- therefore `rho_R2` is a useful comparative stacked diagnostic on the current
  selected family, but it is not yet robust enough to be promoted to the new
  main working criterion.

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

The best next working target is **Candidate R2**:
the selected-class reduced-kernel criterion on `L_red`, with an explicit
membrane-ambiguity caveat.

Why this is the best balance:

- it is anchored on the strongest currently licensed theorem-facing object,
  `L_red`;
- it stops overreading `B_mix` while still keeping `B_mix` useful as a locator;
- it gives one workable criterion-facing target for computation and comparison;
- it keeps mathematical honesty by refusing to treat the membrane candidate as
  already excluded.

Exact next checks needed after this rebuild:

1. build direct clean competition curves for a reduced metric on
   `L_red = [A_int; B_full] V_adm` on the current competition set
   `n = 4, 6, 7, 8`;
2. compare, mode by mode, the minima of that `L_red`-based curve against the
   current `sigma_bal(B_mix)` minima and record any load drift or reordering;
3. compare the best selected-class `(q,n)` from the `L_red` reading against the
   current shallow-method result, explicitly as a selected-class comparison;
4. keep a separate ambiguity flag whenever the membrane channel has not been
   excluded, so the selected-class winner is not silently upgraded to a final
   physical `q_cr / n_cr`.

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
