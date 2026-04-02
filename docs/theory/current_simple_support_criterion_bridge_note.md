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
- No intrinsic higher-order local selector has been identified beyond the
  checked quotient boundary.
- No final physical candidate load/mode is determined here.

## How To Read The Objects

### `A_ls`

Theorem-facing role:
- the current selected reduced family;
- the global weak/KKT-selected family, not the raw unrestricted local
  center-regular family.

Operational role:
- the family actually used by the live clean reduced search and by the current
  reduced-coordinate objects.

Do not read it as:
- the whole raw local regular family;
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

Current clean competition language:
- `n=6`: leading supported candidate near `17.6 MPa`
- `n=8`: main unstable rival near `17.8 MPa`
- `n=7`: sharp raw reserve dip
- `n=4`: weak control mode

Current first-practical `R2` language:
- the stacked selected-family diagnostic `rho_R2` currently places `n=8`
  first, `n=7` second, and `n=6` third on most checked focused settings;
- one small combined discretization variation (`m_basis = 7`,
  `n_collocation = 140`) flips `n=7` above `n=8` by a small margin;
- so `rho_R2` should presently be read as a comparative stacked diagnostic,
  not as the promoted main working criterion.

None of these labels implies a final physical critical-load claim.

## Project Strategy After Outcome B

- The local theorem-facing branch is frozen for now at Outcome B on the current
  checked boundary.
- This is a project-strategy stopping point, not a mathematical impossibility
  claim.
- The next active path is criterion-level synthesis / interpretation.
- The current source-of-truth rebuild reading is recorded separately in
  `docs/theory/current_simple_support_criterion_rebuild_note.md`.
- Do not reopen the same checked local branch unless a genuinely new
  theorem-facing idea appears.
- The next bridge question is how the checked local quotient result should be
  read together with `A_ls`, `L_red`, `B_red`, and `B_mix` without overclaiming
  final physical criticality.
- The current theorem program above that frozen boundary is recorded in
  `docs/theory/current_simple_support_theorem_roadmap.md`.
