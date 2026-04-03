# Current reduced renormalized system draft

## 1. Scope and status

This is a compact working draft for the next **conditional** theorem attempt on
the clean full simple-support `J_0` branch.

It is written **under Assumption LC only**. The strict ambient-to-local closure
theorem remains open, and nothing in this note should be read as discharging
that strict barrier.

This draft does **not** prove the extra-asymptotic-order lemma for the reduced
first post-leading slots `U1, N1, P1, Y1`. Its purpose is only to record the
reduced renormalized local system that should feed that next theorem attempt.

The augmented membrane slots `V1, T1` are deliberately **not** treated here,
except for the reminder that the reduced slot `U1` is only the visible part of
the first post-leading membrane thickening in the full recurrence model.

---

## 2. Reduced renormalized channels

On the punctured local witness germ `G`, fix the reduced renormalized channels

\[
S(x) = x^{-n}u_s(x),\qquad
N(x) = x^{-n}u_n(x),\qquad
P(x) = x^{1-n}\varphi(x),\qquad
Y(x) = x^{1-n}\psi(x).
\]

Let the leading coefficients already accepted on the current branch be

\[
U_0,\qquad N_0,\qquad P_0,\qquad Y_0.
\]

Define the leading-data-subtracted remainders

\[
R_s(x) = S(x) - U_0,\qquad
R_n(x) = N(x) - N_0,\qquad
R_\varphi(x) = P(x) - P_0,\qquad
R_\psi(x) = Y(x) - Y_0.
\]

To write the reduced local equations in renormalized form, also keep the
auxiliary renormalized source channels

\[
E_s^{ren}(x) = x^{1-n} e_s(x),
\qquad
e_s = T_s - \nu T_\theta,
\]

and

\[
E_\varphi^{ren}(x) = \Lambda\,x^{2-n}\bigl(M_s - \nu M_\theta\bigr).
\]

These are **not** new theorem-facing chart slots. They are only working local
source terms appearing in the reduced equations for `u_s` and `varphi`.

Their leading-data-subtracted forms are

\[
Q_s(x) = E_s^{ren}(x) - nU_0,
\qquad
Q_\varphi(x) = E_\varphi^{ren}(x) - (n-1)P_0.
\]

---

## 3. Reduced local equations on the punctured witness germ

The reduced line for `U1, N1, P1, Y1` is fed only by the four local clean mixed
equations already used in the checked recurrence helper:

\[
u_s'(x) - e_s(x) = 0,
\]

\[
u_n'(x) + \lambda_c\,\varphi(x) = 0,
\]

\[
\frac{n}{x}u_n(x) + \psi(x) = 0,
\]

\[
\varphi'(x) - \Lambda\bigl(M_s(x) - \nu M_\theta(x)\bigr) = 0.
\]

These are exactly the four rows of the checked local system that feed the
leading and first post-leading slots

\[
U_0,\ N_0,\ P_0,\ Y_0,\ U_1,\ N_1,\ P_1,\ Y_1
\]

in the reduced richer chart `Xi_rich^(1,eta)`.

This note does **not** reopen the full augmented membrane block. The only
membrane quantity kept explicitly here is the visible reduced slot `U1`, and
even that slot is treated only through the renormalized `u_s` channel.

---

## 4. Renormalized form of the reduced system

### Exact checked frozen-principal form

After dividing by the corresponding leading powers of `x`, the four reduced
equations become

\[
xS'(x) + nS(x) = E_s^{ren}(x),
\]

\[
xN'(x) + nN(x) + \lambda_c P(x) = 0,
\]

\[
Y(x) + nN(x) = 0,
\]

\[
xP'(x) + (n-1)P(x) = E_\varphi^{ren}(x).
\]

Subtracting the leading data gives the exact reduced remainder system in the
checked frozen-principal model:

\[
xR_s'(x) + nR_s(x) = Q_s(x),
\]

\[
xR_n'(x) + nR_n(x) + \lambda_c R_\varphi(x) = 0,
\]

\[
R_\psi(x) + nR_n(x) = 0,
\]

\[
xR_\varphi'(x) + (n-1)R_\varphi(x) = Q_\varphi(x).
\]

Equivalently, with

