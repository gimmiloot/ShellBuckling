# Current chart-realization proof draft

## Purpose of this note

This is a working theorem-facing draft for the current local proof line on the clean full simple-support branch.

It is **not**:
- a proof of the full weak/KKT selector theorem;
- a criterion-authority result;
- a numerical winner note.

Its only purpose is to keep the current proof target, proof decomposition, and first expected analytic obstruction in one stable repo location.

---

## Current target lemma

**Lemma (ambient punctured-neighborhood first post-leading chart realization).**  
Fix `(n,q)`. For every
\[
c \in A_{\mathrm{full}}^{th,n}(q),
\]
there exist `\delta > 0` and punctured near-center chart data on `(0,\delta)` realizing
\[
\Xi_{\mathrm{rich}}^{(1,\eta)}
\quad\text{and, when needed,}\quad
\Xi_{\mathrm{rich}}^{(1+,\eta)},
\]
such that:

1. they extend
   \[
   W_c(x)
   =
   \bigl(
   x^{-n}u_s(x),\;
   x^{-n}u_n(x),\;
   x^{1-n}\varphi(x),\;
   x^{1-n}\psi(x)
   \bigr);
   \]

2. they are compatible with the canonical projection
   \[
   \Pi_{\eta\to J_0};
   \]

3. on the weighted-trial overlap they return to the exact ansatz-boundary trace
   \[
   J_0 = C_{\mathrm{center}};
   \]

4. they provide exactly the punctured near-center first post-leading richer chart
   needed for the later regular-singular step.

---

## What is already closed and should not be reproved here

The following should be treated as already closed or already fixed for this draft:

- the clean path itself is not the active blocker;
- the selector layer is not the current proof target;
- the preferred codomain route has already been chosen;
- the theorem-facing codomain is currently read through the pair
  \[
  (A_{\mathrm{full}}^{th,n}(q), J_0);
  \]
- on the ansatz / selected-family boundary the exact trace identities
  \[
  J_0 = C_{\mathrm{center}},
  \qquad
  J_0(A_{ls}) = \operatorname{im}(D_{\mathrm{amp}})
  \]
  are already accepted;
- the projection
  \[
  \Pi_{\eta\to J_0}
  \]
  is already formally exact on the checked richer-jet side;
- the current proof line must now be read as
  \[
  \text{richer-jet lift}
  +
  \text{regular-singular convergence}
  +
  \text{overlap compatibility}
  \Rightarrow
  J_0^{th}\ \text{well-defined}.
  \]

So the current blocker is no longer projection, no longer overlap wording, and no longer selector authority. It is the theorem-facing realization of the first post-leading richer chart for arbitrary ambient objects.

---

## Ambient assumptions actually used

For this draft, the ambient assumptions should be kept minimal and explicit.

Let
\[
c \in A_{\mathrm{full}}^{th,n}(q).
\]

The proof should use only the following ambient information:

1. `c` belongs to the full clean admissible / center-regular tangent class on the current branch;

2. `c` is compatible with the clean mixed equations in the theorem-facing ambient sense currently intended on this branch;

3. the current near-center scaling orders are already the intended ones, namely
   \[
   u_s,\ u_n = O(x^n),
   \qquad
   \varphi,\ \psi = O(x^{n-1});
   \]

4. the theorem-facing local discussion is allowed on a punctured near-center interval
   \[
   (0,\delta).
   \]

No selector-authority claim, no numerical ranking claim, and no stronger theorem than the current local chart-realization target should be used here.

---

## Step 1. Punctured local representative

The first real step is to pass from the ambient object
\[
c \in A_{\mathrm{full}}^{th,n}(q)
\]
to a punctured-neighborhood local representative on some interval `(0,\delta)`.

This step is needed because the richer-jet variables should not remain only formal recurrence symbols. They must become actual local quantities attached to the ambient object.

At this stage the intended output is only:

- a punctured local representative for the channels
  \[
  u_s,\ u_n,\ \varphi,\ \psi;
  \]
- enough local meaning to define the renormalized leading block;
- no convergence or selector conclusion yet.

This is the first place where a genuinely new analytic ingredient may be needed.

---

