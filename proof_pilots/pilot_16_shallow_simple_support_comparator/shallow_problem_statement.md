# Shallow Simple-Support Problem Statement

## Purpose
This note states the compact repository-level shallow simple-support problem
that should be used as the shallow comparator for the active 6-state
non-shallow simple-support branch.

## 1. Shallow Variables

The shallow state is kept in the same reduced variables already used by the
existing shallow comparator:

```text
Y_sh = (theta0', theta0, Phi0', Phi0).
```

So the governing shallow ODE system is the same 4-state shallow system already
present in the repository.

Written componentwise,

```text
(theta0')' = -theta0'/x + theta0/x^2 + Phi0 * theta0 / x
             + q * x * beta^3 * mu / (2 E),
theta0'    = d(theta0)/dx,
(Phi0')'   = -Phi0'/x + Phi0/x^2 - theta0^2 / (2 x),
Phi0'      = d(Phi0)/dx.
```

## 2. Non-Shallow Simple-Support Target

The active 6-state non-shallow simple-support background problem uses

```text
Y = (T_s, T_sn, M_s, u_r, u_z, varphi)
```

with BC set

```text
center: T_sn(x0)=0, u_r(x0)=0, varphi(x0)=0,
edge:   T_s(1)=0, M_s(1)=0, u_z(1)=0.
```

The shallow comparator should therefore match that support type, not the older
moving-clamp/sliding-clamp shallow path.

## 3. Mapping Relations Used

The repository already uses the exact shell-to-shallow-like mappings

```text
theta0   = -beta sin(varphi),
theta0'  = -beta cos(varphi) kappa_s,
Phi0     = gamma x T_s,
```

with

```text
kappa_s = gamma M_s - nu sin(varphi)/r,
gamma   = 12 (1 - nu^2) mu^2,
beta    = sqrt(gamma).
```

From these formulas one gets the exact identity

```text
theta0' + nu cos(varphi) theta0 / r = -beta gamma cos(varphi) M_s.
```

This identity is exact at the repository mapping level.

## 4. Proposed Shallow Simple-Support BC Set

The proposed reduced shallow BC vector is

```text
theta0(x0)=0,
Phi0(x0)=0,
Phi0(1)=0,
theta0'(1) + nu theta0(1) = 0.
```

## 5. Why These BCs

### Center BCs

The center conditions

```text
theta0(x0)=0,
Phi0(x0)=0
```

are the standard reduced regularity conditions already used by the repository's
shallow path.
They are not a one-to-one exact rewrite of the full 6-state center BC triple,
but they are the compact reduced-variable regularity conditions available in
this 4-state shallow formulation.

### Edge force BC

The edge condition

```text
Phi0(1)=0
```

is exact under the current mapping

```text
Phi0 = gamma x T_s,
```

so at `x=1` it is exactly equivalent to

```text
T_s(1)=0.
```

### Edge moment BC

The full simple-support problem requires

```text
M_s(1)=0.
```

Using the exact identity

```text
theta0' + nu cos(varphi) theta0 / r = -beta gamma cos(varphi) M_s,
```

and then applying the shallow-limit reduction

```text
cos(varphi) ~ 1,
r ~ x,
```

gives the shallow relation

```text
theta0' + (nu/x) theta0 ~ -beta gamma M_s.
```

Therefore the moment-free edge condition becomes

```text
theta0'(1) + nu theta0(1) = 0.
```

This is the key BC that distinguishes the new shallow simple-support comparator
from the older moving-clamp/sliding-clamp shallow path, which instead imposed
`theta0(1)=0`.

## 6. What Happens to `u_z(1)=0`

The reduced 4-state shallow background system does not carry `u_z` as an
independent state variable.
So `u_z(1)=0` does not appear as an additional BVP condition in the 4-state
system.

Instead, after the shallow solution is found, one can reconstruct a shallow
transverse-displacement profile from the small-angle relation

```text
u_z'(x) ~ (mu / beta) theta0(x),
```

and then fix the additive constant by choosing

```text
u_z(1)=0.
```

So in the reduced shallow comparator, `u_z(1)=0` is a post-solve normalization,
not an independent BC consuming one of the four BVP slots.

## 7. Established vs Inferred

### Exact inside the repository mapping

- `Phi0(1)=0 <-> T_s(1)=0`.
- `theta0' + nu cos(varphi) theta0 / r = -beta gamma cos(varphi) M_s`.

### Inferred by shallow reduction

- `theta0'(1) + nu theta0(1) = 0` as the shallow simple-support translation of
  `M_s(1)=0`.
- `u_z'(x) ~ (mu/beta) theta0(x)` and the post-solve normalization
  `u_z(1)=0`.

This is the strongest compact repository-level shallow simple-support statement
currently justified for a fair comparator.
