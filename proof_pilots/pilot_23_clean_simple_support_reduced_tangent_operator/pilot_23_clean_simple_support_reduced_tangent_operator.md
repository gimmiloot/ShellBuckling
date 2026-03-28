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

## Object-Selection Step After C3c

After C3c the next task is no longer "derive more coefficients of the same
unrestricted local family". The exact theorem-facing decision point is:

```text
what local object should actually be compared to A_ls?
```

At least four candidates must be separated:

- `O1`: the full local center-regular formal family of the clean mixed
  equations;
- `O2`: that local family plus only admissibility / normalization;
- `O3`: a local center-regular family plus a weak/interior KKT-type selection;
- `O4`: the local germ family obtained by taking center traces of the global
  weak-selected family actually used by the repository.

### What `A_ls` means in the live clean code

The new helper `selection_object_check.py` inspects the current clean
construction in `full_simple_support_critical_search.py` and makes the selected
family explicit.

For each amplitude vector `a = (a1, a2)` the weighted ansatz contains the full
affine fiber

```text
F_n,q(a) = { c in X_trial,n : C_center,n(q) c = [a1, a2, 0, 0] }.
```

The current repository family is not all of that fiber. It is the image of the
unique constrained minimizer

```text
c*(a) = argmin ( ||A_int,n(q) c||^2 + reg ||c||^2 )
        subject to C_center,n(q) c = [a1, a2, 0, 0].
```

Equivalently, with

```text
H_n,q = A_int,n(q)^T A_int,n(q) + reg I,
```

the KKT equations give

```text
H_n,q c*(a) + C_center,n(q)^T lambda(a) = 0,
```

so every fiber direction `z in ker(C_center)` satisfies

```text
z^T H_n,q c*(a) = 0.
```

Therefore `A_ls = im(M_amp)` is not merely a chart for local center-regular
data. It is the `H_n,q`-minimal section of a much larger amplitude fiber.

On the representative clean competition set `(n, q) = (4, 11.1), (6, 17.6),
(7, 17.3), (8, 17.8)` the helper checks that:

- `dim X_trial = 48` and `rank(C_center) = 4`, so each fixed-amplitude fiber is
  still `44`-dimensional;
- the selected map satisfies the KKT stationarity / fiber-orthogonality
  identities to numerical tolerance;
- a simple constraint-only feasible reference has the full objective larger by
  factors ranging from about `10^6` up to about `10^11`;
- replacing the full interior block `A_int` by only the first `5%`, `10%`,
  `20%`, or `50%` of collocation rows changes the selected amplitude map
  strongly and inflates the full objective by many orders of magnitude.

### Conservative reading after the new selection check

This changes the local-comparison question sharply.

- `O1` now looks too broad as the default comparison object for `A_ls`, because
  it forgets the global weak/interior selection layer already built into the
  code.
- `O2` is still too weak unless admissibility secretly encodes the same
  selection rule; current repository evidence does not show that.
- `O3` is the most plausible option if one insists on a genuinely local
  theorem-facing object.
- `O4` is even closer to the live architecture, because the current selection
  depends on the full interior operator `A_int`, not only on center data.

So the exact comparison object is **not yet uniquely closed**, but the
repository boundary now strongly suggests that the previous unrestricted-local-
family comparison was mismatched.

### Resulting next theorem-facing target

The next theorem should probably **not** be framed as raw completeness of `O1`.
It should be one of the following:

1. derive a selected local family `A_sel^loc` carrying a weak/interior
   optimality rule that matches the current KKT family;
2. or prove a global-to-local statement saying that the correct comparison
   object is the local germ family of the globally weak-selected admissible
   family already encoded by `A_ls`.

At the current repository boundary there is still **no adequate purely local
KKT analogue** reproducing `A_ls`. That is the exact remaining gap after this
step.

## C3e: Delimiting the Selected Local Object

For the current clean weighted-trial construction, let

```text
X_trial,n(q) = R^48,
C_center,n(q) = [C_amp,n(q); C_reg,n(q)],
D_amp = [[I_2], [0]],
H_n,q = A_int,n(q)^T A_int,n(q) + reg I.
```

Then the full selected center-data lift is

