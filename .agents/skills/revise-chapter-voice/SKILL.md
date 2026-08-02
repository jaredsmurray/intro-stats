---
name: revise-chapter-voice
description: Revise an existing statistics textbook chapter, section, or older Quarto/Markdown draft into Jared's concise, clear, accessible-academic teaching voice. Use when the user asks to tighten, de-word, modernize, clean up, or bring older notes back into voice; remove repetition and overexplaining; or reconcile legacy prose with the current voice pack and book-style rules while preserving substantive content, equations, examples, figures, and uncertainty.
---

# Revise Chapter Voice

Treat the existing draft as a content source, not a style precedent. Preserve its substantive work while rebuilding the prose under the current voice pack and `book-style` rules.

## Establish the revision contract

1. Read the project instructions, `book-style`, and all three voice-pack files in full.
2. Read the target draft completely, including setup code, figures, tables, cross-references, and inline computations.
3. Read only the current chapters needed to resolve continuity or notation. Do not absorb unrelated prose.
4. Preserve the original file by default. Write a new `_revised.qmd` file unless the user explicitly requests in-place editing; if editing in place, create a recoverable backup first.
5. Identify user edits and protect them. Do not replace newer author prose with older generated language.
6. Classify active prose, visible TODOs, and HTML-commented or parked material before editing. When the user protects comments, preserve them byte-for-byte; Quarto may still execute code chunks inside HTML comments.

## Separate content from inherited style

Preserve unless the user says otherwise:

- the statistical claims and their epistemic strength;
- equations, model specifications, examples, datasets, and empirical results;
- figure and table purposes;
- citations, anchors, and needed cross-references;
- the chapter's substantive sequence.

Do not preserve merely because it appears in the draft:

- repeated explanations of the same point;
- throat-clearing, roadmaps, staged transitions, or payoff sentences;
- prose that recites a figure, table, or equation;
- caveats repeated after their interpretive work is complete;
- long definitions assembled from several near-synonyms;
- invented frameworks, broad lessons, or generic concluding advice;
- old prose habits that conflict with the current voice pack.

## Revise in passes

### 1. Build a claim map

Identify the unique claim or teaching job of each paragraph. Mark duplicated jobs across nearby paragraphs, captions, callouts, and section endings. Keep the strongest occurrence and delete or repurpose the rest.

Apply a one-result, one-explanation, one-caveat default. Adjacent paragraphs answering the same reader question should become one unless the later paragraph adds a new calculation, a distinct interpretation required for what follows, or a decision consequence. Stating an $R^2$ interpretation and then separately re-explaining the same slope-versus-fit distinction is duplication. Repeating an omitted-variable caveat during diagnostics is duplication unless the diagnostic supplies new evidence about it.

Treat coefficient-by-coefficient interpretations as distinct teaching jobs when the coefficients use different reference conditions or answer different comparisons. Preserve a parallel list when students need to map several coefficients to their meanings; shared sentence structure does not make those interpretations redundant.

### 2. Tighten structure

Combine paragraphs that split one thought artificially. Split paragraphs that carry unrelated jobs. Preserve necessary bridges, but do the transition instead of announcing it. Remove headings that divide a continuous argument without helping navigation.

Preserve an explicit analytical question when the chapter later answers it. The question-answer link is structural; remove only rhetorical questions that announce a topic without creating an obligation for the subsequent analysis.

Put ideas in dependency order. Define a technical term before discussing its advantages, limitations, or applications. Choose either a terse caveat label or a fuller explanation at the point of risk; do not use both merely to emphasize caution.

### 3. Rewrite in teaching voice

Lead with the claim, attach the reason, and use a patient academic register. Keep enough explanation for a student to reproduce the reasoning. Concision does not mean fragments, omitted formula interpretations, or unexplained jumps.

Use one colloquial moment only when it carries a technical point. Do not manufacture register drops to satisfy a quota.

### 4. Protect statistical meaning

Check that compression has not changed:

- conditional versus marginal interpretations;
- association versus causation;
- mean, median, probability, or prediction targets;
- confidence-interval and uncertainty language;
- reference categories, held-constant clauses, or model hierarchy;
- the distinction between sample findings and population claims.

Do not add a new method, framework, or interpretation to make the revision feel complete.

### 5. Reconcile prose with displays

Set figures up before they appear. Let captions carry the visible reading. Keep post-display prose only for non-obvious interpretation or the next inferential move. Give each displayed equation one immediate prose restatement, not several paraphrases.

Preserve algebraic substitution or rearrangement when it makes a coefficient interpretation visible. Do not replace a derivation with a verbal assertion merely to reduce length; keep enough algebra for a prepared student to reproduce the reasoning.

Match each model display to its teaching job. Use the standard regression table when coefficients or uncertainty receive substantive interpretation. When fitted shape, predictions, or diagnostics are the target, prefer the corresponding curves, calculations, or diagnostic plots; polynomial coefficient tables are usually unnecessary when the individual terms are not interpreted.

## Verify the revision

- Run the chapter from the project root and fix execution, label, and cross-reference failures.
- Compare all empirical values, equations, figures, and tables with the source draft. Visually inspect every changed figure or table rather than treating a successful render as sufficient.
- Check rendered text for sign, direction, and rounding consistency. Use computed sign formatting and executable checks for fragile claims instead of hard-coded signs or unguarded directional prose.
- If the chapter has a "Data used" closer, confirm that it lists only datasets appearing in rendered material.
- Run `JARED_CHECKLIST.md` in full and scan for banned vocabulary.
- Compare paragraph jobs pairwise, including across section boundaries, and merge or delete duplicated jobs.
- Compare before-and-after paragraph and prose word counts as diagnostics, not targets. If a draft identified as wordy barely changes, rerun the claim-map and redundancy passes or explain why its length is substantively necessary.
- Report material deletions, reorganizations, meaning-preserving changes, and the duplicated jobs removed that the user should review.

Do not measure success only by word-count reduction. The revision succeeds when each remaining paragraph carries unique explanatory freight and a prepared student can still follow the argument.
