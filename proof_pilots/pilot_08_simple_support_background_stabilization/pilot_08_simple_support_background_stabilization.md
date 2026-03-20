# Pilot 08. Simple-Support Background Stabilization

## Goal
This pilot diagnoses and sharpens the current bottleneck of the separate
6-state axisymmetric simple-support background solver in the
`4.30..4.35 MPa` band.

The purpose is not to prove the whole shell theory and not to claim a
final physical simple-support critical load. The narrower goal is to
determine, as cleanly as the current repository allows, whether the
present ceiling comes mainly from:

- numerical failure of the current `solve_bvp` workflow,
- suspicion about the implemented 6-state equations,
- suspicion about the implemented simple-support BCs,
- or a mixed cause.

## Intended 6-State Simple-Support Problem
The active full-state simple-support background module uses the state

```text
[T_s, T_sn, M_s, u_r, u_z, varphi]
```

and is intended to solve the repository-level simple-support BC set

```text
center: T_sn(x0)=0, u_r(x0)=0, varphi(x0)=0,
edge:   T_s(1)=0, M_s(1)=0, u_z(1)=0.
```

This is distinct from both:

- the older 5-state `F_min` fallback still used by the active mixed-weak
  scans, and
- the moving-clamp / sliding-clamp comparison line, which keeps
  `varphi(1)=0` instead of `M_s(1)=0`.

## What This Pilot Checks
The pilot is split into two direct checks.

1. `problem_audit.md`
   records the exact implemented state, ODEs, and BCs, and checks whether
   the BC structure is square and aligned with the intended simple-support
   statement.

2. `bc_structure_check.py`
   verifies that the live BC function really imposes the intended six
   residuals on the intended variables, without a silent replacement or a
   weakened condition.

3. `numerical_diagnostic.py`
   uses the live 6-state solver path to test the `4.30..4.35 MPa` band by:

   - varying the initial seed,
   - varying mesh density, `max_nodes`, and tolerances,
   - inspecting BC residuals near failure,
   - localizing where the node blow-up occurs,
   - and checking whether the active 6-state equations match the
     supporting non-shallow 6-state equations they were extracted from.

## Numerical Failure vs Equation-Level vs BC-Level Suspicion
The pilot treats the following possibilities separately.

### A. Numerical failure only
This would mean:

- the equations match the intended active 6-state system,
- the BC set is implemented exactly and has the right count,
- BC residuals stay small,
- but `solve_bvp` still loses the branch by mesh-node blow-up or stiffness
  in the upper load band.

### B. Equation-level suspicion
This would mean there is some concrete sign that:

- the active 6-state equations no longer match the intended repository
  equations, or
- the current equations develop a structural stiffness/singularity pattern
  that is not plausibly explained by solver settings alone.

### C. Boundary-condition-level suspicion
This would mean there is some concrete sign that:

- the implemented BC residuals do not match the intended simple-support
  statement,
- or the BC count / variable placement is structurally inconsistent,
- or a condition was silently replaced by another one.

## What This Pilot Does Not Prove
This pilot does **not** prove:

- the final article-level axisymmetric simple-support background theorem,
- that the present `4.30..4.35 MPa` ceiling is a physical limit point,
- the final mixed-weak critical problem,
- or the final physical simple-support critical load.

It is a repository-level stabilization and diagnosis pilot only.