```text
P_sel,n(q) = H_n,q^(-1) C_center,n(q)^T
             (C_center,n(q) H_n,q^(-1) C_center,n(q)^T)^(-1),
```

with

```text
C_center,n(q) P_sel,n(q) = I_4.
```

Its image

```text
X_sel,n(q) = im(P_sel,n(q))
```

is a 4D `H_n,q`-orthogonal lift of the full center-data space. The current
repository family is not all center-regular data, but the regularity-zero slice

```text
A_ls,n(q) = im(P_sel,n(q) D_amp)
          = { c in X_sel,n(q) : C_reg,n(q) c = 0 }.
```

Equivalently, for fixed amplitudes `a = (a1, a2)` the current weighted ansatz
still contains the large affine fiber

```text
F_n,q(a) = { c in X_trial,n(q) : C_center,n(q) c = [a1, a2, 0, 0] },
```

and the selected representative is the unique `H_n,q`-minimal point of that
fiber. So center constraints alone do not determine the current family; the
extra content comes from the global weak/interior minimization.

This makes the local theorem-facing question sharper.

- `A_reg^loc`: the raw local center-regular formal family of the clean mixed
  equations.
- `A_sel,trace^loc`: the center-germ trace `J_0(A_ls)` of the globally selected
  family.
- `A_sel,weak^loc`: only a hypothetical intrinsic local selected family,
  obtained from `A_reg^loc` by some local weak/KKT-type rule.

Current C3e result:

1. The comparison object for `A_ls` should no longer be taken to be
   `A_reg^loc` by default.
2. The best exact faithful candidate currently visible in the repository is the
   extrinsic trace object `A_sel,trace^loc = J_0(A_ls)`.
3. No canonical intrinsic local selection law reproducing the same family is
   yet identified.
4. Therefore the next theorem should not be raw completeness of `A_reg^loc`.
   It should be either a global-to-local trace theorem for `A_ls`, or an
   intrinsic characterization theorem showing that `A_sel,trace^loc` is the
   selected subfamily of `A_reg^loc` for a canonically defined local weak form.

The updated helper `selection_object_check.py` now confirms on representative
active clean points `(n, q) = (4, 11.1), (6, 17.6), (7, 17.3), (8, 17.8)` that

- `rank(C_amp) = 2`, `rank(C_reg) = 2`, `rank(C_center) = 4`, so the fixed-
  amplitude fiber remains 44D inside the 48D weighted trial space;
- the KKT-selected 4D lift satisfies `C_center P_sel ≈ I_4` and the expected
  `H`-orthogonality to `ker(C_center)`;
- the amplitude slice `im(P_sel D_amp)` matches the current selected family;
- near-center row surrogates still do not reproduce the full selected map.

So C3e closes only a delimited statement: the theorem-facing local comparison
object must be selected rather than raw, and the best current exact candidate
is the local trace of the globally selected family, not the unrestricted local
center-regular family.

## C3f: Global-to-Local Trace at the Leading Center-Jet Level

The next theorem-facing question is not yet an intrinsic local selector theorem.
It is the following global-to-local trace question for the already selected
family `A_ls`.

### Candidate meanings of `J_0`

At the current repository boundary at least three trace notions must be
separated.

1. `J_amp(c) = C_amp c`:
   only the two leading amplitudes.
2. `J_0(c) = C_center c = [C_amp c; C_reg c]`:
   the full leading center jet currently encoded by the clean weighted ansatz.
3. a higher-order local germ/jet extractor:
   not yet canonical on the current repository boundary.

The best current theorem-facing choice is `J_0 = C_center`, not `J_amp` and not
an unresolved higher-order germ. The reason is that `J_0` keeps both the two
leading amplitudes and the two leading regularity-defect rows, so it is the
smallest current exact object that still distinguishes raw center data from the
selected regularity-zero slice.

### Exact current weighted-ansatz reading of `J_0`

By inspection of `TrialSpace.basis_eval(...)` and
`make_center_constraint_matrix(...)`, evaluation at `x = x0` kills every trial
basis column with `k > 0`. Therefore `C_center` sees only the four `k = 0`
columns of

```text
u_s, u_n, varphi, psi.
```

On those columns the center trace block is exactly

```text
[ 1      0      0      0 ]
[ 0      0      1      0 ]
[ 0      1    lam_c/n  0 ]
[ 0      0    -lam_c   1 ]
```

