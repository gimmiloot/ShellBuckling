# Pilot 18: Revised Analytic Barrier Diagnosis

## Goal

This pilot revisits the current `4.3434..4.3440 MPa` barrier of the active
6-state axisymmetric simple-support background path after the repository status
changed in three important ways:

- `4.3434 MPa` is now a reproducible high-load anchor on the same staged
  secant/profile-mesh strategy;
- `4.3440 MPa` remains the first persistent staged failure;
- the corrected BC-aligned shallow/non-shallow comparison no longer supports a
  special new mismatch jump at the ceiling.

So the question is no longer whether the barrier is simply “the place where the
shallow and non-shallow branches split.” The revised question is narrower and
more analytic:

- is the barrier best interpreted as a stiff right-edge layer on an already
  non-shallow branch,
- is there evidence of a near-fold / near-singular continuation issue,
- or is the present evidence still mixed.

## Current facts entering this pilot

The pilot starts from the following repository-level facts already established by
pilots 08, 09, 12, 15, 16, and 17:

- `4.3434 MPa` is reproducible on the active 6-state simple-support branch;
- `4.3440 MPa` is still the first persistent staged failure;
- failed `4.3440 MPa` attempts keep tiny BC residuals, around `1e-17`;
- failed `4.3440 MPa` attempts show extreme node pile-up near `x=1`;
- the strongest gradients remain dominated by `u_z`, with a smaller
  `varphi` shoulder;
- the corrected shallow/non-shallow mismatch becomes clearly visible around
  `2..3 MPa`, grows with load, and stays smooth through the available high-load
  range;
- therefore the present ceiling is not currently explained by a sudden new
  shallow/non-shallow split right at `4.34 MPa`.

## What this pilot checks

The pilot adds two complementary diagnostics.

1. `jacobian_conditioning_check.py`
   builds a coarse discretized BVP residual Jacobian along the converged branch
   near the ceiling and checks whether a near-zero-singular-value trend appears.

2. `term_balance_check.py`
   evaluates the actual equation terms near the right edge on the converged
   branch and asks which balances dominate as the load approaches `4.3434 MPa`.

3. `edge_layer_scaling.md`
   then gives a compact leading-order heuristic interpretation of the coupled
   edge balance using the actual live equations and the actual numerical
   symptoms.

## What this pilot does not prove

This pilot does **not** prove:

- a full analytic theorem for the edge layer,
- a full proof that the branch cannot fold above `4.3434 MPa`,
- the final closed shell BVP,
- or the final physical simple-support critical load.

It is a revised repository-level analytic diagnosis only.
