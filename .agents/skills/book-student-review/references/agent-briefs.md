# Specialized agent briefs

## Contents

- Blind student trace
- Pedagogical and misconception reviewer
- Technical and continuity auditor
- Pedagogical structure editor
- Evidence verifier
- Revision editor
- Voice adversary
- Voice-pack maintenance auditor
- Targeted verifier
- Fresh student regression reader

Use these as role specifications, not as text that must be copied verbatim.
Give agents stable paths and the review-contract facts relevant to their role.
Do not leak earlier reviews, expected answers, or intended fixes into diagnostic
prompts.

Every role may read only its authorized inputs and must write only its assigned
artifact inside `working/<task>/`. Diagnostic, adjudication, drafting, voice,
and verification agents do not edit live project files or render the live
project. The orchestrator alone may apply an authorized, cleared candidate
after checking the frozen source hash and exact file scope.

## Blind student trace

### Inputs

- Frozen current rendered chapter. For bounded review, include the declared
  target plus its entry-context collar.
- Frozen rendered prerequisite excerpts.
- Reading situation.
- Exact prior-knowledge inventory.

### Withhold

- Author plans and objectives not printed in the chapter.
- Chapter source, hidden code, and commented prose.
- Existing review reports and todo notes.
- Deterministic-check output.
- Terminology ledger and calibration history.
- Other agents' findings.

### Task

Read the rendered chapter in order as a mature, diligent, overloaded student.
Maintain a running inventory of terms, symbols, datasets, and promises. Re-read
and follow available backward references before declaring a stall. Open a
prerequisite excerpt only after the target gives a reason to follow it; do not
browse the bundle for defects in advance. Attempt every exercise using only
material already available.

For bounded review, use the collar to decide whether the target receives the
setup a reader would actually have. Report findings only in the declared
target, except when missing or contradictory collar material directly breaks
the target's entry. Do not excuse a target stall on the assumption that
extraction may have hidden the setup.

For each candidate, report:

1. location;
2. first literal interpretation;
3. what you tried in order to recover;
4. where recovery failed or what unsupported inference made it work;
5. the likely false belief, lost connection, or task failure;
6. severity—only `blocker`, `major`, `moderate`, or `minor`—and confidence;
7. a repair objective in plain language.

Do not audit terminology for its own sake. Do not certify mathematical causes.
Do not infer from one stall that the chapter lacks the broader concept. State
what explanation or recovery support you did find before naming the residual
failure. Do not draft polished replacement prose. Report sections and displays
that held up in a compact coverage table. Do not flag the absence of code or
exercises; chapters are code-free and may contain no exercises by design.

## Pedagogical and misconception reviewer

Use only after the lean initial screen identifies a specific objective-bearing
teach-back or transfer failure whose cause remains unresolved. The prompt must
name that question without supplying the expected diagnosis.

### Inputs

- Frozen current rendered chapter. For bounded review, include the declared
  target plus its entry-context collar.
- Prior-knowledge inventory.
- Declared objectives, or objectives marked as inferred.
- Short teach-back and transfer probes, without the answer key.
- Frozen prerequisite excerpts needed by the probes or target callbacks.

### Withhold

- Existing reviews, todo notes, and author adjudication history.
- Other agents' findings.

### Task

Test whether the chapter changes what the reader can explain, recognize, and
do. For every section:

- identify the intended conceptual move;
- test whether examples and displays actually support it;
- list plausible novice rules or overgeneralizations;
- check whether definitions distinguish nearby concepts;
- when exercises exist, check whether they require only tools already taught;
- test whether callbacks and transitions preserve the throughline;
- distinguish necessary difficulty from avoidable cognitive load.

For bounded review, use the collar to test the target's entry and prerequisite
handoff, but keep proposed interventions within the target or its necessary
entry setup.

Answer the probes using only the chapter and prior knowledge. Diagnose the
likely misconception when an answer fails, not merely that the prose could be
clearer.

Report a problem only when you can name the likely misconception, failed task,
or missed objective. Suggest an intervention class—delete, clarify, change a
display, add contrast, restructure—not polished prose. Do not turn a failed
review probe into a recommendation that the chapter add an exercise; the probe
is an evaluation instrument unless the objective itself requires practice.

## Technical and continuity auditor

### Inputs

- Current rendered chapter and source.
- Prior boundary and objectives.
- Terminology ledger.
- Relevant project decisions and open cross-chapter plans.
- Deterministic-check results.
- Frozen prerequisite excerpts and their per-role completeness record.

### Task

Audit correctness and continuity independently of whether the text reads
smoothly. Reproduce computations and inspect data provenance when feasible.
Check:

- statements of statistical or mathematical fact;
- assumptions and scope conditions;
- model versus observed data;
- population, sample, parameter, statistic, estimate, and realized value;
- association versus causation;
- probability and inference semantics;
- units, denominators, transformations, and rounding;
- prose, table, figure, caption, and code agreement;
- notation and canonical terminology;
- prerequisites, back-references, forward promises, and downstream definitions.

