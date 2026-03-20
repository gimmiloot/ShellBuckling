The current repository-level prestress / load block can be summarized as follows.
Within the mixed weak-form
`A_n(X, Xhat; q) = K_n(X, Xhat) - G_ps,n(X, Xhat; q) + B_partial,n(X, Xhat) = 0`,
the active solver/testbench path realizes `G_ps` through the mixed pairing
`hat(T_s) g_s + hat(Q_s) g_n + hat(M_s) g_m`, with
`g_s = -(T_theta^0/r_0) r_x - T_sn^0 varphi'`,
`g_n = T_s^0 varphi' + (c_0/x) T_theta^0 varphi - (q^0/x)(r_0 e_s^code + lambda_s0 r)`,
and `g_m = (M_theta^0/r_0) r_x`.
This is bilinear in the current mixed trial/test slots and is not a scalar closure `G(U)` of the `U` slot alone, but it is still only a repository-level closed statement rather than the final article-level full formula for all of `G_ps`.
