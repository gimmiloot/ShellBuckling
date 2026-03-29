# Current Theorem Roadmap For Clean Full `simple support / подвижный шарнир`

This note records the current theorem program above the frozen local
Outcome-B boundary. It starts from the current criterion bridge note and does
not reopen the same checked local branch.

## A. Goal

The long-term theorem target is not “find a minimum” and not “promote a raw
boundary dip.” The target is to prove that criticality on the clean full
`simple support / подвижный шарнир` path must be read through the correct
selected reduced object, with `L_red` as the present theorem-facing anchor.

Operational candidate rankings may still use descendants and diagnostics, but
the final theorem program should pass through the selected reduced family and
the nontrivial-kernel question for `L_red`.

## B. What Is Already Closed Enough To Use

- `A_ls` is best read as the global weak/KKT-selected family on the live clean
  reduced path.
- `L_red` is the main theorem-facing reduced object:
  `L_red,n(q) = [A_int,n(q); B_full,n(q)] V_adm,n(q)`.
- `B_red` and `B_mix` are descendants / coordinate presentations on that
  selected reduced family, not independent theorem-level replacements.
- The selected leading trace plane is closed:
  `J_0 = C_center`, `J_0(A_ls) = im(D_amp)`.
- On the current checked higher-order local boundary, the strongest local
  theorem-facing object closes only as the quotient
  `im(D_rich,eta^corr) / span(g_mem)`.

These blocks are enough to organize the next theorem program, even though they
do not yet close final physical criticality.

## C. Main Theorem Program

### `T1`. Global selected-family theorem

Statement:
- identify the clean reduced family as the current global weak/KKT-selected
  family `A_ls`.

Status:
- closed enough on the present repo/ansatz boundary.

### `T2`. Reduced-operator theorem

Statement:
- use `L_red` as the main reduced theorem-facing object and retain
  `B_red`, `B_mix` only as descendants on the same selected family.

Status:
- closed enough on the present reduced-family boundary.

### `T3`. Global selected-kernel bridge program for `L_red`

Statement:
- bridge the correct selected class for the clean path to the nontrivial-kernel
  question for `L_red` without collapsing the theorem to `B_red` / `B_mix`
  alone and without overclaiming final physical criticality.

Status:
- central theorem-facing bottleneck;
- the first implementable stage `T3a` is now closed enough on the current
  repository-selected boundary;
- the candidate-class stage `T3b` is now in place above that boundary;
- the reduction stage `T3c` is now closed enough at the inclusion-plus-
  obstruction level;
- the representative-law stage `T3d` is now closed enough at the exact
  criterion / obstruction level;
- the next active stage is `T3j`, the construction / control theorem for the
  global checked-local coefficient-extraction operator above the `T3i`
  boundary.

### `T3a`. Finite-dimensional selected-kernel bridge on the current repository selected family

Statement:
- for fixed clean `(n, q)`, let
  `L_full,n(q) = [A_int,n(q); B_full,n(q)]`,
  let the current selected reduced family be
  `A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q))`
  on the current weighted-ansatz boundary, and let
  `L_red,n(q) = L_full,n(q) V_adm,n(q)`;
- then on that repository-selected class
  `exists 0 != c in A_sel^repo,n(q) : L_full,n(q) c = 0`
  if and only if
  `exists 0 != a in R^2 : L_red,n(q) a = 0`;
- this is a finite-dimensional selected-family bridge theorem on the current
  repository boundary only;
- it is not yet the full long-term `T3`, not yet a theorem that the current
  selected class is the full exact continuum admissible clean tangent space,
  and not yet a theorem collapsing the problem to `B_red` / `B_mix`.

Status:
- packaged and closed enough on the current repository selected-class boundary;
- broader `T3` remains open beyond that boundary.

### `T3b`. Selected-class upgrade / obstruction beyond the current repository selected family

Statement:
- let
  `A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q))`
  be the current repository-selected class closed by `T3a`;
- let the strongest current theorem-facing candidate beyond that family be the
  shadow-compatible class
  `A_sel^{th,cand},n(q)`
  defined by the simultaneous conditions
  `J_0(c) in im(D_amp,n(q))`
  and
  `Q_chk(c) in im(D_rich,eta^corr,n(q)) / span(g_mem,n(q))`;
- then the implemented `T3b` step is to read the stronger theorem-facing class
  through that candidate level rather than through the shadows separately;
- this does not yet prove that `A_sel^{th,cand}` is the final intrinsic
  stronger class, and it does not yet prove
  `A_sel^repo = A_sel^{th,cand}`;
- the next theorem beyond this candidate-definition step is the exact
  comparison/losslessness theorem deciding whether the selected-class kernel
  reading for `L_full` upgrades from `A_sel^repo` to `A_sel^{th,cand}`.

Status:
- candidate-class implementation step closed enough above `T3a`;
- the comparison/losslessness question has been passed forward to `T3c`.

### `T3c`. Comparison / losslessness stage for `A_sel^repo` versus `A_sel^{th,cand}`

Statement:
- keep
  `A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q))`
  as the exact current repo-selected family;
- keep
  `A_sel^{th,cand},n(q)`
  as the shadow-compatible candidate class from `T3b`;
- then the exact active question is whether the reverse inclusion
  `A_sel^{th,cand},n(q) subseteq A_sel^repo,n(q)` holds, since the forward
  inclusion is already closed;
- equivalently, whether every shadow-compatible admissible perturbation is
  already the unique global weak/KKT-selected representative with its selected
  trace, i.e. whether
  `c = P_sel,n(q) J_0(c)` for every `c in A_sel^{th,cand},n(q)`;
- if yes, `T3a` upgrades immediately to the candidate class;
- if not yet, the exact obstruction must be stated sharply.

Status:
- Outcome B on the current repository/theory boundary:
  exact inclusion plus exact obstruction to the reverse inclusion;
- full equality/losslessness remains open;
- the next active theorem is `T3d`, which rewrites the reverse inclusion as a
  selected-representative theorem.

### `T3d`. Selected-representative theorem / obstruction for `A_sel^{th,cand}`

Statement:
- keep
  `A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q))`
  as the exact repo-selected family;
- keep
  `A_sel^{th,cand},n(q)`
  as the stronger shadow-compatible candidate class;
- then the exact active theorem is whether every `c in A_sel^{th,cand},n(q)`
  coincides with its exact repo-selected representative
  `P_sel,n(q) J_0(c)`;
- on the current repo-selected boundary this is equivalent to the fiberwise
  `H_n,q`-minimality / `H_n,q`-orthogonality theorem in the fixed-trace fiber;
- if proved, one gets
  `A_sel^{th,cand},n(q) subseteq A_sel^repo,n(q)` and hence equality/lossless
  upgrade of `T3a`;
- if not, the exact obstruction must be stated as sharply as possible.

Status:
- Outcome B on the current repository/theory boundary:
  the representative law is reduced exactly to fiberwise `H_n,q`-minimality /
  orthogonality, but candidate-class membership does not yet imply that law.

