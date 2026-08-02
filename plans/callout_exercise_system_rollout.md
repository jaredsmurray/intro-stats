# Promote the callout, formula-detail, and inline-exercise system

Status: **infrastructure merged to `main`; chapter migration continues in
`todo/callout_migration_sweep.md`**

Decision date: 2026-07-30

The visual and behavioral design is accepted, and the tested infrastructure is
on `main`. Chapter-content migration is tracked separately so infrastructure
history and student-facing revision do not share one active plan.

## Accepted design

- **Numbered and referenceable:** Definition, Notation, Technical detail, and
  Exercise. Each has its own chapter-level counter.
- **Native, unnumbered Quarto callouts:** Key idea (`callout-note`),
  Interpretation (`callout-tip`), and Warning/Common mistake
  (`callout-warning`).
- **HTML:** Definition, Notation, and Exercise are static boxes with semantic
  icons. Technical detail starts collapsed. Formula details and solutions
  start collapsed and are opened individually.
- **PDF:** Boxes remain together and expanded. Formula details are omitted by
  default unless a block explicitly opts in. A separate full-formula profile
  includes all formula details. Exercise solutions are always included.
- **Styling:** wine Definition, slate Notation/Technical detail, teal Exercise;
  native callouts retain Quarto's standard colors. Native and custom boxes
  share one visual grammar.

## Authoritative scratch artifacts

The production candidate is:

`working/callouts_exercises/production_candidate/`

Read before implementation:

- `README.md` — authoring syntax, render modes, and promotion boundary.
- `UPSTREAM.md` — pinned versions and the three local extension changes.
- `tests/check.sh` — executable regression contract.
- `styles/callouts.css` — accepted HTML styling.
- `tex/callouts.tex` — accepted PDF styling and paragraph-spacing repair.

The broader decision record is:

`working/callouts_exercises/plan.md`

Do not promote generated `_output/`, `.quarto/`, `tmp/`, cross-reference cache
files, or the pilot's diagnostic profiles.

## Current infrastructure-branch progress

The isolated worktree was created from committed `main` at `4caa76c`. It now
contains the three extension patches, shared CSS and TeX, two PDF profiles,
project configuration, patch documentation, and a non-publishing regression
fixture. `tools/check_callouts.sh` passes for HTML, default PDF, and
full-formula PDF, and the latest PDF pages passed visual inspection.

No real chapter `.qmd` file has changed. Immediately before merge, the
untracked `data/` directory was manually copied into the independent worktree
and verified checksum-for-checksum (34 files). The untracked ERCOT prediction
artifacts required by `prediction_01_error.qmd` were copied and checked the
same way.

The promoted regression command passes for HTML, default PDF, and full-formula
PDF. A live full-book HTML render also passes for all 31 inputs. Both PDF modes
reach LaTeX compilation after successfully executing all 31 inputs, but the
live PDF build is blocked by the book's existing
`images/loess_construction.gif`: XeLaTeX cannot determine a bounding box for a
GIF. This is unrelated to the callout infrastructure and occurs before either
PDF profile can produce a live-book PDF. Resolve or conditionally substitute
that existing GIF before treating live full-book PDF output as a merge gate;
the focused two-chapter PDFs continue to enforce the formula
omission/inclusion contract.

## Scope boundary

Infrastructure promotion and chapter migration are separate changes.

The infrastructure change may modify configuration, extensions, styles,
render profiles, and regression fixtures. It must not rewrite chapter prose or
convert existing callouts.

Chapter migration is student-facing prose/markup work. It requires explicit
chapter scope, the `book-style` skill, normal chapter-edit authority, and
chapter-by-chapter review. Do not perform a blind global conversion of existing
`.callout-note` blocks.

## Phase 0 — preflight and change isolation

1. Create a dedicated Git worktree on `codex/callout-infrastructure`, based on
   the latest committed `main`. Put extension patches, styles, profiles,
   configuration, documentation, and the non-publishing regression fixture
   there. Do not copy uncommitted chapter work into it.
2. Inspect the live worktree. `_quarto.yml` and many chapters may contain
   unrelated work; preserve and rebase around it rather than overwriting it.
3. Record hashes or exact diffs for the three upstream files to be patched:
   - `_extensions/custom-numbered-blocks/cnb-3-crossref.lua`
   - `_extensions/custom-numbered-blocks/textcontainers/foldbox/foldbox.lua`
   - `_extensions/details/details.lua`
4. Confirm the installed extension declarations still match the candidate:
   - `custom-numbered-blocks` version `0.7.1-1`
   - `details` version `0.0.0-dev.2`
   - both require Quarto `>=1.7.0`
