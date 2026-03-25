# Project Layering Refactor Note

## Purpose
This note records a conservative layering and deduplication review of the
repository after the documentation cleanup that centralizes the operational
status of the separate 6-state simple-support background path.

The goal here is not aggressive movement of source files. The goal is to state
what is already layered well, what is still duplicated or easy to confuse, and
which refactor steps are safe versus risky.

## Current Layering Strengths
- Reusable Python logic already lives under `src/` rather than being spread
  across root scripts.
- Runnable entry points are already separated into `tasks/` for active tasks and
  `experiments/supporting/` for supporting comparison workflows.
- Theory, assumptions, journal, and BC-audit material already live under
  `docs/`, which makes documentation-level cleanup safer than code movement.
- The separate 6-state simple-support background path already exists as its own
  module in `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`.
- The active mixed-weak scans are already distinct from the supporting
  moving-clamp/sliding-clamp comparison path at the filesystem level.

## Current Duplication / Problem Areas
### 1. Simple-support operational status used to be repeated in several places
Before this cleanup, README, project map, BC audit notes, and the supervisor
note all carried overlapping status text about the separate 6-state
simple-support background path.

That duplication was risky because the operational numbers drifted. In
particular, some docs still said the path reached only about `4.30 MPa` and
failed near `4.33 MPa`, while the current bounded continuation record had
already moved to the reproducible `4.3434 MPa` anchor with first persistent
failure at `4.3440 MPa`.

### 2. The active mixed-weak scans and the separate 6-state background are easy to mix up
The active mixed-weak scan tasks still use the older `F_min` background, while
the separate 6-state simple-support background path is a different runnable
line. The project layering is already good enough to keep them separate on disk,
but the documentation needed a cleaner pointer structure.

### 3. Supporting comparison paths remain scientifically useful but can be mistaken for active closure
The supporting moving-clamp/sliding-clamp axisymmetric comparison path is still
important for diagnostics, but it should not be mistaken for the current
full simple-support background path.

### 4. Old versus new shallow comparator status also needed a stable pointer
The old shallow comparator was BC-mismatched for simple support, while the new
pilot-16 comparator is the current BC-aligned shallow comparison line. That
history matters, but it should live in role-appropriate docs rather than being
repeated everywhere.

## Safe Next Refactor Steps
- Keep `docs/theory/current_simple_support_status.md` as the canonical
  operational status page for the separate 6-state simple-support background
  path.
- Continue replacing duplicated operational status blurbs with short
  role-specific pointers in documentation.
- Keep README focused on repository orientation and run commands rather than on
  detailed pilot-by-pilot status snapshots.
- Keep `docs/project_map.md` focused on structure and role separation rather
  than on operational load ceilings.
- Keep `docs/theory/current_theory_verification_map.md` focused on claim status,
  with only a pointer to the operational status page where appropriate.
- If more simple-support diagnosis pilots are added, update the canonical status
  page first and then only adjust short pointers elsewhere.

## Risky Refactor Steps To Postpone
- Do not merge the active mixed-weak scan path and the separate 6-state
  simple-support background path into one code path yet.
- Do not move or rename `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`
  while the runnable tasks and proof pilots still refer to it directly.
- Do not collapse `solver_simple_support_core.py` and `solver_patched_core.py`
  until the boundary-row differences and background-role differences are either
  removed or intentionally frozen.
- Do not move pilot scripts into `tasks/` just for cosmetic consistency. Several
  of them are proof/diagnostic packages with their own local notes and artifacts.
- Do not remove the supporting moving-clamp/sliding-clamp comparison path. It is
  still part of the comparison architecture.
- Do not delete the old shallow-comparison history. Keep the distinction between
  the BC-mismatched old shallow path and the pilot-16 BC-aligned comparator.

## Recommendation On Code Moves
Code files should stay in place for now.

That recommendation is explicit for the following reasons:
- the active mixed-weak scans still use the older `F_min` background;
- the separate 6-state simple-support background path is active, but still not
  reconnected to the mixed-weak scans;
- the supporting moving-clamp/sliding-clamp comparison path is still a distinct
  diagnostic line;
- the old versus new shallow-comparator situation is still part of the active
  scientific interpretation and should remain easy to audit.

So the safest near-term layering work is documentation-level deduplication,
clearer pointers, and later extraction of shared utilities only when a code move
can be fully verified.

## Suggested Future Safe Dedup Targets
- Extract a small documentation index for the main simple-support pilot chain
  if the number of pilot folders keeps growing.
- Consider a shared helper module for repeated pilot JSON-report formatting only
  if several pilot scripts begin duplicating the same serialization/report code.
- Consider a small wrapper note that lists the canonical simple-support run order:
  baseline task wrappers, local branch-following, high-load extension, and
  later diagnostic pilots.

## Suggested Future Verification Before Any Code Move
If a later refactor does move code, do it only after all of the following are
checked together:
- imports updated;
- task wrappers updated;
- doc references updated;
- `py_compile` passes for changed Python files;
- the main runnable task wrappers still execute their lightweight startup path.
