# Pilot 25: T3b Candidate Class, T3c Comparison Boundary, T3d Representative-Law Stage, T3e Fiber-Excess Criterion, T3f Zero-Excess Obstruction, T3g Residual-Class Lift Boundary, T3h Membrane-Kernel Global-Lift Boundary, T3i Projected-Lift Injectivity Boundary, T3j Checked-Local Coefficient-Extraction Boundary, T3k Same-Trace Shadow Obstruction Boundary, T3l Pairwise Membrane-Difference Boundary, T3m Membrane-Selector Vanishing Boundary, T3n Membrane-Quotient Uniqueness Boundary, T3o Patchwise Membrane-Constancy Boundary, T3p Membrane-Fiber Singleton Boundary, T3q Representative-Law Obstruction Boundary, T3r Patchwise Representative-Law Boundary, T3s Pointwise Basepoint-Relative Law Boundary, T3t Global Defect-Set Emptiness Boundary, and T3u Scalar-Image Collapse Boundary For Clean `simple support / РїРѕРґРІРёР¶РЅС‹Р№ С€Р°СЂРЅРёСЂ`

## Goal

This note now records twenty consecutive theorem-facing steps above the already
closed `T3a` bridge.

1. `T3b`: construct the strongest currently justified stronger theorem-facing
   candidate class above the exact repository-selected family.
2. `T3c`: reduce the reverse inclusion problem to the selected-representative
   law.
3. `T3d`: identify that representative law with fiberwise
   `H_n,q`-minimality / `H_n,q`-orthogonality.
4. `T3e`: sharpen the remaining gap to an exact nonnegative fiber-excess
   functional and isolate the current obstruction there.
5. `T3f`: test whether the candidate-class conditions actually force zero
   fiber excess, and sharpen the remaining gap to the exact shadow-only
   obstruction / counterexample template now justified on the current boundary.
6. `T3g`: isolate the exact same-trace quotient-invisible residual class and
   reduce the remaining gap to an admissible residual-lift problem.
7. T3h: sharpen that residual-lift problem to the exact global lift class of
   the local membrane-kernel line on the checked boundary.
8. `T3i`: sharpen the global lift problem further to the exact projected-map
   injectivity / kernel-control question on the admissible same-trace residual
   domain.
9. `T3j`: sharpen the missing-operator reading further to the strongest
   currently justified checked-local extractor package and isolate the
   remaining global-shadow bridge obstruction.
10. `T3k`: sharpen the global checked-local shadow target further to the exact
    obstruction theorem showing that any compatible raw same-trace shadow
    already collapses to the zero quotient class and the membrane line.
11. `T3l`: replace the collapsed raw same-trace shadow target by the
    chart-invariant pairwise membrane-difference object on equal-trace
    checked-local ambient pairs before quotient collapse.
12. `T3m`: package that surviving pairwise object as the chart-invariant
    basepoint-relative membrane selector on the exact admissible same-trace
    pair domain.
13. `T3n`: reduce selector vanishing to uniqueness in the equal-trace membrane
    quotient class, equivalently to patchwise membrane constancy on the exact
    admissible checked-local pair domain.
14. `T3o`: remove overlap compatibility as an independent bottleneck by proving
    the constant-shift overlap law on exact admissible residual-generated patch
    covers.
15. `T3p`: sharpen the remaining issue to singletonity of the exact checked-
    local patch image inside the fixed membrane fiber.
16. `T3q`: isolate the exact remaining missing ingredient as a
    representative law inside that fixed membrane fiber and prove that current
    quotient-final theorem-facing constraints do not force singletonity by
    themselves.
17. `T3r`: sharpen that patchwise representative-law question further to the
    pointwise basepoint-relative law on each exact patch and isolate the
    strongest currently justified one-point nonvanishing / non-singleton
    obstruction template.

18. `T3s`: descend that pointwise law to a chart-invariant exact global
    pointwise membrane-deviation map on `D_sigma,n(q; c_sel)` and isolate the
    remaining obstruction as emptiness of its exact nonzero set.
19. `T3t`: sharpen that global emptiness question further to one exact scalar
    defect-image collapse theorem, equivalently to
    `Sigma_sigma,n(q; c_sel) = {0}` on the same exact domain.
20. `T3u`: sharpen that scalar-image collapse question further to the exact
    pairwise scalar-difference image `Omega_sigma,n(q; c_sel)` and isolate the
    remaining obstruction as vanishing of that image on the admissible exact
    pair domain.

This note does not reopen the frozen local Outcome-B branch, does not collapse
anything to `B_red` / `B_mix`, does not change equations, and does not claim
final physical criticality.

## Frozen starting point

For fixed clean `(n, q)`, the exact current repository-selected class is

```text
A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q)).
```

The two already closed theorem-facing shadows are:

```text
A_sel,trace^th,n(q) := J_0(A_ls,n(q)) = im(D_amp,n(q)),
J_0 = C_center,
```

and

```text
Q_sel,loc^th,n(q)
  := im(D_rich,eta^corr,n(q)) / span(g_mem,n(q))
```

on the current checked local boundary.

The strongest currently justified candidate class introduced in `T3b` is

```text
A_sel^{th,cand},n(q)
  := { c in A_adm^th,n(q)
       : J_0(c) in im(D_amp,n(q))
         and Q_chk(c) in Q_sel,loc^th,n(q) }.
```

Here `Q_chk(c)` means the checked local quotient shadow of the current richer
local germ of `c`, whenever that checked local shadow is defined on the current
boundary.

The selected trace on the exact repo-selected family is already closed:

```text
J_0|_{A_sel^repo,n(q)} : A_sel^repo,n(q) -> im(D_amp,n(q))
```

is bijective, with inverse given by the selected lift

```text
P_sel,n(q)
  = H_n,q^(-1) C_center,n(q)^T
    (C_center,n(q) H_n,q^(-1) C_center,n(q)^T)^(-1),

H_n,q = A_int,n(q)^T A_int,n(q) + reg I.
```

## Exact `T3e` theorem target

The `T3e` target is now the fiberwise `H_n,q`-orthogonality / `H_n,q`-minimality
stage for the candidate class `A_sel^{th,cand}`.

The exact theorem that would close the reverse inclusion is:

```text
for every c in A_sel^{th,cand},n(q),

Delta_H,n,q(c)
:= (c - P_sel,n(q) J_0(c))^T H_n,q (c - P_sel,n(q) J_0(c))
= 0.
```

Because `H_n,q` is positive definite, this is equivalent to

```text
c = P_sel,n(q) J_0(c),
```

hence equivalent to

```text
A_sel^{th,cand},n(q) subseteq A_sel^repo,n(q),
```

and therefore to equality/losslessness together with the already closed forward
inclusion.

This is the right form of the theorem because `P_sel` is the exact global
weak/KKT-selected representative map already used by the current clean
architecture, while the difference

```text
z(c) := c - P_sel,n(q) J_0(c)
```

is exactly the same-trace fiber residual. On the current repo-selected
boundary, vanishing of that residual is equivalent to fiberwise
`H_n,q`-orthogonality / `H_n,q`-minimality.

Outside scope for `T3e`:
- not full `T3`;
- not final physical criticality;
- not a theorem that `B_red` or `B_mix` replace the full reduced-kernel
  question;
- not a reopening of the frozen local branch.

## Outcome reached in this turn

Outcome reached:

```text
Outcome B.
```

The fiberwise `H_n,q`-minimality theorem is not proved. But the exact
obstruction is now sharper than in `T3d`:

```text
current candidate-class membership does not yet imply
Delta_H,n,q(c) = 0.
```

So the remaining gap is no longer just the vector orthogonality condition. It
is the vanishing of one explicit nonnegative fiber-excess functional.

No explicit counterexample is constructed in this turn. So the result is an
exact obstruction / counter-condition, not a proved non-equality theorem.

## Strongest result obtained about fiberwise `H_n,q`-orthogonality / minimality

### Theorem `T3e`

For fixed clean `(n, q)`, on the current repository/theory boundary:

1. for every `c in A_sel^{th,cand},n(q)`, the candidate trace

```text
a := J_0(c)
```

lies in `im(D_amp,n(q))`, so the exact repo-selected representative with the
same selected trace is well defined as

```text
c_sel := P_sel,n(q) a = P_sel,n(q) J_0(c);
```

2. `c` and `c_sel` have the same current selected trace, hence their difference

```text
z := c - c_sel
```

lies in the kernel of the current trace map:

```text
J_0(z) = 0.
```

On the current weighted-ansatz boundary this is exactly the fixed-trace fiber
condition `z in ker(C_center,n(q))`;

3. the selected representative `c_sel` is the unique `H_n,q`-minimal point in
   that fixed-trace fiber, so it satisfies the fiberwise stationarity /
   orthogonality condition

```text
w^T H_n,q c_sel = 0   for every w in ker(C_center,n(q));
```

4. therefore the exact same-trace decomposition is `H_n,q`-orthogonal:

```text
c = c_sel + z,
z in ker(C_center,n(q)),
z^T H_n,q c_sel = 0;
```

5. consequently one has the exact fiber-excess identity

```text
c^T H_n,q c = c_sel^T H_n,q c_sel + z^T H_n,q z.
```

Equivalently, with

```text
Delta_H,n,q(c) := z^T H_n,q z,
```

one has

```text
Delta_H,n,q(c) >= 0,
```

with equality if and only if `z = 0`;

6. hence the following statements are equivalent on the current repo-selected
   boundary:

```text
c = P_sel,n(q) J_0(c),
Delta_H,n,q(c) = 0,
z^T H_n,q c = 0   for every z in ker(C_center,n(q)),
c is the unique H_n,q-minimal point in its fixed-trace fiber;
```

7. the candidate-class conditions defining `A_sel^{th,cand}` do not currently
   imply `Delta_H,n,q(c) = 0`;

8. therefore the exact remaining theorem is not another trace/quotient shadow
   statement, but the bridge

```text
c in A_sel^{th,cand}
->
Delta_H,n,q(c) = 0,
```

or equivalently the representative law `c = P_sel J_0(c)`.

### Why this is sharper than `T3d`

`T3d` reduced the reverse inclusion problem to fiberwise
`H_n,q`-orthogonality / `H_n,q`-minimality.
`T3e` now identifies the exact scalar defect functional that measures failure of
that law on the current repo-selected boundary:

```text
representative law
<->
zero fiber residual
<->
zero fiber-excess Delta_H.
```

So the remaining gap is no longer only an orthogonality statement. It is one
explicit nonnegative fiber-excess obstruction.

## Analysis of the candidate-class conditions against fiberwise minimality

### 1. Fixed-trace decomposition

Take `c in A_sel^{th,cand}` and set `a = J_0(c) in im(D_amp)`.
Then `c_sel = P_sel a` is the unique exact repo-selected element with the same
selected trace. Therefore

```text
J_0(c - c_sel) = 0.
```

So every candidate-class element admits the exact decomposition

```text
c = c_sel + z,
```

with

```text
z in ker(C_center,n(q)).
```

The surviving question is whether current candidate-class membership forces that
fiber residual `z` to vanish.

### 2. Orthogonal projection / fiber-excess identity

Inside the current weighted-ansatz architecture, the fixed-trace fiber for the
selected trace `a` is

```text
F_n,q(a) = { u : C_center,n(q) u = [a1, a2, 0, 0] }.
```

The repo-selected family is the unique `H_n,q`-minimal section of these fibers.
Because

```text
H_n,q = A_int,n(q)^T A_int,n(q) + reg I
```

is positive definite, the minimizer in each fiber is unique and equals the
`H_n,q`-orthogonal projection of any feasible section onto the complement of
`ker(C_center,n(q))`.

Therefore, for the same-trace decomposition `c = c_sel + z`, one has

```text
z^T H_n,q c_sel = 0,
```

and hence the exact Pythagorean identity

```text
c^T H_n,q c = c_sel^T H_n,q c_sel + z^T H_n,q z.
```

So the failure of the selected representative law is measured exactly by the
nonnegative excess

```text
Delta_H,n,q(c) = z^T H_n,q z.
```

### 3. What the candidate-class conditions actually force

The trace condition gives only

```text
J_0(c) in im(D_amp).
```

So it fixes the selected trace and therefore fixes the comparison point `c_sel`,
but it says nothing by itself about the fiber residual `z`.

The quotient condition is also weaker than representative selection.
On the current checked local boundary it is already closed that:
- all currently justified local selected invariants factor through the quotient
  coordinates `(a, b)`;
- the canonical `J_0` trace on the corrected local family is exactly `D_amp`
  composed with the quotient map `(a, b, s) -> (a, b)`;
- no checked local condition distinguishes representatives inside one quotient
  class.

So the quotient condition preserves the selected shadow coordinates, but does
not recover a representative-level selector and does not measure the global
fiber-excess `Delta_H,n,q(c)`.

### 4. What the current candidate-class definition does not encode

The current candidate-class definition does not contain the global
`H_n,q`-objective or any equivalent minimality clause.

More precisely:
- the selected trace condition fixes only which fixed-trace fiber is relevant;
- the checked local quotient condition is representative-lossy on the frozen
  Outcome-B boundary;
- the current theorem boundary provides no theorem that these shadow conditions
  force `z = 0` or `Delta_H,n,q(c) = 0`;
- therefore the surviving freedom is exactly the same-trace fiber residual
  `z = c - P_sel J_0(c)`.

This surviving freedom is not another trace coordinate and not another checked
local quotient coordinate. It is the global fiber direction that remains after
all current shadow conditions are imposed.

### 5. Exact obstruction / counter-condition

The exact obstruction is now:

```text
current candidate-class membership does not yet imply
Delta_H,n,q(c) = 0.
```

Equivalently, the exact counter-condition to the reverse inclusion is:

```text
if there exists c in A_sel^{th,cand},n(q)
with Delta_H,n,q(c) > 0,
then c != P_sel,n(q) J_0(c),
so c is not in A_sel^repo,n(q).
```

Because `Delta_H,n,q(c) = z^T H_n,q z` with `H_n,q` positive definite, this is
exactly the same as saying that a nonzero fixed-trace fiber residual survives.

This is sharper than `T3d` because it isolates the remaining obstruction as one
explicit nonnegative scalar defect, not only as an orthogonality condition.

## Minimal `T3e` lemma split

### `T3e-L1`. Fixed-trace decomposition lemma

Statement:

```text
For c in A_sel^{th,cand}, letting c_sel = P_sel J_0(c),
one has c = c_sel + z with z in ker(C_center,n(q)).
```

Status:
- closed enough.

Main support:
- `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.8`-`1.10.10`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.

Verification method:
- manual derivation;
- code inspection;
- CAS/theory reuse for the selected-lift identities.

### `T3e-L2`. Fiber-excess identity lemma

Statement:

On the current repo-selected boundary, with `c = c_sel + z` from `T3e-L1`, one
has

```text
z^T H_n,q c_sel = 0,
c^T H_n,q c = c_sel^T H_n,q c_sel + z^T H_n,q z.
```

Therefore

```text
Delta_H,n,q(c) := (c - c_sel)^T H_n,q (c - c_sel)
```

is nonnegative and measures the exact fiberwise excess above the selected
representative.

Status:
- closed enough.

Main support:
- `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.8`-`1.10.10`;
- `docs/theory/current_theory_verification_map.md` entries `V-S10`, `V-S12`, `V-S22`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`.

Verification method:
- manual derivation;
- code inspection;
- representative live clean evaluation for the KKT-selected section side.

### `T3e-L3`. Minimality criterion lemma

Statement:

On the current repo-selected boundary, the following are equivalent:

```text
c = P_sel J_0(c),
Delta_H,n,q(c) = 0,
z^T H_n,q c = 0 for every z in ker(C_center,n(q)),
c is the unique H_n,q-minimal point in its fixed-trace fiber.
```

Status:
- closed enough.

Main support:
- `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.8`-`1.10.10`;
- `docs/theory/current_theory_verification_map.md` entries `V-S10`, `V-S12`, `V-S22`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`.

Verification method:
- manual derivation;
- code inspection;
- Lean target after the exact equivalence is abstracted.

### `T3e-L4`. Candidate-condition implication / obstruction lemma

Statement:

The current candidate-class conditions do not imply the zero-excess condition
from `T3e-L3`.
More precisely:
- the trace condition fixes only the selected trace plane;
- the checked local quotient condition is representative-lossy on the current
  checked boundary;
- the current candidate-class definition contains no closed `H_n,q`-minimality
  clause;
- therefore the exact surviving freedom is the fiber residual
  `z = c - P_sel J_0(c)`, equivalently the fiber-excess `Delta_H,n,q(c)`.

Status:
- Outcome B: exact obstruction isolated.

Main support:
- `selection_object_check.py` for the global fiber/KKT-selected section side;
- `docs/theory/current_theory_verification_map.md` entries `V-S10`, `V-S18`,
  `V-S20`, `V-S22`;
- this note.

Verification method:
- manual derivation;
- representative live clean evaluation for the global selection side;
- CAS/theory reuse for the quotient-lossiness side.

### `T3e-L5`. Upgrade consequence lemma

Statement:

If one proves, for every `c in A_sel^{th,cand}`,

```text
Delta_H,n,q(c) = 0,
```

then automatically

```text
c = P_sel J_0(c),
A_sel^{th,cand} subseteq A_sel^repo,
and hence A_sel^{th,cand} = A_sel^repo.
```

Therefore `T3a` upgrades losslessly to the candidate class.

Conversely, if one constructs `c in A_sel^{th,cand}` with

```text
Delta_H,n,q(c) > 0,
```

then the reverse inclusion fails on the current repository boundary.

Status:
- closed enough as a conditional theorem / counter-condition package.

Main support:
- this note;
- `proof_pilots/pilot_24_t3a_selected_kernel_bridge/pilot_24_t3a_selected_kernel_bridge.md`.

Verification method:
- manual derivation;
- Lean target after the exact defect functional is isolated.

## Single next bottleneck after `T3e`

The single next bottleneck is now:

```text
prove or refute that Delta_H,n,q(c) = 0 for every c in A_sel^{th,cand}.
```

Equivalently:

```text
prove or refute that every candidate-class element has zero same-trace
fiber residual.
```

This is sharper than before because the reverse inclusion problem is no longer
only a generic representative theorem or only a vector orthogonality gap. It is
one explicit zero-excess bridge.

## Concrete artifact

Chosen artifact:
- this same proof-pilot note.

No new helper script was added.
No solver code was changed.
No new numerical campaign was started.

## Lean / CAS / manual split

Lean:
- only finite-dimensional fixed-fiber / representative templates once the exact
  law is written in the abstract form
  `same trace + zero H-excess <-> selected representative`.

CAS / code inspection:
- `P_sel`, `J_0`, `H_n,q`, and the fixed-center fiber identities;
- `J_0(A_ls) = im(D_amp)` and `J_0|_{A_sel^repo}`;
- the KKT-selected section structure of `A_sel^repo` as the global
  `H_n,q`-minimal family;
- the quotient-factorization statement on the checked local boundary;
- the representative-lossiness of the checked local quotient theorem.

Manual derivation:
- exact theorem scope for `T3e`;
- why zero fiber-excess is equivalent to the selected representative law;
- why the candidate-class conditions do not yet imply vanishing of that
  excess;
- relation of `T3e` to future long-term `T3`.

## Conservative status after `T3e`

Closed enough now:
- `T3a` on `A_sel^repo`;
- the `T3b` candidate class `A_sel^{th,cand}`;
- the `T3c` exact inclusion `A_sel^repo subseteq A_sel^{th,cand}`;
- the `T3d` exact representative-law criterion
  `c = P_sel J_0(c) <-> fiberwise H_n,q-minimality / orthogonality`;
- the `T3e` exact fiber-excess identity
  `Delta_H,n,q(c) = (c - P_sel J_0(c))^T H_n,q (c - P_sel J_0(c))`, together
  with the equivalence
  `Delta_H = 0 <-> c = P_sel J_0(c)`.

Still open:
- whether every candidate-class element satisfies `Delta_H,n,q(c) = 0`;
- whether `A_sel^{th,cand} = A_sel^repo`;
- whether the selected-class kernel reading upgrades losslessly from
  `A_sel^repo` to `A_sel^{th,cand}`.

So the theorem program has moved beyond a generic reverse-inclusion reduction
and beyond a purely vector-form orthogonality bottleneck. The remaining gap is
now one explicit zero-excess bridge on the same fixed-trace fiber.

## Exact `T3f` theorem target

`T3e` already isolated the exact scalar defect

```text
Delta_H,n,q(c)
:= (c - P_sel,n(q) J_0(c))^T H_n,q (c - P_sel,n(q) J_0(c)).
```

The exact `T3f` target is now:

```text
for every c in A_sel^{th,cand},n(q),
Delta_H,n,q(c) = 0.
```

Because `H_n,q` is positive definite, this is equivalent to

```text
c = P_sel,n(q) J_0(c),
```

hence equivalent to the reverse inclusion

```text
A_sel^{th,cand},n(q) subseteq A_sel^repo,n(q),
```

and therefore to equality/losslessness together with the already closed forward
inclusion.

This is the right theorem form because `Delta_H,n,q(c)` is the exact same-trace
fiber excess above the global weak/KKT-selected representative. The present turn
asks whether the current candidate-class conditions actually force this excess
to vanish, or whether they still leave an exact positive-excess mechanism.

Outside scope for `T3f`:
- not full `T3`;
- not final physical criticality;
- not a collapse to `B_red` / `B_mix`;
- not a reopening of the frozen local branch.

## Outcome reached in this turn

Outcome reached:

```text
Outcome B.
```

A zero-excess theorem is still not proved. But the remaining obstruction is now
sharper than in `T3e`:

```text
current candidate-class membership controls only the selected shadow data
currently visible on the repo/theory boundary, and those shadow conditions do
not yet supply any representative-level control on the same-trace fiber
residual z(c) = c - P_sel,n(q) J_0(c).
```

More sharply, the checked local quotient condition is already known to be
representative-lossy and to factor through the same quotient coordinates as the
selected trace. So zero-excess can only follow from an additional theorem that
kills the remaining quotient-invisible same-trace fiber residue on the global
admissible side.

No explicit counterexample is constructed in this turn. But an exact
counterexample template is now available: if a nonzero admissible same-trace,
quotient-invisible fiber residual exists, then `Delta_H,n,q(c) > 0` follows
immediately.

## Strongest result obtained about `Delta_H,n,q(c) = 0`

### Theorem `T3f`

For fixed clean `(n, q)`, on the current repository/theory boundary:

1. for every `c in A_sel^{th,cand},n(q)`, the same-trace decomposition from
   `T3e` is exact:

```text
c = c_sel + z,
c_sel := P_sel,n(q) J_0(c),
z in ker(C_center,n(q));
```

2. the exact fiber-excess identity remains

```text
Delta_H,n,q(c) = z^T H_n,q z >= 0;
```

3. therefore

```text
Delta_H,n,q(c) = 0
```

if and only if

```text
z = 0,
c = P_sel,n(q) J_0(c),
```

and hence if and only if `c` is already the unique `H_n,q`-minimal point in its
fixed-trace fiber;

4. on the current checked local boundary, every currently justified local
   selected invariant factors through the quotient coordinates and does not
   distinguish representatives inside one quotient class;

5. the canonical `J_0` trace on the corrected local family is exactly `D_amp`
   composed with the quotient map `(a, b, s) -> (a, b)`;

6. therefore the checked local quotient condition inside
   `A_sel^{th,cand},n(q)` contributes no closed representative-level invariant
   beyond the same two selected shadow coordinates already carried by
   `J_0(c) in im(D_amp,n(q))`;

7. consequently the current candidate-class conditions do not presently force
   `z = 0` and do not presently imply `Delta_H,n,q(c) = 0`;

8. more sharply, if there exist

```text
c_sel in A_sel^repo,n(q),
0 != z in A_adm^th,n(q) intersect ker(C_center,n(q))
```

such that the checked local quotient shadow of `c_sel + z` still lies in the
selected quotient object

```text
Q_sel,loc^th,n(q) = im(D_rich,eta^corr,n(q)) / span(g_mem,n(q)),
```

then

```text
c := c_sel + z
```

lies in `A_sel^{th,cand},n(q)` and satisfies

```text
Delta_H,n,q(c) = z^T H_n,q z > 0.
```

This is the exact current counterexample template. Its existence is not yet
decided on the current repo/theory boundary.

### Why this is sharper than `T3e`

`T3e` isolated one explicit nonnegative scalar defect. `T3f` sharpens the gap
one step further: the current shadow conditions are already known to be
representative-lossy on the checked local side, so the remaining bridge is not
just an abstract scalar equality. It is whether any nonzero admissible
same-trace, quotient-invisible fiber residual can survive.

## Analysis of the candidate-class conditions against zero-excess

### 1. What remains exact from `T3e`

For `c in A_sel^{th,cand}`, set

```text
a = J_0(c),
c_sel = P_sel a,
z = c - c_sel.
```

Then

```text
z in ker(C_center,n(q)),
Delta_H,n,q(c) = z^T H_n,q z.
```

So `T3f` is exactly the question whether current candidate-class membership
forces `z = 0`.

### 2. What the checked local quotient theorem now adds

The checked local quotient theorem does not add a representative selector.
What it adds is an exact lossiness statement:

- every currently justified local selected invariant factors through the
  membrane quotient;
- the canonical `J_0` trace factors exactly through the quotient coordinates;
- no checked local condition distinguishes representatives inside one quotient
  class.

So the quotient condition preserves the same selected shadow coordinates, but it
still does not measure the global fiber excess `Delta_H,n,q(c)`.

### 3. Exact surviving freedom after all current shadow conditions

The current candidate-class definition now fixes:
- which selected trace plane `J_0(c)` belongs to;
- which checked local quotient object the richer local shadow belongs to.

But it still does not encode:
- the global `H_n,q` objective;
- an intrinsic local representative selector beyond the quotient;
- a theorem that same-trace, quotient-compatible admissible fiber residues must
  vanish.

Therefore the exact surviving freedom is:

```text
the admissible same-trace fiber residual z = c - P_sel,n(q) J_0(c)
that remains invisible to the current selected shadows.
```

### 4. Exact counterexample template / exact missing ingredient

The exact current counterexample template is the conditional construction from
Theorem `T3f` item 8.

So the exact missing ingredient is now sharper than in `T3e`:

```text
prove or refute that every admissible same-trace, quotient-compatible fiber
residual z is zero.
```

Equivalently:

```text
prove or refute that Delta_H,n,q(c) = 0 for every c in A_sel^{th,cand},n(q).
```

## Minimal `T3f` lemma split

### `T3f-L1`. Zero-excess decomposition lemma

