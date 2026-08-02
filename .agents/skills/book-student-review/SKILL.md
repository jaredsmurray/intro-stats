---
name: book-student-review
description: >
  Diagnose, verify, revise, and recheck a statistics textbook chapter using
  specialized agents and deterministic project checks. Use for student review,
  confused-reader testing, misconception prevention, technical and numeric
  auditing, clarity improvement, chapter revision, or a full review-and-repair
  pass on a root .qmd chapter. Produces an evidence-backed issue packet before
  drafting changes, separates student friction from technical diagnosis, and
  adversarially checks revised prose against Jared's voice pack before
  verifying the rendered revision with a fresh reader.
---

# Review and revise a textbook chapter

Use staged specialization. Do not ask every agent to diagnose, verify, and
rewrite the chapter independently. The workflow has three distinct questions:

1. What will a capable but overloaded student misunderstand or fail to recover
   from?
2. What is technically, numerically, or terminologically wrong?
3. What is the smallest coherent revision that resolves the verified problem
   without creating a new one?
4. Does that revision still sound like Jared, rather than like a capable
   generic editor?

Keep the evidence from those questions separate until compilation.

## Choose the review mode

- **Lint**: Run deterministic checks only. Use for mechanical screening.
- **Delta**: Run one blind student trace and the technical auditor on a changed
  section plus its dependencies. Use only for a follow-up or after a localized
  revision, not for a section's initial diagnostic review.
- **Standard**: Run one blind student-friction trace and one technical audit in
  parallel, alongside deterministic and visual checks. This is the default for
  an initial chapter or section review.
- **Deep**: Use the same lean initial screen, but broaden the technical audit's
  continuity and downstream checks. Add a pedagogical, structural, continuity,
  or second-reader role only after the initial evidence identifies a specific
  unresolved risk that role can test. Deep means broader evidence, not more
  reviewers by default.

Do not advertise a multi-chapter Unit mode until its cross-chapter role,
artifact schema, and stopping rules are defined. Review dependent chapters in
prerequisite order using the modes above and promote shared issues to an owned
cross-chapter plan.

State the review stage (`initial`, `follow-up`, or `post-revision`), selected
mode, and action scope in the review contract. The action scope is
`review-only`, `propose-revisions`, or `apply-and-verify`. The user's request
determines whether source edits are authorized; a request to review does not
itself authorize revision.

## Keep author work and background review in separate lanes

Maintain one **author lane** and at most one **background review lane**:

- The author lane contains one chapter's ready decisions, revision approval,
  or verification. Respond to Jared immediately; never wait for a background
  role before presenting work that is already ready.
- The background lane contains one other chapter's lean diagnostic screen.
  When its initial reports finish, let them wait for skeptical compilation.
  Do not automatically launch optional follow-up roles.

Use parallelism to shorten independent evidence collection, not to maximize
agent occupancy. Preserve at least one slot for targeted verification or the
active author chapter when capacity is limited. Report ready decisions as soon
as they clear compilation; do not hold them for wave-level synchronization.

Before dispatching concurrent work, read
`references/parallel-orchestration.md`. Its slot budget, bounded-wait rule,
small-brief rule, and immediate-delivery rule are mandatory. Review agents do
not spawn follow-up agents.

## Establish the review contract

Create `working/<task>/review_contract.yml` before launching agents. Use
`scripts/prepare_review_package.py` to freeze the source, rendered page, and
discoverable local assets in `working/<task>/input/`. Give the helper a new,
nonexistent task slug directly under `working/`; it refuses existing,
non-direct, symlink-escaping, and out-of-project destinations. It never merges
or recursively cleans output. After initialization, a failed build leaves
`.incomplete` in place. If marker initialization itself fails, the helper
leaves the new empty directory and reports it as incomplete. Report that path
and do not reuse or automatically delete it. Do not assemble the package by
hand when the helper can do it. Prevent renders and source edits until all
diagnostic agents finish.
Record:

