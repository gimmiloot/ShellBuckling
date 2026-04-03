# Current richer-variable realization draft

This is a compact working draft for the next **conditional** theorem attempt on
the clean full simple-support `J_0` branch.

It is written **under Assumption LC only**. It does **not** prove the strict
ambient-to-local closure theorem, does **not** prove the conditional
chart-realization lemma, and does **not** change any theorem status by itself.

Its only purpose is to fix the exact local realization tasks behind the current
conditional blocker:

```text
checked first post-leading recurrence data
  =>
actual punctured local chart data on the punctured local witness germ.
```

---

## 1. Target sublemma

**Sublemma R (conditional first post-leading richer-variable realization).**
Fix `(n,q)` and assume Assumption LC.
For every `c in A_full^th,n(q)`, let `G` be the punctured local witness germ
supplied by the conditional LC line.

Then `G` has enough local structure to define the first post-leading richer
variables as actual punctured local quantities, and these agree with the
checked formal recurrence-side variables underlying

\[
\Xi_{\mathrm{rich}}^{(1,\eta)}
\quad\text{and, when needed,}\quad
\Xi_{\mathrm{rich}}^{(1+,\eta)}.
\]

Here the current formal richer charts are:

```text
Xi_rich^(1,eta)
  = [U0, P0, Delta_un^(0), Delta_psi,eta^(0), U1, N1, P1, Y1],

Xi_rich^(1+,eta)
  = [U0, P0, Delta_un^(0), Delta_psi,eta^(0), U1, N1, P1, Y1, V1, T1].
```

This sublemma is still conditional on Assumption LC and should not be read as a
strict theorem on `A_full^th,n(q)`.

---

## 2. Table A: richer variables inventory

| Slot | Formal role in checked recurrence model | Candidate local meaning on punctured witness germ `G` | Directly definable from local mixed data? | Needs extraction / identification argument? |
| --- | --- | --- | --- | --- |
| `U0` | leading `u_s` amplitude in `Xi_rich^(1,eta)` | leading coefficient of `x^{-n} u_s(x)` on `G` | yes, on the current conditional witness-germ reading | no new identification beyond fixing the leading block |
| `P0` | leading `varphi` amplitude | leading coefficient of `x^{1-n} varphi(x)` | yes, on the current conditional witness-germ reading | no new identification beyond fixing the leading block |
| `Delta_un^(0)` | leading normal-defect slot | `N0 + (lambda_c / n) P0`, with `N0` extracted from `x^{-n} u_n(x)` | yes once leading coefficients are fixed | only the leading-coefficient extraction itself |
| `Delta_psi,eta^(0)` | eta-normalized leading fourth defect slot | `Y0 - eta P0`, with `Y0` extracted from `x^{1-n} psi(x)` | yes once leading coefficients are fixed | only the leading-coefficient extraction itself |
| `U1` | first post-leading `u_s` coefficient | coefficient of `x` in the local expansion of `x^{-n} u_s(x)` | not yet | yes |
| `N1` | first post-leading `u_n` coefficient | coefficient of `x` in the local expansion of `x^{-n} u_n(x)` | not yet | yes |
| `P1` | first post-leading `varphi` coefficient | coefficient of `x` in the local expansion of `x^{1-n} varphi(x)` | not yet | yes |
| `Y1` | first post-leading `psi` coefficient | coefficient of `x` in the local expansion of `x^{1-n} psi(x)` | not yet | yes |
| `V1` | first post-leading membrane/tangential coefficient in the augmented jet | coefficient of `x` in the corresponding punctured local membrane channel, when that channel is kept explicit on `G` | not yet | yes |
| `T1` | free membrane nullmode parameter in the augmented jet | first post-leading membrane-stress/resultant coefficient, or equivalently the local parameter selecting the membrane nullmode | not yet | yes |

Auxiliary leading coefficients `N0` and `Y0` are not separate slots of
`\Xi_{\mathrm{rich}}^{(1,\eta)}`, but they are needed to interpret the defect
coordinates `Delta_un^(0)` and `Delta_psi,eta^(0)` locally.

