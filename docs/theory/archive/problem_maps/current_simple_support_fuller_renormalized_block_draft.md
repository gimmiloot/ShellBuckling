# Current fuller renormalized block draft

## 1. Scope and status

This is a compact working draft for the next **conditional** theorem attempt on
the clean full simple-support `J_0` branch.

It is written **under Assumption LC only**. The strict ambient-to-local
continuation theorem remains open, and nothing in this note should be read as
closing that strict barrier.

This draft does **not** prove first post-leading asymptotic closure on the
fuller local block. Its purpose is only to fix the smallest fuller
renormalized local mixed block that honestly repairs the structural non-closure
of the reduced four-channel line.

---

## 2. Exact fuller renormalized block

To match the checked recurrence-side notation, write the fuller renormalized
local mixed block on the punctured local witness germ `G` as

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
M(x) = x^{2-n}M_s(x).
\]

The corresponding leading coefficients are

\[
U_0,\ N_0,\ V_0,\ P_0,\ Y_0,\ T_0,\ Q_{0c},\ M_0.
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
R_M(x) = M(x) - M_0.
\]

To avoid collision with the physical shear-resultant channel `Q(x)`, this note
denotes the two reduced auxiliary source remainders from the reduced draft by

\[
Q_s^{src}(x),\qquad Q_\varphi^{src}(x).
\]

These are the objects previously written simply as `Q_s` and `Q_\varphi` in the
reduced renormalized system draft.

---

## 3. Local equations actually needed

The smallest fuller local block is fed by the same eight local equations used
in the checked recurrence helper:

\[
u_s' - e_s = 0,\qquad
u_n' + \lambda_c \varphi = 0,\qquad
\frac{n}{x}u_n + \psi = 0,\qquad
\varphi' - \Lambda(M_s - \nu M_\theta) = 0,
\]

\[
T_s' + \frac{T_s}{x} - \frac{T_\theta}{x} + \frac{n}{x}S = 0,
\]

\[
Q_s' + \frac{Q_s}{x} + \frac{n}{x}\chi = 0,
\]

\[
M_s' + \frac{M_s}{x} - \frac{M_\theta}{x} - Q_s + \frac{n}{x}H = 0,
\]

\[
S' + \frac{2}{x}S - \frac{n}{x}T_\theta = 0.
\]

The constitutive/derived quantities entering these equations are

\[
T_\theta = \nu T_s + \frac{u_s}{x} + \frac{n v}{x},
\]