Statement:

```text
For c in A_sel^{th,cand}, letting c_sel = P_sel J_0(c),
one has c = c_sel + z with z in ker(C_center,n(q)),
and Delta_H,n,q(c) = z^T H_n,q z.
```

Status:
- closed enough.

Main support:
- `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.8`-`1.10.10`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`;
- this note.

Verification method:
- manual derivation;
- code inspection;
- CAS/theory reuse for the selected-lift identities.

### `T3f-L2`. Candidate-condition control lemma

Statement:

```text
The current candidate-class conditions force only
J_0(c) in im(D_amp,n(q))
and
Q_chk(c) in Q_sel,loc^th,n(q),
while on the checked local boundary all currently justified local selected
invariants factor through the quotient coordinates and do not distinguish
representatives inside one quotient class.
```

Therefore they impose no currently closed representative-level condition forcing
`z = 0` or `Delta_H,n,q(c) = 0`.

Status:
- closed enough.

Main support:
- `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.14`-`1.10.16`;
- `docs/theory/current_theory_verification_map.md` entries `V-S18`, `V-S22`,
  `V-S23`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`.

Verification method:
- manual derivation;
- CAS/theory reuse for the quotient-factorization side;
- code inspection.

### `T3f-L3`. Zero-excess theorem or exact partial implication lemma

Statement:

```text
On the current repo-selected boundary,
c = P_sel J_0(c),
Delta_H,n,q(c) = 0,
and z = 0
are equivalent.
```

But current candidate-class membership implies only the same-trace
decomposition from `T3f-L1` and the shadow-level compatibility from `T3f-L2`;
the implication

```text
c in A_sel^{th,cand} -> Delta_H,n,q(c) = 0
```

is still open.

Status:
- partial.

Main support:
- `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.8`-`1.10.10`;
- `docs/theory/current_theory_verification_map.md` entries `V-S10`, `V-S12`,
  `V-S23`;
- this note.

Verification method:
- manual derivation;
- code inspection;
- Lean target after the exact equivalence is abstracted.

### `T3f-L4`. Exact obstruction / counterexample-template lemma

Statement:

```text
If there exist c_sel in A_sel^repo,n(q)
and 0 != z in A_adm^th,n(q) intersect ker(C_center,n(q))
such that Q_chk(c_sel + z) in Q_sel,loc^th,n(q),
then c := c_sel + z lies in A_sel^{th,cand},n(q)
and Delta_H,n,q(c) = z^T H_n,q z > 0.
```

So any such `z` is an exact counterexample template to reverse inclusion /
losslessness on the current repository boundary.

Status:
- closed enough as a conditional obstruction theorem;
- existence or impossibility of such `z` remains open.

Main support:
- `selection_object_check.py` for the global fiber/KKT-selected section side;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py` for quotient-lossiness;
- `docs/theory/current_theory_verification_map.md` entries `V-S18`, `V-S23`;
- this note.

Verification method:
- manual derivation;
- representative live clean evaluation for the global selection side;
- CAS/theory reuse for the quotient-lossiness side;
- code inspection.

### `T3f-L5`. Upgrade consequence lemma

Statement:

```text
If one proves Delta_H,n,q(c) = 0 for every c in A_sel^{th,cand},n(q),
then A_sel^{th,cand},n(q) subseteq A_sel^repo,n(q),
hence A_sel^{th,cand},n(q) = A_sel^repo,n(q).
```

Conversely, any instance of the template in `T3f-L4` gives
`Delta_H,n,q(c) > 0` and destroys reverse inclusion on the current boundary.

Status:
- closed enough as a conditional theorem / counter-condition package.

Main support:
- this note;
- `proof_pilots/pilot_24_t3a_selected_kernel_bridge/pilot_24_t3a_selected_kernel_bridge.md`.

Verification method:
- manual derivation;
- Lean target after the exact defect/counterexample template is isolated.

## Single next bottleneck after `T3f`

The single next bottleneck is now:

```text
prove or refute that no nonzero admissible same-trace, quotient-invisible
fiber residual survives on the current repo/theory boundary.
```

Equivalently:

```text
prove or refute Delta_H,n,q(c) = 0 for every c in A_sel^{th,cand},n(q).
```

This is sharper than in `T3e` because the remaining gap is no longer only a
scalar equality. It is the existence or impossibility of a same-trace,
quotient-invisible admissible fiber direction carrying positive excess.

## Concrete artifact

Chosen artifact:
- this same proof-pilot note.

No new helper script was added.
No solver code was changed.
No new numerical campaign was started.

## Lean / CAS / manual split for `T3f`

Lean:
- only finite-dimensional fixed-fiber / zero-excess templates once the exact
  law is written in the abstract form
  `same trace + zero H-excess <-> selected representative`, together with the
  conditional counterexample-template implication.

CAS / code inspection:
- `P_sel`, `J_0`, `H_n,q`, and the fixed-center fiber identities;
- `J_0(A_ls) = im(D_amp)` and `J_0|_{A_sel^repo}`;
- the KKT-selected section structure of `A_sel^repo` as the global
  `H_n,q`-minimal family;
- the quotient-factorization statement on the checked local boundary;
- the representative-lossiness of the checked local quotient theorem;
- the exact local statement that all currently justified local selected
  invariants factor through the quotient coordinates.

Manual derivation:
- exact theorem scope for `T3f`;
- why zero fiber-excess is equivalent to the selected representative law;
- why the candidate-class conditions do not yet imply vanishing of that
  excess;
- the exact counterexample template through a same-trace, quotient-invisible
  admissible fiber residual;
- relation of `T3f` to future long-term `T3`.

## Conservative status after `T3f`

Closed enough now:
- `T3a` on `A_sel^repo`;
- the `T3b` candidate class `A_sel^{th,cand}`;
- the `T3c` exact inclusion `A_sel^repo subseteq A_sel^{th,cand}`;
- the `T3d` exact representative-law criterion
  `c = P_sel J_0(c) <-> fiberwise H_n,q-minimality / orthogonality`;
- the `T3e` exact fiber-excess identity
  `Delta_H,n,q(c) = (c - P_sel J_0(c))^T H_n,q (c - P_sel J_0(c))`, together
  with the equivalence
  `Delta_H = 0 <-> c = P_sel J_0(c)`;
- the `T3f` exact shadow-only obstruction package:
  the checked local quotient condition carries no closed representative-level
  invariant beyond the same selected shadow coordinates, and any nonzero
  admissible same-trace, quotient-invisible fiber residual would yield
  `Delta_H > 0`.

Still open:
- whether every candidate-class element satisfies `Delta_H,n,q(c) = 0`;
- whether a nonzero admissible same-trace, quotient-invisible fiber residual
  exists on the current repo/theory boundary;
- whether `A_sel^{th,cand} = A_sel^repo`;
- whether the selected-class kernel reading upgrades losslessly from
  `A_sel^repo` to `A_sel^{th,cand}`.

So the theorem program has moved beyond a generic reverse-inclusion reduction,
beyond a purely vector-form orthogonality bottleneck, and beyond a bare scalar
zero-excess criterion. The remaining gap is now the existence or impossibility
of a same-trace, quotient-invisible admissible fiber residual.

## Exact `T3g` theorem target

The exact `T3g` target is now the existence / impossibility theorem for
nonzero same-trace, quotient-invisible fiber residuals.

For fixed clean `(n, q)`, let

```text
A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q)),
A_sel^{th,cand},n(q)
```

be the current exact repo-selected family and the current shadow-compatible
candidate class. For

```text
c_sel in A_sel^repo,n(q),
```

define the exact same-trace residual space

```text
R_same,n(q) := ker(C_center,n(q)) = ker(J_0,n(q)).
```

Define the admissible quotient-invisible residual class above `c_sel` by

```text
R_inv,n(q; c_sel)
  := { z in A_adm^th,n(q) intersect R_same,n(q)
       : Q_chk(c_sel + z) = Q_chk(c_sel) },
```

whenever both checked local shadows are defined on the current checked
boundary.

Here:
- вЂњsame-traceвЂќ means exactly `J_0(c_sel + z) = J_0(c_sel)`, equivalently
  `J_0(z) = 0`, equivalently `z in ker(C_center,n(q))`;
- вЂњquotient-invisibleвЂќ means exactly equality of checked local quotient shadows
  in
  `Q_sel,loc^th,n(q) = im(D_rich,eta^corr,n(q)) / span(g_mem,n(q))`.

Because `Delta_H,n,q(c_sel + z) = z^T H_n,q z`, vanishing or nonvanishing of
this residual class decides the remaining zero-excess gap:

```text
R_inv,n(q; c_sel) = {0} for every c_sel in A_sel^repo,n(q)
```

if and only if

```text
Delta_H,n,q(c) = 0 for every c in A_sel^{th,cand},n(q).
```

This is still not full `T3`, not final physical criticality, and not a
collapse to `B_red` / `B_mix`.

## Outcome reached in this turn

Outcome reached:

```text
Outcome B.
```

No impossibility theorem and no explicit nonzero residual are proved. The
strongest new result is a sharper exact obstruction theorem:

```text
on the current repo/theory boundary, the existence of a positive-excess
candidate is equivalent to the nontriviality of the exact lift class
R_inv,n(q; c_sel)
for some c_sel in A_sel^repo,n(q).
```

More sharply, the checked local quotient theorem does not merely fail to rule
out residuals abstractly. It identifies the only currently visible
quotient-invisible local direction: the membrane kernel line `span(g_mem)`.
So the remaining theorem is now an exact lift problem:

```text
does the local membrane kernel direction admit a nonzero admissible global
same-trace lift inside ker(C_center,n(q))?
```

## Strongest result obtained about nonzero same-trace, quotient-invisible residuals

### Theorem `T3g`

For fixed clean `(n, q)`, on the current repository/theory boundary:

1. for each `c_sel in A_sel^repo,n(q)`, the exact candidate-residual class is

```text
R_inv,n(q; c_sel)
  := { z in A_adm^th,n(q) intersect ker(C_center,n(q))
       : Q_chk(c_sel + z) = Q_chk(c_sel) };
```

2. if `z in R_inv,n(q; c_sel)`, then `c := c_sel + z` has the same selected
   trace as `c_sel` and lies in `A_sel^{th,cand},n(q)`;

3. for every such `z`, the exact excess is

```text
Delta_H,n,q(c_sel + z) = z^T H_n,q z;
```

4. because `H_n,q` is positive definite, any nonzero element of
   `R_inv,n(q; c_sel)` gives immediately

```text
Delta_H,n,q(c_sel + z) > 0;
```

5. on the current checked local boundary, quotient-invisibility is equivalent
   to invisibility modulo the membrane kernel direction: in a checked corrected
   local chart, two shadows have the same quotient class if and only if their
   difference lies in `span(g_mem,n(q))`;

6. therefore the current local checked theory does not leave an arbitrary
   unknown residual template. It leaves exactly the membrane-kernel template

```text
span(g_mem,n(q))
```

   on the local side;

7. consequently, the remaining existence/impossibility question is not whether
   some abstract quotient-invisible residual might exist, but whether this
   local membrane-kernel template admits a nonzero admissible lift into the
   global same-trace fiber `ker(C_center,n(q))`;

8. equivalently, the exact remaining theorem is the triviality or nontriviality
   of the class `R_inv,n(q; c_sel)` for repo-selected representatives `c_sel`.

This is sharper than `T3f`: the unresolved object is now an exact residual-class
lift problem, not only a shadow-only obstruction in prose.

## Analysis of existence versus impossibility

### 1. Exact residual objects now in play

The same-trace residual space is exact and global:

```text
R_same,n(q) = ker(C_center,n(q)).
```

The quotient-invisible candidate residual class above a selected representative
`c_sel` is exact on the current checked boundary:

```text
R_inv,n(q; c_sel)
  = { z in A_adm^th,n(q) intersect R_same,n(q)
      : Q_chk(c_sel + z) = Q_chk(c_sel) }.
```

So `T3g` is no longer a vague question about residual freedom. It is the
question whether these exact classes are trivial.

### 2. What the checked local quotient theorem really leaves open

The checked local quotient theorem does leave room on the local side for
quotient-invisible variation, but not in an arbitrary way. It leaves exactly
one currently visible local direction: the membrane kernel line `span(g_mem)`.

Thus quotient-lossiness now has a sharper meaning:
- it does not prove a nonzero global residual exists;
- but it does identify the only currently justified local template that such a
  residual could follow.

### 3. What the global admissibility side still has to decide

`H_n,q` being positive definite does not help with existence. It helps only
after a nonzero residual exists, because then `Delta_H = z^T H z > 0`
immediately.

So the real issue is not positivity but admissibility and liftability:

```text
can the local membrane-kernel template be realized by a nonzero admissible
same-trace perturbation in the global theorem-facing class?
```

The current repo/theory boundary still does not answer that.

### 4. Exact sharpened obstruction theorem

The current strongest exact obstruction is therefore:

```text
nonzero positive-excess residuals exist on the current boundary
iff
there exists c_sel in A_sel^repo,n(q) with R_inv,n(q; c_sel) != {0}.
```

Equivalently, zero-excess on the whole candidate class closes if and only if
all these residual classes are trivial.

This is sharper than `T3f` because the missing ingredient is no longer stated as
вЂњprove `Delta_H = 0`вЂќ. It is:

```text
prove or refute triviality of the exact residual-lift class R_inv,n(q; c_sel).
```

## Minimal `T3g` lemma split

### `T3g-L1`. Same-trace residual lemma

Statement:

```text
R_same,n(q) := ker(C_center,n(q)) = ker(J_0,n(q)).
```

For `z in R_same,n(q)` and `c_sel in A_sel^repo,n(q)`, one has
`J_0(c_sel + z) = J_0(c_sel)`.

Status:
- closed enough.

Main support:
- `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.8`-`1.10.10`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`;
- this note.

Verification method:
- manual derivation;
- code inspection;
- representative live clean evaluation.

### `T3g-L2`. Quotient-invisibility lemma

Statement:

```text
R_inv,n(q; c_sel)
  := { z in A_adm^th,n(q) intersect ker(C_center,n(q))
       : Q_chk(c_sel + z) = Q_chk(c_sel) }.
```

On the current checked local boundary, quotient-invisibility is equivalent to
having the checked corrected local shadow difference lie in the membrane kernel
line `span(g_mem,n(q))`.

Status:
- closed enough on the checked local quotient boundary.

Main support:
- `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.14`-`1.10.16`;
- `docs/theory/current_theory_verification_map.md` entries `V-S18`, `V-S24`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`.

Verification method:
- manual derivation;
- CAS/theory reuse;
- code inspection.

### `T3g-L3`. Residual-class comparison lemma

Statement:

If `z in R_inv,n(q; c_sel)`, then `c := c_sel + z` lies in
`A_sel^{th,cand},n(q)` and satisfies

```text
Delta_H,n,q(c) = z^T H_n,q z.
```

Hence `z != 0` implies `Delta_H,n,q(c) > 0`.

Status:
- closed enough.

Main support:
- `docs/theory/current_theory_verification_map.md` entries `V-S23`, `V-S24`;
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`;
- this note.

Verification method:
- manual derivation;
- code inspection.

### `T3g-L4`. Existence / impossibility / template lemma

Statement:

On the current repo/theory boundary, the existence question for nonzero
same-trace, quotient-invisible residuals is reduced exactly to the nontriviality
of the lift class `R_inv,n(q; c_sel)`. The only currently visible local
quotient-invisible template is the membrane kernel line `span(g_mem,n(q))`.
So the remaining theorem is whether that local template has a nonzero admissible
global lift.

Status:
- Outcome B: exact obstruction theorem.

Main support:
- `docs/theory/current_theory_verification_map.md` entries `V-S18`, `V-S24`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`;
- this note.

Verification method:
- manual derivation;
- CAS/theory reuse for the local quotient side;
- representative live clean evaluation for the global selected-section side.

### `T3g-L5`. Zero-excess consequence lemma

Statement:

```text
R_inv,n(q; c_sel) = {0} for every c_sel in A_sel^repo,n(q)
```

if and only if

```text
Delta_H,n,q(c) = 0 for every c in A_sel^{th,cand},n(q).
```

So reverse inclusion closes exactly when the residual lift class is trivial.

Status:
- closed enough as a conditional theorem package.

Main support:
- this note;
- `proof_pilots/pilot_24_t3a_selected_kernel_bridge/pilot_24_t3a_selected_kernel_bridge.md`.

Verification method:
- manual derivation;
- Lean target after the residual-class equivalence is abstracted.

## Single next bottleneck after `T3g`

The single next bottleneck is now:

```text
prove or refute that the local membrane-kernel template span(g_mem,n(q))
has no nonzero admissible global lift inside ker(C_center,n(q)).
```

Equivalently:

```text
prove or refute that R_inv,n(q; c_sel) = {0}
for every c_sel in A_sel^repo,n(q).
```

## Concrete artifact

Chosen artifact:
- this same proof-pilot note.

No new helper script was added.
No solver code was changed.
No new numerical campaign was started.

## Lean / CAS / manual split for `T3g`

Lean:
- only finite-dimensional residual-class / kernel-intersection templates once
  the exact residual class and the zero-excess equivalence are written in
  abstract form.

CAS / code inspection:
- `P_sel`, `J_0`, `H_n,q`, `ker(C_center)`, fixed-trace decomposition;
- quotient-factorization on the checked local boundary;
- the membrane-kernel line `span(g_mem)` as the exact local quotient-invisible
  direction;
- the residual-class formulation `Q_chk(c_sel + z) = Q_chk(c_sel)`.

Manual derivation:
- exact theorem scope for `T3g`;
- why positive definiteness of `H_n,q` does not decide existence;
- the exact obstruction wording as a lift problem from `span(g_mem)` to the
  global admissible same-trace fiber;
- relation of `T3g` to future long-term `T3`.

## Conservative status after `T3g`

Closed enough now:
- the `T3e` exact fiber-excess identity;
- the `T3f` shadow-only obstruction package;
- the exact same-trace residual space `ker(C_center,n(q))`;
- the exact quotient-invisible residual class `R_inv,n(q; c_sel)`;
- the reduction of the remaining zero-excess gap to triviality/nontriviality of
  that residual-lift class.

Still open:
- whether `R_inv,n(q; c_sel)` is trivial for every repo-selected representative;
- whether the local membrane-kernel template `span(g_mem)` has a nonzero
  admissible global lift;
- whether `A_sel^{th,cand} = A_sel^repo`;
- whether the selected-class kernel reading upgrades losslessly from
  `A_sel^repo` to `A_sel^{th,cand}`.

So the remaining gap is now sharper than in `T3f`: it is no longer just a
shadow-only obstruction in prose. It is an exact residual-class lift problem.
## Exact `T3h` theorem target

The exact `T3h` target is now the global lift theorem / impossibility theorem
for the local membrane-kernel line on the current checked boundary.

For fixed clean `(n, q)` and a repo-selected representative

```text
c_sel in A_sel^repo,n(q),
```

keep the exact same-trace residual space

```text
R_same,n(q) := ker(C_center,n(q)) = ker(J_0,n(q)).
```

On the current checked local boundary, write the corrected local coefficient
coordinates as `(a, b, s)` and the exact coefficient quotient map as

```text
q_coeff := [[1, 0, 0], [0, 1, 0]] : R^3_(a,b,s) -> R^2_(a,b).
```

Its kernel is the exact local membrane-kernel line

```text
K_mem,loc,n(q) := ker(q_coeff) = span(e_mem),
e_mem := (0, 0, 1)^T,
g_mem,n(q) = D_rich,eta^corr,n(q) e_mem.
```

Whenever the checked local shadows of `c_sel + z` and `c_sel` are defined in a
common corrected chart, define the checked local coefficient-difference map

```text
delta_chk,n(q; c_sel)(z)
  := chi_chk,n(q)(c_sel + z) - chi_chk,n(q)(c_sel)
  in R^3_(a,b,s).
```

Then define the exact admissible global lift class of the local membrane-kernel
line by

```text
Lift_mem,n(q; c_sel)
  := { z in A_adm^th,n(q) intersect R_same,n(q)
       : delta_chk,n(q; c_sel)(z) in K_mem,loc,n(q) }.
```

So `T3h` asks whether

```text
Lift_mem,n(q; c_sel) = {0}
```

for every repo-selected representative `c_sel`.

This is the right theorem because quotient-invisibility is exactly the
statement that the checked local coefficient difference lies in the kernel of
`q_coeff`, i.e. along `span(g_mem)`. Therefore triviality or nontriviality of
`Lift_mem` decides triviality or nontriviality of `R_inv`, hence the whole
remaining zero-excess gap.

This is still not full `T3`, not final physical criticality, and not a
collapse to `B_red` / `B_mix`.

## Outcome reached in this turn

Outcome reached:

```text
Outcome B.
```

No impossibility theorem and no explicit nonzero global lift are proved. The
strongest new result is the exact local-to-global lift formulation:

```text
Lift_mem,n(q; c_sel) = R_inv,n(q; c_sel)
```

and, on the current linear tangent boundary where `delta_chk,n(q; c_sel)` is
read in the corrected checked local coefficient chart,

```text
Lift_mem,n(q; c_sel)
  = ker(q_coeff o delta_chk,n(q; c_sel)
        |_(A_adm^th,n(q) intersect ker(C_center,n(q)))).
```

So the remaining question is no longer just whether some quotient-invisible
same-trace residual survives. It is whether this exact kernel is trivial.

## Strongest result obtained about admissible global lifts of `span(g_mem)`

### Theorem `T3h`

For fixed clean `(n, q)`, on the current repository/theory boundary:

1. the exact local quotient map on corrected coefficient coordinates is

```text
q_coeff = [[1, 0, 0], [0, 1, 0]],
ker(q_coeff) = span(e_mem),
g_mem = D_rich,eta^corr e_mem;
```

2. quotient-preserving chart changes keep `q_coeff` unchanged on quotient
   coordinates, so the local membrane-kernel line is the same exact current
   local quotient kernel in every corrected checked chart;

3. the exact admissible global lift class of that local kernel above a
   repo-selected representative `c_sel` is

```text
Lift_mem,n(q; c_sel)
  := { z in A_adm^th,n(q) intersect ker(C_center,n(q))
       : delta_chk,n(q; c_sel)(z) in span(e_mem) };
```

4. this class is exactly the same object as the quotient-invisible residual
   class:

```text
Lift_mem,n(q; c_sel) = R_inv,n(q; c_sel);
```

5. equivalently,

```text
z in Lift_mem,n(q; c_sel)
iff
q_coeff delta_chk,n(q; c_sel)(z) = 0;
```

6. on the current linear tangent boundary this becomes the exact kernel test

```text
Lift_mem,n(q; c_sel)
  = ker(q_coeff o delta_chk,n(q; c_sel)
        |_(A_adm^th,n(q) intersect ker(C_center,n(q))));
```

7. hence a nonzero admissible global lift exists if and only if that kernel is
   nontrivial; if the kernel is trivial for every `c_sel`, then
   `R_inv = {0}` and the zero-excess theorem closes.

This is sharper than `T3g`: the remaining object is now an exact preimage /
kernel problem for the checked local quotient map, not just an exact set
written in ambient prose.

## Comparison of local `span(g_mem)` with the global lift space

### 1. What is exact on the local side

The current checked local boundary already closes the local quotient kernel
exactly:

- `q_coeff = [[1,0,0],[0,1,0]]`;
- `ker(q_coeff) = span(e_mem)`;
- under the corrected jet embedding, that kernel is exactly `span(g_mem)`.

So the local quotient-invisible direction is not ambiguous any more.

### 2. What is exact on the global side

The exact global same-trace residual space is already closed:

```text
R_same,n(q) = ker(C_center,n(q)) = ker(J_0,n(q)).
```

Global admissibility still means

```text
z in A_adm^th,n(q) intersect R_same,n(q).
```

So the only unresolved part is not the trace constraint and not the positivity
of `H_n,q`. It is the local-to-global lift relation encoded by `delta_chk`.

### 3. Exact lift comparison now available

The checked local coefficient-difference map gives the sharpest exact
comparison now justified on the repository boundary:

```text
delta_chk,n(q; c_sel)
  : A_adm^th,n(q) intersect ker(C_center,n(q)) -> R^3_(a,b,s).
```

Then:

- impossibility of nonzero global lifts is exactly the statement
  `ker(q_coeff o delta_chk) = {0}`;
- existence of a nonzero admissible global lift is exactly the statement that
  this kernel is nontrivial;
- the lift problem is therefore a genuine local-to-global kernel question.

### 4. What remains undecided

The current repo-selected structure does not yet give a closed explicit theorem
for the operator `delta_chk,n(q; c_sel)` on the admissible same-trace global
residual space. So the current repository boundary does not yet decide:

- whether every local membrane-kernel direction lifts globally;
- whether any nonzero such lift exists at all;
- whether such lifts would be unique if they exist.

Thus the obstruction is now sharper than in `T3g`: it is not only the
nontriviality of a named class, but the still-open kernel problem for the exact
checked local lift map.

## Minimal `T3h` lemma split

### `T3h-L1`. Global same-trace residual space lemma

Statement:

```text
R_same,n(q) := ker(C_center,n(q)) = ker(J_0,n(q)).
```

For `z in R_same,n(q)` and `c_sel in A_sel^repo,n(q)`, one has
`J_0(c_sel + z) = J_0(c_sel)`.

Status:
- closed enough.

Main support:
- `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.8`-`1.10.10`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`;
- this note.

Verification method:
- manual derivation;
- code inspection;
- representative live clean evaluation.

### `T3h-L2`. Local membrane-kernel image lemma

Statement:

On the current checked local boundary, the corrected local coefficient quotient
map is

```text
q_coeff = [[1, 0, 0], [0, 1, 0]],
ker(q_coeff) = span(e_mem),
g_mem = D_rich,eta^corr e_mem.
```

So `span(g_mem)` is exactly the local quotient-invisible direction.

Status:
- closed enough on the checked local quotient boundary.

Main support:
- `docs/theory/vyvod_uravneniy_updated17.md` sections `1.10.14`-`1.10.16`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
- `docs/theory/current_theory_verification_map.md` entries `V-S18`, `V-S25`.

Verification method:
- CAS/theory reuse;
- code inspection;
- representative helper evaluation.

### `T3h-L3`. Lift-class definition / comparison lemma

Statement:

For fixed `c_sel in A_sel^repo,n(q)`, define

```text
Lift_mem,n(q; c_sel)
  := { z in A_adm^th,n(q) intersect ker(C_center,n(q))
       : delta_chk,n(q; c_sel)(z) in span(e_mem) }.
```

Then

