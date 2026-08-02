#!/usr/bin/env python3
"""Safety regression tests for prepare_review_package.py.

Run only from a disposable copy of the project-local skill under
``/private/tmp``. Create ``.book-review-disposable-test-root`` in that copy and
set ``BOOK_REVIEW_DISPOSABLE_TEST_ROOT`` to the copy's project root. Missing or
invalid guards fail the suite rather than skipping it.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import uuid


SCRIPT = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT.parents[4]
HELPER = SCRIPT.with_name("prepare_review_package.py")
WORKING_ROOT = PROJECT_ROOT / "working"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def project_manifest_excluding(excluded: Path) -> dict[str, str]:
    """Describe every project entry except one declared output subtree."""
    manifest: dict[str, str] = {}
    excluded = excluded.resolve(strict=False)
    for path in PROJECT_ROOT.rglob("*"):
        resolved = path.resolve(strict=False)
        if resolved == excluded or excluded in resolved.parents:
            continue
        relative = path.relative_to(PROJECT_ROOT).as_posix()
        if path.is_symlink():
            manifest[relative] = f"symlink:{os.readlink(path)}"
        elif path.is_file():
            manifest[relative] = f"file:{path.stat().st_mode:o}:{sha256(path)}"
        elif path.is_dir():
            manifest[relative] = f"directory:{path.stat().st_mode:o}"
        else:
            manifest[relative] = f"other:{path.lstat().st_mode:o}"
    return manifest


class PrepareReviewPackageSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        declared_root = os.environ.get("BOOK_REVIEW_DISPOSABLE_TEST_ROOT")
        if not declared_root or Path(declared_root).resolve() != PROJECT_ROOT.resolve():
            raise RuntimeError(
                "refusing to run outside a declared disposable project copy"
            )
        private_tmp = Path("/private/tmp").resolve()
        try:
            PROJECT_ROOT.resolve().relative_to(private_tmp)
        except ValueError:
            raise RuntimeError(
                f"refusing to run outside {private_tmp}: {PROJECT_ROOT.resolve()}"
            )
        if not (PROJECT_ROOT / ".book-review-disposable-test-root").is_file():
            raise RuntimeError("disposable project marker is missing")
        if not (PROJECT_ROOT / "AGENTS.md").is_file():
            raise RuntimeError("disposable project copy is missing AGENTS.md")
        WORKING_ROOT.mkdir(exist_ok=True)
        (PROJECT_ROOT / ".test-fixtures").mkdir(exist_ok=True)

    def setUp(self) -> None:
        self.fixture = tempfile.TemporaryDirectory(
            prefix="book-review-package-fixture-",
            dir=PROJECT_ROOT / ".test-fixtures",
        )
        self.fixture_root = Path(self.fixture.name)
        self.source = self.fixture_root / "chapter.qmd"
        self.render_dir = self.fixture_root / "render"
        self.assets_dir = self.render_dir / "assets"
        self.html = self.render_dir / "chapter.html"
        self.prerequisite_render_dir = self.fixture_root / "prior-render"
        self.prerequisite_html = (
            self.prerequisite_render_dir / "prior-chapter.html"
        )
        self.source.write_text(
            "---\ntitle: Safety fixture\n---\n\n# Start\n\nFixture prose.\n",
            encoding="utf-8",
        )
        self.assets_dir.mkdir(parents=True)
        (self.assets_dir / "site.css").write_text(
            "body { background-image: url('texture.txt'); }\n",
            encoding="utf-8",
        )
        (self.assets_dir / "texture.txt").write_text("texture\n", encoding="utf-8")
        (self.assets_dir / "texture with (detail).txt").write_text(
            "detailed texture\n",
            encoding="utf-8",
        )
        (self.assets_dir / "figure.txt").write_text("figure\n", encoding="utf-8")
        self.html.write_text(
            """<!doctype html>
