# Boundary Conditions Summary

| Task | Intended physical interpretation | Essential boundary conditions | Natural / imposed complementary conditions | Main active code path / run script | Current status |
| --- | --- | --- | --- | --- | --- |
| `РїРѕРґРІРёР¶РЅР°СЏ Р·Р°РґРµР»РєР°` | Moving clamp / sliding clamp axisymmetric comparison line | center: `T_sn(x0)=0`, `u_r(x0)=0`, `varphi(x0)=0`; edge: `u_z(1)=0`, `varphi(1)=0` | edge: `T_s(1)=0` | `experiments/supporting/run_supporting_dimensionless_comparison.py`; `experiments/supporting/run_supporting_determinant_comparison.py` | Runnable and useful, but only as a supporting comparison path |
| `РїРѕРґРІРёР¶РЅС‹Р№ С€Р°СЂРЅРёСЂ / simple support` | Hinged / simple-support physical target | center: `T_sn(x0)=0`, `u_r(x0)=0`, `varphi(x0)=0`; edge: `u_z(1)=0` | edge: `T_s(1)=0`, `M_s(1)=0`; clean mixed-weak critical rows: `[u_n(1), varphi(1), T_s(1), S(1), H(1)]` | `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`; `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`; `tasks/run_axisymmetric_simple_support_background.py`; `tasks/run_axisymmetric_simple_support_background_report.py`; `tasks/run_axisymmetric_simple_support_local_branch_following.py`; `tasks/run_full_simple_support_critical_search.py` | Separate honest full-state background path and separate clean full critical-search program now exist; preserved hybrid scan tasks remain available separately |

## Important note about the preserved hybrid mixed-weak scans

The older hybrid mixed-weak task wrappers are still not themselves the clean
full `simple support` program:

- `tasks/run_mixed_weak_boundary_matrix_scan.py` uses the older `F_min`
  background and a broad-scan right-boundary row set
  `[u_n(1), M_s(1), T_s(1), S(1), H(1)]`.
- `tasks/run_mixed_weak_targeted_scan.py` uses the same older `F_min`
  background but a patched right-boundary row set
  `[u_n(1), varphi(1), T_s(1), S(1), H(1)]`.
- `tasks/run_full_simple_support_critical_search.py` is the new standalone
  clean full simple-support critical-search entry point that uses the honest
  full-state background plus the patched critical row set.

So the older two wrappers remain **simple-support-oriented mixed-weak
boundary-matrix testbenches**, while the new runner is the preferred clean
full simple-support critical-search program.
