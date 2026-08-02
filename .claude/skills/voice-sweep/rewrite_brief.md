# Rewrite brief v2.3 — template

Instantiate per section: fill the SPAN, KNOWN ISSUES, and OUTPUT path. ★ marks v2 changes (Thaler benchmark + 2026-07-16 calibration); ★★ marks v2.3 changes (the 2026-07-17 examples-primary correction and the post-worksheet ground-truth rewrites — see `working/proposed_edits/2026-07-15_full-sweep/examples_candidates.md`).

## Read, in this order
1. `/Users/jm75583/Dropbox/voice-pack/voice/JARED_VOICE.md` (§2.6 editing calibration especially)
2. `/Users/jm75583/Dropbox/voice-pack/voice/JARED_CHECKLIST.md`
3. `/Users/jm75583/Dropbox/voice-pack/voice/JARED_EXAMPLES.md` — ★★ the primary reference; when a move needs a defense, the defense is a pack example, never "the draft does this elsewhere"
4. `/Users/jm75583/Dropbox/intro_notes_revision/.claude/skills/book-style/SKILL.md`
5. ★ `working/proposed_edits/2026-07-15_full-sweep/sections/prob_07__clt-thaler-run/jared_diff.md` and ★★ `working/proposed_edits/2026-07-15_full-sweep/examples_candidates.md` — the author's own rewrites, analyzed move by move. Imitate these moves, not just the abstract rules.
6. The section's `original.md` and the chapter file for context (benchmark runs substitute `context_original.md` and add isolation rules).

Do not read `report.md`, `round*_report.md`, or other sections' directories — they contain leans that would homogenize the drafts.

## The task
Rewrite the span to conform to the voice pack and book style. [KNOWN ISSUES — from the sweep, neutral statement, no fix-leans. ★ List optional items only if resolving them is wanted: the benchmark showed every writer resolves whatever the brief mentions.]

## Calibration (learned from the author's own rewrites)

- **Weigh competing methods; don't sell one** (v2.1 — book-style rule 5): comparisons open two-sided with mechanisms; parallel features get parallel treatment; advantages stated as complements; recommendations conditional on use; no crowned winners, no personified virtues; idioms may conclude an itemized argument, never replace one.
- **Replace performance with teaching, not with silence.** Where the original stages or pitches, prefer substituting substance — a mechanism, an interpretation, a decision reading, notation, or a link into the course arc — over bare deletion. Deletion is the fix for redundancy.
- **Cut**: importance-ranking meta-commentary ("worth memorizing/noting/filing away/…", "keep in mind", "deserve emphasis"), payoff-pitches ("here is what X is worth"), lesson-frames ("the lesson generalizes", "this shows that"), phantom callbacks (verify cross-references before keeping them), site-of-move announcements ("One caution before moving on", "One word on…").
- ★★ **Links point backward by default.** Show importance by connecting to what the reader already has ("This is just like the sample covariance we computed in @sec-cov-cor"), not by promising future use ("an identity we will use constantly"). Short forward links ("We'll do that next") stay.
- ★★ **Rate results by information or use, not reader emotion**: "the right panel is the surprise" → "the right panel is more informative."
- ★★ **Closers carry the case result or the decision it informs.** The generalized lesson lives where the machinery is introduced; a closing aphorism gets cut even when true. (Author did this twice: risk epigrams → decision framing; portfolio lesson → case-specific because-clause.)
- **Keep**: claims about the material's standing when calibrated ("one of the most important results"); short claims with justification attached, even exclamatory ("Independence is important here!"); "worth" in decision contexts; informative caption text (what to see, plainly).
- ★★ **Drumrolls get the deliver test, not a default keep** (tightened from v2.2): an existing reveal-beat survives only if the same sentence or the very next one delivers the content it gestures at, and nothing else already carries it. Never add new ones.
- **Calibrate superlatives downward** rather than deleting the sentence ("the most celebrated" → "one of the most important"); "quite" is the house intensity level.
- **The uniqueness test precedes the register test** (v2.2): a crafted line survives on unique freight, not charm — if it restates content carried elsewhere (a metaphor already spent, a point the table or figure shows, the previous sentence), it goes regardless of how good it sounds. Prose never recites what a table or figure already shows; it interprets or moves on. Redundancy is judged across sections, not just within paragraphs.
- **Purpose statements and short forward links are in-register; schedules, teasers, and site-of-move announcements are not** (v2.2): a section-purpose sentence or a short local plan is his style; itemized roadmaps, payoff teasers, and re-announcing a connection at the site of the move are violations.
- **Replacement register matches the section's work** (v2.2): staging → mechanism; flourish → decision framing; drumroll → formal scaffolding/notation. Pick the instrument the passage actually needs. ★★ Where the author adds, he adds pedagogy (a decision-framing question, an explicit calculation), not connective tissue.
- An unquantified degree claim may be fixed by deleting the claim when it isn't needed, not only by adding the number.
- **Course conventions**: when the word "probability" carries a number, the number is on the [0,1] scale.

## Constraints
- Keep all R code chunks, chunk options, labels, cross-references, callouts, and math intact except where a fix requires a minimal touch; `fig-cap:` strings are prose and in scope (they are YAML — raw `$`, no `\$` escapes).
- ★ Bounded additions are in scope: explanatory content of the kinds listed above. New frameworks, taxonomies, or empirical claims remain out (book rule 4).
- ★ Length: similar; somewhat longer is fine when the additions teach.
- Output is a drop-in replacement for the whole span; reproduce unchanged parts verbatim.

## ★ Writer differentiation (restores informative variability)
Two same-brief Opus drafts converge to near-identical strategies. Run:
- **Writer A (additive bias)** — append to A's task message: "Prefer additive fixes: where the original performs, replace it with teaching content. Cut only what adding can't redeem."
- **Writer B (subtractive bias)** — append to B's: "Prefer subtractive fixes: cut and tighten. Add a sentence only where a cut leaves a genuine gap."
- **Fable draft** — no bias addendum (balanced), written before reading A or B.

## Output
- Write the complete replacement span — nothing else — to the `draft_*.md` path given in the task message.
- Final message: 3–6 lines on moves made, code touches, judgment calls. Metadata, not prose for a human.
- ★★ Before the draft is shown to the author, the orchestrator scores it against `JARED_CHECKLIST.md` and attaches the scorecard; a draft that fails a checklist item goes back for one revision pass first.
