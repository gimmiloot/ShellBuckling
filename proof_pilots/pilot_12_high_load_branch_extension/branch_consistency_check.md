# Branch Consistency Check

## Main Outcome
Pilot 12 does **not** yet show a reproducible branch extension beyond
`4.3434 MPa`.

What it does show is narrower and still useful:

- `4.3434 MPa` is reproducible on the current high-load strategy;
- the repeated same-load retests converged to the same solution with the same
  accepted seed `secant_profile_mesh`;
- there is no branch-jump signal in that repeated `4.3434 MPa` check;
- but the next staged ladder load `4.3440 MPa` still failed for every seed that
  was tried.

So the new status is **not** "isolated lucky convergence," but also not yet
"reproducible upward branch extension."

## Same-Branch Evidence At 4.3434 MPa
The strongest same-branch evidence is the repeated same-load retest:

- retest A at `4.3434 MPa`: success;
- retest B at `4.3434 MPa`: success;
- accepted seed in both runs: `secant_profile_mesh`;
- same-load solution difference: numerically zero on the comparison grid in the
  saved pilot-12 check;
- no branch-jump suspicion was triggered.

This means the `4.3434 MPa` point is now reproducible under the current staged
profile-mesh secant strategy.

## Upward Extension Above 4.3434 MPa
The first new ladder step above the reproducible point was

```text
4.3440 MPa.
```

That step failed for all tried seeds:

- `secant_profile_mesh`
- `previous_profile_mesh`
- `secant_prev_mesh`
- `previous_raw_mesh`
- `anchor_profile_mesh`

All of those failures had the same pattern:

- message: `The maximum number of mesh nodes is exceeded`;
- BC residuals remained tiny, about `1e-18 .. 1e-16`;
- node concentration remained heavily piled up near `x = 1`;
- strongest gradients were still dominated by `u_z` near the right edge.

So the branch ceiling has **not** yet moved past `4.3440 MPa`, and certainly
not beyond `4.35 MPa`, in this bounded pilot-12 run.

## Classification
The best evidence-based classification is:

- reproducible extension: `not yet`;
- isolated lucky convergence: `no`;
- unresolved ambiguity: `yes, but now narrowed to the next step above a
  reproducible 4.3434 MPa anchor`.

In other words, the branch point at `4.3434 MPa` is now reproducible, but the
upward continuation branch above that point is still unresolved.

## Bottleneck Interpretation
The bottleneck still looks mainly numerical.

Reasons:

- the equations and BC set were not changed;
- repeated `4.3434 MPa` success is possible on the same strategy;
- `4.3440 MPa` fails for all seeds by mesh-node exhaustion rather than by a
  branch-jump signal;
- right-edge concentration remains dominant;
- no turning-point evidence was produced by this pilot.

So pilot 12 strengthens the interpretation that the current obstruction is a
numerically difficult continuation zone, not a proved branch end.