Before free-form auditing, enumerate every terminology-ledger row whose
`first_defined_in` names the reviewed chapter. For each row, record whether the
canonical term is actually introduced and whether its symbol or concept is
glossed at first in-scope use. Treat a clean deterministic terminology check as
insufficient evidence for this first-definition audit. Include a compact
coverage table even when every row passes.

Also return three coverage tables even when they pass:

- **Input provenance**: every newly visible numeric or categorical assumption
  in a table or flagship example, its stated origin, and whether a reader can
  recover it. Reproducing arithmetic from an unexplained input is not a pass.
- **Bridge claims**: every objective-bearing “like,” “as in,” “same,” “again,”
  “unchanged,” “restated,” or equivalent callback, with both sides checked.
- **Literal instantiation**: every central verbal gloss applied to the
  example's actual support or displayed values.

For every issue, quote both sides of an inconsistency when applicable. Mark the
cause as suspected until reproduced. Return ledger proposals in a separate
section; do not assume chapter adjudication approves them.

If the review contract excludes ledgers, plans, or prerequisite artifacts,
mark the continuity audit limited. Do not infer that no prior owner or
cross-chapter decision exists.

## Blind continuity reader

Use only for a bounded Standard review whose contract marks continuity risk
`high`.

### Inputs

- Frozen target plus entry collar.
- Frozen prerequisite excerpts.
- Reading situation and exact prior-knowledge inventory.

### Withhold

- Source, objectives, checks, ledgers, plans, old reviews, other reports, and
  expected findings.

### Task

Perform a compact cue-triggered trace rather than a second general review.
Enumerate the target's explicit callbacks, analogies, quantity changes, and
imported assumptions. Follow only those cues into the frozen prerequisite
bundle. For each, report whether the target preserves the prior rule or makes
the change explicit. Test visible example inputs for recoverability from the
reader's supplied evidence. Report only broken or costly handoffs plus a pass
table. Stay under 1,000 words.

## Pedagogical structure editor

Use only when several verified local failures may share a structural cause.
Deep mode alone is not a trigger.

### Inputs

- Frozen rendered chapter.
- Prior-knowledge inventory.
- Objectives and probe answer key.

### Withhold

- Other reviews and expected findings.
- Author adjudication history.

### Task

Map each objective to the definitions, examples, displays, interpretation, and
practice that deliver it. Check dependency order, missing bridges, redundancy,
and whether a local-looking problem is really structural. Report a short
chapter map and only high-leverage changes.

## Evidence verifier

Use a separate agent for blocker or major correctness findings and every
quantitative claim changed by a revision. The orchestrator may perform this
role for moderate, minor, or mechanical findings only when the evidence is
directly reproducible. A deterministic check may serve as verifier when it
tests the exact claim.

### Inputs

- Deduplicated candidate packet.
- Source, render, data, and relevant prior/later chapters.
- Deterministic-check output.

### Task

Test the claimed cause without relying on reviewer confidence. For each
candidate:

- reread the full cited explanation and state what it already teaches
  successfully;
- reproduce calculations from reader-visible values and underlying values;
- distinguish estimate from truth, display rounding from computation, and
  source bugs from render bugs;
- inspect the original-resolution rendered figure before asserting what it
  shows;
- check provenance and current cross-chapter plans;
- classify as confirmed, reframed, unresolved, or not substantiated;
- state the narrowest claim the evidence supports;
- state the material student benefit of repair and the cost of no change.

Reject or reframe broad wording contradicted by the chapter's existing
treatment. An omitted derivation or qualification is not a misconception
without a failed objective-bearing student task.

Do not draft final prose.

## Revision editor

Use only for an explicit writing handoff or a revision too large for the
orchestrator to hold coherently. The orchestrator normally makes the integrated
revision directly.

### Inputs

- Verified issue packet.
- Selected dispositions.
- Complete relevant chapter context.
- `book-style`, voice pack, and checklist.
- Voice-pack examples.
- Approved terminology and cross-chapter decisions.

### Task

Write one integrated candidate patch under `working/<task>/candidate/`. Treat
reviewer wording only as diagnostic raw material. Prefer, in order when
suitable:

1. remove an unnecessary claim;
2. repair the computation, table, caption, or figure;
3. make a light, precise wording change;
4. add a short contrast or bridge;
5. restructure the example or section.

Preserve the author's scope. Avoid playful metaphors, slogan-like closers,
engineered examples, and explanations of distinctions the project has
deliberately chosen not to emphasize. Reuse suitable commented author prose.
Compute values inline when they depend on data or simulation.

When the orchestrator confirms a genuine ambiguity, draft two complete
alternatives from the supplied invariant. Draft a third only for a genuinely
different substantive or register choice. Do not generate cosmetic variants.

## Voice adversary

Use after the integrated revision has been applied and rendered. This must be
a different agent from whoever made the revision. Run it in parallel with the
targeted verifier.

### Inputs

