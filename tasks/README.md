# Tasks

`tasks/` is the launcher layer of the repository.

Intended role:

- keep user-facing run entry points here;
- keep reusable solver logic in `src/shell_buckling/...`;
- keep pilot-specific reusable helpers inside the relevant pilot until they are
  safely extracted.

Current status:

- the boundary-matrix and background runners are already thin launchers;
- the three clean full simple-support criterion runners remain somewhat thicker
  because they still carry task-specific orchestration and output bookkeeping;
- those larger runners are preserved as public task entry points in this phase,
  with no behavior change.

When adding a new task:

- prefer a thin launcher in `tasks/`;
- send reusable logic to `src/` or to a well-scoped pilot module;
- write outputs to the appropriate `output/` location instead of beside the
  launcher.
