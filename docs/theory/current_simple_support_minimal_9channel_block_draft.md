# Current minimal 9-channel block draft

## 1. Scope and status

This is a compact working draft for the next **conditional** theorem attempt on
the clean full simple-support `J_0` branch.

It is written **under Assumption LC only**. The strict ambient-to-local
continuation theorem remains open, and nothing in this note should be read as
closing that strict barrier.

This draft does **not** prove first post-leading asymptotic closure on the
minimal 9-channel block. Its purpose is only to fix the exact renormalized
first-order local mixed block on which that next theorem attempt should be
posed.

The point of this note is structural only:

- the reduced 4-channel line was not closed;
- the proposed 8-channel repair was still not first-order closed because the
  membrane side still hid `S^{ren}`;
- `H^{ren}` and `\chi^{ren}` do **not** need their own extra state variables;
- the honest local first-order repair is therefore the 9-channel block
  `(U,N,V,P,Y,T,Q,M,S^{ren})`.

---

## 2. Exact 9-channel renormalized unknowns

On the punctured local witness germ `G`, define the renormalized channels

\[
U(x) = x^{-n}u_s(x),\qquad
N(x) = x^{-n}u_n(x),\qquad
V(x) = x^{-n}v(x),
\]

\[
P(x) = x^{1-n}\varphi(x),\qquad
Y(x) = x^{1-n}\psi(x),
\]

\[
T(x) = x^{1-n}T_s(x),\qquad
Q(x) = x^{2-n}Q_s(x),\qquad
M(x) = x^{2-n}M_s(x),
\]

\[
S^{ren}(x) = x^{1-n}S(x).
\]

Write the leading coefficients as

\[
U_0,\ N_0,\ V_0,\ P_0,\ Y_0,\ T_0,\ Q_{0c},\ M_0,\ S_0.
\]

Define the leading-data-subtracted remainders

\[
R_U(x) = U(x) - U_0,\qquad
R_N(x) = N(x) - N_0,\qquad
R_V(x) = V(x) - V_0,
\]

\[
R_P(x) = P(x) - P_0,\qquad
R_Y(x) = Y(x) - Y_0,
\]

\[
R_T(x) = T(x) - T_0,\qquad
R_Q(x) = Q(x) - Q_{0c},\qquad
R_M(x) = M(x) - M_0,
\]

\[
R_S(x) = S^{ren}(x) - S_0.
\]

For bookkeeping on the current branch, `Y_0` and `S_0` are kept explicit even
though they are not independent after the mixed compatibility and constitutive
relations are enforced.

---

## 3. Equations versus constraints

### A. Propagation equations

After renormalization, the minimal 9-channel propagation system can be written
as

\[
xU'(x) + nU(x) = T(x) - \nu T_\theta^{ren}(x),
\]

\[
xN'(x) + nN(x) + \lambda_c P(x) = 0,
\]

\[
xV'(x) + (n-1)V(x) - nU(x) - 2(1+\nu)S^{ren}(x) = 0,
\]

\[
xP'(x) + (n-1)P(x) = \Lambda\bigl(M(x) - \nu M_\theta^{ren}(x)\bigr),
\]

\[
xY'(x) + nY(x) - n\lambda_c P(x) = 0,
\]

\[
xT'(x) + nT(x) - T_\theta^{ren}(x) + nS^{ren}(x) = 0,
\]

\[
xQ'(x) + (n-1)Q(x) + n\chi^{ren}(x) = 0,
\]

\[
xM'(x) + (n-1)M(x) - M_\theta^{ren}(x) - xQ(x) + nH^{ren}(x) = 0,
\]

\[
x(S^{ren})'(x) + (n+1)S^{ren}(x) - nT_\theta^{ren}(x) = 0.
\]

These are the only propagation rows needed for the local first post-leading
closure attempt on the minimal repaired block.

### B. Algebraic / constitutive relations

The propagation rows use the algebraic renormalized constitutive quantities

\[
T_\theta^{ren}(x) = \nu T(x) + U(x) + nV(x),
\]

\[
M_\theta^{ren}(x) = \nu M(x) + \frac{P(x) + nY(x)}{\Lambda}.
\]

The mixed compatibility row is

\[
Y(x) + nN(x) = 0.
\]

This compatibility may be kept explicitly as an algebraic side relation. It is
preserved by the propagation system because differentiating it and using the
`N` and `Y` rows gives zero identically.

The role of `S^{ren}` is now explicit and honest:

- `S^{ren}` is treated as a genuine state variable;
- its propagation is given by
  `x(S^{ren})' + (n+1)S^{ren} - nT_\theta^{ren} = 0`;
- its constitutive origin from `u_s` and `v` is encoded in the first-order `V`
  row
  `xV' + (n-1)V - nU - 2(1+\nu)S^{ren} = 0`,
  which is just the renormalized first-order rewriting of
  `S = (v' - v/x - n u_s/x)/(2(1+\nu))`.

