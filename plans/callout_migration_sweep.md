# Migrate chapter content into the callout system

Status: **pending; inventory complete, migration not started**

Decision date: 2026-07-30

This is the authoritative plan for identifying and migrating chapter content
into the callout infrastructure. It supersedes the first-wave sketch in Phase
3 of `todo/callout_exercise_system_rollout.md`.

The infrastructure is already on `main`. This todo concerns chapter content,
which may require local prose changes and must be handled separately.

## Durable artifacts

The initial source-only sweep is preserved in
`todo/callout_migration_inventory/`:

- `rubric.md` defines the candidate types and selection rules.
- `summary.md` records the whole-book patterns and recommended order.
- `foundations.md` covers the landing page, single-variable chapters, and
  two-variable chapters.
- `probability_inference.md` covers probability and inference.
- `regression_prediction.md` covers regression, prediction, and the
  appendices.
- `regression04_dry_run.md` records the first chapter pilot and the decisions
  it produced.

The inventory covers all 28 in-scope pages: the landing page, 25 substantive
chapters, and two data appendices. The three embedded app pages were excluded.

## Decisions from the first dry run

1. **Exercises are out of scope for the first migration pass.** Exercise
   candidates remain in the inventory for a later pedagogical pass.
2. **Warnings should be rare.** Use a Warning/Common mistake callout only for
   a failure mode that is unusually salient in that chapter. Do not repeat a
   universal qualification every time it applies; for example, association is
   not causation should not become a box beside every regression coefficient.
3. **Callouts must have a distinct job.** Do not box prose merely because it
   contains a definition, formula, interpretation, or caveat.
4. **Examples and general rules need deliberate ordering.** The regression
   pilot showed that moving concrete interpretations into or out of a callout
   can make the narrative worse even when every sentence remains correct.
   Decide the role of the callout in context rather than applying a fixed
   example-first or rule-first template.
5. **Formula disclosure is promising.** Moving extended substitution algebra
   behind `Details and formulas` shortened the main reading path without
   deleting the derivation.

## First-pass scope

Consider:

- numbered Definitions;
- numbered Notation blocks, used sparingly for symbol systems rather than
  individual symbols;
- numbered Technical details;
- native Key idea callouts;
- native Interpretation callouts;
- a small number of chapter-specific Warning/Common mistake callouts;
- nested `.formula-details` disclosures.

Defer:

- Exercises and Solutions;
- broad prose rewrites whose purpose is not required by an accepted callout;
- new chapter-end exercise sets;
- formula changes or statistical-content changes;
- global mechanical conversion of existing `.callout-note` blocks.

## Collision boundary

Jared is actively working on chapters 1–5. Do not migrate those chapters until
that work pauses and is committed. Begin with a chapter outside that range and
check the live source hash before applying any candidate.

## Migration workflow

### 1. Re-adjudicate the inventory

Review one chapter at a time. Treat every inventory entry as a candidate, not
an accepted change.

For each candidate decide:

- `accept`;
- `accept with narrower scope`;
- `hold for prose restructuring`;
- `defer to the exercise pass`;
- `reject`.

Apply the new warning rule during adjudication. Most warning candidates should
remain ordinary prose.

### 2. Draft a chapter candidate

Work in `working/<chapter-callout-task>/candidate/` before touching the root
chapter. Preserve a hash of the live source.

For each accepted block:

- choose a stable identifier for numbered blocks;
- keep the callout concise enough to retrieve later;
- remove or repair duplicated surrounding prose;
- use `summary="Details and formulas"` for formula disclosures;
- choose explicitly whether a formula appears in the default PDF;
- preserve the chapter's examples, claims, and statistical meaning.

### 3. Review the source diff

Before rendering, inspect the exact diff against the frozen source. Reject
changes that:

- create a box without improving emphasis, retrieval, or reading flow;
- separate an example from the prose needed to understand it;
- repeat the same interpretation inside and outside the callout;
- turn a recurring caveat into visual noise;
- introduce unrelated chapter revision.

### 4. Review HTML

Render only the candidate chapter in a scratch mini-project. Check:

- callout placement in the surrounding narrative;
- title, icon, color, and numbering;
- collapsed/open behavior;
- formula-detail labels;
- paragraph spacing and nested blocks;
- narrow and ordinary browser widths.

### 5. Promote only after approval

Confirm that the live chapter still matches the frozen source hash. Rebase the
candidate if it does not. Apply only the approved blocks and their necessary
local prose repairs.

### 6. Verify the applied chapter

After promotion:

- run terminology and numeric checks applicable to the chapter;
- render the current HTML chapter;
- inspect all changed blocks and neighboring prose;
- render the default and full-formula PDF profiles when the existing
  animation/PDF fallback issue no longer blocks the full book;
- inspect the final Git diff and commit the chapter as a focused change.

## Suggested first wave

Choose one or two chapters outside chapters 1–5 with existing callouts that
can be reclassified without broad rewriting. The `regression_04_categorical`
pilot remains a useful candidate, but its exploratory patch is not approved
for promotion.

The first accepted wave should test:

- one numbered Definition;
- one genuinely useful Interpretation or Key idea;
- one formula disclosure;
- at most one unusually salient Warning;
- no Exercises.

## Later pass: exercises

Return to the exercise candidates only after the prose-callout migration has
stabilized. Evaluate exercises as teaching interventions, not formatting
opportunities. Each accepted exercise needs a clear task, sufficient prior
instruction, a concise Solution, and a transition that still works when the
Solution remains collapsed.

## Completion criteria

This todo is complete when:

1. every in-scope chapter has an adjudicated candidate inventory;
2. accepted first-pass callouts have been migrated chapter by chapter;
3. HTML and applicable PDF checks pass;
4. cross-references and chapter-level counters are correct;
5. held/rejected candidates and the deferred exercise pass are recorded;
6. scratch candidates and renders have been promoted, archived, or removed.
