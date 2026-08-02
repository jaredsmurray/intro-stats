#!/usr/bin/env python3
"""Create a frozen, machine-readable chapter-review package."""

from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
import mmap
from pathlib import Path
import re
import shutil
import sys
from datetime import datetime, timezone
from typing import Any
from urllib.parse import unquote, urlsplit


MODES = ("lint", "delta", "standard", "deep")
REVIEW_STAGES = ("initial", "follow-up", "post-revision")
ACTIONS = ("review-only", "propose-revisions", "apply-and-verify")
RENDER_STATUSES = ("verified-current", "mtime-only", "source-reconstructed")
VOICE_MODES = ("required", "optional", "waived")
CONTINUITY_STATUSES = ("complete", "limited-by-review-contract")
OBJECTIVE_SOURCES = ("author", "chapter-inferred")
PREREQUISITE_BUNDLE_STATUSES = ("not-required", "complete", "limited")
CONTINUITY_RISKS = ("normal", "high")

DIAGNOSTIC_ROLES = {
    "lint": [],
    "delta": ["blind_student", "technical_auditor"],
    "standard": ["blind_student", "technical_auditor"],
    "deep": ["blind_student", "technical_auditor"],
}


def required_roles(mode: str, continuity_risk: str = "normal") -> list[str]:
    """Return the lean initial screen; later roles require an evidence trigger."""
    return list(DIAGNOSTIC_ROLES[mode])


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_machine_yaml(path: Path, value: object) -> None:
    """Write JSON, which is a strict subset of YAML 1.2."""
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def is_external_url(value: str) -> bool:
    stripped = value.strip()
    if not stripped or stripped.startswith(("#", "data:", "javascript:", "mailto:")):
        return True
    parsed = urlsplit(stripped)
    return bool(parsed.scheme and parsed.scheme != "file") or bool(parsed.netloc)


def clean_local_url(value: str) -> str | None:
    if is_external_url(value):
        return None
    parsed = urlsplit(value.strip())
    candidate = unquote(parsed.path)
    return candidate or None