### `T3e`. Fiberwise `H_n,q`-orthogonality / zero-excess theorem for `A_sel^{th,cand}`

Statement:
- keep
  `A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q))`
  as the exact repo-selected family;
- keep
  `A_sel^{th,cand},n(q)`
  as the stronger shadow-compatible candidate class;
- for `c in A_sel^{th,cand},n(q)`, define
  `c_sel := P_sel,n(q) J_0(c)` and
  `z := c - c_sel`;
- on the current repo-selected boundary, one then has
  `z in ker(C_center,n(q))` and the exact identity
  `c^T H_n,q c = c_sel^T H_n,q c_sel + z^T H_n,q z`;
- equivalently, with
  `Delta_H,n,q(c) := (c - P_sel,n(q) J_0(c))^T H_n,q (c - P_sel,n(q) J_0(c))`,
  the active theorem is whether
  `Delta_H,n,q(c) = 0`
  for every `c in A_sel^{th,cand},n(q)`;
- if proved, one gets
  `A_sel^{th,cand},n(q) subseteq A_sel^repo,n(q)` and hence equality/lossless
  upgrade of `T3a`;
- if not, the exact obstruction must be stated through the surviving
  same-trace fiber excess.

Status:
- Outcome B on the current repository/theory boundary:
  the exact fiber-excess functional is now isolated, but candidate-class
  membership does not yet imply its vanishing.

### `T3f`. Zero-excess theorem / exact shadow-only obstruction for `A_sel^{th,cand}`

Statement:
- keep
  `A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q))`
  as the exact repo-selected family;
- keep
  `A_sel^{th,cand},n(q)`
  as the stronger shadow-compatible candidate class;
- keep from `T3e` the exact defect
  `Delta_H,n,q(c) = (c - P_sel,n(q) J_0(c))^T H_n,q (c - P_sel,n(q) J_0(c))`;
- then the exact active theorem is whether
  `Delta_H,n,q(c) = 0`
  for every `c in A_sel^{th,cand},n(q)`;
- on the current checked local boundary the quotient condition is already known
  to be representative-lossy: all currently justified local selected invariants
  factor through the quotient coordinates and do not distinguish
  representatives inside one quotient class;
- therefore the sharpened obstruction question is whether any nonzero
  admissible same-trace, quotient-invisible fiber residual can survive;
- if none survives, one gets
  `A_sel^{th,cand},n(q) subseteq A_sel^repo,n(q)` and hence equality/lossless
  upgrade of `T3a`;
- if such a residual exists, it yields `Delta_H,n,q(c) > 0` and destroys
  reverse inclusion on the current repository boundary.

Status:
- Outcome B on the current repository/theory boundary:
  the current shadow conditions are now identified as shadow-only at
  representative level, and the exact remaining gap is the existence or
  impossibility of a nonzero admissible same-trace, quotient-invisible fiber
  residual.

### `T3g`. Residual-class lift theorem / obstruction for nonzero same-trace, quotient-invisible fiber residuals

Statement:
- keep
  `A_sel^repo,n(q) := A_ls,n(q) = im(V_adm,n(q)) = im(M_amp,n(q))`
  as the exact repo-selected family;
- for `c_sel in A_sel^repo,n(q)`, define the exact same-trace residual space
  `R_same,n(q) := ker(C_center,n(q)) = ker(J_0,n(q))`;
- define the admissible quotient-invisible residual class by
  `R_inv,n(q; c_sel)
   := { z in A_adm^th,n(q) intersect R_same,n(q)
        : Q_chk(c_sel + z) = Q_chk(c_sel) }`;
- then the exact active question is whether `R_inv,n(q; c_sel)` is trivial for
  every repo-selected representative `c_sel`;
- because `Delta_H,n,q(c_sel + z) = z^T H_n,q z`, nontriviality of this class
  is equivalent to the existence of a positive-excess candidate on the current
  repository boundary;
- on the checked local boundary quotient-invisibility is carried exactly by the
  membrane-kernel direction `span(g_mem,n(q))`, so the remaining theorem is an
  exact lift problem from this local template into the global admissible
  same-trace fiber.

Status:
- Outcome B on the current repository/theory boundary:
  the remaining zero-excess gap is reduced exactly to triviality or
  nontriviality of the residual-lift class `R_inv,n(q; c_sel)`; impossibility
  and explicit existence are both still open.

### `T3h`. Global lift theorem / kernel obstruction for the local membrane-kernel line

Statement:
- keep the exact same-trace residual space
  `R_same,n(q) := ker(C_center,n(q)) = ker(J_0,n(q))`;
- on the current checked local boundary, let the corrected local coefficient
  quotient map be
  `q_coeff = [[1,0,0],[0,1,0]]`
  with
  `ker(q_coeff) = span(e_mem)`
  and
  `g_mem,n(q) = D_rich,eta^corr,n(q) e_mem`;
- for a repo-selected representative `c_sel in A_sel^repo,n(q)`, let
  `delta_chk,n(q; c_sel)` be the checked corrected local coefficient-difference
  map on admissible same-trace global residuals whenever the checked local
  shadows are defined;
- define the exact global membrane-lift class by
  `Lift_mem,n(q; c_sel)
   := { z in A_adm^th,n(q) intersect R_same,n(q)
        : delta_chk,n(q; c_sel)(z) in span(e_mem) }`;
- then
  `Lift_mem,n(q; c_sel) = R_inv,n(q; c_sel)`,
  equivalently, on the current linear tangent boundary,
  `Lift_mem,n(q; c_sel)
   = ker(q_coeff o delta_chk,n(q; c_sel)
         |_(A_adm^th,n(q) intersect ker(C_center,n(q))))`;
- so the exact active question is whether this kernel is trivial for every
  repo-selected representative.

Status:
- Outcome B on the current repository/theory boundary:
  the remaining zero-excess gap is now reduced to the exact kernel/preimage
  problem for the checked local lift map; impossibility and explicit existence
  are both still open.

### `T3i`. Injectivity / operator-control theorem for the projected checked local lift map

Statement:
- keep the exact admissible same-trace residual domain
  `D_res,n(q) := A_adm^th,n(q) intersect ker(C_center,n(q))`;
- on the checked boundary, let
  `D_res,chk,n(q; c_sel)
   := { z in D_res,n(q) : delta_chk,n(q; c_sel)(z) is defined }`;
- define the projected checked local lift map
  `Phi_chk,n(q; c_sel)
   := q_coeff o delta_chk,n(q; c_sel)
   : D_res,chk,n(q; c_sel) -> R^2_(a,b)`;
- then
  `ker(Phi_chk,n(q; c_sel)) = Lift_mem,n(q; c_sel) = R_inv,n(q; c_sel)`;
- the exact active injectivity question is therefore whether
  `ker(Phi_chk,n(q; c_sel)) = {0}`;
- on the current boundary, the sharpest conditional linear reading is:
  if there exists an explicit global checked local coefficient-extraction
  operator `chi_chk,n(q)` on `D_res,n(q)`, then
  `delta_chk,n(q; c_sel)(z) = chi_chk,n(q)(z)`,
  so `Phi_chk` becomes a fixed linear map independent of `c_sel`, and the
  remaining gap reduces to an ordinary kernel/rank theorem for
  `q_coeff o chi_chk,n(q)`.

