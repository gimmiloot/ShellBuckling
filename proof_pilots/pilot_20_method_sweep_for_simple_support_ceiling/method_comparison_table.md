# Method Comparison Table

| Method name | Key idea | Old ceiling (MPa) | New ceiling (MPa) | First failure load | Main failure mode | Recommendation |
| --- | --- | ---: | ---: | --- | --- | --- |
| `baseline_old_path` | Current rescue-local secant continuation on one domain | 4.3434 | 4.3434 | 4.3440 | Max nodes exceeded with strong right-edge concentration | Reference only |
| `quadratic_predictor_bundle` | Three-point quadratic predictor on the same single-domain mesh | 4.3434 | 4.3443 | Not reached in bounded run (`<= 4.3443`) | No bounded failure encountered; gain is small | Not worth pursuing alone |
| `arc_like_state_norm_control` | Pseudo-arclength-like tangent step with bounded factor adaptation | 4.3434 | 4.345163122 | Not reached in bounded run (`<= 4.345163122`) | No bounded failure encountered; still same dominant gradients | Lower priority than state scaling |
| `u_z_scaled_state` | Solver-state rescaling with extra weight on `u_z` and unchanged physical equations/BCs | 4.3434 | 4.3520 | Not reached in bounded run (`<= 4.3520`) | No bounded failure encountered in the bounded ladder | Continue |
| `bulk_edge_domain_split` | Multiple-shooting-like bulk/right-edge split with matching at `x=0.97` | 4.3434 | Anchor not reproduced | 4.3434 | Max nodes exceeded already at the anchor retest | Not worth pursuing in the current packaged prototype |

## Notes
- The old-path persistent failure remains `4.3440 MPa`.
- The strongest-gradient ordering stayed the same in the successful methods: `u_z`, then `varphi`, then `T_s`.
- Relative to the old-path failure (`x > 0.995` node fraction about `0.982`), the successful alternative methods used much less right-edge node concentration at their highest accepted loads (about `0.201` in the packaged sweep).
- The best bounded method in this pilot is `u_z_scaled_state`.
