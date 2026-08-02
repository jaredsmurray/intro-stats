# Review artifacts, decisions, and finding schema

## Contents

- Review contract
- Candidate finding
- Severity and evidence standards
- Verification classifications
- Disposition taxonomy
- Revision and voice-clearance record
- Author decisions
- Final report

Keep raw agent reports in the task directory. Compile them into structured
findings before drafting prose.

## Review contract

Record at least:

```yaml
chapter_source:
rendered_artifact:
source_hash:
render_hash:
render_status: verified-current | mtime-only | source-reconstructed
review_stage: initial | follow-up | post-revision
scope_start:
scope_end:
entry_context_start:
entry_context_purpose:
delta_basis: before-after-diff | author-target | bounded-current-section
baseline_source_hash:
visual_bundle_status: self-contained | partial-assets | text-only
continuity_inputs_status: complete | limited-by-review-contract
prerequisite_bundle_status: not-required | complete | limited
continuity_risk: normal | high
continuity_risk_reason:
role_continuity_inputs: {}
reading_situation:
prior_boundary:
objectives_source: author | chapter-inferred
objectives: []
mode: lint | delta | standard | deep
action_scope: review-only | propose-revisions | apply-and-verify
voice_clearance_mode: required | optional | waived
voice_clearance_waiver_reason:
run_status: pending | complete | partial
required_roles: []
missing_required_roles: []
companion_artifacts: []
existing_plan_owners: []
deterministic_checks: {}
```

Do not treat `mtime-only` as proof that every dependency was current.

## Candidate finding

Use one record per underlying problem:

```yaml
id:
location:
class:
  # correctness | misconception | continuity | example-display |
  # cognitive-load | terminology | render | provenance
severity: blocker | major | moderate | minor
confidence: high | medium | low
observed_symptom:
existing_strength:
residual_failure:
failed_student_task:
student_consequence:
recovery_attempt:
objective_at_risk:
reviewer_support: []
replicated: false
suspected_cause:
verification_status: pending | confirmed | reframed | unresolved | not-substantiated
verified_cause:
evidence:
repair_objective:
material_benefit:
no_change_cost: low | moderate | high
intervention_options: []
recommended_disposition:
author_decision_needed: true
decision_class: batch-correction | judgment | structural | cross-chapter | ledger
decision_status: pending | accepted | modified | held | no-change
adjudicated_disposition:
adjudicated_by:
adjudication_reason:
ledger_candidate: false
plan_owner:
```

Use `replicated` only when agents with the same brief independently reported
the issue. Cross-role agreement belongs in `reviewer_support` and does not imply
independent proof.

## Severity

- **Blocker**: makes a central result unusable or teaches a false rule that
  invalidates the rest of the chapter.
- **Major**: blocks a required conceptual move, invalidates a flagship example,
  or corrupts downstream learning.
- **Moderate**: creates a likely misconception or costly recovery failure, but
  the chapter remains usable.
- **Minor**: localized friction with an obvious recovery path and little
  downstream effect.

Keep typo and render-mechanics findings in separate lists when they do not
affect interpretation.

## Evidence standards

High-confidence evidence includes:

- a reproduced computation;
- a direct contradiction between visible surfaces;
- a documented failed recovery trace;
- a definition used outside its stated scope;
- a figure reading verified against the actual rendered figure;
- a broken prerequisite or cross-reference demonstrated from the prior text.

Agent agreement alone is not verification.

Before a candidate enters structured findings, `existing_strength`,
`residual_failure`, `failed_student_task`, `material_benefit`, and
`no_change_cost` must be explicit. If no student task fails and the chapter
already meets the objective, keep the observation in the raw report and
recommend no change rather than manufacturing a repair.

## Verification classifications

- **Confirmed**: the reported cause survives independent checking.
- **Reframed**: the student symptom is real, but the cause or technical claim
  changes after checking.
- **Unresolved**: provenance, author intent, or external evidence is required.
- **Not substantiated**: the evidence does not support the finding.

