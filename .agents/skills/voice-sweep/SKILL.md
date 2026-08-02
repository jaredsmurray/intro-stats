---
name: voice-sweep
description: >
  The book's voice-conformance loop: sweep chapters for violations of Jared's voice pack and the
  book-style rules, adjudicate flags against the pack's examples, produce a gated report, and run
  the three-writer rewrite pipeline on approved sections. Use for "voice sweep," "sweep this
  chapter," "check voice conformance," "run the loop on <chapter>," rewrite-mode requests on a
  flagged section, benchmark runs against Jared's own rewrites, or closing out a review round.
  Never edits chapter files without Jared's approval at a gate; typo fixes are standing-authorized.
  Layers on the book-style skill and the voice pack.
---

# Voice sweep — the conformance loop

Four modes: **sweep** (find and report), **rewrite** (three-writer pipeline on an approved section), **benchmark** (score blind drafts against Jared's own rewrite), **reconcile** (close out a round). All artifacts live in `working/proposed_edits/<date>_<scope>/`. Chapter files change only at a gate with Jared's approval — the single exception is unambiguous typos, which are standing-authorized (fix and log).

## The adjudication law (applies in every mode)

1. **The pack's examples are the primary reference.** `JARED_EXAMPLES.md` plus the rules in `JARED_VOICE.md` (especially §2.6 editing calibration) decide what passes. Draft text is never precedent — much of it is machine-generated imitation, and "the draft does it elsewhere" is not a defense. This holds until Jared declares the revision done.
2. **A keep needs a license.** Every "keep" verdict on a flagged line must cite the pack rule or example that licenses it. No citation, no keep.
3. **Author-touched text is sanctioned.** If Jared wrote or rewrote the passage and left the phrase standing, it stays — his hand outranks any rule. Classify before judging: diff against the round's freeze, and check the applied-fixes ledger (text that differs from the snapshot and isn't in the ledger is his). Weak-sanction cases (he edited nearby but may not have weighed the line) get flagged with the caveat stated.
4. **Two diagnostics for every crafted line:** (a) do its references resolve — real antecedent, real cross-ref, no phantom callbacks? (b) does it deliver content or just gesture ("the right panel is the surprise")? Then the uniqueness test: no restating the previous sentence, no reciting what a table or figure shows, one metaphor per idea, redundancy judged across sections.
5. **Comment-status check.** Quarto chapters carry `<!-- -->` parked blocks and greps don't see them. Map comment blocks (`grep -n '<!--\|-->'`) before adjudicating any hit; parked hits go to the scrub-before-re-enabling ledger, not the live tiers. (Round 1 and round 2 both tripped on this.)

## Mode: sweep

Input: one or more chapter `.qmd`s (or "all"). Output: a tiered report. No chapter edits.

1. Create `working/proposed_edits/<date>_<scope>/` if the round doesn't have a directory yet.
2. **Grep pre-pass** for the mechanical tells — the §2.4 ban lists (vocabulary, meta-commentary, consultant idioms), checklist scan terms, and Jared's named tells (load-bearing, key insight, X-sigma event, worth-family). Save hits to `grep_prepass.txt`.
3. **Comment map** per file; mark each grep hit live or parked.
4. **Scanner fan-out:** one read-only agent per chapter, parallel, using `scanner_brief.md` in this skill's directory verbatim (fill in the target file). Scanners over-flag by instruction.
5. **Adjudicate every flag yourself** under the law above. Never let an unverified scanner flag into the report. Tiers:
   - **fix-inline** — deletions and ≤1-sentence trims, exact before → after text, license/precedent cited. For guidance-asides and reader-advice sentences, test three conditions first — is it redundant, irrelevant to the through-line, or not worth its ink? Those are the reasons he deletes asides whole (the workhorse paragraph, the conditioning caution, the mosaic section); when one applies, propose the deletion. An aside that clears all three gets a repair proposal, not a delete;
   - **needs-prose** — flagged with the violations and the hard constraints (code chunks, cross-refs, math). Do NOT prescribe which prose content must survive: his rewrites restructure at the section level and regularly cut content a flag assumed had to stay (the singlevar_04 returns rewrite deleted the quantified comparison the flag marked as keep-worthy). No drafted prose unless Jared asks (his drafting feedback: flags first);
   - **your-call** — ban-list conflicts inside his own text, rule-4 confirmations, judgment calls;
   - **keeps** — documented with licenses;
   - **parked** — violations inside comment blocks, listed for scrub-at-revival.
