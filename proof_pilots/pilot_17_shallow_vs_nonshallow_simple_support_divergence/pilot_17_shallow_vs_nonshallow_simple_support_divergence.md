# Pilot 17: Shallow vs Non-Shallow Simple-Support Divergence

## Goal

This pilot revisits the shallow-versus-non-shallow divergence question for the
axisymmetric simple-support background, but now in the correct boundary-condition
setting.

Pilot 15 showed that the old shallow comparison path used a
moving-clamp/sliding-clamp-type shallow BC set rather than a BC-equivalent
simple-support set. Pilot 16 then constructed the strongest currently justified
repository-level shallow simple-support comparator. The present pilot uses that
new comparator to answer the original scientific question in the correct
physical setting.

## Why this pilot is needed

Pilot 13 was useful as a mismatch detector, but it did not answer the
simple-support question fairly because its shallow comparison path was not
BC-equivalent to the active 6-state non-shallow simple-support branch.

This pilot therefore supersedes pilot 13 for the specific question:

- when does shallow/non-shallow divergence become visible for the
  simple-support problem;
- does the mismatch grow with load;
- where does it localize first;
- which explicitly non-shallow term groups are the strongest candidates for the
  observed divergence.

## Scope

What this pilot does:

- compares the active 6-state non-shallow simple-support branch against the new
  shallow simple-support comparator from pilot 16;
- uses the repository mapping formulas that convert the non-shallow solution
  into shallow-like variables `theta0`, `theta0'`, `Phi0`, and `Phi0'`;
- sweeps from low load to the highest reliably available non-shallow
  simple-support load in the current repository workflow.

What this pilot does not prove automatically:

- a theorem-level exact equivalence of the full shallow and non-shallow
  problems;
- that every observed mismatch is uniquely attributable to one named
  non-shallow term;
- that the high-load continuation barrier is explained solely by the shallow vs
  non-shallow difference.

## Expected output

The pilot should produce:

- a corrected mismatch-versus-load sweep for the simple-support problem;
- a localization summary for where the mismatch first appears;
- a term-attribution summary based on the explicitly non-shallow correction
  groups already present in the repository formulas.
