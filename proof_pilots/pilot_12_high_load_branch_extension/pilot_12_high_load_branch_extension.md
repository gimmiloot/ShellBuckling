# Pilot 12. High-Load Branch Extension

## Goal
This pilot turns the newly achieved `4.3434 MPa` success into a staged and
reproducible high-load continuation branch for the active 6-state axisymmetric
simple-support background path.

The goal is not to claim that the branch reaches `10 MPa`, and it is not to
reinterpret one lucky convergence as proof of smooth global continuation.
The goal is narrower: check whether the same branch can now be advanced
reliably above `4.3434 MPa` by reusing the successful high-load numerical
strategy in a bounded ladder.

## Why This Pilot Is Needed
Pilot 10 still treated `4.3434 MPa` as unresolved.
Pilot 11 then showed that `4.3434 MPa` can in fact be reached on the
non-shallow branch when the continuation uses the profile-mesh secant strategy
that projects both nearby successful states onto the right-edge-focused local
mesh.

That changes the interpretation of the old barrier.
It now looks less like a proved branch stop and more like a difficult numerical
continuation zone.

What is still missing is reproducibility.
An isolated success is not yet a usable continuation branch.

## What Counts As Success In Pilot 12
Pilot 12 counts as successful only if all three conditions are supported by the
run:

1. `4.3434 MPa` converges repeatedly under the same staged strategy.
2. The branch continues stably to a ladder of slightly higher loads above
   `4.3434 MPa`.
3. Neighboring successful states remain smooth enough that there is no clear
   sign of an accidental branch jump.

## Load Ladders
The first bounded ladder is

```text
4.3434, 4.3440, 4.3450, 4.3475, 4.3500 MPa.
```

Only if that first ladder is genuinely successful and smooth does the pilot
attempt a second ladder above `4.3500 MPa`.

## Numerical Strategy Used
The pilot keeps the same 6-state equations and the same simple-support BC set.
Only the continuation machinery is changed.

The branch-extension run uses:

- the real current 6-state simple-support background path;
- the same anchor plus local-bootstrap workflow developed in pilots 09 and 10;
- the rescue-local right-edge-focused mesh profile that reached `4.3434 MPa` in
  pilot 11;
- a seed order that prioritizes the winning `secant_profile_mesh` strategy;
- reuse of the last converged adaptive solution as the next step seed;
- continuity diagnostics between neighboring successful loads;
- explicit branch-jump suspicion checks;
- incremental JSON writes after every major stage.

## What This Pilot Does Not Prove
This pilot does **not** prove:

- that the branch exists smoothly all the way to `10 MPa`;
- that every future failure is purely numerical;
- that the full mixed-weak workflow is ready to reconnect to this branch;
- or the final physical simple-support critical load.

At most, it establishes whether the present branch can now be extended above
`4.3434 MPa` in a reproducible and smooth staged continuation workflow.
