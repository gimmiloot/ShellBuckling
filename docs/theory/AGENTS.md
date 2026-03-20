# AGENTS.md for docs/theory

## Directory purpose
This directory contains theory-facing documents, not ordinary implementation notes.

Current important files:
- `vyvod_uravneniy_updated17.md` — derivation notebook / theoretical investigations
- `current_theory_verification_map.md` — verification map for the current mixed-weak project theory
- `current_mixed_weak_theory_note.tex` — compact article-style discussion note for supervisor meetings

These files have different roles and must not be merged conceptually.

---

## File roles

### 1. `vyvod_uravneniy_updated17.md`
Use for:
- theoretical investigations,
- derivations,
- alternative formulations,
- development of new equation systems,
- intermediate theoretical work.

This file may be exploratory and research-notebook-like.

### 2. `current_theory_verification_map.md`
Use for:
- structured tracking of the current theory,
- accepted base,
- open claims,
- hypotheses,
- verification methods,
- verification status.

This file is a verification-management document.

### 3. `current_mixed_weak_theory_note.tex`
Use for:
- short article-style presentation of the current theory,
- supervisor-facing explanation of the present mixed-weak approach,
- a compact summary of the current system, BCs, criterion, and solution route.

This file is NOT:
- a full derivation notebook,
- a project journal,
- a changelog,
- an implementation memo.

---

## Policy for current_mixed_weak_theory_note.tex
This file should be readable by a person who has not followed the entire repository history.

Requirements:
- compact and discussion-oriented,
- mathematically careful,
- explicit about current status,
- consistent with repository notation,
- not excessively long.

Preferred section structure:
1. Introduction / motivation
2. Problem statement
3. Unknowns and mixed-weak structure
4. Current system of equations
5. Boundary conditions and conjugate pairs
6. Current criticality criterion
7. Solution procedure
8. Verified components and open points
9. Conclusion

Optional short appendix:
- notation table

When editing:
- preserve article-like readability,
- prefer concise explanation over exhaustive derivation,
- mark exploratory elements explicitly,
- do not claim more than the repository currently supports,
- do not turn open items into closed statements.

---

## Policy for hypotheses and claims in theory files
Whenever a hypothesis or claim appears in theory-facing text, make its status explicit.

Possible statuses include:
- accepted working base
- proven in pilot
- partially confirmed
- exploratory
- strategy only
- not yet checked

Do not blur:
- proved logic,
- symbolic consistency,
- numerical evidence,
- research strategy.

---

## Update rules
Update `current_mixed_weak_theory_note.tex` only when the current theory meaningfully changes.

Examples that DO justify updating it:
- changed active equation set,
- changed boundary conditions,
- changed current criterion,
- changed active solution procedure,
- changed status of verified/open core components.

Examples that do NOT justify updating it:
- file moves,
- code renaming,
- ordinary refactors,
- local plotting changes,
- small cleanup of scripts.