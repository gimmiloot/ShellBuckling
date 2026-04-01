# Current Simple-Support Operational Status

## Scope
This file is the canonical operational snapshot for the separate active 6-state
axisymmetric `simple support` background path.

It is intentionally short and operational. It does not replace:

- `docs/theory/current_theory_verification_map.md` for claim-status tracking;
- `docs/theory/current_simple_support_final_audit_note.md` for the final
  audit-style closure reading of the current clean theorem-facing line;
- `docs/theory/current_mixed_weak_theory_note.tex` for compact scientific
  discussion;
- `docs/theory/vyvod_uravneniy_updated17.md` for derivation work;
- `docs/journal/project_journal_updated14.md` for project-stage discussion.

## Active 6-State Path
The active full-state simple-support background path is:

- core module: `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`
- state: `[T_s, T_sn, M_s, u_r, u_z, varphi]`
- BC set: center `T_sn(x0)=0`, `u_r(x0)=0`, `varphi(x0)=0`; edge `T_s(1)=0`,
  `M_s(1)=0`, `u_z(1)=0`

This path is separate from the preserved hybrid mixed-weak scans. Those older
scan tasks still use the reduced `F_min` background and should not be read as
the fully consistent simple-support solver path. A new clean standalone
critical-search program now also exists:

- core module: `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`
- task wrapper: `tasks/run_full_simple_support_critical_search.py`
- background continuation bridge: `src/shell_buckling/mixed_weak/simple_support_high_load_background_continuation.py`
- critical-layer boundary rows: `[u_n(1), varphi(1), T_s(1), S(1), H(1)]`

This new path reconnects the mixed-weak criticality layer to the honest full-
state simple-support background without reusing the older `F_min` line.


## Current Theorem-Facing Criterion Status
The theorem-facing local branch for the clean full `simple support / подвижный шарнир`
reduction is now carried by pilot 23 rather than by the older hybrid scans.
Its current stopping point is Outcome B on the checked local boundary:

- the selected leading trace plane is still `J_0(A_ls) = im(D_amp)`;
- the first checked higher-order local selected object is a corrected 3D family;
- the correct checked-boundary local theorem-facing object is the quotient
  `im(D_rich,eta^corr) / span(g_mem)`;
- no canonical higher-order 2D representative is currently justified on that
  checked boundary.

For criterion interpretation this means the clean reduced family should now be
read as the global KKT-selected family `A_ls`, the stacked reduced operator
`L_red` remains the theorem-facing target object, and the boundary-only objects
`B_red` / `B_mix` remain exploratory diagnostics rather than proved full
replacements for `L_red`.
The stabilized repo-facing interpretation language is summarized in
`docs/theory/current_simple_support_criterion_bridge_note.md`.

## Current One-Point Closure Boundary
The older theorem-step chain above the frozen local Outcome-B boundary should
now be read as saturated as far as the current clean repository boundary
allows.

The explicit weighted-ansatz membrane template is still important operationally:
it keeps membrane-channel skepticism alive on the present repository boundary.
But the current theorem-facing objects are still not closed enough to decide
the one-point status of

```text
c_temp := c_sel + z_temp,n(q;s_mem).
```

Specifically:

- `A_adm^th,n(q)` is not yet closed enough to decide
  `c_temp in A_adm^th,n(q)`;
- `Pair_chk,n(q)` is structurally defined, but not yet closed enough to decide
  `(c_temp, c_sel) in Pair_chk,n(q)` for this explicit point.

So the active theorem-facing line is no longer another old-style `T3...`
refinement. It is now the one-point closure branch:

- `Z_adm(c_temp)`: build or refute a one-point admissibility closure theorem
  for `c_temp`;
- `Z_chk(c_temp,c_sel)`: build or refute a one-point common-corrected-chart /
  checked-local shadow closure theorem for `(c_temp, c_sel)`.

Until one of those closure theorems is available, the current clean criterion
should not be read as theorem-secured enough to exclude that explicit membrane
candidate.

For the final audit-style project-state reading of this stopping point, see
`docs/theory/current_simple_support_final_audit_note.md`.


## First Clean Full Critical-Search Campaign
The first full exploratory run of the standalone clean simple-support critical
search is still kept in memory as an implementation baseline:

