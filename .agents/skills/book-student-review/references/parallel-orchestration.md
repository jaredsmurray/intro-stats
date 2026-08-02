# Parallel orchestration

Use these rules whenever review work overlaps author decisions, revision, or
another chapter.

## Reserve the critical path

With four agent slots, reserve capacity in this order during diagnosis:

1. The orchestrator remains available to Jared.
2. One slot is available for the active author chapter's next bounded role.
3. The remaining two slots may run one lean background screen: one blind
   student and one technical auditor in parallel.

Do not start a background role that consumes the active author slot. A second
background chapter waits until the first screen finishes or the author lane is
idle. This is a slot-budget constraint, not a reason to delay ready author
work.

During end-of-pass review, pause background dispatch and use the available
slots for the voice adversary and targeted verifier together. A selectively
required fresh student reader may use the fourth slot. All of them inspect the
same finished revision.

## Dispatch without blocking

- Launch independent roles together in one dispatch.
- Do not wait for a background role before presenting compiled author cards,
  applying an approved candidate, or reporting completed verification.
- After dispatch, continue useful orchestrator work. Wait only when no
  independent local action remains.
- Use one bounded status check. If a bounded role has not produced its assigned
  artifact, inspect once, send one scope-narrowing follow-up, and continue other
  work. Do not create a polling loop.
- Stop a role from expanding into a general audit. Each prompt names one output
  artifact, one word or finding cap, and an explicit prohibition on unrelated
  work.
- Do not let review agents spawn additional agents. Optional follow-up roles
  are orchestrator decisions after skeptical compilation.

## Keep briefs small

The orchestrator reads the canonical skill. Role agents receive the applicable
brief from `agent-briefs.md`, the exact frozen inputs, and the minimum relevant
rules. Do not instruct every role to reread the full `SKILL.md`, raw reports,
or the complete voice pack.

For end-of-pass review, provide:

- a compact repair table;
- exact old and new passage boundaries;
- immediate neighboring prose;
- the current render and frozen voice-source hashes;
- only the voice rules and examples implicated by the patch.

The adversary or verifier may open a full source only when the bounded
materials reveal a specific unresolved question.

## Surface results immediately

The unit of delivery is the ready author decision or completed active-chapter
stage, not the review wave.

- Present cards as soon as skeptical compilation finishes.
- Report an applied-and-verified chapter before running unrelated forward
  tests, maintenance checks, or background compilation.
- Keep scratch-package validation and scoped deterministic checks on the
  critical path; keep generic skill tests, cleanup, and future-chapter work off
  it.
- When a background screen finishes during active author work, preserve its
  reports and defer compilation. Do not interrupt the author lane merely
  because agent output arrived.

## Recover from a slow role

A role is stalled when it has the required inputs but produces no assigned
artifact after one bounded wait and one narrow follow-up.

1. Preserve any partial artifact.
2. Cancel or stop the role rather than repeatedly waiting.
3. Complete directly when independence is not required.
4. If independence is required, free the slot and launch one replacement with
   the already bounded brief.
5. Mark the evidence partial if the replacement also fails; do not hold
   unrelated ready work.
