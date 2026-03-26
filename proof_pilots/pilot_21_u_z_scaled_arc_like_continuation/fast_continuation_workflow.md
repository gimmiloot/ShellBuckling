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
  `u_z`-scaled solve, keeps the same auxiliary arc-like continuation logic,
  starts from the latest checkpoint when available, and writes lightweight
  machine-readable progress after every accepted step.
- `confirm_u_z_scaled_arc_like_continuation.py`
  Pointwise confirm/audit runner. It reads the fast-run checkpoints, reruns
  selected milestone loads, checks continuity / branch-jump suspicion only
  where needed, and probes a short first-failure neighborhood without turning
  every run into a full pilot audit.

Shared runtime helper:

- `continuation_runtime.py`
  Local helper for checkpoint I/O, runtime-controlled fast-step adaptation,
  milestone retention, compact log serialization, and explicit audit-policy
  summaries inside the pilot-21 package.

## Fast Step Policy
The historical bounded pilot artifact
`u_z_scaled_arc_like_continuation.py` keeps its original internal controller,
including the old audited cap `MAX_STEP_MPA = 0.0025`.

The operational fast runner is now separate from that historical controller.
Its accepted-step adaptation is runtime-controlled and respects the current CLI
limits rather than silently reusing the old pilot cap. The fast layer exposes:

- `--initial-step-mpa`
- `--min-step-mpa`
- `--max-step-mpa`
- `--success-growth`
- `--conditioning-shrink`
- `--failure-shrink`

The decision logic is intentionally unchanged in structure: smooth accepted
steps may grow, crowded accepted steps may shrink, and failed solves still use
a separate failure shrink. What changed is only where the limits live: the
runtime layer now owns them explicitly.

## Checkpoint Policy
Fast-run artifacts live in
`proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/`.
The default checkpoint mode is `rolling+milestones`, with four explicit
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

The milestone schedule is now explicit. By default the fast layer retains:

- the canonical pilot-20 marker `4.3520 MPa`;
- the audited pilot-21 ceiling `4.3800 MPa`;
- the strongest non-promoted milestone `4.4000 MPa`;
- every `0.5 MPa` round milestone;
- the planned `6 -> 10 MPa` confirm schedule `6.5`, `7.0`, `8.0`, `9.0`, `10.0 MPa`;
- the current `--bootstrap-target-mpa` and `--target-load-mpa`;
- any extra user-requested milestone passed via repeated `--milestone-load-mpa`.

This keeps ordinary local runs far below the old ?hundreds of `npz`? pattern
while preserving resume capability and sparse confirm on milestone loads. If a
confirm target was pruned, rerun the fast layer with a more archival
checkpoint policy or add that load explicitly via `--milestone-load-mpa`. If a copied or legacy run directory still contains the named bootstrap files but has lost their metadata pointers, the fast runner now normalizes those pointers before falling back to an expensive bootstrap-anchor rebuild.

## Tracked vs Runtime Artifacts
The pilot-21 fast workflow separates compact repository artifacts from local
runtime cache:

- `fast_progress.json`
  Current machine-readable state, accepted-step table, checkpoint pointers,
  retained milestone list, and the active fast/audit policy summaries. This
  remains the compact tracked summary.
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

This now follows the repo-wide convention: future pilots that generate the same
kind of runtime cache should either reuse the standard `proof_pilots/<pilot>/fast_run/`
layout or come with an explicit `.gitignore` update.

## Audit Policy
The confirm layer now keeps an explicit split between same-branch indicators and
promotion policy.

Same-branch indicators:

- same accepted seed;
- no `branch_jump_suspicion` in the continuity check;
- repeat drift smoothness across checked milestones;
- repeat drift smaller than an ordinary adjacent continuation step;
- consistent strongest gradient ordering, currently `u_z > varphi > T_s`;
- sane BC residuals.

Promotion language:

- `strict_reproducible`
  Same-load repeat solve closes under the inherited pilot-12 gate
  `1e-7 / 1e-6` in max-relative-L2 / max-relative-max.
- `near_reproducible`
  Same-load repeat solve keeps the same accepted seed and closes under the
  relaxed fast-workflow gate `2e-5 / 2e-4`.
- `stronger milestone`
  Same-branch indicators stay strong, `near_reproducible` remains true, and a
  short confirm probe is recorded without failure.
- `audited ceiling`
  Promotion above the current audited ceiling still requires explicit milestone
  audit closure, including `strict_reproducible`.
- `operational continuation evidence`
  Accepted fast-run continuation result without that milestone-promotion
  closure.

This keeps the repo conservative: loads above `4.3800 MPa` are not silently
relabelled as audited just because same-branch indicators stay strong. The
current `strict_reproducible = false` signal is tracked explicitly as an open
audit-policy issue rather than silently reinterpreted as branch loss.

## Confirm Probe Policy
The confirm runner still stays cheap, but the failure probe is now slightly more
meaningful at high load:

- an explicit `--failure-probe-step-mpa` still overrides everything;
- otherwise the probe step follows the accepted operational step size;
- a separate high-load floor is available through
  `--failure-probe-high-load-step-mpa` and
  `--failure-probe-high-load-threshold-mpa`.

So the default probe can widen modestly at higher loads without turning confirm
into a heavy replay audit.

## Current Smoke Outcome
Keep the status language separated:

- canonical old-path reference pair: `4.3434 / 4.3440 MPa`;
- canonical pilot-20 bounded ceiling: `4.3520 MPa`;
- canonical audited pilot-21 bounded ceiling: `4.3800 MPa`.

Separately from those audited markers, the fast workflow has shown operational
continuation evidence through `10.0000 MPa`, a stronger dedicated milestone at
`4.4000 MPa`, and sparse confirms through `10.0200 MPa`. These newer loads are
still operational continuation results, not a final physical critical load and
not yet a replacement for the current audited pilot-21 `4.3800 MPa` ceiling
language.