5. Run the scratch regression contract before promotion:

   ```bash
   cd working/callouts_exercises/production_candidate
   tests/check.sh
   ```

6. Stop and reevaluate rather than applying the saved patches if an extension
   has changed upstream or locally.

The infrastructure worktree may be completed and committed while parallel book
work continues in the original worktree. Do not add or convert callouts,
details, formulas, exercises, or solutions in any real chapter during this
phase. Once parallel work pauses and is committed, rebase the infrastructure
branch onto the updated `main`, resolve the small project-configuration merge,
rerun the regression fixture and full-book verification, and only then merge
the infrastructure branch.

## Phase 1 — promote the infrastructure

### 1. Patch the pinned extensions narrowly

Apply only the three documented candidate changes:

1. In `cnb-3-crossref.lua`, let level-one headings establish and reset the
   chapter prefix when a PDF book arrives as one Pandoc document.
2. In `foldbox.lua`, render appearances with `collapse: false` as static HTML
   blocks with Bootstrap icons; retain `<details>` for collapsible appearances.
3. In `details.lua`, preserve author-supplied classes other than `.details` on
   the generated HTML `<details>` element.

Do not replace the entire extension directories if the existing copies contain
newer or unrelated changes. Inspect the exact extension diff after patching.

### 2. Promote shared presentation files

Create durable project files from the accepted candidate:

- `styles/callouts.css`
- `tex/callouts.tex`

Keep the selectors semantic:

- `.formula-details`
- `.solution-details`

Do not restore the pilot's ID-prefix selectors such as
`details[id^="formula-"]`.

### 3. Merge configuration into the live project

Merge, rather than replace, `_quarto.yml`:

- retain the current `details`, `custom-numbered-blocks`, and `shinylive`
  filter order unless a fresh render demonstrates a required change;
- add the accepted `details` defaults;
- replace the unused legacy custom block declarations with the accepted
  Concept, Reference, and Practice appearances and the Definition, Notation,
  TechnicalDetail, and Exercise classes;
- preserve any live settings added by concurrent work;
- add `styles/callouts.css` to the HTML format without dropping the current
  theme or numbering settings.

The repository scan on 2026-07-30 found no live chapter uses of the configured
legacy `.Example`, `.Exercise`, or `.Note` custom classes. Repeat that scan
immediately before removing their declarations:

```bash
rg -n '^:{3,}.*\.(Example|Exercise|Note)\b' \
  --glob '*.qmd' --glob '!working/**' --glob '!archived_materials/**'
```

If any live use has appeared, preserve compatibility until it is migrated.

### 4. Add the two PDF profiles

Create:

- `_quarto-pdf-default.yml`
- `_quarto-full-formulas.yml`

Both should include `tex/callouts.tex`. The default profile inherits the global
`details` removal policy; the full-formula profile overrides non-interactive
details to `display: show`.

Before finalizing filenames and output locations, check `WORKFLOW.md`,
`ship.sh`, and cleanup rules so PDF builds do not interfere with the HTML
publishing path or leave root render junk.

Do not promote the pilot-only `pdf-patched` profile or `keep-tex: true`.

### 5. Promote the regression fixture

Choose durable, non-publishing locations consistent with project conventions,
for example:

- `tests/fixtures/callouts/index.qmd`
- `tests/fixtures/callouts/chapter-two.qmd`
- `tools/check_callouts.sh`

Adapt the candidate's test paths without weakening its assertions. The durable
check must cover:

- static Definition, Notation, and Exercise HTML;
- collapsible Technical detail HTML;
- semantic formula and solution classes;
- standard disclosure labels;
- separate counters restarting at 2.1 in chapter two;
- default PDF omission of an ordinary formula;
- per-block default-PDF formula inclusion;
- solution inclusion in the default PDF;
- full-formula PDF inclusion;
- successful HTML and two-profile PDF renders.

The fixture contains solutions and therefore must remain outside every
published resource or output path.

## Phase 2 — infrastructure verification

Run verification before editing any chapter:

1. Run the promoted regression command from a clean render state.
2. Inspect its exact HTML structure rather than relying only on screenshots.
3. Render both PDFs and extract text to confirm the inclusion contract.
4. Render representative PDF pages to PNG and inspect:
   - paragraph separation inside nested boxes;
   - page breaks for long Technical detail blocks;
   - border, title-band, and padding alignment;
   - formula and solution containment;
   - clipping, overlap, and glyph problems.
5. Render the live HTML book without chapter conversions and confirm that
   existing native callouts are visually unchanged.
