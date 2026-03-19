# ShellBuckling

Research repository for shell / shallow-shell stability, prebuckling states, and
bifurcation criteria.

The current active working direction is the mixed-weak branch with independent
circumferential channels `(v, S)` and `(psi, H, chi)`. Supporting determinant
and dimensionless-comparison scripts are kept for comparison and diagnostics.
Candidate critical loads from the current mixed-weak scans should still be read
as exploratory unless they are confirmed in the theory and project-state
materials.

## Repository structure

- `src/shell_buckling/mixed_weak/`
  Active reusable mixed-weak core modules and boundary-matrix scan modules.
- `src/shell_buckling/supporting/`
  Reusable supporting comparison and diagnostic modules.
- `tasks/`
  Active runnable entry points.
- `experiments/supporting/`
  Supporting runnable entry points for comparison scripts.
- `experiments/legacy/`
  Placeholder location for archived experiments. The current checkout does not
  contain separate legacy source files.
- `docs/`
  Theory, assumptions, journal, literature notes, source PDFs, and the project
  map.
- `output/`
  Reserved for generated output files.

## How to run

Run every command below from the repository root.

If you want to use the repository's virtual environment explicitly, use:

```powershell
.\.venv\Scripts\python.exe <command>
```

The examples below use that form so they work without activating the venv.
If you already activated `.venv`, replace `.\.venv\Scripts\python.exe` with
`python`.

### Compact command list

- Main active broad scan:
  `.\.venv\Scripts\python.exe tasks/run_mixed_weak_boundary_matrix_scan.py`
- Main active targeted scan:
  `.\.venv\Scripts\python.exe tasks/run_mixed_weak_targeted_scan.py`
- Supporting determinant comparison:
  `.\.venv\Scripts\python.exe experiments/supporting/run_supporting_determinant_comparison.py`
- Supporting dimensionless comparison:
  `.\.venv\Scripts\python.exe experiments/supporting/run_supporting_dimensionless_comparison.py`

### Active task: broad mixed-weak boundary-matrix scan

What it does:
- Runs the main mixed-weak boundary-matrix workflow on the active
  simple-support branch.
- Can execute the baseline pressure scan plus resolution, fine, and adaptive
  follow-up scans.

Input assumptions:
- Uses the active mixed-weak simple-support core in
  `src/shell_buckling/mixed_weak/solver_simple_support_core.py`.
- Uses the configuration constants near the top of
  `src/shell_buckling/mixed_weak/boundary_matrix_scan.py`.

Exact command:

```powershell
.\.venv\Scripts\python.exe tasks/run_mixed_weak_boundary_matrix_scan.py
```

Where to change parameters:
- `src/shell_buckling/mixed_weak/boundary_matrix_scan.py`
- Main switches: `RUN_BASELINE_SCAN`, `RUN_RESOLUTION_STUDY`,
  `RUN_FINE_SCAN`, `RUN_ADAPTIVE_SCAN`
- Main scan grid: `BASELINE_P_MAX_MPA`, `BASELINE_P_NPTS`, `BASELINE_MODES`
- Follow-up windows: `RESOLUTION_WINDOWS`, `FINE_SCAN_WINDOWS`,
  `ADAPTIVE_SCAN_WINDOWS`

### Active task: targeted mixed-weak follow-up scan

What it does:
- Runs a narrow mixed-weak scan around the current leading candidate windows.
- Useful when you want localized follow-up instead of the full broad scan.

Input assumptions:
- Uses the patched mixed-weak core in
  `src/shell_buckling/mixed_weak/solver_patched_core.py`.
- Uses the targeted-window configuration near the top of
  `src/shell_buckling/mixed_weak/boundary_matrix_targeted_scan.py`.

Exact command:

```powershell
.\.venv\Scripts\python.exe tasks/run_mixed_weak_targeted_scan.py
```

Where to change parameters:
- `src/shell_buckling/mixed_weak/boundary_matrix_targeted_scan.py`
- Main grid seed: `BASELINE_P_MAX_MPA`, `BASELINE_P_NPTS`
- Targeted scan controls: `TARGETED_CASES`, `TARGETED_WINDOWS0`,
  `TARGETED_NPTS`, `TARGETED_MAX_ITERS`

### Supporting task: determinant comparison

What it does:
- Compares determinant-style scans between the shallow and non-shallow models.
- Produces supporting plots and diagnostic minima for wave numbers `n` over a
  prescribed pressure range.

Input assumptions:
- This is supporting comparison tooling, not the main mixed-weak criterion.
- Its run configuration is set inside
  `src/shell_buckling/supporting/determinant_criterion_comparison.py`.

Exact command:

```powershell
.\.venv\Scripts\python.exe experiments/supporting/run_supporting_determinant_comparison.py
```

Where to change parameters:
- `src/shell_buckling/supporting/determinant_criterion_comparison.py`
- In `main()`, edit `n_list` and `p_list`

### Supporting task: dimensionless background comparison

What it does:
- Compares dimensionless background fields and branch-A diagnostics between the
  non-shallow and shallow models.
- Useful for consistency checks and interpretation of the background state.

Input assumptions:
- This is a supporting diagnostic, not the main mixed-weak criterion.
- The wrapper currently passes a single target pressure to
  `compare_dimensionless(...)`.

Exact command:

```powershell
.\.venv\Scripts\python.exe experiments/supporting/run_supporting_dimensionless_comparison.py
```

Where to change parameters:
- `experiments/supporting/run_supporting_dimensionless_comparison.py`
- Change `q_target` in `main()`
- For plotting density or branch-A plotting switches, edit
  `src/shell_buckling/supporting/dimensionless_background_comparison.py`

## Output behavior

- The current scripts mainly print diagnostics to the terminal and show
  matplotlib figures.
- `output/` is reserved for saved artifacts if you decide to add explicit file
  export later.

## Key documents

- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/assumptions/assumptions.md`
- `docs/journal/project_journal_updated14.md`
- `docs/project_map.md`
- `docs/literature/SOURCE_INDEX.md`
