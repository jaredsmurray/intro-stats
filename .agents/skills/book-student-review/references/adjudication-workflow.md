# Streamlined author adjudication workflow

## Contents

- Prepare the decision queue
- Begin with a one-screen summary
- Batch low-judgment corrections
- Respect the write boundary and authorization
- Present judgment cards
- Handle structural choices
- Separate diagnosis, strategy, and wording
- Maintain adjudication state
- Close the round

The goal is to minimize Jared's decision burden without hiding uncertainty or
making substantive choices for him.

## Prepare the decision queue

Adjudicate only deduplicated, verified findings. Keep raw agent reports and
full context in the task directory.

Before sorting findings into the queue, read `prior-rulings.md` and the
declined-edit log whose filename matches the current root chapter source. Close
a semantic match as `previously-adjudicated` unless the card can name the
materially changed source, objective, evidence, teaching purpose, or downstream
use that warrants reopening it.

Sort actionable findings into five classes:

1. **Batch corrections**: confirmed arithmetic, reversed labels, broken
   references, obvious terminology violations, and similarly low-judgment
   repairs. Do not include substantive prose choices merely because the
   reviewer is confident.
2. **Judgment calls**: real misconception or clarity problems with a local
   intervention choice.
3. **Structural choices**: deleting, moving, expanding, or redesigning an
   example or section.
4. **Cross-chapter decisions**: issues whose correct repair changes
   prerequisites, terminology, notation, or several chapters.
5. **Ledger decisions**: proposed terminology rows. Run these separately from
   chapter adjudication.

Present confirmed errors before optional improvements. The author interface
has only two lanes: one correction batch and decision cards.

Put an item in the correction batch only when the defect is confirmed, every
reasonable editor would make essentially the same repair, and the repair is
worth making because it affects correctness, recoverability, or normal reading.
Use a card whenever reasonable repairs differ in meaning, pedagogy, scope, or
structure. Severity alone does not choose the lane.

If an observation would produce no meaningful student benefit, omit it from
structured findings and the final report. The raw agent report is sufficient;
do not create a “logged, no-action” record or mention a suppressed count. Keep
it only when a recurring pattern supports an actionable deterministic check or
policy proposal. A fully recoverable cosmetic or render defect with no
conceptual effect is not batch-worthy merely because its fix is obvious; omit
it unless the same display is already authorized for revision. Never suppress
an item merely because it is minor or because the queue is full.

## Begin with a one-screen summary

State:

- whether the chapter is broadly sound;
- the number of confirmed errors, misconception risks, structural choices,
  holds, and mechanical items;
- the three highest-leverage decisions;
- whether a cross-chapter plan blocks any local repair.

Do not begin with detailed evidence.

## Batch low-judgment corrections

List each correction in one line:

```text
B1. Reverse the loan-status labels so the prose matches the coding.
B2. Recompute the displayed subtraction from reader-visible values.
B3. Repair the broken Section 12.4 reference.
```

Then ask for one decision:

```text
Recommended: approve all three. Reply “batch yes” or name exceptions.
```

Never put a debatable explanation, example, or wording choice into this batch.
Apply standing-authorized typo fixes without reasking, but list them in the
final change summary.

## Respect the write boundary and authorization

Review and adjudication write only inside `working/<task>/`. Keep decisions,
reports, and candidate patches there. Do not edit the chapter merely because a
finding is verified or has entered the decision queue.

Apply a candidate to named project files only when:

- Jared accepts the relevant finding or intervention;
- Jared delegates implementation to the revision editor; or
- the repair fits the standing mechanical waiver.

The standing mechanical waiver covers spelling, punctuation, duplicated
words, unmistakably broken references, and markup or parse repairs with one
reasonable interpretation and no change in meaning or computation. It does
not cover arithmetic, numeric values, statistical claims, terminology,
explanations, examples, structure, or code repairs that can change behavior.
List every waiver-applied change in the final summary.