with determinant `-1`. So the current weighted-ansatz trace map `J_0 = C_center`
is an exact rank-4 leading-center-jet extractor, not merely a heuristic small-
`x` diagnostic.

It forgets:

- all higher `k >= 1` center coefficients;
- all channels not entering the leading center jet;
- any higher-order intrinsic local germ structure.

So `J_0` is a finite leading-center trace, not a full local formal germ map.

### Trace theorem on the selected family

For the current selected family

```text
A_ls = im(P_sel D_amp),
P_sel = H^(-1) C_center^T (C_center H^(-1) C_center^T)^(-1),
D_amp = [[I_2], [0]],
```

one has the exact weighted-ansatz identity

```text
J_0(A_ls) = C_center(im(P_sel D_amp)) = im(D_amp).
```

So the selected trace object is the 2D plane

```text
A_sel,trace^loc = J_0(A_ls) = im(D_amp)
```

inside the 4D center-data space.

Moreover, the restriction

```text
J_0|_{A_ls} : A_ls -> im(D_amp)
```

is bijective, with inverse given by the selected lift `P_sel` on that plane.
Equivalently,

```text
c in A_ls  <->  c = P_sel J_0(c),
J_0(c) in im(D_amp).
```

Hence the selected trace is basis-independent: replacing a basis of `A_ls` by
`M T` with invertible `T` changes only coordinates inside the same trace plane,
not the plane `J_0(A_ls)` itself.

The compressed map `J_amp = C_amp` becomes equivalent only after restricting to
`A_ls`, where `C_reg c = 0` and `J_amp|_{A_ls}` identifies `A_ls` with `R^2`.
But off `A_ls` it forgets the regularity-defect rows, so it is not the best
current theorem-facing definition of `J_0`.

### Relation to earlier local objects

This trace reading fits the earlier center analysis sharply:

- the first two coordinates of `J_0` are exactly the previously tracked leading
  amplitudes `(A_us, A_phi)`;
- the last two coordinates are the leading regularity-defect rows whose
  vanishing gives the known leading regular family condition;
- therefore `J_0(A_ls)` is much narrower than the raw local center-regular
  family `A_reg^loc`.

What remains open is not this finite leading-center trace plane itself, but its
relation to a genuine intrinsic local selected family beyond the currently exact
selected trace layer.

### Conservative C3f conclusion

C3f closes the following statement at the current weighted-ansatz boundary:

1. the best current theorem-facing meaning of `J_0` is the exact finite leading-
   center jet map `J_0 = C_center`;
2. the selected trace object is exactly
   `J_0(A_ls) = im(D_amp)`, a basis-independent 2D plane;
3. `J_0|_{A_ls}` is a bijection onto that plane, with inverse selected lift
   `P_sel`;
4. higher-order intrinsic local-germ selection is still open.

So the next theorem-facing comparison should be organized first against the
selected leading-center trace plane `J_0(A_ls)`, not against the full raw local
center-regular family.


## C3g: Recovering the Selected Trace Plane on the Local Side

The exact C3g target is narrower than a full intrinsic local selector theorem.
At this step the question is only whether the continuum/local selected trace can
already be shown to recover the same leading-center plane as the selected global
trace,

```text
J_0(A_ls) = im(D_amp).
```

### Best current continuum/local object

The best current local theorem-facing candidate is not a full higher-order
selected germ family. It is the leading-center trace object obtained from the
singular compatibility block, written in the same coordinates as the current
exact trace map

```text
J_0 = C_center.
```

So the relevant local object is the set of leading center jets

```text
tau(U0, N0, P0, Y0)
  = [U0, P0, N0 + (lambda_c / n) P0, Y0 - lambda_c P0].
```

This is the smallest current continuum/local object that is directly comparable
with the already closed selected global trace plane.

### Why this trace convention is the right one on the current repository boundary

The updated `formal_local_family_check.py` now makes explicit a structural fact
already built into the live clean background path.

Because the honest background BCs include

```text
T_sn(x0) = 0,  u_r(x0) = 0,  varphi(x0) = 0,
```

and because the live clean background defines

```text
lambda_theta0 = r0 / x,
```

one has on the current truncated clean boundary

