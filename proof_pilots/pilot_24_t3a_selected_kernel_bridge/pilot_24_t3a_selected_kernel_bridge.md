# Pilot 24: T3a Finite-Dimensional Selected-Kernel Bridge For Clean `simple support / подвижный шарнир`

## Goal

This note isolates and packages the first implementable theorem-facing step
above the frozen local Outcome-B boundary:

`T3a` = the finite-dimensional selected-kernel bridge on the current
repository-selected family.

It is a packaging/statement pilot only. It does not change equations,
boundary-condition meaning, solver behavior, or the active clean standalone
search path.

## Exact `T3a` theorem target

Fix a clean mode/load pair `(n, q)` on the current weighted-ansatz repository
boundary. Define

```text
L_full,n(q) = [A_int,n(q); B_full,n(q)],
A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q)),
L_red,n(q) = L_full,n(q) V_adm,n(q).
```

Then the exact `T3a` statement is:

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

`Phi_n,q` is a linear bijection carrying `ker(L_red,n(q))` exactly onto

```text
A_sel^repo,n(q) intersect ker(L_full,n(q)).
```

## Exact scope and exact non-claims

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

## Packaged lemma split

### `T3a-L1`. Selected-family identity

Statement:

```text
A_sel^repo = A_ls = im(V_adm) = im(M_amp)
```

on the current weighted-ansatz repository boundary.

Status:
- already effectively closed on the current repository boundary;
- packaged here as an explicit theorem premise.

Main support:
- `docs/theory/vyvod_uravneniy_updated17.md` sections `1.9`, `1.10.8`-`1.10.10`;
- `docs/theory/current_simple_support_theorem_roadmap.md`;
- `docs/theory/current_theory_verification_map.md` entries `V-S8`, `V-F3`, `V-S19`;
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
- already effectively closed on the current selected-family boundary;
- packaged here as the exact operator identity used by `T3a-L4`.

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
- already effectively closed at the finite-dimensional selected-family level;
- packaged here as the exact bridge map.

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
ker(L_red)  <->  A_sel^repo intersect ker(L_full)
```

through the bijection from `T3a-L3`.

Status:
- already effectively closed at the finite-dimensional selected-family level;
- packaged here as the exact bridge conclusion.

Main support:
- `docs/theory/vyvod_uravneniy_updated17.md` section `1.8`;
- `docs/theory/current_theory_verification_map.md` entries `V-S7`, `V-S19`;
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
- already effectively closed as a theorem-facing caution layer;
- packaged here as an explicit non-claim.

Main support:
- `docs/theory/current_simple_support_criterion_bridge_note.md`;
- `docs/theory/current_simple_support_theorem_roadmap.md`;
- `docs/theory/current_theory_verification_map.md` entry `V-S19`;
- `docs/journal/project_journal_updated14.md` sections `12.20`-`12.21`.

Proof method:
- manual derivation;
- code inspection;
- CAS for the descendant identities.

## Verification ledger for the shell-specific ingredients

### Exact algebra and exact finite-dimensional identities

The following exact algebraic identities are already effectively closed at the
current repository-selected boundary and are checked by
`reduction_check.py`:

- `stacked_restriction_identity = true`;
- `basis_change_stacked_identity = true`;
- `basis_change_boundary_identity = true`;
- `bred_bmix_coordinate_identity = true`;
- `leading_center_block_det_minus_one = true`;
- `leading_regularity_rank_two = true`;
- `leading_regularity_nullspace_two_parameter = true`;
- `leading_regular_parameterization_identity = true`.

This is the exact algebra support for:

- `L_red = L_full V_adm`;
- `B_red = B_full V_adm`;
- `B_mix = B_red G_amp`;
- the two-parameter selected-family parameterization;
- basis-independence on the current selected family.

### Representative live clean checks for the same identities

The same helper checks representative clean sample points
`(n, q_MPa) = (4, 11.1), (6, 17.6), (7, 17.3), (8, 17.8)` and reports:

- `rank_V_adm = 2` and `rank_V_kkt = 2` at all sampled points;
- `det_G_amp > 0` at all sampled points;
- `max_center_full_residual_canon` between about `1.3e-10` and `3.3e-09`;
- `max_center_full_residual_kkt` between about `1.5e-09` and `1.3e-08`;
- `max_vadm_minus_vkkt` between about `2.6e-06` and `6.1e-06`;
- `max_kkt_full_residual` between about `8.1e-10` and `3.7e-09`;
- `max_kkt_boundary_residual` between about `2.8e-11` and `2.8e-10`;
- `max_bmix_reconstruction_residual` between about `8.5e-17` and `3.3e-16`.

These are representative live confirmations only. They do not replace the exact
finite-dimensional identities above.

### Representative live checks for the selected-family reading

`selection_object_check.py` supplies the current shell-specific reading of the
selected class on the same representative clean points:

- the weighted trial space has dimension `48`, while the fixed-center amplitude
  fiber has dimension `44`;
- `A_ls` is the unique `H = A_int^T A_int + reg I`-minimal KKT-selected family
  inside that fiber;
- `max_amplitude_slice_from_lift_residual = 0.0` at all sampled points;
- `max_selected_regularity_residual` stays small, about `1.5e-09`, `4.3e-11`,
  `1.5e-11`, `9.7e-11` on the sampled points;
- `reference_to_selected_objective_ratio` is very large, from about `1.7e6`
  up to about `1.7e11`.

So the live repository-selected reading

```text
A_sel^repo = A_ls = im(V_adm) = im(M_amp)
```

is not just a raw center-regular parameterization. It is the current global
weak/KKT-selected family on the weighted-ansatz boundary.

### Outcome-B compatibility support layer

The checked local Outcome-B quotient result is not part of the proof of the
finite-dimensional bijection itself. Its role here is narrower:

- it is a compatibility constraint on how the selected class should be read
  locally;
- it supports the caution that `T3a` must not be overpromoted into a stronger
  continuum/local theorem;
- it does not replace `T3a`, and it does not reopen the same checked local
  branch.

## What was already available versus what is packaged here

Already available in substance before this note:

- the selected-family identity on the current repository boundary;
- the reduced-object identity `L_red = L_full V_adm`;
- the finite-dimensional bijection `R^2 <-> A_sel^repo`;
- the exact kernel transfer on that class;
- the descendant caution for `B_red` and `B_mix`.

What this note packages explicitly:

- the exact theorem now named `T3a`;
- the precise scope and exact non-claims;
- the explicit lemma split `T3a-L1`--`T3a-L5`;
- the exact separation between exact algebra, representative live checks, and
  broader open questions;
- the explicit Lean-facing abstraction target.

So the substantive mathematical gap inside `T3a` is not a new shell-specific
identity. The packaging task is now closed enough on the current repository
boundary.

## Concrete implementation artifact

Chosen artifact:

- this dedicated proof-pilot note under
  `proof_pilots/pilot_24_t3a_selected_kernel_bridge/`.

No new helper script is required for this stage because the live shell-specific
identities already have direct support in:

- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/reduction_check.py`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`;
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`.