Before application, compare the live source hash with the frozen source hash.
If they differ, stop and rebase the candidate onto the parallel work. After
application, inspect the exact diff and reject edits outside the authorized
files or adjudicated scope.

## Present judgment cards

Show at most three cards before pausing. Keep each under 120 words. Every card
must distinguish the chapter's successful existing treatment from the narrow
residual failure and state the cost of no change:

```text
4. [major · confirmed · misconception]
Already works: The example clearly distinguishes mean return from volatility.
Residual problem: The age-based 401k sentence gives no benefit that would make
the more volatile stock attractive.
Student consequence: A reader may infer that volatility itself raises
long-run growth.
Recommended move: Delete the age-based 401k sentence.
Other reasonable move: Expand the example with the missing return/horizon
tradeoff.
Cost of no change: Moderate; the unsupported investment rule survives.
Reply: 4A accept recommendation · 4W let the writer choose · 4H hold ·
4N no change
```

Link the finding number to its full evidence and context. Do not paste the
enclosing paragraph unless Jared asks for it.

Accept these reply forms:

- `A`: accept the recommended intervention;
- `W`: accept the diagnosis and delegate implementation to the revision editor;
- `H`: hold for evidence or later work;
- `N`: no change;
- free-form wording or another option.

Natural-language rulings always override the shorthand.

Recommend `no change` when the chapter already meets the objective and the
proposed addition would mainly add completeness, formalism, or reviewer
reassurance. Do not force Jared to choose among repairs for a finding the
compiler would not itself recommend changing.

## Handle structural choices one at a time

For a structural or cross-chapter issue, present:

- the root problem;
- affected chapters or objectives;
- two or three genuinely different strategies;
- the recommended strategy and tradeoff;
- the plan owner and unblock condition if deferred.

Do not mix a structural decision into a batch of sentence edits.

## Separate diagnosis, strategy, and wording

Normally ask Jared to decide whether the problem is real and which intervention
class to use. Let the revision editor draft the exact prose afterward.

Request exact-wording approval before applying only when:

- probability or inference semantics are sensitive;
- a mathematical definition is changing;
- the wording itself was Jared's condition of acceptance;
- reasonable phrasings encode different substantive claims.

Otherwise, apply the selected strategy, verify it, and report the resulting
diff concisely.

## Maintain adjudication state

After every reply:

1. append the ruling and reason to `decisions.yml`;
2. update the corresponding decision status in `findings.yml`;
3. regenerate or synchronize `student_review.md` from structured state;
4. record accepted, modified, held, or no-change;
5. quote Jared's reasoning when it establishes a durable rule;
6. after Jared authorizes the plan item, route cross-chapter work into `todo/`
   with an owner and unblock condition; otherwise stage it in the review
   directory;
7. keep ledger approval pending unless explicitly granted.
8. when Jared declines an edit, append the settled ruling and a concrete
   reopening condition to the current source's durable declined-edit log.

Resume with the next unresolved card. Do not repeat decided findings.

## Close the round

After applying and verifying accepted work, report:

- what changed, grouped by chapter section;
- adversarial voice-clearance status and cycle count;
- deviations from the recommended strategy;
- verification failures or new regressions;
- held and plan-owned items;
- the separate ledger decision, if any.

Do not ask Jared to reread every accepted sentence. Surface only changes that
depart from his ruling or require a new choice.

Then run the voice-pack maintenance hook in `voice-clearance.md`. Keep it
separate from chapter and terminology decisions. Report either:

```text
Voice pack: no update recommended.
```

or at most three `VP` cards. Each card identifies the adjudicated evidence, the
gap in the current pack, the smallest proposed addition or edit, and one
recommendation. Accept `VP1A`, `VP1H`, or `VP1N`; a natural-language ruling
overrides the shorthand.

Do not modify the voice pack without explicit approval. A maintenance
candidate is not another request to adjudicate the chapter revision.
