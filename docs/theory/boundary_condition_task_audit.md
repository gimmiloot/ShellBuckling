# Boundary-Condition Task Audit

## Purpose
This note separates the boundary-condition tasks that are easy to mix up in the
repository:

1. `РїРѕРґРІРёР¶РЅР°СЏ Р·Р°РґРµР»РєР°` / moving clamp / sliding clamp
2. preserved hybrid mixed-weak scan/testbench paths
3. `РїРѕРґРІРёР¶РЅС‹Р№ С€Р°СЂРЅРёСЂ` / hinged / `simple support`

The goal is to state which runnable code paths belong to which task and to make
explicit where the clean full simple-support critical-search program now lives.

## Executive Result
The current checkout now contains a role-explicit separation:

- a supporting axisymmetric comparison path for the moving-clamp/sliding-clamp
  side;
- preserved hybrid mixed-weak scan paths that are simple-support-oriented at the
  boundary-matrix level but still reuse the older `F_min` background;
- a separate honest full-state axisymmetric simple-support background path;
- a separate standalone clean full simple-support critical-search program that
  reconnects the patched mixed-weak critical layer to that honest background.

## Runnable Scripts By Task

### 1. Moving clamp / sliding clamp side (`РїРѕРґРІРёР¶РЅР°СЏ Р·Р°РґРµР»РєР°`)

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

- This is the clearest runnable axisymmetric BC path in the checkout for the
  moving-clamp / sliding-clamp side.
- It is supporting comparison tooling, not the main mixed-weak criterion path.

### 2. Preserved hybrid mixed-weak scan/testbench path

Runnable scripts:

- `tasks/run_mixed_weak_boundary_matrix_scan.py`
- `tasks/run_mixed_weak_targeted_scan.py`

Code path:

- `src/shell_buckling/mixed_weak/solver_simple_support_core.py`
- `src/shell_buckling/mixed_weak/boundary_matrix_scan.py`
- `src/shell_buckling/mixed_weak/solver_patched_core.py`
- `src/shell_buckling/mixed_weak/boundary_matrix_targeted_scan.py`

Shared axisymmetric background actually used there:

- center/background BCs: `Q_0(x0)=0`, `r_0(x0)=x0`, `varphi_0(x0)=0`
- edge/background BCs: `T_{s0}(1)=0`, `varphi_0(1)=0`

Actual right-boundary matrix rows in code:

- broad scan: `[u_n(1), M_s(1), T_s(1), S(1), H(1)]`
- targeted patched scan: `[u_n(1), varphi(1), T_s(1), S(1), H(1)]`

Audit interpretation:

- This remains an **exploratory hybrid testbench path**.
- It should not be relabeled as a finalized physical simple-support solver.
- It is preserved for comparison and diagnostics.

### 3. Full hinged / simple-support task (`РїРѕРґРІРёР¶РЅС‹Р№ С€Р°СЂРЅРёСЂ / simple support`)

Written down in theory-facing documents:

- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/assumptions/assumptions.md`

BCs written down there for the full axisymmetric problem:

- center: `T_sn(x0)=0`, `u_r(x0)=0`, `varphi(x0)=0`
- edge: `T_s(1)=0`, `M_s(1)=0`, `u_z(1)=0`

Repository status:

- the honest full-state background path exists in
  `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`;
- the standalone clean full simple-support critical-search program now exists in
  `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`, with
  runnable entry point `tasks/run_full_simple_support_critical_search.py`;
- this new clean path uses the honest background BC set together with the
  patched critical-layer boundary rows `[u_n(1), varphi(1), T_s(1), S(1), H(1)]`;
- the older hybrid mixed-weak scan tasks remain preserved and separate from this
  clean full simple-support program.

## Audit Conclusion
Current separation status: **cleaner and now role-explicit**.

The intended reading is now:

- supporting axisymmetric comparison scripts -> moving-clamp / sliding-clamp side;
- preserved mixed-weak scan scripts -> hybrid simple-support-oriented testbench,
  still using the older `F_min` background;
- full `simple support` axisymmetric background task -> separate honest full-state
  background path;
- full `simple support` critical-load search -> separate standalone clean program
  that uses the honest full-state background together with the patched mixed-weak
  critical boundary rows.