So once `S^{ren}` is promoted to a state, the membrane side no longer hides a
second-order `v`-dependence.

### C. Derived eliminated quantities

The remaining auxiliary quantities are now eliminated rather than added as
states.

First,

\[
H^{ren}(x) = x^{2-n}H(x)
           = \frac{xY'(x) + (n-2)Y(x) - nP(x)}{C_{tw}}.
\]

Using the `Y` propagation row,

\[
xY'(x) = -nY(x) + n\lambda_c P(x),
\]

so

\[
H^{ren}(x) =
\frac{-2Y(x) + n(\lambda_c - 1)P(x)}{C_{tw}}.
\]

Thus `H^{ren}` is algebraic in `(P,Y)`.

Second,

\[
\chi^{ren}(x) = x^{3-n}\chi(x)
              = nM_\theta^{ren}(x) - x(H^{ren})'(x) - nH^{ren}(x).
\]

Using the algebraic form of `H^{ren}` together with

\[
xP'(x) = \Lambda\bigl(M(x) - \nu M_\theta^{ren}(x)\bigr) - (n-1)P(x),
\]

\[
xY'(x) = -nY(x) + n\lambda_c P(x),
\]

one can rewrite `\chi^{ren}` purely algebraically in the current 9-channel
state. A convenient representative is

\[
\chi^{ren}(x)
=
nM_\theta^{ren}(x)
+
\frac{n\bigl((\lambda_c+1)P(x) - (\lambda_c-1)\Lambda(M(x)-\nu M_\theta^{ren}(x))\bigr)}{C_{tw}}.
\]

So neither `H^{ren}` nor `\chi^{ren}` requires an extra lifted state variable.

---

## 4. First-order closure check

On the current branch reading, the 9-channel block is now **genuinely
first-order closed** after correct rewriting.

The reason is:

1. the only true local state variables are
   `(U,N,V,P,Y,T,Q,M,S^{ren})`;
2. every derivative appears only as `x` times the first derivative of one of
   those state variables;
3. `T_\theta^{ren}` and `M_\theta^{ren}` are algebraic constitutive
   expressions;
4. `H^{ren}` is algebraic after substitution of the `Y` row;
5. `\chi^{ren}` is algebraic after substitution of the `P` and `Y` rows;
6. the explicit `S^{ren}` state removes the hidden second-order dependence
   through `v`.

So no hidden `H`-level, `\chi`-level, or second-derivative level remains.

The only extra side relation left is the mixed compatibility constraint

\[
Y + nN = 0,
\]

which is preserved by the propagation system and does not introduce a higher
differential layer. In that sense the current object is a closed first-order
renormalized mixed block, with one preserved algebraic compatibility relation.

If one wanted a smaller pure-ODE presentation, one could eliminate `Y` using
that compatibility. This note deliberately keeps `Y` explicit because it stays
closest to the checked recurrence-side slots and to the current local mixed
notation on the branch.

---

## 5. First-post-leading target on the 9-channel block

To recover the reduced coefficients

\[
U_1,\ N_1,\ P_1,\ Y_1,
\]

it is enough to seek first post-leading asymptotics on the 9-channel block of
the form

\[
U(x) = U_0 + xU_1 + o(x),\qquad
N(x) = N_0 + xN_1 + o(x),\qquad
V(x) = V_0 + xV_1 + o(x),
\]

\[
P(x) = P_0 + xP_1 + o(x),\qquad
Y(x) = Y_0 + xY_1 + o(x),
\]

\[
T(x) = T_0 + xT_1 + o(x),\qquad
Q(x) = Q_{0c} + xQ_1 + o(x),\qquad
M(x) = M_0 + xM_1 + o(x),
\]

\[
S^{ren}(x) = S_0 + xS_1 + o(x).
\]

Then the reduced chart coefficients are recovered by direct projection:

\[
(U_1,N_1,P_1,Y_1)
\]

are the corresponding first post-leading coefficients of the 9-channel block.

The added coefficients

\[
V_1,\ T_1,\ Q_1,\ M_1,\ S_1
\]

are not optional decoration. They are exactly the local mixed data needed to
close the source structure that feeds the reduced richer chart.

---

## 6. Minimal next theorem target

The next exact theorem-facing target is:

> Under Assumption LC, prove first post-leading asymptotic closure on the
> minimal 9-channel first-order renormalized local mixed block
> \[
> (U,N,V,P,Y,T,Q,M,S^{ren}),
> \]
> that is, prove enough punctured near-center control to obtain
> \[
> f(x) = f_0 + x f_1 + o(x)
> \]
> for each of the nine renormalized channels above.

Once that 9-channel first post-leading closure is available, the reduced
coefficients

\[
U_1,\ N_1,\ P_1,\ Y_1
\]

should follow by direct projection, and the earlier reduced source remainders
are no longer external obstructions.
