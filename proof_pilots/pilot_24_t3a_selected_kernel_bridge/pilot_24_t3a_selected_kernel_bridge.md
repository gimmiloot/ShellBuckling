# Pilot 24: T3a Finite-Dimensional Selected-Kernel Bridge For Clean `simple support / подвижный шарнир`

## Goal

This note isolates the first implementable theorem-facing step above the frozen
local Outcome-B boundary:

`T3a` = the finite-dimensional selected-kernel bridge on the current
repository-selected family.

It is a packaging/statement pilot. It does not change equations, boundary-
condition meaning, solver behavior, or the active clean standalone search path.

## Exact `T3a` theorem target

Fix a clean mode/load pair `(n, q)` on the current weighted-ansatz repository
boundary. Define

```text
L_full,n(q) = [A_int,n(q); B_full,n(q)],
A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q)),
L_red,n(q) = L_full,n(q) V_adm,n(q).
```

Then the exact `T3a` target is:

```text
exists 0 != a in R^2 : L_red,n(q) a = 0
iff
exists 0 != c in A_sel^repo,n(q) : L_full,n(q) c = 0.
```

Equivalently, with

```text
Phi_n,q : R^2 -> A_sel^repo,n(q),
Phi_n,q(a) = V_adm,n(q) a,
```

the map `Phi_n,q` is a linear bijection carrying `ker(L_red,n(q))` exactly onto

```text
A_sel^repo,n(q) ∩ ker(L_full,n(q)).
```

## Exact scope

`T3a` is deliberately narrower than the long-term `T3`.

What `T3a` does claim:

- a finite-dimensional selected-family bridge theorem on the current
  repository-selected class;
- the selected class is exactly
  `A_sel^repo = A_ls = im(V_adm) = im(M_amp)` on the current weighted-ansatz
  boundary;
- the theorem is about kernel equivalence between `L_red` and the restriction
  of `L_full` to that selected class.

What `T3a` does not claim:

- it is not yet the full long-term `T3`;
- it is not a theorem that `A_sel^repo` already equals the full exact
  continuum/theorem-facing admissible clean tangent space;
- it is not a theorem collapsing the problem to `B_red` or `B_mix`;
- it is not a final physical shell criticality theorem.

## Minimal lemma split

### `T3a-L1`. Selected-family identity

Statement:

```text
A_sel^repo = A_ls = im(V_adm) = im(M_amp)
```

on the current weighted-ansatz repository boundary.

Status:
- already effectively closed.

Main support:
- `docs/theory/vyvod_uravneniy_updated17.md` sections `1.9`, `1.10.8`-`1.10.10`;
- `docs/theory/current_simple_support_theorem_roadmap.md`;
- `docs/theory/current_theory_verification_map.md` entries `V-S8`, `V-F3`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/reduction_check.py`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`.

Proof method:
- code inspection;
- CAS;
- manual derivation;
- representative live clean checks.

### `T3a-L2`. Reduced-object identity

Statement:

```text
L_red = L_full V_adm,
L_full = [A_int; B_full],
```

with descendants

```text
B_red = B_full V_adm,
B_mix = B_red G_amp.
```

Status:
- already effectively closed.

Main support:
- `docs/theory/vyvod_uravneniy_updated17.md` sections `1.7`-`1.8`;
- `docs/theory/current_simple_support_criterion_bridge_note.md`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/reduction_check.py`;
- `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`.

Proof method:
- code inspection;
- CAS;
- manual derivation.

### `T3a-L3`. Bijection lemma

Statement:

```text
a -> c = V_adm a
```

is a linear bijection from `R^2` onto `A_sel^repo`.

Status:
- already effectively closed at the finite-dimensional selected-family level.

Main support:
- `docs/theory/vyvod_uravneniy_updated17.md` section `1.8`;
- `docs/theory/current_theory_verification_map.md` entry `V-S7`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/reduction_check.py`.