## Step 2. Renormalized leading block

On the punctured representative, define
\[
W_c(x)
=
\bigl(
x^{-n}u_s(x),\;
x^{-n}u_n(x),\;
x^{1-n}\varphi(x),\;
x^{1-n}\psi(x)
\bigr).
\]

This is the theorem-facing leading block corresponding to the current `J_0` coordinates.

The point of this step is to fix the exact leading object that the richer chart must extend. The current proof line should not allow a different leading block unrelated to the already accepted `J_0 = C_center` reading.

At this stage only the object is fixed; convergence is not yet required.

---

## Step 3. First post-leading richer variables

The next step is to realize the first post-leading richer variables corresponding to
\[
\Xi_{\mathrm{rich}}^{(1,\eta)}
\quad\text{and, when needed,}\quad
\Xi_{\mathrm{rich}}^{(1+,\eta)}.
\]

These variables should be introduced as actual punctured local chart data, not merely as formal coefficients in a recurrence table.

The intended output of this step is a finite richer state
\[
Z_c(x) = (W_c(x), R_c(x)),
\]
where `R_c(x)` contains the first post-leading richer variables needed for the later local regular-singular step.

This step still does not require proving convergence. It only aims to realize the chart itself.

---

## Step 4. Projection and overlap return

Once the richer state exists, the remaining structure should become formal:

1. projection back to the current leading trace:
   \[
   \Pi_{\eta\to J_0}(Z_c(x)) = W_c(x);
   \]

2. overlap return to the exact ansatz-boundary trace:
   \[
   J_0 = C_{\mathrm{center}}
   \]
   whenever the richer local description and the weighted-trial description are both defined.

These are not supposed to be the first blockers anymore. If they become blockers again, the proof line has slipped backwards.

---

## Main proof decomposition

The intended proof decomposition is:

1. **punctured local representative exists;**
2. **renormalized leading block is defined;**
3. **first post-leading richer chart is realized;**
4. **projection and overlap return are then formal;**
5. **after that, the later regular-singular step can be attacked on the richer chart.**

So the current local theorem target is not yet convergence and not yet `J_0^{th}` itself. It is the existence of the first post-leading chart-realization layer.

---

## Most likely first real analytic obstruction

The expected first non-formal obstruction is:

> given
> \[
> c \in A_{\mathrm{full}}^{th,n}(q),
> \]
> does there exist a punctured-neighborhood local representative with enough regularity and local structure to realize
> \[
> \Xi_{\mathrm{rich}}^{(1,\eta)}
> \quad\text{and, when needed,}\quad
> \Xi_{\mathrm{rich}}^{(1+,\eta)}
> \]
> as genuine local chart data?

In other words, the likely genuine bottleneck is not selector authority, not projection, and not overlap compatibility, but the local existence of the first post-leading richer chart itself.

---

## What would count as success of this draft line

This draft line is successful if one of the following happens:

### Strong success
The chart-realization lemma is proved:
for every
\[
c \in A_{\mathrm{full}}^{th,n}(q)
\]
there exists a punctured-neighborhood first post-leading richer chart extending `W_c` and compatible with
\[
\Pi_{\eta\to J_0}
\quad\text{and}\quad
J_0 = C_{\mathrm{center}}
\]
on the weighted-trial overlap.

### Still useful progress
The proof reduces honestly to one narrower analytic lemma, for example:
- punctured local representative existence with sufficient regularity;
- ambient realization of `\Xi_{\mathrm{rich}}^{(1,\eta)}`;
- or another equally narrow local chart-existence statement.

That would still be meaningful progress, because it would keep the current proof line local and well-scoped.

---

## What this note is not trying to do

This note is not trying to:
- prove the full weak/KKT selector theorem;
- prove criterion authority;
- reopen the selector/codomain question;
- rerun numerical winner searches;
- replace the current source-of-truth status files.

It is only a compact working draft for the current local theorem line.

---

## Immediate next task

The immediate next theorem-facing task is:

> attempt a direct proof of the ambient punctured-neighborhood first post-leading
> chart-realization lemma in the above form, using only the currently accepted
> clean-path, trace, projection, and richer-jet structure.