Status:
- Outcome D on the current repository/theory boundary:
  the injectivity question is sharpened to an exact operator-construction /
  operator-control gap for the projected checked local lift map; the repo still
  does not package the needed global operator `chi_chk,n(q)`.

### `T3j`. Construction / control theorem for the global checked-local coefficient-extraction operator

Statement:
- keep the exact admissible same-trace residual domain
  `D_res,n(q) := A_adm^th,n(q) intersect ker(C_center,n(q))`;
- seek a theorem-facing linear operator
  `chi_chk,n(q) : D_res,n(q) -> R^3_(a,b,s)`
  such that, on the current tangent boundary,
  `delta_chk,n(q; c_sel)(z) = chi_chk,n(q)(z)`;
- equivalently, seek enough control that
  `Phi_chk,n(q; c_sel) = q_coeff o chi_chk,n(q)`
  becomes a fixed linear map independent of `c_sel`;
- the strongest current partial construction is local:
  on the visible checked local corrected family
  `Xi_sel,corr^(1,eta),n(q) = im(D_rich,eta^corr,n(q))`
  there is an explicit linear extractor
  `chi_chk,vis,n(q) = L_vis,n(q)|_(Xi_sel,corr^(1,eta),n(q))`
  with `L_vis,n(q) D_rich,eta^corr,n(q) = I_3`;
- under quotient-preserving chart changes the full 3-coordinate extractor is
  chart-dependent, but the projected operator `q_coeff o chi_chk,vis,n(q)` is
  chart-invariant and factors exactly through `Pi_eta_to_J0`;
- so the remaining exact gap is no longer the absence of a local extractor, but
  the absence of a global checked-local shadow map from `D_res,n(q)` into the
  checked local corrected family.

Status:
- Outcome D on the current repository/theory boundary:
  partial construction exists on the strict checked local corrected-family
  domain, but the full global operator on `D_res,n(q)` is still not closed.

### `T4`. Local quotient compatibility theorem

Statement:
- show that the checked local quotient result is compatible with the global
  selected-family reading and does not force reopening the same checked local
  branch before `T3`.

Status:
- closed enough on the current checked local boundary;
- not an all-orders local theorem.

### `T5`. Mode-wise critical-load theorem after bridge closure

Statement:
- once `T3` is in place, formulate the mode-wise critical-load theorem on the
  clean path and only then upgrade candidate competition language beyond the
  current operational level.

Status:
- open downstream target.

## D. Supporting Lemmas Already Effectively Available

- selected section / KKT-family meaning for `A_ls`;
- reduced descendant relation
  `B_red = B_full V_adm`, `B_mix = B_red G_amp`;
- selected leading-trace plane
  `J_0(A_ls) = im(D_amp)`;
- richer-trace reconciliation for the checked local branch;
- local quotient result on the checked higher-order boundary.

These are not the final theorem, but they already form the support layer for a
`T3`-oriented bridge program.

## E. Main Open Gap

The main open gap is now the `T3j` global-shadow / coefficient-extraction
theorem above the local checked extractor package between the exact
repo-selected family and the candidate class `A_sel^{th,cand}`.

This is now the central theorem-facing bottleneck because:

- the selected family is already sharp enough to use;
- the local checked branch already has a conservative stopping point at Outcome
  B;
- `B_red` and `B_mix` are already understood as descendants only;
- and the finite-dimensional repo-selected `T3a` layer is now packaged and
  closed enough;
- and the stronger theorem-facing class has now been sharpened to the candidate
  level `A_sel^{th,cand}` rather than left as shadows only;
- and the reverse inclusion problem has now been reduced to one precise
  selected-representative law;
- and that representative law has now been sharpened to one explicit
  zero-excess functional on the same fixed-trace fiber;
- and the checked local quotient condition is now explicitly known to carry no
  closed representative-level invariant beyond the same selected shadow
  coordinates;
- and the existence question is now reduced to one exact residual-lift class;
- and that residual-lift class is now sharpened further to the exact
  local-to-global kernel/preimage problem for the checked local lift map;
- and the injectivity question is now sharpened further to a partial local
  extractor package plus a missing global checked-local shadow bridge;
- but the exact bridge from candidate-class membership to triviality of that
  kernel is still not closed.

Until `T3` is addressed, the project should not pretend that a boundary-only
degeneration theorem or final physical criticality theorem is already available.

## F. Stop Rule / Strategy

- The local theorem-facing branch stays frozen for now at Outcome B.
- This roadmap does not reopen the same checked local branch.
- The dedicated `T3a` stage inside `T3` is now packaged and closed enough on
  the current repository selected family.
- The candidate-definition step `T3b` is now in place.
- The reduction step `T3c` is now in place too.
- The selected-representative criterion step `T3d` is now in place too.
- The next theorem-facing implementation should therefore stay inside `T3j`:
  construct or control a global checked-local shadow map from
  `A_adm^th,n(q) intersect ker(C_center,n(q))`
  into `Xi_sel,corr^(1,eta),n(q)` well enough that the local checked extractor
  can be composed into a theorem-facing global operator `chi_chk,n(q)` and the
  projected map `q_coeff o chi_chk,n(q)` becomes a genuine linear map whose
  kernel can be decided.
- It should not reopen the `T3a` package and should not reopen the same checked
  local branch.
- Only after that broader bridge work should the project decide whether a
  stronger local theorem or a mode-wise critical-load theorem is worth opening
  next.

## G. Current `T3a` Implementation Split

### `T3a-L1`. Selected-family identity

Statement:
- on the current weighted-ansatz repository boundary, the selected/admissible
  class used by the clean reduced architecture is
  `A_sel^repo = A_ls = im(V_adm) = im(M_amp)`.

Status:
- already effectively closed on the current repo/ansatz boundary.

Verification route:
- code inspection, manual derivation, CAS, representative live checks.

### `T3a-L2`. Reduced-object identity

Statement:
- the exact reduced object on that selected class is
  `L_red = [A_int; B_full] V_adm`,
  with descendants
  `B_red = B_full V_adm`,
  `B_mix = B_red G_amp`.

Status:
- already effectively closed on the current reduced-family boundary.

Verification route:
- code inspection, manual derivation, CAS.

### `T3a-L3`. Bijection lemma

Statement:
- the map `a -> c = V_adm a` is a linear bijection from `R^2` onto
  `A_sel^repo`.

Status:
- already effectively closed at the finite-dimensional selected-family level.

Verification route:
- manual derivation, CAS, Lean abstraction target.

### `T3a-L4`. Kernel-transfer lemma

Statement:
- `L_red a = 0` if and only if `L_full(V_adm a) = 0`;
- equivalently, the bijection from `T3a-L3` identifies `ker(L_red)` exactly
  with `A_sel^repo ∩ ker(L_full)`.

Status:
- already effectively closed at the finite-dimensional selected-family level.