```text
Lift_mem,n(q; c_sel) = R_inv,n(q; c_sel),
```

equivalently

```text
Lift_mem,n(q; c_sel)
  = ker(q_coeff o delta_chk,n(q; c_sel)
        |_(A_adm^th,n(q) intersect ker(C_center,n(q))))
```

on the current linear tangent boundary.

Status:
- closed enough as the exact reformulation step.

Main support:
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`;
- this note.

Verification method:
- manual derivation;
- code inspection;
- CAS/theory reuse for the quotient map.

### `T3h-L4`. Impossibility / existence / template lemma

Statement:

The existence/impossibility question for nonzero admissible global lifts of the
local membrane-kernel line is reduced exactly to triviality or nontriviality of

```text
ker(q_coeff o delta_chk,n(q; c_sel)
    |_(A_adm^th,n(q) intersect ker(C_center,n(q)))).
```

No theorem currently proves that this kernel vanishes, and no explicit nonzero
element is currently constructed.

Status:
- Outcome B: exact obstruction theorem.

Main support:
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`;
- this note.

Verification method:
- manual derivation;
- code inspection;
- representative helper evaluation for the closed global/local support pieces.

### `T3h-L5`. Zero-excess consequence lemma

Statement:

```text
Lift_mem,n(q; c_sel) = {0} for every c_sel in A_sel^repo,n(q)
```

if and only if

```text
R_inv,n(q; c_sel) = {0} for every c_sel in A_sel^repo,n(q),
```

hence if and only if

```text
Delta_H,n,q(c) = 0 for every c in A_sel^{th,cand},n(q).
```

Status:
- closed enough as a conditional theorem package.

Main support:
- this note;
- `proof_pilots/pilot_24_t3a_selected_kernel_bridge/pilot_24_t3a_selected_kernel_bridge.md`.

Verification method:
- manual derivation;
- Lean target after the lift-map abstraction is isolated.

## Single next bottleneck after `T3h`

The single next bottleneck is now:

```text
construct or control the checked local lift-difference map
delta_chk,n(q; c_sel)
on A_adm^th,n(q) intersect ker(C_center,n(q))
well enough to decide whether
ker(q_coeff o delta_chk,n(q; c_sel)) = {0}.
```

Equivalently:

```text
prove or refute that the exact global membrane-lift class
Lift_mem,n(q; c_sel)
is trivial for every repo-selected representative.
```

## Lean / CAS / manual split for `T3h`

Lean:
- only finite-dimensional kernel/image/lift templates once the exact
  local-to-global lift map and the kernel criterion are written in abstract
  form.

CAS / code inspection:
- `P_sel`, `J_0`, `H_n,q`, `ker(C_center)`, fixed-trace fibers;
- the corrected local coefficient quotient map `q_coeff`;
- the exact local membrane-kernel line `ker(q_coeff) = span(e_mem)` and its jet
  image `span(g_mem)`;
- quotient-preserving chart invariance on the current checked boundary;
- the lift-map formulation through `delta_chk,n(q; c_sel)`.

Manual derivation:
- exact theorem scope for `T3h`;
- the exact preimage / kernel wording for the global lift problem;
- why positivity of `H_n,q` still does not decide existence;
- relation of `T3h` to future long-term `T3`.

## Conservative status after `T3h`

Closed enough now:
- the `T3g` exact residual-lift class;
- the exact local coefficient quotient kernel
  `ker(q_coeff) = span(e_mem)` on the current checked boundary;
- the exact membrane-jet line `span(g_mem)`;
- the exact global membrane-lift class `Lift_mem,n(q; c_sel)`;
- the reformulation
  `Lift_mem = R_inv = ker(q_coeff o delta_chk)` on the current linear tangent
  boundary.

Still open:
- whether `Lift_mem,n(q; c_sel)` is trivial for every repo-selected
  representative;
- whether the checked local lift-difference map `delta_chk,n(q; c_sel)` has
  nontrivial kernel on the admissible same-trace global residual space;
- whether `A_sel^{th,cand} = A_sel^repo`;
- whether the selected-class kernel reading upgrades losslessly from
  `A_sel^repo` to `A_sel^{th,cand}`.

So the remaining gap is now sharper than in `T3g`: it is an exact
local-to-global kernel/preimage problem for the membrane-kernel lift class.
## Exact `T3i` theorem target

The exact `T3i` target is now the injectivity / kernel-control theorem for the
projected checked local lift map on the admissible same-trace residual domain.

For fixed clean `(n, q)` and a repo-selected representative

```text
c_sel in A_sel^repo,n(q),
```

keep the exact admissible same-trace residual domain

```text
D_res,n(q) := A_adm^th,n(q) intersect ker(C_center,n(q))
           = A_adm^th,n(q) intersect ker(J_0,n(q)).
```

Because the checked local coefficient difference may be available only when both
checked local shadows are defined in a common corrected chart, also define the
checked-boundary domain

```text
D_res,chk,n(q; c_sel)
  := { z in D_res,n(q) : delta_chk,n(q; c_sel)(z) is defined }.
```

Then define the projected checked local lift map

```text
Phi_chk,n(q; c_sel)
  := q_coeff o delta_chk,n(q; c_sel)
  : D_res,chk,n(q; c_sel) -> R^2_(a,b).
```

So `T3i` asks whether

```text
ker(Phi_chk,n(q; c_sel)) = {0}
```

for every repo-selected representative `c_sel`.

This is the right theorem because

```text
Lift_mem,n(q; c_sel) = ker(Phi_chk,n(q; c_sel)) = R_inv,n(q; c_sel),
```

so injectivity / trivial kernel of `Phi_chk` is exactly triviality of the
remaining lift class, hence exactly closure of the zero-excess gap.

This is still not full `T3`, not final physical criticality, and not a
collapse to `B_red` / `B_mix`.

## Outcome reached in this turn

Outcome reached:

```text
Outcome D.
```

No injectivity theorem and no explicit nonzero kernel element are proved. The
strongest new result is a sharper operator-level obstruction theorem:

```text
T3i is not yet a closed rank/nullity theorem because the repository still does
not package an explicit global checked local coefficient-extraction operator
chi_chk,n(q)
on D_res,n(q)
from which delta_chk,n(q; c_sel) would become a fixed linear map.
```

So the bottleneck is now sharper than in `T3h`: not merely вЂњdecide the kernelвЂќ,
but construct or control the exact operator whose kernel is being tested.

## Strongest exact result obtained about injectivity / trivial-kernel of the projected lift map

### Theorem `T3i`

For fixed clean `(n, q)`, on the current repository/theory boundary:

1. the exact admissible same-trace residual domain is

```text
D_res,n(q) = A_adm^th,n(q) intersect ker(C_center,n(q));
```

2. the exact projected checked local lift map is

```text
Phi_chk,n(q; c_sel)
  := q_coeff o delta_chk,n(q; c_sel)
  : D_res,chk,n(q; c_sel) -> R^2_(a,b);
```

3. its kernel is exactly the current global membrane-lift class:

```text
ker(Phi_chk,n(q; c_sel))
  = Lift_mem,n(q; c_sel)
  = R_inv,n(q; c_sel);
```

4. the local quotient map `q_coeff` is exactly linear and chart-invariant under
   quotient-preserving chart changes on the checked local boundary:

```text
q_coeff = [[1,0,0],[0,1,0]],
q_coeff S_(ell1,ell2) = q_coeff;
```

5. by definition `delta_chk,n(q; c_sel)(z)` is affine in the base point
   `c_sel`; if an explicit global checked local coefficient-extraction operator
   `chi_chk,n(q)` existed on `D_res,n(q)`, then one would have

```text
delta_chk,n(q; c_sel)(z) = chi_chk,n(q)(z),
Phi_chk,n(q; c_sel) = q_coeff o chi_chk,n(q),
```

   so the kernel question would be independent of `c_sel` and would reduce to a
   genuine linear injectivity/rank theorem on `D_res,n(q)`;

6. the current repository does not yet provide that global operator or an
   equivalent explicit control of `delta_chk` on the whole residual domain;

7. therefore injectivity is not yet a closed theorem, but the exact missing
   ingredient is now isolated more sharply than before.

This is sharper than `T3h`: the obstruction is now operator-level rather than
merely class-level.

## Comparison of the map and domain

### 1. Exact domain now in play

The kernel is not being tested on an abstract ambient space. It is being tested
on

```text
D_res,n(q) = A_adm^th,n(q) intersect ker(C_center,n(q)),
```

and, on the current checked boundary where the local shadow is actually
available,

```text
D_res,chk,n(q; c_sel)
  := { z in D_res,n(q) : delta_chk,n(q; c_sel)(z) is defined }.
```

### 2. Exact projected map now in play

The projected map is

```text
Phi_chk,n(q; c_sel) = q_coeff o delta_chk,n(q; c_sel).
```

This is the exact map whose kernel is the remaining lift class. So the zero-
excess question is now exactly an injectivity question for `Phi_chk`.

### 3. What is controlled and what is not

What is already controlled exactly:

- `q_coeff` is linear;
- `ker(q_coeff) = span(e_mem)`;
- `q_coeff` is unchanged by quotient-preserving chart changes;
- `ker(Phi_chk) = Lift_mem = R_inv`.

What is not yet controlled as a closed theorem:

- an explicit global operator `chi_chk,n(q)` on `D_res,n(q)`;
- hence linearity / basepoint-independence of `delta_chk,n(q; c_sel)` on the
  full global admissible residual domain;
- hence a closed rank/nullspace theorem for `Phi_chk`.

### 4. Sharpest current injectivity reading

So the exact current injectivity question is now conditional in the strongest
currently justified sense:

```text
if a global linear checked local coefficient-extraction operator chi_chk,n(q)
exists on D_res,n(q),
then T3i reduces to injectivity of q_coeff o chi_chk,n(q)
on D_res,n(q),
independent of c_sel.
```

The current repo boundary still does not close that antecedent.

## Minimal `T3i` lemma split

### `T3i-L1`. Projected lift-map lemma

Statement:

```text
Phi_chk,n(q; c_sel) := q_coeff o delta_chk,n(q; c_sel)
```

on `D_res,chk,n(q; c_sel)`.

`q_coeff` is exactly linear and quotient-preserving-chart invariant on the
checked local boundary. `delta_chk` is affine in `c_sel` by definition, and it
would become linear and basepoint-independent if an explicit global linear
`chi_chk,n(q)` were available.

Status:
- partial.

Verification method:
- code inspection;
- manual derivation;
- CAS/theory reuse for the local quotient chart.

### `T3i-L2`. Admissible residual domain lemma

Statement:

```text
D_res,n(q) := A_adm^th,n(q) intersect ker(C_center,n(q)),
D_res,chk,n(q; c_sel)
  := { z in D_res,n(q) : delta_chk,n(q; c_sel)(z) is defined }.
```

Status:
- closed enough.

Verification method:
- manual derivation;
- code inspection.

### `T3i-L3`. Kernel = lift-class lemma

Statement:

```text
ker(Phi_chk,n(q; c_sel))
  = Lift_mem,n(q; c_sel)
  = R_inv,n(q; c_sel).
```

So injectivity of `Phi_chk` on the checked residual domain is exactly
triviality of the remaining lift class.

Status:
- closed enough.

Verification method:
- manual derivation;
- code inspection.

### `T3i-L4`. Exact obstruction / missing-operator lemma

Statement:

The current repository does not yet package an explicit global checked local
coefficient-extraction operator `chi_chk,n(q)` on `D_res,n(q)` from which the
projected lift map would become a fixed linear map independent of `c_sel`.
Therefore injectivity is not yet a closed rank/nullspace theorem on the global
admissible same-trace residual domain.

Status:
- Outcome D: exact missing ingredient isolated more sharply.

Verification method:
- code inspection;
- manual derivation;
- repository search showing `delta_chk` is currently only a theorem-facing map
  placeholder, not an implemented global operator.

### `T3i-L5`. Zero-excess consequence lemma

Statement:

If `Phi_chk,n(q; c_sel)` is injective on the relevant residual domain for every
repo-selected representative `c_sel`, then

```text
Lift_mem,n(q; c_sel) = {0}
```

for all such `c_sel`, hence

```text
R_inv,n(q; c_sel) = {0},
Delta_H,n,q(c) = 0 on A_sel^{th,cand},n(q).
```

Status:
- closed enough as a conditional theorem package.

Verification method:
- manual derivation;
- Lean target after the map/domain abstraction is isolated.

## Single next bottleneck after `T3i`

The single next bottleneck is now:

```text
construct or control an explicit global checked local coefficient-extraction
operator chi_chk,n(q)
on D_res,n(q) = A_adm^th,n(q) intersect ker(C_center,n(q))
strongly enough that Phi_chk = q_coeff o chi_chk becomes a genuine linear map
whose kernel can be decided.
```

## Lean / CAS / manual split for `T3i`

Lean:
- only finite-dimensional injectivity/kernel templates once the exact map and
  domain are abstracted in linear form.

CAS / code inspection:
- `q_coeff`, `e_mem`, `g_mem`, quotient-preserving chart invariance,
  `P_sel`, `J_0`, `ker(C_center)`, and the current repository status of
  `delta_chk` / `chi_chk`.

Manual derivation:
- exact theorem scope for `T3i`;
- the operator-level obstruction wording;
- relation of `T3i` to future long-term `T3`.

## Conservative status after `T3i`

Closed enough now:
- the exact admissible same-trace residual domain `D_res,n(q)`;
- the projected checked local map `Phi_chk,n(q; c_sel) = q_coeff o delta_chk,n(q; c_sel)`;
- the exact identity `ker(Phi_chk) = Lift_mem = R_inv`;
- the chart-invariant local quotient structure carried by `q_coeff`.

Still open:
- a global explicit linear operator `chi_chk,n(q)` on `D_res,n(q)`;
- hence a closed injectivity/rank theorem for `Phi_chk`;
- hence triviality of `Lift_mem` and the final reverse-inclusion closure.

So the remaining gap is now sharper than in `T3h`: it is an operator-construction/control gap for the projected checked local lift map.


## Exact `T3j` theorem target

The exact `T3j` target is the construction / control theorem for the global
checked-local coefficient-extraction operator.

For fixed clean `(n, q)`, the desired object is a theorem-facing linear map

```text
chi_chk,n(q) : D_res,n(q) -> R^3_(a,b,s),
```

with

```text
D_res,n(q) := A_adm^th,n(q) intersect ker(C_center,n(q)),
```

such that, whenever the checked local shadows are defined in a common corrected
chart, one has

```text
delta_chk,n(q; c_sel)(z) = chi_chk,n(q)(z)
```

for all relevant `z`, hence

```text
Phi_chk,n(q; c_sel) = q_coeff o chi_chk,n(q)
```

independently of `c_sel`.

This is the right theorem because it would turn the remaining lift problem into
a genuine linear kernel question on `D_res,n(q)`. It is still not full `T3`,
not final physical criticality, and not a collapse to `B_red` / `B_mix`.

## Outcome reached in this turn

Outcome reached:

```text
Outcome D.
```

The strongest current result is a partial construction on the checked local
corrected selected family together with an exact obstruction to extending it to
the full admissible same-trace residual domain.

More precisely:

1. there is an explicit linear coefficient-extraction operator on the visible
   corrected checked local family

```text
Xi_sel,corr^(1,eta),n(q) = im(D_rich,eta^corr,n(q));
```

2. this operator is not theorem-facing canonical at the full 3-coordinate
   `(a,b,s)` level because the membrane coordinate is chart-dependent under
   quotient-preserving chart changes;
3. after projection by `q_coeff`, the dependence on the chart disappears
   exactly;
4. what is still missing is a global checked-local shadow map from
   `D_res,n(q)` into the checked local corrected family (or an equivalent exact
   control theorem), not the existence of a local coefficient extractor itself.

So `T3j` sharpens the obstruction from вЂњmissing `chi_chk`вЂќ to:

```text
the local checked coefficient extractor exists on the corrected checked local
family, but the repository still does not package the global checked-local
shadow map needed to compose it into a theorem-facing operator on D_res,n(q).
```

## Current status of `delta_chk`

Retrospective clarification:

In the `T3h` / `T3i` blocks the symbol `chi_chk,n(q)` was used heuristically as
the coefficient extractor behind `delta_chk,n(q; c_sel)`. What is actually
available on the current checked boundary is weaker and more precise:

- a chart-level linear coefficient extractor on the corrected checked local
  family;
- a chart-invariant projected extractor after composition with `q_coeff`;
- but not yet a global theorem-facing operator on `D_res,n(q)`.

So `delta_chk,n(q; c_sel)` is best read as a basepoint-difference of checked
local coefficient vectors whenever the two compared shadows are realized in a
common corrected chart. Its dependence on `c_sel` is therefore not the
fundamental issue; the fundamental issue is the absence of a global shadow map
from `D_res,n(q)` into that checked local corrected family.

## Strongest exact result obtained about construction/control of `chi_chk,n(q)`

### Theorem `T3j`

For fixed clean `(n, q)`, on the current repository/theory boundary:

1. the visible checked local corrected family is the exact 3D plane

```text
Xi_sel,corr^(1,eta),n(q) = im(D_rich,eta^corr,n(q)),
```

with

```text
D_rich,eta^corr,n(q)
 = [[1, 0, 0],
    [0, 1, 0],
    [0, 0, 0],
    [0, lambda_c - eta, 0],
    [0, 0, 1],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]];
```

2. there is an explicit linear left inverse on the visible checked local chart,
   namely

```text
L_vis,n(q)
 := [[1, 0, 0, 0, 0, 0, 0, 0],
     [0, 1, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 1, 0, 0, 0]],
```

   with

```text
L_vis,n(q) D_rich,eta^corr,n(q) = I_3;
```

3. hence the explicit local checked-local coefficient-extraction operator

```text
chi_chk,vis,n(q)
  := L_vis,n(q) |_(Xi_sel,corr^(1,eta),n(q))
  : Xi_sel,corr^(1,eta),n(q) -> R^3_(a,b,s)
```

   is well-defined and linear;

4. after any quotient-preserving chart change

```text
S_(ell1,ell2)
 := [[1, 0, 0],
     [0, 1, 0],
     [ell1, ell2, 1]],
```

   the corresponding local extractor is

```text
chi_chk,(ell1,ell2),n(q)
  := S_(ell1,ell2)^(-1) chi_chk,vis,n(q),
```

   so the full 3-coordinate extractor is chart-dependent, but

```text
q_coeff S_(ell1,ell2) = q_coeff = q_coeff S_(ell1,ell2)^(-1),
```

   hence

```text
q_coeff o chi_chk,(ell1,ell2),n(q)
 = q_coeff o chi_chk,vis,n(q);
```

5. if one defines

```text
L_amp := [[1,0,0,0],[0,1,0,0]],
```

   then on `Xi_sel,corr^(1,eta),n(q)` one has the exact factorization

```text
q_coeff o chi_chk,vis,n(q)
 = L_amp o Pi_eta_to_J0;
```

   equivalently, on the corrected checked local family the projected local
   coefficients `(a,b)` are canonically the first two `J_0` coordinates and are
   independent of the membrane representative;

6. therefore the projected checked-local coefficient extractor is already
   canonically controlled on the checked local corrected family;

7. what the current repository still does not package is a global checked-local
   shadow map

```text
Sh_chk,n(q) : D_res,n(q) -> Xi_sel,corr^(1,eta),n(q)
```

   or an equivalent explicit theorem that would let one compose
   `chi_chk,vis,n(q)` into a global theorem-facing operator on `D_res,n(q)`;

8. therefore a full global operator

```text
chi_chk,n(q) : D_res,n(q) -> R^3_(a,b,s)
```

   is not yet closed, but the precise missing ingredient is now sharper than in
   `T3i`.

## Repackaged lift problem through the local extractor

The strongest currently justified linearization is conditional but exact:

If a global checked-local shadow map

```text
Sh_chk,n(q) : D_res,n(q) -> Xi_sel,corr^(1,eta),n(q)
```

is constructed or controlled so that

```text
delta_chk,n(q; c_sel)(z)
  = chi_chk,vis,n(q)(Sh_chk,n(q)(z)),
```

then one can set

```text
chi_chk,n(q) := chi_chk,vis,n(q) o Sh_chk,n(q)
```

and obtain

```text
Phi_chk,n(q; c_sel) = q_coeff o chi_chk,n(q),
Lift_mem,n(q; c_sel) = ker(q_coeff o chi_chk,n(q)),
```

independently of `c_sel`.

At the current boundary this is not yet a closed theorem because `Sh_chk,n(q)`
is exactly the missing operator-level bridge from global admissible same-trace
residuals to the checked local corrected family.

## Minimal `T3j` lemma split

### `T3j-L1`. Current `delta_chk` structure lemma

Statement:

`delta_chk,n(q; c_sel)(z)` is best read as the difference of checked local
coefficient vectors in a common corrected chart. On the local corrected-family
side it is linear in the local jet variable; its apparent basepoint dependence
comes from comparing two global objects through a not-yet-packaged checked local
shadow map.

Status:
- closed enough.

Verification method:
- code inspection;
- manual derivation;
- CAS/theory reuse from the checked local chart package.

### `T3j-L2`. Local-operator construction lemma

Statement:

On

```text
Xi_sel,corr^(1,eta),n(q) = im(D_rich,eta^corr,n(q)),
```

the explicit visible-chart extractor

```text
chi_chk,vis,n(q) := L_vis,n(q)|_(Xi_sel,corr^(1,eta),n(q))
```

is linear and satisfies

```text
chi_chk,vis,n(q) D_rich,eta^corr,n(q) = I_3.
```

Status:
- closed enough.

Verification method:
- CAS;
- code inspection;
- manual derivation.

### `T3j-L3`. Projected local invariance lemma

Statement:

For every quotient-preserving chart change `S_(ell1,ell2)`, the full local
extractor changes by `S_(ell1,ell2)^(-1)`, but

```text
q_coeff o chi_chk,(ell1,ell2),n(q)
 = q_coeff o chi_chk,vis,n(q)
 = L_amp o Pi_eta_to_J0
```

on `Xi_sel,corr^(1,eta),n(q)`.

So the projected local checked-local coefficient extractor is canonical even
though the membrane coordinate is not.

Status:
- closed enough.

Verification method:
- CAS;
- code inspection;
- manual derivation.

### `T3j-L4`. Exact obstruction / partial-domain lemma

Statement:

The repository currently provides the checked local extractor only on the strict
checked local corrected-family domain

```text
Xi_sel,corr^(1,eta),n(q),
```

not as a theorem-facing operator on the full global admissible same-trace
residual domain

```text
D_res,n(q) = A_adm^th,n(q) intersect ker(C_center,n(q)).
```

What is missing is a global checked-local shadow map

```text
Sh_chk,n(q) : D_res,n(q) -> Xi_sel,corr^(1,eta),n(q)
```

or an equivalent exact control theorem.

Status:
- Outcome D: partial construction with exact remaining gap.

Verification method:
- code inspection;
- manual derivation;
- repository search for a global checked-local shadow operator.

### `T3j-L5`. Consequence lemma for the next injectivity step

Statement:

If the missing global checked-local shadow map `Sh_chk,n(q)` is constructed or
controlled, then the lift problem becomes the genuine linear kernel problem

```text
Lift_mem,n(q; c_sel) = ker(q_coeff o chi_chk,n(q)),
```

independent of `c_sel`, with

```text
chi_chk,n(q) := chi_chk,vis,n(q) o Sh_chk,n(q).
```

Status:
- closed enough as a conditional theorem package.

Verification method:
- manual derivation;
- Lean target after the composition template is abstracted.

## Single next bottleneck after `T3j`

The single next bottleneck is now:

```text
construct or control a global checked-local shadow map
Sh_chk,n(q) : D_res,n(q) -> Xi_sel,corr^(1,eta),n(q)
strongly enough that chi_chk,n(q) := chi_chk,vis,n(q) o Sh_chk,n(q)
is well-defined and the kernel of q_coeff o chi_chk,n(q) can be decided.
```

So the bottleneck is no longer the absence of a local coefficient extractor; it
is the missing global bridge from admissible same-trace residuals to the
checked local corrected family.

## Lean / CAS / manual split for `T3j`

Lean:
- only finite-dimensional linear-map / composition / kernel templates once the
  global shadow map and `chi_chk` composition are abstracted.

CAS / code inspection:
- `D_rich,eta^corr`, `L_vis`, `q_coeff`, `e_mem`, `g_mem`,
  quotient-preserving chart changes, and the factorization
  `q_coeff o chi_chk,vis = L_amp o Pi_eta_to_J0` on the checked local corrected
  family.

Manual derivation:
- exact theorem scope for `T3j`;
- the distinction between the local chart-level extractor and the still-missing
  global theorem-facing operator on `D_res,n(q)`;
- relation of `T3j` to the future injectivity step and long-term `T3`.

## Conservative status after `T3j`

Closed enough now:
- the explicit checked local corrected-family extractor `chi_chk,vis,n(q)`;
- its chart-transformation law under quotient-preserving changes;
- the chart-invariant projected extractor `q_coeff o chi_chk,vis,n(q)`;
- the exact factorization of that projected extractor through `Pi_eta_to_J0`.

Still open:
- a global checked-local shadow map `Sh_chk,n(q)` on `D_res,n(q)`;
- hence a global theorem-facing operator `chi_chk,n(q)` on `D_res,n(q)`;
- hence the fixed linear kernel theorem for `q_coeff o chi_chk,n(q)`.

So the remaining gap is now sharper than in `T3i`: it is a missing
global-shadow bridge, not the absence of the local checked-local coefficient
extractor itself.


## Exact `T3k` theorem target

The exact `T3k` target is the construction / control theorem for the global
checked-local shadow map

```text
Sh_chk,n(q) : D_res,n(q) -> Xi_sel,corr^(1,eta),n(q),
```

with

```text
D_res,n(q) := A_adm^th,n(q) intersect ker(C_center,n(q)),
Xi_sel,corr^(1,eta),n(q) := im(D_rich,eta^corr,n(q)),
```

such that on the current tangent boundary the checked local difference can be
read through `Sh_chk,n(q)` and the remaining lift problem becomes a
basepoint-independent linear kernel question after composition with the already
available local extractor `chi_chk,vis,n(q)`.

Equivalently, `T3k` asks whether one can reach a theorem of the form

```text
Phi_chk,n(q) = q_coeff o chi_chk,vis,n(q) o Sh_chk,n(q),
Lift_mem,n(q) = ker(q_coeff o chi_chk,vis,n(q) o Sh_chk,n(q)),
```

on the raw same-trace admissible residual domain.

This is still not full `T3`, not final physical criticality, and not a collapse
to `B_red` / `B_mix`.

