# Proof Pilots

`proof_pilots/` stores theorem-facing and diagnostic pilot work as preserved
research source material.

Current layering rules:

- Keep the main pilot note or README in the pilot root as the source-of-reasoning
  entry point.
- Keep runnable scripts close to the pilot they belong to until a later safe
  extraction moves shared logic into `src/`.
- Treat generated JSON/NPZ/PNG/checkpoint artifacts as artifacts, not as
  theorem source, even when older pilots still keep them beside the note/script
  files for compatibility.
- For new cleanup-safe work, prefer an explicit `artifacts/` boundary inside the
  pilot instead of adding more generated files directly to the pilot root.

Current artifact-boundary pilots:

- `pilot_18_revised_analytic_barrier_diagnosis/`
- `pilot_21_u_z_scaled_arc_like_continuation/`

Those pilots keep historical generated files at the root because existing
scripts and notes already refer to those paths. New artifact directories were
added only as forward-looking boundaries and indexes; no historical paths were
moved in this pass.