Verification route:
- manual derivation, CAS, Lean abstraction target.

### `T3a-L5`. Boundary-descendant caution lemma

Statement:
- `B_red` and `B_mix` are descendants on the same selected family and remain
  operationally useful, but they do not yet replace the full stacked
  nontrivial-kernel question for `L_red`.

Status:
- already effectively closed as a theorem-facing caution layer.

Verification route:
- manual derivation, CAS, code inspection.

### Outcome-B compatibility support layer

- the checked local quotient result is a compatibility constraint on how the
  selected class may be read locally;
- it does not replace the global `T3a` bridge theorem;
- it does not reopen the same checked local branch.

### Current closure status inside `T3a`

- the dedicated packaging artifact for this stage is now
  `proof_pilots/pilot_24_t3a_selected_kernel_bridge/pilot_24_t3a_selected_kernel_bridge.md`;
- on the current repository selected boundary, no new shell-specific theorem
  ingredient is presently missing for the finite-dimensional bridge itself;
- the remaining open blocks belong to broader `T3`, not to the `T3a` package:
  continuum/theorem-facing losslessness beyond the current selected class,
  stronger local/global selected-family comparison, and any later
  boundary-only collapse theorem.

### Next implementable proof step

- keep `T3a` as the closed enough finite-dimensional bridge layer on the
  current repository selected family;
- if useful, formalize only the abstract finite-dimensional bijection/kernel
  theorem in Lean;
- keep the next broader theorem-facing effort aimed at long-term `T3`, not at
  reopening the same `T3a` package or the frozen local Outcome-B branch.

### What remains open beyond `T3a`

- whether the current selected repository class already equals the full exact
  continuum/theorem-facing admissible clean tangent space;
- whether the full reduced-kernel question can later be replaced by a
  boundary-only descendant;
- the broader long-term `T3` question beyond the current repository-selected
  boundary.

## H. Current `T3b` Implementation Split

### `T3b-I1`. Candidate-definition lemma

Statement:
- the strongest currently justified theorem-facing candidate above `T3a` is the
  shadow-compatible class
  `A_sel^{th,cand}`
  defined by
  `J_0(c) in im(D_amp)`
  and
  `Q_chk(c) in im(D_rich,eta^corr) / span(g_mem)`.

Status:
- closed enough as a candidate-definition step.

Verification route:
- manual derivation, code inspection, CAS for the already closed shadows.

### `T3b-I2`. Trace-shadow compatibility lemma

Statement:
- the candidate class must satisfy
  `J_0(A_sel^{th,cand}) subseteq im(D_amp)`;
- the repo-selected family already realizes this shadow exactly:
  `J_0(A_sel^repo) = J_0(A_ls) = im(D_amp)`.

Status:
- closed enough at the selected-trace layer.

Verification route:
- manual derivation, CAS, code inspection.

### `T3b-I3`. Quotient-shadow compatibility lemma

Statement:
- the candidate class must satisfy
  `Q_chk(A_sel^{th,cand}) subseteq im(D_rich,eta^corr) / span(g_mem)`;
- Outcome B is used only as a compatibility constraint here, and no canonical
  higher-order representative is justified beyond that quotient on the checked
  local boundary.

Status:
- closed enough as a compatibility constraint;
- broader global class interpretation remains partial.

Verification route:
- CAS, manual derivation, structural inspection.

### `T3b-I4`. Relation-to-repo lemma

Statement:
- the strongest currently justified comparison is
  `A_sel^repo subseteq A_sel^{th,cand}`;
- neither equality nor strict inclusion is currently proved.

Status:
- partial.

Verification route:
- manual derivation, CAS for the two closed shadows, code inspection.

### `T3b-I5`. Exact obstruction / upgrade lemma

Statement:
- the remaining theorem needed beyond the current implementation is the exact
  comparison/losslessness theorem deciding whether `A_sel^repo` already
  exhausts `A_sel^{th,cand}`, or whether the stronger selected-class kernel
  reading is strictly larger than the current repository family.

Status:
- open.

Verification route:
- manual derivation;
- Lean abstraction only for the conditional finite-dimensional comparison
  template once the exact comparison theorem is spelled out.

### Main bottleneck inside `T3b`

- an exact comparison/losslessness theorem deciding whether the closed
  repo-selected family `A_sel^repo` already exhausts the new candidate class
  `A_sel^{th,cand}`.

### Concrete artifact for `T3b`

- `proof_pilots/pilot_25_t3b_selected_class_upgrade/pilot_25_t3b_selected_class_upgrade.md`

### Lean / CAS / manual split for `T3b`

- Lean:
  conditional finite-dimensional class-comparison templates only, once a map or
  inclusion theorem from `A_sel^repo` to `A_sel^{th,cand}` is written in exact
  abstract form.
- CAS / code inspection:
  `A_sel^repo = A_ls = im(V_adm) = im(M_amp)`,
  `J_0(A_sel^repo) = im(D_amp)`,
  `Pi_eta_to_J0(im(D_rich,eta^corr)) = im(D_amp)`,
  `im(D_rich,eta^corr) / span(g_mem)`,
  and the descendant identities for `B_red`, `B_mix`.
- Manual derivation:
  theorem scope, candidate-class construction, exact obstruction wording, and
  the relation to the broader long-term `T3`.

## I. Current `T3c` Implementation Split

### `T3c-L1`. Repo-to-candidate inclusion lemma

Statement:
- `A_sel^repo subseteq A_sel^{th,cand}`.

Status:
- closed enough.

Verification route:
- manual derivation;
- CAS/code inspection for the exact shadow identities.

### `T3c-L2`. Selected-trace representative lemma

Statement:
- `J_0|_{A_sel^repo} : A_sel^repo -> im(D_amp)` is bijective;
- the inverse on `im(D_amp)` is the selected lift `P_sel`;
- equivalently, for `c in A_sel^repo`, one has `c = P_sel J_0(c)`.

Status:
- closed enough on the current weighted-ansatz / leading-center-jet boundary.

Verification route:
- manual derivation, CAS, code inspection, representative live clean checks.

### `T3c-L3`. Quotient-shadow collapse lemma

Statement:
- on the current checked local boundary, every currently justified local
  selected invariant factors through the quotient map `(a, b, s) -> (a, b)`;
- the canonical `J_0` trace on the corrected local family is exactly `D_amp`
  composed with that quotient map;
- therefore the quotient condition inside `A_sel^{th,cand}` adds no currently
  closed representative-level invariant beyond the same two selected
  coordinates.

Status:
- closed enough on the checked local boundary.

Verification route:
- CAS, manual derivation, structural inspection.

### `T3c-L4`. Reverse-inclusion reduction lemma

Statement:
- the reverse inclusion `A_sel^{th,cand} subseteq A_sel^repo` is equivalent to
  the selected-representative theorem
  `c = P_sel J_0(c)` for every `c in A_sel^{th,cand}`.

Status:
- closed enough as an exact reduction of the remaining gap.

Verification route:
- manual derivation, code inspection.

