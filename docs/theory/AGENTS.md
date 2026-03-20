# docs/theory/AGENTS.md

## Purpose of this folder
This folder holds the main theory-development and theory-status documents for
the current mixed-weak branch.

Work here must preserve mathematical meaning and must not silently merge:
- full derivation,
- verification status,
- supervisor-facing summary,
- project history,
- or solver-specific implementation details.

If theory documents and active code disagree, report the disagreement
explicitly. Do not silently "clean it up" by rewriting one side to match the
other.

---

## Priority inside `docs/theory`
When working only inside this folder, use the files in this order:

1. `vyvod_uravneniy_updated17.md`
   - main theoretical-development file;
   - source of the current derivations, operator structure, boundary logic,
     and discussion of what is and is not established.

2. `current_theory_verification_map.md`
   - verification boundary and status map for the current mixed-weak theory;
   - use it to separate accepted base, structural claims, formula claims,
     numerical claims, interpretation items, and strategy items.

3. `current_mixed_weak_theory_note.tex`
   - compact discussion note for supervisor-facing conversations;
   - should summarize the current theory state without replacing the full
     derivation or the verification map.

If there is a conflict:
- keep `vyvod_uravneniy_updated17.md` as the derivation source,
- use `current_theory_verification_map.md` to describe claim status,
- and make the note report the conflict rather than hiding it.

---

## File roles

### `vyvod_uravneniy_updated17.md`
Use this file for:
- derivations,
- equation development,
- reformulation of the mixed-weak system,
- boundary-pair logic,
- current theoretical reductions,
- discussion of what has and has not been proved at the derivation level.

Do not use it for:
- routine repository notes,
- changelog entries,
- broad project-stage narration,
- or short supervisor summaries.

### `current_theory_verification_map.md`
Use this file for:
- verification scope,
- claim classification,
- current status labels,
- proof-pilot integration,
- verification boundaries,
- and next verification targets.

Keep the claim categories distinct:
- accepted working base,
- structural,
- formula,
- numerical,
- interpretation,
- strategy.

Do not turn this file into a second derivation document or a general narrative
history.

### `current_mixed_weak_theory_note.tex`
Use this file for a compact, readable note aimed at a mathematically informed
reader who has not followed the entire repository history.

It should usually contain:
- motivation and scope,
- current problem statement,
- active unknowns and resultants,
- current system actually under discussion,
- boundary conditions and conjugate pairs,
- the current working criterion,
- the current numerical/theoretical solution procedure,
- verified components,
- open points and limitations.

It should not try to contain:
- the whole derivation,
- the whole repository history,
- every rejected branch,
- or every implementation detail from every script.

---

## When to update `current_mixed_weak_theory_note.tex`
Update the note when one of these changes materially in the repository:
- the active unknown/resultant set;
- the current boundary-pair statement;
- the current working criterion;
- the current interpretation of what is established vs exploratory;
- the main open bottleneck for the branch;
- the current leading candidate load range that is being discussed publicly.

Do not update the note merely because:
- code was refactored without changing the discussion object;
- a small implementation detail changed;
- or a routine changelog item was added.

---

## Style for `current_mixed_weak_theory_note.tex`
Keep the note:
- compact,
- readable,
- explicit about status,
- and close to repository notation.

Prefer:
- `\varphi` in the theory note, while mentioning once that some code files use
  `phi` for the same variable;
- short equations and short explanatory paragraphs;
- clear labels such as "established", "working", "exploratory", and "open";
- explicit statements when a numerical result is not yet a final validated
  `simple support` conclusion.

Avoid:
- overclaiming validation,
- mixing strategy statements with theorem-like statements,
- or silently replacing repository notation with cleaner alternatives.

---

## Current repository-specific nuance
At present, the theory-facing documents
`vyvod_uravneniy_updated17.md`,
`current_theory_verification_map.md`,
and the project journal summarize the right-boundary discussion object using

- `u_n(1)`,
- `\varphi(1)`,
- `T_s(1)`,
- `S(1)`,
- `H(1)`.

The active code still contains two nearby numerical lines:
- the broad simple-support prototype in
  `src/shell_buckling/mixed_weak/solver_simple_support_core.py` /
  `boundary_matrix_scan.py`, where the boundary row currently uses `M_s(1)`;
- the patched targeted line in
  `src/shell_buckling/mixed_weak/solver_patched_core.py` /
  `boundary_matrix_targeted_scan.py`, where the boundary row uses
  `\varphi(1)`.

When updating the theory note, do not silently choose one and pretend the other
does not exist. State the split explicitly and label it as an open
theory-to-implementation alignment issue.
