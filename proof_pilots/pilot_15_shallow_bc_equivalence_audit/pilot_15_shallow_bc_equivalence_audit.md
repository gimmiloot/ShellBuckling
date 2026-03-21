# Pilot 15. Shallow BC Equivalence Audit

## Goal
This pilot audits the boundary conditions used by the current shallow
comparison path and checks whether they are physically equivalent to the
current 6-state non-shallow simple-support branch.

The question is narrow and structural:

1. what BCs the current shallow comparison path actually imposes;
2. how those BCs map into the non-shallow variables already used in the
   repository;
3. whether that mapped BC set matches the current 6-state simple-support
   problem or instead matches a different physical task.

## Why This Matters
Pilots 11 and 13 compared the active 6-state non-shallow simple-support branch
against the repository's older shallow comparison path.

That comparison is only physically fair if the shallow path solves the same
boundary-value problem, at least at the level of the intended edge and center
constraints.

If the shallow path instead corresponds to a moving-clamp / sliding-clamp-type
task, then shallow/non-shallow mismatch cannot be read purely as a model-depth
effect; part of the mismatch may already be a BC mismatch.

## Scope
This pilot checks BC equivalence only.

It does **not**:

- change solver numerics;
- modify the shallow or non-shallow equations;
- repair or replace the shallow path;
- prove that two branches coincide dynamically.

The purpose is simply to state, as precisely as the current repository allows,
which physical BC problem the present shallow comparison path is actually
solving.