## Outcome reached in this turn

Outcome reached:

```text
Outcome C.
```

The strongest result is an exact obstruction theorem.

A theorem-facing global shadow map on the raw same-trace domain would be too
strong on the current boundary: compatibility with the already closed quotient
reading forces any such map to land in the membrane line, so after projection by
`q_coeff` it collapses to zero and cannot recover a nontrivial projected lift
map.

So the bottleneck is sharper than after `T3j`: the missing object is not a raw
shadow map on `D_res,n(q)` itself, but a basepoint-relative checked-local
representative-difference map on ambient candidate-class objects before quotient
collapse, or an equivalent theorem that kills the membrane amplitude on the
same-trace residual class.

## Current status of the checked-local shadow data

What is already canonical on the current checked boundary:

1. the checked local theorem-facing object is the quotient

```text
im(D_rich,eta^corr,n(q)) / span(g_mem,n(q));
```

2. on the corrected local family the projected coefficient extractor is exactly

```text
q_coeff o chi_chk,vis,n(q) = L_amp o Pi_eta_to_J0;
```

3. the raw same-trace residual domain satisfies

```text
D_res,n(q) subset ker(J_0,n(q)).
```

Therefore every currently justified canonical checked-local selected invariant of
an element `z in D_res,n(q)` already lies in the zero quotient class.

What is not canonical:

- a representative-level membrane coordinate inside that zero quotient class;
- hence a theorem-facing map into the full corrected family rather than the
  quotient;
- hence a raw global shadow map `Sh_chk,n(q)` on `D_res,n(q)` with values in the
  full 3D corrected family.

So the checked-local data are canonical only modulo `span(g_mem)`, while the
same-trace domain already kills the quotient coordinates `(a,b)`.

## Strongest exact result obtained about construction/control of `Sh_chk,n(q)`

### Theorem `T3k`

For fixed clean `(n, q)`, on the current repository/theory boundary:

1. on the corrected checked local family one already has the exact factorization

```text
q_coeff o chi_chk,vis,n(q) = L_amp o Pi_eta_to_J0;
```

2. if a theorem-facing global shadow map

```text
Sh_chk,n(q) : D_res,n(q) -> Xi_sel,corr^(1,eta),n(q)
```

   existed and were compatible with the current canonical quotient reading, then
   for every `z in D_res,n(q)` one would have

```text
q_coeff o chi_chk,vis,n(q)(Sh_chk,n(q)(z)) = 0,
```

   because `z in ker(J_0,n(q))` and the quotient coordinates on the corrected
   family are exactly the selected-trace coordinates;

3. equivalently, every such compatible `Sh_chk,n(q)(z)` must lie in the zero
   quotient class of the corrected family, hence in the membrane line

```text
span(g_mem,n(q)) = D_rich,eta^corr,n(q) span(e_mem);
```

4. therefore any compatible raw global shadow map on `D_res,n(q)` is
   necessarily of the form

```text
Sh_chk,n(q)(z) = sigma_chk,n(q)(z) g_mem,n(q)
```

   for some scalar membrane-selector candidate

```text
sigma_chk,n(q) : D_res,n(q) -> R;
```

5. consequently

```text
q_coeff o chi_chk,vis,n(q) o Sh_chk,n(q) = 0
```

   on `D_res,n(q)`;

6. so a basepoint-independent factorization

```text
Phi_chk,n(q) = q_coeff o chi_chk,vis,n(q) o Sh_chk,n(q)
```

   on the raw same-trace residual domain would force `Phi_chk,n(q) = 0`
   identically;

7. this shows that the naive `T3j` shadow-map target on `D_res,n(q)` is not the
   right remaining global object on the current boundary;

8. the current checked local quotient theorem also says that no intrinsic
   canonical representative selector is presently justified inside a quotient
   class: chart-zero rules are chart-dependent, orthogonality rules are
   metric-dependent, and imported `H`-selection is extrinsic to the local
   theorem.

Therefore the exact obstruction is now sharp:

```text
current checked-boundary data define only the zero quotient shadow on D_res,n(q),
not a canonical representative in that zero quotient class.
```

## Repackaged lift problem through the sharpest exact substitute

The sharpest exact substitute is not a raw shadow map on `D_res,n(q)`, but a
basepoint-relative representative-difference object on ambient candidate-class
pairs before quotient collapse.

Concretely:

- a raw `Sh_chk,n(q)` on `D_res,n(q)` would land in `span(g_mem,n(q))` and so
  would satisfy
  `q_coeff o chi_chk,vis,n(q) o Sh_chk,n(q) = 0`;
- therefore it cannot by itself encode the nontrivial projected lift question;
- any future nontrivial factorization of `Phi_chk` must act on a pairwise or
  ambient shadow-difference object, not just on the raw same-trace residual as a
  standalone quotient-compatible shadow.

So the exact remaining global problem is now:

```text
construct or control a theorem-facing basepoint-relative checked-local
representative-difference map on ambient candidate-class objects before
quotient collapse,
or prove an exact theorem that every admissible same-trace membrane amplitude
must vanish.
```

## Minimal `T3k` lemma split

### `T3k-L1`. Checked-local shadow-data lemma

Statement:

On the corrected checked local family one has

```text
q_coeff o chi_chk,vis,n(q) = L_amp o Pi_eta_to_J0,
```

so the quotient coordinates `(a,b)` are exactly the selected-trace coordinates.

Status:
- closed enough.

Verification method:
- CAS;
- code inspection;
- manual derivation.

### `T3k-L2`. Zero-quotient-on-same-trace lemma

Statement:

Because

```text
D_res,n(q) = A_adm^th,n(q) intersect ker(C_center,n(q))
         subset ker(J_0,n(q)),
```

any theorem-facing checked-local shadow compatible with the current quotient
reading must project to zero under `q_coeff o chi_chk,vis`.

Status:
- closed enough.

Verification method:
- manual derivation;
- code inspection;
- theory reuse from the local quotient package.

### `T3k-L3`. Membrane-line factorization lemma

Statement:

Any compatible global shadow map

```text
Sh_chk,n(q) : D_res,n(q) -> Xi_sel,corr^(1,eta),n(q)
```

must satisfy

```text
Sh_chk,n(q)(z) in span(g_mem,n(q))
```

for every `z in D_res,n(q)`, hence it is equivalent to a scalar membrane
selector `sigma_chk,n(q)` through

```text
Sh_chk,n(q)(z) = sigma_chk,n(q)(z) g_mem,n(q).
```

Status:
- closed enough.

Verification method:
- CAS;
- code inspection;
- manual derivation.

### `T3k-L4`. Exact obstruction theorem

Statement:

A raw basepoint-independent factorization of `Phi_chk` through
`q_coeff o chi_chk,vis o Sh_chk` on `D_res,n(q)` would be identically zero.
Therefore the current boundary does not justify `Sh_chk,n(q)` as the missing
nontrivial global bridge. The precise missing ingredient is instead a
basepoint-relative representative-difference map on ambient candidate-class
objects before quotient collapse, or an exact theorem killing the membrane
selector `sigma_chk,n(q)`.

Status:
- Outcome C: exact obstruction theorem obtained.

Verification method:
- manual derivation;
- code inspection;
- reuse of the closed quotient-finality theorem from pilot 23.

### `T3k-L5`. Consequence lemma for the next kernel step

Statement:

The next nontrivial injectivity/kernel theorem cannot act on
`q_coeff o chi_chk,vis o Sh_chk` over raw `D_res,n(q)` alone. It must either:

1. use a basepoint-relative checked-local representative-difference object on
   ambient candidate-class pairs; or
2. prove directly that the membrane selector `sigma_chk,n(q)` vanishes on the
   admissible same-trace residual class.

Status:
- closed enough as a theorem-program consequence.

Verification method:
- manual derivation;
- Lean target only after the correct global object is abstracted.

## Single next bottleneck after `T3k`

The single next bottleneck is now:

```text
construct or control a theorem-facing basepoint-relative checked-local
representative-difference map on ambient candidate-class objects before
quotient collapse,
or prove that the admissible same-trace membrane selector sigma_chk,n(q)
vanishes identically.
```

This is sharper than the T3j bottleneck because it shows that a raw global
shadow map on `D_res,n(q)` would already collapse to the zero quotient class.

## Lean / CAS / manual split for `T3k`

Lean:
- only finite-dimensional map/composition/kernel templates once the correct
  global object is abstracted beyond the raw `Sh_chk` target on `D_res,n(q)`.

CAS / code inspection:
- `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, the quotient chart identities, and the zero-quotient collapse
  on the same-trace domain.

Manual derivation:
- exact theorem scope for `T3k`;
- the local-vs-global shadow obstruction wording;
- why any compatible raw `Sh_chk` on `D_res,n(q)` must factor through the
  membrane line;
- relation of `T3k` to the next nontrivial global bridge step.

## Conservative status after `T3k`

Closed enough now:
- the exact local extractor `chi_chk,vis,n(q)` on
  `Xi_sel,corr^(1,eta),n(q)`;
- the exact projected factorization `q_coeff o chi_chk,vis = L_amp o Pi_eta_to_J0`;
- the zero-quotient collapse of any compatible same-trace checked-local shadow;
- the membrane-line factorization `Sh_chk(z) = sigma_chk(z) g_mem` for any
  compatible raw shadow map on `D_res,n(q)`.

Still open:
- a theorem-facing basepoint-relative checked-local representative-difference
  object on ambient candidate-class pairs;
- or a theorem that the membrane selector `sigma_chk,n(q)` vanishes on the
  admissible same-trace residual class;
- hence the next genuinely nontrivial kernel theorem above the current checked
  quotient boundary.

So the gap is now sharper than in `T3j`: the obstruction is not merely вЂњmissing
shadow mapвЂќ, but вЂњa raw same-trace shadow map would already collapse to the zero
quotient class and cannot carry the needed nontrivial projected information.вЂќ

## Exact `T3l` theorem target

The exact `T3l` target is the construction / control theorem for a
basepoint-relative checked-local representative-difference object on ambient
same-selected-trace pairs before quotient collapse.

The raw same-trace shadow target from `T3k` is already too collapsed: on

```text
D_res,n(q) := A_adm^th,n(q) intersect ker(C_center,n(q)) subset ker(J_0,n(q)),
```

any compatible raw checked-local shadow lands in the zero quotient class and so
cannot carry the nontrivial projected bridge.

So the new object must live on equal-trace checked-local pairs rather than on
raw same-trace residuals alone.

## Outcome reached in this turn

Outcome reached:

```text
Outcome A.
```

A genuine basepoint-relative checked-local representative-difference object is
now available on the exact checked-local pair domain where both local shadows are
defined in a common corrected chart.

The membrane-selector route does not close vanishing, but it becomes a scalar
reformulation of this pairwise object rather than a separate unknown structure.

## Sharp analysis of the `T3k` obstruction

The `T3k` obstruction is now exact:

1. on the checked local corrected family,

```text
q_coeff o chi_chk,vis,n(q) = L_amp o Pi_eta_to_J0;
```

2. on the raw same-trace residual domain,

```text
D_res,n(q) subset ker(J_0,n(q));
```

3. therefore any raw compatible checked-local shadow on `D_res,n(q)` is already
   quotient-zero and must land in the membrane line `span(g_mem,n(q))`.

So the raw same-trace shadow loses exactly the representative-level membrane
comparison between two equal-trace ambient objects. That is the information that
must be carried by a basepoint-relative object.

Equivalently: if one insists on a raw same-trace shadow map, then the only
surviving datum is the scalar membrane coefficient multiplying `g_mem`.

## Strongest exact result obtained: the basepoint-relative pair object

### Theorem `T3l`

For fixed clean `(n, q)`, define the checked-local equal-trace pair domain

```text
Pair_chk,n(q)
  := { (c, c_ref) :
       c, c_ref have checked local shadows defined in a common corrected chart,
       J_0(c) = J_0(c_ref) }.
```

On this domain, choose any common corrected chart coefficient extractor and
write

```text
chi_chk,chart,n(q)(c)     = (a, b, s)^T,
chi_chk,chart,n(q)(c_ref) = (a_ref, b_ref, s_ref)^T.
```

Then:

1. because `J_0(c) = J_0(c_ref)` and

```text
q_coeff o chi_chk,vis,n(q) = L_amp o Pi_eta_to_J0
```

   on the corrected checked local family, one has

```text
a = a_ref,
b = b_ref,
```

   in every common corrected chart;

2. therefore the coefficient difference satisfies

```text
chi_chk,chart,n(q)(c) - chi_chk,chart,n(q)(c_ref)
  = (0, 0, s - s_ref)^T
  in span(e_mem);
```

3. under every quotient-preserving chart change

```text
S_(ell1,ell2)
 := [[1,0,0],[0,1,0],[ell1,ell2,1]],
```

   the coefficient vectors transform by `S_(ell1,ell2)^(-1)`, but

```text
S_(ell1,ell2)^(-1) (0, 0, s - s_ref)^T = (0, 0, s - s_ref)^T;
```

4. hence the pairwise membrane difference vector

```text
Delta_rep,chk,n(q; c, c_ref)
  := chi_chk,chart,n(q)(c) - chi_chk,chart,n(q)(c_ref)
  in span(e_mem)
```

   is independent of the chosen quotient-preserving corrected chart and is a
   well-defined theorem-facing object on `Pair_chk,n(q)`;

5. equivalently there is a unique scalar selector

```text
sigma_chk,n(q; c, c_ref) in R
```

   such that

```text
Delta_rep,chk,n(q; c, c_ref)
  = sigma_chk,n(q; c, c_ref) e_mem;
```

6. for a repo-selected basepoint `c_sel` and a same-trace residual-generated
   candidate `c = c_sel + z` lying in the checked-local pair domain, define

```text
sigma_chk,n(q; c_sel)(z)
  := sigma_chk,n(q; c_sel + z, c_sel).
```

   This is exactly the surviving basepoint-relative membrane datum left after the
   raw same-trace quotient collapse;

7. vanishing of this pairwise selector is equivalent to vanishing of the checked
   local representative difference:

```text
sigma_chk,n(q; c, c_ref) = 0
iff
Delta_rep,chk,n(q; c, c_ref) = 0.
```

So the current boundary does support a genuine nontrivial theorem-facing pair
object; what `T3k` ruled out was only the raw same-trace shadow map on `D_res`
without a basepoint.

## Comparison of the two routes

### 1. Basepoint-relative route

This route is now closed enough at the structural level.

The nontrivial checked-local datum does survive on equal-trace pairs before
quotient collapse, and it survives canonically exactly as the membrane-difference
vector `Delta_rep,chk` or equivalently the scalar `sigma_chk`.

### 2. Membrane-selector route

The membrane-selector route is now a scalar reformulation of the pairwise route.
It is not a separate object anymore.

What remains open is not the existence of `sigma_chk`, but its vanishing on the
exact admissible residual-generated pair domain.

### 3. Which route is stronger now

The basepoint-relative pair route is stronger on the current repository/theory
boundary.

Reason:
- it is canonical under quotient-preserving chart changes;
- it explains exactly why the raw-shadow route from `T3k` collapses;
- it packages the only surviving local datum before quotient collapse;
- and the membrane-selector question becomes a theorem about this already
  defined pair object.

So the vanishing route is now reducible to the pair route, not vice versa.

## Minimal `T3l` lemma split

### `T3l-L1`. Raw same-trace zero-collapse lemma

Statement:

On `D_res,n(q) subset ker(J_0,n(q))`, every compatible raw checked-local shadow
projects to zero under `q_coeff o chi_chk,vis,n(q)`.

Status:
- closed enough.

Verification method:
- manual derivation;
- CAS/theory reuse;
- code inspection.

### `T3l-L2`. Membrane-line factorization lemma

Statement:

For every equal-trace checked-local pair `(c, c_ref)` in `Pair_chk,n(q)`, the
coefficient difference lies in `span(e_mem)` and is invariant under every
quotient-preserving chart change.

Status:
- closed enough.

Verification method:
- CAS;
- code inspection;
- manual derivation.

### `T3l-L3`. Basepoint-relative checked-local representative-difference construction lemma

Statement:

The pairwise membrane-difference vector

```text
Delta_rep,chk,n(q; c, c_ref) in span(e_mem)
```

is a well-defined theorem-facing object on `Pair_chk,n(q)`, independent of the
chosen quotient-preserving corrected chart.

Status:
- closed enough.

Verification method:
- CAS;
- code inspection;
- manual derivation.

### `T3l-L4`. Membrane-selector control lemma

Statement:

There is a unique scalar selector

```text
sigma_chk,n(q; c, c_ref)
```

such that

```text
Delta_rep,chk,n(q; c, c_ref) = sigma_chk,n(q; c, c_ref) e_mem.
```

On the residual-generated pair domain this gives the scalar membrane selector
`sigma_chk,n(q; c_sel)(z)`. Its vanishing is equivalent to vanishing of the
pairwise checked-local representative difference, but its global vanishing on
all admissible residual-generated pairs is still open.

Status:
- partial.

Verification method:
- manual derivation;
- code inspection;
- CAS for chart invariance.

### `T3l-L5`. Exact consequence lemma for the next global bridge step

Statement:

The next nontrivial theorem can now be posed either as:

1. a vanishing theorem for the pairwise selector
   `sigma_chk,n(q; c_sel)(z)` on the exact admissible residual-generated pair
   domain; or
2. an equivalent theorem that the basepoint-relative representative-difference
   object `Delta_rep,chk,n(q; c_sel + z, c_sel)` vanishes identically there.

Status:
- closed enough as a theorem-program consequence.

Verification method:
- manual derivation;
- Lean target after the pair domain and selector are abstracted.

## Single next bottleneck after `T3l`

The single next bottleneck is now:

```text
prove or refute that the basepoint-relative membrane selector
sigma_chk,n(q; c_sel)(z)
vanishes identically on the exact admissible residual-generated checked-local
pair domain.
```

Equivalently: prove or refute that the pairwise checked-local
representative-difference object `Delta_rep,chk` is identically zero there.

## Lean / CAS / manual split for `T3l`

Lean:
- only finite-dimensional pair-map / scalar-selector / kernel templates once the
  pair domain and the theorem-facing selector are abstracted.

CAS / code inspection:
- `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, raw same-trace collapse, and the invariance of pairwise
  membrane difference under quotient-preserving chart changes.

Manual derivation:
- exact theorem scope for `T3l`;
- why the raw same-trace shadow target collapses but the pairwise equal-trace
  difference survives;
- comparison of the basepoint-relative route and the selector-vanishing route;
- relation of `T3l` to the next bridge step below full `T3`.

## Conservative status after `T3l`

Closed enough now:
- the raw same-trace zero-collapse from `T3k`;
- the existence of a theorem-facing basepoint-relative checked-local
  representative-difference object `Delta_rep,chk` on equal-trace checked-local
  pairs;
- the equivalent scalar membrane selector `sigma_chk` on the same pair domain;
- reduction of the next nontrivial question to vanishing/nonvanishing of that
  pairwise object.

Still open:
- whether `sigma_chk,n(q; c_sel)(z)` vanishes on the exact admissible
  residual-generated pair domain;
- hence whether the remaining checked-local representative difference is
  actually trivial on the theorem-facing candidate boundary.

So the gap is now sharper than in `T3k`: the correct nontrivial bridge object is
no longer a raw shadow on `D_res`, but the chart-invariant membrane-difference
on equal-trace ambient pairs before quotient collapse.
## Exact `T3m` theorem target

For fixed clean `(n, q)`, `T3m` asks whether the basepoint-relative membrane
selector

```text
sigma_chk,n(q; c_sel)(z)
  := sigma_chk,n(q; c_sel + z, c_sel)
```

must vanish on the exact admissible residual-generated checked-local pair
domain.

The exact scalar object under investigation is therefore the unique membrane
coefficient in the chart-invariant pairwise representative difference

```text
Delta_rep,chk,n(q; c_sel + z, c_sel)
  = sigma_chk,n(q; c_sel)(z) e_mem.
```

Define the exact domain of definition

```text
D_sigma,n(q; c_sel)
  := { z in D_res,n(q) :
       (c_sel + z, c_sel) in Pair_chk,n(q) }.
```

This is the exact admissible residual-generated checked-local pair domain on
which `sigma_chk,n(q; c_sel)(z)` is currently meaningful.

Vanishing/nonvanishing of `sigma_chk` decides the remaining checked-local
membrane-difference gap because

```text
sigma_chk,n(q; c_sel)(z) = 0
iff
Delta_rep,chk,n(q; c_sel + z, c_sel) = 0.
```

This is still not full `T3`, not final physical criticality, and not a
collapse to `B_red` / `B_mix`.

## Exact domain and structural laws of `sigma_chk`

Fix a repo-selected basepoint

```text
c_sel in A_sel^repo,n(q).
```

The exact theorem-facing domain is

```text
D_sigma,n(q; c_sel)
  := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
       (c_sel + z, c_sel) in Pair_chk,n(q) }.
```

On this domain:

1. `sigma_chk,n(q; c_sel)(z)` is well-defined by `T3l`.
2. In any common corrected chart with

```text
chi_chk,chart,n(q)(c_sel + z) = (a, b, s)^T,
chi_chk,chart,n(q)(c_sel)     = (a, b, s_sel)^T,
```

   one has

```text
sigma_chk,n(q; c_sel)(z) = s - s_sel.
```

3. Therefore

```text
sigma_chk,n(q; c_sel)(0) = 0.
```

4. On the equal-trace checked-local pair domain the pairwise selector satisfies
the exact antisymmetry and cocycle laws

```text
sigma_chk,n(q; c, c_ref) = -sigma_chk,n(q; c_ref, c),
sigma_chk,n(q; c_1, c_3)
  = sigma_chk,n(q; c_1, c_2) + sigma_chk,n(q; c_2, c_3),
```

   whenever the three equal-trace checked-local objects are defined in a common
   corrected chart.

So `sigma_chk` is not an arbitrary label: it is the exact chart-invariant
membrane-difference cocycle on the current checked-local equal-trace pair
domain.

## Strongest exact result obtained: selector structure closes, vanishing does not

### Theorem `T3m`

For fixed clean `(n, q)` and fixed repo-selected basepoint

```text
c_sel in A_sel^repo,n(q),
```

let `D_sigma,n(q; c_sel)` be the exact admissible residual-generated
checked-local pair domain above.

Then:

1. the selector `sigma_chk,n(q; c_sel)(z)` is a well-defined scalar cocycle on
   `D_sigma,n(q; c_sel)` in the sense above;
2. current theorem-facing admissibility / selected-trace structure forces only
   equality of the quotient coordinates `(a, b)`, not equality of the membrane
   coefficient `s`;
3. by the already closed pilot-23 quotient-finality theorem, all currently
   justified checked-local selected invariants factor through the membrane
   quotient, while no intrinsic canonical representative inside one quotient
   class is currently justified:
   chart-zero rules are chart-dependent, orthogonality/minimal-norm rules are
   metric-dependent, and imported `H`-selection is extrinsic to the local
   checked boundary;
4. therefore the current theorem-facing candidate/admissibility structure does
   not force

```text
sigma_chk,n(q; c_sel)(z) = 0
```

   on all of `D_sigma,n(q; c_sel)`;
5. an exact nonvanishing template is now isolated:
   if there exists

```text
z in D_sigma,n(q; c_sel)
```

   and a common corrected chart in which

```text
chi_chk,chart,n(q)(c_sel + z) = (a, b, s_sel + delta)^T,
chi_chk,chart,n(q)(c_sel)     = (a, b, s_sel)^T,
delta != 0,
```

   then

```text
sigma_chk,n(q; c_sel)(z) = delta != 0.
```

   This is compatible with all currently justified quotient-level invariants,
   because those invariants see only `(a, b)`.

So the strongest honest `T3m` endpoint is not a vanishing theorem and not an
explicit nonzero admissible example. It is an exact obstruction theorem:
vanishing of `sigma_chk` would require one additional theorem that the exact
admissible residual-generated checked-local pair domain selects a unique
representative inside each equal-trace membrane quotient class relative to the
repo-selected basepoint.

## Comparison with the old raw-shadow route

The `sigma_chk` route is now the correct surviving refinement of the earlier
raw-shadow route.

1. The raw same-trace shadow route was too collapsed:

```text
D_res,n(q) subset ker(J_0,n(q))
```

   already kills the quotient coordinates `(a, b)`, so every compatible raw
   shadow is quotient-zero by `T3k`.
2. The pairwise selector `sigma_chk` is strictly sharper than that raw route:
   it records the representative-level membrane difference inside the zero
   quotient class.
3. Therefore vanishing of `sigma_chk` is not equivalent to the old raw-shadow
   triviality question. It is the correct representative-level replacement of
   that question after quotient collapse.

## Minimal `T3m` lemma split

### `T3m-L1`. Exact domain-of-definition lemma for `sigma_chk`

Statement:

For fixed clean `(n, q)` and fixed repo-selected basepoint `c_sel`, the exact
domain of the basepoint-relative membrane selector is

```text
D_sigma,n(q; c_sel)
  := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
       (c_sel + z, c_sel) in Pair_chk,n(q) }.
```

Status:
- closed enough.

Verification method:
- manual derivation;
- code inspection;
- reuse of the `T3l` pair-domain construction.

### `T3m-L2`. Pairwise membrane-selector structure lemma

Statement:

On the equal-trace checked-local pair domain, `sigma_chk` is chart-invariant and
satisfies the exact normalization, antisymmetry, and cocycle laws

```text
sigma_chk(c, c) = 0,
sigma_chk(c, c_ref) = -sigma_chk(c_ref, c),
sigma_chk(c_1, c_3) = sigma_chk(c_1, c_2) + sigma_chk(c_2, c_3).
```

Status:
- closed enough.

Verification method:
- CAS;
- code inspection;
- manual derivation.

### `T3m-L3`. Vanishing / partial-vanishing implication lemma

Statement:

Vanishing of `sigma_chk,n(q; c_sel)(z)` is equivalent to vanishing of the
checked-local pairwise representative difference

```text
Delta_rep,chk,n(q; c_sel + z, c_sel).
```

Current admissibility and selected-trace constraints force equality of the
quotient coordinates `(a, b)` only; they do not currently force vanishing of
the membrane selector.

Status:
- partial.

Verification method:
- manual derivation;
- code inspection;
- CAS for the chart-invariant pair-difference identities.

### `T3m-L4`. Exact obstruction / nonvanishing-template lemma

Statement:

All currently justified checked-local selected invariants factor through the
membrane quotient, so they do not detect the scalar membrane cocycle
`sigma_chk`. Therefore vanishing on the full exact domain would require an
additional representative-selection theorem inside the equal-trace membrane
quotient class.

