# Regression 04 callout dry run

Date: 2026-07-30

Source tested: `regression_04_categorical.qmd`

Status: **exploratory; not approved for promotion**

The pilot used a scratch copy of the chapter and a standalone HTML render. The
live chapter was never edited.

## Changes tested

1. The existing native “Definition: Reference category” note became a
   numbered `Definition` with the identifier `defn-reference-category`.
2. The two substitutions `male = 0` and `male = 1` moved into a collapsed
   `.formula-details` block titled “Details and formulas.”
3. The adjusted categorical-coefficient discussion became a native
   Interpretation callout.
4. A reference-category Exercise/Solution was added and then removed.
5. An association-is-not-causation Warning was added and then removed; the
   qualification returned to ordinary prose.

## Accepted process lessons

- Exercises belong in a later, separate pass.
- Repeated warnings become visual noise. Reserve boxes for failure modes that
  are unusually salient in the local chapter.
- Formula disclosure can shorten the main path while preserving derivations.
- Interpretation callouts require contextual judgment about the order of the
  concrete example and general rule.
- A source-only diff should precede rendering.

## Last reviewed candidate structure

The last scratch version retained:

- the numbered Reference category Definition;
- collapsed two-category substitution algebra;
- the adjusted categorical-comparisons Interpretation;
- the original causal qualification in ordinary prose.

It did not retain the Exercise or Warning.

Jared requested and then rolled back an alternative ordering in which the
concrete coefficient interpretations appeared in prose before a general rule
in the callout. The rollback shows that no universal ordering rule should be
inferred from the pilot.

## Scratch provenance

The unpromoted source candidate and HTML render were created under:

`working/callout_dryrun_regression04/`

The initial whole-book inventory was created under:

`working/callout_candidate_sweep/`

These scratch paths are not durable dependencies; the useful findings and
inventory have been promoted into `todo/`.
