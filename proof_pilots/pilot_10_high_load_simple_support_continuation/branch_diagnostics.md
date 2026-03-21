# Branch Diagnostics

## Main Result
The same high-load 6-state simple-support branch does continue past the previous
pilot-09 ceiling near `4.343 MPa`, but only by a very small additional amount
under the present bounded rescue workflow.

The strongest bounded refinement reached

```text
q = 4.3433 MPa
```

and the first unresolved load above that remained

```text
q = 4.3434 MPa.
```

## Evidence
Two bounded pilot-10 runs were used.

1. Band run `4.34..4.50 MPa`

- bootstrap to the known local branch reached `4.3430 MPa`;
- the first failed attempted load was `4.3440 MPa`;
- all rescue-local seed variants failed there with
  `The maximum number of mesh nodes is exceeded`.

2. Focused refinement just above the ceiling

- `4.3431 MPa` converged;
- `4.3432 MPa` converged;
- `4.3433 MPa` converged;
- `4.3434 MPa` failed for `secant_prev_mesh`, `previous_raw_mesh`, and
  `previous_on_cluster`;
- the failed `4.3434 MPa` attempts kept very small BC residuals
  (`O(1e-17)..O(1e-16)`), while node counts pushed to about
  `4.14e5..6.00e5`.

## Direct Answers

### Does the same branch continue past the previous ceiling?
Yes, but only slightly in the present evidence: from about `4.3430 MPa` to
about `4.3433 MPa`.

### Is failure still mainly numerical?
Yes. The active pattern is still mesh-node exhaustion with tiny BC residuals,
and the difficult structure remains concentrated in the right-edge layer.

### Is there evidence of a turning point, fold, or branch termination?
Not at present. The branch can still be advanced by smaller steps above the old
ceiling, which is evidence against an immediate fold exactly at `4.3430 MPa`.
Current failure is better described as a numerical continuation barrier than as
evidence of proved branch nonexistence.

### Does `10 MPa` currently look reachable on the present branch?
Not yet justified. The evidence supports only a very local continuation past
`4.343 MPa`; it does not support extrapolating that success to `10 MPa`.

## Band Summary

### `4.34..4.50 MPa`

- highest converged load: `4.3433 MPa` with the focused rescue-local refinement;
- first failure load: `4.3440 MPa` in the bounded band run, and
  `4.3434 MPa` in the finer local refinement;
- progress still being made: `yes, but only locally`;
- bottleneck still mainly numerical: `yes`;
- evidence of branch turning or nonexistence: `no concrete evidence`.

### `4.50..5.00 MPa`

- not entered, because the present branch has not been continued to `4.50 MPa`;
- highest converged load remains `4.3433 MPa`;
- progress still being made: `not enough to reach this band`;
- bottleneck still mainly numerical: `yes, based on the unresolved 4.3434 MPa barrier`;
- evidence of branch turning or nonexistence: `still no concrete evidence`.

### `5.00..6.00 MPa`

- not entered, for the same reason;
- highest converged load remains `4.3433 MPa`;
- progress still being made: `not enough to reach this band`;
- bottleneck still mainly numerical: `yes`;
- evidence of branch turning or nonexistence: `still no concrete evidence`.
