# Current Theorem Roadmap For Clean Full `simple support / Р С—Р С•Р Т‘Р Р†Р С‘Р В¶Р Р…РЎвЂ№Р в„– РЎв‚¬Р В°РЎР‚Р Р…Р С‘РЎР‚`

This note records the current theorem program above the frozen local
Outcome-B boundary. It starts from the current criterion bridge note and does
not reopen the same checked local branch.

## A. Goal

The long-term theorem target is not РІР‚Сљfind a minimumРІР‚Сњ and not РІР‚Сљpromote a raw
boundary dip.РІР‚Сњ The target is to prove that criticality on the clean full
`simple support / Р С—Р С•Р Т‘Р Р†Р С‘Р В¶Р Р…РЎвЂ№Р в„– РЎв‚¬Р В°РЎР‚Р Р…Р С‘РЎР‚` path must be read through the correct
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
- the next active stage is `T3u`, the scalar-image collapse theorem,
  equivalently the vanishing theorem for the exact pairwise scalar-difference
  image `Omega_sigma,n(q; c_sel)` on the admissible exact pair domain
  underlying `Sigma_sigma,n(q; c_sel)`;
  current quotient-final checked-local invariants still do not force that
  pairwise scalar-difference image to vanish even after the `T3t` scalar-image
  package.

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

### `T3k`. Construction / control theorem for the global checked-local shadow map

Statement:
- keep
  `D_res,n(q) := A_adm^th,n(q) intersect ker(C_center,n(q))`
  and
  `Xi_sel,corr^(1,eta),n(q) := im(D_rich,eta^corr,n(q))`;
- seek a theorem-facing map
  `Sh_chk,n(q) : D_res,n(q) -> Xi_sel,corr^(1,eta),n(q)`
  strong enough that the projected lift problem factors through
  `q_coeff o chi_chk,vis,n(q) o Sh_chk,n(q)`;
- the sharpest current obstruction is:
  because
  `q_coeff o chi_chk,vis,n(q) = L_amp o Pi_eta_to_J0`
  on `Xi_sel,corr^(1,eta),n(q)` and
  `D_res,n(q) subset ker(J_0,n(q))`,
  any compatible raw `Sh_chk,n(q)` would satisfy
  `q_coeff o chi_chk,vis,n(q) o Sh_chk,n(q) = 0`;
- equivalently, any such raw shadow map must land in the membrane line
  `span(g_mem,n(q))`, so it is equivalent only to a scalar membrane-selector
  candidate, not yet to a nontrivial projected lift map;
- therefore the naive `T3j` shadow-map target on raw `D_res,n(q)` is too
  strong in the wrong direction: it collapses the projected quotient data
  identically.

Status:
- Outcome C on the current repository/theory boundary:
  an exact obstruction theorem is now available; the remaining nontrivial
  global object must be basepoint-relative or must come with a theorem killing
  the membrane selector on the same-trace residual class.

### `T3l`. Basepoint-relative representative-difference theorem or membrane-selector vanishing theorem

Statement:
- keep the raw same-trace collapse from `T3k`:
  any compatible raw shadow on
  `D_res,n(q) = A_adm^th,n(q) intersect ker(C_center,n(q))`
  already lands in the membrane line and cannot be the remaining nontrivial
  bridge by itself;
- define instead the equal-trace checked-local pair domain
  `Pair_chk,n(q)` of pairs `(c, c_ref)` whose checked local shadows are defined
  in a common corrected chart and satisfy `J_0(c) = J_0(c_ref)`;
- on that pair domain, the checked-local coefficient difference lies in
  `span(e_mem)` and is invariant under quotient-preserving chart changes;
- therefore there is a theorem-facing basepoint-relative representative-
  difference object
  `Delta_rep,chk,n(q; c, c_ref) in span(e_mem)`,
  equivalently a unique scalar membrane selector
  `sigma_chk,n(q; c, c_ref)` with
  `Delta_rep,chk = sigma_chk e_mem`;
- the next nontrivial theorem is now to prove or refute vanishing of this
  pairwise object on the exact admissible residual-generated pair domain.

Status:
- Outcome A on the current repository/theory boundary:
  the correct pairwise checked-local object is now constructed; vanishing of the
  induced selector remains open.

### `T3m`. Vanishing / nonvanishing theorem for the basepoint-relative membrane selector

Statement:
- fix a repo-selected basepoint `c_sel in A_sel^repo,n(q)`;
- define the exact residual-generated pair domain
  `D_sigma,n(q; c_sel) := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
  (c_sel + z, c_sel) in Pair_chk,n(q) }`;
- on that domain the basepoint-relative membrane selector
  `sigma_chk,n(q; c_sel)(z) := sigma_chk,n(q; c_sel + z, c_sel)` is the exact
  chart-invariant membrane-difference scalar;
- the next nontrivial question is whether `sigma_chk,n(q; c_sel)(z)` vanishes
  identically on `D_sigma,n(q; c_sel)`;
- current theorem-facing data still force only the quotient coordinates and do
  not yet kill the membrane cocycle.

Status:
- Outcome B on the current repository/theory boundary:
  the selector structure is now sharpened to an exact cocycle / obstruction
  theorem, but a vanishing theorem and an explicit admissible nonzero example
  are both still open.

### `T3n`. Uniqueness-in-membrane-quotient-class theorem

Statement:
- fix a repo-selected basepoint `c_sel in A_sel^repo,n(q)`;
- work on the exact checked-local definability subdomain
  `D_sigma,n(q; c_sel) := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
  (c_sel + z, c_sel) in Pair_chk,n(q) }`;
- the uniqueness question is whether this domain meets each equal-trace
  membrane quotient class only in the repo-selected representative, equivalently
  whether `sigma_chk,n(q; c_sel)(z) = 0` on all of `D_sigma,n(q; c_sel)`;
- on every common corrected-chart patch of that domain, the selector is exactly
  a local membrane-coordinate coboundary `s_U(z) - s_U(0)`;
- therefore vanishing is equivalent to patchwise constancy of the local
  membrane coordinate on the exact admissible residual-generated checked-local
  pair patches;
- current theorem-facing data still force only quotient coordinates and do not
  yet force that constancy.

Status:
- Outcome B on the current repository/theory boundary:
  the selector-vanishing question is now reduced further to an exact
  patchwise membrane-constancy / uniqueness-in-class obstruction theorem.

### `T3o`. Patchwise constancy theorem for the local membrane coordinate

Statement:
- fix a repo-selected basepoint `c_sel in A_sel^repo,n(q)` and the exact
  checked-local definability domain `D_sigma,n(q; c_sel)`;
- cover it by exact admissible residual-generated checked-local patches
  `D_sigma^U,n(q; c_sel)` on which a common corrected chart `U` is available and
  `sigma_chk,n(q; c_sel)(z) = s_U(z) - s_U(0)`;
- under quotient-preserving chart changes, on overlaps the local membrane
  coordinates differ only by a trace-dependent constant, so the constancy
  predicate is cover-invariant;
- therefore global vanishing of `sigma_chk` is equivalent to patchwise
  constancy of `s_U` on any exact admissible residual-generated patch cover;
- current theorem-facing data still do not force constancy on even one such
  patch.

Status:
- Outcome B on the current repository/theory boundary:
  overlap compatibility is now closed as automatic, but patchwise constancy
  itself is still not forced.

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

The main open gap is now the `T3u` scalar-image collapse theorem on the exact
admissible residual-generated domain `D_sigma,n(q; c_sel)`, sharpened further
to vanishing of the exact pairwise scalar-difference image
`Omega_sigma,n(q; c_sel)` on the full admissible exact pair domain.

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
- and the raw same-trace shadow question has already been sharpened to an exact
  obstruction theorem while the correct surviving nontrivial object has now
  been identified on equal-trace checked-local pairs;
