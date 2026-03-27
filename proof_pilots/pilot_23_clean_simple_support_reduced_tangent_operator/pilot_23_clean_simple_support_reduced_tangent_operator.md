# Pilot 23: Clean `simple support / подвижный шарнир` Reduced Tangent Operator, C3 Kernel Logic, and C3b Losslessness Boundary

## Goal

This pilot now records the clean `simple support / подвижный шарнир` theory work
through C3b on the active standalone path:

1. freeze the exact theorem-level target object for criticality;
2. derive the reduced tangent operator from the live clean architecture;
3. state and check the exact C3 kernel-equivalence already justified on the
   current chosen reduced family;
4. determine as sharply as possible what the current reduced family is, and what
   is still missing before it can be called theorem-level lossless.

This pilot does not change equations, boundary-condition meaning, or clean
solver behavior.

## Repository sources used as ground truth

- `AGENTS.md`
- `docs/theory/AGENTS.md`
- `docs/theory/current_simple_support_status.md`
- `docs/theory/current_theory_verification_map.md`
- `docs/theory/current_mixed_weak_theory_note.tex`
- `docs/theory/boundary_condition_task_audit.md`
- `docs/theory/boundary_conditions_summary.md`
- `docs/project_map.md`
- `docs/journal/project_journal_updated14.md`
- `docs/assumptions/assumptions.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`
- `src/shell_buckling/mixed_weak/simple_support_high_load_background_continuation.py`
- `src/shell_buckling/mixed_weak/full_simple_support_critical_search.py`
- `src/shell_buckling/mixed_weak/solver_patched_core.py`

## Frozen clean objects from C1/C2/C3

For a fixed circumferential mode `n` and load `q`, the live finite-dimensional
clean objects are

```text
L_full,n(q) = [A_int,n(q); B_full,n(q)],
C_center,n(q) = [C_amp,n(q); C_reg,n(q)].
```

The active critical boundary rows remain

```text
[u_n(1), varphi(1), T_s(1), S(1), H(1)].
```

The center split is

```text
C_amp(c) =
  [u_s/x^n,
   varphi/x^(n-1)] at x = x0,

C_reg(c) =
  [u_n/x^n + (lambda_c/n) varphi/x^(n-1),
   psi/x^(n-1) - lambda_c varphi/x^(n-1)] at x = x0.
```

The clean canonical reduced basis is defined from the live span `V_reg` by

```text
G_amp = C_amp V_reg,
V_adm = V_reg G_amp^(-1),
```

whenever `det(G_amp) != 0`.

The preferred reduced tangent operator and its boundary-only descendant are

```text
L_red,n(q) = [A_int,n(q); B_full,n(q)] V_adm,n(q),
B_red,n(q) = B_full,n(q) V_adm,n(q),
B_mix,n(q) = B_red,n(q) G_amp,n(q).
```

## Exact C3 statement already closed

Define the current chosen reduced family

```text
A_repo,n(q) = im(V_adm,n(q)).
```

Then the map

```text
Phi_n,q(a) = V_adm,n(q) a
```

is a bijection `R^2 -> A_repo,n(q)` because `C_amp V_adm = I_2` and
`C_reg V_adm = 0`.

With `L_red = L_full V_adm`, one has the exact restricted kernel equivalence

```text
ker(L_red,n(q))  <->  A_repo,n(q) ∩ ker(L_full,n(q))
```

via the bijection `a -> V_adm a`.

This is the closed C3 statement. It is exact only on the current chosen reduced
family `A_repo`.

## Exact C3b target

C3b asks whether the restriction to `A_repo = im(V_adm)` is lossless.

That question must be split carefully.

### 1. The theorem-facing full admissible clean tangent space

The intended theorem-level object is the space of clean center-regular
perturbations of the full linearized mixed problem before the final edge
criticality condition is imposed.

Call this intended object

```text
A_full^th,n(q).
```

On the present repository boundary, `A_full^th,n(q)` is **not** yet available as
an independently closed continuum object with a finished article-level local
solution-family derivation.

### 2. The current weighted trial-coefficient universe

The active code does explicitly provide a finite-dimensional weighted trial space
of coefficient vectors

```text
X_trial,n = R^N,
N = 8 * m_basis,
```

through `TrialSpace` and `field_exponent(...)`, with the current scaling
encoded directly in the basis:

```text
u_s, u_n, v ~ x^n,
varphi, psi, T_s ~ x^(n-1),
Q_s, M_s ~ x^(n-2).
```

So the code-level ansatz already bakes in the principal-part scaling orders.

