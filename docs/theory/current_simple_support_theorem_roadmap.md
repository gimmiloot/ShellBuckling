# Current Theorem Roadmap For Clean Full `simple support / подвижный шарнир`

This note records the current theorem program above the frozen local
Outcome-B boundary. It starts from the current criterion bridge note and does
not reopen the same checked local branch.

## A. Goal

The long-term theorem target is not “find a minimum” and not “promote a raw
boundary dip.” The target is to prove that criticality on the clean full
`simple support / подвижный шарнир` path must be read through the correct
selected reduced object, with `L_red` as the present theorem-facing anchor.

Operational candidate rankings may still use descendants and diagnostics, but
the final theorem program should pass through the selected reduced family and
the nontrivial-kernel question for `L_red`.

## B. What Is Already Closed Enough To Use

- `A_ls` is best read as the global weak/KKT-selected family on the live clean
  reduced path.
- `L_red` is the main theorem-facing reduced object:
  `L_red,n(q) = [A_int,n(q); B_full,n(q)] V_adm,n(q)`.
- `B_red` and `B_mix` are descendants / coordinate presentations on that
  selected reduced family, not independent theorem-level replacements.
- The selected leading trace plane is closed:
  `J_0 = C_center`, `J_0(A_ls) = im(D_amp)`.
- On the current checked higher-order local boundary, the strongest local
  theorem-facing object closes only as the quotient
  `im(D_rich,eta^corr) / span(g_mem)`.

These blocks are enough to organize the next theorem program, even though they
do not yet close final physical criticality.

## C. Main Theorem Program

### `T1`. Global selected-family theorem

Statement:
- identify the clean reduced family as the current global weak/KKT-selected
  family `A_ls`.

Status:
- closed enough on the present repo/ansatz boundary.

### `T2`. Reduced-operator theorem

Statement:
- use `L_red` as the main reduced theorem-facing object and retain
  `B_red`, `B_mix` only as descendants on the same selected family.

Status:
- closed enough on the present reduced-family boundary.

### `T3`. Global selected-kernel bridge theorem for `L_red`

Statement:
- for fixed clean `(n, q)`, let
  `L_full,n(q) = [A_int,n(q); B_full,n(q)]`,
  let the current selected reduced family be
  `A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q))`
  on the current weighted-ansatz boundary, and let
  `L_red,n(q) = L_full,n(q) V_adm,n(q)`;
- then selected-class criticality on the current repository boundary should be
  read through the exact nontrivial-kernel question
  `exists 0 != c in A_sel^repo,n(q) : L_full,n(q) c = 0`
  if and only if
  `exists 0 != a in R^2 : L_red,n(q) a = 0`;
- this is a repository-level selected-class theorem target, not yet a final
  physical shell theorem and not a theorem collapsing the problem to
  `B_red` / `B_mix` alone.

Status:
- open target;
- central theorem-facing bottleneck.

### `T4`. Local quotient compatibility theorem

Statement:
- show that the checked local quotient result is compatible with the global
  selected-family reading and does not force reopening the same checked local
  branch before `T3`.

Status:
- closed enough on the current checked local boundary;
- not an all-orders local theorem.

### `T5`. Mode-wise critical-load theorem after bridge closure

Statement:
- once `T3` is in place, formulate the mode-wise critical-load theorem on the
  clean path and only then upgrade candidate competition language beyond the
  current operational level.

Status:
- open downstream target.

## D. Supporting Lemmas Already Effectively Available

- selected section / KKT-family meaning for `A_ls`;
- reduced descendant relation
  `B_red = B_full V_adm`, `B_mix = B_red G_amp`;
- selected leading-trace plane
  `J_0(A_ls) = im(D_amp)`;
- richer-trace reconciliation for the checked local branch;
- local quotient result on the checked higher-order boundary.

These are not the final theorem, but they already form the support layer for a
`T3`-oriented bridge program.

## E. Main Open Gap

The main open gap is the global selected-kernel bridge theorem for `L_red`.

This is now the central theorem-facing bottleneck because:

- the selected family is already sharp enough to use;
- the local checked branch already has a conservative stopping point at Outcome
  B;
- `B_red` and `B_mix` are already understood as descendants only;
- but the bridge from that selected reduced story to the theorem-facing kernel
  reading of `L_red` is still not closed.

Until `T3` is addressed, the project should not pretend that a boundary-only
degeneration theorem or final physical criticality theorem is already available.

## F. Stop Rule / Strategy

- The local theorem-facing branch stays frozen for now at Outcome B.
- This roadmap does not reopen the same checked local branch.
- The next theorem-facing implementation should start with a dedicated
  `T3` stage:
  `global selected-kernel bridge theorem for L_red`.
- Only after that bridge work should the project decide whether a stronger
  local theorem or a mode-wise critical-load theorem is worth opening next.

## G. Current `T3` Implementation Split

### `T3-L1`. Selected-family lemma

Statement:
- on the current weighted-ansatz repository boundary, the selected/admissible
  class used by the clean reduced architecture is
  `A_sel^repo = A_ls = im(V_adm) = im(M_amp)`.

Status:
- closed enough on the current repo/ansatz boundary.

Verification route:
- code inspection, manual derivation, CAS, representative live checks.

### `T3-L2`. Reduced-object lemma

Statement:
- the exact reduced object on that selected class is
  `L_red = [A_int; B_full] V_adm`,
  with descendants
  `B_red = B_full V_adm`,
  `B_mix = B_red G_amp`.

Status:
- closed enough on the current reduced-family boundary.

Verification route:
- code inspection, manual derivation, CAS.

### `T3-L3`. Restricted-kernel bridge lemma

Statement:
- the map `a -> c = V_adm a` identifies `ker(L_red)` exactly with
  `A_sel^repo ∩ ker(L_full)`.

Status:
- closed enough at the finite-dimensional restricted-family level.

Verification route:
- manual derivation, CAS, Lean abstraction target.

### `T3-L4`. Local-compatibility lemma

Statement:
- the checked local quotient result is a compatibility constraint on how the
  selected class may be read locally; it does not replace the global theorem
  and does not reopen the same checked local branch.

Status:
- closed enough on the current checked local boundary.

Verification route:
- manual derivation, CAS, structural pilot-23 checks.

### `T3-L5`. Boundary-descendant caution lemma

Statement:
- `B_red` and `B_mix` are descendants on the same selected family and remain
  operationally useful, but they do not yet replace the full stacked
  nontrivial-kernel question for `L_red`.

Status:
- closed enough as a theorem-facing caution layer.

Verification route:
- manual derivation, CAS, code inspection.

### Main remaining gap inside `T3`

- package `T3-L1`--`T3-L5` as one clean selected-class bridge theorem whose
  scope is explicit:
  current repository selected class, current reduced object, no silent collapse
  to a boundary-only criterion, and no promotion to a final physical shell
  theorem.

### Next implementable proof step

- open a dedicated `T3` proof stage centered on `T3-L3`:
  formalize the finite-dimensional selected-kernel bridge
  `exists 0 != a : L_red a = 0  <->  exists 0 != c in A_sel^repo : L_full c = 0`
  with `A_sel^repo = im(V_adm)`,
  while recording `T3-L1`, `T3-L2`, `T3-L4`, and `T3-L5` as the shell-specific
  premises/support layer.

### Lean / CAS split for `T3`

- Lean:
  the finite-dimensional abstract bridge
  `L_red = L_full V`, bijectivity of `a -> V a` onto the selected class,
  and basis-independence on that class.
- CAS / code inspection:
  the live clean identities
  `A_sel^repo = A_ls = im(V_adm) = im(M_amp)`,
  `L_red = [A_int; B_full] V_adm`,
  `B_red = B_full V_adm`,
  `B_mix = B_red G_amp`,
  plus the checked local quotient compatibility.
- Manual derivation:
  theorem scope, exact selected-class wording, and the caution that this is not
  yet a final physical criticality theorem.
