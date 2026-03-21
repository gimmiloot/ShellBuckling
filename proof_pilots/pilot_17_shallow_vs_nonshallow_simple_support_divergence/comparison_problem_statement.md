# Comparison Problem Statement

## Non-shallow branch used

The non-shallow side is the active 6-state axisymmetric simple-support
background path in:

- `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`

with state

- `y = [T_s, T_sn, M_s, u_r, u_z, varphi]`

and active BC set

- center: `T_sn(x0)=0`, `u_r(x0)=0`, `varphi(x0)=0`;
- right edge: `T_s(1)=0`, `M_s(1)=0`, `u_z(1)=0`.

Low and medium loads are taken from direct continuation on this active path. The
highest load in the present pilot is obtained by the already validated
high-load branch-extension machinery from pilot 12 so that the comparison stays
on the same currently tracked simple-support branch.

## Shallow comparator used

The shallow side is the new simple-support comparator from:

- `proof_pilots/pilot_16_shallow_simple_support_comparator/shallow_simple_support_solver.py`

with state

- `y = [theta0', theta0, Phi0', Phi0]`

and BC set

- `theta0(x0)=0`,
- `Phi0(x0)=0`,
- `Phi0(1)=0`,
- `theta0'(1) + nu*theta0(1)=0`.

This is the strongest currently justified repository-level shallow
simple-support comparator. It is not the old moving-clamp/sliding-clamp shallow
path.

## Variables compared

The compared mapped variables are:

- `theta0`
- `theta0'`
- `Phi0`
- `Phi0'`

## Exact repository-level correspondences

The following mapping formulas are used exactly as implemented in the current
repository comparison code:

- `r = x + u_r`
- `T_theta = nu*T_s + u_r/x`
- `kappa_s = 12(1-nu^2) mu^2 M_s - nu sin(varphi)/r`
- `theta0 = -beta sin(varphi)`
- `theta0' = -beta cos(varphi) kappa_s`
- `Phi0 = gamma x T_s`
- `Phi0' = gamma T_theta`

The edge correspondence `Phi0(1)=0 <-> T_s(1)=0` is exact under this mapping.

## Repository-level inferred correspondences

The following parts remain inferred at the repository level rather than proved
as a full exact reduction:

- `theta0'(1) + nu theta0(1)=0` is used as the shallow-limit image of
  `M_s(1)=0`;
- the shallow center conditions `theta0(x0)=0`, `Phi0(x0)=0` are reduced
  regularity replacements for the full non-shallow center triple;
- `u_z(1)=0` is treated in the shallow problem through the pilot-16 recovered
  displacement normalization rather than as an independent shallow state BC.

## Load ladder

The target load ladder is:

- `0.02`, `0.05`, `0.1`, `0.25`, `0.5`, `0.75`, `1.0`, `1.5`, `2.0`, `3.0`,
  `4.0`, `4.2`, `4.3`, `4.3434` MPa.

If the non-shallow branch cannot supply a requested load reliably within the
bounded run, the pilot reports the strongest feasible subset explicitly rather
than inventing a surrogate branch.
