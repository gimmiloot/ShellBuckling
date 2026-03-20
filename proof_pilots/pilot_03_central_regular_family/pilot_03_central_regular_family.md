# Pilot 03: Central Regular Family

## Goal

This pilot isolates claim `V-S4` from the current verification map:

> The current mixed-weak class has a two-dimensional physical regular family at
> the center.

The goal is not to prove the whole shell theory and not to jump ahead to the
final `B_mix` criterion. This pilot only checks the center-scaling and
mode-count logic used by the current mixed-weak branch.

The repository-level target sources are:

- `docs/theory/current_theory_verification_map.md` (`V-S4`)
- `docs/theory/vyvod_uravneniy_updated17.md` section `1.6`
- `docs/assumptions/assumptions.md` (`A6`)
- `docs/journal/project_journal_updated14.md` sections `3.4`, `4`, and `6.3`

## What `V-S4` means in the current repository

In the current repository context, `V-S4` means:

1. the mixed-weak branch uses the center scaling

```text
u_s, u_n, v = O(x^n),
varphi, psi = O(x^(n-1)),
T_s, S, T_theta = O(x^(n-1)),
Q_s, M_s, M_theta, H, chi = O(x^(n-2)),
```

2. the present center-regular family is treated as having exactly two free
   leading amplitudes;
3. the current `v2` boundary-matrix workflow should therefore build two
   center-regular modes, not arbitrary global surrogate-nullspace directions.

The theory-side operational form of that logic in the current code is the
center constraint matrix used in:

- `src/shell_buckling/mixed_weak/boundary_matrix_scan.py`
- `src/shell_buckling/mixed_weak/boundary_matrix_targeted_scan.py`

with center-leading functionals

```text
u_s / x^n,
phi / x^(n-1),
u_n / x^n + (lambda_c / n) * phi / x^(n-1),
psi / x^(n-1) - lambda_c * phi / x^(n-1).
```

The current workflow then builds two normalized modes:

```text
mode 1: u_s / x^n = 1,  phi / x^(n-1) = 0,
mode 2: u_s / x^n = 0,  phi / x^(n-1) = 1,
```

while imposing

```text
u_n / x^n + (lambda_c / n) * phi / x^(n-1) = 0,
psi / x^(n-1) - lambda_c * phi / x^(n-1) = 0.
```

This pilot checks exactly that current repository logic.

## Current center-scaling / principal-part logic used by the branch

The theory-side scaling statement is recorded in
`docs/theory/vyvod_uravneniy_updated17.md` section `1.6`.

The implementation-side center logic appears in two layers:

1. `field_exponent(...)` in the active mixed-weak core files
   - `u_s`, `u_n`, `v` use exponent `n`;
   - `phi`, `psi`, `T_s` use exponent `n-1`;
   - `Q_s`, `M_s` use exponent `n-2`.

2. `make_center_constraint_matrix(...)` in the active boundary-matrix scan
   files
   - it evaluates the leading center amplitudes;
   - it imposes the current regularity relations tying `u_n` and `psi` to the
     `phi`-led branch;
   - it supplies the constraints used by `solve_constrained_mode(...)`.

So the current repository logic is:

- the scaling table identifies the allowed center orders;
- the current reduced center ansatz keeps two leading amplitudes free;
- the `v2` workflow builds one `u_s`-led mode and one `phi`-led mode from that
  ansatz.

## What the CAS check verifies

`cas_check.py` verifies a small symbolic slice of the current center logic.

It checks:

- source guards for the current scaling statements in the theory file and the
  current center-constraint formulas in the active code;
- the active exponent table used by `field_exponent(...)`;
- the current reduced center constraint system on the leading amplitudes;
- that the reduced center constraint system has nullity `2`;
- that the current regular leading family can be parameterized by exactly two
  free amplitudes, corresponding to the `u_s`-led and `phi`-led directions used
  by the present workflow.

It does **not** prove the full differential system or a unique article-level
principal-part derivation for every possible mixed extension.

## What the numerical check verifies

`numerical_check.py` uses the actual current mixed-weak implementation.

It checks:

- the active `v2` builder really constructs two modes;
- the center values reported by the implementation satisfy the current
  center-regular relations in the project sense;
- the two computed columns are independent;
- the implementation path is using constrained center-normalized construction,
  not simply reusing raw smallest right-singular vectors of the interior matrix.

The numerical criterion for `regular at the center` in this pilot is the one
already used by the project:

```text
[u_s/x^n, phi/x^(n-1), u_n/x^n + (lambda_c/n)phi/x^(n-1), psi/x^(n-1)-lambda_c phi/x^(n-1)].
```

The stored basis returned by the current workflow is allowed to change under the
post-construction orthogonalization step. So this pilot accepts the current
numerical construction when:

- the last two entries vanish for the constructed span;
- the first two rows form an invertible `2 x 2` center-leading block;
- after re-basing within that span, one recovers the two intended normalized
  center modes.

## What the Lean check verifies

`lean/CentralRegularFamily.lean` stays abstract on purpose and now typechecks in
the current local Lean setup.

It proves two minimal logic steps, by name:

1. `two_dimensional_of_two_parameter_characterization`:
   if a local admissible family is in bijection with pairs of coefficients,
   then it is two-dimensional in the sense relevant to this pilot;
2. `active_regular_family_two_dimensional_of_two_center_modes`:
   if the active regular family is uniquely parameterized by the coefficients of
   two center-regular modes, then the active regular family is two-dimensional.

Lean does **not** prove the shell equations, the center-scaling table, or the
code-level center constraints. It only checks the abstract mode-count logic
used after those ingredients are supplied.

## Combined pilot conclusion

Taken together, the three layers support the following repository-level reading:

- CAS checks the current scaling statements, the reduced center nullity `2`, and
  the two-amplitude parameterization used by the present ansatz.
- the numerical diagnostic checks that the current `v2` implementation actually
  constructs a two-dimensional center-regular span with the intended normalized
  modes in the project sense.
- Lean checks the abstract implication from that two-parameter / two-mode
  parameterization to two-dimensionality.

So pilot 03 now tightens `V-S4` for the current repository boundary. It still
does **not** prove a full article-level derivation of the shell center problem
or uniqueness of every possible regular mixed extension.

## What this pilot does **not** prove

This pilot does not prove:

- the whole shell theory;
- the final full principal-part derivation in article-ready form;
- the final `B_mix` criterion;
- the final physical critical load;
- uniqueness of every possible regular mixed extension outside the current
  repository ansatz;
- a final closed BVP implementation.

## Verification boundary

This pilot is only for:

- the current mixed-weak principal-part / center-scaling statement recorded in
  the repository;
- the current reduced center ansatz used by the `v2` mode construction;
- the current surrogate/testbench mode-construction workflow.

It is **not** a proof beyond the current repository boundary.

## How to run

Run from the repository root.

CAS:

```powershell
.\.venv\Scripts\python.exe proof_pilots/pilot_03_central_regular_family/cas_check.py
```

Numerical:

```powershell
.\.venv\Scripts\python.exe proof_pilots/pilot_03_central_regular_family/numerical_check.py
```

Lean (if Lean is installed and on `PATH`):

```powershell
lean proof_pilots/pilot_03_central_regular_family/lean/CentralRegularFamily.lean
```

