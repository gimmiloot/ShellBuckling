# Output

`output/` stores generated runtime results, curated milestone exports, and
validation trees.

Current repository-side interpretation:

- `clean_full_simple_support/` is the active curated output area for clean full
  simple-support criterion work.
- top-level `full_simple_support_clean_search_*.json` files are legacy curated
  exports kept for direct comparison and reproducibility.
- `pilot21_*_validation_20260326/` directories are validation/runtime trees,
  not source material.

Cleanup policy for this phase:

- no historical output paths were moved, because existing scripts and notes may
  still point to them;
- new non-curated runtime data should be treated as cache/checkpoint material,
  not as hand-maintained source artifacts;
- future cleanup can safely migrate new outputs toward clearer subroles such as
  milestones, checkpoints, cache, and temporary runs once path references are
  audited end-to-end.