Preserve the original symptom even when the diagnosis is reframed.

## Disposition taxonomy

Use explicit outcomes rather than a bare accepted/rejected flag:

- `accept`
- `accept-reframed`
- `delete-instead`
- `repair-display-or-computation`
- `local-clarification`
- `structural-rewrite`
- `held-for-evidence`
- `escalated-to-plan`
- `true-but-immaterial`
- `out-of-scope`
- `not-substantiated`
- `promote-to-policy`

Ledger approval is a separate field and decision.

`true-but-immaterial` is an internal compiler classification only. Do not emit
it into `findings.yml`, the final report, or the author queue. The raw report
already preserves the observation. Promote it only when recurrence makes a
deterministic check or policy change actionable.

## Revision and voice-clearance record

For `propose-revisions` and `apply-and-verify`, add:

```yaml
revision:
  editor:
  candidate_diff:
  fresh_student_required: false
  fresh_student_reason:
  application_authority: author-decision | delegated-wording | standing-mechanical-waiver
  authority_ids: []
  pre_apply_source_hash:
  scope_check: pass | fail
  voice_clearance:
    mode: required | optional | waived
    source_hashes: {}
    adversary:
    cycles:
    verdict: pending | clear | clear-after-bounded-repair | clear-after-author-ruling | author-input | optional-not-run | waived
    blocking_findings_by_cycle: []
    advisory_notes: []
    author_rulings: []
    waiver_reason:
  repair_objective_results: []
voice_pack_maintenance:
  status: pending | pending-author | held | no-update | adjudicated
  candidates: []
  author_decisions: []
```

Advisory voice preferences do not enter the finding packet as chapter defects.
Record only source-backed blockers, meaning changes, genuine ambiguities, and
maintenance candidates.

Each voice-pack maintenance candidate uses:

```yaml
id:
classification: candidate-rule | candidate-checklist-item | candidate-example | candidate-vocabulary | candidate-qualify-or-retire
evidence_ids: []
evidence_summary:
current_pack_gap:
proposed_destination:
smallest_change:
recommendation:
decision_status: pending | accepted | held | no-change
author_reason:
```

The chapter revision may close with voice-pack maintenance marked
`pending-author` or `held`, because this is a separate decision. Do not mark the
maintenance hook `adjudicated` until every candidate has an author ruling.

## Author decisions

Keep `decisions.yml` as the authoritative append-only record of Jared's
rulings:

```yaml
decisions:
  - id:
    target_type: finding | voice-ambiguity | ledger | voice-pack
    target_id:
    decision: accepted | modified | held | no-change
    selected_option:
    reason:
    decided_by: Jared
    decided_at:
```

Mirror the current status into `findings.yml` for convenient filtering, but do
not store an independent prose version of the ruling in `student_review.md`.

## Final report

Use this order:

1. Contract and artifact status.
2. Executive verdict.
3. Verified findings, ranked by severity and consequence. For each, state the
   successful existing treatment before the narrow residual failure.
4. Unresolved evidence questions.
5. Actionable render and typo corrections. Omit immaterial observations already
   preserved in raw reports.
6. Coverage: every section, figure, table, exercise, and callout reviewed.
   Use columns `element`, `friction-read`, `transfer-tested`, `audited`, and
   `result`, so “no finding” is distinct from “not reviewed.”
7. Author decision queue, followed by recommended and adjudicated
   dispositions.
8. Applied revision summary, if authorized.
9. Adversarial voice-clearance result, cycle count, and author rulings.
10. Verification results.
11. Proposed ledger rows, explicitly pending or approved.
12. Voice-pack maintenance result and any separately adjudicated candidates.
13. Follow-up plans with owner and unblock condition.
14. Round metrics: tokens/output by role, findings by class and source,
    verification/disposition rates, voice-review cycles, checker-detectable
    findings, and repair-induced regressions.

Add context windows and exact old-to-new text only after a finding survives
verification and its intervention has been chosen.
