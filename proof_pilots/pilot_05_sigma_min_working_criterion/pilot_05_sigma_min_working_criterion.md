# Pilot 05: `sigma_min(B_mix)` As Working Criterion

## Goal

This pilot isolates claim `V-N1` from the current verification map:

> `sigma_min(B_mix(q)) = 0` is the current working spectral criterion for the
> mixed-weak branch.

The goal is not to prove the whole shell theory and not to validate the final
physical `simple support` critical load. This pilot is only about the current
repository boundary:

- whether the live mixed-weak `B_mix` workflow makes `sigma_min(B_mix(q))`
  numerically computable;
- whether the criterion remains meaningful under the current broad / fine /
  adaptive / targeted scan workflow;
- whether the resulting picture is qualitatively new relative to the rejected
  old architecture, to the extent that this can still be checked in the current
  checkout.

The repository-level target sources are:

- `docs/theory/current_theory_verification_map.md` (`V-N1`)
- `docs/theory/vyvod_uravneniy_updated17.md` sections `2.2.2` and `2.3`
- `docs/assumptions/assumptions.md` (`A7`)
- `docs/journal/project_journal_updated14.md` sections `1`, `4`, and `10`
- `src/shell_buckling/mixed_weak/boundary_matrix_scan.py`
- `src/shell_buckling/mixed_weak/boundary_matrix_targeted_scan.py`

## What `V-N1` means in the current repository

In the current repository context, `V-N1` means:

1. the current mixed-weak branch builds `B_mix(q)` from the active
   center-regular mode pair;
2. the smallest singular value of that matrix is the quantity monitored as the
   present exploratory spectral indicator;
3. the criterion should be usable inside the current scan/testbench workflow,
   even though it is not yet a final theorem of the complete physical problem.

So the repository-level question is not whether `sigma_min(B_mix)=0` has been
proved for the final closed shell problem. The question is narrower:

- can the live code actually evaluate this quantity;
- does it remain numerically meaningful across the current scan workflow;
- does it support the current exploratory mixed-weak picture better than the
  rejected old architecture did.

## What is checked numerically

`numerical_check.py` uses the actual current mixed-weak scan helpers.

It checks five things.

### A. Computability

It verifies that the current code can actually assemble `B_mix` and compute
`sigma_min(B_mix)` over the active broad pressure range.

It also checks that:

- the computed values are finite;
- the assembled matrices do not collapse to all-zero objects;
- the larger singular value stays nontrivial enough that the smallest singular
  value is not being reported from a completely degenerate matrix.

### B. Scan consistency

It reuses the current scan workflow pieces:

- broad baseline scan,
- fine scan windows,
- adaptive windows,
- targeted local scan windows.

For each workflow it reports candidate minima / near-zero locations for the raw
criterion `sigma_min(B_mix)`, together with the current balanced diagnostics
already used by the repository as stability helpers.

### C. Sensitivity / robustness

It also reuses the current resolution-study windows and case list.

The purpose is to see whether modest changes in basis size, collocation, and
local refinement keep the criterion in the same qualitative region or whether
the picture breaks down.

### D. Qualitative novelty

This pilot tries to compare the current picture with the rejected old
architecture.

If the old reduced/full solvers are not runnable in the current checkout, the
pilot says so explicitly and falls back to the strongest current internal
evidence already recorded in the repository documents.

### E. Final explicit conclusion

The script distinguishes two levels of success:

1. support for keeping `sigma_min(B_mix)` as a **working exploratory
   criterion** in the current branch;
2. stronger evidence that would justify tightening `V-N1` beyond its current
   partial status.

These are not the same thing.

## Why there is no Lean layer

No Lean file is added for this pilot.

The optional abstract theorem

```text
sigma_min(A) = 0  <->  rank loss
```

would add only generic linear-algebra bookkeeping, while `V-N1` is mainly about
the numerical behavior and workflow stability of the current repository
criterion. So a Lean layer would not materially verify the repository-level
claim being tested here.

## What this pilot does **not** prove

This pilot does not prove:

- the full shell theory;
- the final physical `simple support` critical load;
- that the current exploratory candidate is already the true physical `q_cr`;
- that the current testbench criterion is already identical to the final closed
  mixed BVP criterion;
- that every coarse scan or every future workflow variant must localize the
  minimum equally well.

It only checks the current repository-level working status of
`sigma_min(B_mix(q))`.

## Verification boundary

This pilot is only for:

- the current mixed-weak exploratory/testbench branch;
- the actual current `B_mix` construction and scan helpers in the repository;
- the current broad / fine / adaptive / targeted workflow;
- the current repository record of what failed in the rejected old
  architecture.

It is **not** a final theorem beyond the current repository boundary.

## Current pilot outcome

On the current repository checkout, the numerical pilot supports keeping
`sigma_min(B_mix)` as the active working spectral criterion and tightens `V-N1`
within the present exploratory/testbench boundary.

What the completed pilot establishes is narrower than a full theorem:

- the live scan modules do compute `sigma_min(B_mix)` reliably enough for the
  current exploratory workflow;
- the refined fine/adaptive/targeted scans reproduce the current candidate
  neighborhoods in a mutually consistent way;
- the current resolution study shows moderate rather than catastrophic drift;
- direct rerun of the rejected old reduced/full architecture is not practical
  in this checkout, so the novelty comparison rests on the repository's
  recorded negative old-architecture evidence plus the live mixed-weak scan
  behavior.

This still does **not** prove the final closed mixed BVP criterion or the final
physical `simple support` critical load.

## How to run

Run from the repository root.

Numerical:

```powershell
.\.venv\Scripts\python.exe proof_pilots/pilot_05_sigma_min_working_criterion/numerical_check.py
```

