# Boundary Conditions Summary

| Task | Intended physical interpretation | Essential boundary conditions | Natural / imposed complementary conditions | Main active code path / run script | Current status |
| --- | --- | --- | --- | --- | --- |
| `подвижная заделка` | Moving clamp / sliding clamp axisymmetric comparison line | center: `T_sn(x0)=0`, `u_r(x0)=0`, `varphi(x0)=0`; edge: `u_z(1)=0`, `varphi(1)=0` | edge: `T_s(1)=0` | `experiments/supporting/run_supporting_dimensionless_comparison.py`; `experiments/supporting/run_supporting_determinant_comparison.py` | Runnable and useful, but only as a supporting comparison path |
| `подвижный шарнир / simple support` | Hinged / simple-support physical target | center: `T_sn(x0)=0`, `u_r(x0)=0`, `varphi(x0)=0`; edge: `u_z(1)=0` | edge: `T_s(1)=0`, `M_s(1)=0` | `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`; `tasks/run_axisymmetric_simple_support_background.py`; `tasks/run_axisymmetric_simple_support_background_report.py` | Separate active full-state background path now exists; default fixed-load and seeded continuation schedules reach `4.30 MPa` and fail near `4.33 MPa`; not yet connected to the active mixed-weak scans |

## Important note about the current mixed-weak scans

The two active mixed-weak task wrappers are not themselves a clean full
`simple support` background program:

- `tasks/run_mixed_weak_boundary_matrix_scan.py` uses the older `F_min`
  background and a broad-scan right-boundary row set
  `[u_n(1), M_s(1), T_s(1), S(1), H(1)]`.
- `tasks/run_mixed_weak_targeted_scan.py` uses the same older `F_min`
  background but a patched right-boundary row set
  `[u_n(1), varphi(1), T_s(1), S(1), H(1)]`.

They should therefore be read as **simple-support-oriented mixed-weak
boundary-matrix testbenches**, not as the final fully separated hinged/simple-
support solver.