- chapter source and rendered HTML paths;
- source hash and rendered-artifact hash;
- how render freshness was established;
- reading situation: pre-lecture or post-lecture;
- exact prior-chapter boundary and a compact inventory of relevant knowledge;
- chapter objectives, inferred from the chapter when the author has not
  supplied them and marked as inferred;
- optional companion artifacts and cross-chapter decisions already owning part
  of the chapter;
- exact scope anchors and, for Delta mode, whether the basis is a before/after
  diff, an author-targeted passage, or a bounded current section;
- for a bounded review, an entry-context collar that includes the chapter
  opener or preceding transition needed to judge whether the target begins
  coherently; keep findings constrained to the declared target unless the
  collar itself invalidates an in-scope dependency;
- review mode, authorized actions, and exclusions;
- voice-clearance mode: `required`, `optional`, or `waived`, with a reason for
  any waiver;
- visual-bundle status and any deliberately limited continuity inputs;
- for a bounded review, exact frozen rendered excerpts behind every in-scope
  back-reference and inherited assumption that determines a flagship example;
- continuity-input status per role and prerequisite access (`cue-triggered`,
  `full`, or `none`);
- continuity risk, marked `high` with a reason for several objective-bearing
  callbacks or multiple materially imported assumptions;
- deterministic-check results and any known render limitations.

Voice clearance is required by default whenever the proposed or applied patch
changes student-facing prose. It may be optional for a purely mechanical,
code-only, or display-only patch. When optional clearance is not run, record
`optional-not-run`. Waive it only at Jared's direction and record why.

Do not run reviewers against live `_book/` while a render is active. Prefer a
successfully rendered artifact from the current source state. If freshness
cannot be established, label the review `source-reconstructed`; do not claim a
student-experience or visual review. Reconstructing the display is a technical
fallback, not a substitute for the blind reader role.

A source-reconstructed Delta, Standard, or Deep run is necessarily `partial`.
Skip the blind and pedagogical roles rather than giving them source disguised
as a rendered student artifact. Resume those roles only after freezing a
current render.

### Enforce phase write boundaries

During diagnosis and adjudication, every agent may read the project but may
write only inside the exact `working/<task>/` review directory. This includes
raw reports, deterministic-check output, structured state, decisions, and
candidate patches. Do not render the live project, execute chapter code that
writes figures, caches, or data elsewhere, or modify chapters, ledgers, plans,
generated assets, or the voice pack during these phases.

If no current render exists, mark the student-facing review partial or perform
a separately declared preflight render before freezing inputs. Do not hide a
write-producing render inside diagnostic review. Use read-only deterministic
checks and redirect their output into the review directory.

Adjudication records decisions; it does not itself authorize unrelated edits.
Apply a candidate to named project files only after Jared approves or delegates
the relevant disposition, or under the standing mechanical waiver in
`references/adjudication-workflow.md`. Keep revision plans, diffs, independent
review reports, and clearance records inside `working/<task>/`; only the
orchestrator edits live project files.

The orchestrator and technical auditor read the source as well as the rendered
chapter. The blind student does not. The rendered artifact shows what the
student sees; the source reveals inline computations, hidden setup, commented
author prose, and whether code is visible.

For bounded student-facing reviews, freeze one rendered artifact containing
both the target and its entry-context collar. Do not give the student a
target-only fragment that makes missing setup look as though it might have
been omitted by extraction. Mark the target start separately in the contract
and prompts; use the collar only to evaluate entry continuity, not to expand
the finding scope. Freeze prerequisite excerpts with
`--prerequisite-excerpt LABEL RENDERED_HTML START_ID END_ID`; do not assemble
them by hand after package creation.

## Run deterministic checks first

Run the applicable project checks before spending agent attention:

```bash
./tools/check_terms.sh --all <chapter.qmd>
Rscript tools/check_number_consistency.R <chapter.qmd>
Rscript tools/check_rounded_arithmetic.R <rendered-chapter.html>
```

Treat the two numeric checks as complementary, not as old and new versions of
the same check:

- `check_number_consistency.R` reads source. It finds inconsistent display
  precision for repeated formatter expressions and reconstructible values
  within a figure. It does not evaluate the chapter's displayed arithmetic.
- `check_rounded_arithmetic.R` reads rendered HTML. It evaluates the narrow
  class of explicit numeric equations and intervals that it recognizes. It
  does not find precision drift across displays or certify arithmetic it did
  not recognize.

Run the source check before diagnosis. Run the rendered check only against an
artifact whose relationship to the frozen source is known. Record each check's
output separately, including the source files scanned and the rendered
checker's statement count. A clean result means no finding within that
checker's recognized scope; it does not mean the chapter's numbers are fully
audited. Route unrecognized cases—such as arithmetic split across displays,
numeric labels baked into images, or prose whose direction depends on a
computed sign—to contextual technical or visual inspection.

Also use the render to check cross-references, structural warnings, broken
encoding, and obvious corrupted prose. Preserve the output in the task
directory. Deterministic findings enter the technical evidence stream; do not
show them to the blind student reader.

For a bounded review, retain whole-chapter check output but route into the issue
packet only findings inside the frozen scope or findings that invalidate an
in-scope dependency.

When the same confirmed error class recurs, prefer a reliable project check to
asking future agents to rediscover it.

## Run a lean parallel screen

Launch one blind student-friction reader and one technical auditor together,
alongside the deterministic and visual checks. Read
`references/agent-briefs.md` before constructing the prompts. Do not fill every
available agent slot merely because it exists.

### A. Blind student trace

Give only the frozen rendered artifact, reading situation, prior-knowledge
inventory, and the frozen prerequisite bundle. The reader may open a
prerequisite excerpt only when following a back-reference, analogy, or
inherited example assumption encountered in the target. Withhold source,
objectives, author plans, deterministic-check output, existing review reports,
todo notes, calibration history, and other agents' work.

Require an in-order comprehension trace. For each candidate problem, record the
student's first interpretation, recovery attempt, and likely retained
misconception. Do not ask this agent to certify the cause or draft polished
replacement prose.

### B. Technical and continuity audit

Give the source, rendered artifact, chapter objectives, prior boundary,
cumulative terminology ledger, relevant project decisions, and deterministic
check output. Check:

- mathematical and statistical correctness;
- model/data, population/sample, parameter/statistic, and causal distinctions;
- units, scaling, displayed arithmetic, and prose/display agreement;
- definitions, notation, terminology, and cross-chapter continuity;
- every terminology-ledger row whose `first_defined_in` names the reviewed
  chapter: confirm that the canonical term is actually introduced, and check
  symbols and named concepts at their first in-scope use even when the
  deterministic term checker passes;
- data and computation provenance;
- figure and table claims;
- forward references, promised explanations, and dependent later chapters.

Require three compact ledgers before free-form findings: **input provenance**
for assumptions in tables/flagship examples (arithmetic consistency is not
provenance); **bridge claims** testing objective-bearing callbacks against
frozen prerequisites; and **literal instantiation** applying each central
verbal interpretation to the example's actual support or values.

Report suspected causes as hypotheses until reproduced. Keep proposed ledger
changes separate from chapter findings.

After the initial screen, add one specialized role only when the compiler can
state the unresolved question it will answer:

- use a pedagogical reviewer when an objective-bearing teach-back or transfer
  task failed but the cause remains unclear;
- use a structure editor when several verified local failures may share a
  dependency-order or example-design cause;
- use a blind continuity reader when a bounded target imports several
  prerequisite claims that the initial reader could not recover;
- use a second blind reader only to test whether a central stall replicates
  under a meaningfully different reading method.

These roles are evidence-triggered and optional. Do not require all of them for
a Deep review, and do not treat same-prompt agreement as verification.

Keep diagnostic output bounded:

- Delta: at most 1,000 words per role.
- Standard: at most 1,500 words per role.
- Deep: at most 2,000 words per initial role; optional follow-up roles stay
  under 1,000 words and answer only their triggering question.