- and that surviving object has now been sharpened further to an exact
  basepoint-relative scalar membrane cocycle on the residual-generated pair
  domain;
- and that selector question is now reduced further to exact patchwise
  constancy of the local membrane coordinate on the checked-local admissible
  pair patches;
- and overlap / chart-cover compatibility for that local membrane coordinate is
  now reduced to an automatic constant-shift rule under quotient-preserving
  chart changes;
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
- The next theorem-facing implementation should therefore stay inside `T3u`:
  prove or refute that `Sigma_sigma,n(q; c_sel) = {0}` on the full exact
  domain, equivalently prove or refute that
  `Omega_sigma,n(q; c_sel) = {0}`
  on the full exact admissible pair domain, equivalently prove or refute that
  `N_sigma,n(q; c_sel) = emptyset`,
  `Delta_rep^pt,n(q; c_sel)(z) = 0`, and
  `sigma_chk,n(q; c_sel)(z) = 0`
  for every `z in D_sigma,n(q; c_sel)`;
- no separate overlap/gluing theorem is the main bottleneck anymore, because
  patch transitions now change the membrane coordinate only by a z-independent
  constant on each fixed equal-trace class.
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
  with `A_sel^repo РІв‚¬В© ker(L_full)`.

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

## Q. Current `T3k` Implementation Split

### `T3k-L1`. Checked-local shadow-data lemma

Statement:
- on `Xi_sel,corr^(1,eta),n(q)` one has
  `q_coeff o chi_chk,vis,n(q) = L_amp o Pi_eta_to_J0`;
- so the quotient coordinates `(a,b)` are exactly the selected-trace
  coordinates on the corrected checked local family.

Status:
- closed enough.

Verification route:
- CAS, code inspection, manual derivation.

### `T3k-L2`. Zero-quotient-on-same-trace lemma

Statement:
- because
  `D_res,n(q) = A_adm^th,n(q) intersect ker(C_center,n(q))
              subset ker(J_0,n(q))`,
  any theorem-facing checked-local shadow compatible with the current quotient
  reading must project to zero under `q_coeff o chi_chk,vis`.

Status:
- closed enough.

Verification route:
- manual derivation, code inspection, theory reuse from the local quotient
  package.

### `T3k-L3`. Membrane-line factorization lemma

Statement:
- any compatible global shadow map
  `Sh_chk,n(q) : D_res,n(q) -> Xi_sel,corr^(1,eta),n(q)`
  must satisfy
  `Sh_chk,n(q)(z) in span(g_mem,n(q))`
  for every `z in D_res,n(q)`;
- equivalently it is only a scalar membrane-selector candidate
  `sigma_chk,n(q)` through
  `Sh_chk,n(q)(z) = sigma_chk,n(q)(z) g_mem,n(q)`.

Status:
- closed enough.

Verification route:
- CAS, code inspection, manual derivation.

### `T3k-L4`. Exact obstruction theorem

Statement:
- any raw basepoint-independent factorization
  `Phi_chk = q_coeff o chi_chk,vis o Sh_chk`
  on `D_res,n(q)` would be identically zero;
- therefore the naive raw-shadow target is not the correct remaining global
  bridge on the current boundary;
- the precise missing ingredient is a basepoint-relative checked-local
  representative-difference object on ambient candidate-class pairs before
  quotient collapse, or a theorem that the membrane selector vanishes.

Status:
- Outcome C: exact obstruction theorem obtained.

Verification route:
- manual derivation, code inspection, reuse of the closed quotient-finality
  theorem from pilot 23.

### `T3k-L5`. Consequence lemma for the next kernel step

Statement:
- the next nontrivial injectivity/kernel theorem cannot act on
  `q_coeff o chi_chk,vis o Sh_chk`
  over raw `D_res,n(q)` alone;
- it must either use a basepoint-relative checked-local
  representative-difference object on ambient candidate-class pairs, or prove
  directly that the admissible same-trace membrane selector vanishes.

Status:
- closed enough as a theorem-program consequence.

Verification route:
- manual derivation, Lean target only after the correct global object is
  abstracted.

### Main bottleneck inside `T3k`

- construct or control a theorem-facing basepoint-relative checked-local
  representative-difference object on ambient candidate-class pairs before
  quotient collapse, or prove directly that the admissible same-trace membrane
  selector vanishes on
  `A_adm^th,n(q) intersect ker(C_center,n(q))`.

### Lean / CAS / manual split for `T3k`

- Lean:
  finite-dimensional map/composition/kernel templates once the correct global
  object is abstracted beyond the raw `Sh_chk` target on `D_res,n(q)`.
- CAS / code inspection:
  `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, the quotient chart identities, and the zero-quotient
  collapse on the same-trace domain.
- Manual derivation:
  exact theorem scope for `T3k`, the local-vs-global shadow obstruction
  wording, why any compatible raw `Sh_chk` on `D_res,n(q)` must factor through
  the membrane line, and the relation to the broader long-term `T3`.

## R. Current `T3l` Implementation Split

### `T3l-L1`. Raw same-trace zero-collapse lemma

Statement:
- on `D_res,n(q) subset ker(J_0,n(q))`, every compatible raw checked-local
  shadow projects to zero under `q_coeff o chi_chk,vis,n(q)`.

Status:
- closed enough.

Verification route:
- manual derivation, CAS/theory reuse, code inspection.

### `T3l-L2`. Membrane-line factorization lemma

Statement:
- for every equal-trace checked-local pair `(c, c_ref)` in `Pair_chk,n(q)`,
  the checked-local coefficient difference lies in `span(e_mem)` and is
  invariant under every quotient-preserving chart change.

Status:
- closed enough.

Verification route:
- CAS, code inspection, manual derivation.

### `T3l-L3`. Basepoint-relative checked-local representative-difference construction lemma

Statement:
- the pairwise membrane-difference vector
  `Delta_rep,chk,n(q; c, c_ref) in span(e_mem)`
  is a well-defined theorem-facing object on `Pair_chk,n(q)`, independent of
  the chosen quotient-preserving corrected chart.

Status:
- closed enough.

Verification route:
- CAS, code inspection, manual derivation.

### `T3l-L4`. Membrane-selector control lemma

Statement:
- there is a unique scalar selector
  `sigma_chk,n(q; c, c_ref)` such that
  `Delta_rep,chk,n(q; c, c_ref) = sigma_chk,n(q; c, c_ref) e_mem`;
- on the residual-generated pair domain this gives
  `sigma_chk,n(q; c_sel)(z)`;
- vanishing of `sigma_chk` is equivalent to vanishing of the pairwise checked-
  local representative difference, but global vanishing on the exact admissible
  residual-generated pair domain is still open.

Status:
- partial.

Verification route:
- manual derivation, code inspection, CAS for chart invariance.

### `T3l-L5`. Exact consequence lemma for the next bridge step

Statement:
- the next nontrivial theorem can now be posed as vanishing/nonvanishing of the
  pairwise selector `sigma_chk,n(q; c_sel)(z)`, equivalently as vanishing of
  `Delta_rep,chk` on the exact admissible residual-generated pair domain.

Status:
- closed enough as a theorem-program consequence.

Verification route:
- manual derivation, Lean target after the pair domain and selector are
  abstracted.

### Main bottleneck inside `T3l`

- prove or refute that the basepoint-relative membrane selector
  `sigma_chk,n(q; c_sel)(z)` vanishes identically on the exact admissible
  residual-generated checked-local pair domain.

### Lean / CAS / manual split for `T3l`

- Lean:
  finite-dimensional pair-map / scalar-selector / kernel templates once the
  pair domain and theorem-facing selector are abstracted.
- CAS / code inspection:
  `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, raw same-trace collapse, and the invariance of pairwise
  membrane difference under quotient-preserving chart changes.
