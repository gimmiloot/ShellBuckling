# Pilot 07. Axisymmetric Simple-Support Background

## Goal
This pilot diagnoses the main current bottleneck for the full
`подвижный шарнир / simple support` branch:
the axisymmetric prebuckling background is not yet available in the repository
as a clean stable runnable solver path.

The purpose here is diagnostic only.
The pilot does not try to close the whole shell theory and it does not try to
promote any mixed-weak candidate load to a final physical `q_cr`.

## Intended Axisymmetric Simple-Support BCs
In the current project sense, the intended full axisymmetric simple-support
background uses

```text
center:  T_sn(x0)=0, u_r(x0)=0, varphi(x0)=0,
edge:    T_s(1)=0, M_s(1)=0, u_z(1)=0.
```

This is the theory-facing simple-support target currently recorded in
`vyvod_uravneniy_updated17.md`, the assumptions file, and the recent boundary
condition audit documents.

## Distinction from Moving Clamp / Sliding Clamp
The supporting moving-clamp / sliding-clamp comparison line uses a different
axisymmetric edge condition set:

```text
center:  T_sn(x0)=0, u_r(x0)=0, varphi(x0)=0,
edge:    T_s(1)=0, u_z(1)=0, varphi(1)=0.
```

So the decisive difference is not in the center conditions, but at the outer
edge:

- moving clamp / sliding clamp keeps `varphi(1)=0`;
- simple support replaces that by `M_s(1)=0`.

## Current Hybrid Fallback Actually Used
The active mixed-weak cores do not use a full simple-support axisymmetric
background.
Both

- `src/shell_buckling/mixed_weak/solver_simple_support_core.py`
- `src/shell_buckling/mixed_weak/solver_patched_core.py`

reuse the same older `F_min` continuation/background family with the reduced
5-state axisymmetric variable set

```text
[T_s0, Q0, M_s0, r0, varphi0]
```

and with the live BC function

```text
T_s0(1)=0, varphi0(1)=0, Q0(x0)=0, r0(x0)=x0, varphi0(x0)=0.
```

This is the hybrid fallback currently feeding the active mixed-weak scans.

## What Is Missing or Failing
The pilot isolates two separate issues.

### 1. Structural mismatch in the active path
The current active background state does not contain `u_z`.
Therefore the intended simple-support condition `u_z(1)=0` cannot even be
imposed directly inside the active 5-state `F_min` background path.

So the active mixed-weak branch is not merely "using the wrong right-edge BC";
it is also using a background state that is too reduced to represent the full
simple-support axisymmetric problem cleanly.

### 2. The closest full-state direct path is only partial
The closest full-state axisymmetric non-shallow equations already present in the
repository live in the supporting comparison modules, with state

```text
[T_s, T_sn, M_s, u_r, u_z, varphi].
```

Using those equations, a direct simple-support `solve_bvp` continuation can be
attempted diagnostically.
Pilot 07 shows that such a run is possible at low and moderate loads, but the
current continuation is not stable through the upper part of the current range:
it loses the branch around the `4.3..4.4 MPa` band by mesh-node blow-up.

## Verification Boundary
This pilot verifies only the current repository-level solver status:

- which axisymmetric background path is actually wired into the active
  mixed-weak scans;
- whether the intended simple-support BC set matches that path;
- whether the closest available full-state direct simple-support solve is
  already stable enough to count as a clean runnable solver path.

This pilot does **not** prove:

- the final article-level simple-support shell background theorem;
- that the failure band near `4.3..4.4 MPa` is a physical limit point;
- the final physical simple-support critical load;
- or the final closed mixed BVP.

## Pilot Outcome
The repository currently does **not** have a clean stable runnable solver path
for the full axisymmetric simple-support background.

What it has instead is:

- a stable active hybrid fallback based on the older `F_min` background;
- and a direct full-state simple-support diagnostic route that is only partial
  and loses continuation before it can be treated as a clean active path.

The smallest justified next step is therefore not a new `q_cr` scan, but a
separate reusable simple-support axisymmetric background module built around the
full-state axisymmetric variables, with fixed-load solves stabilized first and
continuation added only after that.