<html>
<head><link rel="stylesheet" href="assets/site.css"></head>
<body>
<div id="chapter-entry"><p>Chapter opening context.</p></div>
<section id="start-here"><h1>Start</h1>
<img src="assets/figure.txt"><p>Fixture text.</p></section>
<section id="stop-here"><h1>Stop</h1></section>
</body>
</html>
""",
            encoding="utf-8",
        )
        self.prerequisite_render_dir.mkdir()
        (self.prerequisite_render_dir / "prior.css").write_text(
            "body { color: #222; }\n",
            encoding="utf-8",
        )
        self.prerequisite_html.write_text(
            """<!doctype html>
<html>
<head><link rel="stylesheet" href="prior.css"></head>
<body>
<section id="prior-start"><h1>Prior definition</h1>
<p>The exact prerequisite rule.</p></section>
<section id="prior-end"><h1>Later material</h1></section>
</body>
</html>
""",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.fixture.cleanup()

    def slug(self, prefix: str) -> str:
        return f"{prefix}_{uuid.uuid4().hex[:10]}"

    def run_helper(
        self,
        task_dir: Path,
        *extra: str,
        review_stage: str = "post-revision",
        mode: str = "delta",
    ) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(HELPER),
            "--chapter-source",
            str(self.source),
            "--rendered-html",
            str(self.html),
            "--task-dir",
            str(task_dir),
            "--mode",
            mode,
            "--review-stage",
            review_stage,
            "--action-scope",
            "apply-and-verify",
            "--max-render-bytes",
            "4096",
        ]
        if mode == "delta":
            command.extend(["--delta-basis", "bounded-current-section"])
        command.extend(extra)
        environment = dict(os.environ)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            command,
            cwd=self.fixture_root,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_helper_contains_no_recursive_delete_or_merge_override(self) -> None:
        source = HELPER.read_text(encoding="utf-8")
        self.assertNotIn("rmtree(", source)
        self.assertNotIn("shutil.rmtree", source)
        self.assertNotIn("--allow-nonempty", source)

    def test_deep_mode_uses_the_lean_initial_screen(self) -> None:
        task_dir = WORKING_ROOT / self.slug("deep_lean")
        result = self.run_helper(
            task_dir,
            mode="deep",
            review_stage="initial",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        contract = json.loads((task_dir / "review_contract.yml").read_text())
        self.assertEqual(
            contract["required_roles"],
            ["blind_student", "technical_auditor"],
        )

    def test_success_is_contained_and_removes_only_incomplete_marker(self) -> None:
        task_dir = WORKING_ROOT / self.slug("success")
        before = project_manifest_excluding(task_dir)

        result = self.run_helper(task_dir)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((task_dir / "review_contract.yml").is_file())
        self.assertTrue((task_dir / "run_status.yml").is_file())
        self.assertTrue((task_dir / "input" / "source" / "chapter.qmd").is_file())
        self.assertFalse((task_dir / ".incomplete").exists())
        self.assertEqual(before, project_manifest_excluding(task_dir))

    def test_bounded_success_covers_the_original_post_build_failure_path(self) -> None:
        task_dir = WORKING_ROOT / self.slug("bounded")
        original_html = self.html.read_text(encoding="utf-8")
        self.html.write_text(
            original_html.replace(
                "<body>",
                """<body>