Use one compact evidence card per candidate. Prioritize blocker, major, and
moderate findings; put minor mechanical observations in a one-line appendix.
Complete exactly one pass and do not spawn additional reviewers from within a
diagnostic role. If the cap is reached, list unreported locations rather than
silently implying full coverage.

## Compile an evidence packet

Preserve the raw reports. The orchestrator then creates one deduplicated issue
packet using `references/finding-schema.md`.

Compilation is a skeptical falsification pass, not a summary or vote count.
Before promoting any candidate into structured findings, reread its cited
chapter passage and inspect every implicated table or figure directly. Require
the compiler to answer:

1. What does the chapter already teach successfully at this location?
2. What exact residual student task or interpretation still fails?
3. What reader-visible evidence causes that failure?
4. Does the claimed cause survive direct reproduction?
5. Would the smallest repair create material student benefit?
6. What is the cost of leaving the chapter unchanged?

If the chapter already supplies the claimed missing explanation, reframe the
candidate to the narrow residual gap or reject it. An omitted derivation,
terminological nuance, or advanced qualification is not a misconception merely
because it could be added. Promote it only when a declared objective or
documented recovery failure depends on it.

Never promote a visual finding without inspecting the actual rendered image at
its original resolution. Never describe an isolated technical bridge as though
the chapter lacks the broader concept it already teaches.

Use these files as the authoritative state:

- `review_contract.yml`: immutable scope, inputs, mode, and authorization;
- `findings.yml`: deduplicated evidence and verification;
- `decisions.yml`: Jared's rulings and reasons;
- `run_status.yml`: required roles, role state, and phase completion.

Treat `student_review.md` as a human-readable projection of those files, not a
second state store. When they conflict, repair the report from the structured
state.

Track every required role as `pending`, `complete`, `failed`, or `timed-out`.
Do not label a packet complete while a required role is missing. Preserve
finished work, list the missing evidence, and mark the run `partial`. If a late
report arrives after compilation, require an explicit recompile.

Separate these fields:

- observed symptom;
- student consequence or misconception;
- reviewer hypothesis about the cause;
- independently verified cause;
- repair objective;
- possible intervention size.

Do not rank primarily by agent count. Rank by:

1. severity of the false belief or blockage;
2. strength and reproducibility of the evidence;
3. importance to the chapter's objectives and downstream learning;
4. likelihood that the student can recover unaided.

A single documented recovery failure may outrank a replicated wording
complaint. A technically clean passage may still need revision when it reliably
causes a misconception.

Agent agreement is a routing signal only. Correlated reviewers can replicate
the same overreading, so agreement never replaces the six-question compiler
gate.

## Verify before drafting

Independently test every factual, numeric, data, source/render, and figure-reading
claim. Mark each candidate:

- `confirmed`;
- `reframed` — the friction is real but the proposed cause was wrong;
- `unresolved` — more evidence or author judgment is needed;
- `not substantiated`.

Inspect the source for authored-but-disabled prose before generating a new
explanation. Check whether a current todo or cross-chapter plan already owns the
issue.

Do not turn an unverified reviewer claim into replacement text.

Verification must test the narrow residual claim produced by skeptical
compilation, not the reviewer's broadest wording. When the chapter already
teaches the central concept, explicitly record that strength and verify only
the alleged remaining failure.

For blocker or major correctness findings, and for every quantitative claim
that a revision changes, assign a verifier who did not detect or compile the
finding. The orchestrator may verify moderate, minor, or mechanical claims
only when the evidence is directly reproducible. A deterministic check may
satisfy independence when it tests the exact claim.

## Choose dispositions before writing prose

Before constructing the author queue, read
`references/prior-rulings.md` and the durable declined-edit log matching the
current root chapter source basename. Keep these logs out of initial diagnostic
prompts. Do not reopen an active author ruling without identifying materially
changed prose, objectives, evidence, teaching purpose, or downstream use.

For each verified issue, recommend one disposition:

