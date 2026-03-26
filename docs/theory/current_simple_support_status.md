# Current Simple-Support Operational Status

## Scope
This file is the canonical operational snapshot for the separate active 6-state
axisymmetric `simple support` background path.

It is intentionally short and operational. It does not replace:

- `docs/theory/current_theory_verification_map.md` for claim-status tracking;
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
- critical-layer boundary rows: `[u_n(1), varphi(1), T_s(1), S(1), H(1)]`

This new path reconnects the mixed-weak criticality layer to the honest full-
state simple-support background without reusing the older `F_min` line.


## First Clean Full Critical-Search Campaign
The first full exploratory run of the standalone clean simple-support critical
search has now been executed with:

- runner: `tasks/run_full_simple_support_critical_search.py`
- honest background BC set: center `T_sn(x0)=0`, `u_r(x0)=0`, `varphi(x0)=0`;
  edge `T_s(1)=0`, `M_s(1)=0`, `u_z(1)=0`
- critical rows: `[u_n(1), varphi(1), T_s(1), S(1), H(1)]`
- first mode range: `n=2..6`

Current numerical reading from that clean program is still limited by the
honest background continuation itself rather than by a detected high-load
critical region:

- the first moderate scan on `0..15 MPa` with 31 load points succeeded only
  through `4.0 MPa` and then lost the background at `4.5 MPa`;
- a narrow upper-edge refinement on `3.0..4.4 MPa` pushed the clean program to
  `4.3 MPa` and then lost the background at `4.4 MPa`;
- a second upper-edge refinement on `4.30..4.343 MPa` reached `4.3246 MPa` and
  then failed at `4.3276 MPa`;
- no clean-program search point reached the FEM-oriented `12..14 MPa` band in
  this first campaign.

Current exploratory candidate loads from the clean program are:

- `n=2`: `4.3215 MPa`, smooth upper-edge local minimum before background loss;
- `n=3`: `4.3215 MPa`, smooth upper-edge local minimum before background loss;
- `n=4`: `2.9 MPa`, broad interior minimum on the refined grid;
- `n=5`: about `1.84 MPa`, currently the lowest raw `sigma_bal` point but with
  noticeably more local oscillation / sensitivity than the smoother `n=2,4,6`
  trends;
- `n=6`: `4.3154 MPa`, smooth upper-edge local minimum before background loss.

So within the range currently reachable by the clean standalone program, the
lowest raw criterion value comes from `n=5`, but the smoother and more
numerically believable downward trends currently appear for `n=2` and `n=6` as
both continue decreasing toward the same background-loss barrier near
`4.32..4.33 MPa`. These are exploratory candidates only, not final physical
critical loads.


## Current Reproducible Loads
Several load markers should now be kept separate:

- old-path reproducible anchor load: `4.3434 MPa`
- old-path first persistent failure load: `4.3440 MPa`
- best bounded method-sweep ceiling from pilot 20: `4.3520 MPa` (`u_z_scaled_state`)
- best bounded staged continuation ceiling from pilot 21: `4.3800 MPa` (`u_z`-scaled continuation + auxiliary arc-like step adaptation)
- strongest post-audited validated operational milestone: `4.4000 MPa` (same accepted seed, repeated pointwise confirm, `near_reproducible = true`, no branch-jump suspicion, short probe through `4.4100 MPa`, but `strict_reproducible = false`)
- higher validated operational milestones from the fast/confirm workflow: `7.0000 MPa` and `10.0000 MPa` (same accepted seed, no branch-jump suspicion, smooth repeat drift smaller than adjacent-step drift, short confirm probes through `7.0080` and `10.0200 MPa`, `strict_reproducible = false`, `near_reproducible = false`)
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
The current next step is still conservative numerical stabilization of the
separate 6-state simple-support background path, but the preferred high-load
workflow is now explicitly split into two layers:

- use `u_z`-scaled continuation with auxiliary arc-like step adaptation as the
  default high-load path;
- use `fast_u_z_scaled_arc_like_continuation.py` for resumable upward progress
  from the latest checkpoint rather than replaying the whole path from scratch;
- use `confirm_u_z_scaled_arc_like_continuation.py` only at milestone loads,
  first-failure neighborhoods, or when branch-jump suspicion needs to be
  checked more carefully;
- keep the old `4.3434 / 4.3440 MPa` pair explicit as the canonical old-path
  anchor/failure reference rather than merging it with the newer bounded
  ceilings;
- keep the audited pilot-21 `4.3800 MPa` ceiling explicit even when the fast
  runner temporarily moves higher in operational continuation runs;
- use the new `validated operational milestone` class for high-load same-branch
  points that have dedicated milestone confirm discipline but still lack strict
  audited-ceiling closure;
- treat the current `strict_reproducible` thresholds themselves as an open
  audit-policy question before promoting loads above `4.3800 MPa` to audited
  status;
- keep the historical bounded pilot-21 script unchanged with its old
  `MAX_STEP_MPA = 0.0025` record, but use the fast runner's explicit
  runtime-controlled step policy for operational climbing so `--max-step-mpa`
  is no longer silently shadowed by the historical cap;
- do not spend more time on simple edge-mesh concentration by itself;
- use the new standalone clean critical-search program `tasks/run_full_simple_support_critical_search.py` when the goal is the consistent full simple-support mixed-weak search rather than the preserved hybrid testbenches;
- keep the preserved hybrid scan wrappers separate and readable as legacy/exploratory testbenches rather than as the preferred clean simple-support solver;
- treat the present clean-program bottleneck as a background-continuation issue: the standalone search now works and yields exploratory mode candidates, but with its current honest background stepping it still loses the branch near `4.32..4.5 MPa` and therefore does not yet probe the expected `12..14 MPa` region;
- the next unresolved engineering step before a real clean `12..15 MPa` search is to give this standalone critical-search path access to the same kind of robust high-load background continuation discipline already demonstrated separately on the 6-state simple-support path, without falling back to the old hybrid `F_min` line;
- keep reporting candidate loads as exploratory.

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