```text
lambda_theta0(x0) = r0(x0) / x0 = 1
```

exactly. Representative clean checks at `q = 11.1, 17.3, 17.6, 17.8` MPa now
confirm that the active background path indeed gives

```text
u_r(x0) = 0,
T_sn(x0) = 0,
varphi(x0) = 0,
lambda_theta0(x0) = 1,
lambda_s0(x0) > 1.
```

So the theorem-facing local comparison with `J_0(A_ls)` must keep this same
`x0`-trace convention. A different fourth-coordinate normalization is a
different trace object and should not be silently substituted in C3g.

### Leading local recovery of `im(D_amp)`

At the singular leading-center level, the clean mixed equations give

```text
E_un     = n N0 + lambda_c P0 = 0,
E_gtheta = n N0 + Y0 = 0.
```

Solving these two equations gives

```text
N0 = -(lambda_c / n) P0,
Y0 = lambda_c P0.
```

Substituting into the current theorem-facing trace coordinates yields

```text
tau(U0, N0, P0, Y0) = [U0, P0, 0, 0] = D_amp [U0, P0].
```

Therefore the continuum/local selected leading-center trace plane agrees exactly
with the already closed global selected trace plane:

```text
A_sel,lead-trace^loc = im(D_amp).
```

This is an exact symbolic identity at the leading-center-jet level, not a
numerical pattern.

### Why the older richer local obstruction does not by itself contradict this

The same helper also shows the exact coordinate sensitivity.
If one changes only the fourth coordinate to

```text
Y0 - P0,
```

then after the same singular substitution one gets

```text
[U0, P0, 0, (lambda_c - 1) P0],
```

which lands in `im(D_amp)` only when `lambda_c = 1`.

So the earlier richer-local object that was written with `Y0 = P0` is not yet a
proved contradiction to the selected trace theorem. It is a different local
trace normalization that still needs an explicit reconciliation theorem before
it can be used as the direct theorem-facing comparison partner for `J_0(A_ls)`.

### Conservative C3g conclusion

C3g closes the following theorem-facing statement.

1. On the current repository boundary, the correct local comparison object for
   the selected trace problem is the leading-center trace written in the same
   coordinates as `J_0 = C_center`.
2. In those coordinates, the singular local compatibility block recovers the
   exact selected trace plane
   `im(D_amp)`.
3. This does **not** identify a full intrinsic higher-order local selector.
4. The exact remaining gap is now sharper: prove a higher-order intrinsic local
   selected-family theorem, or explicitly reconcile the current `J_0`
   coordinates with any alternative richer-local trace normalization.


## C3h: Reconciling Richer Local Trace Charts with `J_0 = C_center`

The exact C3h target is not a higher-order preservation theorem yet. It is the
coordinate-reconciliation problem between the already closed selected trace
plane

```text
J_0(A_ls) = im(D_amp)
```

and the richer local trace objects suggested by the checked regular-singular
expansions.

### Best current richer trace candidate

The best current richer theorem-facing trace candidate is the first truncated
regular-singular jet

```text
Xi_rich^(1,eta)
  = [U0, P0, Delta_un^(0), Delta_psi,eta^(0), U1, N1, P1, Y1],
```

with

```text
Delta_un^(0)     = N0 + (lambda_c / n) P0,
Delta_psi,eta^(0)= Y0 - eta P0.
```

This is the smallest current local jet that already goes beyond `J_0` by one
post-leading layer and at the same time makes the fourth-coordinate
normalization explicit.

It is not canonical yet: it depends on the chosen normalization parameter
`eta` and on how many higher coefficients are retained.

### Canonical projection to `J_0`

For any such richer trace chart there is an explicit triangular projection

```text
Pi_eta_to_J0 : Xi_rich^(1,eta) -> J_0,
```

given on coordinates by

```text
[U0, P0, Delta_un^(0), Delta_psi,eta^(0), U1, N1, P1, Y1]
  |->
[U0, P0, Delta_un^(0), Delta_psi,eta^(0) + (eta - lambda_c) P0].
```

This identity is exact and simply rewrites

```text
Y0 - lambda_c P0 = (Y0 - eta P0) + (eta - lambda_c) P0.
```

So the part of the richer trace that is canonical is not the raw fourth
coordinate itself, but its projection to the current exact `J_0` trace.