- accept as diagnosed;
- accept with a reframed cause;
- delete the low-value claim;
- repair a computation, table, caption, or figure rather than the prose;
- add a local clarification;
- restructure the explanation or example;
- escalate to a cross-chapter plan;
- hold for provenance or research;
- true but intentionally omitted as too fine a point;
- out of scope;
- not substantiated;
- promote to a deterministic policy or check.

Do not present a recommendation as an author decision. If author adjudication
is required, present the diagnosis and intervention choice before spending
tokens on polished prose. Record the adjudicated disposition and adjudicator
separately. Keep ledger approval a separate decision.

Preserve raw reports, but put only actionable findings into structured state.
The author queue has two lanes:

1. **Correction batch**: the defect is confirmed, every reasonable editor
   would make essentially the same repair, and the repair is worth making.
2. **Decision card**: reasonable repairs encode different choices about
   meaning, pedagogy, scope, or structure.

If repair would produce no meaningful student benefit, omit the observation
from structured state; the raw report is already the audit trail. A fully
recoverable cosmetic/render defect with no conceptual effect is not a batch
item merely because its fix is obvious. Retain such a pattern only when
recurrence supports an actionable check/policy or the display is already
authorized for revision. Never omit solely because severity is minor or the
queue is full.

Treat `no change` as a substantive recommended disposition whenever the
chapter's existing treatment meets its objective and the proposed addition
would mainly add completeness, formalism, or reviewer reassurance.

## Make adjudication easy for Jared

Before presenting findings for decision, read
`references/adjudication-workflow.md`. Never hand Jared raw agent reports or
ask him to adjudicate several competing rewrites.

Present:

1. a one-screen verdict and count by decision class;
2. one batch of verified, low-judgment corrections;
3. at most three judgment cards at a time;
4. structural or cross-chapter choices one at a time;
5. terminology-ledger decisions in a separate pass.

Each card states what the chapter already does, the narrow residual problem,
the demonstrated student consequence, verification status, one recommendation,
and the cost of leaving it unchanged in under 120 words. A card may recommend
no change. Accept terse replies such as `batch yes; 4A; 5H; 6 no change` as
well as natural-language rulings.

Log each decision and Jared's reasoning immediately. Do not require approval of
exact prose before revision unless probability/inference semantics, a
mathematical definition, or Jared's ruling makes wording itself the decision.
When Jared declines an edit, append the durable ruling to the chapter's
`review_history/declined_edits/<source-basename>.yml` log using
`references/prior-rulings.md`. Do not log compiler-rejected observations as
author decisions.
After revision, return a compact change summary and surface only deviations,
failed verification, or genuinely new decisions.

## Make one integrated revision

After dispositions are known, the orchestrator makes one integrated patch.
Use a separate revision-editor agent only when Jared explicitly requests a
handoff or the revision is too large for the active task to hold coherently.
Never ask competing writers for independent chapter rewrites.

Prefer the lightest repair that fully resolves the verified problem. Consider
deletion, a display change, or a structural source fix before adding
explanatory prose. Do not introduce engineered examples merely to exercise a
formula. Compute changing values inline rather than hardcoding them.

Before applying, compare the live source hash with the frozen source hash. If
they differ, rebase the revision rather than overwriting parallel work. Apply
only the adjudicated files and scope, then inspect the complete diff.

## Render once, then batch independent review

Run source checks in parallel, render the integrated revision once, and inspect
changed displays at original resolution. For isolated chapter verification,
use `quarto render <chapter> --no-clean`; project cleanup is not part of
chapter review.

After the current render exists, launch these independent roles together:

1. A voice adversary checks the complete applied diff and neighboring prose for
   voice and semantic fidelity.
2. A targeted verifier checks every accepted repair objective, changed
   calculation, and display against the current source and render.
3. Add a fresh student regression reader in the same batch only when the
   revision restructures a central explanation or example, changes a flagship
   display, or creates a plausible chapter-level comprehension regression.

