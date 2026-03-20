# Pilot 04: `B_mix` From Regular Modes

## Goal

This pilot isolates claim `V-S5` from the current verification map:

> The current boundary matrix `B_mix` must be constructed from two central
> regular modes, not from arbitrary surrogate kernel directions.

The goal is not to prove the whole shell theory. It is narrower:

- use the actual current repository code and theory;
- check how the active `B_mix` builders assemble the two columns of `B_mix`;
- compare that construction to a raw surrogate-direction alternative built from
  the two smallest right-singular vectors of the surrogate interior matrix.

The repository-level target sources are:

- `docs/theory/current_theory_verification_map.md` (`V-S5`)
- `docs/theory/vyvod_uravneniy_updated17.md` sections `2.2.1` and `2.2.2`
- `proof_pilots/pilot_03_central_regular_family/pilot_03_central_regular_family.md`
- `src/shell_buckling/mixed_weak/boundary_matrix_scan.py`
- `src/shell_buckling/mixed_weak/boundary_matrix_targeted_scan.py`

## What `V-S5` means in the current repository

In the current repository context, `V-S5` means:

1. pilot 03 already fixes the current repository boundary in which the active
   center-regular family is treated as two-dimensional;
2. the two columns used to form `B_mix` must therefore come from that
   center-regular family;
3. the current workflow must not replace those columns by arbitrary directions
   extracted only from the surrogate interior near-kernel.

Operationally, both active boundary-matrix builders use:

```text
C_center = make_center_constraint_matrix(...)
d1 = [1, 0, 0, 0]
d2 = [0, 1, 0, 0]
c1 = solve_constrained_mode(A_int, C_center, d1)
c2 = solve_constrained_mode(A_int, C_center, d2), then orthogonalized
V_reg = [c1, c2]
B_mix = B_full @ V_reg
```

So the current repository claim is not merely that two columns are chosen, but
that they are chosen as the two active center-regular modes.

## Two center-regular modes versus raw surrogate directions

The difference checked in this pilot is:

### A. Two center-regular modes

These are the two constrained modes built from the active center functionals

```text
[u_s/x^n, phi/x^(n-1), u_n/x^n + (lambda_c/n)phi/x^(n-1), psi/x^(n-1)-lambda_c phi/x^(n-1)].
```

They are built so that, in the current repository sense,

```text
mode 1 -> [1, 0, 0, 0]
mode 2 -> [0, 1, 0, 0]
```

after re-basing within the constructed span if needed.

### B. Arbitrary surrogate kernel directions / raw SVD directions

These are the two smallest right-singular vectors of the surrogate interior
matrix `A_int`, taken without imposing the active center constraints.

They may be near-null directions of the surrogate interior operator, but that
alone does not make them admissible center-regular modes.

So the key distinction is:

- `V_reg` is built by constrained center-regular construction;
- `V_raw` is built only from the raw surrogate interior near-kernel.

This pilot checks that the actual `B_mix` path uses `V_reg`, and that `V_raw`
is genuinely different in the current repository sense.

## What the numerical check verifies

`numerical_check.py` uses the active current code paths:

- `src/shell_buckling/mixed_weak/boundary_matrix_scan.py`
- `src/shell_buckling/mixed_weak/boundary_matrix_targeted_scan.py`

It checks four things.

### A. Current workflow check

It verifies that the live builders:

- form `V_reg` from the two constrained center-normalized modes;
- assemble `B_mix` as `B_full @ V_reg`;
- produce modes whose center-regular rows vanish in the current repository
  sense;
- produce a rank-2 center-leading block.

### B. Raw surrogate-direction comparison

It builds the comparison pair

```text
V_raw = two smallest right-singular vectors of A_int
```

and measures:

- their center values;
- their active regularity-row violations;
- how their coefficient-space span differs from the actual regular span.

### C. Boundary matrix comparison

It compares:

- `B_mix_reg = B_full @ V_reg`
- `B_mix_raw = B_full @ V_raw`

and reports whether they coincide or differ numerically, together with a
boundary-column-space comparison.

Even if some boundary quantities were accidentally close, the current
repository meaning would still differ if `V_raw` fails the active center
constraints.

### D. Final explicit conclusion

It reports whether the current repository actually builds `B_mix` from the
center-regular pair and whether replacing that pair by raw surrogate directions
would change the construction in a meaningful current-repository sense.

## What the Lean check verifies

`lean/BmixFromRegularModes.lean` is intentionally abstract.

It proves two minimal logic steps:

1. if a boundary object is defined to come from an admissible family, then a
   pair that does not satisfy the admissibility constraints cannot be the pair
   used for that boundary object;
2. in project language, if `B_mix` is a boundary object of the center-regular
   family and only the regular pair satisfies the active center constraints,
   then `B_mix` must be built from the center-regular pair rather than from the
   non-admissible surrogate pair.

Lean does **not** formalize the shell system or the numerical boundary-matrix
assembly. It only checks the abstract admissibility logic.

## What this pilot does **not** prove

This pilot does not prove:

- the full shell theory;
- the full principal-part derivation at the center;
- the final article-level correctness of the mixed-weak BVP;
- that the current surrogate/testbench builder is already the final solver;
- the final physical critical load;
- that every possible alternative surrogate construction must fail in every
  future code variant.

It is only a repository-level check of the current `B_mix` construction rule.

## Verification boundary

This pilot is only for:

- the current reduced-center / surrogate-testbench workflow;
- the actual current `build_boundary_matrix_test_v2(...)` construction path in
  the active scan files;
- the abstract admissibility logic that explains why a boundary object of the
  regular family should use the regular pair rather than a non-admissible raw
  surrogate pair.

It is **not** a full proof beyond the current repository boundary.

## How to run

Run from the repository root.

Numerical:

```powershell
.\.venv\Scripts\python.exe proof_pilots/pilot_04_bmix_from_regular_modes/numerical_check.py
```

Lean:

```powershell
lean proof_pilots/pilot_04_bmix_from_regular_modes/lean/BmixFromRegularModes.lean
```