### 3. The center-regular coefficient space inside the current ansatz

Inside `X_trial,n`, the explicit center-regular coefficient constraint space is

```text
W_reg,n(q) = { c in X_trial,n : C_reg,n(q) c = 0 }.
```

This is the largest center-regular coefficient space that is explicit in the
current code.

### 4. The current repo-selected family

The current solver does **not** take all of `W_reg`. Instead it picks a special
2D family by solving a constrained regularized least-squares problem for each
choice of the two free center amplitudes.

That selected family is exactly what the repository currently uses as

```text
A_repo,n(q) = im(V_adm,n(q)).
```

## Deriving the current ansatz-level admissible space

### 1. What the weighted trial basis already fixes

Because the basis functions have the form

```text
x^p * t^k,    t = (x - x0) / (1 - x0),
```

one has `t(x0) = 0`. Therefore only the `k = 0` columns contribute to the
leading center data used by `C_center`.

So, inside the current weighted trial ansatz, the leading center data is carried
exactly by four coefficients:

```text
(a_us, a_un, a_phi, a_psi)
```

corresponding to the `k = 0` coefficients of `u_s`, `u_n`, `varphi`, `psi`.

The leading-center block is therefore

```text
[a_us,
 a_phi,
 a_un + (lambda_c/n) a_phi,
 a_psi - lambda_c a_phi].
```

Equivalently, on these four leading amplitudes the center matrix is

```text
[1  0      0       0]
[0  0      1       0]
[0  1  lambda_c/n  0]
[0  0   -lambda_c  1].
```

### 2. What the current regularity constraints do

Imposing `C_reg = 0` on the leading data gives exactly

```text
a_un = -(lambda_c/n) a_phi,
a_psi = lambda_c a_phi.
```

So the current ansatz-level leading regular family is parameterized by exactly

```text
(a_us, a_phi).
```

This reproduces the current two-amplitude center logic used by the project.

### 3. What this does **not** imply

The two-amplitude statement above is only a statement about the leading center
data.

It does **not** mean that the whole coefficient space `W_reg = ker(C_reg)` is
2D. In the current weighted trial basis, `C_reg` imposes only two linear
constraints on the full coefficient vector, so `W_reg` is much larger.

That is the key C3b distinction:

- the leading admissible center data is 2D;
- the full weighted trial coefficient space satisfying `C_reg = 0` is not 2D;
- therefore `A_repo` cannot be identified with the full center-regular trial
  coefficient space from `C_reg = 0` alone.

## The exact current selected family inside the ansatz

To make the current repository family explicit, define the KKT-selected
amplitude-to-coefficient map `M_amp,n(q)` as the coefficient block of the unique
solution of

```text
minimize ||A_int c||^2 + reg ||c||^2
subject to C_center c = [a_1, a_2, 0, 0].
```

For each amplitude vector `a = (a_1, a_2)`, this gives one coefficient vector
`c = M_amp a`.

So the exact current selected family inside the weighted ansatz is

```text
A_ls,n(q) = im(M_amp,n(q)).
```

This is the strongest tractable explicit surrogate for the unknown continuum
space `A_full^th` on the current repository boundary.

## C3b result obtained here

### Proposition C3b.1. What is proved now

Inside the current weighted trial ansatz, the current repository family is
exactly the KKT-selected two-parameter constrained-least-squares family:

```text
A_repo,n(q) = im(V_adm,n(q)) = A_ls,n(q) = im(M_amp,n(q)).
```

So the reduction is lossless with respect to the **current selected ansatz-level
family**.

### Why this is true in the current repository sense

- `solve_constrained_mode(...)` solves a fixed KKT system with right-hand side
  determined by the chosen amplitude data, so the underlying unnormalized
  constrained family is linear in `(a_1, a_2)`;
- `c1` and `c2_raw` are just two nonzero amplitude-normalized representatives of
  that same family;
- the post-construction normalization / orthogonalization changes the basis but
  not the span;
- `V_adm = V_reg (C_amp V_reg)^(-1)` then recovers the unique basis of that span
  with canonical center amplitudes.

Therefore `im(V_adm)` is exactly the current selected constrained family.

### Proposition C3b.2. What is **not** proved now

This pilot does **not** prove

```text
A_repo,n(q) = A_full^th,n(q).
```

The missing step is a theorem-level derivation linking the full clean
center-regular tangent space of the continuous linearized mixed problem to the
current weighted trial / constrained-least-squares construction.