- Manual derivation:
  exact theorem scope for `T3l`, why the raw same-trace shadow target
  collapses but the pairwise equal-trace difference survives, the comparison of
  the pairwise and selector routes, and the relation to the broader long-term
  `T3`.

## S. Current `T3m` Implementation Split

### `T3m-L1`. Exact domain-of-definition lemma for `sigma_chk`

Statement:
- for fixed clean `(n, q)` and fixed repo-selected basepoint `c_sel`, the exact
  domain of the basepoint-relative membrane selector is
  `D_sigma,n(q; c_sel) := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
  (c_sel + z, c_sel) in Pair_chk,n(q) }`.

Status:
- closed enough.

Verification route:
- manual derivation, code inspection, reuse of the `T3l` pair-domain
  construction.

### `T3m-L2`. Pairwise membrane-selector structure lemma

Statement:
- on the equal-trace checked-local pair domain, `sigma_chk` is chart-invariant
  and satisfies
  `sigma_chk(c, c) = 0`,
  `sigma_chk(c, c_ref) = -sigma_chk(c_ref, c)`,
  and
  `sigma_chk(c_1, c_3) = sigma_chk(c_1, c_2) + sigma_chk(c_2, c_3)`.

Status:
- closed enough.

Verification route:
- CAS, code inspection, manual derivation.

### `T3m-L3`. Vanishing / partial-vanishing implication lemma

Statement:
- vanishing of `sigma_chk,n(q; c_sel)(z)` is equivalent to vanishing of
  `Delta_rep,chk,n(q; c_sel + z, c_sel)`;
- the current admissibility and selected-trace constraints force equality of
  the quotient coordinates `(a, b)` only and do not yet force vanishing of the
  membrane selector.

Status:
- partial.

Verification route:
- manual derivation, code inspection, CAS for the chart-invariant pair-
  difference identities.

### `T3m-L4`. Exact obstruction / nonvanishing-template lemma

Statement:
- all currently justified checked-local selected invariants factor through the
  membrane quotient, so they do not detect the scalar cocycle `sigma_chk`;
- vanishing on the full exact domain would therefore require an additional
  representative-selection theorem inside the equal-trace membrane quotient
  class;
- any admissible residual-generated pair with common corrected-chart
  coordinates `(a, b, s_sel + delta)` and `(a, b, s_sel)` and `delta != 0`
  yields the exact nonvanishing template `sigma_chk = delta != 0`.

Status:
- closed enough as an exact obstruction theorem;
- explicit admissible nonzero example still open.

Verification route:
- manual derivation, code inspection, theorem reuse from pilot 23 quotient-
  finality.

### `T3m-L5`. Exact consequence lemma for the next bridge step

Statement:
- the next nontrivial theorem is exactly one of the following equivalent
  statements:
  `sigma_chk,n(q; c_sel)(z) = 0` for every `z in D_sigma,n(q; c_sel)`;
  `Delta_rep,chk,n(q; c_sel + z, c_sel) = 0` for every
  `z in D_sigma,n(q; c_sel)`;
  or the exact residual-generated checked-local pair domain meets each
  equal-trace membrane quotient class only in the repo-selected
  representative.

Status:
- closed enough as a theorem-program consequence.

Verification route:
- manual derivation, Lean target after the selector domain and cocycle law are
  abstracted.

### Main bottleneck inside `T3m`

- prove or refute that the exact admissible residual-generated checked-local
  pair domain meets each equal-trace membrane quotient class only in the
  repo-selected representative, equivalently that
  `sigma_chk,n(q; c_sel)(z) = 0` on all of `D_sigma,n(q; c_sel)`.

### Lean / CAS / manual split for `T3m`

- Lean:
  finite-dimensional pair-map / scalar-cocycle / vanishing templates once the
  exact selector domain and cocycle laws are abstracted.
- CAS / code inspection:
  `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, the pairwise membrane-difference identities, and the
  quotient-preserving chart-change formulas.
- Manual derivation:
  exact theorem scope for `T3m`, why `sigma_chk` is the correct surviving
  representative-level object after raw same-trace collapse, why current
  theorem-facing constraints do not yet force vanishing, and the relation to
  the broader long-term `T3`.

## T. Current `T3n` Implementation Split

### `T3n-L1`. Exact domain-of-uniqueness lemma

Statement:
- for fixed clean `(n, q)` and fixed repo-selected basepoint `c_sel`,
  uniqueness is tested on
  `D_sigma,n(q; c_sel) := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
  (c_sel + z, c_sel) in Pair_chk,n(q) }`,
  not on the whole residual space by default.

Status:
- closed enough.

Verification route:
- manual derivation, code inspection, reuse of the `T3l` / `T3m` pair-domain
  package.

### `T3n-L2`. Membrane-quotient uniqueness vs selector-vanishing lemma

Statement:
- on `D_sigma,n(q; c_sel)`, the following are equivalent:
  `sigma_chk,n(q; c_sel)(z) = 0` for all `z`;
  `Delta_rep,chk,n(q; c_sel + z, c_sel) = 0` for all `z`;
  and the exact admissible residual-generated checked-local pair domain meets
  each equal-trace membrane quotient class only in the repo-selected
  representative.

Status:
- closed enough.

Verification route:
- manual derivation, code inspection.

### `T3n-L3`. Local-coboundary / patchwise-constancy lemma

Statement:
- on every common corrected-chart patch `D_sigma^U,n(q; c_sel)`, there is a
  local membrane coordinate `s_U` such that
  `sigma_chk,n(q; c_sel)(z) = s_U(z) - s_U(0)`;
- therefore selector vanishing on that patch is equivalent to constancy of
  `s_U` on that patch.

Status:
- closed enough.

Verification route:
- CAS, code inspection, manual derivation.

### `T3n-L4`. Exact obstruction / nonvanishing-template lemma

Statement:
- the current theorem-facing candidate/admissibility constraints determine only
  the quotient coordinates `(a, b)` and therefore do not yet force constancy of
  the local membrane coordinate `s_U`;
- vanishing on the full exact domain would require an additional membrane-
  constancy / unique-representative theorem on the admissible residual-
  generated checked-local pair patches;
- any patch with one point `z` satisfying `s_U(z) != s_U(0)` yields an exact
  nonvanishing template.

Status:
- closed enough as an exact obstruction theorem;
- explicit admissible nonzero example still open.

Verification route:
- manual derivation, code inspection, theorem reuse from pilot 23 quotient-
  finality.

### `T3n-L5`. Exact consequence lemma for the next bridge step

Statement:
- the next reverse-inclusion / zero-excess bridge step is exactly the theorem
  that the local membrane coordinate is constant on every exact admissible
  residual-generated checked-local pair patch, equivalently that
  `sigma_chk,n(q; c_sel)(z) = 0` on all of `D_sigma,n(q; c_sel)`.

Status:
- closed enough as a theorem-program consequence.

Verification route:
- manual derivation, Lean target after the exact domain, local-coboundary law,
  and constancy formulation are abstracted.

### Main bottleneck inside `T3n`

- prove or refute patchwise constancy of the local membrane coordinate on every
  exact admissible residual-generated checked-local pair patch, equivalently
  prove or refute that `sigma_chk,n(q; c_sel)(z) = 0` on all of
  `D_sigma,n(q; c_sel)`.

### Lean / CAS / manual split for `T3n`

- Lean:
  finite-dimensional pair-map / cocycle / local-coboundary / vanishing
  templates once the exact domain and patchwise constancy law are abstracted.
- CAS / code inspection:
  `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, pairwise membrane difference, cocycle laws, and the local
  membrane-coordinate difference formulas.
- Manual derivation:
  exact theorem scope for `T3n`, why uniqueness-in-class is equivalent to
  selector vanishing, why selector vanishing is equivalent to patchwise
  membrane constancy, why current theorem-facing constraints do not yet force
  that constancy, and the relation to the broader long-term `T3`.