\[
\widehat Z(x) =
\begin{pmatrix}
R_s(x)\\
R_n(x)\\
R_\varphi(x)
\end{pmatrix},
\qquad
A_0 =
\begin{pmatrix}
-n & 0 & 0\\
0 & -n & -\lambda_c\\
0 & 0 & 1-n
\end{pmatrix},
\]

the differential part can be written as

\[
x\widehat Z'(x)

=
A_0 \widehat Z(x)
+
\begin{pmatrix}
Q_s(x)\\
0\\
Q_\varphi(x)
\end{pmatrix},
\]

with the algebraic companion relation

\[
R_\psi(x) = -nR_n(x).
\]

### Working punctured-witness-germ remainder form

For the actual punctured local witness germ under Assumption LC, the checked
frozen-principal system above should be read as the principal near-center
structure. The working next theorem target is to justify a remainder form of
the shape

\[
xR_s'(x) + nR_s(x) = Q_s(x) + x\,b_s(x),
\]

\[
xR_n'(x) + nR_n(x) + \lambda_c R_\varphi(x) = x\,b_n(x),
\]

\[
R_\psi(x) + nR_n(x) = x\,b_\psi(x),
\]

\[
xR_\varphi'(x) + (n-1)R_\varphi(x) = Q_\varphi(x) + x\,b_\varphi(x),
\]

for some punctured local remainder terms `b_s, b_n, b_psi, b_varphi`.

This remainder form is **not yet proved theorem-facingly** on the current
branch. It is the exact working target that should feed the next extra-order
lemma.

---

## 5. Match to checked recurrence data

The correspondence to the checked recurrence-side slots should be read as
follows.

### Leading block

The already accepted leading quantities are the constant terms of the reduced
renormalized channels:

\[
S(x) = U_0 + o(1),\qquad
N(x) = N_0 + o(1),\qquad
P(x) = P_0 + o(1),\qquad
Y(x) = Y_0 + o(1).
\]

The defect slots in `Xi_rich^(1,eta)` are then

\[
\Delta_{un}^{(0)} = N_0 + \frac{\lambda_c}{n}P_0,
\qquad
\Delta_{\psi,\eta}^{(0)} = Y_0 - \eta P_0.
\]

### First post-leading block

If the reduced renormalized channels admit one extra order,

\[
S(x) = U_0 + xU_1 + o(x),
\]

\[
N(x) = N_0 + xN_1 + o(x),
\]

\[
P(x) = P_0 + xP_1 + o(x),
\]

\[
Y(x) = Y_0 + xY_1 + o(x),
\]

and if the auxiliary renormalized source remainders satisfy

\[
Q_s(x) = xq_s + o(x),
\qquad
Q_\varphi(x) = xq_\varphi + o(x),
\]

then the reduced remainder system gives the first post-leading coefficient
relations

\[
(n+1)U_1 = q_s,
\]

\[
(n+1)N_1 + \lambda_c P_1 = 0,
\]

\[
Y_1 + nN_1 = 0,
\]

\[
nP_1 = q_\varphi.
\]

This is the precise reduced local meaning of the recurrence-side slots

\[
U_1,\ N_1,\ P_1,\ Y_1
\]

underlying `Xi_rich^(1,eta)`.

In the checked recurrence model, the flexural/algebraic reduced block remains
rigid under nonresonance, while `U1` is the visible reduced slot of the first
membrane thickening. This note does **not** attempt to resolve the hidden
augmented membrane parameters behind that visible reduced slot.

---

## 6. Minimal next theorem target

The next exact reduced theorem target is:

> Under Assumption LC, prove that the reduced renormalized witness-germ
> channels admit one extra near-center asymptotic order
> \[
> f(x) = f_0 + x f_1 + o(x),
> \]
> sufficient to define `U1, N1, P1, Y1` as actual punctured local first
> post-leading coefficients.

The first expected analytic blocker is now:

- **not** selector/codomain/`J_0` structure;
- **not** the strict ambient-to-local closure theorem;
- but proving the first-order remainder control for the reduced renormalized
  system once that system is fixed, namely enough control on
  `Q_s, Q_\varphi` and the remainder terms
  `b_s, b_n, b_\psi, b_\varphi` to conclude the desired
  `f(x) = f_0 + x f_1 + o(x)` asymptotics for the reduced channels.

So the expected first hard point after this draft is no longer derivation of
the reduced principal system itself. It is the first-order remainder control
needed to extract the reduced first post-leading coefficients from the punctured
local witness germ.
