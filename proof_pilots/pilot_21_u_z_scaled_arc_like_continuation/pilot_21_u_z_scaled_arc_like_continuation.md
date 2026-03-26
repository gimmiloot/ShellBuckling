# Pilot 21: `u_z`-Scaled Arc-Like Continuation

## Goal
This pilot takes the separate active 6-state simple-support background path one
conservative step beyond pilot 20.

The aim is not a new method sweep. It is to turn the pilot-20 lesson into one
main high-load workflow:

- keep the exact 6-state equations unchanged;
- keep the same simple-support BC set unchanged;
- use the exact pilot-20 `u_z`-scaled continuation path as the main numerical
  formulation;
- add bounded arc-like step adaptation only as an auxiliary continuation layer;
- check whether the bounded continuation ceiling can be moved above `4.3520 MPa`
  without reconnecting the mixed-weak scans.

## Scope
This pilot keeps fixed:

- `src/shell_buckling/mixed_weak/axisymmetric_simple_support_background.py` as
  the governing 6-state background path;
- the simple-support BC set `T_s(1)=0`, `M_s(1)=0`, `u_z(1)=0`,
  `T_sn(x0)=0`, `u_r(x0)=0`, `varphi(x0)=0`;
- the separation between this path and the active mixed-weak scans that still
  use the older reduced `F_min` background.

## Outcome Summary
The old-path reference pair remains unchanged at `4.3434 / 4.3440 MPa`.
Separately from that, pilot 20 still supplies the standalone bounded
`u_z`-scaled ceiling `4.3520 MPa`.

Pilot 21 then reproduced that exact `u_z`-scaled path and added only bounded
arc-like step adaptation above it. In the packaged ladder it reached
`4.3800 MPa` with reproducible stage retests at every planned target and no
bounded failure inside the ladder. The dominant gradient ordering stayed
`u_z`, then `varphi`, then `T_s`.

This is still a bounded numerical continuation result, not a final physical
critical load claim.

## Staged Ladder
| Stage target (MPa) | Accepted highest (MPa) | Reproducible | First failure load | Strongest gradients | Reading |
| --- | ---: | --- | --- | --- | --- |
| `4.3520` | `4.3520` | yes | not reached | `u_z, varphi, T_s` | no non-numerical signal seen in the bounded stage; still consistent with a numerical / conditioning barrier |
| `4.3550` | `4.3550` | yes | not reached | `u_z, varphi, T_s` | no non-numerical signal seen in the bounded stage; still consistent with a numerical / conditioning barrier |
| `4.3600` | `4.3600` | yes | not reached | `u_z, varphi, T_s` | no non-numerical signal seen in the bounded stage; still consistent with a numerical / conditioning barrier |
| `4.3700` | `4.3700` | yes | not reached | `u_z, varphi, T_s` | no non-numerical signal seen in the bounded stage; still consistent with a numerical / conditioning barrier |
| `4.3800` | `4.3800` | yes | not reached | `u_z, varphi, T_s` | no non-numerical signal seen in the bounded stage; still consistent with a numerical / conditioning barrier |

## Files
- runnable script: `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/u_z_scaled_arc_like_continuation.py`
- recorded results: `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/u_z_scaled_arc_like_results.json`