## U. Current `T3o` Implementation Split

### `T3o-L1`. Exact patch-domain lemma

Statement:
- the exact admissible residual-generated checked-local patches are
  `D_sigma^U,n(q; c_sel) subseteq D_sigma,n(q; c_sel)`, where a common corrected
  chart `U` represents both `c_sel + z` and `c_sel`.

Status:
- closed enough.

Verification route:
- manual derivation, code inspection, reuse of the `T3n` local-coboundary
  package.

### `T3o-L2`. Local-coboundary vs patchwise-constancy lemma

Statement:
- on every exact patch `D_sigma^U,n(q; c_sel)`, one has
  `sigma_chk,n(q; c_sel)(z) = s_U(z) - s_U(0)`;
- therefore selector vanishing on that patch is equivalent to constancy of
  `s_U` on that patch.

Status:
- closed enough.

Verification route:
- manual derivation, CAS, code inspection.

### `T3o-L3`. Overlap-compatibility lemma

Statement:
- if `U` and `V` are two quotient-preserving corrected charts on the same fixed
  equal-trace class with coordinates related by `S_(ell1,ell2)^(-1)`, then on
  overlaps
  `s_V(z) = s_U(z) - ell1 a_sel - ell2 b_sel`,
  where `(a_sel, b_sel)` are the fixed selected-trace coordinates of the class;
- hence constancy of `s_U` on one overlap patch is equivalent to constancy of
  `s_V` there, and no separate overlap/gluing obstruction remains.

Status:
- closed enough.

Verification route:
- CAS, code inspection, manual derivation.

### `T3o-L4`. Exact obstruction / nonconstancy-template lemma

Statement:
- current theorem-facing candidate/admissibility constraints still determine
  only `(a, b)` and do not yet force constancy of `s_U` on an exact patch;
- any exact patch containing one point `z` with `s_U(z) != s_U(0)` yields the
  nonvanishing template `sigma_chk,n(q; c_sel)(z) != 0`;
- more generally, any two points `z_1, z_2` in one exact patch with
  `s_U(z_1) != s_U(z_2)` yield a nonzero pairwise selector.

Status:
- closed enough as an exact obstruction theorem;
- explicit admissible nonconstant patch still open.

Verification route:
- manual derivation, code inspection, theorem reuse from pilot 23 quotient-
  finality.

### `T3o-L5`. Exact consequence lemma for the next bridge step

Statement:
- global vanishing of `sigma_chk` on `D_sigma,n(q; c_sel)` is equivalent to
  patchwise constancy of `s_U` on any exact admissible residual-generated
  checked-local patch cover;
- the only remaining bottleneck is therefore constancy on the patches
  themselves, not compatibility across overlaps.

Status:
- closed enough as a theorem-program consequence.

Verification route:
- manual derivation, Lean target after the exact patch-domain and overlap-
  compatibility laws are abstracted.

### Main bottleneck inside `T3o`

- prove or refute constancy of `s_U` on the full exact admissible residual-
  generated checked-local patch cover; overlap compatibility is no longer the
  blocker.

### Lean / CAS / manual split for `T3o`

- Lean:
  finite-dimensional patch / coboundary / constancy templates once the exact
  patch-domain and overlap-compatibility law are abstracted.
- CAS / code inspection:
  `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, local membrane-coordinate difference formulas, cocycle laws,
  and quotient-preserving patch-overlap relations.
- Manual derivation:
  exact theorem scope for `T3o`, why overlap compatibility is automatic, why
  current theorem-facing constraints still do not force patchwise constancy,
  and the relation to the broader long-term `T3`.

## V. Current `T3p` Implementation Split

### `T3p-L1`. Exact patch-domain and patch-image lemma

Statement:
- for every exact patch `D_sigma^U,n(q; c_sel)`, the checked-local image
  `Im_chk,U,n(q; c_sel)
   := { chi_chk,U,n(q)(c_sel + z) : z in D_sigma^U,n(q; c_sel) }`
  is well-defined and satisfies
  `Im_chk,U,n(q; c_sel) subseteq { (a_sel, b_sel, s)^T : s in R }`.

Status:
- closed enough.

Verification route:
- manual derivation, code inspection, reuse of the `T3o` overlap/patch
  package.

### `T3p-L2`. Patchwise-constancy vs membrane-fiber singleton lemma

Statement:
- on every exact patch, the following are equivalent:
  `sigma_chk = 0` on the patch;
  `s_U` is constant on the patch;
  `S_U,n(q; c_sel) := { s_U(z) : z in D_sigma^U,n(q; c_sel) }` is a singleton;
  `Im_chk,U,n(q; c_sel)` is a singleton in the fixed membrane fiber.

Status:
- closed enough.

Verification route:
- manual derivation, CAS, code inspection.

### `T3p-L3`. Cover-invariant singletonity lemma

Statement:
- under quotient-preserving corrected chart changes, the membrane coordinate
  changes only by a z-independent constant shift;
- therefore singletonity of the membrane-fiber image is cover-invariant, and no
  separate overlap/gluing theorem remains.

Status:
- closed enough.

Verification route:
- CAS, code inspection, manual derivation.

### `T3p-L4`. Exact obstruction / nonconstancy-template lemma

Statement:
- current theorem-facing candidate/admissibility constraints still determine
  only the quotient base point `(a_sel, b_sel)`;
- therefore they prove only fiber containment, not fiber singletonity;
- any exact patch containing two different membrane-coordinate values yields an
  exact nonvanishing template for `sigma_chk`.

Status:
- closed enough as an exact obstruction theorem;
- explicit admissible nonsingleton patch still open.

Verification route:
- manual derivation, code inspection, theorem reuse from pilot 23 quotient-
  finality and `T3o`.

### `T3p-L5`. Exact consequence lemma for the next bridge step

Statement:
- global vanishing of `sigma_chk` on `D_sigma,n(q; c_sel)` is equivalent to
  singletonity of the exact checked-local patch image in the fixed membrane
  fiber on every patch of any exact admissible residual-generated cover;
- the only remaining bottleneck is therefore the membrane-fiber singleton
  theorem itself.

Status:
- closed enough as a theorem-program consequence.

Verification route:
- manual derivation, Lean target after the exact patch-image and singletonity
  laws are abstracted.

### Main bottleneck inside `T3p`

- prove or refute that for every exact admissible residual-generated checked-
  local patch, the membrane-fiber image is a singleton, equivalently prove or
  refute patchwise constancy of `s_U`, equivalently prove or refute that
  `sigma_chk,n(q; c_sel)(z) = 0` on all of `D_sigma,n(q; c_sel)`.

### Lean / CAS / manual split for `T3p`

- Lean:
  finite-dimensional patch-image / singletonity / constancy templates once the
  exact patch-domain and membrane-fiber image law are abstracted.
- CAS / code inspection:
  `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, local membrane-coordinate difference formulas, and the exact
  patchwise chart formulas with fixed `(a_sel, b_sel)`.
- Manual derivation:
  exact theorem scope for `T3p`, why overlap compatibility is no longer
  independent after `T3o`, why current theorem-facing constraints force only
  fiber containment and not singletonity, and the relation to the broader long-
  term `T3`.


## W. Current T3q Implementation Split

### T3q-L1. Exact patch-domain / representative-law lemma

Statement:
- keep the exact global domain D_sigma,n(q; c_sel) and the exact patch family
  D_sigma^U,n(q; c_sel) from T3p;
- on every exact patch define the representative law
  Rep_U,n(q; c_sel) by
  chi_chk,U,n(q)(c_sel + z_1) = chi_chk,U,n(q)(c_sel + z_2) for all
  z_1, z_2 in D_sigma^U,n(q; c_sel);
- because the quotient coordinates are fixed on the patch, Rep_U is exactly
  equivalent to singletonity of Im_chk,U,n(q; c_sel) in the fixed membrane
  fiber.