In other words, the repository now knows exactly what current family it is using,
but it does not yet know that this family exhausts the full theorem-facing clean
admissible tangent space.

## What `reduction_check.py` now verifies

### 1. Symbolic algebra / CAS

Using SymPy matrix expressions, the script checks:

- `([A; B] V) = [A V; B V]`;
- `([A; B] V)^T ([A; B] V) = V^T (A^T A + B^T B) V`;
- `[A; B]^T [A; B] = A^T A + B^T B`;
- `L_full (V T) = (L_full V) T` for reduced basis changes;
- `B_full (V T) = (B_full V) T`;
- `B_full V G^(-1) G = B_full V`;
- the exact leading-center block has determinant `-1`;
- the leading regularity subsystem has rank `2` and a two-parameter nullspace;
- the current regular leading family is parameterized by `(a_us, a_phi)`.

### 2. Live clean representative checks

On representative clean competition points

```text
(n, q) = (4, 11.1), (6, 17.6), (7, 17.3), (8, 17.8) MPa,
```

the script checks that:

- `rank(C_amp) = 2`, `rank(C_reg) = 2`, `rank(C_center) = 4`;
- in the present `48`-dimensional trial basis, `dim ker(C_reg) = 46` and
  `dim ker(C_center) = 44`;
- `C_reg V_reg ≈ 0` and `C_center V_adm ≈ [[I_2], [0]]`;
- the direct KKT-selected canonical map `M_amp` satisfies
  `C_center M_amp ≈ [[I_2], [0]]`;
- `V_adm` and `M_amp` are numerically close, and their interior / boundary
  images under `L_full` and `B_full` agree to numerical tolerance.

### 3. Conservative reading after C3b

The current repository now supports the following sharp statement:

- `A_repo = im(V_adm)` is fully characterized as the exact current selected
  constrained-least-squares family inside the weighted trial ansatz;
- the leading center-regular data is exactly two-parameter;
- `C_reg = 0` alone does **not** define the current theorem-facing reduced family;
- equality between `A_repo` and the full clean admissible tangent space remains
  open.

## Lean abstraction target after C3b

The next Lean step should formalize the cleanest already-closed finite-
dimensional part.

1. The leading center data space
   `W_lead = {(a_us, a_un, a_phi, a_psi) : a_un + (lambda_c/n)a_phi = 0,
   a_psi - lambda_c a_phi = 0}` is linearly equivalent to `R^2` via
   `(a_us, a_phi)`.
2. The current KKT-selected family `A_ls = im(M_amp)` is linearly equivalent to
   `R^2` via the amplitude map.
3. `A_repo = im(V_adm) = A_ls` for the current canonical rebasing of that same
   family.
4. The C3 statement then gives
   `ker(L_red) <-> A_repo ∩ ker(L_full)`.

Lean should **not** yet try to prove `A_repo = A_full^th`, because that is
exactly the still-open C3b gap.

## Verification boundary

This pilot is valid only for:

- the current clean standalone `simple support / подвижный шарнир` architecture;
- the current weighted trial ansatz and center split encoded in `TrialSpace`
  and `C_center`;
- the current KKT-based constrained mode construction in
  `full_simple_support_critical_search.py`.

It is a repository-level reduction note, not a final theorem for the full shell
problem.

## How to run

From the repository root:

```powershell
.\.venv\Scripts\python.exe proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator\reduction_check.py
```

## Continuum/local completeness step after C3b

This pilot now also records the next theorem-facing step after C3b.

### Exact target of the step

The new target is to compare

```text
A_full^th,n(q)
```

the full theorem-facing clean admissible center-regular local tangent family,
with

```text
A_ls,n(q) = im(M_amp,n(q)) = im(V_adm,n(q)),
```

the current weighted-trial KKT-selected two-parameter family.

The sharpest currently tractable success statement is not full equality yet.
It is:

- derive the continuum/local leading regular family directly from the current
  mixed equations at the principal center level;
- prove whether it is two-parameter;
- compare that leading local family to the current amplitudes used by `A_ls`;
- identify the exact missing step between that local family and a full theorem-
  level losslessness result.

### What the new local helper checks

`formal_local_family_check.py` introduces the current principal center model
used only for the theorem-facing local-leading derivation:

```text
c0 -> 1,
s0 -> 0,
a0 -> 1/x,
a0' -> -1/x^2,
lambda_s0 -> lambda_c,
lambda_theta0 -> 1,
```

while the fields are written in the current regular orders

