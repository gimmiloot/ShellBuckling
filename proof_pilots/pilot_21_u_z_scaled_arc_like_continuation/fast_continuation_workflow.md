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

## Checkpoint Layout
Fast-run artifacts live in `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/`:

- `fast_progress.json`
  Current machine-readable state, accepted-step table, and checkpoint pointers.
- `progress_log.jsonl`
  Append-only lightweight event log.
- `checkpoints/*.npz`
  Accepted-step checkpoints used for resume and confirm mode.
- `confirm_results.json`
  Latest pointwise confirm output.

## Current Smoke Outcome
Keep the status language separated:

- canonical old-path reference pair: `4.3434 / 4.3440 MPa`;
- canonical pilot-20 bounded ceiling: `4.3520 MPa`;
- canonical audited pilot-21 bounded ceiling: `4.3800 MPa`.

Separately from those audited markers, the new fast workflow has already shown:

- a first from-scratch checkpointed run reached `4.3900 MPa` in about `798 s`;
- resume runs then extended the saved path to `4.3950 MPa` and `4.4000 MPa`
  in under a second each on the same workspace;
- confirm at `4.4000 MPa` returned `strict_reproducible = false` but
  `near_reproducible = true`, with the same accepted seed, no branch-jump
  suspicion, and no failure in the short probe through `4.4040 MPa`.

These fast-run loads are operational continuation results, not a final physical
critical load and not yet a replacement for the current audited pilot-21
`4.3800 MPa` ceiling language.