Status:
- closed enough.

Verification route:
- manual derivation, code inspection, reuse of the T3p patch-image package.

### T3q-L2. Representative-law vs selector-vanishing lemma

Statement:
- on every exact patch, the following are equivalent:
  Rep_U;
  sigma_chk = 0 on the patch;
  s_U is constant on the patch;
  S_U is a singleton;
  Im_chk,U is a singleton in the fixed membrane fiber.

Status:
- closed enough.

Verification route:
- manual derivation, CAS, code inspection.

### T3q-L3. Quotient-finality obstruction lemma

Statement:
- the canonical J_0 trace, the checked local residual, and the next checked
  local compatibility layer all factor through the quotient map (a, b, s) ->
  (a, b) or are blind along the membrane line on the current checked
  boundary;
- the strongest currently checked selector candidates remain chart-dependent,
  metric-dependent, or extrinsic;
- therefore the currently closed quotient-final theorem-facing package does not
  force Rep_U on an exact patch.

Status:
- closed enough as an exact obstruction theorem.

Verification route:
- theorem reuse from pilot 23 quotient-finality, code inspection, manual
  derivation.

### T3q-L4. Exact non-singleton / nonvanishing-template lemma

Statement:
- if one exact admissible patch contains two points with the same quotient
  coordinates (a_sel, b_sel) and different membrane coordinates s_1 != s_2,
  then all currently closed quotient-final invariants agree on that pair while
  singletonity fails and the pairwise selector is nonzero.

Status:
- closed enough as an exact obstruction/template theorem;
- explicit admissible realization still open.

Verification route:
- manual derivation, theorem reuse from T3l / T3m / T3p, code inspection.

### T3q-L5. Exact consequence lemma for the next bridge step

Statement:
- if one proves Rep_U,n(q; c_sel) on every exact admissible residual-
  generated patch of every exact cover, then sigma_chk vanishes on
  D_sigma,n(q; c_sel) and the remaining membrane obstruction in the reverse-
  inclusion / zero-excess bridge disappears on the current boundary;
- conversely, any admissible non-singleton patch yields an exact nonvanishing
  obstruction.

Status:
- closed enough as a theorem-program consequence.

Verification route:
- manual derivation, Lean target after the exact representative-law abstraction
  is packaged.

### Main bottleneck inside T3q

- prove or refute the exact patchwise representative law on every exact
  admissible residual-generated checked-local patch, equivalently prove or
  refute singletonity of the exact checked-local patch image in the fixed
  membrane fiber, equivalently prove or refute that
  sigma_chk,n(q; c_sel)(z) = 0 on all of D_sigma,n(q; c_sel);
- no further quotient-final theorem alone can close this gap.

### Lean / CAS / manual split for T3q

- Lean:
  finite-dimensional patch-image / representative-law / singletonity templates
  once the exact patch-domain and fixed-fiber formulation are abstracted.
- CAS / code inspection:
  D_rich,eta^corr, chi_chk,vis, q_coeff, e_mem, g_mem, J_0,
  ker(C_center), exact patchwise chart formulas, and the factorization of the
  currently justified checked-local invariants through the quotient map.
- Manual derivation:
  exact theorem scope for T3q, why current theorem-facing constraints remain
  quotient-final on the exact patches, why singletonity and patchwise
  constancy are equivalent rather than distinct after T3p, and the relation
  to the broader long-term T3.

## X. Current `T3r` Implementation Split

### `T3r-L1`. Exact patch-domain / fixed-fiber / pointwise-difference lemma

Statement:
- keep the exact global domain `D_sigma,n(q; c_sel)` and the exact patch family
  `D_sigma^U,n(q; c_sel)` from `T3q`;
- on every exact patch define the pointwise basepoint-relative representative
  difference
  `Delta_rep,U^pt,n(q; c_sel)(z)
   := chi_chk,U,n(q)(c_sel + z) - chi_chk,U,n(q)(c_sel)`;
- because both representatives lie in the same fixed membrane fiber,
  `Delta_rep,U^pt(z) = sigma_chk,n(q; c_sel)(z) e_mem` and therefore
  `Delta_rep,U^pt(z) in span(e_mem)`.

Status:
- closed enough.

Verification route:
- manual derivation, CAS, code inspection.

### `T3r-L2`. Pairwise representative law vs pointwise basepoint law lemma

Statement:
- on every exact patch, the following are equivalent:
  `Rep_U`;
  `chi_chk,U(c_sel + z) = chi_chk,U(c_sel)` for all `z` on the patch;
  `Delta_rep,U^pt = 0` on the patch;
  `sigma_chk = 0` on the patch;
  `s_U` is constant on the patch;
  `Im_chk,U` is a singleton in the fixed membrane fiber.

Status:
- closed enough.

Verification route:
- manual derivation, CAS, code inspection.

### `T3r-L3`. Quotient-finality obstruction lemma

Statement:
- current theorem-facing admissibility and candidate constraints still force
  only the fixed quotient coordinates `(a_sel, b_sel)`;
- therefore they force only
  `Delta_rep,U^pt(z) in span(e_mem)`,
  not
  `Delta_rep,U^pt(z) = 0`;
- so the currently closed quotient-final package does not force `Rep_U`.

Status:
- closed enough as an exact obstruction theorem.

Verification route:
- theorem reuse from pilot 23 quotient-finality, code inspection, manual
  derivation.

### `T3r-L4`. Exact one-point non-singleton / nonvanishing-template lemma

Statement:
- failure of `Rep_U` on an exact patch is equivalent to existence of one point
  `z_*` on that patch with
  `Delta_rep,U^pt,n(q; c_sel)(z_*) = delta_* e_mem`,
  `delta_* != 0`;
- equivalently one exact patch point already realizes a distinct membrane
  coordinate above the same fixed quotient point `(a_sel, b_sel)`.

Status:
- closed enough as an exact obstruction/template theorem;
- explicit admissible realization still open.

Verification route:
- manual derivation, theorem reuse from `T3m` / `T3q`, code inspection.

### `T3r-L5`. Exact consequence lemma for the next bridge step

Statement:
- if one proves the pointwise basepoint law on every exact admissible
  residual-generated checked-local patch of every exact cover, then `Rep_U`
  holds on every such patch, `sigma_chk` vanishes on `D_sigma,n(q; c_sel)`,
  and the remaining membrane obstruction in the reverse-inclusion / zero-excess
  bridge disappears on the current boundary.

Status:
- closed enough as a theorem-program consequence.

Verification route:
- manual derivation, Lean target after the pointwise basepoint-relative law is
  abstracted.

### Main bottleneck inside `T3r`

- prove or refute the pointwise basepoint-relative law
  `chi_chk,U,n(q)(c_sel + z) = chi_chk,U,n(q)(c_sel)` for every `z` on every
  exact admissible residual-generated checked-local patch;
- equivalently prove or refute that
  `Delta_rep,U^pt,n(q; c_sel)(z) = 0`
  on the full exact patch cover;
- no further quotient-final theorem alone can close this gap.

### Lean / CAS / manual split for `T3r`

- Lean:
  finite-dimensional patch-image / pointwise representative-law /
  selector-vanishing templates once the exact patch-domain and pointwise
  basepoint-relative difference law are abstracted.
