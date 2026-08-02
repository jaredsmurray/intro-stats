---
name: draft-from-brief
description: Draft a statistics textbook chapter or section from an approved writer brief, source artifacts, Jared's voice pack, applicable project style skills, and a deliberately limited set of current-book chapters. Use when the user asks to write, generate, or hand off a chapter from a brief, including production drafts and matched book/no-book conditions. Prevent existing book prose from expanding scope or importing wordiness, repetition, and unwanted style.
---

# Draft From Brief

Treat the approved brief as the composition contract. Use original artifacts for teaching logic, empirical sources for facts, the voice pack for prose, and selected book chapters only for continuity.

Every `must`, exclusion, length range, and output condition in the brief is binding. A test setting, time pressure, preferred concision, or convenience is not permission to produce a partial or shortened draft. If a requirement is genuinely impossible with the authorized sources, stop and report the blocker rather than silently underdelivering.

## Read in this order

1. Read the approved brief completely, including access restrictions and output path.
2. Read `JARED_VOICE.md`, `JARED_CHECKLIST.md`, and `JARED_EXAMPLES.md` in full before drafting. Treat the examples as primary prose authority.
3. Read the applicable project skill in full. Chapter prose requires `book-style`.
4. Read the original artifacts, scripts, data, and provenance files authorized by the brief.
5. Read only the current-book files authorized by the brief.

Do not open neighboring drafts or unlisted chapters because they are convenient.

Treat HTML-commented sections and parked TODOs as inactive unless the brief activates them. If the user protects existing comments, preserve them byte-for-byte; remember that Quarto can still execute code chunks inside HTML comments.

## Keep source roles separate

- Follow the brief and source artifact for scope, flow, arguments, examples, and deliberate repetition.
- Follow scripts and data for empirical values and model behavior.
- Follow the voice pack and surface skill for prose.
- Use the existing book only to learn what readers know, how datasets were introduced, which notation and anchors exist, and how established mechanics work.

Never treat existing book prose as a sentence template. If it is wordy, repetitive, overexplained, or inconsistent with the voice pack, do not reproduce that feature. Book access is not permission to mention every related idea the writer encounters.

## Compose without coverage anxiety

Before drafting, make an internal list of the required teaching moves and assign each one a job. Do not emit this list.

Every paragraph must do at least one of the following:

- advance the source artifact's argument;
- interpret a required equation, result, table, or figure;
- resolve a likely misconception needed for the next move;
- connect to prior coverage more economically than reteaching it.

Cut a paragraph that exists only because the current book contains related material. State a caveat once, where it changes interpretation. Do not repeat the same claim in prose, a caption, a table, and post-figure commentary.

Compare adjacent paragraph jobs, not just repeated wording. If two paragraphs answer the same reader question, merge them unless the second adds a new calculation, a distinct interpretation needed for the next move, or a decision consequence. For example, do not interpret a model's $R^2$ and then add a second paragraph that restates the same fit-versus-slope distinction in more general language.

Treat coefficient-by-coefficient interpretations as distinct teaching jobs when the coefficients use different reference conditions or answer different comparisons. Use parallel full-sentence items when students need to map several coefficients to their meanings; do not compress that mapping into a dense paragraph merely because the items share a grammatical structure.

Meet full coverage through economical explanation, not omission. Do not drop a required interpretation, example, figure, appendix item, or empirical check to make the draft feel tighter.

Set up each figure before it appears. Afterward, discuss only a non-obvious reading or the fact needed for the next step. Keep section closers tied to the example or decision rather than adding a general aphorism.

## Draft the chapter

- Preserve the requested content progression without converting slide headings one-for-one into book headings.
- Use hidden computation for empirical values, fitted equations, tables, and figures. Recompute values rather than hard-coding check numbers. Use `format_signed()` or an equivalent helper for signed inline values, and guard fragile directional or threshold claims with executable checks.
- Keep rendered prose programming-language agnostic when the brief requires it.
- Introduce a dataset fully only if it is new to the book; otherwise give the brief reminder and define only new variables.
- Give every displayed equation an immediate prose interpretation.
- When an interpretation depends on algebraic substitution or rearrangement, show enough of that algebra for a student to reproduce the reasoning. Do not replace the derivation with a verbal assertion merely to shorten the draft.
- For each fitted regression model whose coefficients or uncertainty receive substantive interpretation, place the project's standard `coef_table()` or `reg_table()` near its first substantive use unless the brief explicitly excludes a table. Do not add a table when fitted shape, predictions, or diagnostics are the teaching target; polynomial models ordinarily use curves and residual plots when their individual coefficients are not interpreted.
- If the chapter has a "Data used" closer, list only datasets that appear in rendered prose, figures, or tables; parked or commented material does not count.
- Present confidence intervals before significance language and keep observational analyses associational.
- Treat competing specifications as tradeoffs. Do not sell the selected model as a universal fix.
- Do not invent a framework, taxonomy, or broad rule absent from the brief or source artifact.

Write only the authorized output file. Do not alter the brief, sources, current chapters, or comparison drafts.

## Audit before handoff

Run four passes:

1. **Brief compliance:** Make a requirement-by-requirement internal checklist of every `must`, example, figure, exclusion, length constraint, and output rule. Do not write the file while any item is absent or contradicted.
2. **Empirical execution:** Run all code from the project root; verify inline values, tables, figures, labels, and cross-references. Inspect changed figures visually. Check rendered text for sign, direction, and rounding consistency. Confirm that every substantively interpreted regression fit has its standard table near first use unless the brief excludes it, and that other fits use the display named in the brief.
3. **Voice:** Apply every item in `JARED_CHECKLIST.md`, including paragraph openings, formula restatements, long-short rhythm, vocabulary, and evidence framing.
4. **Redundancy and contamination:** Search for repeated claims, adjacent paragraphs with the same teaching job, post-figure recaps, extra book-derived coverage, inherited prose habits, and caveats that do not alter interpretation.

If the current book and voice pack conflict, revise toward the voice pack while preserving factual continuity. Deliberate deviations require explicit user authorization; otherwise resolve them or report a true blocker. Report the output path, prose word count, and any authorized deviation from the brief.
