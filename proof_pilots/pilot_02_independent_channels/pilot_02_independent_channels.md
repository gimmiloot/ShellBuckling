# Pilot 02: Independent Circumferential Channels

## Goal

This pilot checks assumption A4 on a small, reproducible slice of the current
mixed-weak branch:

- the membrane circumferential channel `(v, S)` must remain structurally
  distinct from
- the twist/shear channel `(psi, H, chi)`.

The point is not to re-derive the whole shell theory. The point is to verify
that the current operator class really contains two independent circumferential
blocks and does not collapse back into the old closure logic.

The project-level statement being tested is recorded in:

- `docs/assumptions/assumptions.md:63`
- `docs/theory/vyvod_uravneniy_updated17.md:244`
- `docs/journal/project_journal_updated14.md:15`

## Exact current formulas used

The pilot uses the current mixed-weak reconstruction formulas from the active
core files:

- `src/shell_buckling/mixed_weak/solver_simple_support_core.py:445`
- `src/shell_buckling/mixed_weak/solver_simple_support_core.py:452`
- `src/shell_buckling/mixed_weak/solver_simple_support_core.py:455`
- `src/shell_buckling/mixed_weak/solver_simple_support_core.py:456`
- `src/shell_buckling/mixed_weak/solver_simple_support_core.py:460`
- `src/shell_buckling/mixed_weak/solver_simple_support_core.py:461`
- `src/shell_buckling/mixed_weak/solver_simple_support_core.py:463`

The same formulas are also present in the targeted follow-up core:

- `src/shell_buckling/mixed_weak/solver_patched_core.py:445`
- `src/shell_buckling/mixed_weak/solver_patched_core.py:452`
- `src/shell_buckling/mixed_weak/solver_patched_core.py:455`
- `src/shell_buckling/mixed_weak/solver_patched_core.py:456`
- `src/shell_buckling/mixed_weak/solver_patched_core.py:460`
- `src/shell_buckling/mixed_weak/solver_patched_core.py:461`
- `src/shell_buckling/mixed_weak/solver_patched_core.py:463`

The exact formulas copied into the CAS pilot are:

```text
r = c0 * us + s0 * un

S = (v_x - a0 * v - (n / x_safe) * us) / (2.0 * (1.0 + nu))

kappa_theta_new = (c0 / r0) * phi - (s0 / (r0 * r0)) * r + b_theta * psi
M_theta = nu * Ms + kappa_theta_new / Lambda

H = (psi_x - a0 * psi - b_s * phi) / C_twist
H_x = (psi_xx - a0_p * psi - a0 * psi_x - b_s_p * phi - b_s * phi_x) / C_twist

chi = (b_theta * M_theta - H_x - 2.0 * a0 * H) / lam_th0
```

No alternative formulas are introduced in this pilot.

## Witness states used by the CAS layer

The CAS script constructs explicit symbolic witnesses.

### A. v-block witness

Turn on only the `v`-channel data:

```text
us = 0, un = 0, v = v0, v_x = vx0,
phi = 0, phi_x = 0, psi = 0, psi_x = 0, psi_xx = 0, Ms = 0.
```

Then:

```text
S = (vx0 - a0*v0) / (2.0*(1.0 + nu)),
H = 0,
chi = 0.
```

So the `(v, S)` block can be active while the `(psi, H, chi)` block stays
inactive.

### B. psi-block witness

Turn off the `v`-block and activate only `psi_x`:

```text
us = 0, un = 0, v = 0, v_x = 0,
phi = 0, phi_x = 0, psi = 0, psi_x = psix0, psi_xx = 0, Ms = 0.
```

Then:

```text
S = 0,
H = psix0 / C_twist,
chi = -a0*psix0 / (C_twist*lam_th0).
```

This shows that the `(psi, H, chi)` block does not require the `v`-channel to
be active.

### C. chi-only witness

The CAS script also records a second psi-side witness tailored to `chi`:

```text
us = 0, un = 0, v = 0, v_x = 0,
phi = 0, phi_x = 0, psi = psi0, psi_x = a0*psi0, psi_xx = 0, Ms = 0.
```

Then:

```text
S = 0,
H = 0,
chi = psi0*(C_twist*b_theta^2 + Lambda*(a0^2 + a0_p))
      / (C_twist*Lambda*lam_th0).
```

This is useful because it isolates a `chi` witness without reactivating `S`.

## What the CAS check verifies

`cas_check.py` performs three kinds of checks.

### Exact symbolic checks

It checks, exactly:

- the expected source-formula lines are still present in the current mixed-weak
  core files;
- `S` has zero symbolic dependence on the twist/shear variables
  `phi`, `phi_x`, `psi`, `psi_x`, `psi_xx`, `Ms`;
- `H` has zero symbolic dependence on the `v`-channel variables
  `us`, `v`, `v_x`;
- `chi` has no direct symbolic dependence on `v` or `v_x`.

### Witness-based separation checks

It then evaluates the witness states above and confirms:

- `S` can be active with `H = 0` and `chi = 0`;
- `H` can be active while `S = 0`;
- `chi` can also be active while `S = 0`.

These witness states are used as the clean non-collapse test when a global
closed-form scalar-multiple criterion would be less readable than the witnesses
themselves.

## What the Lean check verifies

`lean/IndependentChannels.lean` stays abstract on purpose. It does not encode
the shell formulas.

It proves:

- theorem `separating_witnesses_imply_structural_independence`:
  if two channel maps on a product space admit separating witnesses, then
  neither map is a scalar multiple of the other;
- theorem `vS_type_channel_independent_of_psiHchi_type_channel`:
  the same argument restated in the project language for a `v/S`-type channel
  and a `psi/H/chi`-type channel.

The Lean layer therefore checks the logical shape of the independence argument,
while the CAS layer supplies the shell-specific witnesses from the current
formulas.

## What this pilot does not prove

This pilot does not prove:

- the full mixed-weak shell theory;
- correctness of the complete BVP solver;
- existence of a final validated critical load;
- that every possible closure failure mode is excluded;
- any stronger claim than structural channel separation in the current formulas.

## How to run

Run from the repository root.

SymPy check:

```powershell
.\.venv\Scripts\python.exe proof_pilots/pilot_02_independent_channels/cas_check.py
```

Lean file:

```powershell
lean proof_pilots/pilot_02_independent_channels/lean/IndependentChannels.lean
```

If `lean` is not on your `PATH`, use your local Lean 4 executable directly.