<div data-id="start-here">fake data attribute before scope</div>
<div data-template="<section id='start-here'>">fake quoted attribute before scope</div>
<!-- <section id="start-here">fake comment before scope</section> -->
<script>const fake = '<section id="start-here">fake script before scope</section>';</script>""",
            ).replace(
                '<img src="assets/figure.txt">',
                '<img src="assets/figure.txt"><iframe src="chapter.html"></iframe>',
            ),
            encoding="utf-8",
        )

        result = self.run_helper(
            task_dir,
            "--scope-start-id",
            "start-here",
            "--scope-end-id",
            "stop-here",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        rendered = task_dir / "input" / "render" / "chapter.html"
        self.assertTrue(rendered.is_file())
        text = rendered.read_text(encoding="utf-8")
        self.assertIn("start-here", text)
        self.assertNotIn("stop-here", text)
        self.assertNotIn("fake data attribute before scope", text)
        self.assertNotIn("fake quoted attribute before scope", text)
        self.assertNotIn("fake comment before scope", text)
        self.assertNotIn("fake script before scope", text)
        self.assertFalse((task_dir / ".bounded-render.input.html").exists())
        self.assertFalse((task_dir / ".incomplete").exists())
        contract = json.loads((task_dir / "review_contract.yml").read_text())
        self.assertEqual(contract["render_extraction"]["method"], "id-bounded-html")
        self.assertEqual(contract["render_hash"], sha256(rendered))

    def test_bounded_entry_context_is_frozen_but_target_stays_separate(self) -> None:
        task_dir = WORKING_ROOT / self.slug("entry_context")

        result = self.run_helper(
            task_dir,
            "--scope-start-id",
            "start-here",
            "--scope-end-id",
            "stop-here",
            "--context-start-id",
            "chapter-entry",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        rendered = task_dir / "input" / "render" / "chapter.html"
        text = rendered.read_text(encoding="utf-8")
        self.assertIn("Chapter opening context.", text)
        self.assertIn("Fixture text.", text)
        self.assertNotIn("stop-here", text)
        contract = json.loads((task_dir / "review_contract.yml").read_text())
        extraction = contract["render_extraction"]
        self.assertEqual(
            extraction["method"],
            "id-bounded-html-with-entry-context",
        )
        self.assertEqual(extraction["context_start_id"], "chapter-entry")
        self.assertEqual(extraction["scope_start_id"], "start-here")
        self.assertGreater(extraction["entry_context_bytes"], 0)
        self.assertEqual(contract["entry_context_start"], "chapter-entry")

    def test_prerequisite_bundle_and_lean_roles_are_frozen(self) -> None:
        task_dir = WORKING_ROOT / self.slug("prerequisites")

        result = self.run_helper(
            task_dir,
            "--prerequisite-excerpt",
            "prior-rule",
            str(self.prerequisite_html),
            "prior-start",
            "prior-end",
            "--prerequisite-bundle-status",
            "complete",
            "--continuity-risk",
            "high",
            "--continuity-risk-reason",
            "The target imports several prior assumptions.",
            "--continuity-inputs-status",
            "complete",
            mode="standard",
            review_stage="initial",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        contract = json.loads((task_dir / "review_contract.yml").read_text())
        self.assertEqual(contract["prerequisite_bundle_status"], "complete")
        self.assertEqual(contract["continuity_risk"], "high")
        self.assertEqual(
            contract["required_roles"],
            ["blind_student", "technical_auditor"],
        )
        prerequisite = contract["frozen_inputs"]["prerequisites"][0]
        frozen = task_dir / prerequisite["path"]
        self.assertTrue(frozen.is_file())
        self.assertEqual(prerequisite["sha256"], sha256(frozen))
        text = frozen.read_text(encoding="utf-8")
        self.assertIn("The exact prerequisite rule.", text)
        self.assertNotIn("Later material", text)
        self.assertTrue(prerequisite["assets"])
        self.assertEqual(
            contract["role_continuity_inputs"]["blind_student"][
                "prerequisite_access"
            ],
            "cue-triggered",
        )
        self.assertEqual(
            contract["role_continuity_inputs"]["technical_auditor"][
                "prerequisite_access"
            ],
            "full",
        )

    def test_initial_review_rejects_delta_before_creating_task_dir(self) -> None:
        task_dir = WORKING_ROOT / self.slug("initial_delta")

        result = self.run_helper(task_dir, review_stage="initial")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("initial reviews require Standard or Deep", result.stderr)
        self.assertFalse(task_dir.exists())

    def test_failure_leaves_a_visible_partial_package_without_cleanup(self) -> None:
        task_dir = WORKING_ROOT / self.slug("incomplete")
        before = project_manifest_excluding(task_dir)

        result = self.run_helper(
            task_dir,
            "--scope-start-id",
            "start-here",
            "--scope-end-id",
            "missing-end",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(task_dir.is_dir())
        self.assertTrue((task_dir / ".incomplete").is_file())
        self.assertIn("incomplete package left in place", result.stderr)
        self.assertEqual(before, project_manifest_excluding(task_dir))

    def test_asset_traversal_and_symlink_escape_are_not_copied(self) -> None:
        secret = self.fixture_root / "secret.txt"
        secret.write_text("do not package\n", encoding="utf-8")
        (self.assets_dir / "secret-link.txt").symlink_to(secret)
        html_text = self.html.read_text(encoding="utf-8")
        self.html.write_text(
            html_text.replace(
                '<img src="assets/figure.txt">',
                (
                    '<img src="assets/figure.txt">'
                    '<img src="../secret.txt">'
                    '<img src="assets/secret-link.txt">'
                ),
            ),
            encoding="utf-8",
        )
        task_dir = WORKING_ROOT / self.slug("asset_escape")

        result = self.run_helper(task_dir)

        self.assertEqual(result.returncode, 0, result.stderr)
        packaged_text = "\n".join(
            path.read_text(encoding="utf-8", errors="replace")
            for path in task_dir.rglob("*")
            if path.is_file()
        )
        self.assertNotIn("do not package", packaged_text)
        contract = json.loads((task_dir / "review_contract.yml").read_text())
        limitations = contract["visual_bundle_limitations"]["missing_local_assets"]
        self.assertEqual(contract["visual_bundle_status"], "partial-assets")
        self.assertTrue(
            all("outside rendered-artifact directory" in item for item in limitations)
        )

    def test_existing_directory_is_refused_even_when_empty(self) -> None:
        task_dir = WORKING_ROOT / self.slug("existing")
        task_dir.mkdir()
        sentinel = task_dir / "keep.txt"
        sentinel.write_text("preserve me\n", encoding="utf-8")

        result = self.run_helper(task_dir)

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "preserve me\n")
        self.assertNotIn("Prepared review package", result.stdout)

    def test_marker_write_failure_leaves_the_new_empty_directory(self) -> None:
        task_dir = WORKING_ROOT / self.slug("marker_failure")
        before = project_manifest_excluding(task_dir)
        spec = importlib.util.spec_from_file_location("prepare_review_package", HELPER)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with mock.patch.object(Path, "write_text", side_effect=OSError("fixture")):
            with self.assertRaises(OSError):
                module.initialize_task_dir(task_dir)

        self.assertTrue(task_dir.is_dir())
        self.assertEqual(list(task_dir.iterdir()), [])
        self.assertEqual(before, project_manifest_excluding(task_dir))

    def test_quoted_css_asset_with_spaces_and_parentheses_is_copied(self) -> None:
        css = self.assets_dir / "site.css"
        css.write_text(
            'body { background-image: url("texture with (detail).txt"); }\n',
            encoding="utf-8",
        )
        task_dir = WORKING_ROOT / self.slug("quoted_css")

        result = self.run_helper(task_dir)

        self.assertEqual(result.returncode, 0, result.stderr)
        copied = (
            task_dir
            / "input"
            / "render"
            / "assets"
            / "texture with (detail).txt"
        )
        self.assertTrue(copied.is_file())
        contract = json.loads((task_dir / "review_contract.yml").read_text())
        self.assertEqual(contract["visual_bundle_status"], "self-contained")

    def test_data_url_srcset_does_not_create_a_false_missing_asset(self) -> None:
        html_text = self.html.read_text(encoding="utf-8")
        self.html.write_text(
            html_text.replace(
                '<img src="assets/figure.txt">',
                (
                    '<img src="assets/figure.txt" '
                    'srcset="data:image/png;base64,AAAA 1x">'
                ),
            ),
            encoding="utf-8",
        )
        task_dir = WORKING_ROOT / self.slug("data_srcset")

        result = self.run_helper(task_dir)

        self.assertEqual(result.returncode, 0, result.stderr)
        contract = json.loads((task_dir / "review_contract.yml").read_text())
        self.assertEqual(contract["visual_bundle_status"], "self-contained")
        self.assertEqual(
            contract["visual_bundle_limitations"]["missing_local_assets"],
            [],
        )

    def test_srcset_candidate_after_descriptorless_data_url_is_checked(self) -> None:
        html_text = self.html.read_text(encoding="utf-8")
        self.html.write_text(
            html_text.replace(
                '<img src="assets/figure.txt">',
                (
                    '<img src="assets/figure.txt" '
                    'srcset="data:image/png;base64,AAAA, missing.png 2x">'
                ),
            ),
            encoding="utf-8",
        )
        task_dir = WORKING_ROOT / self.slug("mixed_data_srcset")

        result = self.run_helper(task_dir)

        self.assertEqual(result.returncode, 0, result.stderr)
        contract = json.loads((task_dir / "review_contract.yml").read_text())
        self.assertEqual(contract["visual_bundle_status"], "partial-assets")
        limitations = contract["visual_bundle_limitations"]["missing_local_assets"]
        self.assertTrue(any(item.endswith("/missing.png") for item in limitations))

    def test_commas_inside_data_url_payload_are_not_local_candidates(self) -> None:
        html_text = self.html.read_text(encoding="utf-8")
        self.html.write_text(
            html_text.replace(
                '<img src="assets/figure.txt">',
                (
                    '<img src="assets/figure.txt" '
                    'srcset="data:text/plain,a,b 1x">'
                ),
            ),
            encoding="utf-8",
        )
        task_dir = WORKING_ROOT / self.slug("comma_data_srcset")

        result = self.run_helper(task_dir)

        self.assertEqual(result.returncode, 0, result.stderr)
        contract = json.loads((task_dir / "review_contract.yml").read_text())
        self.assertEqual(contract["visual_bundle_status"], "self-contained")
        self.assertEqual(
            contract["visual_bundle_limitations"]["missing_local_assets"],
            [],
        )

    def test_dangerous_and_escaping_destinations_are_refused(self) -> None:
        outside = self.fixture_root / "outside"
        nested = WORKING_ROOT / self.slug("parent") / "child"
        traversal = WORKING_ROOT / ".." / "working" / self.slug("traversal")
        destinations = [
            PROJECT_ROOT,
            WORKING_ROOT,
            outside,
            nested,
            traversal,
        ]

        for destination in destinations:
            with self.subTest(destination=destination):
                result = self.run_helper(destination)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Prepared review package", result.stdout)

    def test_symlink_escape_is_refused(self) -> None:
        outside = self.fixture_root / "symlink-target"
        outside.mkdir()
        link = WORKING_ROOT / self.slug("escape")
        link.symlink_to(outside, target_is_directory=True)

        result = self.run_helper(link)

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(outside.iterdir()), [])

    def test_dangling_task_symlink_is_refused_without_creating_its_target(self) -> None:
        target = WORKING_ROOT / self.slug("dangling_target")
        link = WORKING_ROOT / self.slug("dangling_link")
        link.symlink_to(target, target_is_directory=True)

        result = self.run_helper(link)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--task-dir must not be a symlink", result.stderr)
        self.assertTrue(link.is_symlink())
        self.assertFalse(target.exists())

    def test_symlinked_working_root_is_refused(self) -> None:
        alternate = self.fixture_root / "alternate-project"
        alternate_helper = (
            alternate
            / ".agents"
            / "skills"
            / "book-student-review"
            / "scripts"
            / "prepare_review_package.py"
        )
        alternate_helper.parent.mkdir(parents=True)
        shutil.copy2(HELPER, alternate_helper)
        (alternate / "AGENTS.md").write_text("fixture\n", encoding="utf-8")
        outside_working = self.fixture_root / "outside-working"
        outside_working.mkdir()
        (alternate / "working").symlink_to(outside_working, target_is_directory=True)
        destination = outside_working / self.slug("escaped")
        command = [
            sys.executable,
            str(alternate_helper),
            "--chapter-source",
            str(self.source),
            "--rendered-html",
            str(self.html),
            "--task-dir",
            str(destination),
            "--mode",
            "lint",
            "--action-scope",
            "review-only",
        ]

        result = subprocess.run(
            command,
            cwd=self.fixture_root,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("working/ directory must not be a symlink", result.stderr)
        self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
