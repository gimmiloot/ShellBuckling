# Pilot 06: `G_ps` As The Mixed-Weak Prestress/Load Block

## Goal

This pilot isolates claim `V-S1` from the current verification map:

> The current branch must be formulated as a mixed weak-form with a bilinear
> prestress/load block `G_ps`, rather than by forcing everything into a single
> scalar-potential closure.

The goal is not to re-derive the whole shell theory from scratch. The goal is
to clarify the strongest current repository-level statement of this claim and to
check the structural pieces that can be checked now without inventing a new
theory.

## What `V-S1` means in the current repository

In the current repository, `V-S1` means the following narrower statement.

1. The active mixed-weak branch is organized around a weak-form

   ```text
   A_n(X, Xhat; q) = K_n(X, Xhat) - G_ps,n(X, Xhat; q) + B_partial,n(X, Xhat) = 0,
   ```

   with `X = (U, P)`, rather than around one scalar prestress potential
   `G(U)`.

2. The prestress/load contribution is treated as a genuine mixed bilinear block
   acting on independent trial/test slots in the current operator class.

3. The current active solver/testbench path reflects that structure through the
   reconstructed prestress/load forcing terms used in the mixed residual rows.

This is a repository-level structural claim. It is not yet a full
article-level theorem about every equivalent formulation of the complete shell
system.

## The strongest current repository-level statement of `G_ps`

The repository does **not** yet contain a final article-level full formula for
`G_ps`.

The strongest current repository-level statement is the combination of:

- the theory statement in `docs/theory/vyvod_uravneniy_updated17.md` that the
  active branch is a mixed weak-form with a separate block `G_ps`;
- the assumptions/journal statement that the prestress/load part does **not**
  close into one scalar potential `G(U)`;
- the active solver-level forcing reconstruction used in
  `solver_simple_support_core.py` and `solver_patched_core.py`.

At the current solver level, the active reconstructed forcing terms are:

```text
r     = c0 * u_s + s0 * u_n
r_x   = -(kappa_s0 * s0) * u_s + c0 * u_s_x + (kappa_s0 * c0) * u_n + s0 * u_n_x
e_th  = r / x + (n / x) * v
e_s   = T_s - nu * T_theta

g_s = -(T_theta^0 / r_0) * r_x - T_sn^0 * phi_x
g_n =  T_s^0 * phi_x + (c0 / x) * T_theta^0 * phi
       - (q^0 / x) * (r_0 * e_s + lambda_s^0 * r)
g_m =  (M_theta^0 / r_0) * r_x
```

with the corresponding active residual rows

```text
R_Ts = ... - g_s
R_Qs = ... - g_n
R_Ms = ... - g_m
```

So the strongest current repository reading is that `G_ps` is represented, at
least at the active solver/testbench level, by a background-weighted bilinear
block pairing these trial-side forcing expressions with the mixed test slots
associated to `T_s`, `Q_s`, and `M_s`.

## What "scalar-potential closure route" means here

In the current project context, the rejected scalar-potential closure route does
**not** just mean "any different notation."

It means the older idea that the forcing/prestress contribution could be packed
into one scalar object `G(U)` or one closure-style formula, so that the needed
mixed structure would effectively collapse back toward the old reduced/full
logic.

Within the current repository this route is considered insufficient because:

- the theory and assumptions explicitly say the prestress/load part does not
  close into one scalar potential `G(U)`;
- the journal records that the corrected functional route was the working one,
  while the old route did not give the needed structure;
- the active solver-level forcing already acts through mixed residual slots and
  depends on stress-like as well as displacement/rotation-like trial fields.

## What this pilot checks

This pilot checks three things.

### A. Structural clarification

`structure_check.md` isolates the strongest current repository statement of:

- the mixed weak-form;
- the current solver-level candidate for the `G_ps` forcing block;
- the repository reason the scalar-potential route is considered insufficient.

It also separates repository facts, current interpretation, and remaining
ambiguity.

### B. CAS layer

`cas_check.py` performs the strongest useful symbolic/structural checks that the
current repository formulas actually support.

It checks that:

- the active source files contain the current forcing terms and residual
  insertions used by the live mixed-weak workflow;
- the current solver-level forcing block is linear in the trial slot;
- the corresponding mixed block is linear in the test slot;
- the block depends on independent mixed test slots and therefore is not just a
  scalar quantity of one slot;
- the active block depends on the stress-like variable `T_s` as well as on
  displacement/rotation-like fields, so it does not fit the repository phrase
  "scalar potential `G(U)`" with `U = (u_s, u_n, v, phi, psi)` alone.

### C. Explicit scope control

The pilot keeps the logical boundary explicit:

- it checks the current repository formulation and active solver structure;
- it does **not** prove that no mathematically equivalent scalar reformulation
  could ever exist in a fuller theory;
- it does **not** close the full article-level derivation of `G_ps`.

## Why there is no numerical or Lean layer

No `numerical_check.py` is added for this pilot.

That is deliberate: the repository currently does not expose a live runnable
alternative solver implementing the rejected scalar-potential closure route.
Creating one here would mean inventing a new comparison architecture rather than
checking the current one.

No Lean file is added either.

An abstract theorem about bilinear forms versus scalar potentials would add much
less value than the repository-specific structural clarification and CAS check,
because `V-S1` is currently limited mainly by the exact repository meaning of
`G_ps`, not by a missing abstract logic lemma.

## What this pilot does **not** prove

This pilot does not prove:

- the full shell theory from first principles;
- the final article-level exact full formula for `G_ps`;
- that every background-coupling term has already been uniquely assigned to the
  final `G_ps` block rather than to another operator piece;
- a theorem that every possible scalar reformulation is impossible;
- any final physical buckling load.

## Verification boundary

This pilot is only about the current mixed-weak repository theory and the active
solver/testbench implementation.

It gives a repository-level clarification plus structural/CAS support. It is
not a full article-level theorem for the complete shell system.

## How to run

Run from the repository root.

CAS:

```powershell
.\.venv\Scripts\python.exe proof_pilots/pilot_06_gps_mixed_weak_block/cas_check.py
```