---

## 3. Table B: required local regularity

| Variable / class | Local regularity needed on `G` | Extraction type needed | Current source-of-truth read |
| --- | --- | --- | --- |
| leading renormalized channels `x^{-n} u_s`, `x^{-n} u_n`, `x^{1-n} varphi`, `x^{1-n} psi` | punctured boundedness plus one-sided near-center leading-coefficient extraction | leading asymptotic coefficient / punctured limit | conditionally supported on the current LC witness-germ line |
| defect slots `Delta_un^(0)`, `Delta_psi,eta^(0)` | same leading extraction as above | algebraic combination of extracted leading coefficients | conditionally supported once the leading coefficients are admitted |
| first post-leading channel coefficients `U1`, `N1`, `P1`, `Y1` | one additional local asymptotic order for the renormalized channels | first derivative at `0+` of the renormalized channel, or an equivalent `f(x) = f(0) + x f_1 + o(x)` extraction | still open |
| augmented membrane coefficients `V1`, `T1` | one additional local asymptotic order in the explicit membrane / mixed variables retained by the LC continuation | coefficient extraction from the local membrane block, or equivalent nullmode parameter extraction | still open |
| agreement with recurrence-side variables | enough regularity to compare extracted local coefficients with the checked recurrence slots | identification of extracted coefficients with the symbolic recurrence coordinates | still open |

Continuity alone is not enough for the first post-leading layer. The working
need is one extra near-center asymptotic order beyond the already accepted
leading scaling class.

---

## 4. Table C: formal-to-local identification status

| Variable / class | Current identification status |
| --- | --- |
| `U0`, `P0` | already identical to the current leading local witness data once the renormalized leading block is fixed |
| `Delta_un^(0)`, `Delta_psi,eta^(0)` | already identical by explicit formula once the leading coefficients `N0`, `P0`, `Y0` are extracted |
| `U1`, `N1`, `P1`, `Y1` | locally meaningful only after first post-leading extraction; then still need proof of agreement with the checked recurrence variables |
| `V1`, `T1` | not yet locally definable from the current reduced witness-germ packaging alone; they require either explicit access to the relevant membrane/mixed channels on `G` or an equivalent local nullmode-extraction argument |

So the current conditional gap is not at the level of `Pi_eta_to_J0` or the
overlap trace. It is the bridge

```text
formal checked recurrence variables
  ->
extracted punctured local first post-leading quantities.
```

---

## 5. Short proof skeleton for sublemma R

1. Under Assumption LC, pick the punctured local witness germ `G` for
   `c in A_full^th,n(q)`.
2. Fix the already accepted leading local data and hence the directly
   definable slots `U0`, `P0`, `Delta_un^(0)`, `Delta_psi,eta^(0)`.
3. Isolate the first post-leading slots `U1`, `N1`, `P1`, `Y1` and, when the
   augmented chart is used, `V1`, `T1`, as the only genuinely new local data.
4. Prove the required punctured local extraction statement:
   the witness germ has one extra near-center asymptotic order sufficient to
   define those first post-leading coefficients.
5. Prove identification of the extracted local coefficients with the checked
   recurrence-side variables underlying `Xi_rich^(1,eta)` and
   `Xi_rich^(1+,eta)`.
6. Assemble the actual punctured local chart data, after which
   `Pi_eta_to_J0` compatibility and overlap return to `J_0 = C_center` are
   already formal on the current branch reading.

---

## 6. First expected blocker

The first expected analytic blocker is:

> whether the punctured local witness germ supplied by Assumption LC has enough
> away-from-center regularity and one extra near-center asymptotic order to
> extract the first post-leading coefficients
> `(U1, N1, P1, Y1)` and, when needed, `(V1, T1)` as genuine local punctured
> quantities, and then identify them with the checked recurrence-side
> variables.

So the expected first hard point is not projection, not overlap compatibility,
and not the formal recurrence algebra itself. It is the local extraction and
recurrence-to-local identification step for the first post-leading coefficients
on the punctured witness germ.
