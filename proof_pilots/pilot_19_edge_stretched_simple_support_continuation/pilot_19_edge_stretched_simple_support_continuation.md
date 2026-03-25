# Pilot 19. Edge-Stretched Simple-Support Continuation

## Goal
This pilot tests whether the current simple-support continuation ceiling can be
moved upward by changing only the numerical representation near the right edge
`x = 1`.

The target is narrow and explicit:

- keep the real current 6-state simple-support branch;
- keep the same equations;
- keep the same simple-support BC set;
- improve right-edge-layer resolution;
- check whether the present ceiling can be pushed materially beyond the current
  `4.3440 MPa` failure band.

## Scientific Scope
This pilot is **not** a change of model.

It does **not**:

- replace the active 6-state equations;
- alter the simple-support boundary conditions;
- reconnect the mixed-weak scans;
- claim a final physical simple-support critical load;
- claim reachability to `10 MPa`.

It changes only the numerical representation used for continuation near the
right edge.

## Current Interpretation Entering Pilot 19
The pilot starts from the repository-level status sharpened by pilots 08, 09,
12, 17, and 18:

- `4.3434 MPa` is a reproducible anchor on the active 6-state branch;
- `4.3440 MPa` is the first persistent failure of the current documented path;
- the bottleneck still looks mainly numerical;
- the difficult structure is strongly right-edge-layer dominated;
- there is no clear near-fold signal yet;
- the branch is already measurably non-shallow, but the shallow/non-shallow
  mismatch does not show a special jump at the ceiling.

## Numerical Idea
The present failure pattern suggests that the continuation difficulty is
connected to how the right-edge layer is represented numerically.

This pilot therefore compares:

1. the current documented continuation path from pilot 12;
2. one or two transparent edge-aware mesh representations that cluster nodes
   more aggressively near `x = 1`.

The aim is not to hide the right-edge layer, but to resolve it more directly.

## What The Script Must Report
The numerical script in this folder reports:

- the highest converged load on the old path;
- the first failure load on the old path;
- the highest converged load on each edge-aware path;
- the first failure load on each edge-aware path;
- BC residuals at the ceiling/failure points;
- node concentration near `x = 1`;
- strongest-gradient variables;
- whether the ceiling moved materially beyond the current `4.3440 MPa`
  failure band.

## Bounded Run Policy
The run is intentionally staged and bounded.

It tests a short ladder above the reproducible anchor rather than attempting a
large extrapolation to `10 MPa`.
