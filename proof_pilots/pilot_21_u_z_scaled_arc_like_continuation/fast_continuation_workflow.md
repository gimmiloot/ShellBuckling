# Pilot 21 Fast Continuation Workflow

## Goal
Turn the audited pilot-21 `u_z`-scaled + auxiliary arc-like continuation path
into a practically usable high-load workflow that can resume from checkpoints
instead of replaying the whole branch from the old `4.3434 / 4.3440 MPa`
reference pair every time.

## Scope
This workflow keeps fixed:

- the same 6-state equations in
  `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`;
- the same simple-support BC set
  `T_s(1)=0`, `M_s(1)=0`, `u_z(1)=0`, `T_sn(x0)=0`, `u_r(x0)=0`, `varphi(x0)=0`;
- the separation between this path and the active mixed-weak scans that still
  use the older reduced `F_min` background.

## Architecture
Two runnable layers now sit inside the pilot-21 package:

- `fast_u_z_scaled_arc_like_continuation.py`
  Fast checkpointed continuation runner. It reuses the exact pilot-20
  `u_z`-scaled solve, keeps the same auxiliary arc-like step adaptation,
  starts from the latest checkpoint when available, and writes lightweight
  machine-readable progress after every accepted step.
- `confirm_u_z_scaled_arc_like_continuation.py`
  Pointwise confirm/audit runner. It reads the fast-run checkpoints, reruns
  selected milestone loads, checks continuity / branch-jump suspicion only
  where needed, and probes a short first-failure neighborhood without turning
  every run into a full pilot audit.

Shared runtime helper:

- `continuation_runtime.py`
  Local helper for checkpoint I/O, profile reconstruction, and compact log
  serialization inside the pilot-21 package.

## Checkpoint Policy
Fast-run artifacts live in `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/`.
The default checkpoint mode is now `rolling+milestones`, with four explicit
policies available from the CLI:

- `all`
  Keep every accepted-step checkpoint. This is a debug/archive mode, not the
  normal recommendation.
- `rolling`
  Keep only the latest rolling history plus the active resume pair and required
  bootstrap anchors.
- `milestones`
  Keep only milestone loads, their local predecessor context, and the active
  resume pair.
- `rolling+milestones`
  Recommended default. Keep a bounded rolling history together with milestone
  loads and special context points.

Default retention keeps:

- the named bootstrap files `bootstrap_previous_4p3433_mpa.npz` and
  `scaled_anchor_4p3434_mpa.npz`;
- the current active `older/previous` resume pair;
- milestone checkpoints plus their two-step local predecessor context;
- rolling checkpoints every `N` accepted steps (default `N=5`) capped at the
  latest `24` rolling points;
- failure/suspicious context checkpoints if they appear.

This keeps ordinary local runs far below the old "hundreds of `npz`" pattern
while preserving resume capability and sparse confirm on milestone loads. If a
confirm target was pruned, rerun the fast layer with a more archival checkpoint
policy or keep that load as a milestone.

## Tracked vs Runtime Artifacts
The pilot-21 fast workflow now separates compact repository artifacts from local
runtime cache:

- `fast_progress.json`
  Current machine-readable state, accepted-step table, and checkpoint pointers.
  This remains the compact tracked summary.
- `confirm_results.json`
  Default pointwise confirm output. This remains the compact tracked confirm
  summary.
- `progress_log.jsonl`
  Append-only event log. This is local runtime cache and is ignored from git by
  default.
- `checkpoints/*.npz`
  Raw accepted-step checkpoints used for resume and confirm mode. These are
  local runtime cache and are ignored from git by default.
- `confirm_*.json`
  Ad hoc milestone-audit dumps from custom `--output-json` runs. These are also
  treated as local runtime cache unless a result is promoted manually.

## Current Smoke Outcome
Keep the status language separated:

- canonical old-path reference pair: `4.3434 / 4.3440 MPa`;
- canonical pilot-20 bounded ceiling: `4.3520 MPa`;
- canonical audited pilot-21 bounded ceiling: `4.3800 MPa`.

Separately from those audited markers, the fast workflow has now shown:

- a first from-scratch checkpointed run reached `4.3900 MPa` in about `798 s`;
- resume runs then extended the saved path through `4.4200`, `4.4400`,
  `4.4600`, `4.4800`, and `4.5000 MPa` in about `3.9 s` total across the five
  post-`4.4000 MPa` chunks on the same workspace;
- two further resume runs then carried the stored path from `4.5000 MPa` to
  `5.7500 MPa` and on to `6.0000 MPa` in about `34.9 s` total, again without a
  bounded failure in the saved ladder;
- a dedicated `4.4000 MPa` milestone audit ran twice and both passes returned
  `strict_reproducible = false` but `near_reproducible = true`, with the same
  accepted seed, no branch-jump suspicion, and no failure in the short probe
  through `4.4100 MPa`;
- sparse confirm at `5.0000`, `5.5000`, and `6.0000 MPa` kept the same accepted
  seed, showed no branch-jump suspicion, and did not hit short failure probes
  through `6.0040 MPa`, but `near_reproducible` turned false above `5.0 MPa`
  because the repeat drift gradually exceeded the current confirm threshold;
- the observed repeat drift stays smooth and is currently `M_s`-dominated,
  while the ordinary adjacent-step branch drift remains roughly `20x..38x`
  larger in max-relative-L2 than the repeat drift across the checked
  milestones.

Open method notes:

- the current strict gate is still inherited from pilot 12 as `1e-7 / 1e-6`,
  so the remaining `strict_reproducible = false` signal is presently better
  read as an audit-policy / metric issue than as evidence of branch loss;
- the current fast runner cannot actually exceed the pilot-21 package cap
  `MAX_STEP_MPA = 0.0025`, because `adapt_step_size()` already clamps there,
  so the workflow is now cheap enough for further operational climbing but not
  yet aggressively optimized for a much faster march toward `~10 MPa`.

These fast-run loads are operational continuation results, not a final physical
critical load and not yet a replacement for the current audited pilot-21
`4.3800 MPa` ceiling language; the stronger `4.4000 MPa` audit still remains
below canonical audited status because the stricter reproducibility gate has not
closed.
