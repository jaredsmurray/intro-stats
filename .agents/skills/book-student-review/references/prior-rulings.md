# Prior author rulings

Use the durable chapter logs in `review_history/declined_edits/` to prevent a
new review from sending Jared the same declined edit again. Log filenames match
the root chapter source basename, not chapter numbers; for example,
`regression_03_model.qmd` maps to `regression_03_model.yml`.

## When to read the logs

Do not give these logs to blind readers, technical auditors, or other initial
diagnostic roles. Independent diagnosis should remain independent.

After skeptical compilation and verification, but before constructing the
author queue, read the current source file's log. Read another chapter's log
only when the candidate depends on that chapter's explicit handoff or an owned
cross-chapter ruling.

For each surviving candidate, ask:

1. Does it propose the same or a substantively similar edit?
2. Does the prior rationale still describe the current passage and objective?
3. Has the source, evidence, teaching purpose, or downstream use changed in a
   way named by `reopen_if`?

If the first two answers are yes and the third is no, mark the candidate
`previously-adjudicated` and omit it from the author queue. Preserve the new
diagnostic report as evidence, but do not ask Jared again.

If a ruling may no longer apply, the decision card must state the prior ruling
and the material change that justifies reopening it. Reviewer disagreement or
more elaborate technical argument is not, by itself, materially new evidence.

## What to record

After Jared explicitly declines an edit, append one concise entry to the
current source file's log. Record settled author choices, not compiler-rejected
noise or every observation left out of the queue.

```yaml
schema_version: 1
chapter_source: regression_03_model.qmd
declined_edits:
  - id: stable-semantic-id
    location: section anchor or stable passage description
    declined_proposal: One-sentence description of the edit Jared declined.
    author_rationale: Jared's reason, quoted or faithfully compressed.
    scope: What the ruling protects or leaves unchanged.
    reopen_if: A concrete condition that could make reconsideration legitimate.
    decided_at: YYYY-MM-DD
    evidence:
      - path/to/decisions.yml
    tags: [optional, search-only, tags]
```

Use semantic IDs and stable section anchors rather than line numbers. Tags are
for retrieval only; they never become automatic decision rules.

Do not treat a hold or an owned future redesign as a permanent decline. Record
it only when the current no-change ruling is useful, and make the owner or
unblock condition explicit in `reopen_if`.

## Maintenance

- Keep one file per root chapter source. Do not create empty files.
- When a ruling is superseded, retain it with `status: superseded` and name the
  replacement decision.
- When a source file is renamed, rename its log in the same change.
- Do not copy these rulings into `SKILL.md`, the voice pack, or terminology
  ledger unless Jared separately approves a genuinely general rule.