### `T3c-L5`. Exact obstruction lemma

Statement:
- `A_sel^repo` is the unique `H`-minimal section of a much larger fixed-center
  fiber;
- `A_sel^{th,cand}` is defined only by selected trace and checked local
  quotient compatibility;
- the checked local quotient theorem contributes no representative-level local
  invariant;
- therefore the still-open theorem is exactly the implication
  `c in A_sel^{th,cand} -> c = P_sel J_0(c)`.

Status:
- Outcome B: exact obstruction isolated, positive losslessness theorem still
  open.

Verification route:
- manual derivation;
- representative live clean evaluation for the fiber/selection side;
- CAS/theory reuse for the quotient-lossiness side.

### Main bottleneck inside `T3c`

- prove or refute the selected-representative theorem
  `c = P_sel J_0(c)` for every `c in A_sel^{th,cand}`;
- equivalently, decide whether `A_sel^{th,cand} subseteq A_sel^repo`.

### Lean / CAS / manual split for `T3c`

- Lean:
  only conditional finite-dimensional comparison templates once an exact map or
  inclusion theorem from `A_sel^{th,cand}` to `A_sel^repo` is available.
- CAS / code inspection:
  `A_sel^repo = A_ls = im(V_adm) = im(M_amp)`,
  `J_0(A_ls) = im(D_amp)`,
  the selected lift `P_sel`,
  the quotient factorization on the checked local boundary,
  and the fixed-center fiber / KKT-selected section structure.
- Manual derivation:
  exact theorem scope for `T3c`, the representative-lossiness obstruction, and
  the relation to the broader long-term `T3`.

## J. Current `T3d` Implementation Split

### `T3d-L1`. Same-trace fiber lemma

Statement:
- for `c in A_sel^{th,cand}`, letting `c_sel = P_sel J_0(c)`, one has
  `J_0(c - c_sel) = 0`;
- on the current weighted-ansatz boundary this means `c` and `c_sel` lie in the
  same fixed-trace fiber.

Status:
- closed enough.

Verification route:
- manual derivation, code inspection, CAS/theory reuse for the selected-lift
  identities.

### `T3d-L2`. Candidate-class constraints lemma

Statement:
- the candidate-class conditions force the selected trace
  `J_0(c) in im(D_amp)` and checked quotient compatibility with
  `im(D_rich,eta^corr) / span(g_mem)`;
- they do not yet impose any currently closed representative-level invariant
  beyond those selected shadow coordinates.

Status:
- closed enough.

Verification route:
- manual derivation, CAS/theory reuse, structural inspection.

### `T3d-L3`. Representative law criterion lemma

Statement:
- on the current repo-selected boundary,
  `c = P_sel J_0(c)` is equivalent to fiberwise `H_n,q`-orthogonality
  `z^T H_n,q c = 0` for every `z in ker(C_center,n(q))`;
- equivalently, it is the `H_n,q`-minimality statement in the fixed-trace
  fiber.

Status:
- closed enough.

Verification route:
- manual derivation, code inspection, representative live clean checks for the
  KKT-selected section side.

### `T3d-L4`. Obstruction lemma

Statement:
- current candidate-class membership does not yet imply the
  `H_n,q`-orthogonality / `H_n,q`-minimality condition from `T3d-L3`;
- the checked local quotient theorem is representative-lossy and does not kill
  the same-trace representative freedom;
- therefore the exact missing bridge is from shadow-compatible membership to the
  global weak/KKT-selected representative law.

Status:
- Outcome B: exact obstruction isolated.

Verification route:
- manual derivation, representative live clean evaluation for the global
  selection side, CAS/theory reuse for the quotient-lossiness side.

### `T3d-L5`. Upgrade consequence lemma

Statement:
- if one proves fiberwise `H_n,q`-orthogonality / `H_n,q`-minimality for every
  `c in A_sel^{th,cand}`, then one gets
  `c = P_sel J_0(c)`, hence
  `A_sel^{th,cand} subseteq A_sel^repo`, and therefore equality/losslessness.

Status:
- closed enough as a conditional theorem.

Verification route:
- manual derivation, Lean target after the exact law is isolated.

### Main bottleneck inside `T3d`

- prove or refute the bridge from candidate-class membership to fiberwise
  `H_n,q`-minimality / `H_n,q`-orthogonality;
- equivalently, prove or refute `c = P_sel J_0(c)` for every
  `c in A_sel^{th,cand}`.

### Lean / CAS / manual split for `T3d`

- Lean:
  only finite-dimensional fiber / representative templates once the exact law
  or exact obstruction is written in abstract form.
- CAS / code inspection:
  `P_sel`, `J_0`, fixed-center fibers, the selected trace shadow,
  the local quotient shadow, and the selected-section structure.
- Manual derivation:
  exact theorem scope for `T3d`, the `H_n,q`-minimality criterion, the exact
  obstruction wording, and the relation to the broader long-term `T3`.

## K. Current `T3e` Implementation Split

### `T3e-L1`. Fixed-trace decomposition lemma

Statement:
- for `c in A_sel^{th,cand}`, letting `c_sel = P_sel J_0(c)`, one has
  `c = c_sel + z` with
  `z in ker(C_center,n(q))`.

Status:
- closed enough.

Verification route:
- manual derivation, code inspection, CAS/theory reuse for the selected-lift
  identities.

### `T3e-L2`. Fiber-excess identity lemma

Statement:
- for the same-trace decomposition `c = c_sel + z`, one has
  `z^T H_n,q c_sel = 0`;
- therefore
  `c^T H_n,q c = c_sel^T H_n,q c_sel + z^T H_n,q z`;
- equivalently, with
  `Delta_H,n,q(c) := (c - P_sel J_0(c))^T H_n,q (c - P_sel J_0(c))`,
  the exact fiberwise excess above the selected representative is nonnegative.

Status:
- closed enough.

Verification route:
- manual derivation, code inspection, representative live clean evaluation for
  the KKT-selected section side.

### `T3e-L3`. Zero-excess criterion lemma

Statement:
- on the current repo-selected boundary, the following are equivalent:
  `c = P_sel J_0(c)`,
  `Delta_H,n,q(c) = 0`,
  fiberwise `H_n,q`-orthogonality,
  and `H_n,q`-minimality in the fixed-trace fiber.

Status:
- closed enough.

Verification route:
- manual derivation, code inspection, Lean target after the exact equivalence
  is abstracted.

### `T3e-L4`. Candidate-condition implication / obstruction lemma

Statement:
- current candidate-class membership does not yet imply
  `Delta_H,n,q(c) = 0`;
- the trace condition fixes only the selected trace plane;
- the checked local quotient theorem is representative-lossy and does not kill
  the same-trace fiber residual;
- therefore the exact surviving freedom is the same-trace fiber excess
  `Delta_H,n,q(c)`.

Status:
- Outcome B: exact obstruction isolated.

Verification route:
- manual derivation, representative live clean evaluation for the global
  selection side, CAS/theory reuse for the quotient-lossiness side.

### `T3e-L5`. Upgrade consequence lemma

