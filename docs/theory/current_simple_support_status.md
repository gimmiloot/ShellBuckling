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
Two load markers should now be kept separate:

- old-path reproducible anchor load: `4.3434 MPa`
- old-path first persistent failure load: `4.3440 MPa`
- best bounded method-sweep ceiling to date: `4.3520 MPa`
- best bounded method-sweep first failure: not reached within the packaged pilot-20 ladder

The `4.3434 / 4.3440 MPa` pair is still the reproducible reference for the
original single-domain rescue-local continuation path. The new `4.3520 MPa`
value is a bounded numerical-method result from pilot 20, not a final physical
critical load claim.

## Current Barrier Interpretation
The current reading is still mainly numerical, but more specifically numerical
formulation / conditioning dominated:

- the old single-domain path still reaches a reproducible `4.3434 MPa` anchor
  and still fails first at `4.3440 MPa` with very small BC residuals;
- pilot 18 still shows no clear near-fold / collapsing-singular-value signal;
- pilot 19 showed that simple right-edge mesh concentration alone does not move
  the ceiling materially;
- pilot 20 showed that predictor-only changes help only modestly, while an
  unchanged-equation state representation change (`u_z`-scaled solve) can move
  the bounded ceiling materially upward;
- the dominant gradient ordering remains `u_z`, then `varphi`, then `T_s`.

So the barrier still reads as numerical rather than as a verified physical fold,
but the evidence now points more toward solver formulation / conditioning than
toward raw right-edge mesh density by itself.

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
separate 6-state simple-support background path, but the preferred next methods
are now sharper:

- continue the `u_z`-scaled state path first;
- treat the arc-like continuation surrogate as lower-priority backup only;
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

For comparison context only, not as the canonical simple-support background
solver path:

- `experiments/supporting/run_supporting_dimensionless_comparison.py`
- `experiments/supporting/run_supporting_determinant_comparison.py`
