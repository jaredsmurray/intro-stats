---
name: build-chapter-brief
description: Build an authoritative writer brief for a statistics textbook chapter or section from source artifacts such as slide decks, outlines, Markdown or Quarto notes, analysis scripts, data, figures, and older drafts. Use when the user asks to plan, brief, scope, or prepare a chapter-writing handoff; when examples must be substituted or empirically checked before drafting; or when matched book/no-book prompts are needed. Stop after producing the brief unless the user separately asks for a draft.
---

# Build Chapter Brief

Turn the author's source artifacts into an editorial and empirical contract for a chapter writer. Preserve the artifact's teaching logic while assigning narrow roles to the current book, voice pack, and style guides.

## Load the governing sources

1. Read the project instructions and applicable surface skill in full. For chapter prose, this includes `book-style` and Jared's three-file voice pack.
2. Read every user-designated source artifact in full. Treat slides, outlines, and notes as the content spine unless the user says otherwise.
   Classify HTML-commented sections, parked TODOs, and other author notes separately from active content; do not promote them into the brief without authorization.
3. Read analysis scripts and the data they use. Run read-only analyses needed to verify coefficients, sample sizes, diagnostics, figures, or candidate models.
4. Inspect only the current book chapters needed for continuity. Use `_quarto.yml` to identify them, but do not default to reading the whole book.
5. Put scratch analyses and temporary figures in `working/` or a temporary directory. Do not edit source artifacts while briefing unless requested.

## Assign authority by dimension

Do not give any source blanket authority. Record the following roles explicitly in the brief:

| Dimension | Authority |
|---|---|
| User changes and exclusions | The current user request controls. |
| Structure, flow, arguments, and example sequence | The designated source artifact controls. |
| Empirical values and model behavior | Data and analysis scripts control. |
| Prose voice | `JARED_EXAMPLES.md` controls, followed by the voice rules and applicable style skill. Existing book prose is not a voice precedent. |
| Prior coverage, notation, dataset reminders, anchors, and Quarto mechanics | Selected current book chapters control. |
| Final scope and output | The approved brief controls. |

If two sources conflict within the same dimension, resolve the conflict before handoff. Ask the user only when the choice would materially change the chapter.

When a current author-edited file and an older `working/` draft overlap, the current file controls. Use the older draft only to recover provenance or understand the change; never use it to overwrite newer prose or decisions.

Treat explicit substitution language as a scope decision, not a suggestion. If the user says to replace an example, use the examples or models in a named source, or substitute one dataset for another, the designated replacement source controls that slot and the displaced artifact material is out of scope by default. Plural language such as “models here” ordinarily authorizes all pedagogically distinct models supplied there; do not demote some to optional merely to simplify the brief. Retain displaced material only when the user expressly asks for it.

## Protect against book contamination

The current book is a continuity reference, not the chapter's content outline or prose model.

- Authorize only relevant chapters or sections.
- State what the writer may take from them: prior knowledge, notation, cross-references, dataset status, and established mechanics.
- State what the writer may not take from them: extra coverage, inherited examples, paragraph structure, repeated caveats, wordiness, or stylistic habits unsupported by the voice pack.
- Preserve established notation, reference categories, and dataset conventions from the authorized book material unless the user request, source artifact, or empirical result supplies a substantive reason to change them.
- Include a short `Do not import` list when nearby book material contains tempting but out-of-scope content.
- Require backward links where they save explanation, but never require a tour of everything the book has covered.

## Build the content specification

Extract the source artifact's ordered teaching moves before writing brief prose. For each move, record:

- the question or claim it advances;
- the example, data, model, or figure that carries it;
- what readers must interpret or conclude;
- the display that carries the teaching job: coefficient table, fitted equation, worked prediction, fitted curve, diagnostic, or no separate display;
- what prior material can be assumed;
- any substitution, omission, or extension requested by the user.

After applying substitutions, remove the displaced example from the progression, model list, figure catalog, and optional-material list. Do not manufacture an unresolved choice when the user's wording and designated source resolve it. Ask only about a genuine ambiguity that would yield materially different chapters.

Do not turn slide count into chapter structure mechanically. Preserve the progression, combine repeated slide beats, and retain deliberate repetitions only when they perform a teaching function.

## Verify the examples

Resolve empirical choices before handing off the brief.

- Confirm variable names, reference categories, filters, sample sizes, fitted equations, intervals, and plotted behavior.
- Inspect diagnostics rather than assuming a requested example works.
- If the user permits alternatives, test the smallest plausible set and document why the chosen specification remains.
- Distinguish values the writer must recompute from approximate values supplied as checks.
- Specify hidden implementation only as far as needed for reproducibility. Keep the rendered chapter programming-language agnostic when required.
- Catalog required figures by teaching purpose, source, placement, and allowed modifications.
- For each fitted model, state whether coefficients, uncertainty, fitted values, shape, or diagnostics are the teaching target. Require a regression table only when coefficients or uncertainty receive substantive interpretation; fits used for shape or diagnostics ordinarily need curves or diagnostic plots instead.

## Write the brief

Read [the brief template](references/brief-template.md) before creating a brief. Include only sections relevant to the task, but always include:

1. The output goal and unit of work.
2. An exact source allowlist and access rules.
3. The authority map.
4. Voice and style requirements by reference, not by copying the full guides.
5. Prior coverage and dataset status.
6. The ordered content progression.
7. Exact example and model specifications.
8. The visualization and diagnostic contract.
9. Quarto and language-independence conventions.
10. Verification and output requirements.

Separate `must`, `may`, and `do not` requirements. Give the writer freedom over sentences and paragraphing unless a specific construction carries essential mathematics or pedagogy.

## Support matched drafting conditions

Create a shared core brief plus access wrappers when the user requests book/no-book or model comparisons.

- The no-book wrapper must contain a compact continuity and mechanics catalog sufficient for a usable draft.
- The with-book wrapper must authorize only the smallest relevant current-book set.
- Keep data, models, figures, voice rules, and output requirements identical across conditions.
- Make clear that the experiment tests direct prose access after editorial context has been distilled; it is not a context-free condition.

## Audit the handoff

Before finishing, confirm that:

- every path exists and every access rule is internally consistent;
- the writer can execute the requested analysis without discovering a missing choice;
- source roles cannot be mistaken for blanket authority;
- the brief does not invite extra coverage from the current book;
- empirical check values match current data;
- the brief specifies outcomes without dictating ordinary prose;
- every requested replacement has fully displaced the old example unless retention was explicit;
- all supplied, distinct models covered by the user's request are assigned a clear role;
- every model's required display matches its teaching target, including explicit table inclusions or exclusions;
- established continuity choices are preserved or any change is justified;
- no “unresolved decision” is already answered by the request or its designated sources;
- the output path and final response contract are exact.

Stop after writing the brief. Report unresolved decisions and empirical surprises; do not draft the chapter unless the user asks for the next phase.