- CAS / code inspection:
  `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, exact patchwise chart formulas, and the identity
  `Delta_rep,U^pt = sigma_chk e_mem`.
- Manual derivation:
  exact theorem scope for `T3r`, why the pairwise representative law reduces
  to a pointwise basepoint law, why current theorem-facing constraints still
  do not force that pointwise vanishing, and the relation to the broader
  long-term `T3`.

## Y. Current `T3s` Implementation Split

### `T3s-L1`. Exact pointwise domain / chart-invariant pointwise-difference lemma

Statement:
- the patchwise pointwise-difference maps
  `Delta_rep,U^pt,n(q; c_sel)` glue on overlaps and define an exact chart-
  invariant map
  `Delta_rep^pt,n(q; c_sel) : D_sigma,n(q; c_sel) -> span(e_mem)`;
- equivalently for every `z in D_sigma,n(q; c_sel)` and every patch `U`
  containing `z`, one has
  `Delta_rep^pt,n(q; c_sel)(z) = Delta_rep,U^pt,n(q; c_sel)(z)`;
- this map satisfies
  `Delta_rep^pt,n(q; c_sel)(z) = sigma_chk,n(q; c_sel)(z) e_mem`.

Status:
- closed enough.

Verification route:
- manual derivation, CAS, code inspection.

### `T3s-L2`. Pointwise law vs selector-vanishing vs `Rep_U` lemma

Statement:
- on the exact domain `D_sigma,n(q; c_sel)`, the following are equivalent:
  `Delta_rep^pt = 0` on `D_sigma`;
  `sigma_chk = 0` on `D_sigma`;
  `Rep_U` on every exact patch;
  patchwise constancy of `s_U`;
  patchwise singletonity of `Im_chk,U`.

Status:
- closed enough.

Verification route:
- manual derivation, CAS, code inspection.

### `T3s-L3`. Pointwise codomain / normalization obstruction lemma

Statement:
- current theorem-facing admissibility and candidate constraints still force
  only
  `Delta_rep^pt(D_sigma,n(q; c_sel)) subseteq span(e_mem)`
  and the normalization
  `Delta_rep^pt,n(q; c_sel)(0) = 0`;
- they do not force full pointwise vanishing on `D_sigma,n(q; c_sel)`.

Status:
- closed enough as an exact obstruction theorem.

Verification route:
- theorem reuse from pilot 23 quotient-finality, code inspection, manual
  derivation.

### `T3s-L4`. Exact pointwise nonzero-set / one-point template lemma

Statement:
- define
  `N_sigma,n(q; c_sel)
   := { z in D_sigma,n(q; c_sel) :
        Delta_rep^pt,n(q; c_sel)(z) != 0 }`;
- failure of the `T3s` pointwise law is exactly equivalent to
  `N_sigma,n(q; c_sel) != emptyset`;
- equivalently there exists one point `z_* in D_sigma,n(q; c_sel)` with
  `Delta_rep^pt,n(q; c_sel)(z_*) = delta_* e_mem`, `delta_* != 0`.

Status:
- closed enough as an exact obstruction/template theorem;
- explicit admissible realization still open.

Verification route:
- manual derivation, theorem reuse from `T3m` / `T3o` / `T3r`, code inspection.

### `T3s-L5`. Exact consequence lemma for the next bridge step

Statement:
- if one proves `N_sigma,n(q; c_sel) = emptyset` for every exact domain, then
  the pointwise law holds globally, `Rep_U` holds on every exact patch,
  `sigma_chk` vanishes on `D_sigma,n(q; c_sel)`, and the remaining membrane
  obstruction in the reverse-inclusion / zero-excess bridge disappears on the
  current boundary.

Status:
- closed enough as a theorem-program consequence.

Verification route:
- manual derivation, Lean target after the chart-invariant pointwise-defect law
  is abstracted.

### Main bottleneck inside `T3s`

- prove or refute that `N_sigma,n(q; c_sel) = emptyset` on the full exact
  pair-definability domain `D_sigma,n(q; c_sel)`;
- equivalently prove or refute that
  `Delta_rep^pt,n(q; c_sel)(z) = 0`
  for every `z in D_sigma,n(q; c_sel)`;
- no further quotient-final theorem alone can close this gap.

### Lean / CAS / manual split for `T3s`

- Lean:
  finite-dimensional exact-domain / chart-invariant pointwise-defect / nonzero-
  set templates once the overlap law and codomain `span(e_mem)` are abstracted.
- CAS / code inspection:
  `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, the quotient-preserving chart-change matrices, the identity
  `S_(ell1,ell2)^(-1) e_mem = e_mem`, and `Delta_rep^pt = sigma_chk e_mem`.
- Manual derivation:
  exact theorem scope for `T3s`, why the patchwise pointwise law descends to a
  chart-invariant global pointwise defect map, why current theorem-facing
  constraints still do not force its vanishing, and the relation to the broader
  long-term `T3`.
## Z. Current `T3t` Implementation Split

### `T3t-L1`. Exact global defect-map / scalar defect-image / defect-set lemma

Statement:
- on the exact domain `D_sigma,n(q; c_sel)`, define
  `N_sigma,n(q; c_sel)
   := { z in D_sigma,n(q; c_sel) : Delta_rep^pt,n(q; c_sel)(z) != 0 }`
  and
  `Sigma_sigma,n(q; c_sel)
   := { sigma_chk,n(q; c_sel)(z) : z in D_sigma,n(q; c_sel) }`;
- then
  `N_sigma,n(q; c_sel) = emptyset`
  if and only if
  `Sigma_sigma,n(q; c_sel) = {0}`.

Status:
- closed enough.

Verification route:
- manual derivation, CAS, code inspection.

### `T3t-L2`. Pairwise defect-difference factorization lemma

Statement:
- whenever `(c_sel + z_1, c_sel + z_2) in Pair_chk,n(q)`, one has
  `Delta_rep,chk,n(q; c_sel + z_1, c_sel + z_2)
   = (sigma_chk,n(q; c_sel)(z_1) - sigma_chk,n(q; c_sel)(z_2)) e_mem`;
- so all surviving pairwise representative-sensitive differences factor through
  scalar defect-value differences.

Status:
- closed enough.

Verification route:
- manual derivation, theorem reuse from `T3m` / `T3s`, code inspection.

### `T3t-L3`. Emptiness vs selector-vanishing vs image-collapse lemma

Statement:
- on `D_sigma,n(q; c_sel)`, the following are equivalent:
  `N_sigma = emptyset`;
  `Sigma_sigma = {0}`;
  `Delta_rep^pt = 0` on `D_sigma`;
  `sigma_chk = 0` on `D_sigma`;
  `Rep_U` on every exact patch.

Status:
- closed enough.

Verification route:
- manual derivation, CAS, code inspection.

### `T3t-L4`. Exact obstruction / nonempty-template lemma

Statement:
- failure of `T3t` is exactly equivalent to
  `N_sigma,n(q; c_sel) != emptyset`, equivalently
  `Sigma_sigma,n(q; c_sel) != {0}`;
- equivalently there exists one point `z_* in D_sigma,n(q; c_sel)` with
  `Delta_rep^pt,n(q; c_sel)(z_*) = delta_* e_mem`, `delta_* != 0`.

Status:
- closed enough as an exact obstruction/template theorem;
- explicit admissible realization still open.

Verification route:
- manual derivation, theorem reuse from `T3s`, code inspection.

### `T3t-L5`. Exact consequence lemma for the next bridge step

Statement:
- if one proves `Sigma_sigma,n(q; c_sel) = {0}` for every exact domain, then
  `N_sigma,n(q; c_sel) = emptyset`, `sigma_chk` vanishes on `D_sigma`,
  `Rep_U` holds on every exact patch, and the remaining membrane obstruction in
  the reverse-inclusion / zero-excess bridge disappears on the current
  boundary.

Status:
- closed enough as a theorem-program consequence.

Verification route:
- manual derivation, Lean target after the scalar defect-image abstraction is
  packaged.

### Main bottleneck inside `T3t`

- prove or refute that `Sigma_sigma,n(q; c_sel) = {0}` on the full exact
  domain `D_sigma,n(q; c_sel)`;
- equivalently prove or refute that `N_sigma,n(q; c_sel) = emptyset`;
- no further quotient-final theorem alone can close this gap.

### Lean / CAS / manual split for `T3t`

