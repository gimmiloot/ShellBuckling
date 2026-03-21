# Pilot 10. High-Load Simple-Support Continuation

## Goal
This pilot pushes the separate 6-state axisymmetric simple-support background
continuation as far upward in load as the current repository can support
honestly, while keeping the same equations and the same simple-support BC set.

The target is exploratory continuation toward approximately `10 MPa`.
That target is **not** assumed reachable in advance.

## Ceiling Before This Pilot
Before pilot 10, the best documented local branch-following result was the
pilot 09 ceiling near

```text
q approx 4.343 MPa,
```

with first loss of the branch near

```text
q approx 4.344 MPa.
```

That ceiling came from a dedicated local helper using smaller load steps,
right-edge-focused meshes, and a secant-style predictor, but it still lost the
branch by mesh-node blow-up.

## What Pilot 10 Investigates
Pilot 10 keeps the same 6-state simple-support background problem and asks a
narrower numerical question:

- can the same branch be continued above the current ceiling,
- how far can it be pushed,
- and what kind of obstruction is currently best supported by the evidence.

The obstruction is tracked in four explicitly separated categories.

### A. Numerical mesh / tolerance failure
This means:

- the equations and BCs are kept fixed,
- BC residuals remain small,
- but the solver still fails because the adaptive mesh runs out of nodes or the
  correction becomes too stiff for the current tolerance / mesh budget.

### B. Local right-edge boundary-layer stiffness
This is a more specific numerical diagnosis:

- failure is concentrated near `x approx 1`,
- node density piles up near the right edge,
- and the most singular-looking gradients localize there.

This is still numerical evidence, but more specific than a generic
"the solver failed" statement.

### C. Branch-turning or branch-ending suspicion
This would require evidence stronger than ordinary mesh pressure, for example:

- repeated loss of continuation even after step reduction and rescue profiles,
- without the failure looking dominated by right-edge mesh blow-up,
- or clear signs that the branch observables stop varying smoothly with load.

Pilot 10 does not assume this in advance; it only reports it if the run
produces concrete signs.

### D. Equation / BC issue
This category is reserved for new concrete evidence that the implemented
6-state equations or the simple-support BC mapping are wrong or internally
inconsistent.

If such evidence appears, it must be isolated and reported explicitly rather
than silently corrected inside the pilot.

## Numerical Changes Used in This Pilot
Pilot 10 is allowed to change only the continuation machinery, not the
mathematical problem. The campaign therefore focuses on:

- systematic reuse of the last converged adaptive mesh instead of always
  projecting back to one fixed mesh;
- secant-style prediction when two nearby converged states are available;
- adaptive load-step reduction when a target load fails;
- strict versus rescue solver profiles;
- right-edge-focused mesh profiles with different clustering strength;
- detailed per-attempt diagnostics for BC residuals, mesh pressure, and
  singular-looking gradients.

## What This Pilot Does Not Prove
Pilot 10 does **not** prove:

- that the simple-support branch exists smoothly all the way to `10 MPa`;
- that failure above the current ceiling is a true physical turning point;
- the final article-level axisymmetric simple-support background theorem;
- the final mixed-weak critical problem;
- or the final physical simple-support critical load.

At most, it sharpens the current repository-level statement about how far the
present 6-state continuation can be pushed and what the present bottleneck most
likely is.
