# Boundary-Condition Task Audit

## Purpose
This note separates the boundary-condition tasks that are currently easy to mix
up in the repository:

1. `подвижная заделка` / moving clamp / sliding clamp
2. `подвижный шарнир` / hinged / `simple support`

The goal is to state which runnable code paths belong to which task, where the
current mixed-weak scan workflow is still hybrid, and where the documentation
was previously ambiguous.

## Executive Result
The repository now has a cleaner separation than before, but it is still not a
fully closed two-path story.

What the current checkout now has is:

- a supporting axisymmetric comparison path whose written BC set matches the
  moving-clamp / sliding-clamp side;
- an active mixed-weak scan path that is `simple-support`-oriented at the
  boundary-matrix level but still reuses the older `F_min` background;
- a separate active full-state axisymmetric simple-support background path,
  which is runnable and reaches `4.30 MPa` in the current implementation but
  still fails near `4.33 MPa` and is not yet connected to the mixed-weak scans.

## Runnable Scripts by Task

### 1. Moving clamp / sliding clamp side (`подвижная заделка`)

Runnable scripts:

- `experiments/supporting/run_supporting_dimensionless_comparison.py`
- `experiments/supporting/run_supporting_determinant_comparison.py`

Code path:

- `src/shell_buckling/supporting/dimensionless_background_comparison.py`
- `src/shell_buckling/supporting/determinant_criterion_comparison.py`

BCs written down in code:

- center: `T_sn(x0)=0`, `u_r(x0)=0`, `varphi(x0)=0`
- edge: `T_s(1)=0`, `u_z(1)=0`, `varphi(1)=0`

Audit interpretation:

- This is the clearest runnable axisymmetric BC path in the checkout that
  matches the moving-clamp / sliding-clamp side of the project comparison.
- It is supporting comparison tooling, not the main mixed-weak criterion path.

### 2. Active mixed-weak scan/testbench path

Runnable scripts:

- `tasks/run_mixed_weak_boundary_matrix_scan.py`
- `tasks/run_mixed_weak_targeted_scan.py`

Code path:

- `src/shell_buckling/mixed_weak/solver_simple_support_core.py`
- `src/shell_buckling/mixed_weak/boundary_matrix_scan.py`
- `src/shell_buckling/mixed_weak/solver_patched_core.py`
- `src/shell_buckling/mixed_weak/boundary_matrix_targeted_scan.py`

Shared axisymmetric background actually used in both mixed-weak cores:

- center/background BCs: `Q_0(x0)=0`, `r_0(x0)=x0`, `varphi_0(x0)=0`
- edge/background BCs: `T_{s0}(1)=0`, `varphi_0(1)=0`

This means the active mixed-weak scans still reuse the older `F_min`
axisymmetric background line rather than a separately stabilized full
`simple support` background solver.

#### Broad scan variant

Runnable script:

- `tasks/run_mixed_weak_boundary_matrix_scan.py`

Actual right-boundary matrix rows in code:

- `[u_n(1), M_s(1), T_s(1), S(1), H(1)]`

Documentation issue:

- the core file still contains an earlier nearby comment about
  `u_n(1), varphi(1), T_s(1), S(1), H(1)`, but the actual `bvec` used by the
  broad scan is the `M_s(1)` variant;
- `boundary_matrix_scan.py` prints row labels with `M_s(1)`.

#### Targeted patched variant

Runnable script:

- `tasks/run_mixed_weak_targeted_scan.py`

Actual right-boundary matrix rows in code:

- `[u_n(1), varphi(1), T_s(1), S(1), H(1)]`

Documentation issue:

- this matches the pilot-backed mixed-weak testbench boundary logic, but it is
  still paired with the older `F_min` background rather than a full
  `simple support` axisymmetric background solver.

Audit interpretation of the active mixed-weak path:

- It is an **exploratory hybrid testbench path**.
- It should not be relabeled as a finalized physical `simple support` solver.
- It is also not identical to the moving-clamp comparison path, because its
  right-boundary criterion is different.

### 3. Full hinged / simple-support task (`подвижный шарнир / simple support`)

Written down in theory-facing documents:

- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/assumptions/assumptions.md`

BCs written down there for the full axisymmetric problem:

- center: `T_sn(x0)=0`, `u_r(x0)=0`, `varphi(x0)=0`
- edge: `T_s(1)=0`, `M_s(1)=0`, `u_z(1)=0`

Repository status:

- this task is documented as the intended full `simple support` background
  problem;
- a separate active full-state background path now exists in
  `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`;
- that path is runnable but not yet closed: in the current implementation it
  reaches `4.30 MPa` and fails near `4.33 MPa`, and it is not yet connected to
  the active mixed-weak scans.

## Where the BCs Are Currently Stated

### In code

- Moving-clamp/sliding-clamp-side BCs appear in the supporting axisymmetric
  comparison modules.
- The shared `F_min` background BCs appear in both active mixed-weak cores.
- The broad and targeted mixed-weak scans use different second right-boundary
  rows: `M_s(1)` in the broad scan, `varphi(1)` in the targeted patched scan.

### In `README.md`

Before this audit, the active mixed-weak scans were described simply as the
`simple-support branch`, without explaining that:

- they still reuse the older `F_min` background;
- the broad and targeted scan variants do not use the same right-boundary row
  set;
- a clean full `simple support` background program is not yet present.

### In `docs/project_map.md`

Before this audit, the project map called the active mixed-weak core the
`simple-support line`, but it did not separate:

- the supporting moving-clamp/sliding-clamp axisymmetric comparison path,
- the hybrid mixed-weak scan/testbench path,
- the still-missing full simple-support background program.

### In `docs/theory/current_mixed_weak_theory_note.tex`

The theory note correctly states the pilot-backed mixed-weak testbench boundary
logic

- `u_n(1)=0`, `varphi(1)=0`
- natural `T_s(1)=0`, `S(1)=0`, `H(1)=0`

but by itself it did not make sufficiently explicit that this is not yet the
same thing as the full axisymmetric `simple support` background task.

### In `docs/assumptions/assumptions.md`

The assumptions file already records that:

- the earlier `simple support` interpretation was too strong;
- a full `simple support` background requires `T_s(1)=0`, `M_s(1)=0`, `u_z(1)=0`;
- the main open bottleneck is the axisymmetric `simple support` background.

## Where the Documentation Was Incomplete or Ambiguous

The pre-audit ambiguities were:

- `solver_simple_support_core.py` and README language suggested a clean
  `simple support` path even though the active scans still reuse the older
  `F_min` background;
- the broad and targeted mixed-weak scan variants were not documented as using
  different second right-boundary rows;
- the repository did not yet have one compact place that separated moving clamp,
  full `simple support`, and the current hybrid mixed-weak testbench.

## Audit Conclusion

Current separation status: **not clean enough before documentation repair**.

After the documentation updates linked to this audit, the intended reading is:

- supporting axisymmetric comparison scripts -> moving-clamp / sliding-clamp side;
- active mixed-weak scan scripts -> hybrid simple-support-oriented testbench,
  still using the older `F_min` background;
- full `simple support` axisymmetric background task -> separate active full-state`r`n  background path now exists, but it is still only partially stabilized and is`r`n  not yet the background used by the active mixed-weak scans.