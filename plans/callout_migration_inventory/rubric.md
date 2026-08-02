# Callout candidate sweep

Status: in progress

This is a review-only, source-based inventory. It does not authorize edits to
book chapters, callout markup, prose, formulas, exercises, or generated
outputs.

## Scope

Review the book landing page, 25 substantive chapters, and the two prose/data
appendices in `_quarto.yml`. Exclude the three embedded app pages, test
fixtures, slides, supplements, problem sets, and example-bank material.

## Candidate types

- **Definition** — a term or concept that receives a precise reusable meaning.
- **Notation** — a symbol, indexing convention, or compact reference that
  students will need again.
- **Technical detail** — a correct but interruptive derivation, formula,
  qualification, or implementation detail that can be hidden in HTML.
- **Exercise** — a short inline knowledge check with a concise solution.
- **Key idea** — an unnumbered conceptual takeaway worth emphasizing.
- **Interpretation** — an unnumbered translation of a result, parameter,
  display, or model into substantive language.
- **Warning/Common mistake** — an unnumbered misconception, invalid move, or
  boundary students are likely to violate.

Formula-only details use the semantic `.formula-detail` mechanism inside the
appropriate surrounding block; they are not a separate callout type.

## Selection rules

Prefer passages that are important, locally coherent, and likely to benefit
from visual emphasis or optional disclosure. Do not recommend a callout merely
because a passage contains a definition, formula, or example. Avoid turning
ordinary narrative transitions into boxes.

Exercises are out of scope for the first migration pass. Retain the inventory
of possible exercises for a later, separate pedagogical pass.

Use Warning/Common mistake callouts only for failure modes that are especially
salient to the chapter at hand. A broadly applicable qualification should
usually be established once and then handled in ordinary prose when it recurs.
For example, do not add an association-is-not-causation warning beside every
regression coefficient.

For every candidate record:

- chapter and stable source anchor;
- proposed type;
- a short description of the content;
- confidence: high, medium, or low;
- preparation: `drop-in`, `local rewrite`, or `structural rewrite`;
- why the callout improves reading or retrieval;
- any overlap with an existing callout.

This first pass identifies candidates only. It does not adjudicate exact
boundaries, wording, titles, numbering, or solutions.
