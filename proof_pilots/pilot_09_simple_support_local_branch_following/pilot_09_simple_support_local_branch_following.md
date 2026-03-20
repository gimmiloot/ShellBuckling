# Pilot 09. Simple-Support Local Branch Following

## Goal
This pilot adds the next numerical stabilization step for the separate
6-state axisymmetric simple-support background solver.

The goal is not to change the model, the BC set, or the mixed-weak scans.
The goal is only to improve continuation through the difficult
`4.32..4.34 MPa` band by using a dedicated local branch-following helper.

## Numerical Changes Introduced
The new helper keeps the same 6-state equations and the same simple-support
BC set, but changes the continuation workflow locally.

1. It first builds a relaxed uniform-mesh anchor schedule up to the last load
   that was already known to converge reproducibly in pilot 08.
2. It then switches to a separate local continuation stage on a
   right-edge-focused mesh.
3. In that local stage it reuses the last converged solution directly and,
   once two local points are available, adds a secant-style predictor.
4. Each local load is attempted with a stricter local configuration first.
   Only if that fails is a looser local configuration tried.
5. The local stage also allows larger `max_nodes` than the baseline path.

This is a numerical stabilization path only. It is not relabeled as the
final production simple-support solver.

## Load Band Tested
The anchor schedule used the loads

```text
4.3000, 4.3250, 4.3275, 4.3280, 4.3290, 4.3300, 4.3320, 4.3350 MPa.
```

The dedicated local branch-following stage then tested

```text
4.3350, 4.3360, 4.3370, 4.3380, 4.3390, 4.3400,
4.3410, 4.3420, 4.3430, 4.3440 MPa.
```

## Actual Outcome
Under the new helper:

- the local branch now converges through `4.3430 MPa`;
- the first failed load is `4.3440 MPa`;
- so the ceiling moved upward relative to the pilot 08 local ceiling near
  `4.335 MPa`.

The successful local steps use:

- `previous_solution` for the first local move from `4.3350` to `4.3360`,
- then predominantly the `secant_predictor` seed,
- with the stricter local configuration through `4.3380 MPa`,
- and the looser local configuration from `4.3390 MPa` onward.

## Current Interpretation
The evidence still points to a mainly numerical bottleneck.

Reasons:

- the BC set was not changed;
- the equations were not changed;
- the ceiling moved upward by changing only continuation / mesh / tolerance
  strategy;
- the first new failure still appears as mesh-node exhaustion rather than as
  a detected BC inconsistency.

## What This Pilot Does Not Prove
This pilot does **not** prove:

- the final article-level simple-support background theorem,
- that the remaining ceiling is a physical limit point,
- the final mixed-weak critical problem,
- or the final physical simple-support critical load.

## Next Bottleneck
After this change, the next bottleneck is still local branch following near
the right edge. The immediate next step is to improve that local stage
further, not to reconnect the mixed-weak scans yet.