- runner: `tasks/run_full_simple_support_critical_search.py`
- honest background BC set: center `T_sn(x0)=0`, `u_r(x0)=0`, `varphi(x0)=0`;
  edge `T_s(1)=0`, `M_s(1)=0`, `u_z(1)=0`
- critical rows: `[u_n(1), varphi(1), T_s(1), S(1), H(1)]`
- first mode range: `n=2..6`

That first clean campaign used the right formulation but not yet the proven
high-load continuation discipline of the separate honest background path:

- the initial moderate scan on `0..15 MPa` with 31 load points succeeded only
  through `4.0 MPa` and then lost the background at `4.5 MPa`;
- a narrow upper-edge refinement on `3.0..4.4 MPa` pushed the clean program to
  `4.3 MPa` and then lost the background at `4.4 MPa`;
- a second upper-edge refinement on `4.30..4.343 MPa` reached `4.3246 MPa` and
  then failed at `4.3276 MPa`.

This earlier `4.32..4.5 MPa` clean-program loss should now be read only as a
superseded continuation bottleneck inside the first standalone implementation.
It is not evidence that the honest full-state simple-support background
physically ends there.

## High-Load-Enabled Clean Critical Search
The clean standalone search now also reuses the proven honest high-load
background-following discipline through:

- reusable bridge: `src/shell_buckling/mixed_weak/simple_support_high_load_background_continuation.py`
- same equations and same honest simple-support BC set as the active 6-state
  background path;
- exact retained high-load checkpoints from the separate pilot-21 background
  path where they already exist;
- the same `u_z`-scaled secant continuation attempts and runtime-controlled
  bounded step adaptation above the directly solved low-load band;
- no fallback to the old hybrid `F_min` background line.

With that upgrade the clean standalone `0..15 MPa` search for `n=2..6` now
succeeds through the full scheduled band with no background failure:

- successful background solves: `31 / 31`;
- highest reached clean-program load: `15.0 MPa`;
- first background failure in the scheduled clean run: not reached;
- the clean program now genuinely probes the FEM-oriented `12..14 MPa` region.

Current exploratory mode-by-mode reading from the clean program is now broader:

- `n=4`: weak control-mode interior minimum remains near `11.1 MPa`; this mode
  is still kept in the competition set because of the older FEM-oriented prior,
  not because the clean broad scan now makes it numerically strong;
- `n=6`: current leading supported clean candidate is an interior minimum near
  `17.6 MPa`; it remains exploratory and not yet a final physical claim, but it
  is still the strongest current candidate that has survived the clean
  competition workflow with at least moderate stability support;
- `n=8`: main unstable rival now sits near `17.8 MPa`; on some local windows it
  can beat `n=6` in raw `sigma_bal`, but its advantage remains sensitive to the
  exact local window and selected discretization;
- `n=7`: reserve mode can produce very sharp raw dips near `17.2..17.4 MPa`,
  including raw `sigma_bal` values below the current supported candidate, but
  these sharp dips have not yet shown acceptable robustness and should stay
  classified as raw-but-unsupported reserve readings;
- `n=14`: reserve mode also produces an interior point above the older
  `18 MPa` broad ceiling neighborhood, near `19.3 MPa`, but it has not yet
  upgraded into a stable real competitor;
- the earlier `n=5` / `n=6` target-band reading near `13.95..14.25 MPa`
  remains part of the project memory, but it is no longer the full current
  clean competition reading.

So the unresolved bottleneck is no longer honest-background reach. It is now
criterion discrimination / candidate selection inside the clean full
simple-support search: how to separate supported interior valleys from raw
window-sensitive sharp dips. The leading supported reading is presently `n=6`
near `17.6 MPa`; `n=8` remains the main unstable rival; `n=7` remains a raw
reserve dip without acceptable robustness; `n=4` remains a weak control mode.
None of these values is yet a final physical critical-load claim.