Statement:
- if one proves `Delta_H,n,q(c) = 0` for every `c in A_sel^{th,cand}`, then
  one gets
  `A_sel^{th,cand} subseteq A_sel^repo`, hence equality/losslessness;
- if one constructs `c in A_sel^{th,cand}` with `Delta_H,n,q(c) > 0`, then the
  reverse inclusion fails on the current repository boundary.

Status:
- closed enough as a conditional theorem / counter-condition package.

Verification route:
- manual derivation, Lean target after the exact defect functional is
  isolated.

### Main bottleneck inside `T3e`

- prove or refute
  `Delta_H,n,q(c) = 0`
  for every `c in A_sel^{th,cand}`;
- equivalently, prove or refute vanishing of the same-trace fiber excess on the
  candidate class.

### Lean / CAS / manual split for `T3e`

- Lean:
  finite-dimensional same-trace / projection templates once the exact law is
  written in the abstract form
  `same trace + zero H-excess <-> selected representative`.
- CAS / code inspection:
  `P_sel`, `J_0`, `H_n,q`, fixed-center fibers, the selected-section structure,
  and the quotient-factorization / representative-lossiness statements on the
  checked local boundary.
- Manual derivation:
  exact theorem scope for `T3e`, the zero-excess criterion, the exact
  obstruction wording, and the relation to the broader long-term `T3`.

## L. Current `T3f` Implementation Split

### `T3f-L1`. Zero-excess decomposition lemma

Statement:
- for `c in A_sel^{th,cand}`, letting `c_sel = P_sel J_0(c)`, one has
  `c = c_sel + z` with
  `z in ker(C_center,n(q))`;
- equivalently,
  `Delta_H,n,q(c) = z^T H_n,q z`.

Status:
- closed enough.

Verification route:
- manual derivation, code inspection, CAS/theory reuse for the selected-lift
  identities.

### `T3f-L2`. Candidate-condition control lemma

Statement:
- current candidate-class membership forces only
  `J_0(c) in im(D_amp,n(q))`
  and
  `Q_chk(c) in Q_sel,loc^th,n(q)`;
- on the checked local boundary all currently justified local selected
  invariants factor through the quotient coordinates and do not distinguish
  representatives inside one quotient class;
- therefore the current shadow conditions impose no closed
  representative-level condition forcing `z = 0` or `Delta_H,n,q(c) = 0`.

Status:
- closed enough.

Verification route:
- manual derivation, CAS/theory reuse for the quotient-factorization side, code
  inspection.

### `T3f-L3`. Zero-excess theorem or exact partial implication lemma

Statement:
- on the current repo-selected boundary,
  `c = P_sel J_0(c)`,
  `Delta_H,n,q(c) = 0`,
  and `z = 0`
  are equivalent;
- but the implication
  `c in A_sel^{th,cand} -> Delta_H,n,q(c) = 0`
  is still open.

Status:
- partial.

Verification route:
- manual derivation, code inspection, Lean target after the exact equivalence
  is abstracted.

### `T3f-L4`. Exact obstruction / counterexample-template lemma

Statement:
- if there exist
  `c_sel in A_sel^repo,n(q)`
  and
  `0 != z in A_adm^th,n(q) intersect ker(C_center,n(q))`
  such that
  `Q_chk(c_sel + z) in Q_sel,loc^th,n(q)`,
  then
  `c := c_sel + z`
  lies in `A_sel^{th,cand},n(q)` and satisfies
  `Delta_H,n,q(c) = z^T H_n,q z > 0`;
- any such `z` is therefore an exact counterexample template to reverse
  inclusion / losslessness on the current repository boundary.

Status:
- Outcome B: exact conditional obstruction theorem written;
- existence or impossibility of such `z` remains open.

Verification route:
- manual derivation, representative live clean evaluation for the global
  selection side, CAS/theory reuse for the quotient-lossiness side, code
  inspection.

### `T3f-L5`. Upgrade consequence lemma

Statement:
- if one proves `Delta_H,n,q(c) = 0` for every `c in A_sel^{th,cand},n(q)`,
  then one gets
  `A_sel^{th,cand},n(q) subseteq A_sel^repo,n(q)`,
  hence equality/losslessness;
- any instance of the template in `T3f-L4` gives `Delta_H,n,q(c) > 0` and
  destroys reverse inclusion on the current boundary.

Status:
- closed enough as a conditional theorem / counter-condition package.

Verification route:
- manual derivation, Lean target after the exact defect/counterexample template
  is isolated.

### Main bottleneck inside `T3f`

- prove or refute that no nonzero admissible same-trace, quotient-invisible
  fiber residual survives on the current repo/theory boundary;
- equivalently, prove or refute `Delta_H,n,q(c) = 0` for every
  `c in A_sel^{th,cand}`.

### Lean / CAS / manual split for `T3f`

- Lean:
  finite-dimensional same-trace / zero-excess templates once the exact law and
  the conditional counterexample template are abstracted cleanly.
- CAS / code inspection:
  `P_sel`, `J_0`, `H_n,q`, fixed-center fibers, the selected-section
  structure, and the quotient-factorization / representative-lossiness
  statements on the checked local boundary.
- Manual derivation:
  exact theorem scope for `T3f`, the shadow-only obstruction wording, the
  conditional counterexample template, and the relation to the broader long-term
  `T3`.

## M. Current `T3g` Implementation Split

### `T3g-L1`. Same-trace residual lemma

Statement:
- `R_same,n(q) := ker(C_center,n(q)) = ker(J_0,n(q))`;
- for `z in R_same,n(q)` and `c_sel in A_sel^repo,n(q)`, one has
  `J_0(c_sel + z) = J_0(c_sel)`.

Status:
- closed enough.

Verification route:
- manual derivation, code inspection, representative live clean evaluation.

### `T3g-L2`. Quotient-invisibility lemma

Statement:
- define
  `R_inv,n(q; c_sel)
   := { z in A_adm^th,n(q) intersect ker(C_center,n(q))
        : Q_chk(c_sel + z) = Q_chk(c_sel) }`;
- on the current checked local boundary, quotient-invisibility is equivalent to
  having checked corrected-shadow difference in the membrane-kernel line
  `span(g_mem,n(q))`.

Status:
- closed enough on the checked local quotient boundary.

Verification route:
- manual derivation, CAS/theory reuse, code inspection.

### `T3g-L3`. Residual-class comparison lemma

Statement:
- if `z in R_inv,n(q; c_sel)`, then `c := c_sel + z` lies in
  `A_sel^{th,cand},n(q)` and satisfies
  `Delta_H,n,q(c) = z^T H_n,q z`;
- hence `z != 0` implies `Delta_H,n,q(c) > 0`.

Status:
- closed enough.

Verification route:
- manual derivation, code inspection.

### `T3g-L4`. Exact obstruction / lift lemma

Statement:
- the only currently visible local quotient-invisible template is the
  membrane-kernel line `span(g_mem,n(q))`;
