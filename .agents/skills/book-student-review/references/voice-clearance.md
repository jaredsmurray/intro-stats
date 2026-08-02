# Adversarial voice clearance and voice-pack maintenance

## Contents

- Default policy
- Freeze the sources of voice truth
- Run the batched end-of-pass review
- Define blocking findings
- Escalate genuine ambiguity
- Record the loop
- Run the voice-pack maintenance hook

Use this reference after chapter findings and repair strategies have been
adjudicated. Voice review is one independent part of the batched review of the
finished revision; it is not a pre-application gate.

## Default policy

Set `voice_clearance_mode: required` for every revision that changes
student-facing prose. Set it to `optional` for a mechanical, code-only, or
display-only patch whose neighboring prose is unchanged. Use `waived` only at
Jared's direction, and record the reason. When optional clearance is not run,
record `optional-not-run`.

The voice adversary must be independent of the orchestrator or editor who made
the revision. Run it in parallel with the targeted verifier after rendering.

## Freeze the sources of voice truth

At the start of the revision loop, record hashes for:

- `JARED_VOICE.md`;
- `JARED_CHECKLIST.md`;
- `JARED_EXAMPLES.md`;
- the applicable surface skill, normally `book-style`.

Record the snapshot used by the adversary. If a voice source changed after the
revision was drafted, the adversary applies the current source and records the
version it used.

Treat the files in this order:

1. explicit project and surface rules;
2. the voice pack's non-negotiables and editing calibration;
3. contextual examples, interpreted by the function described in their notes;
4. the checklist as a final audit.

Examples guide judgment; they are not phrases to imitate mechanically. Draft
chapter prose and prior agent output are not voice precedents.

## Run the batched end-of-pass review

1. Apply the adjudicated integrated revision and render it.
2. Launch the voice adversary and targeted verifier together against that same
   source, diff, and render.
3. The adversary returns `clear`, `revise`, or `author-input`.
4. Consolidate all end-of-pass blockers before changing the source again.
5. The orchestrator applies determinate corrections and rerenders once.
6. Verify the exact corrections directly. Do not send them through another
   adversarial cycle unless they change substantive meaning or scope.

The adversary proposes the narrowest repair but does not edit the live chapter.
Advisory preferences do not trigger another pass.

## What may block clearance

A finding may block only when it identifies at least one of:

- a direct conflict with a cited voice-pack, checklist, `book-style`, or
  project rule;
- a generic prose pattern the pack expressly rejects, with local evidence;
- a change in statistical meaning, certainty, causal interpretation, scope, or
  the approved teaching point;
- an unadjudicated addition, deletion, or structural move;
- new repetition, overexplaining, or transition language that violates the
  pack's editing calibration;
- failure to resolve an accepted repair objective.

The adversary must identify the location, controlling source, consequence, and
narrowest repair objective. A preferred synonym, taste-based rhythm judgment,
or equally valid alternative cannot block on its own.

An unchanged baseline voice defect cannot block a scoped patch. Record it
separately only when useful. It becomes blocking for this loop only when the
patch worsens it, relies on it, or must change it to satisfy an accepted repair
objective.

Clearance does not require zero advisory notes. It requires zero blocking
findings and no unresolved ambiguity that changes meaning or depends on an
unrecorded author preference.

## Escalate genuine ambiguity

Stop and ask Jared when:

- reasonable phrasings encode different substantive claims or degrees of
  certainty;
- the voice sources conflict or do not cover a consequential register choice;
- a voice repair would violate an adjudicated teaching or technical objective;
- a proposed correction changes an adjudicated claim or intervention;
- the consolidated pass exposes several interacting structural failures that
  cannot be repaired locally.

Do not interrupt Jared for ordinary editing choices. Add at most three
voice-ambiguity cards to the next decision queue unless the ambiguity blocks
all further verification.

The revision editor drafts the alternatives from one fixed invariant. Before
Jared sees them, the voice adversary confirms that each preserves the
adjudicated meaning, represents a genuinely different choice, and contains no
unambiguous blocking violation. If the adversary can eliminate a version by
applying an existing rule, it is not an author ambiguity and should not appear
on the card.

Use this format:

```text
V1. [voice ambiguity · rule/example cited]
Invariant: What both versions must preserve.
A: First complete rewrite.
Tradeoff: One sentence.
B: Second complete rewrite.
Tradeoff: One sentence.
Recommended: A, because ...
Reply: V1A · V1B · V1W let the writer choose · or give wording.
```

Offer a third rewrite only when it represents a genuinely different
substantive or register choice. Do not present cosmetic variants.

After Jared rules, treat his wording and tradeoff as controlling. Apply it,
rerender if needed, and verify faithful implementation directly.

## Record the loop

Keep a compact record rather than the agents' full internal discussion:

```yaml
voice_clearance:
  mode: required
  source_hashes: {}
  editor:
  adversary:
  cycles: 1
  verdict: clear | clear-after-bounded-repair | clear-after-author-ruling | author-input | optional-not-run | waived
  blocking_findings_by_cycle: []
  advisory_notes: []
  author_rulings: []
  waiver_reason:
```

The final report states the verdict, cycle count, and any author ruling. Include
advisory notes only when they suggest a durable voice-pack gap.

## Run the voice-pack maintenance hook

At final adjudication, compare:

- every source-backed failure found by the adversary;
- revisions the adversary cleared but Jared rewrote;
- recommendations Jared rejected or modified, with his reason;
- disagreements that required author input;
- recurring drift patterns already visible in prior logs.

Classify the result as:

- `no-update`;
- `candidate-rule`;
- `candidate-checklist-item`;
- `candidate-example`;
- `candidate-vocabulary`;
- `candidate-qualify-or-retire`.

Use a high bar. A proposed rule or checklist item should be general,
operational, and supported by repeated adjudicated evidence, unless Jared
explicitly identifies a new bright-line preference. A single incident may
justify an example candidate only when Jared supplied or accepted the rewrite
or explicitly explained the preference. Agent-only evidence from one round is
logged for recurrence, not surfaced as a pack change. Do not add a candidate
when an existing source already settles the issue; instead record that the
workflow failed to apply the existing source.

Present the hook after the chapter decisions, separate from terminology-ledger
approval:

```text
Voice pack: 1 candidate

VP1. [candidate-example]
Evidence IDs: V1 author ruling; revision cycle 2.
Evidence: Jared replaced ... because ...
Gap: The current pack does not show ...
Proposed home: JARED_EXAMPLES.md, teaching register.
Smallest change: Add one before/after example with notes on ...
Recommended: hold until this pattern recurs.
Reply: VP1A add · VP1H hold · VP1N no change
```

When there is no candidate, write exactly:

```text
Voice pack: no update recommended.
```

Never update the voice pack automatically. If Jared approves a candidate,
apply it as a separate authorized change, preserve the evidence and reasoning,
and rerun the voice-pack checklist or validator before closing the maintenance
item. The chapter revision may close while a `VP` candidate is explicitly
pending or held because pack maintenance is a separate decision; do not label
the maintenance hook itself adjudicated until Jared rules.
