# Structure Check For `V-S1`

## Repository Facts Already Stated

### 1. Mixed weak-form is the active repository statement

The current theory file states the active form as

```text
A_n(X, Xhat; q) = K_n(X, Xhat) - G_ps,n(X, Xhat; q) + B_partial,n(X, Xhat) = 0,
```

with `X = (U, P)`.

This is an explicit repository fact from
`docs/theory/vyvod_uravneniy_updated17.md`, section `1.4`.

### 2. The prestress/load part is explicitly said not to be one scalar potential

The same theory file states that the prestress/load part does **not** close into
one scalar potential `G(U)` and is instead introduced as a separate bilinear
weak-form `G_ps`.

This is repeated in:

- `docs/assumptions/assumptions.md`, assumption `A5`;
- `docs/journal/project_journal_updated14.md`, section `5.1`.

So the repository already records the intended structural distinction:

- accepted route: mixed bilinear block `G_ps(U, Uhat)` or `G_ps(X, Xhat)`;
- rejected route: one scalar-potential closure `G(U)`.

### 3. The journal localizes the unresolved part

`docs/journal/project_journal_updated14.md`, section `5.3`, says the bulk
equations in `u_s` and `u_n` were structurally recovered, and that the missing
piece is localized in the prestress/load part rather than being spread across
the whole variational philosophy.

That matters because `V-S1` is not a claim about the entire mixed-weak system.
It is specifically about the current prestress/load block.

### 4. The active solver contains a concrete solver-level forcing structure

The two active cores

- `src/shell_buckling/mixed_weak/solver_simple_support_core.py`
- `src/shell_buckling/mixed_weak/solver_patched_core.py`

use the reconstructed forcing terms

```text
g_s = -(T_theta^0 / r_0) * r_x - T_sn^0 * phi_x
g_n =  T_s^0 * phi_x + (c0 / x) * T_theta^0 * phi
       - (q^0 / x) * (r_0 * e_s + lambda_s^0 * r)
```

and a third background coupling in the moment row

```text
g_m = (M_theta^0 / r_0) * r_x
```

through

```text
R_Ts = ... - g_s
R_Qs = ... - g_n
R_Ms = ... - g_m.
```

The active scan/testbench modules are wired directly to these cores, so these
terms are not dead code. They are the current repository implementation path.

## Current Interpretation

The strongest current repository-level interpretation of `V-S1` is:

1. `G_ps` is not yet fixed as one final article-level explicit integral formula.
2. But the repository does already fix its structural role:
   it is the prestress/load block subtracted from `K_n + B_partial,n`.
3. At the active solver level, the current `G_ps` candidate is best read as a
   background-dependent bilinear block acting on mixed test slots
   `(hat T_s, hat Q_s, hat M_s)` through the trial-side forcing expressions
   `(g_s, g_n, g_m)`.

The cleanest repository-level candidate statement is therefore

```text
G_ps^code(X, Xhat; q)  ~  ∫ [hat(T_s) * g_s(X) + hat(Q_s) * g_n(X) + hat(M_s) * g_m(X)] dx,
```

with the sign convention left explicit by the main theory identity

```text
A_n = K_n - G_ps,n + B_partial,n.
```

This is a compact structural statement of the current code/theory object.

## Why This Is Not The Old Scalar Closure Route

Within the current repository meaning, the active block is not the rejected
scalar-potential route for two separate reasons.

### 1. It acts through independent mixed test slots

The active forcing lives in the residual rows for `T_s`, `Q_s`, and `M_s`.
So the block is naturally expressed against independent test variables in the
mixed operator, not as one scalar object in a single primal slot.

### 2. It depends on more than `U = (u_s, u_n, v, phi, psi)` alone

The current `g_n` expression contains `e_s`, and therefore the active trial
variable `T_s`.

So even at the current solver level, the block is not naturally a function of
the displacement/rotation-type slot `U` alone.

That does not prove every other reformulation impossible. But it does support
the repository statement that the active branch is genuinely mixed and should
not be described as one scalar potential `G(U)`.

## Remaining Ambiguity

The pilot also exposes exactly where the repository statement is still not
closed.

### 1. No final article-level full formula for `G_ps`

The theory file explicitly says this is still missing. So `V-S1` cannot be
upgraded to a full proof from this pilot alone.

### 2. The precise final partition of background-coupling terms is not fully frozen

The active code clearly contains `g_s`, `g_n`, and the moment-row coupling
`g_m`, but the theory text only says that the forcing structure is reconstructed
from corrected strong meridional/normal equations.

So the current repository supports a strong solver-level interpretation, but it
does not yet fully spell out whether every background-coupling term has already
been assigned once and for all to the final `G_ps` block rather than to another
background-dependent part of the operator.

### 3. No runnable old scalar-potential comparator remains in the active checkout

The repository documents the rejection of the old route, but the current active
checkout does not expose a clean live alternative solver implementing that
scalar closure for a side-by-side test in this pilot.

That is why this pilot is structural/CAS-focused rather than numerical.
