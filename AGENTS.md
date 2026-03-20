# AGENTS.md

## Project identity
This repository contains a research codebase on shell / shallow shell stability, prebuckling states, and bifurcation criteria.

This is a research repository, not a clean production codebase.
It contains:
- active research code,
- task-specific scripts,
- comparison scripts,
- legacy / experimental branches,
- theory notes,
- project state documents.

Your job is to help organize and improve the repository without silently changing the scientific meaning.

---

## Main rule
Preserve the mathematical meaning of the project.

Unless explicitly instructed otherwise:
- do not change equations,
- do not change notation,
- do not change the meaning of variables,
- do not replace one model by another,
- do not alter numerical algorithms in ways that change scientific interpretation.

Prefer:
- structural cleanup,
- clearer repository organization,
- reproducibility,
- minimal intrusive edits,
- explicit reporting of all changes.

---

## Current scientific status
Treat the mixed weak criterion branch as the current active working path.

More specifically:
- mixed weak files are the current active theory / prototype implementation;
- scripts for dimensionless comparison are supporting diagnostics;
- scripts based on the original Huang / Cheo determinant criterion are supporting legacy comparison tools;
- old or dead-end research branches must be preserved, not deleted.

Important:
- candidate critical loads obtained in current mixed-weak experiments are exploratory unless explicitly confirmed in the theory files or project journal;
- do not present exploratory values as final validated conclusions.

---

## Repository priorities
When in doubt, prioritize sources in this order:

1. `vyvod_uravneniy_updated17.md`
   - main file for theoretical development;
   - contains theoretical investigations, new systems of equations, derivations, and related mathematical development.

2. `assumptions.md`
   - register of the main hypotheses currently used in the project;
   - use it to understand which assumptions are active.

3. `project_journal_updated14.md`
   - global project state;
   - contains current questions, considered theories, accepted/rejected directions, and major stage-level conclusions.

4. active mixed-weak solver / prototype files.

If there is a conflict:
- report it explicitly,
- do not silently resolve it by editing code.

---

## File roles and classification rules
When analyzing or refactoring the repository, classify files into these groups:

### 1. Active core
Reusable code implementing the current main research path:
- axisymmetric background,
- interpolation of background fields,
- trial spaces,
- mixed weak operator assembly,
- channel reconstruction,
- scans used by the active mixed-weak workflow.

### 2. Runnable task scripts
Entry points that run specific tasks:
- scans,
- figure generation,
- determinant studies,
- diagnostics,
- comparisons.

These should usually live in `tasks/`.

### 3. Supporting / legacy comparison scripts
Scripts still useful for comparison but not the main path:
- dimensionless comparison scripts,
- Huang/Cheo determinant scan scripts,
- branch-A comparison scripts.

These should usually be marked as `supporting` or `legacy`, not as default core workflow.

### 4. Archived / experimental code
Older or dead-end directions that must be preserved for history and comparison.
Do not delete them unless explicitly instructed.

### 5. Documentation
Important project memory:
- changelog,
- project journal,
- theory file,
- assumptions,
- source notes,
- project map.

Documentation is part of the project, not clutter.

---

## Documentation policy
Documentation must be updated carefully and by role.

### 1. `CHANGELOG.md`
Use this file for ordinary project changes:
- file moves,
- renamings,
- structural refactoring,
- code cleanup,
- new scripts,
- updated plotting behavior,
- test-related changes,
- small implementation changes that do not change the global scientific status.

### 2. `project_journal_updated14.md`
Use this file only for global project-level updates, such as:
- current open questions,
- theories under consideration,
- accepted or rejected directions,
- major conclusions,
- changes of project stage,
- important research milestones.

Do not use this file for routine refactoring notes or small code edits.

### 3. `vyvod_uravneniy_updated17.md`
Use this file for theoretical development only:
- new systems of equations,
- derivations,
- modifications of theoretical formulations,
- mathematical reductions,
- reformulations of the governing system,
- new criterion derivations.

Do not use this file for ordinary code notes or refactoring logs.

### 4. `assumptions.md`
Use this file to record the main active hypotheses and assumptions:
- modeling assumptions,
- regularity assumptions,
- simplifications,
- working hypotheses,
- provisional scientific assumptions currently being used.

When assumptions change, add or update them explicitly rather than silently changing code.

---

## Changelog requirement
Maintain `CHANGELOG.md`.

Whenever a nontrivial repository change is made, update `CHANGELOG.md` with:
- date,
- short title,
- affected files,
- brief description of what changed.

Examples of entries:
- repository restructuring,
- file renaming,
- new task script added,
- shared module extracted,
- plotting workflow changed,
- testbench separated from core solver.

If the change is only a tiny local correction, changelog update is optional.
If the change affects repository organization or workflow, changelog update is required.

---

## Refactoring policy
When refactoring:
- prefer moving and renaming files over rewriting them;
- prefer extracting duplicated utilities into shared modules;
- keep behavior unchanged unless explicitly told to modify it;
- preserve comments that contain scientific context;
- preserve old paths in archived form when necessary.

Good refactor:
- split reusable logic into `src/...`
- keep runnable scripts in `tasks/...`
- move old branches into `experiments/legacy/` or `experiments/archived/`
- centralize documentation in `docs/...`

Bad refactor:
- merging all code into one giant file,
- deleting “obsolete” files without asking,
- renaming variables that carry mathematical meaning,
- rewriting formulas for style only.

