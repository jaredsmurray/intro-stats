# Introduction to Statistics and Data Science — Project Instructions

Single source for project instructions; `CLAUDE.md` imports this file. Edit
here, not there.

This repository holds the book: root chapter `.qmd` sources, the Quarto book
configuration, book tooling, and the review memory that travels with the
chapters. Slides, problem sets, coding supplements, exams, the Canvas
machinery, the shiny apps, and the datasets live in separate repositories.

## Project hygiene

- All scratch and experimental work goes in `working/` — never the repo root —
  as **one directory per task** (`working/<task-slug>/`). When a task ends,
  promote its keepers to their real homes and archive or delete the rest.
- Durable plans and pending decisions go in `plans/` (tracked). Actionable work
  belongs in GitHub Issues; a tracking Issue links to its plan, and the plan
  does not maintain a second open/closed checklist.
- One-off figure-generation scripts live in `tools/figures/`. Generated
  figure/animation assets land in `images/` — never at the repo root.
- Shared R code goes in `R/` by bucket — `render/` (render-time helpers for
  chapters) and `pkg/` (package-candidate, possibly student-facing one day).
- **This repository is public.** Nothing in it may contain solution content,
  exam material, student names, credentials, or private absolute paths. The
  one documented exception is the voice-pack import paths below, which point at
  a local Dropbox directory that is deliberately external to this repo.

## Data

Datasets are not tracked here. `data/` is gitignored and populated by
`tools/get_data.sh`, which reads the one-line `data_pin` file at the repo root
and fetches that release of the `teaching-data` repository, including the data
cards that `appendix_data.qmd` includes from `data/cards/`. Numbers in the book
cannot drift unless the pin moves. A fresh clone renders with:

```
./tools/get_data.sh
quarto render
```

`data_derived/` is tracked: it holds small derived analysis artifacts (not
teaching data) that chapters read directly.

## Checks

The check engines are vendored from the `qmd-checks` toolkit into
`tools/checks/` (`tools/checks/VERSION` records the pinned toolkit tag);
re-run that toolkit's `install.sh` to refresh them. The book owns its config:
`style_terms.tsv`, `tools/number_consistency_ignore.tsv`,
`tools/terminology_ledger.tsv`, and the scan set declared in
`tools/checks.conf`. Two checks are book-specific and stay here:
`tools/check_callouts.sh` (a render regression test tied to the patched
callout extension, with fixtures in `tests/fixtures/callouts/`) and
`tools/check_review_history.sh`.

House terminology and displayed-number precision are machine-checked. Hand
edits made directly in an editor never hit the Claude PostToolUse hooks —
sweep with `./tools/check_terms.sh --all` (`--fix` to apply) and
`./tools/check_number_consistency.R --all`.

## Writing prose

- **Chapter prose** (root `.qmd` files): follow the `book-style` skill. It
  carries the book-specific rules plus the machine-checked house terminology
  (`style_terms.tsv`); the skill file is canonical — read it rather than
  working from a remembered summary.

## Reviewing and revising chapters

- The canonical chapter review, adjudication, revision, and verification
  workflow is the `book-student-review` skill at
  `.agents/skills/book-student-review/SKILL.md`. The entry under
  `.claude/skills/` is a compatibility pointer, not a second source.
- Use its streamlined author decision queue: batch verified low-judgment
  corrections, present no more than five judgment calls at once, handle
  structural choices individually, and keep terminology-ledger approval
  separate.
- The active task makes one integrated adjudicated revision. After rendering,
  run the independent voice adversary and targeted verifier in parallel against
  that finished revision; use a separate revision-editor only for an explicit
  handoff. At final adjudication, run the voice-pack maintenance hook; never
  modify the voice pack from that hook without explicit approval.
- During diagnosis and adjudication, review agents may read project files but
  write only inside their exact `working/<review-task>/` directory. They do not
  render the live project, execute code that writes elsewhere, or edit chapters,
  ledgers, plans, generated assets, or the voice pack.
- Keep proposed revisions under `working/<review-task>/candidate/`. Apply a
  candidate to named project files only after Jared approves or delegates the
  relevant disposition, or under the standing mechanical waiver below.
- The standing mechanical waiver covers spelling, punctuation, duplicated
  words, unmistakably broken references, and markup or parse repairs with one
  reasonable interpretation and no change in meaning or computation. It does
  not cover numeric, statistical, terminological, explanatory, structural, or
  behavior-changing fixes. List every waiver-applied change in the final
  summary.
- Before applying a candidate, confirm that its frozen source hash still
  matches the live file. If parallel work changed the file, rebase the
  candidate rather than overwriting it. After application, inspect the exact
  diff for unapproved files or scope.
- Rendering and generated-output writes belong to post-application
  verification, after edit authority exists; they are not part of diagnostic
  review.
- Do not automatically delete review artifacts. Any review cleanup involving
  deletion must target exactly one non-symlink `working/<review-task>/`
  directory containing its review contract or incomplete marker, after all
  review agents have stopped. Delete nothing elsewhere.

## Review memory

`review_history/` travels with the chapters:

- `declined_edits/*.yml` — settled author no-change rulings, one file per root
  chapter source, with concrete reopening conditions. Their `evidence:` entries
  are frozen-tag references of the form
  `sta380_2026@final-summer-2026:<path>` into the private pre-split repo; the
  evidence files themselves are not public.
- `coverage.yml` — which source state received which review, so a later edit
  can use a Delta review instead of a fresh full-chapter review.

`tools/check_review_history.sh` enforces the consistency rules. A chapter-source
rename therefore requires three coordinated moves: a Quarto `aliases:` redirect,
the matching declined-edit-log rename, and the coverage-key rename.

## URL permanence

Chapter file stems are URL slugs and the site may be cited. Any chapter rename
requires a Quarto `aliases:` redirect entry, alongside the two review-history
renames above.

## Voice

The project follows Jared's general writing voice. Apply it to all
student-facing prose, including chapters, figure and table captions, and
appendix pages. Surface-specific skills add constraints; they do not replace
the voice pack.

The voice pack is external to this repository and is not public. Read the rules
and examples before drafting or revising prose, then use the checklist before
finalizing:

@/Users/jm75583/Dropbox/voice-pack/voice/JARED_VOICE.md
@/Users/jm75583/Dropbox/voice-pack/voice/JARED_CHECKLIST.md
@/Users/jm75583/Dropbox/voice-pack/voice/JARED_EXAMPLES.md
