# Pilot 22 Exact-Load Shallow vs Current Simple-Support Comparison

## Scope

- old shallow system: `proof_pilots/pilot_16_shallow_simple_support_comparator/shallow_simple_support_solver.py`
- current mapped quantities: `src/shell_buckling/supporting/determinant_criterion_comparison.py::arrays_nepol_sin`
- exact comparison loads: `4.0`, `7.0`, `10.0 MPa`
- equations unchanged, simple-support BCs unchanged, mixed-weak scans untouched

## Mapping Used

- old shallow arrays: `arrays_shallow(sol, x)` with `theta0=y[1]`, `theta0'=y[0]`, `Phi0=y[3]`, `Phi0'=y[2]`
- mapped current arrays: `arrays_nepol_sin(sol, x)`
- `theta0 = -beta * sin(phi)`
- `theta0' = -beta * cos(phi) * kappa_s`
- `Phi0 = gamma * x * T_s`
- `Phi0' = gamma * T_theta`
- `T_theta = nu * T_s + u_r / x`
- `kappa_s = 12 * (1 - nu^2) * M_s * mu^2 - nu * sin(phi) / r`, `r = x + u_r`

## Load Summary

| Load MPa | Old shallow | Current 6-state | Figure | Interpretation |
| --- | --- | --- | --- | --- |
| 4.0 | exact pilot-16 shallow continuation solve | exact low-load 6-state continuation solve | `current_vs_shallow_exact_4.0_mpa.png` | visible but still moderate divergence |
| 7.0 | exact pilot-16 shallow continuation solve | exact retained pilot-21 fast-run checkpoint | `current_vs_shallow_exact_7.0_mpa.png` | clear visible divergence |
| 10.0 | exact pilot-16 shallow continuation solve | exact retained pilot-21 fast-run checkpoint | `current_vs_shallow_exact_10.0_mpa.png` | clear visible divergence |

## Operational Outcome

- current fast path highest stored load: `10.0000 MPa`
- current fast path bounded first failure: `None`
- shallow path last success in this pilot: `10.0`
- shallow path first failure in this pilot: `None`

## Notes

- `4.0 MPa` on the current 6-state side is an exact low-load continuation solve, not an interpolated fast-run checkpoint.
- `7.0` and `10.0 MPa` on the current 6-state side are exact retained pilot-21 fast-run checkpoints.
- The status language above the audited `4.3800 MPa` ceiling remains operational only; nothing here promotes `7..10 MPa` to a new audited ceiling.
