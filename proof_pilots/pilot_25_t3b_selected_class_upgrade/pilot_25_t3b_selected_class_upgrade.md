# Pilot 25: T3b Candidate Class, T3c Comparison Boundary, T3d Representative-Law Stage, T3e Fiber-Excess Criterion, T3f Zero-Excess Obstruction, T3g Residual-Class Lift Boundary, T3h Membrane-Kernel Global-Lift Boundary, T3i Projected-Lift Injectivity Boundary, and T3j Checked-Local Coefficient-Extraction Boundary For Clean `simple support / подвижный шарнир`

## Goal

This note now records nine consecutive theorem-facing steps above the already
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
- “same-trace” means exactly `J_0(c_sel + z) = J_0(c_sel)`, equivalently
  `J_0(z) = 0`, equivalently `z in ker(C_center,n(q))`;
- “quotient-invisible” means exactly equality of checked local quotient shadows
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
“prove `Delta_H = 0`”. It is:

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

So the bottleneck is now sharper than in `T3h`: not merely “decide the kernel”,
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

So `T3j` sharpens the obstruction from “missing `chi_chk`” to:

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

