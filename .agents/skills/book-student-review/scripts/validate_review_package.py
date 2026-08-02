#!/usr/bin/env python3
"""Validate a frozen chapter-review package and its completion claims."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


MODES = {"lint", "delta", "standard", "deep"}
REVIEW_STAGES = {"initial", "follow-up", "post-revision"}
ACTIONS = {"review-only", "propose-revisions", "apply-and-verify"}
RUN_STATUSES = {"pending", "complete", "partial"}
ROLE_STATUSES = {"pending", "complete", "failed", "timed-out"}
RENDER_STATUSES = {"verified-current", "mtime-only", "source-reconstructed"}
VISUAL_STATUSES = {"self-contained", "partial-assets", "text-only"}
CONTINUITY_STATUSES = {"complete", "limited-by-review-contract"}
PREREQUISITE_BUNDLE_STATUSES = {"not-required", "complete", "limited"}
CONTINUITY_RISKS = {"normal", "high"}
PREREQUISITE_ACCESS = {"cue-triggered", "full", "none"}
OBJECTIVE_SOURCES = {"author", "chapter-inferred"}
VOICE_MODES = {"required", "optional", "waived"}
VOICE_VERDICTS = {
    "pending",
    "clear",
    "clear-after-bounded-repair",
    "clear-after-author-ruling",
    "author-input",
    "optional-not-run",
    "waived",
}
FINDING_CLASSES = {
    "correctness",
    "misconception",
    "continuity",
    "example-display",
    "cognitive-load",
    "terminology",
    "render",
    "provenance",
}
SEVERITIES = {"blocker", "major", "moderate", "minor"}
CONFIDENCES = {"high", "medium", "low"}
VERIFICATION_STATUSES = {
    "pending",
    "confirmed",
    "reframed",
    "unresolved",
    "not-substantiated",
}
DECISION_CLASSES = {
    "batch-correction",
    "judgment",
    "structural",
    "cross-chapter",
    "ledger",
}
DECISION_STATUSES = {"pending", "accepted", "modified", "held", "no-change"}
DISPOSITIONS = {
    "accept",
    "accept-reframed",
    "delete-instead",
    "repair-display-or-computation",
    "local-clarification",
    "structural-rewrite",
    "held-for-evidence",
    "escalated-to-plan",
    "true-but-immaterial",
    "out-of-scope",
    "not-substantiated",
    "promote-to-policy",
}
MAINTENANCE_STATUSES = {
    "pending",
    "pending-author",
    "held",
    "no-update",
    "adjudicated",
}
DIAGNOSTIC_ROLES = {
    "lint": [],
    "delta": ["blind_student", "technical_auditor"],
    "standard": ["blind_student", "technical_auditor"],
    "deep": ["blind_student", "technical_auditor"],
}
KNOWN_ROLES = {
    role for roles in DIAGNOSTIC_ROLES.values() for role in roles
} | {
    "blind_student_1",
    "blind_student_2",
    "pedagogical_reviewer",
    "structure_editor",
    "blind_continuity_reader",
    "evidence_verifier",
    "revision_editor",
    "voice_adversary",
    "targeted_verifier",
    "fresh_student_regression",
}


def initial_required_roles(mode: str, continuity_risk: str = "normal") -> list[str]:
    return list(DIAGNOSTIC_ROLES.get(mode, []))


def role_record(
    role_continuity: dict[str, Any],
    role: str,
) -> Any:
    """Accept pre-redesign blind_student_1 as the legacy primary-reader name."""
    if role == "blind_student" and role not in role_continuity:
        return role_continuity.get("blind_student_1")
    return role_continuity.get(role)


def has_accepted_revision(findings_data: Any) -> bool:
    if not isinstance(findings_data, dict):
        return False
    revision = findings_data.get("revision")
    if not isinstance(revision, dict):
        return False
    explicit_status = revision.get("status")
    if explicit_status in {"accepted", "proposed", "applied", "voice-cleared", "verified"}:
        return True
    if explicit_status in {"pending", "not-started", "declined", "none"}:
        return False
    return bool(
        revision.get("candidate_diff")
        or revision.get("editor")
        or revision.get("applied") is True
        or revision.get("accepted") is True
    )


def dynamic_required_roles(
    findings: list[Any],
    findings_data: Any,
    action: str,
    voice_mode: str,
) -> list[str]:
    roles: list[str] = []
    correctness_needing_independence = any(
        isinstance(finding, dict)
        and finding.get("class") == "correctness"
        and finding.get("severity") in {"blocker", "major"}
        for finding in findings
    )
    if correctness_needing_independence:
        roles.append("evidence_verifier")

    if has_accepted_revision(findings_data):
        if action not in {"propose-revisions", "apply-and-verify"}:
            return roles
        roles.append("revision_editor")
        if voice_mode == "required":
            roles.append("voice_adversary")
        if action == "apply-and-verify":
            roles.append("targeted_verifier")
            revision = findings_data.get("revision", {})
            if (
                isinstance(revision, dict)
                and revision.get("fresh_student_required") is True
            ):
                roles.append("fresh_student_regression")
    return roles


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_scalar(text: str) -> Any:
    value = text.strip()
    if not value:
        return None
    if value in {"null", "Null", "NULL", "~"}:
        return None
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.startswith(("[", "{")):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            if value.startswith("[") and value.endswith("]"):
                inside = value[1:-1].strip()
                return [] if not inside else [parse_scalar(part) for part in inside.split(",")]
    if (
        len(value) >= 2
        and value[0] == value[-1]
        and value[0] in {"'", '"'}
    ):
        if value[0] == '"':
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass
        return value[1:-1].replace("''", "'")
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?(?:\d+\.\d*|\d*\.\d+)", value):
        return float(value)
    return value


def yaml_lines(text: str) -> list[tuple[int, str, str]]:
    result: list[tuple[int, str, str]] = []
    for line_number, raw in enumerate(text.splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith(("#", "---", "...")):
            continue
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            raise ValueError(f"line {line_number}: tabs are not supported for indentation")
        indent = len(raw) - len(raw.lstrip(" "))
        result.append((indent, raw.strip(), raw[indent:]))
    return result


def split_mapping(text: str, line_number: int) -> tuple[str, str]:
    match = re.match(r"([^:]+):(.*)$", text)
    if not match:
        raise ValueError(f"line {line_number}: expected key: value")
    key = match.group(1).strip()
    if not key:
        raise ValueError(f"line {line_number}: empty mapping key")
    return key, match.group(2).strip()


def parse_simple_yaml(text: str) -> Any:
    """Parse the conservative YAML subset used by review package files."""
    lines = yaml_lines(text)
    if not lines:
        return None

    def parse_block(index: int, indent: int) -> tuple[Any, int]:
        if index >= len(lines):
            return None, index
        is_list = lines[index][1].startswith("-")
        container: Any = [] if is_list else {}

        while index < len(lines):
            current_indent, stripped, _ = lines[index]
            line_number = index + 1
            if current_indent < indent:
                break
            if current_indent > indent:
                raise ValueError(f"line {line_number}: unexpected indentation")

            if is_list:
                if not stripped.startswith("-"):
                    break
                rest = stripped[1:].strip()
                index += 1
                if not rest:
                    if index < len(lines) and lines[index][0] > indent:
                        value, index = parse_block(index, lines[index][0])
                    else:
                        value = None
                    container.append(value)
                    continue
                if ":" in rest and not rest.startswith(("http:", "https:")):
                    key, value_text = split_mapping(rest, line_number)
                    item: dict[str, Any] = {}
                    if value_text in {"|", ">"}:
                        value, index = parse_block_scalar(index, indent, value_text)
                    elif value_text:
                        value = parse_scalar(value_text)
                    elif index < len(lines) and lines[index][0] > indent:
                        value, index = parse_block(index, lines[index][0])
                    else:
                        value = None
                    item[key] = value
                    if index < len(lines) and lines[index][0] > indent:
                        continuation, index = parse_block(index, lines[index][0])
                        if not isinstance(continuation, dict):
                            raise ValueError(
                                f"line {line_number}: list mapping continuation must be a mapping"
                            )
                        item.update(continuation)
                    container.append(item)
                else:
                    container.append(parse_scalar(rest))
                continue

            if stripped.startswith("-"):
                break
            key, value_text = split_mapping(stripped, line_number)
            index += 1
            if value_text in {"|", ">"}:
                value, index = parse_block_scalar(index, indent, value_text)
            elif value_text:
                value = parse_scalar(value_text)
            elif index < len(lines) and lines[index][0] > indent:
                value, index = parse_block(index, lines[index][0])
            else:
                value = None
            container[key] = value

        return container, index

    def parse_block_scalar(index: int, parent_indent: int, style: str) -> tuple[str, int]:
        pieces: list[str] = []
        while index < len(lines) and lines[index][0] > parent_indent:
            pieces.append(lines[index][2].strip() if style == ">" else lines[index][2])
            index += 1
        separator = " " if style == ">" else "\n"
        return separator.join(pieces), index

    value, final_index = parse_block(0, lines[0][0])
    if final_index != len(lines):
        raise ValueError(f"line {final_index + 1}: could not parse remaining YAML")
    return value


def load_data(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return parse_simple_yaml(text)


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


class Validator:
    def __init__(self, task_dir: Path) -> None:
        self.task_dir = task_dir
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def enum(self, mapping: dict[str, Any], key: str, allowed: set[str], label: str) -> None:
        value = mapping.get(key)
        if value not in allowed:
            self.error(f"{label}.{key}: expected one of {sorted(allowed)}, got {value!r}")

    def safe_path(self, relative: Any, label: str) -> Path | None:
        if not isinstance(relative, str) or not relative:
            self.error(f"{label}: missing package-relative path")
            return None
        candidate = (self.task_dir / relative).resolve()
        try:
            candidate.relative_to(self.task_dir)
        except ValueError:
            self.error(f"{label}: path escapes task directory: {relative}")
            return None
        return candidate

    def validate_hash(self, record: Any, label: str) -> None:
        if not isinstance(record, dict):
            self.error(f"{label}: expected path/hash mapping")
            return
        path = self.safe_path(record.get("path"), f"{label}.path")
        expected = record.get("sha256")
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            self.error(f"{label}.sha256: missing or invalid SHA-256")
            return
        if path is None:
            return
        if not path.is_file():
            self.error(f"{label}: frozen input missing: {path}")
            return
        actual = sha256_file(path)
        if actual != expected:
            self.error(f"{label}: SHA-256 mismatch for {path}")

    def validate_finding(self, finding: Any, index: int) -> None:
        label = f"findings[{index}]"
        if not isinstance(finding, dict):
            self.error(f"{label}: expected a mapping")
            return
        enum_fields = {
            "class": FINDING_CLASSES,
            "severity": SEVERITIES,
            "confidence": CONFIDENCES,
            "verification_status": VERIFICATION_STATUSES,
            "decision_class": DECISION_CLASSES,
            "decision_status": DECISION_STATUSES,
        }
        for key, allowed in enum_fields.items():
            if key in finding and finding[key] not in allowed:
                self.error(
                    f"{label}.{key}: expected one of {sorted(allowed)}, "
                    f"got {finding[key]!r}"
                )
        disposition = finding.get("adjudicated_disposition")
        if disposition not in {None, ""} and disposition not in DISPOSITIONS:
            self.error(f"{label}.adjudicated_disposition: invalid value {disposition!r}")
        if finding.get("recommended_disposition") == "true-but-immaterial":
            self.error(
                f"{label}: true-but-immaterial observations belong only in raw "
                "reports and must not enter structured findings"
            )
        if disposition == "true-but-immaterial":
            self.error(
                f"{label}: true-but-immaterial observations must not be "
                "adjudicated or retained in structured findings"
            )

    def validate_decision(self, decision: Any, index: int) -> None:
        label = f"decisions[{index}]"
        if not isinstance(decision, dict):
            self.error(f"{label}: expected a mapping")
            return
        status = decision.get("decision_status", decision.get("status"))
        if status is not None and status not in DECISION_STATUSES:
            self.error(f"{label}.status: invalid value {status!r}")
        disposition = decision.get(
            "adjudicated_disposition", decision.get("disposition")
        )
        if disposition not in {None, ""} and disposition not in DISPOSITIONS:
            self.error(f"{label}.disposition: invalid value {disposition!r}")

    def run(self) -> None:
        if not self.task_dir.is_dir():
            self.error(f"task directory does not exist: {self.task_dir}")
            return
        filenames = {
            "contract": "review_contract.yml",
            "status": "run_status.yml",
            "findings": "findings.yml",
            "decisions": "decisions.yml",
        }
        loaded: dict[str, Any] = {}
        for label, filename in filenames.items():
            path = self.task_dir / filename
            if not path.is_file():
                self.error(f"missing required artifact: {filename}")
                continue
            try:
                loaded[label] = load_data(path)
            except (OSError, ValueError) as exc:
                self.error(f"{filename}: could not parse: {exc}")

        contract = loaded.get("contract")
        status = loaded.get("status")
        findings_data = loaded.get("findings")
        decisions_data = loaded.get("decisions")
        if not isinstance(contract, dict) or not isinstance(status, dict):
            return

        self.enum(contract, "mode", MODES, "contract")
        if "review_stage" in contract:
            self.enum(contract, "review_stage", REVIEW_STAGES, "contract")
        self.enum(contract, "action_scope", ACTIONS, "contract")
        self.enum(contract, "render_status", RENDER_STATUSES, "contract")
        self.enum(contract, "visual_bundle_status", VISUAL_STATUSES, "contract")
        self.enum(
            contract,
            "continuity_inputs_status",
            CONTINUITY_STATUSES,
            "contract",
        )
        self.enum(
            contract,
            "prerequisite_bundle_status",
            PREREQUISITE_BUNDLE_STATUSES,
            "contract",
        )
        self.enum(contract, "continuity_risk", CONTINUITY_RISKS, "contract")
        self.enum(contract, "objectives_source", OBJECTIVE_SOURCES, "contract")
        self.enum(contract, "voice_clearance_mode", VOICE_MODES, "contract")
        self.enum(contract, "run_status", RUN_STATUSES, "contract")
        self.enum(status, "run_status", RUN_STATUSES, "status")

        if (
            contract.get("render_status") == "verified-current"
            and not (
                isinstance(contract.get("render_freshness_evidence"), dict)
                and contract["render_freshness_evidence"].get("note")
            )
        ):
            self.error("verified-current render lacks explicit freshness evidence")
        if (
            contract.get("voice_clearance_mode") == "waived"
            and not contract.get("voice_clearance_waiver_reason")
        ):
            self.error("waived voice clearance lacks a waiver reason")
        if contract.get("mode") == "delta" and not contract.get("delta_basis"):
            self.error("Delta mode lacks delta_basis")
        if (
            contract.get("mode") == "delta"
            and contract.get("review_stage") == "initial"
        ):
            self.error("initial review incorrectly uses Delta mode")
        if contract.get("mode") != "delta" and contract.get("delta_basis"):
            self.error("non-Delta review declares delta_basis")
        if (
            contract.get("continuity_risk") == "high"
            and not contract.get("continuity_risk_reason")
        ):
            self.error("high continuity risk lacks a reason")
        entry_context_start = contract.get("entry_context_start")
        if entry_context_start:
            extraction = contract.get("render_extraction")
            if not isinstance(extraction, dict):
                self.error("entry context declared without bounded render extraction")
            else:
                if extraction.get("context_start_id") != entry_context_start:
                    self.error(
                        "contract.entry_context_start disagrees with render extraction"
                    )
                if not extraction.get("scope_start_id"):
                    self.error("entry-context extraction lacks target scope_start_id")

        frozen = contract.get("frozen_inputs")
        if not isinstance(frozen, dict):
            self.error("contract.frozen_inputs: missing mapping")
        else:
            self.validate_hash(frozen.get("source"), "frozen_inputs.source")
            self.validate_hash(frozen.get("render"), "frozen_inputs.render")
            assets = frozen.get("assets", [])
            if not isinstance(assets, list):
                self.error("frozen_inputs.assets: expected a list")
            else:
                for index, asset in enumerate(assets):
                    self.validate_hash(asset, f"frozen_inputs.assets[{index}]")
            prerequisites = frozen.get("prerequisites", [])
            if not isinstance(prerequisites, list):
                self.error("frozen_inputs.prerequisites: expected a list")
                prerequisites = []
            else:
                labels: set[str] = set()
                for index, prerequisite in enumerate(prerequisites):
                    label = f"frozen_inputs.prerequisites[{index}]"
                    self.validate_hash(prerequisite, label)
                    if not isinstance(prerequisite, dict):
                        continue
                    prerequisite_label = prerequisite.get("label")
                    if not isinstance(prerequisite_label, str) or not prerequisite_label:
                        self.error(f"{label}.label: missing")
                    elif prerequisite_label in labels:
                        self.error(f"{label}.label: duplicate {prerequisite_label!r}")
                    else:
                        labels.add(prerequisite_label)
                    prerequisite_assets = prerequisite.get("assets", [])
                    if not isinstance(prerequisite_assets, list):
                        self.error(f"{label}.assets: expected a list")
                    else:
                        for asset_index, asset in enumerate(prerequisite_assets):
                            self.validate_hash(
                                asset,
                                f"{label}.assets[{asset_index}]",
                            )
            source_record = frozen.get("source")
            render_record = frozen.get("render")
            if isinstance(source_record, dict) and contract.get("source_hash") != source_record.get("sha256"):
                self.error("contract.source_hash disagrees with frozen source record")
            if isinstance(render_record, dict) and contract.get("render_hash") != render_record.get("sha256"):
                self.error("contract.render_hash disagrees with frozen render record")

            bundle_status = contract.get("prerequisite_bundle_status")
            if bundle_status == "complete" and not prerequisites:
                self.error("complete prerequisite bundle contains no excerpts")
            if bundle_status == "not-required" and prerequisites:
                self.error("not-required prerequisite bundle contains excerpts")

        findings: list[Any] = []
        if isinstance(findings_data, list):
            findings = findings_data
        elif isinstance(findings_data, dict):
            candidate = findings_data.get("findings", [])
            if isinstance(candidate, list):
                findings = candidate
            else:
                self.error("findings.yml: findings must be a list")
            maintenance = findings_data.get("voice_pack_maintenance")
            if isinstance(maintenance, dict):
                maintenance_status = maintenance.get("status")
                if maintenance_status not in MAINTENANCE_STATUSES:
                    self.error(
                        "findings.voice_pack_maintenance.status: "
                        f"invalid value {maintenance_status!r}"
                    )
        elif findings_data is not None:
            self.error("findings.yml: expected a mapping or list")
        for index, finding in enumerate(findings):
            self.validate_finding(finding, index)

        decisions: list[Any] = []
        if isinstance(decisions_data, list):
            decisions = decisions_data
        elif isinstance(decisions_data, dict):
            candidate = decisions_data.get("decisions", [])
            if isinstance(candidate, list):
                decisions = candidate
            else:
                self.error("decisions.yml: decisions must be a list")
        elif decisions_data is not None:
            self.error("decisions.yml: expected a mapping or list")
        for index, decision in enumerate(decisions):
            self.validate_decision(decision, index)

        mode = contract.get("mode")
        action = contract.get("action_scope")
        voice_mode = contract.get("voice_clearance_mode")
        base_roles = initial_required_roles(
            mode,
            contract.get("continuity_risk", "normal"),
        )
        dynamic_roles = dynamic_required_roles(
            findings,
            findings_data,
            action,
            voice_mode,
        )
        derived_roles = base_roles + [
            role for role in dynamic_roles if role not in base_roles
        ]
        declared_roles = contract.get("required_roles")
        if not isinstance(declared_roles, list):
            self.error("contract.required_roles: expected a list")
            declared_roles = []
        unknown_roles = [
            role for role in declared_roles if not isinstance(role, str) or role not in KNOWN_ROLES
        ]
        if unknown_roles:
            self.error(f"contract.required_roles contains unknown roles: {unknown_roles}")
        omitted_roles = [
            role
            for role in derived_roles
            if role not in declared_roles
            and not (
                role == "blind_student"
                and "blind_student_1" in declared_roles
            )
        ]
        if omitted_roles:
            self.error(
                "contract.required_roles omits roles required by the current phase: "
                + ", ".join(omitted_roles)
            )
        effective_roles = [
            role for role in declared_roles if isinstance(role, str) and role in KNOWN_ROLES
        ]

        role_continuity = contract.get("role_continuity_inputs")
        if not isinstance(role_continuity, dict):
            self.error("contract.role_continuity_inputs: expected a mapping")
            role_continuity = {}
        for role in base_roles:
            record = role_record(role_continuity, role)
            if not isinstance(record, dict):
                self.error(
                    f"contract.role_continuity_inputs missing required role: {role}"
                )
                continue
            role_status = record.get("status")
            if role_status not in CONTINUITY_STATUSES:
                self.error(
                    f"contract.role_continuity_inputs.{role}.status: invalid "
                    f"value {role_status!r}"
                )
            access = record.get("prerequisite_access")
            if access not in PREREQUISITE_ACCESS:
                self.error(
                    f"contract.role_continuity_inputs.{role}."
                    f"prerequisite_access: invalid value {access!r}"
                )
            if (
                contract.get("prerequisite_bundle_status") == "complete"
                and access == "none"
            ):
                self.error(
                    f"role {role} has no access to a complete prerequisite bundle"
                )
        if (
            contract.get("continuity_inputs_status") == "complete"
            and any(
                isinstance(record, dict)
                and record.get("status") != "complete"
                for role, record in role_continuity.items()
                if role in base_roles
            )
        ):
            self.error(
                "global continuity status is complete while a required "
                "diagnostic role is limited"
            )

        role_states = status.get("roles")
        if not isinstance(role_states, dict):
            self.error("status.roles: expected a mapping")
            role_states = {}

        missing_or_incomplete: list[str] = []
        late_roles: list[str] = []
        compiled_at = parse_time(status.get("compiled_at"))
        findings_path = self.task_dir / "findings.yml"
        findings_mtime = (
            datetime.fromtimestamp(findings_path.stat().st_mtime).astimezone()
            if findings_path.is_file()
            else None
        )
        for role in effective_roles:
            state = role_states.get(role)
            if not isinstance(state, dict):
                self.error(f"required role missing from status.roles: {role}")
                missing_or_incomplete.append(role)
                continue
            role_status = state.get("status")
            if role_status not in ROLE_STATUSES:
                self.error(f"role {role}: invalid status {role_status!r}")
            artifact = self.safe_path(state.get("artifact"), f"role {role}.artifact")
            if role_status != "complete":
                missing_or_incomplete.append(role)
            if role_status == "complete":
                if artifact is None or not artifact.is_file() or artifact.stat().st_size == 0:
                    self.error(f"role {role}: complete but artifact is missing or empty")
                    missing_or_incomplete.append(role)
                completed_at = parse_time(state.get("completed_at"))
                if compiled_at and completed_at and completed_at > compiled_at:
                    late_roles.append(role)
                elif (
                    compiled_at
                    and artifact is not None
                    and artifact.is_file()
                    and datetime.fromtimestamp(artifact.stat().st_mtime).astimezone()
                    > compiled_at
                ):
                    late_roles.append(role)
                elif (
                    findings_mtime is not None
                    and artifact is not None
                    and artifact.is_file()
                    and artifact.stat().st_mtime > findings_path.stat().st_mtime
                    and status.get("run_status") == "complete"
                ):
                    late_roles.append(role)

        recorded_missing = status.get("missing_required_roles")
        if not isinstance(recorded_missing, list):
            self.error("status.missing_required_roles: expected a list")
        elif sorted(recorded_missing) != sorted(set(missing_or_incomplete)):
            self.error(
                "status.missing_required_roles is stale: "
                f"expected {sorted(set(missing_or_incomplete))}, got {sorted(recorded_missing)}"
            )
        recorded_late = status.get("late_reports", [])
        if not isinstance(recorded_late, list):
            self.error("status.late_reports: expected a list")
        elif sorted(recorded_late) != sorted(set(late_roles)):
            self.error(
                "status.late_reports is stale: "
                f"expected {sorted(set(late_roles))}, got {sorted(recorded_late)}"
            )

        is_claimed_complete = (
            contract.get("run_status") == "complete"
            or status.get("run_status") == "complete"
        )
        if contract.get("run_status") != status.get("run_status"):
            self.error("contract and status disagree on run_status")
        if is_claimed_complete:
            if missing_or_incomplete:
                self.error(
                    "run falsely claims complete with incomplete roles: "
                    + ", ".join(sorted(set(missing_or_incomplete)))
                )
            if late_roles:
                self.error(
                    "run falsely claims complete with reports newer than compilation: "
                    + ", ".join(sorted(set(late_roles)))
                )
            if not contract.get("deterministic_checks"):
                self.error("complete run has no recorded deterministic-check results")
            final_report = self.task_dir / "student_review.md"
            if not final_report.is_file() or final_report.stat().st_size == 0:
                self.error("complete run lacks a nonempty student_review.md")

            if action == "apply-and-verify" and has_accepted_revision(findings_data):
                for index, finding in enumerate(findings):
                    if (
                        isinstance(finding, dict)
                        and finding.get("severity") in {"blocker", "major"}
                        and finding.get("decision_status") in {None, "", "pending"}
                    ):
                        self.error(
                            f"findings[{index}]: unapplied blocker/major lacks adjudication"
                        )
                revision = (
                    findings_data.get("revision")
                    if isinstance(findings_data, dict)
                    else None
                )
                if not isinstance(revision, dict):
                    self.error("apply-and-verify completion lacks revision record")
                else:
                    clearance = revision.get("voice_clearance")
                    if voice_mode == "required":
                        verdict = (
                            clearance.get("verdict")
                            if isinstance(clearance, dict)
                            else None
                        )
                        if verdict not in {
                            "clear",
                            "clear-after-bounded-repair",
                            "clear-after-author-ruling",
                        }:
                            self.error(
                                "required voice clearance has not reached a closing verdict"
                            )
                    results = revision.get("repair_objective_results")
                    if not isinstance(results, list):
                        self.error("revision.repair_objective_results must be a list")
                    elif any(
                        isinstance(result, dict)
                        and result.get("result") not in {"pass", "held", "not-applicable"}
                        for result in results
                    ):
                        self.error("one or more repair objectives did not pass")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate review contract, status, findings, decisions, frozen hashes, "
            "role artifacts, and any completion claim."
        )
    )
    parser.add_argument("task_dir", type=Path, help="Review task directory to validate")
    parser.add_argument(
        "--warnings-as-errors",
        action="store_true",
        help="Return nonzero when advisory warnings are present.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    validator = Validator(args.task_dir.expanduser().resolve())
    validator.run()
    for warning in validator.warnings:
        print(f"WARNING: {warning}")
    for error in validator.errors:
        print(f"ERROR: {error}")
    if validator.errors or (args.warnings_as_errors and validator.warnings):
        print(
            f"INVALID: {len(validator.errors)} error(s), "
            f"{len(validator.warnings)} warning(s)"
        )
        return 1
    print(f"VALID: {validator.task_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