These roles review the same finished revision in parallel. Voice review never
blocks application or rendering, and verification never waits for voice
clearance. Give each role a compact repair table and exact changed context; do
not make it reread the full review history.

Consolidate their blocking findings once. The orchestrator directly applies
determinate local corrections, rerenders once if needed, and verifies those
specific corrections. Do not create agent-to-agent micro-cycles. Ask Jared
only when a finding exposes a substantive ambiguity or conflicts with an
adjudicated decision. Read `references/voice-clearance.md` for the blocking
standard and maintenance hook.

Rendering and expected generated-output writes occur only here, after edit
authority exists. They are verification effects, not diagnostic-review writes.
Do not treat a request for review-only or propose-revisions scope as authority
to render into live project outputs.

The targeted verifier combines repair-objective checks with neighboring
regression checks and knows what changed. A selectively required fresh student
does not. For local repairs, do not rerun a blind full-chapter review merely to
complete a role list. For Delta mode, reread the changed section and its
conceptual dependencies.

Report completion immediately when the batched checks pass. Do not append
generic skill tests, cleanup, package maintenance, or future-chapter work to the
critical path.

Stop according to action scope:

- **Review-only:** required diagnostics are complete or the packet is marked
  partial; candidates are verified as far as the evidence permits; coverage and
  limitations are explicit; recommendations are clearly non-adjudicated.
- **Propose-revisions:** satisfy review-only criteria, then record selected
  intervention strategies and draft proposals without applying them. Any
  proposed student-facing prose must complete the same adversarial voice
  clearance required for an applied revision.
- **Apply-and-verify:** every blocker and major issue has an adjudicated
  disposition; every factual claim in an applied fix is verified; the revised
  render is current; deterministic checks pass or have an explicit waiver;
  every student-facing prose change has cleared the adversarial voice review
  or has an explicit Jared ruling or waiver;
  accepted repair objectives pass targeted verification; any required fresh
  reader finds no repair-induced blocker, major, or moderate problem; any
  pre-existing moderate finding is explicitly held; and remaining dependencies
  are recorded in `todo/` with an owner and unblock condition.

## Close with a voice-pack maintenance check

At final adjudication, review the voice adversary's findings, Jared's rewrites
or overrides, and any recurring drift exposed by the loop. Use the maintenance
hook in `references/voice-clearance.md`.

Report either `Voice pack: no update recommended` or a short, separate queue of
voice-pack candidates. Do not silently edit the voice pack. Prefer a contextual
example for a one-off subtle judgment; propose a rule or checklist item only
when the evidence is general, testable, and not already covered. If Jared
accepts a candidate, record the destination file and exact proposed change,
then update and recheck the pack as a separate authorized action.

## Keep durable memory concise

The final `student_review.md` contains the contract summary, verified findings,
dispositions, applied revision summary, voice-clearance outcome, verification
outcome, voice-pack maintenance decision, and round metrics. Record tokens and
output words by role, findings by role and class, verification and disposition
rates, voice-review cycles, checker-detectable findings, and regressions
introduced by repairs. It is not a dump of all agent prose.

The task directory must contain the review contract, frozen inputs,
deterministic output, one raw report per required role, structured findings,
decisions, final report, and run status. Run
`scripts/validate_review_package.py` before calling the package complete. Do
not imply completion when the validator fails or an artifact is missing.

Keep detailed historical rulings outside this skill. Read
`references/adjudication-rules.md` when choosing dispositions or drafting
repairs. Promote only genuinely general rules into that reference.

Append terminology-ledger rows only after explicit ledger approval. Never send
problem-set solutions or solution-profile output to reviewer agents.

The review workflow performs no automatic deletion. If Jared requests cleanup,
first stop every review agent. Resolve the target and require it to be exactly
one non-symlink direct child of `working/` containing `review_contract.yml` or
`.incomplete`; refuse `working/`, the repository root, `.`, traversal, or any
other path. Delete nothing outside that one review directory. The project's
existing interactive scratch cleanup remains the normal way to retire review
artifacts.