```text
u_s = A_us x^n,
u_n = A_un x^n,
v = A_v x^n,
varphi = A_phi x^(n-1),
psi = A_psi x^(n-1),
T_s = A_Ts x^(n-1),
Q_s = A_Qs x^(n-2),
M_s = A_Ms x^(n-2).
```

From the leading singular block of the live mixed equations it derives

```text
A_un = -(lambda_c / n) A_phi,
A_psi = lambda_c A_phi,
A_Ms  = ((n + nu - 1) + nu n lambda_c) A_phi / (Lambda (1 - nu^2)),
```

and one leading relation tying `A_Ts` to `A_us` and `A_v`.

So the current mixed equations do support a two-parameter leading local center
family parameterized by `(A_us, A_phi)`.

### What remains open even after this local derivation

The same helper also shows that the fully frozen principal truncation does not
close the whole higher-order local family by itself: solving all frozen
principal equations simultaneously does not produce a nontrivial closed family.

So the current repository boundary after this step is:

- the local **leading-order** clean center-regular family is two-parameter and
  matches the same amplitudes used by `A_ls`;
- this is stronger than a pure trial-space statement;
- but a full local formal-completeness theorem still needs the next regular-
  singular recurrence layer, and only after that can one compare the resulting
  local family to the global weighted-trial KKT family in a lossless theorem-
  level sense.

### Resulting conservative reading

After this step the project should read the situation as follows:

- `A_ls = im(V_adm)` is exactly the current selected ansatz-level family;
- the continuum/local principal center model yields the same two leading free
  amplitudes;
- therefore the current ansatz matches the continuum/local family at leading
  order;
- but full equality `A_full^th = A_ls` is still not proved, because the local
  higher-order formal continuation / completeness step is still missing.

## Higher-order frozen-principal recurrence refinement

The next theorem-facing step after the previous leading-order note was to stop
reading the singular leading block as if it were already a full local family,
and instead assemble the full frozen principal layer-by-layer system on the same
current scaling orders.

### Exact target of this refinement

The target here is intentionally narrower than a full continuum theorem:

- keep the same current principal center replacements
  `c0 -> 1`, `s0 -> 0`, `a0 -> 1/x`, `a0' -> -1/x^2`,
  `lambda_s0 -> lambda_c`, `lambda_theta0 -> 1`;
- do **not** yet restore the first omitted finite center coefficients;
- derive the first checked recurrence layers of the fully frozen principal
  model;
- determine whether that fully frozen model really supports the expected clean
  two-amplitude local family.

### Finite-order result in the fully frozen principal model

The symbolic helper now gives a sharper answer than the earlier leading-order
reading.

1. The singular leading block remains two-parameter in `(A_us, A_phi)` and
   determines the accompanying leading relations for `u_n`, `psi`, and `M_s`.
2. But once the full frozen principal leading layer is assembled from
   `R_us`, `R_un`, `R_Ts`, `R_gtheta`, `R_phi`, `R_Ms`, and `R_v`, the exact
   physical determinant becomes

```text
n^2 (2n - 1) (2n + 1)
[lambda_c n nu^3 - lambda_c n nu^2 + lambda_c n
 - 2 lambda_c nu^3 + 2 lambda_c nu^2 + lambda_c nu - 3 lambda_c
 - n nu^3 + n nu^2 + n nu - 2]
/ [2 (nu + 1)],
```

   so under generic nonresonance the full leading layer is forced to

```text
U0 = V0 = T0 = N0 = P0 = Y0 = M0 = 0.
```

3. After that zero leading layer, the next checked layer has full rank `7` and
   nullity `1`. Its generic solution is

```text
N1 = P1 = Y1 = M1 = Q0 = 0,
U1 = T1 (-n nu - n - 2 nu + 2) / (-n^2 + n + 2),
V1 = T1 (n nu + n + 4) / (-n^2 + n + 2),
```

   so only one membrane parameter `T1` remains free. The denominator exposes
   the same special factor `(n - 2)(n + 1)`.
4. After substituting that generic next-layer membrane mode, the checked second
   layer becomes invertible again and forces

```text
U2 = N2 = V2 = P2 = Y2 = T2 = M2 = Q1 = 0.
```

### Representative live clean check

The helper evaluates the derived determinant factors on the representative clean
competition set `(n, q) = (4, 11.1), (6, 17.6), (7, 17.3), (8, 17.8)` using the
live clean value `lambda_c = lambda_s0(x0)`. On that set the leading full-layer
factor, the next flexural determinant, and the checked second-layer determinant
are all far from zero, so this finite-order pattern is not a sample-point
resonance artifact on the current live clean path.

