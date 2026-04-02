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