- Lean:
  finite-dimensional exact-domain / chart-invariant pointwise-defect /
  scalar-image / defect-set templates once `Delta_rep^pt`, `Sigma_sigma`, and
  `N_sigma` are abstracted.
- CAS / code inspection:
  `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, the quotient-preserving chart-change matrices, the identity
  `S_(ell1,ell2)^(-1) e_mem = e_mem`, `Delta_rep^pt = sigma_chk e_mem`, and
  the pairwise factorization through scalar defect-value differences.
- Manual derivation:
  exact theorem scope for `T3t`, why emptiness of `N_sigma` is equivalent to
  collapse of `Sigma_sigma` to `{0}`, why current theorem-facing constraints
  still do not force that collapse, and the relation to the broader long-term
  `T3`.

## AA. Current `T3u` Implementation Split

### `T3u-L1`. Exact scalar-image / defect-set / pairwise-difference lemma

Statement:
- on the exact domain `D_sigma,n(q; c_sel)`, the scalar selector
  `sigma_chk,n(q; c_sel) : D_sigma,n(q; c_sel) -> R`
  determines the exact scalar image `Sigma_sigma`, the exact defect set
  `N_sigma`, and the exact pairwise scalar-difference image `Omega_sigma`;
- moreover
  `Sigma_sigma = {0}`
  if and only if
  `N_sigma = emptyset`
  if and only if
  `Omega_sigma = {0}`.

Status:
- closed enough.

Verification route:
- manual derivation, CAS, code inspection.

### `T3u-L2`. Scalar-image collapse vs selector-vanishing lemma

Statement:
- on `D_sigma,n(q; c_sel)`, the following are equivalent:
  `Sigma_sigma = {0}`;
  `N_sigma = emptyset`;
  `sigma_chk = 0` on `D_sigma`;
  `Delta_rep^pt = 0` on `D_sigma`;
  `Rep_U` on every exact patch.

Status:
- closed enough.

Verification route:
- manual derivation, CAS, code inspection.

### `T3u-L3`. Exact scalar-difference / cocycle package lemma

Statement:
- the exact pairwise scalar-difference image `Omega_sigma` satisfies
  `0 in Omega_sigma`,
  `Omega_sigma = -Omega_sigma`,
  and the additive cocycle law wherever the three exact admissible pairs are
  defined.

Status:
- closed enough.

Verification route:
- theorem reuse from `T3m` / `T3t`, manual derivation, code inspection.

### `T3u-L4`. Exact obstruction / nonzero-scalar-template lemma

Statement:
- failure of `T3u` is exactly equivalent to
  `Sigma_sigma != {0}`, equivalently
  `N_sigma != emptyset`, equivalently
  `Omega_sigma != {0}`;
- equivalently there exists one point `z_* in D_sigma,n(q; c_sel)` with
  `sigma_chk,n(q; c_sel)(z_*) = delta_* != 0`.

Status:
- closed enough as an exact obstruction/template theorem;
- explicit admissible realization still open.

Verification route:
- manual derivation, theorem reuse from `T3t`, code inspection.

### `T3u-L5`. Exact consequence lemma for the next bridge step

Statement:
- if one proves `Omega_sigma,n(q; c_sel) = {0}` for every exact domain, then
  `Sigma_sigma = {0}`, `N_sigma = emptyset`, `sigma_chk` vanishes on
  `D_sigma`, `Rep_U` holds on every exact patch, and the remaining membrane
  obstruction in the reverse-inclusion / zero-excess bridge disappears on the
  current boundary.

Status:
- closed enough as a theorem-program consequence.

Verification route:
- manual derivation, Lean target after the scalar-map / scalar-difference
  abstraction is packaged.

### Main bottleneck inside `T3u`

- prove or refute that `Omega_sigma,n(q; c_sel) = {0}` on the full exact
  admissible pair domain;
- equivalently prove or refute that `Sigma_sigma,n(q; c_sel) = {0}`;
- no further quotient-final theorem alone can close this gap.

### Lean / CAS / manual split for `T3u`

- Lean:
  finite-dimensional exact-domain / scalar map / scalar-image / defect-set /
  pairwise scalar-difference templates once `sigma_chk`, `Sigma_sigma`,
  `N_sigma`, and `Omega_sigma` are abstracted.
- CAS / code inspection:
  `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, chart-change identities, `Delta_rep^pt = sigma_chk e_mem`,
  the pairwise factorization through scalar defect-value differences, and the
  scalar-image formulas.
- Manual derivation:
  exact theorem scope for `T3u`, why scalar-image collapse is equivalent to
  vanishing of `Omega_sigma`, why current theorem-facing constraints still do
  not force that vanishing, and the relation to the broader long-term `T3`.


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
## AB. Current `T3v` Implementation Split

### `T3v-L1`. Exact admissible pair-domain / pairwise-image lemma

Statement:
- define the exact admissible pair domain
  `Pair_sigma,n(q; c_sel)
   := { (z_1, z_2) in D_sigma,n(q; c_sel)^2 :
        (c_sel + z_1, c_sel + z_2) in Pair_chk,n(q) }`;
- define the exact pairwise scalar-difference image
  `Omega_sigma,n(q; c_sel)
   := { sigma_chk(z_1) - sigma_chk(z_2) :
        (z_1, z_2) in Pair_sigma,n(q; c_sel) }`;
- then `Omega_sigma` is chart-invariant and satisfies
  `Sigma_sigma subseteq Omega_sigma subseteq Sigma_sigma - Sigma_sigma`.

Status:
- closed enough.

Verification route:
- manual derivation, CAS, code inspection.

### `T3v-L2`. Pairwise-collapse vs scalar-image-collapse lemma

Statement:
- on `D_sigma,n(q; c_sel)`, the following are equivalent:
  `Omega_sigma = {0}`;
  `Sigma_sigma = {0}`;
  `N_sigma = emptyset`;
  `sigma_chk = 0` on `D_sigma`;
  `Delta_rep^pt = 0` on `D_sigma`;
  `Rep_U` on every exact patch.

Status:
- closed enough.

Verification route:
- manual derivation, theorem reuse from `T3t` / `T3u`, code inspection.

### `T3v-L3`. Pairwise-factorization / basepoint-star reduction lemma

Statement:
- whenever `(z_1, z_2) in Pair_sigma,n(q; c_sel)`, one has
  `Delta_rep,chk,n(q; c_sel + z_1, c_sel + z_2)
   = (sigma_chk(z_1) - sigma_chk(z_2)) e_mem`;
- because `(z, 0) in Pair_sigma,n(q; c_sel)` for every `z in D_sigma`, no
  separate pair-completeness theorem is required to reduce collapse of
  `Omega_sigma` to vanishing of the basepoint-relative values of `sigma_chk`.

Status:
- closed enough.

Verification route:
- manual derivation, theorem reuse from `T3l` / `T3m` / `T3u`, code inspection.

### `T3v-L4`. Exact quotient-final obstruction / nonzero-pairwise-template lemma

Statement:
- on the current checked boundary, the current theorem-facing candidate /
  admissibility package is quotient-final: it fixes `(a_sel, b_sel)` and the
  scalar cocycle package, but not equality of membrane coordinates inside the
  fixed quotient fiber;
- therefore current theorem-facing constraints do not force
  `Omega_sigma,n(q; c_sel) = {0}`;
- failure is exactly compatible with the template
  `(z_1, z_2) in Pair_sigma`,
  `chi_chk,chart(c_sel + z_i) = (a_sel, b_sel, s_i)^T`,
  `s_1 - s_2 != 0`.

Status:
- Outcome B: exact obstruction theorem obtained; explicit admissible nonzero
  pair still open.

Verification route:
- manual derivation, theorem reuse from pilot 23 quotient-finality and `T3u`,
  code inspection.

### `T3v-L5`. Exact consequence lemma for the next bridge step