Equivalently, any admissible residual-generated pair with common corrected-chart
coordinates

```text
(a, b, s_sel + delta), (a, b, s_sel)
```

and `delta != 0` yields the exact nonvanishing template

```text
sigma_chk = delta != 0.
```

Status:
- closed enough as an exact obstruction theorem;
- explicit admissible nonzero example still open.

Verification method:
- manual derivation;
- code inspection;
- theorem reuse from pilot 23 quotient-finality.

### `T3m-L5`. Exact consequence lemma for the next bridge step

Statement:

The next nontrivial theorem is now exactly one of the following equivalent
statements:

1. `sigma_chk,n(q; c_sel)(z) = 0` for every `z in D_sigma,n(q; c_sel)`;
2. `Delta_rep,chk,n(q; c_sel + z, c_sel) = 0` for every
   `z in D_sigma,n(q; c_sel)`;
3. the exact admissible residual-generated checked-local pair domain meets each
   equal-trace membrane quotient class only in the repo-selected
   representative.

Status:
- closed enough as a theorem-program consequence.

Verification method:
- manual derivation;
- Lean target after the selector domain and cocycle law are abstracted.

## Single next bottleneck after `T3m`

The single next bottleneck is now:

```text
prove or refute that the exact admissible residual-generated checked-local
pair domain D_sigma,n(q; c_sel)
meets each equal-trace membrane quotient class only in the repo-selected
representative,
equivalently that sigma_chk,n(q; c_sel)(z) = 0 on all of D_sigma,n(q; c_sel).
```

## Lean / CAS / manual split for `T3m`

Lean:
- only finite-dimensional pair-map / scalar-cocycle / vanishing templates once
  the exact selector domain and cocycle laws are abstracted.

CAS / code inspection:
- `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, the pairwise membrane-difference identities, and the
  quotient-preserving chart-change formulas.

Manual derivation:
- exact theorem scope for `T3m`;
- why `sigma_chk` is the correct surviving representative-level object after
  raw same-trace collapse;
- why current theorem-facing constraints do not yet force its vanishing;
- relation of `T3m` to the next reverse-inclusion / zero-excess bridge step.

## Conservative status after `T3m`

Closed enough now:
- the exact domain of definition of the basepoint-relative membrane selector;
- the chart-invariant cocycle structure of `sigma_chk`;
- the equivalence between vanishing of `sigma_chk` and vanishing of the
  pairwise checked-local representative difference;
- the exact obstruction theorem that current theorem-facing constraints still
  act only through the membrane quotient and therefore do not force
  `sigma_chk = 0`.

Still open:
- whether an exact admissible residual-generated pair with nonzero
  `sigma_chk,n(q; c_sel)(z)` actually exists;
- whether the exact selector instead vanishes identically on
  `D_sigma,n(q; c_sel)`;
- hence whether the remaining checked-local membrane-difference obstruction is
  truly present or already trivial on the theorem-facing candidate boundary.

So the gap is sharper than after `T3l`: the open issue is no longer existence of
the pairwise selector, but whether the admissible residual-generated pair domain
still carries a nontrivial membrane cocycle relative to the repo-selected
basepoint.
## Exact `T3n` theorem target

For fixed clean `(n, q)`, fixed repo-selected basepoint

```text
c_sel in A_sel^repo,n(q),
```

and exact admissible residual-generated checked-local pair domain

```text
D_sigma,n(q; c_sel)
  := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
       (c_sel + z, c_sel) in Pair_chk,n(q) },
```

`T3n` asks whether this domain meets each equal-trace membrane quotient class
only in the repo-selected representative. Equivalently, it asks whether

```text
sigma_chk,n(q; c_sel)(z) = 0
```

for every `z in D_sigma,n(q; c_sel)`.

This is equivalent to vanishing of the checked-local representative difference
because

```text
Delta_rep,chk,n(q; c_sel + z, c_sel)
  = sigma_chk,n(q; c_sel)(z) e_mem.
```

The relevant domain is not all of `A_adm^th,n(q) intersect ker(C_center,n(q))`
by default, but only the exact checked-local definability subdomain
`D_sigma,n(q; c_sel)`.

This is still not full `T3`, not final physical criticality, and not a
collapse to `B_red` / `B_mix`.

## Exact domain sharpening and local-coboundary reduction

For fixed `(n, q)` and fixed `c_sel`, define the exact residual domain

```text
D_res,n(q) := A_adm^th,n(q) intersect ker(C_center,n(q)).
```

Then

```text
D_sigma,n(q; c_sel) subseteq D_res,n(q)
```

is the strict theorem-facing domain on which the pairwise selector is currently
meaningful.

The domain-of-definition conditions are exactly:

1. `z in A_adm^th,n(q)`;
2. `z in ker(C_center,n(q)) = ker(J_0,n(q))`;
3. the pair `(c_sel + z, c_sel)` lies in `Pair_chk,n(q)`, i.e. the two checked-
   local shadows are defined in a common corrected chart.

So uniqueness is being tested only on the checked-local definability subdomain,
not on the whole residual space by default.

For every common corrected chart `U` with

```text
D_sigma^U,n(q; c_sel)
  := { z in D_sigma,n(q; c_sel) :
       (c_sel + z, c_sel) is represented in the same corrected chart U },
```

write

```text
chi_chk,U,n(q)(c_sel + z) = (a, b, s_U(z))^T,
chi_chk,U,n(q)(c_sel)     = (a, b, s_U(0))^T.
```

Then on `D_sigma^U,n(q; c_sel)` one has the exact local formula

```text
sigma_chk,n(q; c_sel)(z) = s_U(z) - s_U(0).
```

So `sigma_chk` is locally a coboundary of the membrane coordinate. Therefore:

```text
sigma_chk,n(q; c_sel)(z) = 0  for all z in D_sigma^U,n(q; c_sel)
iff
s_U(z) = s_U(0)          for all z in D_sigma^U,n(q; c_sel).
```

This is the exact patchwise membrane-constancy formulation of the uniqueness
question.

It also shows that dependence on `c_sel` is only partially essential.
Locally on one common corrected chart patch, changing the basepoint only shifts
` s_U ` by a constant, so vanishing on that patch is basepoint-independent.
Globally, the dependence on `c_sel` is still essential because the exact domain
`D_sigma,n(q; c_sel)` itself is pair-relative.

## Strongest exact result obtained: vanishing reduced to patchwise membrane constancy, but not closed

### Theorem `T3n`

For fixed clean `(n, q)` and fixed repo-selected basepoint `c_sel`, let
`D_sigma,n(q; c_sel)` be the exact admissible residual-generated checked-local
pair domain.

Then:

1. the uniqueness-in-equal-trace-membrane-quotient-class theorem

```text
sigma_chk,n(q; c_sel)(z) = 0
for all z in D_sigma,n(q; c_sel)
```

   is exactly equivalent to patchwise constancy of the local membrane
   coordinate on every checked-local common-chart patch:

```text
for every U and every z in D_sigma^U,n(q; c_sel),
s_U(z) = s_U(0);
```

2. equivalently, on every such patch the exact admissible residual-generated
   checked-local pair domain meets each equal-trace membrane quotient class only
   in the repo-selected representative;
3. current theorem-facing candidate/admissibility constraints still do not
   force that constancy, because they determine only the quotient coordinates
   `(a, b)`;
4. by the already closed pilot-23 quotient-finality theorem, all currently
   justified checked-local selected invariants factor through the membrane
   quotient, and no intrinsic canonical representative inside one quotient class
   is currently justified on the checked boundary;
5. therefore the current theorem-facing structure does not yet force
   `sigma_chk,n(q; c_sel)(z) = 0` on all of `D_sigma,n(q; c_sel)`;
6. the exact nonvanishing template is now sharper than in `T3m`:
   if there exists one common corrected-chart patch `U` and one
   `z in D_sigma^U,n(q; c_sel)` with

```text
s_U(z) != s_U(0),
```

   then

```text
sigma_chk,n(q; c_sel)(z) != 0.
```

   More generally, for any two points `z_1, z_2` in the same patch,

```text
sigma_chk,n(q; c_sel + z_1, c_sel + z_2)
  = s_U(z_1) - s_U(z_2),
```

   so one nonconstant membrane-coordinate patch already carries the full local
   nonvanishing obstruction.

So the strongest honest `T3n` endpoint is an exact obstruction theorem:
vanishing has been reduced to patchwise membrane constancy on the exact
checked-local admissible residual-generated pair patches, but that constancy is
not yet forced by the current theorem-facing constraints.

## Comparison with the earlier raw-shadow and pairwise routes

The relation of the three routes is now exact.

1. Raw same-trace shadow route:
   too collapsed, because on `D_res,n(q) subset ker(J_0,n(q))` every compatible
   raw shadow is already quotient-zero and cannot carry the representative-level
   membrane datum.
2. Pairwise route from `T3l`:
   necessary intermediate step, because it first recovers the surviving
   theorem-facing representative-difference object on equal-trace checked-local
   pairs.
3. `sigma_chk` route from `T3m`/`T3n`:
   the exact scalar form of that pairwise object; `T3n` sharpens it further by
   showing that vanishing is equivalent to patchwise constancy of the local
   membrane coordinate.

So uniqueness-in-class is strictly stronger than the old raw-shadow triviality
question: the raw shadow can already be quotient-zero while the selector still
records nontrivial representative-level membrane difference inside that zero
quotient class.

## Minimal `T3n` lemma split

### `T3n-L1`. Exact domain-of-uniqueness lemma

Statement:

For fixed clean `(n, q)` and fixed repo-selected basepoint `c_sel`, uniqueness
is tested on

```text
D_sigma,n(q; c_sel)
  := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
       (c_sel + z, c_sel) in Pair_chk,n(q) },
```

not on the whole residual space by default.

Status:
- closed enough.

Verification method:
- manual derivation;
- code inspection;
- reuse of the `T3l` / `T3m` pair-domain package.

### `T3n-L2`. Membrane-quotient uniqueness vs selector-vanishing lemma

Statement:

On the exact domain `D_sigma,n(q; c_sel)`, the following are equivalent:

1. `sigma_chk,n(q; c_sel)(z) = 0` for all `z` in the domain;
2. `Delta_rep,chk,n(q; c_sel + z, c_sel) = 0` for all `z` in the domain;
3. each exact admissible residual-generated checked-local pair lies in the same
   equal-trace membrane quotient class as `c_sel` only trivially.

Status:
- closed enough.

Verification method:
- manual derivation;
- code inspection.

### `T3n-L3`. Local-coboundary / patchwise-constancy lemma

Statement:

On every common corrected-chart patch `D_sigma^U,n(q; c_sel)`, there is a local
membrane coordinate `s_U` such that

```text
sigma_chk,n(q; c_sel)(z) = s_U(z) - s_U(0).
```

Hence selector vanishing on that patch is equivalent to constancy of `s_U` on
that patch.

Status:
- closed enough.

Verification method:
- CAS;
- code inspection;
- manual derivation.

### `T3n-L4`. Exact obstruction / nonvanishing-template lemma

Statement:

Current theorem-facing candidate/admissibility constraints determine only the
quotient coordinates `(a, b)` and therefore do not yet force constancy of the
local membrane coordinate `s_U`. Consequently vanishing of `sigma_chk` on the
full exact domain would require an additional membrane-constancy / unique-
representative theorem on the admissible residual-generated checked-local pair
patches.

Equivalently, any patch with one point `z` satisfying `s_U(z) != s_U(0)` gives
an exact nonvanishing template.

Status:
- closed enough as an exact obstruction theorem;
- explicit admissible nonzero example still open.

Verification method:
- manual derivation;
- code inspection;
- theorem reuse from pilot 23 quotient-finality.

### `T3n-L5`. Exact consequence lemma for the next bridge step

Statement:

The next reverse-inclusion / zero-excess bridge step is now exactly the theorem
that the local membrane coordinate is constant on every exact admissible
residual-generated checked-local pair patch, equivalently that
`sigma_chk,n(q; c_sel)(z) = 0` on all of `D_sigma,n(q; c_sel)`.

Status:
- closed enough as a theorem-program consequence.

Verification method:
- manual derivation;
- Lean target after the exact domain, local-coboundary law, and constancy
  formulation are abstracted.

## Single next bottleneck after `T3n`

The single next bottleneck is now:

```text
prove or refute patchwise constancy of the local membrane coordinate
s_U on every exact admissible residual-generated checked-local pair patch
D_sigma^U,n(q; c_sel),
equivalently prove or refute sigma_chk,n(q; c_sel)(z) = 0 on all of
D_sigma,n(q; c_sel).
```

## Lean / CAS / manual split for `T3n`

Lean:
- only finite-dimensional pair-map / cocycle / local-coboundary / vanishing
  templates once the exact domain and patchwise constancy law are abstracted.

CAS / code inspection:
- `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, pairwise membrane difference, cocycle laws, and the local
  membrane-coordinate difference formulas.

Manual derivation:
- exact theorem scope for `T3n`;
- why uniqueness-in-class is equivalent to selector vanishing;
- why selector vanishing is equivalent to patchwise membrane constancy;
- why current theorem-facing constraints do not yet force that constancy;
- relation of `T3n` to the future reverse-inclusion / zero-excess bridge below
  full `T3`.

## Conservative status after `T3n`

Closed enough now:
- the exact uniqueness domain `D_sigma,n(q; c_sel)`;
- the equivalence between uniqueness-in-class and selector vanishing;
- the local-coboundary reduction of `sigma_chk` to patchwise membrane
  constancy;
- the exact obstruction theorem that current theorem-facing constraints still do
  not force that constancy.

Still open:
- whether the exact admissible residual-generated checked-local pair domain is
  patchwise membrane-constant;
- whether an explicit admissible nonzero selector value can be constructed on
  that exact domain;
- hence whether the remaining checked-local membrane obstruction is truly
  present or already trivial on the theorem-facing candidate boundary.

So the gap is sharper than after `T3m`: the remaining question is no longer
just вЂњdoes the cocycle vanish?вЂќ, but вЂњis the local membrane coordinate constant
on the exact admissible residual-generated checked-local pair patches?вЂќ.
## Exact `T3o` theorem target

For fixed clean `(n, q)`, fixed repo-selected basepoint

```text
c_sel in A_sel^repo,n(q),
```

and exact admissible residual-generated checked-local definability domain

```text
D_sigma,n(q; c_sel),
```

`T3o` asks whether the local membrane coordinate is constant on every exact
admissible residual-generated checked-local patch

```text
D_sigma^U,n(q; c_sel),
```

equivalently whether

```text
sigma_chk,n(q; c_sel)(z) = 0
```

for every `z in D_sigma,n(q; c_sel)`.

The exact local object under investigation is the patchwise membrane coordinate
` s_U ` defined by

```text
chi_chk,U,n(q)(c_sel + z) = (a_sel, b_sel, s_U(z))^T,
chi_chk,U,n(q)(c_sel)     = (a_sel, b_sel, s_U(0))^T
```

on each exact patch.

This is still not full `T3`, not final physical criticality, and not a
collapse to `B_red` / `B_mix`.

## Exact patchwise domain and overlap law

For fixed `(n, q)` and `c_sel`, the exact global definability domain is

```text
D_sigma,n(q; c_sel)
  := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
       (c_sel + z, c_sel) in Pair_chk,n(q) }.
```

An exact checked-local patch is any subset

```text
D_sigma^U,n(q; c_sel)
  := { z in D_sigma,n(q; c_sel) :
       (c_sel + z, c_sel) is represented in one common corrected chart U }.
```

The patch cover is not canonical as a named atlas, because it depends on the
available common corrected charts. But the constancy predicate is cover-
invariant.

Indeed, if `U` and `V` are two quotient-preserving corrected charts on the same
fixed equal-trace class, then their coefficient extractors differ by

```text
chi_chk,V = S_(ell1,ell2)^(-1) chi_chk,U,
S_(ell1,ell2)^(-1)
  = [[1,0,0],[0,1,0],[-ell1,-ell2,1]].
```

So for fixed selected-trace coordinates `(a_sel, b_sel)` one has on overlaps

```text
s_V(z) = s_U(z) - ell1 a_sel - ell2 b_sel.
```

The shift is independent of `z`. Therefore:

```text
s_V(z) - s_V(0) = s_U(z) - s_U(0),
```

hence constancy of `s_U` on an overlap is equivalent to constancy of `s_V`
there. So global vanishing of `sigma_chk` is equivalent to patchwise constancy
on any exact admissible residual-generated patch cover; no separate overlap
compatibility theorem remains to be proved.

## Strongest exact result obtained: overlap compatibility closes automatically, patchwise constancy does not

### Theorem `T3o`

For fixed clean `(n, q)` and fixed repo-selected basepoint `c_sel`, let

```text
{ D_sigma^U,n(q; c_sel) }_U
```

be any exact admissible residual-generated checked-local patch cover of
`D_sigma,n(q; c_sel)`.

Then:

1. on every patch `D_sigma^U,n(q; c_sel)` one has the exact local-coboundary
   law

```text
sigma_chk,n(q; c_sel)(z) = s_U(z) - s_U(0);
```

2. on every overlap of two quotient-preserving corrected charts, the local
   membrane coordinates differ only by a z-independent constant,

```text
s_V(z) = s_U(z) - ell1 a_sel - ell2 b_sel;
```

3. therefore constancy of the local membrane coordinate is automatically a
   cover-invariant notion, and

```text
sigma_chk,n(q; c_sel)(z) = 0  on all of D_sigma,n(q; c_sel)
```

   is equivalent to constancy of `s_U` on every patch of any exact admissible
   residual-generated patch cover;
4. no separate patch-overlap or gluing obstruction remains after this
   reduction;
5. current theorem-facing candidate/admissibility constraints still do not
   force constancy of `s_U` on even one exact patch, because they determine only
   the quotient coordinates `(a, b)`;
6. therefore the current theorem-facing structure still does not force
   `sigma_chk,n(q; c_sel)(z) = 0` on all of `D_sigma,n(q; c_sel)`;
7. the exact nonconstancy template is now sharper than in `T3n`:
   any exact patch `D_sigma^U,n(q; c_sel)` containing two points `z_1, z_2`
   with

```text
s_U(z_1) != s_U(z_2)
```

   yields

```text
sigma_chk,n(q; c_sel + z_1, c_sel + z_2) != 0,
```

   and in particular if `z_2 = 0` then

```text
sigma_chk,n(q; c_sel)(z_1) != 0.
```

So the strongest honest `T3o` endpoint is an exact obstruction theorem:
overlap compatibility is now closed as automatic, but patchwise constancy of the
local membrane coordinate is still not forced by the current theorem-facing
constraints.

## Comparison with the earlier routes

The four-step relation is now exact.

1. Raw same-trace shadow route:
   too collapsed, because raw compatible shadows on `D_res,n(q)` are already
   quotient-zero and cannot carry the representative-level membrane datum.
2. Pairwise route from `T3l`:
   necessary intermediate step, because it first recovers the surviving
   checked-local representative-difference object on equal-trace pairs.
3. Cocycle route from `T3m`:
   packages that pairwise object as the chart-invariant scalar selector
   `sigma_chk`, but by itself does not identify whether the remaining issue is
   constancy or patch gluing.
4. Patchwise-constancy route from `T3n` / `T3o`:
   sharpens the picture further by showing that overlap/gluing is automatic, so
   the only remaining issue is constancy on the patches themselves.

So patchwise constancy is strictly stronger than the old cocycle package, and
much stronger than the raw-shadow triviality question.

## Minimal `T3o` lemma split

### `T3o-L1`. Exact patch-domain lemma

Statement:

The exact admissible residual-generated checked-local patches are

```text
D_sigma^U,n(q; c_sel) subseteq D_sigma,n(q; c_sel),
```

where a common corrected chart `U` represents both `c_sel + z` and `c_sel`.

Status:
- closed enough.

Verification method:
- manual derivation;
- code inspection;
- reuse of the `T3n` local-coboundary package.

### `T3o-L2`. Local-coboundary vs patchwise-constancy lemma

Statement:

On every exact patch `D_sigma^U,n(q; c_sel)`, one has

```text
sigma_chk,n(q; c_sel)(z) = s_U(z) - s_U(0),
```

so selector vanishing on that patch is equivalent to constancy of `s_U` there.

Status:
- closed enough.

Verification method:
- manual derivation;
- CAS;
- code inspection.

### `T3o-L3`. Overlap-compatibility lemma

Statement:

If `U` and `V` are two quotient-preserving corrected charts on the same fixed
selected-trace class, then on overlaps

```text
s_V(z) = s_U(z) - ell1 a_sel - ell2 b_sel,
```

with a shift independent of `z`. Hence constancy is equivalent across overlaps,
and no separate gluing obstruction remains.

Status:
- closed enough.

Verification method:
- CAS;
- code inspection;
- manual derivation.

### `T3o-L4`. Exact obstruction / nonconstancy-template lemma

Statement:

Current theorem-facing candidate/admissibility constraints still determine only
`(a, b)` and do not yet force constancy of `s_U` on an exact patch.
Consequently any exact patch containing two points with different `s_U` values
already yields a nonzero pairwise selector, hence a nonconstancy / nonvanishing
template.

Status:
- closed enough as an exact obstruction theorem;
- explicit admissible nonconstant patch still open.

Verification method:
- manual derivation;
- code inspection;
- theorem reuse from pilot 23 quotient-finality.

### `T3o-L5`. Exact consequence lemma for the next bridge step

Statement:

Global vanishing of `sigma_chk` on `D_sigma,n(q; c_sel)` is equivalent to
patchwise constancy of `s_U` on any exact admissible residual-generated
checked-local patch cover. The only remaining bottleneck is therefore
constancy on the patches themselves, not compatibility across overlaps.

Status:
- closed enough as a theorem-program consequence.

Verification method:
- manual derivation;
- Lean target after the exact patch-domain and overlap-compatibility laws are
  abstracted.

## Single next bottleneck after `T3o`

The single next bottleneck is now:

```text
prove or refute constancy of s_U on the full exact admissible residual-
generated checked-local patch cover,
equivalently prove or refute sigma_chk,n(q; c_sel)(z) = 0 on all of
D_sigma,n(q; c_sel).
```

## Lean / CAS / manual split for `T3o`

Lean:
- only finite-dimensional patch / coboundary / constancy templates once the
  exact patch-domain and overlap-compatibility law are abstracted.

CAS / code inspection:
- `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, local membrane-coordinate difference formulas, cocycle laws,
  and quotient-preserving patch-overlap relations.

Manual derivation:
- exact theorem scope for `T3o`;
- why overlap compatibility is automatic;
- why current theorem-facing constraints still do not force patchwise
  constancy;
- relation of `T3o` to the future reverse-inclusion / zero-excess bridge below
  full `T3`.

## Conservative status after `T3o`

Closed enough now:
- the exact admissible residual-generated patch family;
- the equivalence between selector vanishing and patchwise constancy;
- the exact overlap law showing that constancy is automatically compatible
  across quotient-preserving corrected charts;
- the exact obstruction theorem that only patchwise constancy itself remains
  open.

Still open:
- whether `s_U` is constant on the full exact admissible residual-generated
  patch cover;
- whether an explicit admissible nonconstant patch can be constructed;
- hence whether the remaining checked-local membrane obstruction is truly
  present or already trivial on the theorem-facing candidate boundary.

So the gap is sharper than after `T3n`: overlap compatibility is no longer a
separate theorem bottleneck, and the only remaining issue is constancy of the
local membrane coordinate on the exact admissible residual-generated patches.
## Exact `T3p` theorem target

For fixed clean `(n, q)`, fixed repo-selected basepoint

```text
c_sel in A_sel^repo,n(q),
```

and any exact admissible residual-generated checked-local patch

```text
D_sigma^U,n(q; c_sel),
```

`T3p` studies the exact local checked-local patch image

```text
Im_chk,U,n(q; c_sel)
  := { chi_chk,U,n(q)(c_sel + z) : z in D_sigma^U,n(q; c_sel) }.
```

Because the selected trace is fixed on the whole exact patch, this image always
lies inside the one-dimensional membrane fiber

```text
F_U,n(q; c_sel)
  := { (a_sel, b_sel, s)^T : s in R }.
```

So the exact `T3p` question is whether the patch image is a singleton in that
fiber,

```text
Im_chk,U,n(q; c_sel) = { (a_sel, b_sel, s_U(0))^T },
```

equivalently whether the local membrane coordinate is constant on the patch,
equivalently whether

```text
sigma_chk,n(q; c_sel)(z) = 0
```

for every `z in D_sigma^U,n(q; c_sel)`, hence on all of
`D_sigma,n(q; c_sel)`.

This is still not full `T3`, not final physical criticality, and not a
collapse to `B_red` / `B_mix`.

## Exact patchwise domain and membrane-fiber image

The exact global residual-generated checked-local domain remains

```text
D_sigma,n(q; c_sel)
  := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
       (c_sel + z, c_sel) in Pair_chk,n(q) }.
```

For every corrected chart `U`, the corresponding exact patch is

```text
D_sigma^U,n(q; c_sel)
  := { z in D_sigma,n(q; c_sel) :
       (c_sel + z, c_sel) is represented in one common corrected chart U }.
```

On such a patch one has

```text
chi_chk,U,n(q)(c_sel + z) = (a_sel, b_sel, s_U(z))^T,
```

so define the exact membrane-fiber image

```text
S_U,n(q; c_sel)
  := { s_U(z) : z in D_sigma^U,n(q; c_sel) } subseteq R.
```

Then

```text
Im_chk,U,n(q; c_sel)
  = { (a_sel, b_sel, s)^T : s in S_U,n(q; c_sel) }.
```

By `T3o`, if `U` and `V` overlap on the same equal-trace class, then

```text
s_V(z) = s_U(z) - ell1 a_sel - ell2 b_sel,
```

so `S_V` is obtained from `S_U` by a constant shift. Therefore the predicate

```text
S_U,n(q; c_sel) is a singleton
```

is patch-cover invariant. After `T3o`, no separate overlap/gluing theorem is
needed: global vanishing of `sigma_chk` is equivalent to singletonity of the
membrane-fiber image on the patches themselves.

## Strongest exact result obtained: the remaining issue is singletonity in the fixed membrane fiber, not overlap or quotient data

### Theorem `T3p`

For fixed clean `(n, q)`, fixed repo-selected basepoint `c_sel`, and any exact
admissible residual-generated checked-local patch
`D_sigma^U,n(q; c_sel)`, let

```text
Im_chk,U,n(q; c_sel)
  := { chi_chk,U,n(q)(c_sel + z) : z in D_sigma^U,n(q; c_sel) },