class AssetReferenceParser(HTMLParser):
    """Collect asset-bearing HTML references without following navigation."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.local_refs: set[str] = set()
        self.remote_refs: set[str] = set()
        self.inline_css: list[str] = []
        self._in_style = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value for key, value in attrs if value is not None}
        tag = tag.lower()
        candidates: list[str] = []
        if tag in {"img", "script", "iframe", "embed", "audio", "video", "source", "track"}:
            if "src" in values:
                candidates.append(values["src"])
        if tag == "object" and "data" in values:
            candidates.append(values["data"])
        if tag == "video" and "poster" in values:
            candidates.append(values["poster"])
        if tag == "link" and "href" in values:
            rel = set(values.get("rel", "").lower().split())
            if rel & {"stylesheet", "icon", "preload", "modulepreload", "manifest"}:
                candidates.append(values["href"])
        if tag == "use":
            href = values.get("href") or values.get("xlink:href")
            if href:
                candidates.append(href)
        if "srcset" in values:
            for candidate in srcset_urls(values["srcset"]):
                if candidate:
                    candidates.append(candidate)
        if "style" in values:
            self.inline_css.append(values["style"])
        for candidate in candidates:
            local = clean_local_url(candidate)
            if local is None:
                if candidate and not candidate.lstrip().startswith(("#", "data:")):
                    self.remote_refs.add(candidate)
            else:
                self.local_refs.add(local)
        if tag == "style":
            self._in_style = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "style":
            self._in_style = False

    def handle_data(self, data: str) -> None:
        if self._in_style:
            self.inline_css.append(data)


CSS_URL_RE = re.compile(
    r"""url\(\s*(?:(?P<quote>["'])(?P<quoted>.*?)(?P=quote)|(?P<bare>[^)]*?))\s*\)""",
    re.IGNORECASE | re.DOTALL,
)
CSS_IMPORT_RE = re.compile(
    r"""@import\s+(?P<quote>["'])(?P<url>.*?)(?P=quote)""",
    re.IGNORECASE | re.DOTALL,
)


def srcset_urls(value: str) -> list[str]:
    """Extract srcset URLs without splitting commas inside data URLs."""
    urls: list[str] = []
    position = 0
    length = len(value)
    while position < length:
        while position < length and (
            value[position].isspace() or value[position] == ","
        ):
            position += 1
        if position >= length:
            break

        start = position
        while position < length and not value[position].isspace():
            position += 1
        candidate = value[start:position]
        if candidate.endswith(","):
            candidate = candidate.rstrip(",")
            if candidate:
                urls.append(candidate)
            continue
        if candidate:
            urls.append(candidate)

        parenthesis_depth = 0
        while position < length:
            character = value[position]
            if character == "(":
                parenthesis_depth += 1
            elif character == ")" and parenthesis_depth:
                parenthesis_depth -= 1
            elif character == "," and parenthesis_depth == 0:
                position += 1
                break
            position += 1
    return urls


def css_references(text: str) -> tuple[set[str], set[str]]:
    local: set[str] = set()
    remote: set[str] = set()
    for match in CSS_URL_RE.finditer(text):
        raw = (match.group("quoted") or match.group("bare") or "").strip()
        cleaned = clean_local_url(raw)
        if cleaned is None:
            if raw and not raw.lstrip().startswith(("#", "data:")):
                remote.add(raw)
        else:
            local.add(cleaned)
    for match in CSS_IMPORT_RE.finditer(text):
        raw = match.group("url").strip()
        cleaned = clean_local_url(raw)
        if cleaned is None:
            if raw and not raw.lstrip().startswith(("#", "data:")):
                remote.add(raw)
        else:
            local.add(cleaned)
    return local, remote


def resolve_reference(raw: str, base_dir: Path, html_dir: Path) -> Path:
    path = Path(raw)
    if path.is_absolute():
        # Root-relative web paths are usually relative to the rendered site.
        path = html_dir / raw.lstrip("/")
    else:
        path = base_dir / path
    return path.resolve()


def discover_assets(
    html_path: Path,
    reference_base_dir: Path | None = None,
    excluded_paths: set[Path] | None = None,
) -> tuple[list[Path], list[str], list[str]]:
    html_text = html_path.read_text(encoding="utf-8", errors="replace")
    reference_base_dir = (reference_base_dir or html_path.parent).resolve()
    excluded_paths = {
        path.resolve() for path in (excluded_paths or set())
    }
    parser = AssetReferenceParser()
    parser.feed(html_text)
    inline_local: set[str] = set()
    inline_remote: set[str] = set()
    for css in parser.inline_css:
        local, remote = css_references(css)
        inline_local.update(local)
        inline_remote.update(remote)

    queue: list[tuple[str, Path]] = [
        (reference, reference_base_dir)
        for reference in parser.local_refs | inline_local
    ]
    remote_refs = set(parser.remote_refs) | inline_remote
    assets: set[Path] = set()
    missing: set[str] = set()
    visited_css: set[Path] = set()

    while queue:
        raw, base_dir = queue.pop()
        resolved = resolve_reference(raw, base_dir, reference_base_dir)
        try:
            resolved.relative_to(reference_base_dir)
        except ValueError:
            missing.add(f"{resolved} (outside rendered-artifact directory)")
            continue
        if resolved in excluded_paths:
            continue
        if not resolved.is_file():
            missing.add(str(resolved))
            continue
        assets.add(resolved)
        if resolved.suffix.lower() != ".css" or resolved in visited_css:
            continue
        visited_css.add(resolved)
        css_text = resolved.read_text(encoding="utf-8", errors="replace")
        local, remote = css_references(css_text)
        remote_refs.update(remote)
        queue.extend((reference, resolved.parent) for reference in local)

    return sorted(assets), sorted(missing), sorted(remote_refs)


HTML_TOKEN_RE = re.compile(
    rb"""<!--.*?-->|<(?P<closing>/)?(?P<tag>[A-Za-z][A-Za-z0-9:_-]*)
        (?P<attrs>(?:"[^"]*"|'[^']*'|[^'">])*)>""",
    re.IGNORECASE | re.DOTALL | re.VERBOSE,
)
ATTRIBUTE_RE = re.compile(
    rb"""(?P<name>[^\s"'=<>`/]+)(?:\s*=\s*
        (?:"(?P<double>[^"]*)"|'(?P<single>[^']*)'|
        (?P<bare>[^\s"'=<>`]+)))?""",
    re.IGNORECASE | re.VERBOSE,
)
RAW_TEXT_TAGS = {b"script", b"style", b"textarea", b"title"}


def element_id(attributes: bytes) -> bytes | None:
    """Return the actual id attribute without searching inside quoted values."""
    for attribute in ATTRIBUTE_RE.finditer(attributes):
        if attribute.group("name").lower() != b"id":
            continue
        return (
            attribute.group("double")
            or attribute.group("single")
            or attribute.group("bare")
            or b""
        )
    return None


def find_html_boundaries(
    path: Path,
    start_id: str,
    end_id: str,
) -> tuple[int, int, int, int]:
    """Find actual head and element boundaries without matching comments/scripts."""
    start_value = start_id.encode("utf-8")
    end_value = end_id.encode("utf-8")
    head_start: int | None = None
    head_end: int | None = None
    scope_start: int | None = None
    scope_end: int | None = None
    raw_text_tag: bytes | None = None

    with path.open("rb") as handle:
        with mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ) as mapped:
            for token in HTML_TOKEN_RE.finditer(mapped):
                if token.group(0).startswith(b"<!--"):
                    continue
                tag = token.group("tag").lower()
                closing = token.group("closing") is not None

                if raw_text_tag is not None:
                    if closing and tag == raw_text_tag:
                        raw_text_tag = None
                    continue

                if closing:
                    if tag == b"head" and head_start is not None and head_end is None:
                        head_end = token.end()
                    continue

                if tag == b"head" and head_start is None:
                    head_start = token.start()

                value = element_id(token.group("attrs"))
                if value is not None:
                    if scope_start is None and value == start_value:
                        scope_start = token.start()
                    elif (
                        scope_start is not None
                        and scope_end is None
                        and value == end_value
                    ):
                        scope_end = token.start()

                if tag in RAW_TEXT_TAGS:
                    raw_text_tag = tag

    if head_start is None or head_end is None or head_end <= head_start:
        fail("could not identify a complete <head>...</head> in rendered HTML")
    if scope_start is None:
        fail(f"scope start id not found in rendered HTML: {start_id!r}")
    if scope_end is None:
        fail(f"scope end id not found after start id: {end_id!r}")
    return head_start, head_end, scope_start, scope_end


def copy_byte_range(
    source: Path,
    destination_handle: Any,
    start: int,
    end: int,
    *,
    byte_budget: int,
) -> int:
    if end < start:
        fail("bounded render end precedes its start")
    remaining = end - start
    if remaining > byte_budget:
        fail(
            f"bounded render segment is {remaining:,} bytes, exceeding "
            f"--max-render-bytes={byte_budget:,}; choose tighter scope IDs"
        )
    written = 0
    with source.open("rb") as handle:
        handle.seek(start)
        while remaining:
            chunk = handle.read(min(1024 * 1024, remaining))
            if not chunk:
                fail("render ended while extracting bounded HTML")
            destination_handle.write(chunk)
            written += len(chunk)
            remaining -= len(chunk)
    return written


def extract_bounded_html(
    source: Path,
    destination: Path,
    start_id: str,
    end_id: str,
    max_bytes: int,
    context_start_id: str | None = None,
) -> dict[str, Any]:
    """Preserve <head> and copy entry context plus [start-id, end-id)."""
    head_start, head_end, scope_start, scope_end = find_html_boundaries(
        source,
        start_id,
        end_id,
    )
    extraction_start = scope_start
    if context_start_id:
        _, _, context_start, context_end = find_html_boundaries(
            source,
            context_start_id,
            end_id,
        )
        if context_end != scope_end:
            fail("entry-context and target extractions resolved different ends")
        if context_start > scope_start:
            fail("--context-start-id must appear at or before --scope-start-id")
        extraction_start = context_start

    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as output:
        output.write(b"<!doctype html>\n<html>\n")
        head_bytes = copy_byte_range(
            source,
            output,
            head_start,
            head_end,
            byte_budget=max_bytes,
        )
        output.write(b"\n<body>\n")
        remaining_budget = max_bytes - head_bytes
        combined_bytes = copy_byte_range(
            source,
            output,
            extraction_start,
            scope_end,
            byte_budget=remaining_budget,
        )
        output.write(b"\n</body>\n</html>\n")
    final_size = destination.stat().st_size
    if final_size > max_bytes:
        destination.unlink(missing_ok=True)
        fail(
            f"bounded HTML is {final_size:,} bytes, exceeding "
            f"--max-render-bytes={max_bytes:,}; choose tighter scope IDs"
        )
    return {
        "method": (
            "id-bounded-html-with-entry-context"
            if extraction_start < scope_start
            else "id-bounded-html"
        ),
        "scope_start_id": start_id,
        "scope_end_id": end_id,
        "context_start_id": context_start_id or start_id,
        "end_semantics": "exclusive",
        "original_start_byte": extraction_start,
        "target_scope_start_byte": scope_start,
        "original_end_byte": scope_end,
        "head_bytes": head_bytes,
        "entry_context_bytes": scope_start - extraction_start,
        "target_scope_bytes": scope_end - scope_start,
        "scope_bytes": combined_bytes,
        "bounded_render_bytes": final_size,
    }


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def project_root_from_script() -> Path:
    """Return the project root for the canonical project-local skill."""
    script = Path(__file__).resolve()
    try:
        project_root = script.parents[4]
    except IndexError:
        fail(f"could not derive project root from skill path: {script}")
    if not (project_root / "AGENTS.md").is_file():
        fail(
            "prepare_review_package.py must run from the canonical project-local "
            f"skill; AGENTS.md was not found under {project_root}"
        )
    return project_root.resolve()


def validate_new_task_dir(raw_task_dir: Path) -> Path:
    """Require one new, direct child of the project's working directory."""
    if ".." in raw_task_dir.parts:
        fail("--task-dir must not contain '..'")

    project_root = project_root_from_script()
    working_root = (project_root / "working").resolve()
    if (project_root / "working").is_symlink():
        fail("canonical project working/ directory must not be a symlink")
    if not working_root.is_dir():
        fail(f"project working directory is missing: {working_root}")
    if working_root.parent != project_root:
        fail(f"project working directory resolves outside the project: {working_root}")

    candidate = raw_task_dir.expanduser()
    if not candidate.is_absolute():
        candidate = Path.cwd() / candidate
    if candidate.is_symlink():
        fail(f"--task-dir must not be a symlink: {candidate}")
    task_dir = candidate.resolve(strict=False)

    if task_dir == working_root:
        fail("--task-dir must name a task directory, not working/ itself")
    if task_dir.parent != working_root:
        fail(
            "--task-dir must be one direct child of the canonical project working "
            f"directory: {working_root}"
        )
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", task_dir.name):
        fail(
            "--task-dir name must be a lowercase task slug containing only "
            "letters, digits, underscores, and hyphens"
        )
    if task_dir.exists():
        fail(
            f"task directory already exists: {task_dir}; choose a new task slug "
            "and never merge a package into existing work"
        )
    return task_dir


def initialize_task_dir(task_dir: Path) -> Path:
    """Create a new output directory and its durable failure marker."""
    task_dir.mkdir(mode=0o700)
    incomplete_marker = task_dir / ".incomplete"
    try:
        incomplete_marker.write_text(
            "Review package creation did not complete. Inspect this directory; "
            "the helper will never delete or reuse it.\n",
            encoding="utf-8",
        )
    except BaseException:
        print(
            "prepare_review_package: could not write .incomplete; the new empty "
            f"package directory remains and must not be reused: {task_dir}",
            file=sys.stderr,
        )
        raise
    return incomplete_marker


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Freeze a chapter source, rendered HTML, and discoverable local assets "
            "into a machine-readable review package."
        )
    )
    parser.add_argument("--chapter-source", required=True, type=Path)
    parser.add_argument("--rendered-html", required=True, type=Path)
    parser.add_argument("--task-dir", required=True, type=Path)
    parser.add_argument("--mode", required=True, choices=MODES)
    parser.add_argument(
        "--review-stage",
        choices=REVIEW_STAGES,
        default="initial",
        help=(
            "Review lifecycle stage. Delta is allowed only for follow-up or "
            "post-revision review; initial reviews require Standard or Deep."
        ),
    )
    parser.add_argument("--action-scope", required=True, choices=ACTIONS)
    parser.add_argument("--scope-start", default="")
    parser.add_argument("--scope-end", default="")
    parser.add_argument(
        "--scope-start-id",
        help=(
            "HTML id at which bounded extraction begins. Must be paired with "
            "--scope-end-id."
        ),
    )
    parser.add_argument(
        "--scope-end-id",
        help=(
            "HTML id marking the exclusive end of bounded extraction. Must be "
            "paired with --scope-start-id."
        ),
    )
    parser.add_argument(
        "--context-start-id",
        help=(
            "Optional HTML id before --scope-start-id. Includes an entry-context "
            "collar in the frozen render while keeping the declared finding "
            "scope at --scope-start-id."
        ),
    )
    parser.add_argument(
        "--delta-basis",
        choices=("before-after-diff", "author-target", "bounded-current-section"),
    )
    parser.add_argument(
        "--reading-situation",
        choices=("pre-lecture", "post-lecture"),
        default="pre-lecture",
    )
    parser.add_argument("--prior-boundary", default="")
    parser.add_argument("--objective", action="append", default=[])
    parser.add_argument(
        "--objectives-source",
        choices=OBJECTIVE_SOURCES,
        default="chapter-inferred",
    )
    parser.add_argument(
        "--continuity-inputs-status",
        choices=CONTINUITY_STATUSES,
        default="limited-by-review-contract",
    )
    parser.add_argument(
        "--prerequisite-excerpt",
        action="append",
        nargs=4,
        metavar=("LABEL", "RENDERED_HTML", "START_ID", "END_ID"),
        default=[],
        help=(
            "Freeze one exact rendered prerequisite excerpt. Repeat for each "
            "explicit back-reference or inherited example assumption."
        ),
    )
    parser.add_argument(
        "--prerequisite-bundle-status",
        choices=PREREQUISITE_BUNDLE_STATUSES,
        default="not-required",
    )
    parser.add_argument(
        "--continuity-risk",
        choices=CONTINUITY_RISKS,
        default="normal",
        help=(
            "Use high when a bounded Standard target depends on several "
            "callbacks or materially imports prior assumptions."
        ),
    )
    parser.add_argument("--continuity-risk-reason", default="")
    parser.add_argument(
        "--role-continuity-status",
        action="append",
        default=[],
        metavar="ROLE=STATUS",
        help=(
            "Override continuity evidence status for one required role. STATUS "
            "is complete or limited-by-review-contract."
        ),
    )
    parser.add_argument(
        "--render-status",
        choices=RENDER_STATUSES,
        default="mtime-only",
        help=(
            "Freshness classification. verified-current additionally requires "
            "--freshness-evidence."
        ),
    )
    parser.add_argument("--freshness-evidence", default="")
    parser.add_argument(
        "--voice-clearance-mode",
        choices=VOICE_MODES,
        help="Defaults to required for revision scopes and optional for review-only.",
    )
    parser.add_argument("--voice-clearance-waiver-reason", default="")
    parser.add_argument("--companion-artifact", action="append", default=[])
    parser.add_argument("--existing-plan-owner", action="append", default=[])
    parser.add_argument(
        "--max-render-bytes",
        type=int,
        default=256 * 1024 * 1024,
        help=(
            "Maximum HTML bytes to copy (default: 268435456). Larger renders "
            "require paired scope IDs and the bounded result must also fit."
        ),
    )
    parser.add_argument(
        "--no-copy-assets",
        action="store_true",
        help="Copy only the HTML and mark the visual bundle text-only.",
    )
    return parser.parse_args()