---

## Naming policy
Use names that reflect scientific role.

Prefer:
- `run_*.py` for task entry points,
- `*_core.py` for reusable solver logic,
- `*_background.py`, `*_operator.py`, `*_trial_space.py` for reusable modules,
- clear names for comparison and legacy tasks.

Avoid vague names like:
- `main.py`,
- `main2.py`,
- `patched.py`,
- `new_final.py`,
unless explicitly required by the user.

If such files already exist, propose better names before changing behavior.

---

## Scientific notation policy
Notation is important in this repository.

Unless explicitly instructed:
- do not rename core variables,
- do not replace notation by “cleaner” alternatives,
- do not normalize naming style if it obscures correspondence with theory,
- do not rewrite formulas just for elegance.

When a code variable corresponds to a quantity from theory, preserve or document that correspondence.

---

## Required transparency in responses
When you make changes, always report:

1. which files were changed,
2. which files were moved or renamed,
3. whether behavior was intended to stay the same,
4. whether any mathematical or numerical assumption was changed,
5. what commands or scripts were run to test the result,
6. whether `CHANGELOG.md` was updated,
7. whether the change also required updates to:
   - `project_journal_updated14.md`,
   - `vyvod_uravneniy_updated17.md`,
   - `assumptions.md`.

If uncertain, say so explicitly.
Do not claim validation that was not actually performed.

---

## Preferred workflow
For nontrivial tasks, follow this order:

1. inspect the repository,
2. identify relevant files,
3. classify them by role,
4. propose a plan,
5. perform the smallest safe set of edits,
6. run a minimal relevant test,
7. update `CHANGELOG.md` if appropriate,
8. summarize exactly what changed.

For broad cleanup tasks:
- first do structure,
- then shared utilities,
- only then deeper code changes.

---

## Definition of done
A task is not complete unless:
- the repository structure is clearer than before,
- the scientific meaning is preserved,
- active vs supporting vs archived paths are clearly separated,
- changes are explicitly summarized,
- `CHANGELOG.md` is updated when required.

---

## Repository-specific guidance
Treat the repository approximately as follows unless later files show otherwise:

- mixed-weak solver/prototype files -> `active`
- boundary-matrix test scripts -> `active tasks`
- dimensionless comparison scripts -> `supporting`
- Huang/Cheo determinant scripts -> `supporting legacy`
- rejected or dead-end criterion branches -> `archived/experimental`
- `project_journal_updated14.md` -> global research state
- `vyvod_uravneniy_updated17.md` -> theoretical development
- `assumptions.md` -> active hypotheses register
- `CHANGELOG.md` -> ordinary change history

---

## Do not do these things
Do not:
- silently change the current scientific hypothesis,
- silently replace the active path by a legacy one,
- delete legacy scripts because they look redundant,
- remove exploratory code that may be historically important,
- treat numerical coincidence as proof,
- present exploratory critical loads as final validated results,
- write routine refactoring notes into `project_journal_updated14.md`,
- write code-structure notes into `vyvod_uravneniy_updated17.md`.

---

## Minimal output style
Be concrete, structured, and concise.
Prefer explicit file names over vague descriptions.
Prefer small safe edits over ambitious rewrites.

## Theory note for discussion
Maintain a compact article-style theory file for supervisor discussions:

- file: `docs/theory/current_mixed_weak_theory_note.tex`
- purpose: present the current mixed-weak theory in a short, readable, discussion-oriented form
- target reader: a mathematically informed reader who has not read the whole repository
- target length: compact; do not let it turn into a derivation notebook

Preferred contents:
- problem statement
- active unknowns and mixed-weak structure
- current system of equations
- boundary conditions and conjugate pairs
- current criticality criterion
- current solution procedure
- verified components
- open points / unresolved parts

Do not turn this file into:
- a project journal,
- a changelog,
- a full derivation archive,
- a dump of experiments,
- a code-oriented note.

Update `docs/theory/current_mixed_weak_theory_note.tex` only when one of the following changes materially:
- the current mixed-weak equation set,
- the active boundary conditions,
- the current criterion,
- the current solution procedure,
- the list of verified vs open components,
- the status of a central verification-map claim changes because of a completed proof pilot,
- a repository-level closed statement becomes available for an important open block such as `G_ps`.

Routine refactors, file moves, code cleanup, or small numerical tweaks should not trigger an update to this file.

When editing this file:
- preserve readability for an external reader,
- keep notation aligned with the active theory files,
- explicitly distinguish established parts from exploratory parts,
- do not present surrogate/testbench evidence as final physical validation.

## Hypotheses policy
Treat hypotheses explicitly and classify them.

Allowed categories:
- accepted working base
- structural/formal claim
- formula-level claim
- numerical claim
- interpretation claim
- strategy-level hypothesis

Do not silently upgrade a hypothesis into a theorem.

When a hypothesis is discussed, checked, or referenced:
- identify its category,
- identify what would count as verification,
- identify the verification method:
  - manual derivation
  - CAS
  - Lean
  - numerical testbench
  - literature alignment

Use the current verification map in:
- `docs/theory/current_theory_verification_map.md`

If a hypothesis is only a research strategy, label it as strategy, not as proved mathematics.
If a hypothesis is only supported within the current mixed-weak version or only at surrogate/testbench level, say so explicitly.