S_U,n(q; c_sel)
  := { s_U(z) : z in D_sigma^U,n(q; c_sel) }.
```

Then:

1. the exact patch image is always contained in the fixed equal-trace membrane
   fiber,

```text
Im_chk,U,n(q; c_sel) subseteq F_U,n(q; c_sel)
  = { (a_sel, b_sel, s)^T : s in R };
```

2. equivalently,

```text
Im_chk,U,n(q; c_sel)
  = { (a_sel, b_sel, s)^T : s in S_U,n(q; c_sel) };
```

3. the following are exactly equivalent on that patch:
   - `sigma_chk,n(q; c_sel)(z) = 0` for every `z in D_sigma^U,n(q; c_sel)`;
   - `s_U(z) = s_U(0)` for every `z in D_sigma^U,n(q; c_sel)`;
   - `S_U,n(q; c_sel) = { s_U(0) }`;
   - `Im_chk,U,n(q; c_sel) = { (a_sel, b_sel, s_U(0))^T }`;

4. after `T3o`, global vanishing of `sigma_chk` on `D_sigma,n(q; c_sel)` is
   equivalent to this singleton condition on every patch of any exact
   admissible residual-generated cover;
5. current theorem-facing candidate/admissibility constraints still determine
   only the quotient coordinates `(a_sel, b_sel)`, so they currently prove only

```text
Im_chk,U,n(q; c_sel) subseteq F_U,n(q; c_sel),
```

   not that this image is a singleton;
6. therefore the exact surviving local freedom is now isolated sharply as the
   possible nonsingleton set `S_U,n(q; c_sel)` inside the one-dimensional
   membrane fiber;
7. hence the strongest honest `T3p` endpoint is an exact obstruction theorem:
   current theorem-facing constraints reduce the whole remaining question to a
   membrane-fiber singleton problem on each exact admissible patch, but do not
   yet force that singletonity;
8. the exact nonconstancy / nonvanishing template is:
   any patch containing two points `z_1, z_2` with

```text
chi_chk,U,n(q)(c_sel + z_1) = (a_sel, b_sel, s_1)^T,
chi_chk,U,n(q)(c_sel + z_2) = (a_sel, b_sel, s_2)^T,
s_1 != s_2,
```

   yields

```text
sigma_chk,n(q; c_sel + z_1, c_sel + z_2) = s_1 - s_2 != 0,
```

   and in particular if `z_2 = 0` then

```text
sigma_chk,n(q; c_sel)(z_1) != 0.
```

So the strongest current `T3p` outcome is not a constancy theorem, but a
single-fiber image theorem: all unresolved freedom now sits entirely inside the
fixed one-dimensional membrane fiber above `(a_sel, b_sel)`.

## Comparison with the earlier routes

The refinement chain is now exact.

1. Raw same-trace shadow route:
   too collapsed, because on `D_res,n(q) subseteq ker(J_0,n(q))` all compatible
   raw shadows are already quotient-zero and lose the representative-level
   membrane datum.
2. Pairwise route from `T3l`:
   necessary intermediate step, because it first recovers the surviving
   checked-local representative-difference object on equal-trace pairs.
3. Cocycle route from `T3m`:
   packages that difference object as the chart-invariant scalar selector
   `sigma_chk`, but by itself does not say where the remaining freedom lives.
4. Patchwise-constancy route from `T3n` / `T3o`:
   shows that vanishing is equivalent to local membrane constancy and that
   overlap/gluing is automatic.
5. Membrane-fiber singleton route from `T3p`:
   sharpens the remaining issue further by identifying the exact surviving local
   freedom as nonsingletonity of the exact patch image inside the fixed fiber
   `{ (a_sel, b_sel, s) }`.

So `T3p` is strictly stronger than the earlier cocycle / patchwise packages: it
does not merely say that constancy is open, but isolates the exact one-
dimensional local fiber in which the unresolved freedom lives.

## Minimal `T3p` lemma split

### `T3p-L1`. Exact patch-domain and patch-image lemma

Statement:

For every exact patch `D_sigma^U,n(q; c_sel)`, the checked-local image

```text
Im_chk,U,n(q; c_sel)
  := { chi_chk,U,n(q)(c_sel + z) : z in D_sigma^U,n(q; c_sel) }
```

is well-defined and satisfies

```text
Im_chk,U,n(q; c_sel) subseteq { (a_sel, b_sel, s)^T : s in R }.
```

Status:
- closed enough.

Verification method:
- manual derivation;
- code inspection;
- reuse of the `T3o` overlap/patch package.

### `T3p-L2`. Patchwise-constancy vs membrane-fiber singleton lemma

Statement:

For every exact patch `D_sigma^U,n(q; c_sel)`, the following are equivalent:

```text
sigma_chk = 0 on D_sigma^U;
s_U is constant on D_sigma^U;
S_U = { s_U(0) };
Im_chk,U = { (a_sel, b_sel, s_U(0))^T }.
```

Status:
- closed enough.

Verification method:
- manual derivation;
- CAS;
- code inspection.

### `T3p-L3`. Cover-invariant singletonity lemma

Statement:

Under quotient-preserving corrected chart changes, the membrane coordinate shifts
by a z-independent constant. Therefore singletonity of `S_U` and singletonity
of `Im_chk,U` in the fixed membrane fiber are cover-invariant predicates, so no
separate overlap/gluing theorem remains.

Status:
- closed enough.

Verification method:
- CAS;
- code inspection;
- manual derivation.

### `T3p-L4`. Exact obstruction / nonconstancy-template lemma

Statement:

Current theorem-facing candidate/admissibility constraints still determine only
the quotient base point `(a_sel, b_sel)` and therefore prove only fiber
containment, not fiber singletonity. Consequently any patch containing two
distinct membrane-coordinate values already yields an exact nonvanishing
template for `sigma_chk`.

Status:
- closed enough as an exact obstruction theorem;
- explicit admissible nonsingleton patch still open.

Verification method:
- manual derivation;
- code inspection;
- theorem reuse from pilot 23 quotient-finality and `T3o`.

### `T3p-L5`. Exact consequence lemma for the next bridge step

Statement:

Global vanishing of `sigma_chk` on `D_sigma,n(q; c_sel)` is equivalent to
singletonity of the exact checked-local patch image in the fixed membrane fiber
on every patch of any exact admissible residual-generated cover. The only
remaining bottleneck is therefore the membrane-fiber singleton theorem itself.

Status:
- closed enough as a theorem-program consequence.

Verification method:
- manual derivation;
- Lean target after the exact patch-image and singletonity laws are abstracted.

## Single next bottleneck after `T3p`

The single next bottleneck is now:

```text
prove or refute that for every exact admissible residual-generated checked-
local patch D_sigma^U,n(q; c_sel), the membrane-fiber image
S_U,n(q; c_sel) = { s_U(z) : z in D_sigma^U,n(q; c_sel) }
is a singleton,
equivalently that sigma_chk,n(q; c_sel)(z) = 0 on all of
D_sigma,n(q; c_sel).
```

## Lean / CAS / manual split for `T3p`

Lean:
- only finite-dimensional patch-image / singletonity / constancy templates once
  the exact patch-domain and membrane-fiber image law are abstracted.

CAS / code inspection:
- `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, local membrane-coordinate difference formulas, and the exact
  patchwise chart formulas showing fixed `(a_sel, b_sel)` and variable membrane
  coordinate.

Manual derivation:
- exact theorem scope for `T3p`;
- why overlap compatibility is no longer independent after `T3o`;
- why current theorem-facing constraints force only fiber containment and not
  singletonity;
- relation of `T3p` to the future reverse-inclusion / zero-excess bridge below
  full `T3`.

## Conservative status after `T3p`

Closed enough now:
- the exact patch-domain and patch-image package;
- the equivalence between selector vanishing, patchwise constancy, and
  membrane-fiber singletonity;
- the cover-invariance of that singletonity predicate under quotient-preserving
  corrected chart changes;
- the exact obstruction theorem that the only surviving unresolved freedom is a
  possible nonsingleton subset of the fixed membrane fiber.

Still open:
- whether the exact patch image is a singleton on every admissible patch;
- whether an explicit admissible nonsingleton patch can be constructed;
- hence whether the remaining checked-local membrane obstruction is truly
  present or already trivial on the theorem-facing candidate boundary.

So the gap is sharper than after `T3o`: the remaining question is no longer
just вЂњis `s_U` constant?вЂќ, but вЂњdoes the exact admissible checked-local patch
image collapse to a single point inside the fixed membrane fiber?вЂќ.
## Exact `T3q` theorem target

For fixed clean `(n, q)`, fixed repo-selected basepoint

```text
c_sel in A_sel^repo,n(q),
```

and every exact admissible residual-generated checked-local patch

```text
D_sigma^U,n(q; c_sel),
```

the exact `T3q` target is to decide whether the checked-local patch image

```text
Im_chk,U,n(q; c_sel)
  := { chi_chk,U,n(q)(c_sel + z) : z in D_sigma^U,n(q; c_sel) }
```

is a singleton inside the fixed membrane fiber

```text
F_U,n(q; c_sel) := { (a_sel, b_sel, s)^T : s in R }.
```

Equivalently, `T3q` asks whether

```text
sigma_chk,n(q; c_sel)(z) = 0
```

for every `z in D_sigma,n(q; c_sel)`.

The relevant exact domain family is any admissible residual-generated checked-
local patch cover

```text
{ D_sigma^U,n(q; c_sel) }_U
```

of the global exact definability domain `D_sigma,n(q; c_sel)`.

Outside scope for `T3q`:

- not full `T3`;
- not final physical criticality;
- not a collapse to `B_red` / `B_mix`;
- not a reopening of the frozen local Outcome-B branch.

## Exact singletonity domain and representative-law sharpening

The global exact same-trace definability domain remains

```text
D_sigma,n(q; c_sel)
  := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
       (c_sel + z, c_sel) in Pair_chk,n(q) }.
```

For each corrected chart `U`, the corresponding exact patch is

```text
D_sigma^U,n(q; c_sel)
  := { z in D_sigma,n(q; c_sel) :
       (c_sel + z, c_sel) is represented in one common corrected chart U }.
```

On such a patch one has

```text
chi_chk,U,n(q)(c_sel + z) = (a_sel, b_sel, s_U(z))^T,
```

so the exact membrane-fiber image is

```text
S_U,n(q; c_sel)
  := { s_U(z) : z in D_sigma^U,n(q; c_sel) } subseteq R,
```

and

```text
Im_chk,U,n(q; c_sel)
  = { (a_sel, b_sel, s)^T : s in S_U,n(q; c_sel) }.
```

The more primitive object behind singletonity is the exact patchwise
representative law

```text
Rep_U,n(q; c_sel) :
for all z_1, z_2 in D_sigma^U,n(q; c_sel),
chi_chk,U,n(q)(c_sel + z_1) = chi_chk,U,n(q)(c_sel + z_2).
```

Since the quotient coordinates are fixed on the whole patch, this is equivalent
to

```text
for all z_1, z_2 in D_sigma^U,n(q; c_sel),  s_U(z_1) = s_U(z_2),
```

hence equivalent to singletonity of `Im_chk,U` in `F_U`.

Singletonity is tested patchwise on the exact cover, and globally only through
that cover. By `T3o`, if `U` and `V` overlap on the same equal-trace class,
then

```text
s_V(z) = s_U(z) - ell1 a_sel - ell2 b_sel,
```

so singletonity and the representative law are automatically equivalent across
overlaps. Therefore no separate overlap/gluing theorem remains after `T3o`.

## Outcome reached in this turn

Outcome B.

Singletonity is still not proved. But the sharpest exact result is now stronger
than `T3p`: the current theorem-facing boundary is shown to be quotient-final
with respect to all currently justified checked-local invariants, so the whole
remaining gap is exactly one missing representative-sensitive law on the exact
patch domain.

## Strongest exact result obtained: singletonity is reduced to one missing representative law, and current quotient-final data do not force it

### Theorem `T3q`

For fixed clean `(n, q)`, fixed repo-selected basepoint `c_sel`, and any exact
admissible residual-generated checked-local patch `D_sigma^U,n(q; c_sel)`, let

```text
Im_chk,U,n(q; c_sel)
  := { chi_chk,U,n(q)(c_sel + z) : z in D_sigma^U,n(q; c_sel) },
S_U,n(q; c_sel)
  := { s_U(z) : z in D_sigma^U,n(q; c_sel) }.
```

Then:

1. the singletonity question on that patch is exactly the representative-law
   question

```text
Rep_U,n(q; c_sel),
```

   equivalently the exact vanishing question

```text
sigma_chk,n(q; c_sel)(z) = 0  for all z in D_sigma^U,n(q; c_sel);
```

2. equivalently, on that patch the following are exactly equivalent:
   - `Rep_U,n(q; c_sel)`;
   - `s_U` is constant on `D_sigma^U,n(q; c_sel)`;
   - `S_U,n(q; c_sel)` is a singleton;
   - `Im_chk,U,n(q; c_sel)` is a singleton in `F_U,n(q; c_sel)`;
   - `sigma_chk,n(q; c_sel)` vanishes on that patch;
3. by the boundary-scoped quotient-finality package from pilot 23, every
   currently justified checked-local invariant on the present checked boundary
   factors through the quotient map `(a, b, s) -> (a, b)` or is blind along the
   membrane line:
   - the canonical `J_0` trace is exactly `D_amp q_coeff`;
   - the checked local residual vanishes identically on the corrected family;
   - the next checked local compatibility layer contributes no
     representative-level invariant;
   - the strongest plausible selector candidates checked so far are
     chart-dependent, metric-dependent, or extrinsic to the current local
     theory;
4. therefore current theorem-facing candidate/admissibility constraints still
   control only the fixed quotient coordinates `(a_sel, b_sel)` on the patch
   and do not imply `Rep_U,n(q; c_sel)`;
5. equivalently, current theorem-facing constraints prove only

```text
Im_chk,U,n(q; c_sel) subseteq F_U,n(q; c_sel),
```

   not that `Im_chk,U,n(q; c_sel)` is a singleton;
6. hence non-singletonity is still compatible with all currently closed
   quotient-final theorem-facing constraints, provided the exact admissible
   patch domain realizes two distinct membrane-coordinate values on the same
   fixed fiber;
7. the exact non-singleton / nonvanishing template is therefore:
   if there exist `z_1, z_2 in D_sigma^U,n(q; c_sel)` with

```text
chi_chk,U,n(q)(c_sel + z_1) = (a_sel, b_sel, s_1)^T,
chi_chk,U,n(q)(c_sel + z_2) = (a_sel, b_sel, s_2)^T,
s_1 != s_2,
```

   then all currently closed quotient-final invariants stay the same while

```text
sigma_chk,n(q; c_sel + z_1, c_sel + z_2) = s_1 - s_2 != 0,
```

   so singletonity fails on that exact patch;
8. therefore the single exact missing ingredient after `T3p` is now sharper:
   one needs a representative-sensitive theorem on the exact admissible patch
   domain, not another quotient-final theorem, in order to force singletonity.

So the strongest honest `T3q` endpoint is an exact obstruction theorem:
the current repo/theory boundary still does not decide singletonity, but it now
isolates the remaining gap as one precise missing representative law inside the
fixed membrane fiber on each exact admissible patch.

### Why this is sharper than `T3p`

`T3p` isolated the remaining freedom as a possible nonsingleton subset of the
fixed membrane fiber. `T3q` goes one step further: it identifies exactly why
the current theorem-facing package still cannot decide that singletonity. The
reason is not merely that singletonity is open; it is that all currently closed
checked-local invariants remain quotient-final and therefore are incapable, by
their present form alone, of selecting one representative inside a fixed
membrane fiber.

## Comparison with the earlier routes

The comparison with the earlier theorem-facing routes is now explicit.

1. Raw same-trace shadow route:
   too collapsed, because compatible raw shadows on `D_res,n(q)` already factor
   through the zero quotient class and lose the representative-level membrane
   datum entirely.
2. Pairwise route from `T3l`:
   necessary intermediate step, because it first recovers the surviving
   representative-sensitive checked-local difference object on equal-trace
   pairs.
3. Cocycle route from `T3m`:
   packages that pairwise object as the chart-invariant selector `sigma_chk`,
   but cocycle laws alone do not force vanishing and do not say which extra
   theorem could force it.
4. Patchwise-constancy route from `T3n` / `T3o`:
   shows that selector vanishing is equivalent to constancy of the local
   membrane coordinate and that overlap compatibility is automatic.
5. Membrane-fiber singleton route from `T3p`:
   packages the same issue as singletonity of the exact patch image inside the
   fixed fiber `{ (a_sel, b_sel, s) }`.
6. Representative-law route from `T3q`:
   makes explicit that singletonity and patchwise constancy are not stronger
   than one another on an exact patch; they are equivalent formulations of one
   missing representative-sensitive law `Rep_U`.

So singletonity is strictly stronger than the earlier raw-shadow and cocycle
packages in the sense of localization of the remaining freedom, but it is not
stronger than patchwise constancy after `T3p`; those two are exact equivalent
reformulations on each exact patch.

## Minimal `T3q` lemma split

### `T3q-L1`. Exact patch-domain / representative-law lemma

Statement:

For every exact admissible residual-generated checked-local patch
`D_sigma^U,n(q; c_sel)`, the patchwise representative law
`Rep_U,n(q; c_sel)` is well-defined, and because the quotient coordinates are
fixed on that patch it is equivalent to singletonity of `Im_chk,U` in the
fixed membrane fiber.

Status:
- closed enough.

Verification method:
- manual derivation;
- code inspection;
- reuse of the `T3p` patch-image package.

### `T3q-L2`. Representative law vs selector-vanishing lemma

Statement:

On every exact patch `D_sigma^U,n(q; c_sel)`, the following are equivalent:

```text
Rep_U;
sigma_chk = 0 on D_sigma^U;
s_U is constant on D_sigma^U;
S_U is a singleton;
Im_chk,U is a singleton in F_U.
```

Status:
- closed enough.

Verification method:
- manual derivation;
- CAS;
- code inspection.

### `T3q-L3`. Quotient-finality obstruction lemma

Statement:

All currently justified checked-local invariants on the present boundary factor
through the quotient map `(a, b, s) -> (a, b)` or are blind along the membrane
line. Therefore no theorem using only the currently closed quotient-final
package can force `Rep_U` on an exact patch.

Status:
- closed enough as an exact obstruction theorem.

Verification method:
- theorem reuse from pilot 23 quotient-finality;
- code inspection;
- manual derivation.

### `T3q-L4`. Exact non-singleton / nonvanishing-template lemma

Statement:

If one exact admissible patch contains two points with the same quotient
coordinates `(a_sel, b_sel)` and different membrane coordinates `s_1 != s_2`,
then all currently closed quotient-final invariants agree on that pair while
singletonity fails and the pairwise selector is nonzero.

Status:
- closed enough as an exact obstruction/template theorem;
- explicit admissible realization still open.

Verification method:
- manual derivation;
- theorem reuse from `T3l` / `T3m` / `T3p`;
- code inspection.

### `T3q-L5`. Exact consequence lemma for the next reverse-inclusion / zero-excess bridge

Statement:

If one proves `Rep_U,n(q; c_sel)` on every exact admissible residual-generated
checked-local patch of every exact cover, then
`sigma_chk,n(q; c_sel)(z) = 0` on all of `D_sigma,n(q; c_sel)`, hence the
remaining membrane obstruction in the reverse-inclusion / zero-excess bridge
disappears on the current boundary. Conversely, any admissible nonsingleton
patch yields an exact nonvanishing obstruction.

Status:
- closed enough as a theorem-program consequence.

Verification method:
- manual derivation;
- Lean target after the exact representative-law abstraction is packaged.

## Single next bottleneck after `T3q`

The single next bottleneck is now:

```text
prove or refute the exact patchwise representative law
Rep_U,n(q; c_sel)
on every exact admissible residual-generated checked-local patch
D_sigma^U,n(q; c_sel),
equivalently prove or refute that
S_U,n(q; c_sel) = { s_U(0) }
on every such patch.
```

This is sharper than `T3p`: the next missing ingredient is no longer just
"singletonity somewhere in the fiber", but one theorem-level
representative-sensitive law that cannot factor only through the quotient
coordinates.

## Lean / CAS / manual split for `T3q`

Lean:
- finite-dimensional patch-image / representative-law / singletonity templates
  once the exact patch-domain and fixed-fiber formulation are abstracted.

CAS / code inspection:
- `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, exact patchwise chart formulas, and the factorization of the
  currently justified checked-local invariants through the quotient map.

Manual derivation:
- exact theorem scope for `T3q`;
- exact wording of the representative-law obstruction;
- why current theorem-facing constraints are still quotient-final on the exact
  patches;
- comparison of singletonity with the earlier constancy, cocycle, pairwise,
  and raw-shadow routes;
- relation of `T3q` to the future reverse-inclusion / zero-excess bridge below
  full `T3`.

## Conservative status after `T3q`

Closed enough now:
- the exact patch-domain / fixed-fiber / representative-law formulation of the
  singletonity problem;
- the equivalence between patchwise representative law, selector vanishing,
  patchwise constancy, and membrane-fiber singletonity;
- the exact obstruction theorem that current theorem-facing constraints remain
  quotient-final and therefore do not force singletonity by themselves;
- the exact non-singleton template at the level of two realized membrane
  coordinates on one exact admissible patch.

Still open:
- whether the exact admissible patch domain actually realizes more than one
  membrane-coordinate value on some patch;
- whether a representative-sensitive theorem closes `Rep_U` on the full exact
  patch cover;
- hence whether the remaining membrane obstruction is truly present or already
  trivial on the current theorem-facing candidate boundary.

So the gap is sharper than after `T3p`: the remaining question is no longer
only whether the patch image is a singleton, but exactly whether one can derive
an intrinsic representative law on the exact admissible patch domain that is
strong enough to force that singletonity.

## Exact `T3r` theorem target

For fixed clean `(n, q)`, fixed repo-selected basepoint

```text
c_sel in A_sel^repo,n(q),
```

and every exact admissible residual-generated checked-local patch

```text
D_sigma^U,n(q; c_sel),
```

the exact `T3r` target is to prove or refute the patchwise representative law

```text
Rep_U,n(q; c_sel) :
chi_chk,U,n(q)(c_sel + z_1) = chi_chk,U,n(q)(c_sel + z_2)
for all z_1, z_2 in D_sigma^U,n(q; c_sel).
```

By the already closed `T3p` / `T3q` package, this is equivalent to:

```text
Im_chk,U,n(q; c_sel) is a singleton;
S_U,n(q; c_sel) is a singleton;
s_U is constant on D_sigma^U,n(q; c_sel);
sigma_chk,n(q; c_sel)(z) = 0 on D_sigma^U,n(q; c_sel).
```

The relevant exact domain family is still the admissible residual-generated
checked-local patch cover

```text
{ D_sigma^U,n(q; c_sel) }_U
```

of the exact definability domain `D_sigma,n(q; c_sel)`.

Outside scope for `T3r`:

- not full `T3`;
- not final physical criticality;
- not a collapse to `B_red` / `B_mix`;
- not a reopening of the frozen local Outcome-B branch.

## Exact patch-domain and pointwise representative setting

The exact global same-trace definability domain remains

```text
D_sigma,n(q; c_sel)
  := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
       (c_sel + z, c_sel) in Pair_chk,n(q) }.
```

For a corrected chart `U`, the exact patch is

```text
D_sigma^U,n(q; c_sel)
  := { z in D_sigma,n(q; c_sel) :
       (c_sel + z, c_sel) is represented in one common corrected chart U }.
```

So the domain-of-definition conditions for `chi_chk,U,n(q)(c_sel + z)` on that
patch are exactly:

1. `z in A_adm^th,n(q) intersect ker(C_center,n(q))`;
2. the pair `(c_sel + z, c_sel)` belongs to `Pair_chk,n(q)`;
3. one common corrected chart `U` represents both `c_sel + z` and `c_sel`.

On such a patch one has

```text
chi_chk,U,n(q)(c_sel + z) = (a_sel, b_sel, s_U(z))^T,
chi_chk,U,n(q)(c_sel)     = (a_sel, b_sel, s_U(0))^T,
```

so the whole patch image already lies in the fixed membrane fiber

```text
F_U,n(q; c_sel) = { (a_sel, b_sel, s)^T : s in R }.
```

The sharper pointwise object for `T3r` is therefore the basepoint-relative
checked-local representative difference

```text
Delta_rep,U^pt,n(q; c_sel)(z)
  := chi_chk,U,n(q)(c_sel + z) - chi_chk,U,n(q)(c_sel).
```

Because both representatives lie in the same fixed fiber, one has exactly

```text
Delta_rep,U^pt,n(q; c_sel)(z)
  = (0, 0, s_U(z) - s_U(0))^T
  = sigma_chk,n(q; c_sel)(z) e_mem
  in span(e_mem).
```

So `T3r` reduces the pairwise law `Rep_U` to the pointwise basepoint law

```text
Rep_U^0,n(q; c_sel) :
chi_chk,U,n(q)(c_sel + z) = chi_chk,U,n(q)(c_sel)
for every z in D_sigma^U,n(q; c_sel).
```

Equivalently,

```text
Rep_U  <->  Rep_U^0  <->  Delta_rep,U^pt = 0 on D_sigma^U.
```

Singletonity is still tested patchwise on the exact cover and globally only via
that cover. By `T3o`, overlap compatibility is already automatic, so no
separate gluing theorem remains.

## Outcome reached in this turn

Outcome B.

`Rep_U` is still not proved. But the remaining obstruction is now sharper than
in `T3q`: failure of the full pairwise representative law is exactly
equivalent to one pointwise basepoint-relative nonvanishing statement on an
exact patch.

## Strongest exact result obtained about `Rep_U`

### Theorem `T3r`

For fixed clean `(n, q)`, fixed repo-selected basepoint `c_sel`, and any exact
admissible residual-generated checked-local patch `D_sigma^U,n(q; c_sel)`:

1. the pairwise representative law `Rep_U,n(q; c_sel)` is exactly equivalent
   to the pointwise basepoint law

```text
Rep_U^0,n(q; c_sel) :
chi_chk,U,n(q)(c_sel + z) = chi_chk,U,n(q)(c_sel)
for every z in D_sigma^U,n(q; c_sel);
```

2. equivalently,

```text
Rep_U
<-> Rep_U^0
<-> Delta_rep,U^pt,n(q; c_sel)(z) = 0 for every z in D_sigma^U
<-> sigma_chk,n(q; c_sel)(z) = 0 for every z in D_sigma^U;
```

3. because

```text
Delta_rep,U^pt,n(q; c_sel)(z) = sigma_chk,n(q; c_sel)(z) e_mem,
```

   current admissibility and candidate constraints force only

```text
Delta_rep,U^pt,n(q; c_sel)(z) in span(e_mem),
```

   not

```text
Delta_rep,U^pt,n(q; c_sel)(z) = 0;
```

4. equivalently, all currently closed theorem-facing constraints still control
   only the fixed quotient coordinates `(a_sel, b_sel)` and remain blind to the
   scalar membrane deviation

```text
sigma_chk,n(q; c_sel)(z) = s_U(z) - s_U(0);
```

5. hence non-singletonity is still compatible with all currently closed
   theorem-facing constraints provided there exists one patch point

```text
z_* in D_sigma^U,n(q; c_sel)
```

   such that

```text
Delta_rep,U^pt,n(q; c_sel)(z_*) != 0,
```

   equivalently

```text
sigma_chk,n(q; c_sel)(z_*) != 0;
```

6. this yields the sharpest exact non-singleton / nonvanishing template now
   available on the exact patch domain:

```text
chi_chk,U,n(q)(c_sel + z_*)
  = (a_sel, b_sel, s_*)^T,
