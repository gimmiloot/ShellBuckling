# Comparison Note

## Main Outcome
Pilot 19 does **not** show a substantial upward move of the current simple-support
ceiling from edge-aware right-edge representation alone.

The recorded old path from pilot 12 remains

```text
highest converged load = 4.3434 MPa,
first failure load     = 4.3440 MPa.
```

The best usable edge-aware run in pilot 19, `edge_power_tail`, gives the same
bounded outcome:

```text
highest converged load = 4.3434 MPa,
first failure load     = 4.3440 MPa.
```

So the observed ceiling shift in the bounded pilot-19 comparison is

```text
0.0000 MPa.
```

This is not a material improvement beyond the current `4.3440 MPa` failure
band.

## Edge-Aware Representations Tested
The pilot kept the same active 6-state equations and the same simple-support BC
set, and changed only the numerical representation near `x = 1`.

1. `edge_power_tail`

- single power-stretched tail mesh;
- stronger node clustering near `x = 1` than the current rescue-local profile;
- usable through the anchor ramp up to `4.3434 MPa`.

2. `edge_double_tail`

- two-zone tail mesh with a separate ultra-edge layer inside `x in [0.992, 1]`;
- did **not** produce a usable continuation path in this bounded run;
- the anchor ramp already failed at `4.3430 MPa` by mesh-node exhaustion.

## Diagnostic Reading
For the best usable edge-aware path `edge_power_tail`:

- highest converged load: `4.3434 MPa`;
- max BC residual there: about `3.46e-18`;
- node fraction with `x > 0.995`: about `0.926`;
- strongest gradients: `u_z`, then `varphi`, then `T_s`.

At the first failed load `4.3440 MPa`:

- failure message: `The maximum number of mesh nodes is exceeded.`;
- max BC residual stayed small, about `4.62e-17`;
- node count reached `486769 / 600000`;
- node fraction with `x > 0.995`: about `0.937`;
- strongest gradients remained `u_z`, then `varphi`, then `T_s`.

So the failure signature is still small-BC, right-edge-concentrated, and
numerical in character rather than a new clear fold-like signal.

## Conclusion
In this bounded pilot, the edge-aware discretization improves right-edge sampling
but does **not** move the ceiling substantially upward. The bottleneck still
looks mainly numerical after the change.