- Compact repair table with approved dispositions and repair objectives.
- Exact applied old-to-new diff with enough local chapter context to assess
  flow.
- Current rendered chapter.
- `book-style`.
- The complete current `JARED_VOICE.md`, `JARED_CHECKLIST.md`, and
  `JARED_EXAMPLES.md`.
- Approved terminology and cross-chapter decisions relevant to the patch.

Withhold the orchestrator or editor's rationale, drafting notes, and
self-assessment.

### Task

Try to falsify the claim that the patch is both in Jared's voice and faithful
to the adjudicated repair. Check every changed sentence and the neighboring
paragraph for:

- violations of a voice-pack or `book-style` rule;
- generic LLM momentum, overexplaining, telegraphing, salesmanship, cute
  phrasing, or slogan-like compression;
- a locally smooth rewrite that changes scope, certainty, causal meaning,
  statistical meaning, or the approved teaching point;
- new redundancy, unearned transitions, or a closer that performs instead of
  teaching;
- a change that imitates the surface wording of an example without preserving
  the example's function and register.

Every blocking finding must cite the controlling rule, checklist item, or
example pattern and explain the consequence in context. Distinguish:

- `blocking`: a source-backed voice failure, meaning drift, unapproved scope
  change, or contradiction with the repair objective;
- `advisory`: a defensible preference that does not violate the pack;
- `ambiguity`: two reasonable versions differ on an author-specific or
  substantive choice that the supplied materials do not settle.

Advisory preferences cannot block clearance. Do not rewrite the whole passage
or introduce a third intervention strategy. Return:

```yaml
verdict: clear | revise | author-input
cycle:
blocking_findings: []
advisory_notes: []
ambiguities: []
```

Use `clear` only when there are no blocking findings. Use `author-input` only
for genuine uncovered ambiguity, not low confidence or a desire for a second
opinion.

Do not block on an unchanged baseline voice defect unless the candidate
worsens it, relies on it, or must alter it to meet the approved repair
objective. Keep such observations out of the active loop.

Do not edit the live chapter or candidate. Return one consolidated set of
blocking findings and the narrowest repairs. The orchestrator applies
determinate corrections after combining them with the targeted verifier's
results. Do not request another adversarial cycle for a local correction whose
meaning is fixed; direct verification is sufficient.

Before an ambiguity card reaches Jared, verify the alternatives against the
fixed invariant. Exclude any version that an existing rule clearly
disqualifies.

## Voice-pack maintenance auditor

Use at round close after the revision is voice-cleared and Jared has made any
final wording rulings. The orchestrator may perform this role.

### Inputs

- Voice-adversary findings from every cycle.
- Final cleared diff.
- Jared's accepted rewrites, rejected recommendations, overrides, and stated
  reasons.
- Current voice pack, checklist, and examples.
- Compact evidence from earlier review logs only when testing recurrence.

### Task

Check whether the round exposed a reusable gap or a misleading part of the
voice pack. Return `no-update` unless the evidence supports one of:

- a new or clarified bright-line rule;
- a testable checklist item;
- a contextual example and notes for a subtle judgment;
- a vocabulary addition or replacement;
- qualification or retirement of a conflicting example.

Do not infer a durable preference from one agent's taste. A one-round example
candidate requires an explicit Jared rewrite, acceptance, or explanation;
otherwise log the pattern for recurrence. Do not edit the pack. Prepare at most
three maintenance candidates for Jared, each with evidence IDs, the uncovered
gap, the proposed destination, and the smallest proposed change.

## Targeted verifier

### Inputs

- Before/after diff.
- Accepted issue packet and repair objectives.
- Revised source and current render.

For a bounded local revision, a compact repair table plus the exact changed
passages and immediate neighbors satisfies the issue-packet input. Do not
require the full diagnostic history when those materials establish the
invariant and verification task.

### Task

For each accepted issue, state whether the repair objective is met and cite the
revised evidence. Check neighboring prose and displays for contradictions
introduced by the patch. Reproduce all changed quantitative claims and perform
the local regression check in the same pass. Return pass, partial, or fail.

For a blocker or major repair, or any repair that changes a quantitative claim,
this role must be independent of the detector, compiler, revision editor, and
voice adversary.

## Fresh student regression reader

Use only when the revision restructures a central explanation or example,
changes a flagship display, or otherwise creates a plausible chapter-level
comprehension regression. Do not run it by default for local repairs.

### Inputs

- Frozen revised rendered chapter.
- Same reading situation and prior-knowledge boundary as the original blind
  student.

### Withhold

- Original findings.
- Revised source, diff, and intended fixes.
- Targeted verifier output.
- Author plans and adjudication.

### Task

Perform a compact in-order reread. Focus on conceptual handoffs, examples,
changed displays, and likely misconceptions. Report only major or moderate
friction plus any new problem created by the revision. A clean result is
allowed. Distinguish a pre-existing problem from one caused or worsened by the
patch; any repair-induced moderate-or-higher problem fails regression. Treat a
visual claim as provisional until a verifier inspects the actual rendered
image.
