# Problem Audit: 6-State Simple-Support Background

## Implemented State Vector
The active full-state simple-support background module
`src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`
uses the state labels

```text
[T_s, T_sn, M_s, u_r, u_z, varphi].
```

In code, the local variable names are

```text
Ts, Tsn, Ms, ur, uz, phi.
```

so `phi` in code corresponds to repository notation `varphi`.

## Implemented First-Order Equations
With

```text
r      = x + u_r,
e_theta = u_r / x,
e_s     = (1 - nu^2) T_s - nu e_theta,
T_theta = nu T_s + e_theta,
kappa_s = 12 (1 - nu^2) mu^2 M_s - nu sin(varphi) / r,
M_theta = nu M_s + sin(varphi) / (12 mu^2 r),
qbar    = q a / (E h),
```

the implemented ODE is

```text
T_s'   = -(T_s / r) + cos(varphi) T_theta / r - kappa_s T_sn,
T_sn'  = -(T_sn / r) + sin(varphi) T_theta / r + kappa_s T_s - qbar,
M_s'   = -(M_s / r) + cos(varphi) M_theta / r + T_sn,
u_r'   = (1 + e_s) cos(varphi) - 1,
u_z'   = -mu (1 + e_s) sin(varphi),
varphi'= kappa_s.
```

At repository level this matches the supporting 6-state non-shallow
equation function `axisym_nepol(...)` in
`src/shell_buckling/supporting/determinant_criterion_comparison.py`.
Pilot 08 checks that match numerically.

## Implemented Boundary Conditions
The live BC function returns

```text
[yb[0], yb[2], yb[4], ya[1], ya[3], ya[5]],
```

i.e.

```text
edge:   T_s(1)=0, M_s(1)=0, u_z(1)=0,
center: T_sn(x0)=0, u_r(x0)=0, varphi(x0)=0.
```

This is exactly the intended theory-facing simple-support BC statement.
No condition is silently replaced by `varphi(1)=0` inside the 6-state
module.

## Essential / Natural Reading at Repository Level
The repository-level simple-support reading remains:

- essential side: `u_r(x0)=0`, `varphi(x0)=0`, `u_z(1)=0`;
- complementary side: `T_sn(x0)=0`, `T_s(1)=0`, `M_s(1)=0`.

Pilot 08 does not try to elevate this reading to a full article-level
weak-form theorem; it only checks that the implemented 6-state BC set is
consistent with the current project statement.

## Structural Consistency of the BVP
The implemented background problem is structurally square:

- 6 first-order ODEs,
- 6 scalar BC residuals.

So there is no immediate over-determination or under-determination at the
level of BC count.

## Relation to the Older 5-State F_min Fallback
The older background path still used by the active mixed-weak scans has
state

```text
[T_s0, Q0, M_s0, r0, varphi0]
```

and BCs

```text
T_s0(1)=0, varphi0(1)=0, Q0(x0)=0, r0(x0)=x0, varphi0(x0)=0.
```

That 5-state path is different in both state content and right-edge BCs,
and should not be confused with the present 6-state simple-support BVP.

## Repository-Level Audit Conclusion
At the level of implementation structure, the 6-state module currently
looks internally consistent:

- the state vector is the intended one,
- the equations match the current supporting 6-state equations,
- the BC function matches the intended simple-support BC set,
- and the problem is square.

So the present `4.30..4.35 MPa` ceiling is not, at repository level,
explained by an obvious BC-count mismatch or a silent BC swap.