def fail(message: str) -> "NoReturn":
    print(f"prepare_review_package: error: {message}", file=sys.stderr)
    raise SystemExit(2)


def main() -> int:
    args = parse_args()
    source = args.chapter_source.expanduser().resolve()
    html = args.rendered_html.expanduser().resolve()
    task_dir = validate_new_task_dir(args.task_dir)

    if not source.is_file():
        fail(f"chapter source is not a file: {source}")
    if not html.is_file():
        fail(f"rendered HTML is not a file: {html}")
    if source == html:
        fail("chapter source and rendered HTML must be different files")
    if args.mode == "delta" and args.review_stage == "initial":
        fail("initial reviews require Standard or Deep mode; Delta is follow-up only")
    if args.mode == "delta" and not args.delta_basis:
        fail("Delta mode requires --delta-basis")
    if args.mode != "delta" and args.delta_basis:
        fail("--delta-basis is valid only in Delta mode")
    if bool(args.scope_start_id) != bool(args.scope_end_id):
        fail("--scope-start-id and --scope-end-id must be supplied together")
    if args.context_start_id and not args.scope_start_id:
        fail("--context-start-id requires paired scope IDs")
    if args.max_render_bytes <= 0:
        fail("--max-render-bytes must be positive")
    if html.stat().st_size > args.max_render_bytes and not args.scope_start_id:
        fail(
            f"rendered HTML is {html.stat().st_size:,} bytes, exceeding "
            f"--max-render-bytes={args.max_render_bytes:,}; provide paired "
            "--scope-start-id/--scope-end-id anchors for bounded extraction"
        )
    if args.render_status == "verified-current" and not args.freshness_evidence.strip():
        fail("verified-current requires explicit --freshness-evidence")
    if args.continuity_risk == "high" and not args.continuity_risk_reason.strip():
        fail("high continuity risk requires --continuity-risk-reason")

    prerequisite_specs: list[dict[str, Any]] = []
    prerequisite_labels: set[str] = set()
    for label, raw_html, start_id, end_id in args.prerequisite_excerpt:
        if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", label):
            fail(
                "prerequisite labels must be lowercase slugs containing only "
                "letters, digits, underscores, and hyphens"
            )
        if label in prerequisite_labels:
            fail(f"duplicate prerequisite label: {label}")
        prerequisite_labels.add(label)
        prerequisite_html = Path(raw_html).expanduser().resolve()
        if not prerequisite_html.is_file():
            fail(f"prerequisite rendered HTML is not a file: {prerequisite_html}")
        prerequisite_specs.append(
            {
                "label": label,
                "html": prerequisite_html,
                "start_id": start_id,
                "end_id": end_id,
            }
        )
    if prerequisite_specs and args.prerequisite_bundle_status == "not-required":
        fail(
            "prerequisite excerpts require --prerequisite-bundle-status "
            "complete or limited"
        )
    if (
        args.prerequisite_bundle_status == "complete"
        and not prerequisite_specs
    ):
        fail("a complete prerequisite bundle must contain at least one excerpt")

    roles = required_roles(args.mode, args.continuity_risk)
    role_continuity: dict[str, str] = {
        role: args.continuity_inputs_status for role in roles
    }
    for override in args.role_continuity_status:
        if "=" not in override:
            fail("--role-continuity-status must use ROLE=STATUS")
        role, status = override.split("=", 1)
        if role not in role_continuity:
            fail(f"role continuity override names a non-required role: {role}")
        if status not in CONTINUITY_STATUSES:
            fail(
                f"invalid continuity status for {role}: {status}; expected one "
                f"of {', '.join(CONTINUITY_STATUSES)}"
            )
        role_continuity[role] = status
    if (
        args.continuity_inputs_status == "complete"
        and any(status != "complete" for status in role_continuity.values())
    ):
        fail(
            "global continuity status cannot be complete while a required role "
            "is limited"
        )

    voice_mode = args.voice_clearance_mode
    if voice_mode is None:
        voice_mode = "optional" if args.action_scope == "review-only" else "required"
    if voice_mode == "waived" and not args.voice_clearance_waiver_reason.strip():
        fail("waived voice clearance requires --voice-clearance-waiver-reason")

    incomplete_marker = initialize_task_dir(task_dir)
    try:
        extraction: dict[str, Any] | None = None
        render_input = html
        if args.scope_start_id:
            render_input = task_dir / ".bounded-render.input.html"
            extraction = extract_bounded_html(
                html,
                render_input,
                args.scope_start_id,
                args.scope_end_id,
                args.max_render_bytes,
                args.context_start_id,
            )

        assets: list[Path] = []
        missing_assets: list[str] = []
        remote_assets: list[str] = []
        if not args.no_copy_assets:
            assets, missing_assets, remote_assets = discover_assets(
                render_input,
                reference_base_dir=html.parent,
                excluded_paths={html, render_input},
            )

        render_root = html.parent

        source_destination = task_dir / "input" / "source" / source.name
        rendered_destination = (
            task_dir / "input" / "render" / html.relative_to(render_root)
        )
        copy_file(source, source_destination)
        copy_file(render_input, rendered_destination)
        if render_input != html:
            render_input.unlink()

        frozen_assets: list[dict[str, str]] = []
        for asset in assets:
            destination = task_dir / "input" / "render" / asset.relative_to(render_root)
            if destination == rendered_destination:
                missing_assets.append(
                    f"{asset} (asset destination collides with rendered artifact)"
                )
                continue
            copy_file(asset, destination)
            frozen_assets.append(
                {
                    "path": destination.relative_to(task_dir).as_posix(),
                    "sha256": sha256_file(destination),
                    "original_path": str(asset),
                }
            )

        frozen_prerequisites: list[dict[str, Any]] = []
        prerequisite_missing_assets: list[str] = []
        prerequisite_remote_assets: list[str] = []
        for spec in prerequisite_specs:
            label = spec["label"]
            prerequisite_html = spec["html"]
            prerequisite_input = task_dir / f".{label}.prerequisite.input.html"
            prerequisite_extraction = extract_bounded_html(
                prerequisite_html,
                prerequisite_input,
                spec["start_id"],
                spec["end_id"],
                args.max_render_bytes,
            )
            prerequisite_assets: list[Path] = []
            prerequisite_missing: list[str] = []
            prerequisite_remote: list[str] = []
            if not args.no_copy_assets:
                (
                    prerequisite_assets,
                    prerequisite_missing,
                    prerequisite_remote,
                ) = discover_assets(
                    prerequisite_input,
                    reference_base_dir=prerequisite_html.parent,
                    excluded_paths={prerequisite_html, prerequisite_input},
                )

            prerequisite_root = task_dir / "input" / "prerequisites" / label
            prerequisite_destination = prerequisite_root / prerequisite_html.name
            copy_file(prerequisite_input, prerequisite_destination)
            prerequisite_input.unlink()

            frozen_prerequisite_assets: list[dict[str, str]] = []
            for asset in prerequisite_assets:
                destination = (
                    prerequisite_root
                    / asset.relative_to(prerequisite_html.parent)
                )
                if destination == prerequisite_destination:
                    prerequisite_missing.append(
                        f"{asset} (asset destination collides with prerequisite)"
                    )
                    continue
                copy_file(asset, destination)
                frozen_prerequisite_assets.append(
                    {
                        "path": destination.relative_to(task_dir).as_posix(),
                        "sha256": sha256_file(destination),
                        "original_path": str(asset),
                    }
                )

            prerequisite_missing_assets.extend(prerequisite_missing)
            prerequisite_remote_assets.extend(prerequisite_remote)
            frozen_prerequisites.append(
                {
                    "label": label,
                    "path": prerequisite_destination.relative_to(task_dir).as_posix(),
                    "sha256": sha256_file(prerequisite_destination),
                    "original_path": str(prerequisite_html),
                    "start_id": spec["start_id"],
                    "end_id": spec["end_id"],
                    "extraction": prerequisite_extraction,
                    "assets": frozen_prerequisite_assets,
                    "missing_local_assets": sorted(set(prerequisite_missing)),
                    "remote_assets": sorted(set(prerequisite_remote)),
                }
            )

        if args.no_copy_assets:
            visual_status = "text-only"
        elif (
            missing_assets
            or remote_assets
            or prerequisite_missing_assets
            or prerequisite_remote_assets
        ):
            visual_status = "partial-assets"
        else:
            visual_status = "self-contained"

        source_stat = source.stat()
        html_stat = html.stat()
        mtime_relation = (
            "render-not-older-than-source"
            if html_stat.st_mtime_ns >= source_stat.st_mtime_ns
            else "render-older-than-source"
        )
        created_at = utc_now()
        source_relative = source_destination.relative_to(task_dir).as_posix()
        render_relative = rendered_destination.relative_to(task_dir).as_posix()
        source_hash = sha256_file(source_destination)
        render_hash = sha256_file(rendered_destination)

        contract = {
            "schema_version": 1,
            "created_at": created_at,
            "chapter_source": source_relative,
            "rendered_artifact": render_relative,
            "original_chapter_source": str(source),
            "original_rendered_artifact": str(html),
            "source_hash": source_hash,
            "render_hash": render_hash,
            "render_status": args.render_status,
            "render_freshness_evidence": {
                "method": (
                    "explicit"
                    if args.render_status == "verified-current"
                    else args.render_status
                ),
                "note": args.freshness_evidence,
                "source_mtime_ns": source_stat.st_mtime_ns,
                "render_mtime_ns": html_stat.st_mtime_ns,
                "mtime_relation": mtime_relation,
            },
            "render_extraction": extraction,
            "review_stage": args.review_stage,
            "scope_start": args.scope_start,
            "scope_end": args.scope_end,
            "entry_context_start": (
                args.context_start_id or args.scope_start_id or ""
            ),
            "entry_context_purpose": (
                "Judge target entry continuity without expanding finding scope."
                if args.context_start_id
                else ""
            ),
            "delta_basis": args.delta_basis,
            "baseline_source_hash": None,
            "visual_bundle_status": visual_status,
            "visual_bundle_limitations": {
                "missing_local_assets": sorted(
                    set(missing_assets + prerequisite_missing_assets)
                ),
                "remote_assets": sorted(
                    set(remote_assets + prerequisite_remote_assets)
                ),
            },
            "continuity_inputs_status": args.continuity_inputs_status,
            "prerequisite_bundle_status": args.prerequisite_bundle_status,
            "continuity_risk": args.continuity_risk,
            "continuity_risk_reason": args.continuity_risk_reason,
            "role_continuity_inputs": {
                role: {
                    "status": role_continuity[role],
                    "prerequisite_access": (
                        "cue-triggered"
                        if role in {"blind_student", "blind_student_1",
                                    "blind_student_2", "blind_continuity_reader"}
                        and frozen_prerequisites
                        else "full"
                        if frozen_prerequisites
                        else "none"
                    ),
                    "limitations": [],
                }
                for role in roles
            },
            "reading_situation": args.reading_situation,
            "prior_boundary": args.prior_boundary,
            "objectives_source": args.objectives_source,
            "objectives": args.objective,
            "mode": args.mode,
            "action_scope": args.action_scope,
            "voice_clearance_mode": voice_mode,
            "voice_clearance_waiver_reason": args.voice_clearance_waiver_reason,
            "run_status": "pending",
            "required_roles": roles,
            "missing_required_roles": roles,
            "companion_artifacts": args.companion_artifact,
            "existing_plan_owners": args.existing_plan_owner,
            "deterministic_checks": {},
            "frozen_inputs": {
                "source": {
                    "path": source_relative,
                    "sha256": source_hash,
                    "original_path": str(source),
                },
                "render": {
                    "path": render_relative,
                    "sha256": render_hash,
                    "original_path": str(html),
                },
                "assets": frozen_assets,
                "prerequisites": frozen_prerequisites,
            },
        }

        role_state = {
            role: {
                "required": True,
                "status": "pending",
                "artifact": f"reports/{role}.md",
                "completed_at": None,
            }
            for role in roles
        }
        status = {
            "schema_version": 1,
            "updated_at": created_at,
            "run_status": "pending",
            "compiled_at": None,
            "roles": role_state,
            "missing_required_roles": roles,
            "late_reports": [],
            "artifacts": {
                "findings": "findings.yml",
                "decisions": "decisions.yml",
                "final_report": "student_review.md",
            },
        }
        findings = {
            "schema_version": 1,
            "findings": [],
            "revision": None,
            "voice_pack_maintenance": {
                "status": "pending",
                "candidates": [],
                "author_decisions": [],
            },
        }
        decisions = {"schema_version": 1, "decisions": []}

        write_machine_yaml(task_dir / "review_contract.yml", contract)
        write_machine_yaml(task_dir / "run_status.yml", status)
        write_machine_yaml(task_dir / "findings.yml", findings)
        write_machine_yaml(task_dir / "decisions.yml", decisions)
        (task_dir / "reports").mkdir(exist_ok=False)
    except BaseException:
        print(
            "prepare_review_package: incomplete package left in place for "
            f"inspection: {task_dir}",
            file=sys.stderr,
        )
        raise

    incomplete_marker.unlink()

    print(f"Prepared review package: {task_dir}")
    print(f"Render status: {args.render_status} ({mtime_relation})")
    print(f"Visual bundle: {visual_status}")
    print(f"Required roles: {', '.join(roles) if roles else '(none)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