6. Run the repository's normal deterministic checks and a full book build.
7. Inspect the final diff. At this phase it should contain infrastructure,
   tests, and configuration only—no chapter prose.

Because the change affects project-wide rendering and cross-reference
machinery, use a full-book build rather than `ship.sh --only`.

## Phase 3 — staged chapter migration

Begin only after Phase 2 passes and the infrastructure-only diff is accepted.

Phase 3 is now owned by `todo/callout_migration_sweep.md`, which incorporates
the completed whole-book inventory and the decisions from the first chapter
dry run. The outline below is retained as the original rollout record; follow
the newer todo when the two differ.

### 1. Inventory and classify

Create a chapter-by-chapter inventory of:

- existing native callouts;
- candidate definitions;
- notation declarations;
- technical asides;
- short inline knowledge checks and their solutions;
- formulas that are useful but optional for the main reading path.

Classification requires judgment. Do not infer that every existing
`.callout-note` is a Key idea, and do not turn ordinary explanatory prose into
a callout merely to use the new system.

### 2. Select a small first wave

Choose one or two chapters that collectively exercise:

- at least one Definition;
- at least one Notation or Technical detail;
- at least one optional formula;
- at least one inline Exercise with Solution;
- a cross-reference to a numbered block.

Prefer chapters already under active revision, and coordinate with their
outstanding todo/review plans to avoid conflicting prose edits.

### 3. Apply the accepted source syntax

- Use stable, descriptive identifiers.
- Add `.formula-details` and `.solution-details` explicitly.
- Give formula disclosures `summary="Details and formulas"`.
- Give solution disclosures `summary="Solution"`,
  `non-interactive-summary="Solution"`, and `display="show"`.
- Use a per-formula `display="show"` only when that formula belongs in the
  default PDF.
- Keep Technical detail collapsed by class default unless a block has a clear
  reason to override it.
- Do not number or identify native Key idea, Interpretation, or
  Warning/Common mistake callouts unless a later requirement changes.

### 4. Verify each migrated chapter

For each chapter:

1. Inspect the source diff for accidental prose or reference changes.
2. Render HTML and inspect open/closed states, icons, labels, nesting, and
   links.
3. Render default and full-formula PDFs and compare inclusion.
4. Check numbering and all new cross-references in the full book.
5. Run terminology, arithmetic, and other project checks applicable to the
   chapter.
6. Review the rendered chapter at narrow and ordinary HTML widths.

### 5. Expand only after the first wave is accepted

Record any taxonomy or styling adjustments before migrating additional
chapters. Once markup spreads through the book, class names and disclosure
labels should be treated as stable public authoring conventions.

## Phase 4 — documentation and maintenance

1. Add a concise authoring guide to the project's durable documentation,
   including copyable examples for all seven block roles, formula details,
   solutions, and PDF overrides.
2. Record the extension versions and three local patches near the vendored
   extensions or in the authoring guide.
3. Add the promoted regression command to the appropriate verification
   documentation or build/check entry point.
4. When upgrading Quarto or either extension:
   - check whether each local patch is now upstream;
   - remove obsolete patches rather than layering over them;
   - rerun the full regression fixture;
   - visually inspect HTML and PDF before accepting the upgrade.
5. After promotion is complete, move durable keepers out of
   `working/callouts_exercises/` and archive or remove the remaining scratch
   material according to `working/README.md`. Do not delete the scratch task
   until the promoted regression fixture and documentation are verified.

## Rollback plan

Keep infrastructure promotion in a focused commit or otherwise recoverable
change set. If full-book verification fails:

1. revert the project configuration, shared CSS/TeX, regression files, and
   three extension patches together;
2. do not leave chapters authored against partially installed classes;
3. retain the accepted scratch candidate for diagnosis;
4. identify whether the failure is HTML rendering, PDF rendering,
   cross-reference numbering, disclosure inclusion, or publishing integration
   before attempting a narrower correction.

## Completion criteria

Infrastructure promotion is complete when:

- the promoted regression command passes from a clean state;
- the live HTML book and both PDF profiles render;
- chapter-level counters and cross-references are correct;
- default and full-formula PDF inclusion differs exactly as designed;
- HTML and PDF visual inspection shows no layout defects;
- existing content is unchanged except for project-wide presentation effects;
- extension versions and local patches are documented; and
- the full infrastructure diff has been reviewed.

Book rollout is complete when:

- the approved chapter set has been migrated and verified;
- no accidental global conversion occurred;
- all new identifiers and references resolve in a full-book build;
- authoring documentation is durable and current; and
- the scratch task has been cleaned according to project policy.
