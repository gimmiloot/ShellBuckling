# Pilot 01: Boundary Pairs

## Goal

This pilot isolates one local step of the current mixed-weak theory: the right
boundary-pair reduction used in the boundary testbench.

The point of the pilot is not to re-derive the full mixed-weak formulation. It
only checks the boundary-pair step:
- start from the full right boundary form,
- impose the admissible reduction coming from the essential conditions,
- confirm the reduced free-variation form,
- confirm the resulting natural conditions.

## Boundary form

For the current mixed-weak notation, the right boundary form is

```text
B_right = T_s*u_s_hat + Q_s*u_n_hat + S*v_hat + M_s*varphi_hat + H*psi_hat.
```

The boundary pairs are therefore

```text
(T_s, u_s), (Q_s, u_n), (S, v), (M_s, varphi), (H, psi).
```

## Admissible reduction

In the testbench step we impose the essential conditions

```text
u_n(1) = 0,
varphi(1) = 0.
```

So admissible test variations satisfy

```text
u_n_hat = 0,
varphi_hat = 0.
```

The free boundary variations are therefore

```text
u_s_hat, v_hat, psi_hat.
```

Substituting the admissibility conditions into the full boundary form gives the
reduced form

```text
B_right,free = T_s*u_s_hat + S*v_hat + H*psi_hat.
```

If this reduced form vanishes for all free variations, the natural conditions at
`x = 1` are

```text
T_s(1) = 0,
S(1) = 0,
H(1) = 0.
```

## What the CAS check verifies

`cas_check.py` checks the purely symbolic reduction step.

It verifies:
- the full boundary form is reduced under `un_hat = 0` and `phi_hat = 0`, with
  `phi_hat` used as an alias for `varphi_hat`;
- the reduced form is exactly
  `T_s*u_s_hat + S*v_hat + H*psi_hat`;
- the basis tests for the free-variation triple `(u_s_hat, v_hat, psi_hat)`:
  `(1, 0, 0)`, `(0, 1, 0)`, `(0, 0, 1)`;
- the three basis tests isolate the coefficients `T_s`, `S`, and `H`.

## What the Lean check verifies

`lean/BoundaryPairs.lean` checks the logical step after the symbolic reduction.

It proves:
- theorem `coeffs_zero_of_linear_form_vanishes`: if
  `T_s*u_s_hat + S*v_hat + H*psi_hat = 0`
  for all free variations, then
  `T_s = 0`, `S = 0`, and `H = 0`;
- theorem `natural_bc_from_admissible_variations`: a shell-notation version where `Q_s` and `M_s` are still present,
  but their factors are zero because admissibility forces `u_n_hat = 0` and
  `varphi_hat = 0`.

The Lean file is intentionally minimal. It only formalizes this coefficient
extraction step.

## How to run

Run from the repository root.

SymPy check (requires the `sympy` package in the active Python environment):

```powershell
.\.venv\Scripts\python.exe proof_pilots/pilot_01_boundary_pairs/cas_check.py
```

Lean file:

```powershell
lean proof_pilots/pilot_01_boundary_pairs/lean/BoundaryPairs.lean
```

If `lean` is not on your `PATH`, open the file in your local Lean 4 setup and
run it there.