- therefore the existence problem for positive-excess residuals is reduced
  exactly to the nontriviality of the lift class `R_inv,n(q; c_sel)`, i.e. to
  whether this local membrane template has a nonzero admissible global lift
  inside `ker(C_center,n(q))`.

Status:
- Outcome B: exact obstruction theorem.

Verification route:
- manual derivation, CAS/theory reuse for the local quotient side,
  representative live clean evaluation for the global selection side.

### `T3g-L5`. Zero-excess consequence lemma

Statement:
- `R_inv,n(q; c_sel) = {0}` for every `c_sel in A_sel^repo,n(q)` if and only if
  `Delta_H,n,q(c) = 0` for every `c in A_sel^{th,cand},n(q)`;
- so reverse inclusion closes exactly when the residual-lift classes are
  trivial.

Status:
- closed enough as a conditional theorem package.

Verification route:
- manual derivation, Lean target after the residual-class equivalence is
  abstracted.

### Main bottleneck inside `T3g`

- prove or refute that the local membrane-kernel template `span(g_mem,n(q))`
  has no nonzero admissible global lift inside `ker(C_center,n(q))`;
- equivalently, prove or refute `R_inv,n(q; c_sel) = {0}` for every
  `c_sel in A_sel^repo,n(q)`.

### Lean / CAS / manual split for `T3g`

- Lean:
  finite-dimensional residual-class / kernel-intersection templates once the
  exact residual class and the zero-excess equivalence are abstracted cleanly.
- CAS / code inspection:
  `P_sel`, `J_0`, `H_n,q`, `ker(C_center)`, fixed-trace fibers,
  quotient-factorization on the checked local boundary, and the exact
  membrane-kernel line `span(g_mem)`.
- Manual derivation:
  exact theorem scope for `T3g`, the lift-problem wording, why positivity of
  `H_n,q` does not decide existence, and the relation to the broader long-term
  `T3`.

## N. Current `T3h` Implementation Split

### `T3h-L1`. Global same-trace residual space lemma

Statement:
- `R_same,n(q) := ker(C_center,n(q)) = ker(J_0,n(q))`;
- for `z in R_same,n(q)` and `c_sel in A_sel^repo,n(q)`, one has
  `J_0(c_sel + z) = J_0(c_sel)`.

Status:
- closed enough.

Verification route:
- manual derivation, code inspection, representative live clean evaluation.

### `T3h-L2`. Local membrane-kernel image lemma

Statement:
- on the current checked local boundary,
  `q_coeff = [[1,0,0],[0,1,0]]`,
  `ker(q_coeff) = span(e_mem)`,
  and
  `g_mem,n(q) = D_rich,eta^corr,n(q) e_mem`;
- so `span(g_mem,n(q))` is exactly the local quotient-invisible direction.

Status:
- closed enough on the checked local quotient boundary.

Verification route:
- CAS/theory reuse, code inspection, representative helper evaluation.

### `T3h-L3`. Lift-class definition / comparison lemma

Statement:
- for fixed `c_sel in A_sel^repo,n(q)`, define
  `Lift_mem,n(q; c_sel)
   := { z in A_adm^th,n(q) intersect ker(C_center,n(q))
        : delta_chk,n(q; c_sel)(z) in span(e_mem) }`;
- then
  `Lift_mem,n(q; c_sel) = R_inv,n(q; c_sel)`;
- equivalently, on the current linear tangent boundary,
  `Lift_mem,n(q; c_sel)
   = ker(q_coeff o delta_chk,n(q; c_sel)
         |_(A_adm^th,n(q) intersect ker(C_center,n(q))))`.

Status:
- closed enough as the exact reformulation step.

Verification route:
- manual derivation, code inspection, CAS/theory reuse for the quotient map.

### `T3h-L4`. Exact obstruction / kernel lemma

Statement:
- the existence/impossibility question for nonzero admissible global lifts of
  the local membrane-kernel line is reduced exactly to the triviality or
  nontriviality of
  `ker(q_coeff o delta_chk,n(q; c_sel)
      |_(A_adm^th,n(q) intersect ker(C_center,n(q))))`;
- no theorem currently proves this kernel vanishes, and no explicit nonzero
  element is currently constructed.

Status:
- Outcome B: exact obstruction theorem.

Verification route:
- manual derivation, code inspection, representative helper evaluation.

### `T3h-L5`. Zero-excess consequence lemma

Statement:
- `Lift_mem,n(q; c_sel) = {0}` for every `c_sel in A_sel^repo,n(q)` if and
  only if `R_inv,n(q; c_sel) = {0}` for every such `c_sel`;
- hence if and only if
  `Delta_H,n,q(c) = 0` for every `c in A_sel^{th,cand},n(q)`.

Status:
- closed enough as a conditional theorem package.

Verification route:
- manual derivation, Lean target after the lift-map abstraction is isolated.

### Main bottleneck inside `T3h`

- construct or control the checked local lift-difference map
  `delta_chk,n(q; c_sel)` on
  `A_adm^th,n(q) intersect ker(C_center,n(q))`
  well enough to decide whether
  `ker(q_coeff o delta_chk,n(q; c_sel)) = {0}`;
- equivalently, prove or refute that the exact global membrane-lift class
  `Lift_mem,n(q; c_sel)` is trivial for every repo-selected representative.

### Lean / CAS / manual split for `T3h`

- Lean:
  finite-dimensional kernel/image/lift templates once the exact local-to-global
  lift map and the kernel criterion are written in abstract form.
- CAS / code inspection:
  `P_sel`, `J_0`, `H_n,q`, `ker(C_center)`, the corrected local coefficient
  quotient map `q_coeff`, the exact local membrane-kernel line
  `ker(q_coeff) = span(e_mem)`, its jet image `span(g_mem)`, and the
  local-to-global lift formulation through `delta_chk,n(q; c_sel)`.
- Manual derivation:
  exact theorem scope for `T3h`, the preimage/kernel wording for the global
  lift problem, why positivity of `H_n,q` still does not decide existence, and
  the relation to the broader long-term `T3`.

## O. Current `T3i` Implementation Split

### `T3i-L1`. Projected lift-map lemma

Statement:
- on the checked boundary, define
  `Phi_chk,n(q; c_sel) := q_coeff o delta_chk,n(q; c_sel)`
  on
  `D_res,chk,n(q; c_sel)`;
- `q_coeff` is exactly linear and quotient-preserving-chart invariant;
- `delta_chk,n(q; c_sel)` is affine in the base point by definition;
- if an explicit global linear `chi_chk,n(q)` exists on `D_res,n(q)`, then
  `delta_chk,n(q; c_sel)(z) = chi_chk,n(q)(z)`, so `Phi_chk` becomes linear
  and independent of `c_sel`.

Status:
- partial.

Verification route:
- code inspection, manual derivation, CAS/theory reuse for the local quotient
  chart.

### `T3i-L2`. Admissible residual domain lemma

Statement:
- `D_res,n(q) := A_adm^th,n(q) intersect ker(C_center,n(q))`;
- `D_res,chk,n(q; c_sel)
   := { z in D_res,n(q) : delta_chk,n(q; c_sel)(z) is defined }`.