chi_chk,U,n(q)(c_sel)
  = (a_sel, b_sel, s_sel)^T,
s_* != s_sel;
```

7. therefore the exact remaining degree of freedom is no longer a general
   two-point comparison on the patch, but one basepoint-relative membrane
   deviation invisible to the current quotient-final theorem-facing package.

So the strongest honest `T3r` endpoint is an exact obstruction theorem:
`Rep_U` is reduced to pointwise vanishing of the basepoint-relative membrane
deviation on each exact patch, and the current checked-local package still does
not force that pointwise vanishing.

### Reduction of the proof routes

The strongest plausible proof routes now collapse to the same pointwise object.

1. Direct representative-law route:
   prove `Rep_U` by proving `Rep_U^0` on every exact patch.
2. Selector route:
   prove `sigma_chk,n(q; c_sel)(z) = 0` pointwise on every exact patch, then
   recover `Rep_U`.
3. Fiber route:
   prove that admissibility/candidate constraints force the pointwise
   membrane-fiber deviation `Delta_rep,U^pt(z)` to vanish, not merely to lie in
   `span(e_mem)`.
4. Reduction route:
   because of cocycle normalization and the presence of the fixed basepoint
   `c_sel`, arbitrary pairwise equality on the patch reduces exactly to the
   one-point basepoint-relative law `Rep_U^0`.

No further exact reduction to a smaller set of basepoints, a finite list of
residuals, or a quotient-final theorem is currently justified.

## Comparison with the earlier routes

The relation to the earlier theorem-facing routes is now:

1. Raw same-trace shadow route:
   too collapsed, because it already loses the representative-level membrane
   datum before one can even state `Rep_U`.
2. Pairwise route from `T3l`:
   necessary, because it constructs the surviving representative-sensitive
   difference object.
3. Cocycle route from `T3m`:
   necessary, because it packages that difference as the exact selector
   `sigma_chk`, but cocycle laws alone still permit nonzero pointwise values.
4. Patchwise constancy / singletonity routes from `T3n` / `T3p` / `T3q`:
   equivalent to `Rep_U` on each exact patch, but less sharp than the
   basepoint-relative wording of `T3r`.
5. `T3r` route:
   cleanest current bottleneck statement, because it reduces the full pairwise
   patch law to vanishing of one pointwise basepoint-relative object
   `Delta_rep,U^pt(z)`.

So `Rep_U` is not stronger than patchwise constancy or singletonity on a fixed
patch; all of these are equivalent. The sharpened gain in `T3r` is that the
obstruction is now one-point and basepoint-relative, not merely pairwise or
set-valued.

## Minimal `T3r` lemma split

### `T3r-L1`. Exact patch-domain / fixed-fiber / pointwise-difference lemma

Statement:

For every exact admissible residual-generated checked-local patch
`D_sigma^U,n(q; c_sel)`, one has `0 in D_sigma^U,n(q; c_sel)` and the
pointwise basepoint-relative representative difference

```text
Delta_rep,U^pt,n(q; c_sel)(z)
  := chi_chk,U,n(q)(c_sel + z) - chi_chk,U,n(q)(c_sel)
```

is well-defined and lies in `span(e_mem)`.

Status:
- closed enough.

Verification method:
- manual derivation;
- CAS;
- code inspection.

### `T3r-L2`. Pairwise representative law vs pointwise basepoint law lemma

Statement:

On every exact patch `D_sigma^U,n(q; c_sel)`, the following are equivalent:

```text
Rep_U;
Rep_U^0;
Delta_rep,U^pt = 0 on D_sigma^U;
sigma_chk = 0 on D_sigma^U;
s_U is constant on D_sigma^U;
Im_chk,U is a singleton.
```

Status:
- closed enough.

Verification method:
- manual derivation;
- CAS;
- code inspection.

### `T3r-L3`. Quotient-finality obstruction lemma

Statement:

Current theorem-facing admissibility and candidate constraints force only the
fixed quotient coordinates `(a_sel, b_sel)` and therefore only
`Delta_rep,U^pt(z) in span(e_mem)`. They do not force
`Delta_rep,U^pt(z) = 0`.

Status:
- closed enough as an exact obstruction theorem.

Verification method:
- theorem reuse from pilot 23 quotient-finality;
- manual derivation;
- code inspection.

### `T3r-L4`. Exact one-point non-singleton / nonvanishing-template lemma

Statement:

Failure of `Rep_U` on an exact patch is equivalent to existence of one point
`z_* in D_sigma^U,n(q; c_sel)` such that

```text
Delta_rep,U^pt,n(q; c_sel)(z_*) = delta_* e_mem,
delta_* != 0.
```

Equivalently, one exact patch point already realizes a distinct membrane
coordinate above the same fixed quotient base point `(a_sel, b_sel)`.

Status:
- closed enough as an exact obstruction/template theorem;
- explicit admissible realization still open.

Verification method:
- manual derivation;
- theorem reuse from `T3m` / `T3q`;
- code inspection.

### `T3r-L5`. Exact consequence lemma for the next bridge step

Statement:

If one proves the pointwise basepoint law `Rep_U^0,n(q; c_sel)` on every exact
admissible residual-generated checked-local patch of every exact cover, then
`Rep_U` holds on every such patch, `sigma_chk` vanishes on
`D_sigma,n(q; c_sel)`, and the remaining membrane obstruction in the
reverse-inclusion / zero-excess bridge disappears on the current boundary.

Status:
- closed enough as a theorem-program consequence.

Verification method:
- manual derivation;
- Lean target after the pointwise basepoint-relative abstraction is packaged.

## Single next bottleneck after `T3r`

The single next bottleneck is now:

```text
prove or refute the pointwise basepoint-relative law
chi_chk,U,n(q)(c_sel + z) = chi_chk,U,n(q)(c_sel)
for every z in every exact admissible residual-generated checked-local patch
D_sigma^U,n(q; c_sel),
equivalently prove or refute that
Delta_rep,U^pt,n(q; c_sel)(z) = 0
on the full exact patch cover.
```

This is sharper than `T3q`: the remaining gap is not merely a pairwise
representative law, but one pointwise vanishing theorem for the exact
basepoint-relative membrane deviation.

## Lean / CAS / manual split for `T3r`

Lean:
- finite-dimensional patch-image / pointwise representative-law / selector-
  vanishing templates once the exact patch-domain and pointwise basepoint
  difference law are abstracted.

CAS / code inspection:
- `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, exact patchwise chart formulas, and the identity
  `Delta_rep,U^pt = sigma_chk e_mem`.

Manual derivation:
- exact theorem scope for `T3r`;
- why the pairwise representative law reduces to a pointwise basepoint law;
- why current theorem-facing constraints still do not force that pointwise
  vanishing;
- why the sharpest remaining non-singleton template is now one-point rather
  than genuinely pairwise;
- relation of `T3r` to the future reverse-inclusion / zero-excess bridge below
  full `T3`.

## Conservative status after `T3r`

Closed enough now:

- the exact reduction of `Rep_U` to a pointwise basepoint-relative law on each
  exact admissible patch;
- the equivalence between that pointwise law, selector vanishing, patchwise
  constancy, and singletonity of the exact checked-local patch image;
- the exact obstruction theorem that current theorem-facing constraints still
  force only membrane-line containment of the pointwise representative
  difference and not its vanishing;
- the sharpest currently justified non-singleton template: one exact patch
  point with nonzero basepoint-relative membrane deviation.

Still open:

- whether such a nonzero pointwise membrane deviation can actually be realized
  on the exact admissible patch domain;
- whether a representative-sensitive theorem kills that deviation on the full
  exact patch cover;
- hence whether the remaining membrane obstruction is truly present or already
  trivial on the current theorem-facing candidate boundary.

So the gap is sharper than after `T3q`: the remaining question is no longer
only whether all representatives on a patch coincide pairwise, but exactly
whether the basepoint-relative representative deviation vanishes pointwise on
the full exact admissible patch cover.
## Exact `T3s` theorem target

The exact `T3s` target is now the pointwise basepoint-relative law written in a
chart-invariant form on the full exact pair-definability domain.

Fix clean `(n, q)` and a repo-selected basepoint

```text
c_sel in A_sel^repo,n(q).
```

Keep the exact domain

```text
D_sigma,n(q; c_sel)
  := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
       (c_sel + z, c_sel) in Pair_chk,n(q) }.
```

For every corrected chart `U`, keep the exact patch

```text
D_sigma^U,n(q; c_sel)
  := { z in D_sigma,n(q; c_sel) :
       (c_sel + z, c_sel) is represented in one common corrected chart U }.
```

On every such patch, `T3r` already defines

```text
Delta_rep,U^pt,n(q; c_sel)(z)
  := chi_chk,U,n(q)(c_sel + z) - chi_chk,U,n(q)(c_sel)
  = sigma_chk,n(q; c_sel)(z) e_mem.
```

The new `T3s` question is whether this patchwise object descends to one exact
chart-invariant pointwise defect map on `D_sigma,n(q; c_sel)` and then vanishes
there identically:

```text
Delta_rep^pt,n(q; c_sel) : D_sigma,n(q; c_sel) -> span(e_mem),
Delta_rep^pt,n(q; c_sel)(z) = 0  for every z in D_sigma,n(q; c_sel).
```

Equivalently:

```text
sigma_chk,n(q; c_sel)(z) = 0  for every z in D_sigma,n(q; c_sel).
```

By `T3r-L2`, this is also equivalent to:

- `Rep_U,n(q; c_sel)` on every exact admissible residual-generated checked-local
  patch;
- singletonity of `Im_chk,U,n(q; c_sel)` on every such patch;
- constancy of `s_U` on every such patch.

Outside scope for `T3s`:

- not full `T3`;
- not final physical criticality;
- not a collapse to `B_red` / `B_mix`;
- not a reopening of the frozen local branch;
- not a new numerical campaign.

## Exact pointwise domain and chart-invariant pointwise defect map

The exact pointwise object is now defined as follows.

### 1. Domain-of-definition

For a point `z`, the local difference

```text
Delta_rep,U^pt,n(q; c_sel)(z)
```

is defined exactly when all three conditions hold:

1. `z in A_adm^th,n(q) intersect ker(C_center,n(q))`;
2. `(c_sel + z, c_sel) in Pair_chk,n(q)`;
3. the pair `(c_sel + z, c_sel)` is represented in one common corrected chart
   `U`.

So the exact global domain is `D_sigma,n(q; c_sel)`, and the patch family
`{ D_sigma^U,n(q; c_sel) }_U` is any cover of that domain by common corrected
charts.

The dependence on `c_sel` is essential:
the same-trace condition itself depends only on `ker(C_center)`, but the exact
pair-definability condition `(c_sel + z, c_sel) in Pair_chk,n(q)` and the
anchoring of the pointwise difference both use the fixed repo-selected
basepoint.

### 2. Patch transport and chart invariance

Suppose `z` lies in two patches `D_sigma^U,n(q; c_sel)` and
`D_sigma^V,n(q; c_sel)` with overlap relation

```text
chi_chk,V = S_(ell1,ell2)^(-1) chi_chk,U,
S_(ell1,ell2)^(-1)
  = [[1,0,0],[0,1,0],[-ell1,-ell2,1]].
```

Then

```text
Delta_rep,V^pt(z)
  = chi_chk,V(c_sel + z) - chi_chk,V(c_sel)
  = S_(ell1,ell2)^(-1) Delta_rep,U^pt(z).
```

But `T3r` already gives

```text
Delta_rep,U^pt(z) in span(e_mem),
e_mem = (0,0,1)^T,
S_(ell1,ell2)^(-1) e_mem = e_mem.
```

Hence

```text
Delta_rep,V^pt(z) = Delta_rep,U^pt(z).
```

Therefore the pointwise basepoint-relative difference descends to the exact
chart-invariant map

```text
Delta_rep^pt,n(q; c_sel) : D_sigma,n(q; c_sel) -> span(e_mem),
Delta_rep^pt,n(q; c_sel)(z)
  := Delta_rep,U^pt,n(q; c_sel)(z)
```

for any patch `U` containing `z`.

### 3. Exact pointwise formula

For every `z in D_sigma,n(q; c_sel)`, one has

```text
Delta_rep^pt,n(q; c_sel)(z)
  = sigma_chk,n(q; c_sel)(z) e_mem.
```

So the pointwise law is now a global exact statement on `D_sigma,n(q; c_sel)`,
not merely a patch-relative statement:

```text
Delta_rep^pt,n(q; c_sel)(z) = 0
iff
sigma_chk,n(q; c_sel)(z) = 0.
```

Because `sigma_chk,n(q; c_sel)(0) = 0`, one also has

```text
Delta_rep^pt,n(q; c_sel)(0) = 0.
```

So `T3s` is local in the sense that it is tested pointwise, but it is no
longer chart-local:
vanishing/nonvanishing at one fixed `z` can be checked in any patch containing
that point.

## Strongest exact result obtained about the pointwise law

### Theorem `T3s`

For fixed clean `(n, q)` and fixed repo-selected basepoint

```text
c_sel in A_sel^repo,n(q),
```

let `D_sigma,n(q; c_sel)` be the exact admissible residual-generated
checked-local pair domain above.

Then:

1. the patchwise pointwise-difference object from `T3r` descends to an exact
   chart-invariant pointwise map

```text
Delta_rep^pt,n(q; c_sel) : D_sigma,n(q; c_sel) -> span(e_mem);
```

2. for every `z in D_sigma,n(q; c_sel)` one has the exact identity

```text
Delta_rep^pt,n(q; c_sel)(z)
  = sigma_chk,n(q; c_sel)(z) e_mem;
```

3. therefore the following are equivalent:

```text
Delta_rep^pt,n(q; c_sel)(z) = 0  for every z in D_sigma,n(q; c_sel);
sigma_chk,n(q; c_sel)(z) = 0     for every z in D_sigma,n(q; c_sel);
Rep_U,n(q; c_sel) holds on every exact admissible patch;
Im_chk,U,n(q; c_sel) is a singleton on every exact admissible patch.
```

4. current theorem-facing admissibility / candidate constraints still force
   only

```text
Delta_rep^pt,n(q; c_sel)(z) in span(e_mem)
```

   together with the normalization

```text
Delta_rep^pt,n(q; c_sel)(0) = 0,
```

   and they do not force

```text
Delta_rep^pt,n(q; c_sel)(z) = 0
```

   at an arbitrary exact admissible point;

5. define the exact pointwise nonzero set

```text
N_sigma,n(q; c_sel)
  := { z in D_sigma,n(q; c_sel) :
       Delta_rep^pt,n(q; c_sel)(z) != 0 }
   = { z in D_sigma,n(q; c_sel) :
       sigma_chk,n(q; c_sel)(z) != 0 }.
```

   Then `T3s` closes if and only if

```text
N_sigma,n(q; c_sel) = emptyset;
```

6. all currently closed theorem-facing constraints remain compatible with
   `N_sigma,n(q; c_sel) != emptyset`; an explicit admissible point in that set
   is still not constructed.

So the strongest honest `T3s` endpoint is again an exact obstruction theorem:
the pointwise law becomes a global chart-invariant defect map on the full exact
domain, but current theorem-facing structure still does not force that map to
vanish identically.

## Reduction of the proof routes

After `T3s`, the strongest plausible proof routes all reduce to the same exact
global pointwise object.

1. Direct pointwise-vanishing route:
   prove
   `Delta_rep^pt,n(q; c_sel)(z) = 0`
   for every `z in D_sigma,n(q; c_sel)`.
2. Selector route:
   prove
   `sigma_chk,n(q; c_sel)(z) = 0`
   on `D_sigma,n(q; c_sel)` and use
   `Delta_rep^pt = sigma_chk e_mem`.
3. Fiber route:
   prove that exact admissibility/candidate constraints kill the remaining
   scalar membrane coefficient along `span(e_mem)` at each point, not merely
   the quotient coordinates.
4. Reduction route:
   because the pointwise defect is chart-invariant, the theorem is no longer an
   all-pairs or all-overlaps problem; it is enough to test one patch containing
   each `z`.

No further reduction to a smaller exact family of basepoints, residuals, or
patches is currently justified.

## Comparison with the earlier routes

The present pointwise formulation is the cleanest current bottleneck statement
for the following reasons.

1. Raw same-trace shadows were too collapsed:
   they already land in the membrane line and cannot distinguish zero from
   nonzero representative displacement there.
2. The pairwise route from `T3l` was necessary:
   it recovered the surviving representative-sensitive difference before
   quotient collapse.
3. The cocycle route from `T3m` was necessary but insufficient:
   antisymmetry, cocycle additivity, and normalization at `0` still permit a
   nonzero pointwise selector value.
4. The constancy/singletonity/`Rep_U` routes from `T3p` / `T3q` / `T3r` are not
   stronger on a fixed patch; they are equivalent after choosing the
   repo-selected basepoint and the fixed membrane fiber.
5. The gain in `T3s` is sharper wording of the obstruction:
   the remaining issue is now one global chart-invariant pointwise defect map
   and the emptiness or nonemptiness of its exact nonzero set.

So the pointwise formulation is not stronger than `Rep_U` on a fixed patch, but
it is strictly sharper as the current obstruction package because it no longer
depends on a chosen patch index.

## Minimal `T3s` lemma split

### `T3s-L1`. Exact pointwise domain / chart-invariant pointwise-difference lemma

Statement:

For every fixed clean `(n, q)` and repo-selected basepoint `c_sel`, the
patchwise pointwise-difference maps `Delta_rep,U^pt,n(q; c_sel)` glue on
overlaps and define an exact chart-invariant map

```text
Delta_rep^pt,n(q; c_sel) : D_sigma,n(q; c_sel) -> span(e_mem),
Delta_rep^pt(z) = sigma_chk,n(q; c_sel)(z) e_mem.
```

Status:
- closed enough.

Verification method:
- manual derivation;
- CAS;
- code inspection.

### `T3s-L2`. Pointwise law vs selector-vanishing vs `Rep_U` lemma

Statement:

On the exact domain `D_sigma,n(q; c_sel)`, the following are equivalent:

```text
Delta_rep^pt,n(q; c_sel)(z) = 0  for all z in D_sigma;
sigma_chk,n(q; c_sel)(z) = 0     for all z in D_sigma;
Rep_U,n(q; c_sel) holds on every exact patch;
s_U is constant on every exact patch;
Im_chk,U is a singleton on every exact patch.
```

Status:
- closed enough.

Verification method:
- manual derivation;
- CAS;
- code inspection.

### `T3s-L3`. Pointwise codomain / normalization obstruction lemma

Statement:

Current theorem-facing admissibility and candidate constraints force only

```text
Delta_rep^pt(D_sigma,n(q; c_sel)) subseteq span(e_mem)
```

and the normalization

```text
Delta_rep^pt,n(q; c_sel)(0) = 0,
```

but not the full pointwise vanishing theorem on `D_sigma,n(q; c_sel)`.

Status:
- closed enough as an exact obstruction theorem.

Verification method:
- theorem reuse from pilot 23 quotient-finality;
- manual derivation;
- code inspection.

### `T3s-L4`. Exact pointwise nonzero-set / one-point template lemma

Statement:

Failure of the `T3s` pointwise law is equivalent to nonemptiness of

```text
N_sigma,n(q; c_sel)
  := { z in D_sigma,n(q; c_sel) :
       Delta_rep^pt,n(q; c_sel)(z) != 0 }.
```

Equivalently, there exists one point `z_* in D_sigma,n(q; c_sel)` such that

```text
Delta_rep^pt,n(q; c_sel)(z_*) = delta_* e_mem,
delta_* != 0.
```

Status:
- closed enough as an exact obstruction/template theorem;
- explicit admissible realization still open.

Verification method:
- manual derivation;
- theorem reuse from `T3m` / `T3o` / `T3r`;
- code inspection.

### `T3s-L5`. Exact consequence lemma for the next bridge step

Statement:

If one proves

```text
N_sigma,n(q; c_sel) = emptyset
```

for every fixed clean `(n, q)` and repo-selected basepoint `c_sel`, then the
pointwise law holds on the full exact domain, hence `Rep_U` holds on every
exact patch, `sigma_chk` vanishes on `D_sigma,n(q; c_sel)`, and the remaining
membrane obstruction in the reverse-inclusion / zero-excess bridge disappears
on the current theorem-facing boundary.

Status:
- closed enough as a theorem-program consequence.

Verification method:
- manual derivation;
- Lean target after the chart-invariant pointwise-defect abstraction is
  packaged.

## Single next bottleneck after `T3s`

The single next bottleneck is now:

```text
prove or refute that
N_sigma,n(q; c_sel) = emptyset
for every fixed clean (n, q) and repo-selected basepoint c_sel,
equivalently prove or refute that
Delta_rep^pt,n(q; c_sel)(z) = 0
for every z in D_sigma,n(q; c_sel).
```

This is sharper than `T3r`:
the remaining gap is no longer phrased as a patchwise pointwise law, but as
emptiness of one exact chart-invariant global pointwise nonzero set on the full
pair-definability domain.

## Lean / CAS / manual split for `T3s`

Lean:
- finite-dimensional exact-domain / chart-invariant pointwise-defect / nonzero-
  set templates once the overlap-gluing law and the codomain `span(e_mem)` are
  abstracted.

CAS / code inspection:
- `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, the quotient-preserving chart-change matrices
  `S_(ell1,ell2)`, the identity `S_(ell1,ell2)^(-1) e_mem = e_mem`, and
  `Delta_rep^pt = sigma_chk e_mem`.

Manual derivation:
- exact theorem scope for `T3s`;
- why the patchwise pointwise-difference object descends to a global chart-
  invariant pointwise defect map;
- why current theorem-facing constraints still do not force its vanishing;
- why the exact remaining obstruction is now the nonzero set `N_sigma`;
- relation of `T3s` to the future reverse-inclusion / zero-excess bridge below
  full `T3`.

## Conservative status after `T3s`

Closed enough now:

- the exact chart-invariant descent
  `Delta_rep,U^pt -> Delta_rep^pt` on the full exact domain
  `D_sigma,n(q; c_sel)`;
- the exact equivalence between global pointwise vanishing of `Delta_rep^pt`,
  global vanishing of `sigma_chk`, patchwise `Rep_U`, patchwise constancy, and
  patchwise singletonity;
- the exact obstruction theorem that current theorem-facing constraints still
  force only codomain containment in `span(e_mem)` plus the basepoint
  normalization at `z = 0`;
- the sharpest currently justified nonvanishing package: the exact nonzero set
  `N_sigma,n(q; c_sel)` and its one-point realization template.

Still open:

- whether `N_sigma,n(q; c_sel)` is actually empty on the full exact domain;
- whether an explicit admissible point `z_*` with
  `Delta_rep^pt,n(q; c_sel)(z_*) != 0`
  can be realized;
- whether a representative-sensitive theorem kills the pointwise membrane
  deviation everywhere on the exact pair-definability domain.

So the gap is sharper than after `T3r`:
the remaining question is no longer only whether the patchwise pointwise law
holds in each chart, but exactly whether the chart-invariant global pointwise
defect map has empty nonzero set on the full exact admissible domain.

## Exact `T3t` theorem target

The exact `T3t` target is now the emptiness / nonemptiness theorem for the
exact global defect set

```text
N_sigma,n(q; c_sel)
  := { z in D_sigma,n(q; c_sel) :
       Delta_rep^pt,n(q; c_sel)(z) != 0 }
   = { z in D_sigma,n(q; c_sel) :
       sigma_chk,n(q; c_sel)(z) != 0 }.
```

So for fixed clean `(n, q)` and fixed repo-selected basepoint
`c_sel in A_sel^repo,n(q)`, `T3t` asks whether

```text
N_sigma,n(q; c_sel) = emptyset.
```

By the already closed `T3s` package, this is exactly equivalent to

```text
Delta_rep^pt,n(q; c_sel)(z) = 0   for all z in D_sigma,n(q; c_sel),
sigma_chk,n(q; c_sel)(z) = 0      for all z in D_sigma,n(q; c_sel),
Rep_U,n(q; c_sel)                 on every exact admissible patch.
```

Hence it is also equivalent to patchwise singletonity / constancy on every
exact admissible residual-generated checked-local patch.

Relevant exact domain:

```text
D_sigma,n(q; c_sel)
  := { z in A_adm^th,n(q) ∩ ker(C_center,n(q)) :
       (c_sel + z, c_sel) in Pair_chk,n(q) }.
```

Outside scope for `T3t`:

- not full `T3`;
- not final physical criticality;
- not a collapse to `B_red` / `B_mix`;
- not a reopening of the frozen local branch;
- not a new numerical campaign.

## Exact global defect-set setting

The exact admissible residual-generated domain is the same `D_sigma,n(q; c_sel)`
from `T3s`.

For every `z in D_sigma,n(q; c_sel)`, choose any corrected checked-local chart
`U` on which both `c_sel` and `c_sel + z` are defined, and set

```text
Delta_rep^pt,n(q; c_sel)(z)
  := chi_chk,U,n(q)(c_sel + z) - chi_chk,U,n(q)(c_sel).
```

By `T3s`, this is independent of the chosen exact patch and defines a global
chart-invariant map

```text
Delta_rep^pt,n(q; c_sel) : D_sigma,n(q; c_sel) -> span(e_mem),
Delta_rep^pt,n(q; c_sel)(z) = sigma_chk,n(q; c_sel)(z) e_mem.
```

So the exact defect set is equivalently

```text
N_sigma,n(q; c_sel)
  = (Delta_rep^pt,n(q; c_sel))^(-1)(span(e_mem) \ {0})
  = sigma_chk,n(q; c_sel)^(-1)(R \ {0}).