### The invariant selected object

Under the current live local selected relations

```text
N0 = -(lambda_c / n) P0,
Y0 = lambda_c P0,
```

the richer trace is not generally the zero-defect slice. Instead it is the 2D
lifted plane

```text
im(D_rich,eta),

D_rich,eta =
[[1, 0],
 [0, 1],
 [0, 0],
 [0, lambda_c - eta],
 [0, 0],
 [0, 0],
 [0, 0],
 [0, 0]].
```

The key exact identity checked in the helper is

```text
Pi_eta_to_J0(im(D_rich,eta)) = im(D_amp).
```

So the invariant selected object that should be preserved at higher order is not
"the zero fourth row" in an arbitrary richer normalization. It is the 2D lifted
selected family whose canonical `J_0` projection is `im(D_amp)`.

### Special case `eta = 1`

The older richer local note corresponds to the specific choice `eta = 1`.
Then the selected richer trace is the lifted plane with fourth component

```text
(lambda_c - 1) P0,
```

not the zero fourth row in current `J_0` coordinates. On the representative
clean points this coefficient is small but definitely nonzero, about
`0.0125 .. 0.0175`.

So the older richer local object was not actually contradicting C3g; it was
using another trace chart that had not yet been reconciled with `J_0`.

### Conservative C3h conclusion

C3h closes the following statement.

1. The richer local trace object is best treated, for now, as a truncated jet
   with an explicit fourth-coordinate normalization parameter `eta`.
2. There is an explicit projection `Pi_eta_to_J0` from that richer trace to the
   canonical current selected trace coordinates.
3. The invariant selected object to preserve at higher order is a 2D lifted
   plane inside the richer trace space whose `J_0` projection is exactly
   `im(D_amp)`.
4. A full higher-order selected-family theorem is still open.


## C3i: First Higher-Order Preservation for the Lifted Selected Family

The exact C3i target is no longer to ask whether the raw 2D lifted plane
`im(D_rich,eta)` survives unchanged at higher order. The question is sharper:
what does the first checked post-leading recurrence actually preserve?

### First post-leading recurrence over the selected leading trace

In the current richer trace chart

```text
Xi_rich^(1,eta)
  = [U0, P0, Delta_un^(0), Delta_psi,eta^(0), U1, N1, P1, Y1],
```

the first checked post-leading recurrence is an exact direct product over the
already selected leading amplitudes `(U0, P0)`: its Jacobian with respect to
`(U0, P0)` is identically zero.

At this layer the flexural block is still rigid under the same nonresonance
assumption as before:

```text
N1 = P1 = Y1 = M1 = Q0c = 0.
```

But the membrane block leaves one free parameter `T1`, with

```text
U1 = alpha * T1,
V1 = beta  * T1,

alpha = (-n*nu - n - 2*nu + 2)/(-n^2 + n + 2),
beta  = (n*nu + n + 4)/(-n^2 + n + 2).
```

For `n > 2` and positive `nu` the zero loci of `alpha` and `beta` lie outside
that physical regime, so the first membrane nullmode is already visible in the
current richer jet through `U1`.

### Raw 2D plane is not exactly preserved

The raw lifted object from C3h,

```text
im(D_rich,eta),
```

fixes

```text
U1 = N1 = P1 = Y1 = 0.
```

That is too small for the first checked post-leading recurrence, because the
exact recurrence admits the one-parameter membrane mode above. Therefore the raw
2D lifted plane is **not** exactly preserved.

### Corrected higher-order selected object

The smallest corrected object visible inside the current eight-coordinate richer
jet is the 3D plane

```text
Xi_sel,corr^(1,eta)
  = {[U0, P0, 0, (lambda_c - eta) P0, U1, 0, 0, 0]}
  = im(D_rich,eta^corr),
```

with

```text
D_rich,eta^corr =
[[1, 0, 0],
 [0, 1, 0],
 [0, 0, 0],
 [0, lambda_c - eta, 0],
 [0, 0, 1],
 [0, 0, 0],
 [0, 0, 0],
 [0, 0, 0]].
```

If one wants the coefficient-faithful object that keeps the hidden membrane
parameter explicit, the jet must be enlarged to