### Conservative reading after this refinement

This does **not** prove or disprove the theorem-facing equality
`A_full^th = A_ls`.

What it does prove is narrower and more useful:

- the earlier two-amplitude principal-center statement must now be read only as
  a singular leading-block compatibility result;
- the fully frozen principal model itself does **not** realize the expected
  clean two-amplitude local family through the checked finite orders;
- therefore the next theorem-facing step is no longer “push the same frozen
  model further”, but “restore the first omitted finite center coefficients /
  forcing terms and derive the richer regular-singular recurrence there”.

## C3c: Richer Local Center Model With First Omitted Finite Coefficients

The next theorem-facing step was to restore the first honest finite center terms
of the clean background instead of staying inside the fully frozen principal
model.

### What was restored

At the richer local level the background is now read as

```text
c0 = 1 + O(x^2),
s0 = K x + O(x^3),
a0 = 1/x + O(x),
a0' = -1/x^2 + O(1),
lambda_s0 = lambda_c + O(x^2),
lambda_theta0 = lambda_c + O(x^2),
kappa_s0 = K + O(x^2),
kappa_theta0 = K / lambda_c + O(x^2),
T_s^0 = T_s^0(0) + O(x^2),
T_theta^0 = T_theta^0(0) + O(x^2),
M_theta^0 = M_theta^0(0) + O(x^2),
T_sn^0 = Q1 x + O(x^3).
```

The honest background recurrence fixes the first omitted coefficients
`Ts2, U3, K3, Ms2, Q3` uniquely. Their full CAS formulas are long, but the key
point for C3c is their order: all of them enter only at `O(x^2)` or `O(x^3)`.

### Exact C3c result

This richer first-finite layer still does **not** repair the decisive low-order
obstruction.

By direct order counting:

- in `R_Ts`, the obstruction layer sits in
  `-(s0 c0 / r0^2) Mtheta ~ x^(-1) x^(n-2) = x^(n-3)`;
- in `R_Ms`, the obstruction layer sits in
  `Ms_x`, `a0 M_s`, `-a0 M_theta`, `-Q_s`, and `(n/x) H`, again at `x^(n-3)`;
- in `R_v`, the obstruction layer sits in `kappa_theta0 chi` with
  `chi ~ x^(n-3)`.

Since the restored background corrections start only at `O(x^2)` or `O(x^3)`,
they first affect these rows at `x^(n-1)` or higher. Therefore the low-order
obstruction formulas remain exactly the same as in the constant-finite model.

After the singular leading relations

```text
N0 = -(lambda_c / n) P0,
Y0 = P0,
M0 = (n - 1) P0 / [12 mu^2 (1 - nu^2)^2],
```

the unchanged low-order rows are

```text
R_Ts[-1] = -K P0 [lambda_c n nu - lambda_c nu + n + 1]
           / [12 lambda_c^3 mu^2 (1 - nu^2)^2],

R_Ms[-1] = -P0 [ ... ] / [12 lambda_c mu^2 (1 - nu^2)^2],

R_v[-1]  =  K P0 n [ ... ] / [12 lambda_c^4 mu^2 (1 - nu^2)^2].
```

The simplest factor is already enough:

```text
lambda_c n nu - lambda_c nu + n + 1
= lambda_c nu (n - 1) + n + 1 > 0
```

for the active nonshallow clean regime with `lambda_c > 0`, `nu > 0`, and
`n >= 4`.

So, whenever `K != 0`, the richer first-finite layer still forces

```text
P0 = 0.
```

### Representative live clean check

On the current clean competition set `(n, q) = (4, 11.1), (6, 17.6), (7, 17.3),
(8, 17.8)` the helper now confirms that

- `K = kappa_s0(x0)` is nonzero on all sample points;
- the `R_Ts[-1]`, `R_Ms[-1]`, and `R_v[-1]` obstruction factors are all far
  from zero.

So the richer first-finite-corrections layer does not rescue a nontrivial
`P0` branch on the live clean path either.

### Conservative reading after C3c

This is **not** a theorem-level proof about the final clean local family.
But it is already a stronger negative boundary than before:

- the fully frozen principal model was too crude;
- restoring the first omitted finite center coefficients is still not enough;
- therefore the main completeness gap remains open, and `A_full^th = A_ls` is
  still not proved.

The next theorem-facing step is no longer "add only the first `O(x^2)` /
`O(x^3)` center corrections". It is to identify a local ingredient that can
act at the same low orders as the unchanged obstruction, or else to reconsider
what the exact theorem-facing local comparison object should be.