```

The pointwise map is defined exactly when `z in D_sigma,n(q; c_sel)`; that is,
exactly when the pair `(c_sel + z, c_sel)` belongs to the admissible checked-
local pair domain and can therefore be represented in some corrected local
chart. The domain depends essentially on `c_sel`, because exact pair-
definability is measured relative to that fixed repo-selected basepoint.

A sharper scalar reformulation is now available. Define the exact scalar defect
image

```text
Sigma_sigma,n(q; c_sel)
  := { delta in R : exists z in D_sigma,n(q; c_sel),
       Delta_rep^pt,n(q; c_sel)(z) = delta e_mem }
   = { sigma_chk,n(q; c_sel)(z) : z in D_sigma,n(q; c_sel) }.
```

Then

```text
N_sigma,n(q; c_sel) = emptyset
iff
Sigma_sigma,n(q; c_sel) = {0}.
```

This is the cleanest current exact setting because the remaining issue is no
longer indexed by a chosen patch or pair once `Delta_rep^pt` is global: it is
exactly the emptiness or nonemptiness of one chart-invariant defect set,
equivalently collapse or noncollapse of one scalar image set.

## Attack on emptiness of `N_sigma`

### Theorem `T3t`

Fix clean `(n, q)` and `c_sel in A_sel^repo,n(q)`.

1. The current theorem-facing admissibility / candidate package implies

   ```text
   Delta_rep^pt(D_sigma,n(q; c_sel)) subseteq span(e_mem),
   0 in Sigma_sigma,n(q; c_sel),
   Delta_rep^pt,n(q; c_sel)(0) = 0,
   ```

   but it does not force the stronger statement

   ```text
   Sigma_sigma,n(q; c_sel) = {0}.
   ```

2. Whenever `(c_sel + z_1, c_sel + z_2) in Pair_chk,n(q)`, the surviving
   representative-sensitive difference factors through scalar defect values:

   ```text
   Delta_rep,chk,n(q; c_sel + z_1, c_sel + z_2)
     = Delta_rep^pt,n(q; c_sel)(z_1) - Delta_rep^pt,n(q; c_sel)(z_2)
     = (sigma_chk,n(q; c_sel)(z_1) - sigma_chk,n(q; c_sel)(z_2)) e_mem.
   ```

   So all remaining pairwise representative information is already controlled
   by differences of values in `Sigma_sigma,n(q; c_sel)`.

3. Therefore `T3t` closes if and only if

   ```text
   Sigma_sigma,n(q; c_sel) = {0},
   ```

   equivalently if and only if

   ```text
   N_sigma,n(q; c_sel) = emptyset.
   ```

4. All currently closed theorem-facing constraints remain compatible with

   ```text
   Sigma_sigma,n(q; c_sel) != {0},
   ```

   equivalently with `N_sigma,n(q; c_sel) != emptyset`; an explicit admissible
   nonzero defect value is still not constructed.

So the strongest honest `T3t` endpoint is again an exact obstruction theorem:
emptiness of the global defect set is now reduced further to one scalar image-
collapse statement, but current theorem-facing structure still does not force
that collapse.

## Reduction of the proof routes

After `T3t`, the strongest plausible proof routes all reduce to the same exact
scalar residual freedom.

1. Direct emptiness route:
   prove `N_sigma,n(q; c_sel) = emptyset` on the full exact domain.
2. Selector route:
   prove `sigma_chk,n(q; c_sel)(z) = 0` for every `z in D_sigma`, then deduce
   `Sigma_sigma = {0}`.
3. Fiber route:
   prove that exact admissibility / candidate constraints kill the remaining
   scalar membrane coefficient above the fixed quotient point at every exact
   admissible point.
4. Reduction route:
   because pairwise representative differences already factor through scalar
   defect values, it is enough to prove collapse of the scalar image set
   `Sigma_sigma`, not to control a larger vector-valued family.
5. Obstruction route:
   isolate the exact surviving degree of freedom as one nonzero scalar value in
   `Sigma_sigma`.
6. Nonempty-template route:
   if `T3t` cannot be proved, characterize a point `z_* in D_sigma` with
   `Delta_rep^pt(z_*) = delta_* e_mem`, `delta_* != 0`, equivalently one exact
   nonzero element `delta_* in Sigma_sigma`.

No further reduction to a smaller exact class of basepoints, patches, or
residuals is currently justified.

## Comparison with the earlier routes

The present defect-set formulation is the cleanest current bottleneck statement
for the following reasons.

1. Raw same-trace shadows were too collapsed:
   they already lost the representative-sensitive scalar defect value along the
   membrane line.
2. The pairwise route from `T3l` was necessary:
   it recovered the surviving representative-sensitive difference before
   quotient collapse.
3. The cocycle route from `T3m` was necessary but insufficient:
   antisymmetry, cocycle additivity, and normalization at `0` control only
   differences of scalar defect values and still permit a noncollapsed scalar
   image.
4. The singletonity / constancy / `Rep_U` routes from `T3p` / `T3q` / `T3r`
   are not stronger after `T3s`; they already reduce to global vanishing of
   `Delta_rep^pt`.
5. The gain in `T3t` is sharper obstruction wording:
   the remaining issue is now not merely a global vanishing map, but the
   emptiness of one exact chart-invariant nonzero set, equivalently collapse of
   one scalar image set to `{0}`.

So the defect-set formulation is not stronger than global vanishing of
`Delta_rep^pt` as a truth condition, but it is strictly sharper as the current
obstruction package because it isolates the exact surviving scalar freedom.

## Minimal `T3t` lemma split

### `T3t-L1`. Exact global defect-map / scalar defect-image / defect-set lemma

Statement:

For fixed clean `(n, q)` and repo-selected basepoint `c_sel`, the exact global
pointwise defect map `Delta_rep^pt,n(q; c_sel)` determines both

```text
N_sigma,n(q; c_sel)
  := { z in D_sigma,n(q; c_sel) : Delta_rep^pt,n(q; c_sel)(z) != 0 }
```

and

```text
Sigma_sigma,n(q; c_sel)
  := { sigma_chk,n(q; c_sel)(z) : z in D_sigma,n(q; c_sel) }.
```

Moreover,

```text
N_sigma = emptyset  iff  Sigma_sigma = {0}.
```

Status:
- closed enough.

Verification method:
- manual derivation;
- CAS;
- code inspection.

### `T3t-L2`. Pairwise defect-difference factorization lemma

Statement:

Whenever `(c_sel + z_1, c_sel + z_2) in Pair_chk,n(q)`, one has

```text
Delta_rep,chk,n(q; c_sel + z_1, c_sel + z_2)
  = (sigma_chk,n(q; c_sel)(z_1) - sigma_chk,n(q; c_sel)(z_2)) e_mem.
```

So every surviving pairwise representative-sensitive difference factors through
scalar defect-value differences.

Status:
- closed enough.

Verification method:
- manual derivation;
- theorem reuse from `T3m` / `T3s`;
- code inspection.

### `T3t-L3`. Emptiness vs selector-vanishing vs image-collapse lemma

Statement:

On the exact domain `D_sigma,n(q; c_sel)`, the following are equivalent:

```text
N_sigma,n(q; c_sel) = emptyset;
Sigma_sigma,n(q; c_sel) = {0};
Delta_rep^pt,n(q; c_sel)(z) = 0    for all z in D_sigma;
sigma_chk,n(q; c_sel)(z) = 0       for all z in D_sigma;
Rep_U,n(q; c_sel)                  on every exact patch.
```

Status:
- closed enough.

Verification method:
- manual derivation;
- CAS;
- code inspection.

### `T3t-L4`. Exact obstruction / nonempty-template lemma

Statement:

Failure of `T3t` is exactly equivalent to either of the following exact forms:

```text
N_sigma,n(q; c_sel) != emptyset,
Sigma_sigma,n(q; c_sel) != {0}.
```

Equivalently, there exists one point `z_* in D_sigma,n(q; c_sel)` and one
scalar `delta_* != 0` such that

```text
Delta_rep^pt,n(q; c_sel)(z_*) = delta_* e_mem,
sigma_chk,n(q; c_sel)(z_*) = delta_*.
```

Status:
- closed enough as an exact obstruction/template theorem;
- explicit admissible realization still open.

Verification method:
- manual derivation;
- theorem reuse from `T3s`;
- code inspection.

### `T3t-L5`. Exact consequence lemma for the next bridge step

Statement:

If one proves

```text
Sigma_sigma,n(q; c_sel) = {0}
```

for every fixed clean `(n, q)` and repo-selected basepoint `c_sel`, then
`N_sigma,n(q; c_sel) = emptyset`, `Delta_rep^pt = 0` on `D_sigma`, `sigma_chk`
vanishes on the full exact domain, `Rep_U` holds on every exact patch, and the
remaining membrane obstruction in the reverse-inclusion / zero-excess bridge
disappears on the current theorem-facing boundary.

Status:
- closed enough as a theorem-program consequence.

Verification method:
- manual derivation;
- Lean target after the scalar defect-image abstraction is packaged.

## Single next bottleneck after `T3t`

The single next bottleneck is now:

```text
prove or refute that
Sigma_sigma,n(q; c_sel) = {0}
for every fixed clean (n, q) and repo-selected basepoint c_sel,
equivalently prove or refute that
N_sigma,n(q; c_sel) = emptyset.
```

This is sharper than `T3s`:
the remaining gap is no longer phrased only as global vanishing of one defect
map, but as collapse of the exact scalar defect image to the singleton `{0}` on
the full exact admissible domain.

## Lean / CAS / manual split for `T3t`

Lean:
- finite-dimensional exact-domain / chart-invariant pointwise-defect /
  scalar-image / defect-set templates after abstracting `Delta_rep^pt`,
  `Sigma_sigma`, and `N_sigma`.

CAS / code inspection:
- `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, the quotient-preserving chart-change matrices
  `S_(ell1,ell2)`, the identity `S_(ell1,ell2)^(-1) e_mem = e_mem`,
  `Delta_rep^pt = sigma_chk e_mem`, and the pairwise factorization through
  scalar defect-value differences.

Manual derivation:
- exact theorem scope for `T3t`;
- why emptiness of `N_sigma` is equivalent to collapse of `Sigma_sigma` to
  `{0}`;
- why current theorem-facing constraints still do not force that collapse;
- why the exact surviving obstruction is one scalar defect value;
- relation of `T3t` to the future reverse-inclusion / zero-excess bridge below
  full `T3`.

## Conservative status after `T3t`

Closed enough now:

- the exact global defect-set formulation
  `N_sigma,n(q; c_sel) = (Delta_rep^pt)^(-1)(span(e_mem) \ {0})`;
- the exact scalar defect-image formulation
  `Sigma_sigma,n(q; c_sel) = { sigma_chk,n(q; c_sel)(z) : z in D_sigma }`;
- the equivalence between emptiness of `N_sigma`, collapse of `Sigma_sigma` to
  `{0}`, global vanishing of `Delta_rep^pt`, global vanishing of `sigma_chk`,
  and patchwise `Rep_U` / constancy / singletonity;
- the exact pairwise factorization of surviving representative-sensitive
  differences through scalar defect-value differences;
- the obstruction theorem that current theorem-facing constraints still force
  only `0 in Sigma_sigma`, not `Sigma_sigma = {0}`.

Still open:

- whether `Sigma_sigma,n(q; c_sel) = {0}` on the full exact domain;
- equivalently whether `N_sigma,n(q; c_sel) = emptyset` on the full exact
  admissible residual-generated pair domain;
- whether an explicit admissible point `z_*` with
  `Delta_rep^pt,n(q; c_sel)(z_*) != 0` can be realized;
- whether a representative-sensitive theorem kills every nonzero scalar defect
  value on the exact checked-local domain.

So the gap is sharper than after `T3s`:
the remaining question is no longer only whether the global pointwise defect map
vanishes, but exactly whether its scalar defect image collapses to `{0}`,
equivalently whether the exact global nonzero defect set is empty.
## Exact `T3u` theorem target

The exact `T3u` target is now the scalar-image collapse theorem

```text
Sigma_sigma,n(q; c_sel) = {0},
```

where

```text
Sigma_sigma,n(q; c_sel)
  := { sigma_chk,n(q; c_sel)(z) : z in D_sigma,n(q; c_sel) }.
```

So for fixed clean `(n, q)` and fixed repo-selected basepoint
`c_sel in A_sel^repo,n(q)`, `T3u` asks whether the exact scalar image of the
chart-invariant membrane selector collapses to the singleton `{0}` on the full
exact admissible residual-generated domain.

By the already closed `T3t` package, this is exactly equivalent to

```text
N_sigma,n(q; c_sel) = emptyset,
sigma_chk,n(q; c_sel)(z) = 0      for all z in D_sigma,n(q; c_sel),
Delta_rep^pt,n(q; c_sel)(z) = 0   for all z in D_sigma,n(q; c_sel),
Rep_U,n(q; c_sel)                 on every exact admissible patch.
```

Relevant exact domain:

```text
D_sigma,n(q; c_sel)
  := { z in A_adm^th,n(q) ∩ ker(C_center,n(q)) :
       (c_sel + z, c_sel) in Pair_chk,n(q) }.
```

Outside scope for `T3u`:

- not full `T3`;
- not final physical criticality;
- not a collapse to `B_red` / `B_mix`;
- not a reopening of the frozen local branch;
- not a new numerical campaign.

## Exact scalar-image setting

On the exact domain `D_sigma,n(q; c_sel)`, the chart-invariant pointwise defect
map from `T3s` / `T3t`

```text
Delta_rep^pt,n(q; c_sel) : D_sigma,n(q; c_sel) -> span(e_mem)
```

has the exact scalar form

```text
Delta_rep^pt,n(q; c_sel)(z) = sigma_chk,n(q; c_sel)(z) e_mem.
```

So the scalar selector is defined exactly when `z in D_sigma,n(q; c_sel)`;
that is, exactly when the pair `(c_sel + z, c_sel)` belongs to the admissible
checked-local pair domain and can therefore be represented in some corrected
local chart. Its chart-invariance follows because `Delta_rep^pt` is already a
global chart-invariant map and the membrane basis vector `e_mem` is fixed under
the quotient-preserving chart changes.

The exact scalar image and exact defect set are therefore

```text
Sigma_sigma,n(q; c_sel)
  := { sigma_chk,n(q; c_sel)(z) : z in D_sigma,n(q; c_sel) },

N_sigma,n(q; c_sel)
  := sigma_chk,n(q; c_sel)^(-1)(R \ {0}).
```

The new sharper object for `T3u` is the exact pairwise scalar-difference image

```text
Omega_sigma,n(q; c_sel)
  := { sigma_chk,n(q; c_sel)(z_1) - sigma_chk,n(q; c_sel)(z_2) :
       z_1, z_2 in D_sigma,n(q; c_sel),
       (c_sel + z_1, c_sel + z_2) in Pair_chk,n(q) }.
```

Because `z = 0` belongs to `D_sigma,n(q; c_sel)`, one has `sigma_chk(0) = 0`.
Hence

```text
Sigma_sigma,n(q; c_sel) = {0}
iff
Omega_sigma,n(q; c_sel) = {0}.
```

The forward implication is immediate. For the reverse implication, every
`z in D_sigma,n(q; c_sel)` satisfies `(c_sel + z, c_sel) in Pair_chk,n(q)` by
definition, so

```text
sigma_chk(z) - sigma_chk(0) in Omega_sigma;
```

if `Omega_sigma = {0}`, then `sigma_chk(z) = 0` for all `z`, hence
`Sigma_sigma = {0}`.

This is the cleanest current exact formulation because every surviving
representative-sensitive difference already factors through scalar differences,
so the remaining theorem is no longer about a higher-dimensional chart object,
but about collapse or noncollapse of one exact scalar image, equivalently
vanishing or nonvanishing of one exact scalar-difference image.

## Attack on scalar-image collapse

### Theorem `T3u`

Fix clean `(n, q)` and `c_sel in A_sel^repo,n(q)`.

1. The current theorem-facing admissibility / candidate package implies

   ```text
   0 in Sigma_sigma,n(q; c_sel),
   0 in Omega_sigma,n(q; c_sel),
   N_sigma,n(q; c_sel) = sigma_chk^(-1)(R \ {0}),
   Delta_rep^pt = sigma_chk e_mem.
   ```

2. The cocycle / antisymmetry / normalization package descends exactly to the
   scalar-difference image:

   ```text
   Omega_sigma,n(q; c_sel) = - Omega_sigma,n(q; c_sel),
   ```

   and whenever the three exact admissible pairs are defined,

   ```text
   (sigma_chk(z_1) - sigma_chk(z_2))
 + (sigma_chk(z_2) - sigma_chk(z_3))
   = sigma_chk(z_1) - sigma_chk(z_3).
   ```

3. All exact pairwise representative-sensitive differences factor through
   `Omega_sigma,n(q; c_sel)`:

   ```text
   Delta_rep,chk,n(q; c_sel + z_1, c_sel + z_2)
     = (sigma_chk,n(q; c_sel)(z_1) - sigma_chk,n(q; c_sel)(z_2)) e_mem.
   ```

4. Therefore `T3u` closes if and only if

   ```text
   Omega_sigma,n(q; c_sel) = {0},
   ```

   equivalently if and only if

   ```text
   Sigma_sigma,n(q; c_sel) = {0}.
   ```

5. Current theorem-facing admissibility / candidate constraints still do not
   force `Omega_sigma,n(q; c_sel) = {0}` and therefore do not force
   `Sigma_sigma,n(q; c_sel) = {0}`. They force only the scalar cocycle package,
   the basepoint normalization, and codomain containment in the membrane line.

So the strongest honest `T3u` endpoint is again an exact obstruction theorem:
scalar-image collapse is now reduced further to vanishing of one exact pairwise
scalar-difference image, but current theorem-facing structure still does not
force that vanishing.

## Reduction of the proof routes

After `T3u`, the strongest plausible proof routes all reduce to the same exact
scalar-difference obstruction.

1. Direct scalar-collapse route:
   prove `sigma_chk,n(q; c_sel)(z) = 0` for every `z in D_sigma`.
2. Defect-set route:
   prove `N_sigma,n(q; c_sel) = emptyset` directly.
3. Pairwise-difference route:
   prove `Omega_sigma,n(q; c_sel) = {0}` on the full exact admissible pair
   domain.
4. Admissibility route:
   prove that any nonzero scalar value would violate the current exact
   admissibility / candidate / compatibility constraints.
5. Reduction route:
   because `sigma_chk(0) = 0` and every exact point pairs with the basepoint,
   it is enough to kill the exact scalar differences against the repo-selected
   basepoint, equivalently to kill the whole pairwise-difference image.
6. Obstruction route:
   isolate the exact surviving degree of freedom as one nonzero element of
   `Omega_sigma`, equivalently one nonzero element of `Sigma_sigma`.
7. Nonzero-scalar-template route:
   if `T3u` cannot be proved, characterize a point `z_* in D_sigma` with
   `Delta_rep^pt(z_*) = delta_* e_mem`, `delta_* != 0`, equivalently one exact
   nonzero scalar value in `Sigma_sigma` and one exact nonzero scalar
   difference against the basepoint.

No further reduction to a smaller exact class of basepoints, patches, or
residuals is currently justified.

## Comparison with the earlier routes

The present scalar-image formulation is the cleanest current bottleneck
statement for the following reasons.

1. Raw same-trace shadows were too collapsed:
   they already lost the surviving representative-sensitive scalar datum along
   the membrane line.
2. The pairwise route from `T3l` was necessary:
   it recovered the surviving representative-sensitive difference before
   quotient collapse.
3. The cocycle route from `T3m` was necessary but insufficient:
   antisymmetry, additivity, and normalization alone do not force the scalar
   difference image to vanish.
4. The singletonity / constancy / `Rep_U` / pointwise-vanishing routes from
   `T3p` / `T3r` / `T3s` are not stronger after `T3t`; they already reduce to
   `Sigma_sigma = {0}`.
5. The gain in `T3u` is sharper obstruction wording:
   scalar-image collapse is now seen to be exactly equivalent to vanishing of
   the pairwise scalar-difference image `Omega_sigma` on the exact admissible
   pair domain.

So the scalar-image formulation is not stronger than the earlier packages as a
truth condition, but it is strictly sharper as the current obstruction package
because it isolates the exact scalar-difference object naturally controlled by
the cocycle theorem.

## Minimal `T3u` lemma split

### `T3u-L1`. Exact scalar-image / defect-set / pairwise-difference lemma

Statement:

For fixed clean `(n, q)` and repo-selected basepoint `c_sel`, the exact scalar
selector

```text
sigma_chk,n(q; c_sel) : D_sigma,n(q; c_sel) -> R
```

determines the exact scalar image `Sigma_sigma`, the exact defect set
`N_sigma`, and the exact pairwise scalar-difference image `Omega_sigma`.
Moreover,

```text
Sigma_sigma = {0}
iff
N_sigma = emptyset
iff
Omega_sigma = {0}.
```

Status:
- closed enough.

Verification method:
- manual derivation;
- CAS;
- code inspection.

### `T3u-L2`. Scalar-image collapse vs selector-vanishing lemma

Statement:

On the exact domain `D_sigma,n(q; c_sel)`, the following are equivalent:

```text
Sigma_sigma,n(q; c_sel) = {0};
N_sigma,n(q; c_sel) = emptyset;
sigma_chk,n(q; c_sel)(z) = 0       for all z in D_sigma;
Delta_rep^pt,n(q; c_sel)(z) = 0    for all z in D_sigma;
Rep_U,n(q; c_sel)                  on every exact patch.
```

Status:
- closed enough.

Verification method:
- manual derivation;
- CAS;
- code inspection.

### `T3u-L3`. Exact scalar-difference / cocycle package lemma

Statement:

The exact pairwise scalar-difference image satisfies

```text
0 in Omega_sigma,
Omega_sigma = -Omega_sigma,
```

and, wherever the three exact admissible pairs are defined,

```text
delta_12 + delta_23 = delta_13.
```

Status:
- closed enough.

Verification method:
- theorem reuse from `T3m` / `T3t`;
- manual derivation;
- code inspection.

### `T3u-L4`. Exact obstruction / nonzero-scalar-template lemma

Statement:

Failure of `T3u` is exactly equivalent to any of the following exact forms:

```text
Sigma_sigma,n(q; c_sel) != {0},
N_sigma,n(q; c_sel) != emptyset,
Omega_sigma,n(q; c_sel) != {0}.
```

Equivalently, there exists one point `z_* in D_sigma,n(q; c_sel)` such that

```text
sigma_chk,n(q; c_sel)(z_*) = delta_* != 0,
Delta_rep^pt,n(q; c_sel)(z_*) = delta_* e_mem.
```

Status:
- closed enough as an exact obstruction/template theorem;
- explicit admissible realization still open.

Verification method:
- manual derivation;
- theorem reuse from `T3t`;
- code inspection.

### `T3u-L5`. Exact consequence lemma for the next bridge step

Statement:

If one proves

```text
Omega_sigma,n(q; c_sel) = {0}
```

for every fixed clean `(n, q)` and repo-selected basepoint `c_sel`, then
`Sigma_sigma,n(q; c_sel) = {0}`, `N_sigma,n(q; c_sel) = emptyset`,
`Delta_rep^pt = 0` on `D_sigma`, `sigma_chk` vanishes on the full exact domain,
`Rep_U` holds on every exact patch, and the remaining membrane obstruction in
the reverse-inclusion / zero-excess bridge disappears on the current theorem-
facing boundary.

Status:
- closed enough as a theorem-program consequence.

Verification method:
- manual derivation;
- Lean target after the scalar map / scalar-difference-image abstraction is
  packaged.

## Single next bottleneck after `T3u`

The single next bottleneck is now:

```text
prove or refute that
Omega_sigma,n(q; c_sel) = {0}
on the full exact admissible pair domain,
equivalently prove or refute that
Sigma_sigma,n(q; c_sel) = {0}.
```

This is sharper than `T3t`:
the remaining gap is no longer phrased only as collapse of one scalar image, but
as vanishing of the exact pairwise scalar-difference image that already governs
all surviving representative-sensitive pairwise differences.

## Lean / CAS / manual split for `T3u`

Lean:
- finite-dimensional exact-domain / scalar map / scalar-image / defect-set /
  pairwise scalar-difference templates after abstracting `sigma_chk`,
  `Sigma_sigma`, `N_sigma`, and `Omega_sigma`.

CAS / code inspection:
- `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, chart-change identities, `Delta_rep^pt = sigma_chk e_mem`,
  the pairwise factorization
  `Delta_rep,chk = (sigma_chk(z_1) - sigma_chk(z_2)) e_mem`, and the scalar-
  image / scalar-difference formulas.

Manual derivation:
- exact theorem scope for `T3u`;
- why scalar-image collapse is equivalent to vanishing of the exact pairwise
  scalar-difference image;
- why current theorem-facing constraints still do not force that vanishing;
- why the exact surviving obstruction is one nonzero scalar difference;
- relation of `T3u` to the future reverse-inclusion / zero-excess bridge below
  full `T3`.

## Conservative status after `T3u`

Closed enough now:

- the exact chart-invariant scalar selector
  `sigma_chk,n(q; c_sel) : D_sigma,n(q; c_sel) -> R`;
- the exact scalar image `Sigma_sigma`, the exact defect set `N_sigma`, and the
  exact pairwise scalar-difference image `Omega_sigma`;
- the equivalence between scalar-image collapse, defect-set emptiness,
  selector-vanishing, pointwise-defect vanishing, and pairwise scalar-
  difference-image vanishing;
- the exact scalar cocycle package on `Omega_sigma`:
  normalization at `0`, antisymmetry, and additivity where the exact pairs are
  defined;
- the obstruction theorem that current theorem-facing constraints still force
  only the scalar cocycle package plus basepoint normalization, not
  `Omega_sigma = {0}`.

Still open:

- whether `Omega_sigma,n(q; c_sel) = {0}` on the full exact admissible pair
  domain;
- equivalently whether `Sigma_sigma,n(q; c_sel) = {0}` on the full exact
  domain;
- whether an explicit admissible point `z_*` with
  `sigma_chk,n(q; c_sel)(z_*) != 0` can be realized;
- whether a representative-sensitive theorem kills every exact pairwise scalar
  difference on the checked-local admissible pair domain.

So the gap is sharper than after `T3t`:
the remaining question is no longer only whether the scalar image collapses, but
exactly whether the exact pairwise scalar-difference image vanishes on the full
admissible exact pair domain.