Statement:
- if one proves `Omega_sigma,n(q; c_sel) = {0}` for every fixed clean `(n, q)`
  and repo-selected basepoint `c_sel`, then `Sigma_sigma = {0}`,
  `N_sigma = emptyset`, `sigma_chk` vanishes on `D_sigma`, `Delta_rep^pt = 0`
  on the full exact domain, `Rep_U` holds on every exact patch, and the
  remaining membrane obstruction in the reverse-inclusion / zero-excess bridge
  disappears on the current boundary.

Status:
- closed enough as a conditional theorem package.

Verification route:
- manual derivation, Lean target after the exact pair-domain / scalar-
  difference-image abstraction is packaged.

### Main bottleneck inside `T3v`

- prove or refute one representative-sensitive rigidity law on the exact
  admissible pair domain:
  there do not exist exact admissible pair data `(z_1, z_2) in Pair_sigma`
  with the same quotient coordinates `(a_sel, b_sel)` and different membrane
  coordinates `s_1 != s_2`;
- equivalently prove or refute that `Omega_sigma,n(q; c_sel) = {0}`.

### Lean / CAS / manual split for `T3v`

- Lean:
  finite-dimensional exact-domain / exact pair-domain / scalar-image /
  pairwise scalar-difference / defect-set templates after abstracting
  `sigma_chk`, `Sigma_sigma`, `Omega_sigma`, and `N_sigma`.
- CAS / code inspection:
  `D_rich,eta^corr`, `chi_chk,vis`, `q_coeff`, `e_mem`, `g_mem`, `J_0`,
  `ker(C_center)`, quotient-preserving chart-change identities, the fixed-fiber
  coordinate law `chi_chk,chart(c_sel + z_i) = (a_sel, b_sel, s_i)^T`, and the
  identities `Delta_rep^pt = sigma_chk e_mem` and
  `Delta_rep,chk = (sigma_chk(z_1) - sigma_chk(z_2)) e_mem`.
- Manual derivation:
  exact theorem scope for `T3v`, why `Pair_sigma` is the correct exact pair
  domain, why current theorem-facing constraints still do not force pairwise
  scalar-difference collapse, and how `T3v` relates to the later reverse-
  inclusion / zero-excess bridge below full `T3`.

## Admissible-lift branch after the saturated `T3` chain

- keep the already closed global selected full-center lift
  `X_sel,n(q) := im(P_sel,n(q))` with `C_center,n(q) P_sel,n(q) = I_4`;
- the restricted map `C_center|_(X_sel)` is therefore bijective, with inverse
  `P_sel`;
- for every clean `(n, q)` and every repo-selected basepoint `c_sel in A_ls`,
  the selected-architecture lift class
  `Lift_mem^sel,n(q; c_sel)
   := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
        c_sel + z in X_sel,n(q),
        (c_sel + z, c_sel) in Pair_chk,n(q) }`
  satisfies the exact obstruction theorem
  `Lift_mem^sel,n(q; c_sel) = {0}`;
- equivalently,
  `A_sel^{th,cand},n(q) intersect X_sel,n(q) = A_ls,n(q)`;
- hence any nonzero admissible global lift of the local membrane mode, if it
  exists at all, must lie outside the current KKT-selected global architecture
  `X_sel`, and in particular outside `A_ls`;
- the next admissible-lift bottleneck is therefore not inside `X_sel`, but the
  existence or impossibility of candidate-class points in
  `A_sel^{th,cand},n(q) \ X_sel,n(q)` whose same-trace residual remains
  checked-local pair-definable and membrane-visible.
## Extrinsic admissible-lift branch after the `X_sel` obstruction

- the exact intersection law
  `X_sel,n(q) intersect ker(C_center,n(q)) = {0}`
  follows from `C_center,n(q) P_sel,n(q) = I_4`;
- hence for every repo-selected basepoint `c_sel in A_ls subset X_sel` and every
  nonzero residual direction `0 != z in A_adm^th,n(q) intersect ker(C_center,n(q))`,
  one automatically has `c_sel + z notin X_sel,n(q)`;
- so outside-`X_sel` is no longer an independent condition in the lift branch;
- the extrinsic admissible-lift problem is now exactly to decide whether there
  exists a nonzero direction in the residual fiber
  `A_adm^th,n(q) intersect ker(C_center,n(q))`
  that is both checked-local pair-definable with `c_sel` and membrane-visible;
- the single remaining exact blocking condition is therefore a global-to-local
  theorem on that residual fiber deciding pair-definability and the resulting
  representative-sensitive membrane deviation.
## Residual-fiber low-order jet obstruction on the active clean branch

- for the residual fiber `R_res,n(q) := A_adm^th,n(q) intersect ker(C_center,n(q))`,
  any nonzero candidate `z` that is checked-local pair-definable with `c_sel`
  and membrane-visible must have augmented checked-local residual jet in the
  one-dimensional line
  `span(g_mem^aug,n(q))`, where
  `g_mem^aug,n(q) = [0,0,0,0,alpha,0,0,0,beta,1]`;
- equivalently, under the same pilot-23 nonresonance regime its first checked
  nontrivial coefficients satisfy
  `U1 = alpha T1`, `V1 = beta T1`, `N1 = P1 = Y1 = 0`, with `T1 != 0`, while
  the checked next layer closes uniquely to zero;
- thus the residual-fiber search space is cut from all of
  `A_adm^th,n(q) intersect ker(C_center,n(q))` to those directions whose
  extracted low-order local jet satisfies this explicit membrane-nullmode
  equation family;
- the exact remaining blocking condition is therefore a global checked-local
  coefficient-extraction theorem on the residual fiber deciding membership in
  `span(g_mem^aug,n(q))`.
## Explicit weighted-ansatz realization of the residual-fiber membrane-nullmode jet

- the current weighted trial ansatz does not kill the membrane-nullmode jet on
  the residual fiber;
- for any `s_mem != 0`, one has an explicit same-trace coefficient template with
  only
  `u_s,k=1,2`, `v,k=1,2`, and `T_s,k=1,2` nonzero,
  chosen as
  `u_s,k=1 = -L alpha s_mem`, `u_s,k=2 = -(L^2/x0) alpha s_mem`,
  `v,k=1 = -L beta s_mem`, `v,k=2 = -(L^2/x0) beta s_mem`,
  `T_s,k=1 = -L s_mem`, `T_s,k=2 = -(L^2/x0) s_mem`;
- equivalently,
  `u_s^z = alpha s_mem x^n (x - x^2/x0)`,
  `v^z   = beta  s_mem x^n (x - x^2/x0)`,
  `T_s^z =       s_mem x^(n-1) (x - x^2/x0)`,
  with all other channels zero;
- this template lies in `ker(C_center)` and has exact low-order jet
  `s_mem g_mem^aug,n(q)`;
- so the current weighted-ansatz repository boundary already realizes the local
  membrane-nullmode jet globally on the residual fiber;
- the remaining open issue is therefore no longer low-order realizability of the
  jet itself, but its full theorem-facing upgrade to an exact admissible
  representative-sensitive membrane lift in `A_adm^th,n(q)`.
## Exact failure point after the explicit weighted-ansatz membrane template

- after the explicit residual template is built, the clean branch is no longer
  blocked by low-order realizability of `g_mem^aug` on `ker(C_center)`;
- the template does not yet extend to a theorem-facing admissible lift on the
  current exact repository boundary, because the upgrade already breaks at the
  passage from the explicit weighted trial vector to `A_adm^th` / `Pair_chk`;
- this is sharper than the earlier residual-fiber wording: the remaining open
  issue is not whether the membrane-nullmode jet can occur, and not whether a
  nonzero membrane coordinate would be visible if a checked-local shadow were
  available;
- the exact unresolved step is the theorem-facing admissibility / checked-local
  shadow upgrade for that explicit template.