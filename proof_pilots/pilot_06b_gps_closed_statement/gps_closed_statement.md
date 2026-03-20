# Closed Repository-Level Statement Of `G_ps`

## Final statement

The strongest current repository-level closed statement of the active prestress / load block is:

```text
X = (U, P),
U = (u_s, u_n, v, varphi, psi),
P = (T_s, T_theta, S, Q_s, M_s, M_theta, H, chi).

G_ps,n^repo(X, Xhat; q)
  := int_[x0,1] [ hat(T_s) * g_s^repo(X; q)
                + hat(Q_s) * g_n^repo(X; q)
                + hat(M_s) * g_m^repo(X; q) ] dx,
```

with overall sign fixed only through the current theory convention

```text
A_n(X, Xhat; q) = K_n(X, Xhat) - G_ps,n(X, Xhat; q) + B_partial,n(X, Xhat) = 0.
```

The trial-side forcing terms are

```text
r(X)          = c_0 u_s + s_0 u_n,
r_x(X)        = -kappa_s0 s_0 u_s + c_0 u_s' + kappa_s0 c_0 u_n + s_0 u_n',
T_theta(X)    = nu T_s + r(X)/x + (n/x) v,
e_s^code(X)   = T_s - nu T_theta(X),

g_s^repo(X;q) = -(T_theta^0/r_0) * r_x(X) - T_sn^0 * varphi',
g_n^repo(X;q) =  T_s^0 * varphi' + (c_0/x) * T_theta^0 * varphi
                 - (q^0/x) * (r_0 * e_s^code(X) + lambda_s0 * r(X)),
g_m^repo(X;q) =  (M_theta^0/r_0) * r_x(X).
```

This is the current repository-level closed statement only. It is not yet the
final article-level formula for the complete `G_ps` block.

## A. Directly grounded in the active code

The active cores

- `src/shell_buckling/mixed_weak/solver_simple_support_core.py`
- `src/shell_buckling/mixed_weak/solver_patched_core.py`

contain exactly the code-level forcing terms

```text
g_s = -(b["T_theta"] / r0) * r_x - b["T_sn"] * phi_x
g_n =  b["T_s"] * phi_x + (c0 / x_safe) * b["T_theta"] * phi
       - (b["q"] / x_safe) * (r0 * e_s + lam_s0 * r)
g_m =  (b["M_theta"] / r0) * r_x
```

inserted into the mixed residual rows

```text
R_Ts = ... - g_s
R_Qs = ... - g_n
R_Ms = ... - g_m.
```

In the active code:

- `phi` is the code name for theory `varphi`;
- `T_sn^0 = Q_0`, because `BaseInterp` stores the background axisymmetric shear
  quantity as `T_sn=Q0`;
- the active primary code unknowns are
  `(u_s, u_n, v, phi, psi, T_s, Q_s, M_s)`;
- `T_theta, S, M_theta, H, chi` are reconstructed algebraically.

So the active code grounds the concrete forcing formulas and the active mixed
trial/test slots touched by this block.

## B. Directly grounded in `vyvod_uravneniy_updated17.md`

The theory notebook currently fixes the following points.

1. The active branch is a mixed weak-form:

   ```text
   A_n(X, Xhat; q) = K_n(X, Xhat) - G_ps,n(X, Xhat; q) + B_partial,n(X, Xhat) = 0.
   ```

2. The trial-side block decomposition is written with

   ```text
   U = (u_s, u_n, v, varphi, psi),
   P = (T_s, T_theta, S, Q_s, M_s, M_theta, H, chi).
   ```

3. The prestress / load part is explicitly said **not** to close into one scalar
   potential `G(U)`, but to enter as a separate bilinear weak-form `G_ps`.

4. The forcing structure is described as reconstructed from corrected strong
   meridional / normal equations, but the notebook also states that the full
   article-level final formula for `G_ps` is still not written down completely.

## C. Interpretation needed to reconcile code and theory

The theory gives the abstract mixed weak-form and the code gives the concrete
forcing rows. The repository-level reconciliation is therefore:

- the current code realizes the active `G_ps` contribution through the mixed
  residual duals of `T_s`, `Q_s`, and `M_s`;
- the corresponding repository-level bilinear block is the integral pairing of
  `hat(T_s), hat(Q_s), hat(M_s)` with `g_s^repo, g_n^repo, g_m^repo`;
- `e_s^code(X) = T_s - nu T_theta(X)` is the quantity actually used in the
  active code-level forcing block.

This is the step where the repository is closed enough for discussion, even
though it is not closed enough for an article-level final theorem.

## Trial-side and test-side slots

The current active `G_ps` statement uses:

- trial-side content: `u_s, u_n, v, varphi, T_s` together with
  `u_s', u_n', varphi'`;
- test-side content: `hat(T_s), hat(Q_s), hat(M_s)`.

It does **not** act as a scalar closure in `U` alone, because:

1. the block is evaluated against independent mixed test slots;
2. `g_n^repo` depends explicitly on the stress-like trial variable `T_s`, which
   is not part of `U`.

## D. What still remains open

The repository still does **not** settle the following points.

- The final article-level full formula for all of `G_ps` is still open.
- The exact final partition between `G_ps` and other background-dependent
  operator pieces is still not fully frozen.
- The present statement is grounded in the active code and theory documents, but
  it is still a repository-level consolidation rather than a from-scratch shell
  theorem.
