# Barrier Problem Statement

## Active branch near the ceiling

The active branch is the separate 6-state axisymmetric simple-support
background path in
`src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py` with
state

```text
(T_s, T_sn, M_s, u_r, u_z, varphi).
```

The active BC set is

```text
center: T_sn(x0)=0, u_r(x0)=0, varphi(x0)=0,
edge:   T_s(1)=0, M_s(1)=0, u_z(1)=0.
```

The present high-load branch status is:

- reproducible anchor: `4.3434 MPa`;
- first persistent staged failure: `4.3440 MPa`.

## Active equations

With

```text
r = x + u_r,
etheta = u_r / x,
es = (1-nu^2) T_s - nu etheta,
T_theta = nu T_s + etheta,
kappa_s = 12 (1-nu^2) mu^2 M_s - nu sin(varphi) / r,
M_theta = nu M_s + sin(varphi) / (12 mu^2 r),
qbar = q a / (E h),
```

the active ODE system is

```text
T_s'   = -(T_s / r) + (cos(varphi) T_theta) / r - kappa_s T_sn,
T_sn'  = -(T_sn / r) + (sin(varphi) T_theta) / r + kappa_s T_s - qbar,
M_s'   = -(M_s / r) + (cos(varphi) M_theta) / r + T_sn,
u_r'   = (1 + es) cos(varphi) - 1,
u_z'   = -mu (1 + es) sin(varphi),
varphi'= kappa_s.
```

## Current numerical symptoms

The branch diagnostics near the ceiling are currently very specific:

- `4.3434 MPa` is reproducible on the staged secant/profile-mesh strategy;
- `4.3440 MPa` keeps failing by `maximum number of mesh nodes is exceeded`;
- BC residuals at the failed step stay tiny, around `7.5e-17` in the fresh
  pilot-18 cache build;
- node concentration at the failed step is extreme:
  about `99.1%` of nodes lie above `x=0.99`, about `98.2%` above `x=0.995`;
- the strongest failed-step gradients remain
  `u_z` near `x~0.99967`, then `varphi` near `x~0.93466`.

So the observed obstruction is a right-edge/near-edge stiffness pattern, not a
BC breakdown.

## Updated shallow/non-shallow interpretation

The current shallow/non-shallow interpretation must use the corrected BC story:

- pilot 15 showed that the old shallow comparator was BC-mismatched for simple
  support;
- pilot 16 built the strongest currently justified shallow simple-support
  comparator;
- pilot 17 repeated the divergence sweep in that corrected BC setting.

The corrected simple-support comparison shows:

- the mismatch is small at low load;
- the first single-variable clear signal appears at `2.0 MPa` in `Phi0'`;
- the mismatch becomes clearly overall visible at `3.0 MPa`;
- it grows with load;
- it stays smooth through the available high-load range up to `4.3434 MPa`.

So the analytic diagnosis here is now about the right-edge balance on an
already measurably non-shallow branch, not about a sudden new branch split that
appears only at `4.34 MPa`.
