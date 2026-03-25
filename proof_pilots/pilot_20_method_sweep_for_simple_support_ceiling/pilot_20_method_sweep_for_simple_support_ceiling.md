# Pilot 20: Method Sweep for the Simple-Support Ceiling

## Goal
This pilot runs a bounded numerical method sweep for the active 6-state axisymmetric simple-support background path. The aim is to test whether the present simple-support load ceiling can be moved upward without changing the governing equations or the simple-support boundary conditions.

## Why this pilot is justified
The current reference path has a reproducible anchor at `4.3434 MPa` and a first persistent failure at `4.3440 MPa`. Pilot 18 and pilot 19 already sharpened the interpretation of that band:

- the bottleneck still looks mainly numerical;
- the branch is already non-shallow, but there is still no clear near-fold signal;
- simple right-edge mesh concentration by itself did not move the ceiling materially.

That makes a method sweep justified. The next conservative question is not whether to change the mathematics, but whether a better numerical formulation can carry the same 6-state branch farther.

## Scope
This pilot compares numerical methods, not mathematics.

It keeps fixed:

- the active 6-state simple-support equations in `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`;
- the same simple-support BC set;
- the same interpretation boundary between the separate 6-state simple-support path and the exploratory mixed-weak scans that still use the older `F_min` background.

## Methods tested
The bounded sweep compares four transparent strategy classes plus the old path as a control:

- baseline old path: the current rescue-local secant continuation workflow;
- quadratic predictor bundle: a stronger three-point predictor on the same single-domain mesh;
- arc-like state-norm control: a pseudo-arclength-like tangent step with bounded factor adaptation;
- `u_z`-scaled state: unchanged physics, but a numerically rescaled solver state with extra weight on the dominant barrier variable `u_z`;
- bulk/edge domain split: a multiple-shooting-like split between the bulk and the right-edge region with explicit matching.

## Bounded-run policy
The sweep is staged and budgeted. It does not try to push to `10 MPa`, and it records incremental results in `method_sweep_results.json` after each method.

## Outcome summary
The control path stayed at the known `4.3434 / 4.3440 MPa` ceiling/failure pair. Predictor-only changes helped only modestly. The strongest bounded result came from the unchanged-equation `u_z`-scaled state representation, which reached `4.3520 MPa` in the packaged sweep without a bounded failure being hit. The pseudo-arclength-like surrogate also moved the ceiling upward, but much less. The current packaged bulk/edge domain-split prototype did not reproduce the `4.3434 MPa` anchor cleanly and is not the recommended next step in its present form.

## Main interpretation
This pilot strengthens the numerical-barrier reading. The ceiling is sensitive to numerical formulation and conditioning, not only to raw right-edge mesh concentration. Because the best improvement came from a transparent state representation change with unchanged equations and BCs, the present bottleneck still reads as numerical rather than as a verified physical fold.

## Files
- runnable script: `proof_pilots/pilot_20_method_sweep_for_simple_support_ceiling/method_sweep.py`
- recorded results: `proof_pilots/pilot_20_method_sweep_for_simple_support_ceiling/method_sweep_results.json`
- compact method table: `proof_pilots/pilot_20_method_sweep_for_simple_support_ceiling/method_comparison_table.md`
