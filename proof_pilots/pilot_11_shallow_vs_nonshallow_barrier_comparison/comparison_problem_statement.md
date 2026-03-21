# Comparison Problem Statement

## Non-Shallow Branch Used
The non-shallow side of the comparison uses the current active 6-state
axisymmetric simple-support background path

```text
Y = (T_s, T_sn, M_s, u_r, u_z, varphi)
```

from

- `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`

with BC set

```text
center: T_sn(x0)=0, u_r(x0)=0, varphi(x0)=0,
edge:   T_s(1)=0, M_s(1)=0, u_z(1)=0.
```

The branch is built using the same anchor + rescue-local continuation workflow
validated in pilot 10:

- anchor schedule to `4.335 MPa`,
- rescue-local bootstrap through `4.343 MPa`,
- finer rescue-local refinement above that ceiling.

So this pilot does not invent a new non-shallow branch.

## Shallow Comparison Path Used
The shallow side uses the repository's existing supporting shallow path from

- `src/shell_buckling/supporting/dimensionless_background_comparison.py`
- `src/shell_buckling/supporting/determinant_criterion_comparison.py`

with state

```text
Y_sh = (theta0', theta0, Phi0', Phi0)
```

and live BCs

```text
theta0(x0)=0, theta0(1)=0, Phi0(x0)=0, Phi0(1)=0.
```

This is the current repository shallow comparison path.
It is useful diagnostically, but it is not claimed here to be a separately
closed theorem-level simple-support rebuild of the full 6-state problem.

## Mapping Formulas Used
The pilot uses the existing repository mapping formulas from the supporting
comparison scripts.

With

```text
r        = x + u_r,
T_theta  = nu T_s + u_r / x,
kappa_s  = 12 (1 - nu^2) mu^2 M_s - nu sin(varphi) / r,
beta     = sqrt(12 (1 - nu^2)) mu,
gamma    = 12 (1 - nu^2) mu^2,
```

the mapped shallow-like variables are

```text
theta0   = -beta sin(varphi),
theta0'  = -beta cos(varphi) kappa_s,
Phi0     = gamma x T_s,
Phi0'    = gamma T_theta.
```

These are the formulas already used in:

- `compute_branchA_diagnostics(...)` in
  `src/shell_buckling/supporting/dimensionless_background_comparison.py`
- `arrays_nepol_sin(...)` in
  `src/shell_buckling/supporting/determinant_criterion_comparison.py`

## Loads Compared In The Bounded Run
The actual bounded pilot-11 run compared:

1. `4.3400 MPa`
   matched-load comparison below the barrier neighborhood.
2. `4.3430 MPa`
   matched-load comparison near the earlier local ceiling.
3. `4.3433 MPa`
   matched-load comparison near the pilot-10 refined ceiling.
4. `4.3434 MPa`
   barrier-adjacent matched-load comparison.
   In this pilot-11 run the non-shallow branch reached `4.3434 MPa` after two
   mesh-pressure failures on raw-mesh seeds and then a success with the
   `secant_profile_mesh` predictor.

So the originally planned `4.3434 MPa` failed-target precursor comparison was
not needed in this run.
The wider barrier neighborhood is still taken to be about `4.3434..4.3440 MPa`,
but a fresh `4.3440 MPa` precursor comparison is outside the bounded scope of
this specific pilot-11 execution.