Proof method:
- manual derivation;
- CAS;
- Lean abstraction target.

### `T3a-L4`. Kernel-transfer lemma

Statement:

```text
L_red a = 0
iff
L_full(V_adm a) = 0,
```

hence

```text
ker(L_red)  <->  A_sel^repo ∩ ker(L_full)
```

through the bijection from `T3a-L3`.

Status:
- already effectively closed at the finite-dimensional selected-family level.

Main support:
- `docs/theory/vyvod_uravneniy_updated17.md` section `1.8`;
- `docs/theory/current_theory_verification_map.md` entry `V-S7`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/reduction_check.py`.

Proof method:
- manual derivation;
- CAS;
- Lean abstraction target.

### `T3a-L5`. Descendant caution lemma

Statement:

`T3a` does not collapse to `B_red` or `B_mix`. These remain descendants on the
same selected family and diagnostic/companion objects only.

Status:
- already effectively closed as a theorem-facing caution layer.

Main support:
- `docs/theory/current_simple_support_criterion_bridge_note.md`;
- `docs/theory/current_simple_support_theorem_roadmap.md`;
- `docs/theory/current_theory_verification_map.md` entry `V-S19`;
- `docs/journal/project_journal_updated14.md` sections `12.20`-`12.21`.

Proof method:
- manual derivation;
- code inspection;
- CAS for the descendant identities.

## What is already proved versus what still needs packaging

Already available in substance:

- the exact current selected-family identity on the repository boundary;
- the exact reduced-object identity `L_red = L_full V_adm`;
- the exact finite-dimensional bijection `R^2 <-> A_sel^repo`;
- the exact restricted-kernel transfer on that class;
- the quotient-aware local caution and the descendant caution for `B_red` /
  `B_mix`.

Still missing before `T3a` can be cited cleanly as one theorem:

- one isolated theorem statement that names the object as `T3a` rather than
  leaving it spread across `C3`, `T3`, and bridge-note language;
- one proof-pilot artifact that explicitly packages `T3a-L1`--`T3a-L5` as the
  premises/support layer for the finite-dimensional bridge;
- one explicit reminder that `T3a` is not yet full `T3`, not yet continuum
  losslessness, and not yet a final physical theorem.

So the main gap here is proof packaging and scope control, not a new numerical
campaign and not a new local-branch extension.

## Concrete implementation artifact

Chosen artifact:

- this dedicated proof-pilot note under
  `proof_pilots/pilot_24_t3a_selected_kernel_bridge/`.

No new helper script is required at this stage because the live shell-specific
identities already have direct support in:

- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/reduction_check.py`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`.

## Lean / CAS / manual split

Lean:

- the finite-dimensional abstraction
  `L_red = L_full V`;
- bijectivity of `a -> V a` onto the selected class;
- kernel equivalence under that bijection.

CAS / code inspection:

- `A_sel^repo = A_ls = im(V_adm) = im(M_amp)`;
- `L_red = [A_int; B_full] V_adm`;
- `B_red = B_full V_adm`;
- `B_mix = B_red G_amp`;
- the local Outcome-B compatibility/caution layer as an already checked
  constraint, not as a replacement theorem.

Manual derivation:

- the exact theorem wording and scope of `T3a`;
- the distinction `T3a` versus full `T3`;
- the caution that `T3a` is not yet a final physical criticality theorem and
  does not promote `B_red` / `B_mix` into theorem-level substitutes.

## What remains open beyond `T3a`

Even after clean `T3a` packaging, the following stay open:

- whether the current selected repository class already equals the full exact
  continuum/theorem-facing admissible clean tangent space;
- whether a stronger theorem can replace `L_red` by a boundary-only object;
- how the frozen local Outcome-B quotient theorem should ultimately connect to a
  broader theorem-facing selected-family statement beyond the current checked
  repository boundary;
- any final physical critical-load theorem for clean `simple support /
  подвижный шарнир`.
