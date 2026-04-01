# Pilot 18 Artifacts

This directory marks the preferred artifact boundary for
`pilot_18_revised_analytic_barrier_diagnosis`.

Source material for the pilot remains in the pilot root:

- note: `pilot_18_revised_analytic_barrier_diagnosis.md`
- supporting notes: `barrier_problem_statement.md`, `edge_layer_scaling.md`
- scripts: `analysis_common.py`, `jacobian_conditioning_check.py`,
  `term_balance_check.py`

Historical generated artifacts are still co-located in the pilot root for path
compatibility with the existing scripts and notes:

- `branch_state_cache.json`
- `branch_state_cache.npz`
- `jacobian_conditioning_results.json`
- `term_balance_results.json`

Future generated outputs for this pilot should prefer `artifacts/` when that
does not break existing references.