6. Write `report.md` (or `roundN_report.md`), present the summary in chat, and **stop for Jared's triage**. This is Gate A.

## Mode: rewrite

Input: a section Jared approved for rewriting at Gate A (only when he asks for drafts — his default is rewriting flagged sections himself). Pipeline per section, in `sections/<chapter>__<slug>/`:

1. `original.md` — the span verbatim with file and line range. Freeze it before anyone writes.
2. `brief.md` — instantiate `rewrite_brief.md` from this skill's directory (fill SPAN, KNOWN ISSUES as neutral statements, OUTPUT paths).
3. **Two Opus writers, biased pair, run in parallel, no cross-visibility:** Writer A additive, Writer B subtractive (the differentiation addenda are in the brief). Save `draft_opus_A.md` / `draft_opus_B.md` verbatim; never edit them.
4. **Own draft** (`draft_fable.md`) written before reading A or B, book-style skill invoked.
5. `recommendation.md` — score all three against `JARED_CHECKLIST.md`, cite which pack examples each move leans on, recommend one draft or a labeled splice. Present and **stop** for Jared's pick.
6. On approval: apply, render-verify, log in the ledger.

## Mode: benchmark

When Jared rewrites a flagged section himself, use it to calibrate: freeze the pre-rewrite text, build a blind context file that excludes his ground truth, run the rewrite pipeline against it, then diff each draft against his version in `jared_diff.md` and score. What the drafts missed becomes brief/pack update candidates. His diffs are calibration material for writers; adjudication licenses still come only from the pack.

## Mode: reconcile

Closes a round after Jared reviews. The chapters are authoritative, not the worksheet:

1. Diff every touched chapter against the round's freeze; classify each change (his hand vs. applied item).
2. **Worksheet deletion ≠ flag rejection** — he deletes items he handled in the chapter; verify by diff before closing anything.
3. Verify his edited replacements landed (not the originally proposed text); catch typos introduced by the round's own edits.
4. Update the applied-fixes ledger, write final dispositions (`*_resolved.md`), archive the worksheet.
5. Harvest calibration: new before/after pairs into the round's `examples_candidates.md` (staged in-repo; promoted to `JARED_EXAMPLES.md` only when Jared declares the book done), and stage any pack-rule deltas in `voice_pack_update_*.md` — **pack files are edited only on his explicit OK**.
6. **Distill rules as conditions, not blanket bans.** Before writing "never X" from a deletion, look for places he does X (in his rewrites and reviewed keeps) and name what separates the kept cases from the cut ones. Two over-generalizations from single edits — "never narrate after a figure" (really: post-figure prose must be non-obvious or feed what follows) and "state math as math" (really: displays only for math the reader will need; he often skips math entirely) — both drew corrections.

## Mechanics

- **Render verification:** after any applied edit, `export PATH="/Applications/Positron.app/Contents/Resources/app/quarto/bin:$PATH"` then `quarto render <file> --to html`. Background shells don't have quarto on PATH without the export. Use Positron's bundled Quarto, not RStudio's — it's the newer one and the version `publish.sh` builds with.
- **Caption strings** (`#| fig-cap:`) are prose and in scope; they are YAML, so `\$` escapes are invalid there — use a raw `$` (the `\$` convention is body-prose only). Computed captions use `#| fig-cap: !expr '<R expression>'` — the expression MUST be single-quoted after the tag, or every render in the project fails YAML validation, not just that chapter's.
- **Course convention:** when the word "probability" carries a number, the number is on the [0,1] scale — in figures too (axis scales and value labels on probability charts use `number()`, not `percent()`).
- **Concurrent Opus writers** occasionally stall on infrastructure; stagger the pair or budget one resume-via-message.
- Reference paths: voice pack at `/Users/jm75583/Dropbox/voice-pack/voice/{JARED_VOICE,JARED_CHECKLIST,JARED_EXAMPLES}.md`; book rules in `.claude/skills/book-style/SKILL.md`; round-1 archives and the benchmark exemplars in `working/proposed_edits/2026-07-15_full-sweep/`.
