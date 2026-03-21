# BC Equivalence Audit

## Purpose
This note extracts the live BCs from the current comparison code paths and
checks whether the shallow comparison path is physically equivalent to the
current 6-state simple-support background problem.

## 1. Exact Shallow BCs Currently Used

The shallow comparison path used in pilots 11 and 13 comes from

- `src/shell_buckling/supporting/determinant_criterion_comparison.py`

with the same shallow BC vector also present in

- `src/shell_buckling/supporting/dimensionless_background_comparison.py`.

The live shallow state is

```text
Y_sh = (theta0', theta0, Phi0', Phi0),
```

and the code imposes

```text
bc_sh(ya, yb) = [ya[1], yb[1], ya[3], yb[3]]
              = [theta0(x0), theta0(1), Phi0(x0), Phi0(1)].
```

So the exact shallow BC set is

```text
theta0(x0)=0,
theta0(1)=0,
Phi0(x0)=0,
Phi0(1)=0.
```

## 2. Exact Supporting Non-Shallow Comparison BCs

The supporting non-shallow comparison path in the same supporting modules uses
state

```text
Y_np = (T_s, T_sn, M_s, u_r, u_z, varphi),
```

with BC vector

```text
bcNP(ya, yb) = [yb[0], ya[1], ya[3], yb[4], ya[5], yb[5]]
             = [T_s(1), T_sn(x0), u_r(x0), u_z(1), varphi(x0), varphi(1)].
```

So the exact supporting non-shallow BC set is

```text
center: T_sn(x0)=0, u_r(x0)=0, varphi(x0)=0,
edge:   T_s(1)=0, u_z(1)=0, varphi(1)=0.
```

This is the same moving-clamp / sliding-clamp-side path already documented in
the theory audit notes.

## 3. Exact 6-State Simple-Support BCs

The current active 6-state simple-support background path lives in

- `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py`

with state

```text
Y_ss = (T_s, T_sn, M_s, u_r, u_z, varphi),
```

and BC vector

```text
axisymmetric_simple_support_bc(ya, yb)
  = [yb[0], yb[2], yb[4], ya[1], ya[3], ya[5]]
  = [T_s(1), M_s(1), u_z(1), T_sn(x0), u_r(x0), varphi(x0)].
```

So the exact 6-state simple-support BC set is

```text
center: T_sn(x0)=0, u_r(x0)=0, varphi(x0)=0,
edge:   T_s(1)=0, M_s(1)=0, u_z(1)=0.
```

## 4. Mapping the Shallow BCs Into Non-Shallow Variables

The live repository mapping used in the comparison pilots is

```text
theta0   = -beta sin(varphi),
Phi0     = gamma x T_s.
```

Therefore the shallow BCs map structurally to

```text
theta0(x0)=0  ->  -beta sin(varphi(x0)) = 0,
theta0(1)=0   ->  -beta sin(varphi(1))  = 0,
Phi0(x0)=0    ->  gamma x0 T_s(x0)      = 0,
Phi0(1)=0     ->  gamma T_s(1)          = 0.
```

On the small-rotation branch actually being continued in the repository, this
means:

- `theta0(x0)=0` matches `varphi(x0)=0`;
- `theta0(1)=0` matches `varphi(1)=0`;
- `Phi0(1)=0` matches `T_s(1)=0`;
- `Phi0(x0)=0` is a reduced-variable center regularity condition on `x T_s`,
  not the full 6-state pair `T_sn(x0)=0`, `u_r(x0)=0`.

So the shallow BC set does **not** encode the 6-state simple-support edge
condition `M_s(1)=0`. Instead it encodes the rotation-free edge condition
`varphi(1)=0`.

## 5. Physical Interpretation of Each BC Set

### Shallow path

The shallow comparison path is a reduced 4-state problem with:

- center regularity written as `theta0(x0)=0`, `Phi0(x0)=0`;
- edge conditions structurally corresponding to `varphi(1)=0` and `T_s(1)=0`.

That is not a shallow simple-support edge.
It is a reduced shallow problem whose edge type is clamp-like / sliding-clamp-
like rather than moment-free hinged.

### Supporting non-shallow comparison path

This path uses:

- center regularity/axisymmetry constraints `T_sn(x0)=0`, `u_r(x0)=0`,
  `varphi(x0)=0`;
- edge constraints `T_s(1)=0`, `u_z(1)=0`, `varphi(1)=0`.

This is the moving-clamp / sliding-clamp-side comparison path documented in
the repository.

### 6-state simple-support path

This path uses:

- the same center regularity/axisymmetry constraints
  `T_sn(x0)=0`, `u_r(x0)=0`, `varphi(x0)=0`;
- a different edge set
  `T_s(1)=0`, `M_s(1)=0`, `u_z(1)=0`.

This is the current full simple-support target.

## 6. Audit Conclusion

### Is the current shallow comparison path physically equivalent to the 6-state simple-support path?

No.

The decisive mismatch is at the outer edge:

- shallow path imposes `theta0(1)=0`, which maps to `varphi(1)=0`;
- 6-state simple-support imposes `M_s(1)=0` instead.

Those are different physical edge conditions.

### Is the current shallow path equivalent to moving clamp / sliding clamp?

It is not a full one-to-one 6-state BC vector, because the 4-state shallow
reduction does not explicitly carry `u_z`, `u_r`, or `T_sn`.

But structurally, its edge conditions align with the supporting moving-clamp /
sliding-clamp path, not with the simple-support path:

- both use `T_s(1)=0`;
- both use the rotation-free edge condition `varphi(1)=0` after mapping.

### Best classification

The present shallow comparison path is best read as:

```text
a reduced shallow moving-clamp / sliding-clamp-type comparison problem
with center regularity in the reduced variables,
not as a shallow simple-support comparator.
```

So pilots 11 and 13 should be interpreted with that limitation made explicit:
they compared the 6-state non-shallow simple-support branch against an older
shallow path that is **not** BC-equivalent to the simple-support problem.
