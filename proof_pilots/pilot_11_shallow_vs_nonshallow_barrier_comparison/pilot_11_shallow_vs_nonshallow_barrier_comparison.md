# Pilot 11. Shallow vs Non-Shallow Barrier Comparison

## Goal
This pilot compares the current 6-state non-shallow axisymmetric
simple-support background branch against the repository's existing shallow
comparison path near the present non-shallow continuation barrier around
`4.3434..4.3440 MPa`.

The purpose is diagnostic only.
The pilot does not change the solver mathematics and does not promote any
comparison into a final theorem about the physical simple-support problem.

## Why This Comparison Is Useful
The present non-shallow simple-support branch reaches only a narrow band above
`4.343 MPa` before continuation is lost again by strong right-edge mesh
pressure.

By contrast, the repository's supporting shallow comparison path is routinely
continued through the same load neighborhood without showing a matching solver
barrier there.

This makes a localized comparison useful for separating three possibilities:

1. the current barrier is mainly numerical and tied to the right-edge layer;
2. the barrier reflects genuinely non-shallow behavior that the shallow model
   does not reproduce;
3. the two paths are no longer close enough near the barrier that a shallow
   comparison can be read as the same branch without extra caution.

## What Is Compared
The pilot compares:

- the current validated non-shallow 6-state simple-support branch built from
  the active `axisymmetric_simple_support_background.py` path together with the
  bounded rescue bootstrap from pilot 10;
- the repository's existing supporting shallow 4-state path from the shallow /
  non-shallow comparison scripts;
- the mapped shallow-like variables
  `theta0`, `theta0'`, `Phi0`, `Phi0'`
  reconstructed from the non-shallow solution using the live repository
  formulas.

The comparison is made both on the full interval and with special focus near
`x = 1`.

## What This Pilot Does Not Conclude Automatically
This pilot does **not** automatically prove:

- that the shallow comparison path is a theorem-level exact simple-support
  counterpart of the current 6-state branch;
- that visual similarity alone means the two descriptions are the same branch;
- that divergence alone proves branch nonexistence;
- or that the present non-shallow barrier is a physical limit point.

At most, it sharpens which interpretation the current repository evidence
supports more strongly: numerical edge-layer difficulty, non-shallow structural
separation, or unresolved ambiguity.