```text
Xi_rich^(1+,eta)
  = [U0, P0, Delta_un^(0), Delta_psi,eta^(0), U1, N1, P1, Y1, V1, T1],
```

and the corrected selected family is the exact 3D plane spanned by the two
leading selected amplitudes and the membrane nullmode

```text
(U1, V1, T1) = T1 * (alpha, beta, 1).
```

The helper checks this exact residual identity symbolically: after substituting
that 3D family into the first post-leading recurrence, every checked row is zero.

### Canonical projection remains unchanged

The key preserved invariant is still the canonical leading selected trace.
For both the visible corrected plane and the coefficient-faithful augmented
plane, the projection back to current `J_0` coordinates satisfies

```text
Pi_eta_to_J0(im(D_rich,eta^corr)) = im(D_amp),
Pi_eta_to_J0(im(D_rich,eta^aug))  = im(D_amp).
```

So the already closed selected leading-center trace plane is not lost. What
changes is only the richer post-leading lift above it.

### Checked next support

Within the same frozen-principal recurrence model, once this first membrane
thickening is admitted, the next checked layer closes uniquely to zero under the
same nonresonance assumptions. So at the checked orders there is no second new
independent post-leading direction.

### Conservative C3i conclusion

C3i closes the following statement.

1. The raw lifted 2D plane `im(D_rich,eta)` is not exactly preserved at the
   first checked post-leading order.
2. The smallest corrected higher-order selected object is a one-parameter
   membrane thickening over that lifted selected plane.
3. The canonical projection of this corrected object back to `J_0` remains
   exactly `im(D_amp)`.
4. This is still not an all-orders selected-family theorem; the intrinsic rule
   that should select, normalize, or quotient out the membrane thickening
   direction remains open.


## C3j: Canonical Treatment of the Membrane Thickening Direction

The exact C3j target is not to force the corrected higher-order selected family
back to a 2D chart. It is to decide what the membrane thickening direction means
canonically.

### The corrected family and its membrane kernel

After C3i the first checked higher-order selected object is the corrected 3D
family

```text
Xi_sel,corr^(1,eta) = im(D_rich,eta^corr)
```

inside the visible richer jet, or equivalently its coefficient-faithful
augmented version

```text
Xi_sel,corr^(1+,eta) = im(D_rich,eta^aug).
```

The canonical projection to current `J_0` coordinates acts on the coefficient
space of both objects as

```text
(a, b, s) |-> [a, b, 0, 0],
```

so its kernel is exactly the one-dimensional membrane line

```text
span(e_3).
```

In the visible jet this generator is simply the `U1` direction;
in the augmented jet it is the exact membrane nullmode

```text
g_mem^aug = [0, 0, 0, 0, alpha, 0, 0, 0, beta, 1].
```

The helper checks both facts symbolically and also confirms that the next
checked recurrence layer still does not kill this direction.

### Why a canonical 2D normalization is not yet available

A natural question is whether one can now impose an extra condition such as
`U1 = 0` and recover a canonical 2D family. The current checked local data do
not justify that.

The reason is exact linear algebra: there is a whole two-parameter family of 2D
sections of the corrected 3D family, namely graphs of arbitrary linear maps
from the quotient coordinates `(a, b)` into the membrane parameter `s`.
On the coefficient space this family is

```text
S_(ell1,ell2) =
[[1, 0],
 [0, 1],
 [ell1, ell2]].
```

Each such section satisfies

```text
Pi_eta_to_J0(D_rich,eta^corr S_(ell1,ell2)) = D_amp,
```

and likewise in the augmented chart. So the checked local recurrence and the
canonical `J_0` trace do not single out one privileged 2D section. Any choice
such as `U1 = 0` is therefore a section choice, not a canonical theorem-facing
normalization on the current repository boundary.

### Conservative C3j reading

At the checked order the membrane direction is best treated as quotient-like.
This is stronger than saying only that it is ?unresolved?, and weaker than
claiming a proved gauge symmetry.

- It is not seen by the canonical `J_0` trace.
- It is not killed by the next checked recurrence layer.
- The current local data do not canonically normalize it away.
- The global selected family is still 2D, so the theorem-facing local object
  that best matches the current clean selection architecture is the quotient of
  the corrected 3D local family by this membrane line.

### Conservative C3j conclusion

C3j closes the following statement.

