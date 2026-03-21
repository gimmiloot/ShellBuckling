# Pilot 16. Shallow Simple-Support Comparator

## Goal
This pilot builds the shallow-shell comparator that is physically aligned with
the active 6-state non-shallow simple-support background branch.

The repository already has a shallow comparison path, but pilot 15 showed that
it is **not** BC-equivalent to simple support.
Its edge conditions align with the moving-clamp / sliding-clamp side through
`varphi(1)=0`, not with the simple-support edge condition `M_s(1)=0`.

The purpose of the present pilot is therefore not to reuse that old path with a
new interpretation.
The purpose is to create the separate shallow comparator that is actually
needed for a fair simple-support comparison.

## Why This Matters
Future shallow-vs-nonshallow divergence studies only answer the intended
question if both sides solve boundary-value problems with the same physical
support type.

If the shallow comparator uses the wrong edge BC, then any observed mismatch
mixes together:

- model-depth differences,
- BC differences,
- and possible branch differences.

This pilot isolates the BC issue first and builds the shallow simple-support
path that later comparisons should use instead.

## Scope
This pilot:

- keeps the existing shallow equations;
- replaces the old shallow moving-clamp/sliding-clamp edge interpretation with
  a separate simple-support shallow BC set;
- keeps the new path clearly separate from the old comparator.

It does **not** claim theorem-level closure of the shallow reduction.
In particular, one of the simple-support BC translations is exact at the level
of the current mapping (`T_s(1)`), while the moment-free edge condition
`M_s(1)=0` is introduced through the shallow-limit reduction of the exact shell
mapping formulas.