The later `A + C` criterion pilot did not materially improve this competition
picture: branch-aware descriptors were useful mainly negatively, while the
augmented / bordered solvability reading stayed boundary-led and unstable. A
first light `D` pilot on the same clean architecture then gave interior-
dominated local signals for `n=6`, `n=7`, and `n=8`, no longer read `n=7` as
the single strongest point-like dip, and placed `n=8` first in the focused
baseline D ranking; however, it did not settle the `n=6` versus `n=8`
competition robustly enough to replace the conservative supported-candidate
operational memory. A first light `E` pilot has now also been checked on the
same clean architecture: it uses an energy-like reduced-coercivity surrogate
based on the local tangent bundle plus an amplitude norm built from current
strain / curvature channels. This `E` reading is much more interpretable than
the raw boundary-only metric and stays interior-distributed on the checked
windows, but it still places `n=8` first in the focused baseline E ranking,
keeps `n=7` competitive, and therefore also does not yet settle the
competition strongly enough to replace the current conservative operational
memory.



## Current Reproducible Loads
Several load markers should now be kept separate:

- old-path reproducible anchor load: `4.3434 MPa`
- old-path first persistent failure load: `4.3440 MPa`
- best bounded method-sweep ceiling from pilot 20: `4.3520 MPa` (`u_z_scaled_state`)
- best bounded staged continuation ceiling from pilot 21: `4.3800 MPa` (`u_z`-scaled continuation + auxiliary arc-like step adaptation)
- strongest post-audited validated operational milestone: `4.4000 MPa` (same accepted seed, repeated pointwise confirm, `near_reproducible = true`, no branch-jump suspicion, short probe through `4.4100 MPa`, but `strict_reproducible = false`)
- higher validated operational milestones from the fast/confirm workflow: `7.0000 MPa` and `10.0000 MPa` (same accepted seed, no branch-jump suspicion, smooth repeat drift smaller than adjacent-step drift, short confirm probes through `7.0080` and `10.0200 MPa`, `strict_reproducible = false`, `near_reproducible = false`)
- current clean full simple-support critical-search broad compatible scan reach: `18.0000 MPa` with `38 / 38` scheduled background points on the clean compatible load ladder
- selected local competition / reserve windows have also been checked up to `22.0000 MPa` with retained-checkpoint-seeded clean helper continuation using the same equations and BC set; these local checks have not yet established a deeper supported candidate above `18 MPa`
- current fast-engine highest stored accepted load: `10.0000 MPa` (`fast_u_z_scaled_arc_like_continuation.py`), still kept separate from the canonical audited ceiling language
- best bounded staged continuation first failure in the audited pilot-21 ladder: not reached
- current short confirm probes above the newer fast-engine checkpoints: no failure reached through `4.4100 MPa` from the dedicated `4.4000 MPa` audit and through `10.0200 MPa` from the sparse `7.0000 / 10.0000 MPa` confirms

The `4.3434 / 4.3440 MPa` pair is still the canonical old-path reference for
the original single-domain rescue-local continuation workflow. The `4.3520 MPa`
value remains the bounded pilot-20 method ceiling for the standalone
`u_z`-scaled solve. The `4.3800 MPa` value remains the current audited
pilot-21 continuation ceiling on the same 6-state equations and BC set. The
`4.4000 MPa`, `7.0000 MPa`, and `10.0000 MPa` points should now be read as
validated operational milestones: they have dedicated milestone confirms with
strong same-branch indicators and successful short probes, but they do not have
strict audit closure and therefore do not replace the canonical audited
ceiling. Intermediate accepted points on the fast/resumable path remain
operational continuation evidence unless they are explicitly rechecked. None of
these values is a final physical critical load claim.

## Current Milestone / Audit Policy
The confirm language is now explicit and split into same-branch indicators plus
a three-level reporting ladder.

Same-branch indicators:

- same accepted seed;
- no `branch_jump_suspicion` in the continuity check;
- repeat drift remains smooth across checked milestones;
- repeat drift remains smaller than an ordinary adjacent continuation step;
- strongest gradient ordering remains `u_z > varphi > T_s`;
- BC residuals remain sane.

Promotion policy:

- `strict_reproducible`
  same-load repeat solve closes under the inherited pilot-12 gate
  `1e-7 / 1e-6` in max-relative-L2 / max-relative-max;
- `near_reproducible`
  same-load repeat solve keeps the same accepted seed and closes under the
  relaxed fast-workflow gate `2e-5 / 2e-4`;
- `operational continuation evidence`
  accepted fast-run continuation result without dedicated milestone validation;