1. The extra membrane thickening direction is not yet proved to be a gauge
   symmetry and not yet proved to be a genuine additional selected degree of
   freedom.
2. The best current canonical reading is quotient-like: the corrected local
   higher-order selected object should be treated modulo that direction.
3. The quotient is canonically identified by the `J_0` projection with the
   already closed selected trace plane `im(D_amp)`.
4. What remains open is an intrinsic higher-order rule that would either pick a
   distinguished representative of this quotient class or show that the quotient
   itself is the final theorem-facing local object.


## C3k: canonical representative vs final quotient theorem

C3k tests whether the membrane-quotient class identified in C3j already has a
canonically selected higher-order representative on the current checked local
boundary.

### Candidate selectors checked

The symbolic helper now checks four natural selector candidates.

1. The next checked local compatibility layer does not distinguish
   representatives inside the membrane-thickened corrected family.
2. Checked local residual minimization does not distinguish them either,
   because the corrected augmented family already has exact zero checked
   residual along the membrane line.
3. Chart conditions such as `U1 = 0` are not intrinsic: after a
   quotient-preserving chart change they become arbitrary 2D sections.
4. Orthogonality / minimal-norm rules depend on an additional metric choice.
   They do pick a section once a metric is chosen, but that section varies with
   the metric, so it is not currently an intrinsic local theorem-facing rule.

A global weighted-trial KKT metric still exists on the clean finite-dimensional
selection side, but no intrinsic local metric has been derived that canonically
reproduces one representative of each membrane-quotient class.

### Conservative C3k reading

At the current checked local boundary, no intrinsic canonical higher-order
representative is justified. The quotient statement from C3j can now be
strengthened:

- the membrane line is invisible to the canonical `J_0` trace;
- all representatives of one quotient class carry the same selected leading
  trace plane `im(D_amp)`;
- the currently checked local equations do not canonically prefer one 2D
  section over another.

So the best current theorem-facing local selected object remains the quotient
class

```text
im(D_rich,eta^corr) / span(g_mem),
```

or equivalently its coefficient-faithful augmented version.

### Conservative C3k conclusion

C3k closes the following statement.

1. No intrinsic canonical higher-order representative has been identified on
   the current checked local boundary.
2. The quotient theorem is stronger than before: all currently justified local
   selected invariants factor through the membrane quotient.
3. Future higher-order local theorems should therefore act on the quotient
   object unless a later intrinsic selector is derived.
4. What remains open is whether such an intrinsic selector exists, or whether
   the quotient itself is already the final local selected object.


## C3l: boundary-scoped fork decision in favor of the quotient object

C3l is a controlled stop-rule step. Its purpose is not to keep extending the
same local line, but to decide the A/B/C fork on the current checked local
boundary.

### What was tested

The current corrected higher-order local selected family is still the 3D family
from C3i/C3j, with exact membrane kernel direction and quotient coordinates
`(a, b)`.

The checked decision uses only the strongest plausible intrinsic selectors.

1. The next checked local compatibility layer still does not distinguish
   representatives inside one membrane-quotient class.
2. The checked local residual vanishes identically on the corrected augmented
   family, so residual minimization cannot select a unique representative.
3. Chart rules such as `U1 = 0` are section choices after quotient-preserving
   chart changes.
4. Orthogonality / minimal-norm rules become unique only after an extra metric
   choice, hence are not intrinsic on the current local boundary.

### Strongest quotient theorem now available

At this point the quotient theorem is stronger than in C3k.

- The canonical `J_0` trace on the corrected 3D family factors exactly through
  the quotient map `(a, b, s) -> (a, b)`.
- The checked local residual also factors trivially through the quotient,
  because it vanishes identically on the corrected family.
- The next checked local compatibility layer adds no extra representative-level
  invariant on the current checked boundary.

So every currently justified local selected invariant factors through the
membrane quotient.

### Outcome B on the current checked boundary

The A/B/C fork is therefore closed as Outcome B on the current checked local
boundary.

```text
im(D_rich,eta^corr) / span(g_mem)
```

is the final local theorem-facing selected object on that boundary.
This is a boundary-scoped finality statement: it does not say that no future
unchecked higher-order intrinsic selector could ever appear, only that none is
currently justified on the checked local boundary.

