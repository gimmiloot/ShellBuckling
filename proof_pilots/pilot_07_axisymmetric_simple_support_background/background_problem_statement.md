# Axisymmetric Simple-Support Background: Repository-Level Problem Statement

## Intended Problem
The current theory-facing simple-support background problem is the non-shallow
axisymmetric prebuckling problem with state

```text
Y(x) = (T_s, T_sn, M_s, u_r, u_z, varphi).
```

At repository level, this is the closest currently available variable set that
can express the intended simple-support BCs directly.

## Boundary Conditions
The intended current project-level BC set is

```text
center x=x0:  T_sn(x0)=0, u_r(x0)=0, varphi(x0)=0,
edge   x=1:   T_s(1)=0, M_s(1)=0, u_z(1)=0.
```

## Essential vs Natural Reading
Within the current repository discussion, the conditions are read as follows.

Essential:

- `u_r(x0)=0`,
- `varphi(x0)=0`,
- `u_z(1)=0`.

Natural / complementary:

- `T_sn(x0)=0`,
- `T_s(1)=0`,
- `M_s(1)=0`.

This is a repository-level BC reading only.
It is not claimed here as a final article-level proof of the full weak-form
translation for the axisymmetric simple-support shell problem.

## Closest Current Code Paths
There are two nearby but different code paths in the repository.

### A. Closest full-state axisymmetric path

- `src/shell_buckling/supporting/dimensionless_background_comparison.py`
- `src/shell_buckling/supporting/determinant_criterion_comparison.py`

These use the full 6-state axisymmetric variable set

```text
[T_s, T_sn, M_s, u_r, u_z, varphi]
```

but their live boundary conditions correspond to the moving-clamp /
sliding-clamp comparison line, not to full simple support.

### B. Active mixed-weak background path

- `src/shell_buckling/mixed_weak/solver_simple_support_core.py`
- `src/shell_buckling/mixed_weak/solver_patched_core.py`

These use the reduced 5-state `F_min` background state

```text
[T_s0, Q0, M_s0, r0, varphi0]
```

with live BCs

```text
T_s0(1)=0, varphi0(1)=0, Q0(x0)=0, r0(x0)=x0, varphi0(x0)=0.
```

## Where the Mismatch Appears
The mismatch with the current active workflow appears at three levels.

1. State mismatch:
   the active 5-state background does not carry `u_z`, so it cannot directly
   impose `u_z(1)=0`.

2. BC mismatch:
   the active path imposes `varphi0(1)=0`, whereas the intended simple-support
   background uses `M_s(1)=0`.

3. Workflow mismatch:
   the active mixed-weak scans are therefore seeded from the older `F_min`
   background family rather than from a dedicated full simple-support
   axisymmetric continuation.

## Current Repository Conclusion
The full axisymmetric simple-support background is not yet present as a clean
active solver path in the current checkout.
The closest full-state direct route is diagnostic only at present, while the
actual active path remains the hybrid `F_min` fallback.