- `validated operational milestone`
  dedicated milestone confirm keeps the same accepted seed, stays free of
  `branch_jump_suspicion`, keeps repeat drift smooth and smaller than an
  ordinary adjacent continuation step, preserves the current strongest
  gradient ordering and BC sanity checks, and records a short confirm probe
  without failure. `strict_reproducible` is not required; `near_reproducible`
  is supportive but not mandatory if the repeat drift still looks like a small
  smooth same-branch drift;
- `audited ceiling`
  promotion above the current audited ceiling still requires explicit milestone
  audit closure under the stricter current standard, including
  `strict_reproducible`.

This reporting change is about project discipline, not changed equations or BCs.
It keeps the status language conservative while preventing high-load same-branch
points from getting stuck between overly weak generic operational wording and
overly strong audited-ceiling wording. Loads above `4.3800 MPa` are still not
promoted silently, and the current `strict_reproducible = false` signal remains
an explicit open audit-policy issue rather than a silent branch-loss claim.

Milestone retention is also explicit in the fast workflow. By default the
retained confirmable milestone schedule includes:

- `4.3520 MPa`;
- `4.3800 MPa`;
- `4.4000 MPa`;
- the `0.5 MPa` round grid;
- the next `10 -> 15 MPa` confirm-critical schedule `11.0`, `12.0`, `12.5`,
  `13.0`, `13.5`, `14.0`, `15.0 MPa`;
- the current bootstrap/target loads;
- any extra user-requested `--milestone-load-mpa` values that are actually
  reached.

## Current Barrier Interpretation
The current reading is still mainly numerical, but now more sharply numerical
formulation / conditioning dominated:

- the old single-domain path still reaches a reproducible `4.3434 MPa` anchor
  and still fails first at `4.3440 MPa` with very small BC residuals;
- pilot 18 still shows no clear near-fold / collapsing-singular-value signal;
- pilot 19 showed that simple right-edge mesh concentration alone does not move
  the ceiling materially;
- pilot 20 showed that predictor-only changes help only modestly, while an
  unchanged-equation state representation change (`u_z`-scaled solve) moves the
  bounded ceiling to `4.3520 MPa`;
- pilot 21 then turned that into one main audited high-load workflow: the exact
  `u_z`-scaled continuation path plus auxiliary arc-like step adaptation
  reproduced `4.3520 MPa` and carried the bounded staged ladder through
  `4.3550`, `4.3600`, `4.3700`, and `4.3800 MPa` with reproducible stage
  retests and no bounded failure in the packaged ladder;
- the fast/confirm operational split reuses the same equations and BCs, adds
  checkpoint/resume, and now carries the stored path through `4.4200`,
  `4.4400`, `4.4600`, `4.4800`, `4.5000`, `4.6000`, `4.7000`, `4.8000`,
  `4.9000`, `5.0000`, `5.2000`, `5.4000`, `5.6000`, `5.8000`, `6.0000`,
  `6.5000`, `7.0000`, `8.0000`, `9.0000`, and `10.0000 MPa` without a bounded
  failure event in the saved fast ladder;
- a stricter dedicated audit at `4.4000 MPa` repeats the same accepted seed in
  two independent pointwise confirm passes, stays `near_reproducible`, shows no
  branch-jump suspicion, and does not hit a short failure probe through
  `4.4100 MPa`; under the new reporting policy this closes `4.4000 MPa` as a
  validated operational milestone, but it still does not satisfy the stricter
  `strict_reproducible` gate and therefore does not replace the audited ceiling;
- sparse confirms at `7.0000` and `10.0000 MPa` keep the same accepted
  seed, show no branch-jump suspicion, and do not hit short failure probes
  through `10.0200 MPa`; their repeat drift stays in the same smooth
  `2.85e-5..3.30e-5` max-relative-L2 band and still fails the current
  `near_reproducible` threshold even while remaining much smaller than an
  ordinary adjacent continuation step, so under the new reporting policy they
  also qualify as validated operational milestones rather than as audited
  ceiling replacements;
- after the clean standalone critical-search path was upgraded to reuse the
  same high-load continuation discipline, the honest background also stays
  alive through the clean `0..15 MPa` mixed-weak search; this confirms that the
  earlier standalone `4.32..4.5 MPa` loss was a solver-workflow bottleneck,
  not evidence of a physical end of the honest background branch;
