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
- Reproducible anchor load: `4.3434 MPa`
- First persistent failure load: `4.3440 MPa`

These values come from the current staged continuation record centered on pilot
12 and the later pilot-18 / pilot-19 follow-up diagnostics.

## Current Barrier Interpretation
The current reading is still mainly numerical:

- the branch reaches a reproducible `4.3434 MPa` anchor;
- the first persistent staged failure at `4.3440 MPa` keeps very small BC
  residuals;
- failure remains strongly right-edge-layer dominated with `u_z` as the leading
  gradient variable and `varphi` as the secondary shoulder;
- pilot 18 did not show a clear near-fold / collapsing-singular-value signal;
- pilot 19 tested edge-aware right-edge discretizations, but the best usable
  edge-aware path still stopped at the same `4.3434 / 4.3440 MPa` ceiling/failure
  pair.

So the barrier still reads as a stiff numerical right-edge-layer bottleneck on
an already non-shallow branch, not as a verified physical fold.

## Shallow / Non-Shallow Comparison Status
The current shallow-comparison picture is:

- the old shallow comparison path was BC-mismatched for simple support;
- pilot 16 built the strongest current BC-aligned shallow simple-support
  comparator;
- pilot 17 showed that the corrected shallow/non-shallow mismatch becomes
  clearly visible around `2..3 MPa`, grows with load, and stays smooth through
  the available high-load range;
- there is no special new shallow/non-shallow jump localized exactly at the
  present `4.3434..4.3440 MPa` ceiling band.

## Current Next Step
The current next step is still conservative numerical stabilization of the
separate 6-state simple-support background path above the reproducible
`4.3434 MPa` anchor.

That means:

- continue bounded, explicitly diagnosed continuation work near `4.3440 MPa`;
- keep equations and BCs fixed while testing safe numerical strategies;
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

For comparison context only, not as the canonical simple-support background
solver path:

- `experiments/supporting/run_supporting_dimensionless_comparison.py`
- `experiments/supporting/run_supporting_determinant_comparison.py`
