# Minimum Next Implementation Step for the Simple-Support Background

The smallest justified engineering step is not to modify the mixed-weak
criterion first.
It is to create a **separate active axisymmetric simple-support background
module** with the full-state variable set

```text
[T_s, T_sn, M_s, u_r, u_z, varphi].
```

That module should expose, at minimum:

1. the current non-shallow axisymmetric ODE already used in supporting form;
2. a dedicated simple-support BC function
   `T_sn(x0)=0, u_r(x0)=0, varphi(x0)=0, T_s(1)=0, M_s(1)=0, u_z(1)=0`;
3. a fixed-load solve entry point;
4. a short continuation wrapper added only after the fixed-load solves are
   stable.

Why this is the minimum step:

- the active 5-state `F_min` background cannot encode `u_z(1)=0`;
- the full-state equations already exist in supporting form, so the next step
  is extraction and stabilization, not invention of a new model;
- the mixed-weak scans should keep using the hybrid fallback until this
  separate background path is stable enough to replace it honestly.