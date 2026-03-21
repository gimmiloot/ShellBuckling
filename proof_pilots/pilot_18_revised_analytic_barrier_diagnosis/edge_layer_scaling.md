# Edge-Layer Scaling Note

## Scope

This note gives a compact leading-order discussion of the right-edge layer near
`x=1` for the active 6-state simple-support background path.

It is intentionally heuristic.
It uses the actual live equations and the actual pilot-18 term-balance data,
but it does **not** claim a closed asymptotic theorem.

## 1. Why a stretched edge coordinate is reasonable

Near the outer edge, introduce

```text
xi = (1 - x) / delta,
```

so that

```text
d/dx = -(1/delta) d/dxi.
```

The failed `4.3440 MPa` attempts show extreme node pile-up near `x=1`, while the
largest gradient is in `u_z` and the next strongest shoulder is in `varphi`.
That is exactly the situation where an edge scale `delta` is a natural analytic
question.

## 2. The live near-edge equations

For `x~1`, the denominators `1/x` and `1/r` stay `O(1)` because the branch
keeps `r>0` and `x` is close to `1`. So the edge difficulty is not an actual
singularity of the form `1/(1-x)`.

The leading coupled subsystem is instead

```text
-(1/delta) Tsn_xi   = -(T_sn / r) + (sin(varphi) T_theta) / r + kappa_s T_s - qbar,
-(1/delta) Ms_xi    = -(M_s / r) + (cos(varphi) M_theta) / r + T_sn,
-(1/delta) varphi_xi= 12 (1-nu^2) mu^2 M_s - nu sin(varphi) / r,
-(1/delta) uz_xi    = -mu (1 + es) sin(varphi).
```

This already suggests that the edge correction is controlled by the coupled
chain

```text
T_theta -> T_sn -> M_s -> varphi -> u_z.
```

## 3. Which variables actually control the layer

The pilot-18 data point to the following hierarchy.

### A. `u_z`

The sharpest visible edge concentration is in `u_z`.
At `4.3434 MPa`, the dominant `u_z` term is the linear-looking piece

```text
u_z' approx -mu (1 + es) varphi,
```

with the explicit trig gap

```text
-mu (1 + es) (sin(varphi) - varphi)
```

still only about `0.176` of that dominant ultra-edge `L2` size.
So `u_z` is strongly amplified by the large factor `mu`, but not mainly by a
new trig blow-up.

### B. `varphi`

The `varphi` equation is controlled primarily by the bending term

```text
12 (1-nu^2) mu^2 M_s,
```

with the hoop correction

```text
-nu sin(varphi) / r
```

remaining non-negligible but smaller. At `4.3434 MPa`, the ultra-edge ratio is

```text
|phi_hoop| / |phi_bending| approx 0.25.
```

So the branch is genuinely non-shallow, but the hoop correction does not take
over the `varphi` balance near the ceiling.

### C. `T_sn` and `M_s`

The right-edge term balance shows

- `T_sn'` is dominated by `(sin(varphi) T_theta) / r`,
- `M_s'` is dominated by `T_sn`.

At the highest converged load, the dominant edge labels stay

```text
Tsnprime_hoop_trig,
Msprime_shear.
```

That means the edge correction is not set mainly by the small radius terms
`-T_sn/r` or `-M_s/r`; it is driven by the geometric hoop-induced forcing in
`T_theta`, which then feeds the `T_sn -> M_s` chain.

## 4. The key geometric balance

The most decisive pilot-18 ratio is

```text
|Ttheta_geometric| / |Ttheta_membrane| approx 1.12e3
```

in the ultra-edge region at `4.3434 MPa`.

So near the edge,

```text
T_theta = nu T_s + u_r/x
```

is overwhelmingly controlled by the geometric hoop term `u_r/x`, not by the
membrane piece `nu T_s`.

That immediately propagates into

```text
T_sn' ~ (sin(varphi) T_theta)/r,
```

which then drives `M_s'`, then `varphi'`, then `u_z'`.

This is why the present barrier is best read as a coupled right-edge geometric
balance on an already non-shallow branch.

## 5. Peak locations and layer geometry

The pilot-18 peak locations are also informative.
At `4.3434 MPa`:

- `T_theta` geometric peak: `x=1`;
- dominant `T_sn'` hoop-trig peak: `x=1`;
- dominant `M_s'` shear peak: `x=1`;
- dominant `u_z` terms peak near `x~0.999`;
- `varphi` bending term peaks earlier, around `x~0.951`;
- `varphi` hoop correction peaks near `x~0.994`.

So the numerically difficult region is not a single ultra-thin one-variable
layer. It looks more like:

- a broader near-edge shoulder for `varphi` and the `T_sn/M_s` chain,
- feeding into the sharpest final `u_z` adjustment very near `x=1`.

That matches the observed failed-step gradients:

- strongest `u_z` gradient near `x~0.99967`,
- next `varphi` gradient near `x~0.93466`.

## 6. Why this does not look like a fold-first explanation

The same pilot shows that the dominant ratios remain smooth from
`4.3400` to `4.3434 MPa`:

- `Ttheta_geometric / Ttheta_membrane` stays around `1.12e3`,
- `phi_hoop / phi_bending` stays around `0.25`,
- `uz_trig_gap / uz_linear` stays around `0.174..0.176`.

Even the nonconverged `4.3440 MPa` secant-profile attempt shows very similar
ultra-edge ratios, although that failed state should be treated only as
supportive context.

So there is no obvious abrupt term swap or explosive new non-shallow correction
turning on exactly at the first persistent failure.

## 7. Interpretation

### What is actually derived here

From the live equations, one can derive that near the edge the coupled
subsystem necessarily involves `T_theta`, `T_sn`, `M_s`, `varphi`, and `u_z`,
and that the right-edge BCs force a terminal correction in those fields.

### What is heuristic

The actual size of `delta`, the exact asymptotic scaling exponents, and the
final reduced edge-layer system are not yet derived rigorously.

### Best current reading

The present barrier is most consistent with:

```text
stiff right-edge geometric balance on an already non-shallow branch,
with moderate but smooth trig corrections,
not with a newly triggered high-load-only term flip.
```
