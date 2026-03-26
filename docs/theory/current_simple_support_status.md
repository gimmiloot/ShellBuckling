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

This path is separate from the active mixed-weak scans. The active mixed-weak
scan tasks still use the older reduced `F_min` background and should not be read
as the fully consistent simple-support background solver.

## Current Reproducible Loads
Several load markers should now be kept separate:

- old-path reproducible anchor load: `4.3434 MPa`
- old-path first persistent failure load: `4.3440 MPa`
- best bounded method-sweep ceiling from pilot 20: `4.3520 MPa` (`u_z_scaled_state`)
- best bounded staged continuation ceiling from pilot 21: `4.3800 MPa` (`u_z`-scaled continuation + auxiliary arc-like step adaptation)
- stronger dedicated milestone point above the audited ceiling: `4.4000 MPa` (same accepted seed, repeated pointwise confirm, `near_reproducible = true`, no branch-jump suspicion, but `strict_reproducible = false`)
- current fast-engine highest stored operational continuation load: `6.0000 MPa` (`fast_u_z_scaled_arc_like_continuation.py`), still kept separate from the canonical audited ceiling language
- sparse milestone confirms at `5.0000`, `5.5000`, and `6.0000 MPa`: same accepted seed, no branch-jump suspicion, `strict_reproducible = false` throughout, and `near_reproducible = false` above `5.0 MPa` because the repeat drift gradually exceeds the current confirm threshold
- best bounded staged continuation first failure in the audited pilot-21 ladder: not reached
- current short confirm probes above the newer fast-engine checkpoints: no failure reached through `4.4100 MPa` from the dedicated `4.4000 MPa` audit and through `6.0040 MPa` from the sparse `5.0000 / 5.5000 / 6.0000 MPa` confirms

The `4.3434 / 4.3440 MPa` pair is still the canonical old-path reference for
the original single-domain rescue-local continuation workflow. The `4.3520 MPa`
value remains the bounded pilot-20 method ceiling for the standalone
`u_z`-scaled solve. The `4.3800 MPa` value remains the current audited
pilot-21 continuation ceiling on the same 6-state equations and BC set. The
`4.4000 MPa` point is still the strongest post-`4.3800 MPa` milestone because
it already has repeated same-seed near-reproducible confirms and no
branch-jump signal. The higher `5.0000..6.0000 MPa` points belong to the
fast/resumable continuation workflow as operational continuation evidence with
same-branch indicators, but without audit closure under the current confirm
policy. None of these values is a final physical critical load claim.

## Current Milestone / Audit Policy
The confirm language is now explicit and split into two layers.

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
- `stronger milestone`
  same-branch indicators stay strong, `near_reproducible` remains true, and a
  short confirm probe is recorded without failure;
- `audited ceiling`
  promotion above the current audited ceiling still requires explicit milestone
  audit closure, including `strict_reproducible`;
- `operational continuation evidence`
  accepted fast-run continuation result without that milestone-promotion
  closure.

This keeps the status language conservative. Loads above `4.3800 MPa` are not
promoted silently, and the current `strict_reproducible = false` signal remains
an explicit open audit-policy issue rather than a silent branch-loss claim.

Milestone retention is also explicit in the fast workflow. By default the
retained confirmable milestone schedule includes:

- `4.3520 MPa`;
- `4.3800 MPa`;
- `4.4000 MPa`;
- the `0.5 MPa` round grid;
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
  `4.9000`, `5.0000`, `5.2000`, `5.4000`, `5.6000`, `5.8000`, and `6.0000 MPa`
  without a bounded failure event in the saved fast ladder;
- a stricter dedicated audit at `4.4000 MPa` repeats the same accepted seed in
  two independent pointwise confirm passes, stays `near_reproducible`, shows no
  branch-jump suspicion, and does not hit a short failure probe through
  `4.4100 MPa`, but still does not satisfy the stricter
  `strict_reproducible` gate;
- sparse confirms at `5.0000`, `5.5000`, and `6.0000 MPa` keep the same
  accepted seed, show no branch-jump suspicion, and do not hit short failure
  probes through `6.0040 MPa`, but their repeat drift grows smoothly from about
  `2.30e-5` to `3.23e-5` in max-relative-L2, so they no longer satisfy the
  current `near_reproducible` threshold above `5.0 MPa` even while remaining
  much closer to the retest point than an ordinary adjacent continuation step;
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
The current shallow-comparison picture is unchanged:

- the old shallow comparison path was BC-mismatched for simple support;
- pilot 16 built the strongest current BC-aligned shallow simple-support
  comparator;
- pilot 17 showed that the corrected shallow/non-shallow mismatch becomes
  clearly visible around `2..3 MPa`, grows with load, and stays smooth through
  the available high-load range;
- there is still no special new shallow/non-shallow jump localized exactly at
  the old `4.3434..4.3440 MPa` ceiling band.

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
- treat the current `strict_reproducible` thresholds themselves as an open
  audit-policy question before promoting loads above `4.3800 MPa` to audited
  status;
- keep the historical bounded pilot-21 script unchanged with its old
  `MAX_STEP_MPA = 0.0025` record, but use the fast runner's explicit
  runtime-controlled step policy for operational climbing so `--max-step-mpa`
  is no longer silently shadowed by the historical cap;
- do not spend more time on simple edge-mesh concentration by itself;
- do not reconnect the mixed-weak scans to this path yet;
- keep reporting candidate loads as exploratory.

## Canonical Runnable Entry Points
Baseline and report entry points:

- `tasks/run_axisymmetric_simple_support_background.py`
- `tasks/run_axisymmetric_simple_support_background_report.py`
- `tasks/run_axisymmetric_simple_support_local_branch_following.py`

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