Status:
- closed enough.

Verification route:
- manual derivation, code inspection.

### `T3i-L3`. Kernel = lift-class lemma

Statement:
- `ker(Phi_chk,n(q; c_sel)) = Lift_mem,n(q; c_sel) = R_inv,n(q; c_sel)`;
- so injectivity of `Phi_chk` on the checked residual domain is exactly
  triviality of the remaining lift class.

Status:
- closed enough.

Verification route:
- manual derivation, code inspection.

### `T3i-L4`. Exact obstruction / missing-operator lemma

Statement:
- the repository does not yet package an explicit global checked local
  coefficient-extraction operator `chi_chk,n(q)` on `D_res,n(q)`;
- therefore injectivity of `Phi_chk` is not yet a closed global rank/nullspace
  theorem on the admissible same-trace residual domain.

Status:
- Outcome D: exact missing ingredient isolated more sharply.

Verification route:
- code inspection, manual derivation, repository search for `delta_chk` /
  `chi_chk`.

### `T3i-L5`. Zero-excess consequence lemma

Statement:
- if `Phi_chk,n(q; c_sel)` is injective on the relevant residual domain for
  every repo-selected representative `c_sel`, then
  `Lift_mem,n(q; c_sel) = {0}`;
- hence `R_inv,n(q; c_sel) = {0}` and
  `Delta_H,n,q(c) = 0` on `A_sel^{th,cand},n(q)`.

Status:
- closed enough as a conditional theorem package.

Verification route:
- manual derivation, Lean target after the map/domain abstraction is isolated.

### Main bottleneck inside `T3i`

- construct or control an explicit global checked local coefficient-extraction
  operator `chi_chk,n(q)` on
  `D_res,n(q) = A_adm^th,n(q) intersect ker(C_center,n(q))`
  strongly enough that `q_coeff o chi_chk,n(q)` becomes a genuine linear map
  whose kernel can be decided.

### Lean / CAS / manual split for `T3i`

- Lean:
  finite-dimensional injectivity/kernel templates once the exact map and domain
  are abstracted in linear form.
- CAS / code inspection:
  `q_coeff`, `e_mem`, `g_mem`, quotient-preserving chart invariance,
  `P_sel`, `J_0`, `ker(C_center)`, and the current repository status of
  `delta_chk` / `chi_chk`.
- Manual derivation:
  exact theorem scope for `T3i`, the operator-level obstruction wording, and
  the relation to the broader long-term `T3`.

## P. Current `T3j` Implementation Split

### `T3j-L1`. Current `delta_chk` structure lemma

Statement:
- `delta_chk,n(q; c_sel)(z)` is best read as the difference of checked local
  coefficient vectors in a common corrected chart;
- on the local corrected-family side it is linear in the local jet variable;
- its apparent basepoint dependence comes from comparing two global objects
  through a not-yet-packaged checked local shadow map.

Status:
- closed enough.

Verification route:
- code inspection, manual derivation, CAS/theory reuse from the checked local
  chart package.

### `T3j-L2`. Local-operator construction lemma

Statement:
- on
  `Xi_sel,corr^(1,eta),n(q) = im(D_rich,eta^corr,n(q))`,
  the visible-chart extractor
  `chi_chk,vis,n(q) := L_vis,n(q)|_(Xi_sel,corr^(1,eta),n(q))`
  is linear and satisfies
  `chi_chk,vis,n(q) D_rich,eta^corr,n(q) = I_3`.

Status:
- closed enough.

Verification route:
- CAS, code inspection, manual derivation.

### `T3j-L3`. Projected local invariance lemma

Statement:
- under quotient-preserving chart changes the full 3-coordinate extractor is
  chart-dependent;
- but
  `q_coeff o chi_chk,(ell1,ell2),n(q)
   = q_coeff o chi_chk,vis,n(q)
   = L_amp o Pi_eta_to_J0`
  on `Xi_sel,corr^(1,eta),n(q)`.

Status:
- closed enough.

Verification route:
- CAS, code inspection, manual derivation.

### `T3j-L4`. Exact obstruction / partial-domain lemma

Statement:
- the repository currently provides the checked local extractor only on the
  strict checked local corrected-family domain
  `Xi_sel,corr^(1,eta),n(q)`,
  not as a theorem-facing operator on
  `D_res,n(q) = A_adm^th,n(q) intersect ker(C_center,n(q))`;
- what is missing is a global checked-local shadow map
  `Sh_chk,n(q) : D_res,n(q) -> Xi_sel,corr^(1,eta),n(q)`
  or an equivalent exact control theorem.

Status:
- Outcome D: partial construction with exact remaining gap.

Verification route:
- code inspection, manual derivation, repository search for a global checked
  local shadow operator.

### `T3j-L5`. Consequence lemma for the next injectivity step

Statement:
- if the missing global checked-local shadow map `Sh_chk,n(q)` is constructed
  or controlled, then
  `chi_chk,n(q) := chi_chk,vis,n(q) o Sh_chk,n(q)`
  becomes well-defined and the lift problem reduces to the fixed linear kernel
  question
  `Lift_mem,n(q; c_sel) = ker(q_coeff o chi_chk,n(q))`
  independent of `c_sel`.

Status:
- closed enough as a conditional theorem package.

Verification route:
- manual derivation, Lean target after the composition template is abstracted.

### Main bottleneck inside `T3j`

- construct or control a global checked-local shadow map
  `Sh_chk,n(q) : D_res,n(q) -> Xi_sel,corr^(1,eta),n(q)`
  strongly enough that
  `chi_chk,n(q) := chi_chk,vis,n(q) o Sh_chk,n(q)`
  is well-defined and the kernel of `q_coeff o chi_chk,n(q)` can be decided.

### Lean / CAS / manual split for `T3j`

- Lean:
  finite-dimensional linear-map / composition / kernel templates once the
  global shadow map and `chi_chk` composition are abstracted.
- CAS / code inspection:
  `D_rich,eta^corr`, `L_vis`, `q_coeff`, `e_mem`, `g_mem`,
  quotient-preserving chart changes, and the factorization
  `q_coeff o chi_chk,vis = L_amp o Pi_eta_to_J0`.
- Manual derivation:
  exact theorem scope for `T3j`, the distinction between the local chart-level
  extractor and the still-missing global theorem-facing operator on `D_res`,
  and the relation to the broader long-term `T3`.

### Lean / CAS split for `T3a`

- Lean:
  the finite-dimensional abstract bridge
  `L_red = L_full V`, bijectivity of `a -> V a` onto the selected class,
  and basis-independence on that class.
- CAS / code inspection:
  the live clean identities
  `A_sel^repo = A_ls = im(V_adm) = im(M_amp)`,
  `L_red = [A_int; B_full] V_adm`,
  `B_red = B_full V_adm`,
  `B_mix = B_red G_amp`,
  plus the checked local quotient compatibility.
- Manual derivation:
  theorem scope, exact selected-class wording, and the caution that this is not
  yet a final physical criticality theorem.
