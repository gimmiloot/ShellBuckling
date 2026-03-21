# Pilot 13. Shallow vs Non-Shallow Divergence Source

## Goal
This pilot studies the divergence between the repository's existing shallow
axisymmetric comparison path and the mapped 6-state non-shallow simple-support
branch across a wider load sweep.

The goal is not only to check the high-load barrier neighborhood.
The goal is to determine:

1. from what load range the shallow vs non-shallow mismatch becomes visible,
2. whether that mismatch grows with load,
3. where it is localized first,
4. and, if possible, which non-shallow correction terms are the main cause.

## What Is Already Known From Pilot 11
Pilot 11 already showed two important facts.

1. The mismatch exists below the `4.34 MPa` barrier neighborhood.
2. The mismatch is not a new barrier-localized effect that suddenly appears only
   near the high-load continuation bottleneck.

So the next question is no longer "does a mismatch exist?"
The next question is how that mismatch develops along the branch and which
non-shallow ingredients track it best.

## New Questions For Pilot 13
Pilot 13 therefore asks three narrower questions.

### A. Where does the mismatch start?
A load sweep is needed to see whether the shallow and mapped non-shallow paths
already separate at low load or only after some intermediate threshold.

### B. Does the mismatch grow with load?
If the mismatch is already present, the next issue is whether it stays roughly
load-invariant or grows systematically toward higher load.

### C. What is the likely source?
Using the live repository formulas, the pilot then checks which non-shallow
term groups are most plausibly responsible, for example:

- trigonometric nonlinearity,
- radius / geometry corrections involving `r = x + u_r`,
- curvature corrections containing `sin(varphi) / r`,
- or other exact-shell geometric factors.

## Pilot Structure
The pilot is split into two scripts.

1. `load_sweep_comparison.py`
   builds a bounded load sweep, compares the shallow and mapped non-shallow
   variables at each load, and records where the mismatch first becomes clearly
   non-negligible.

2. `term_attribution.py`
   reads the cached sweep data and computes diagnostic sizes for several
   non-shallow correction groups, then checks which of them correlate best with
   the measured mismatch.

## What This Pilot Does Not Prove
This pilot does **not** prove:

- that the shallow path and the non-shallow path are the same branch in a
  theorem-level sense;
- that any one diagnostic term group is the unique full cause of divergence;
- that the current barrier is explained completely by this comparison;
- or the final physical simple-support critical load.

At most, it sharpens the current repository-level statement about when the
shallow/non-shallow mismatch becomes visible, how it evolves with load, and
which non-shallow corrections appear most responsible.