## Lean-facing abstraction target

Lean should formalize only the finite-dimensional abstract bridge, not the full
shell-specific derivation.

Target statement:

```text
Let V : R^2 -> X be linear and injective, let
A_sel := im(V), let L_full : X -> Y be linear, and let
L_red := L_full o V.
Then V restricts to a linear bijection
ker(L_red) <-> A_sel intersect ker(L_full).
Equivalently,
exists 0 != a in R^2 : L_red a = 0
iff
exists 0 != c in A_sel : L_full c = 0.
```

Minimal formal skeleton to aim for next:

```lean
-- Abstract target only; not implemented in this turn.
theorem selected_kernel_bridge
  (V : (Fin 2 -> R) -> X)
  (L_full : X -> Y)
  (h_inj : Function.Injective V)
  (h_red : L_red = L_full ∘ V)
  (A_sel : Set X)
  (h_sel : A_sel = Set.range V) :
  (∃ a, a ≠ 0 ∧ L_red a = 0) ↔
  (∃ c, c ∈ A_sel ∧ c ≠ 0 ∧ L_full c = 0)
```

The shell-specific equalities
`A_sel^repo = A_ls = im(V_adm) = im(M_amp)` and
`L_red = [A_int; B_full] V_adm`
stay outside Lean and belong to CAS/code-inspection support.

## Final `T3a` status

Verdict:

`T3a packaged and closed enough on the current repo boundary`.

Meaning of this verdict:

- the finite-dimensional selected-kernel bridge statement is now explicit;
- the needed shell-specific premises/supporting lemmas are explicitly packaged;
- the exact algebra and the representative live clean checks are separated;
- the broader long-term `T3` remains open beyond this repository-selected
  boundary.

## What remains open beyond `T3a`

Even after this packaging, the following stay open:

- whether the current selected repository class already equals the full exact
  continuum/theorem-facing admissible clean tangent space;
- whether a stronger theorem can replace `L_red` by a boundary-only object;
- how the frozen local Outcome-B quotient theorem should ultimately connect to a
  broader theorem-facing selected-family statement beyond the current checked
  repository boundary;
- any final physical critical-load theorem for clean `simple support /
  подвижный шарнир`.