- the repeat drift is smooth and currently dominated by `M_s`, while the
  strongest gradient ordering inside the accepted branch still remains `u_z`,
  then `varphi`, then `T_s`;
- the current `strict_reproducible` gate is still inherited from the older
  pilot-12 threshold pair `1e-7 / 1e-6`, so the remaining strict-false signal
  presently reads more like an open audit-policy / metric issue than like
  evidence of branch loss.

So the barrier still reads as numerical rather than as a verified physical fold,
and the newer data sharpen that reading toward solver formulation / conditioning
plus confirm-policy sensitivity rather than toward a verified physical end of
branch.

## Shallow / Non-Shallow Comparison Status
The shallow-comparison picture is now sharper but still conservative:

- the old shallow comparison path was BC-mismatched for simple support;
- pilot 16 built the strongest current BC-aligned shallow simple-support
  comparator;
- pilot 17 showed that the corrected shallow/non-shallow mismatch becomes
  clearly visible around `2..3 MPa`, grows with load, and stays smooth through
  the available high-load range;
- a new exact-load comparison pilot at `4.0`, `7.0`, and `10.0 MPa` reuses the
  same corrected shallow comparator and the same mapped `arrays_nepol_sin(...)`
  logic from the current 6-state system: the mismatch is already moderately
  visible at `4.0 MPa`, becomes clearly visible at `7.0 MPa`, stays clearly
  visible at `10.0 MPa`, and remains dominated by right-edge differences rather
  than by a special new jump localized exactly at the old `4.3434..4.3440 MPa`
  ceiling band.

## Current Next Step
The preferred next move is no longer deeper continuation of the same checked
local theorem branch. That branch is frozen for now at Outcome B on its current
checked boundary.

Operationally, the clean full `simple support / подвижный шарнир` workflow still
keeps the same high-load discipline:

- use `u_z`-scaled continuation with auxiliary arc-like step adaptation as the
  default high-load path for the separate 6-state background family;
- use `fast_u_z_scaled_arc_like_continuation.py` for resumable upward progress
  and `confirm_u_z_scaled_arc_like_continuation.py` only at milestone or audit
  loads;
- keep the clean standalone search `tasks/run_full_simple_support_critical_search.py`
  as the preferred clean mixed-weak search, and keep the preserved hybrid scan
  wrappers only as legacy/exploratory testbenches;
- keep candidate loads reported conservatively as exploratory, supported,
  unstable-rival, or reserve readings rather than as final physical critical
  loads.

The theorem-facing next move is now criterion-level synthesis / interpretation:

- read `A_ls` as the global weak/KKT-selected family, not as the raw local
  regular family;
- keep `L_red` as the main reduced theorem-facing operator;
- read `B_red` and `B_mix` as boundary-only / exploratory diagnostics on the
  current reduced family, not as already proved full replacements for `L_red`;
- use the local Outcome-B quotient result as a caution layer when interpreting
  clean candidate loads and modes;
- prefer a bridge from the checked local quotient theorem back to the global
  reduced criterion story over deeper continuation of the same local branch.

## Canonical Runnable Entry Points
Baseline, report, and clean critical-search entry points:

- `tasks/run_axisymmetric_simple_support_background.py`
- `tasks/run_axisymmetric_simple_support_background_report.py`
- `tasks/run_axisymmetric_simple_support_local_branch_following.py`
- `tasks/run_full_simple_support_critical_search.py`

Canonical bounded high-load / diagnosis scripts:

- `proof_pilots/pilot_12_high_load_branch_extension/numerical_extension.py`
- `proof_pilots/pilot_18_revised_analytic_barrier_diagnosis/jacobian_conditioning_check.py`
- `proof_pilots/pilot_18_revised_analytic_barrier_diagnosis/term_balance_check.py`
- `proof_pilots/pilot_19_edge_stretched_simple_support_continuation/edge_stretched_continuation.py`
- `proof_pilots/pilot_20_method_sweep_for_simple_support_ceiling/method_sweep.py`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/u_z_scaled_arc_like_continuation.py`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_u_z_scaled_arc_like_continuation.py`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/confirm_u_z_scaled_arc_like_continuation.py`

For comparison context only, not as the canonical simple-support background
solver path:

- `experiments/supporting/run_supporting_dimensionless_comparison.py`
- `experiments/supporting/run_supporting_determinant_comparison.py`