\[
S = \frac{v' - v/x - n u_s/x}{2(1+\nu)},
\]

\[
M_\theta = \nu M_s + \frac{\varphi + n\psi}{\Lambda x},
\]

\[
H = \frac{\psi' - \psi/x - n\varphi/x}{C_{tw}},
\]

\[
\chi = \frac{n M_\theta}{x} - H' - \frac{2H}{x}.
\]

In renormalized form, these become the working derived quantities

\[
T_\theta^{ren}(x) = \nu T(x) + U(x) + nV(x),
\]

\[
S^{ren}(x) = x^{1-n}S(x)
           = \frac{xV'(x) + (n-1)V(x) - nU(x)}{2(1+\nu)},
\]

\[
M_\theta^{ren}(x) = x^{2-n}M_\theta(x)
                  = \nu M(x) + \frac{P(x) + nY(x)}{\Lambda},
\]

\[
H^{ren}(x) = x^{2-n}H(x)
           = \frac{xY'(x) + (n-2)Y(x) - nP(x)}{C_{tw}},
\]

\[
\chi^{ren}(x) = x^{3-n}\chi(x)
              = nM_\theta^{ren}(x) - x(H^{ren})'(x) - nH^{ren}(x).
\]

With these conventions, the renormalized propagation equations needed for the
fuller block can be written compactly as

\[
xU' + nU = T - \nu T_\theta^{ren},
\]

\[
xN' + nN + \lambda_c P = 0,
\]

\[
Y + nN = 0,
\]

\[
xP' + (n-1)P = \Lambda\bigl(M - \nu M_\theta^{ren}\bigr),
\]

\[
xT' + nT - T_\theta^{ren} + nS^{ren} = 0,
\]

\[
xQ' + (n-1)Q + n\chi^{ren} = 0,
\]

\[
xM' + (n-1)M - M_\theta^{ren} - xQ + nH^{ren} = 0,
\]

\[
x(S^{ren})' + (n+1)S^{ren} - nT_\theta^{ren} = 0.
\]

This is not a full new derivation of the whole model. It is only the smallest
local equation package needed to propagate/control the fuller renormalized
block that repairs the reduced-line failure.

---

## 4. Structural dependency map

### How `Q_s^{src}` is fed

The reduced source remainder entering the `U` equation is

\[
Q_s^{src}(x) = x^{1-n}e_s(x) - nU_0,
\]

with

\[
x^{1-n}e_s(x) = T(x) - \nu T_\theta^{ren}(x)
              = (1-\nu^2)T(x) - \nu U(x) - n\nu V(x).
\]

So `Q_s^{src}` is **not** a function of the reduced channels
`(U,N,P,Y)` alone. It depends on the membrane auxiliary block

\[
(V,T),
\]

and its actual first post-leading control comes through the coupled local
propagation equations for

\[
(U,V,T),
\]

namely the renormalized `u_s`, `T_s`, and `v` equations.

### How `Q_\varphi^{src}` is fed

The reduced source remainder entering the `P` equation is

\[
Q_\varphi^{src}(x)
=
\Lambda x^{2-n}\bigl(M_s - \nu M_\theta\bigr) - (n-1)P_0
=
\Lambda\bigl(M - \nu M_\theta^{ren}\bigr) - (n-1)P_0.
\]

Since

\[
M_\theta^{ren}(x) = \nu M(x) + \frac{P(x) + nY(x)}{\Lambda},
\]

the source term `Q_\varphi^{src}` depends on

\[
(P,Y,M).
\]

But `M` is not propagated by the reduced block alone. Its local evolution is
coupled to the shear-resultant channel `Q` through the renormalized `M_s` and
`Q_s` equations, with `H^{ren}` and `\chi^{ren}` built from `(P,Y)` and their
punctured local derivatives.

So first post-leading control of `Q_\varphi^{src}` really lives on the fuller
flexural/shear block

\[
(N,P,Y,Q,M),
\]

not on the reduced channels alone.

### Why the reduced block failed

The reduced four-channel line failed structurally because it treated

\[
Q_s^{src},\qquad Q_\varphi^{src}
\]

as if they were external first-order source terms, while in fact they are
generated by omitted local mixed channels and their companion propagation
equations.

### Why this fuller block is the smallest natural repair

The reduced line already kept

\[
(U,N,P,Y).
\]

To close `Q_s^{src}` one must add the membrane auxiliary channels

\[
(V,T).
\]

To close `Q_\varphi^{src}` one must add the bending/shear auxiliary channels

\[
(Q,M).
\]

No smaller addition repairs both failures simultaneously. So the smallest
natural renormalized local mixed block is exactly

\[
(U,N,V,P,Y,T,Q,M).
\]

---

## 5. First-post-leading target on the fuller block

To recover the reduced coefficients

\[
U_1,\ N_1,\ P_1,\ Y_1,
\]

it is enough to seek first post-leading asymptotics on the fuller block of the
form

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
M(x) = M_0 + xM_1 + o(x).
\]

The reduced coefficients are then recovered simply by projection:

\[
(U_1,N_1,P_1,Y_1)
\]

are the corresponding first post-leading coefficients of the fuller block.

The added coefficients

\[
V_1,\ T_1,\ Q_1,\ M_1
\]

are not optional decoration. They are the local mixed data required to close
the source terms that feed the reduced block.

---

## 6. Minimal next theorem target

The next exact theorem-facing target is:

> Under Assumption LC, prove first post-leading asymptotic closure on the
> smallest fuller renormalized local mixed block
> \[
> (U,N,V,P,Y,T,Q,M),
> \]
> that is, prove enough punctured near-center control to obtain
> \[
> f(x) = f_0 + x f_1 + o(x)
> \]
> for each of the eight renormalized channels above.

Once that fuller-block closure is available, the reduced coefficients

\[
U_1,\ N_1,\ P_1,\ Y_1
\]

should follow by direct projection, and the reduced source remainders

\[
Q_s^{src},\qquad Q_\varphi^{src}
\]

will no longer be external obstructions.
