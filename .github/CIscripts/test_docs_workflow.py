import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml


WORKFLOW = Path(__file__).resolve().parents[1] / "workflows/Docs.yml"


class RevisionGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        steps = yaml.safe_load(WORKFLOW.read_text())["jobs"]["deploy"]["steps"]
        cls.guard = next(step for step in steps if step.get("id") == "revision")
        cls.following_steps = steps[steps.index(cls.guard) + 1:]

    def check_revision(self, ref, revision, head, exit_code=0):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "output"
            environment = {
                **os.environ,
                "GITHUB_REF": ref,
                "GITHUB_SHA": revision,
                "GITHUB_OUTPUT": str(output),
                "TEST_HEAD": head,
                "TEST_GIT_EXIT": str(exit_code),
            }
            script = (
                'git() { printf "%s\\trefs/heads/develop\\n" "$TEST_HEAD"; '
                'return "$TEST_GIT_EXIT"; }\n' + self.guard["run"]
            )
            result = subprocess.run(
                ["bash", "-e", "-o", "pipefail", "-c", script],
                env=environment, capture_output=True, text=True,
            )
            return result, output.read_text() if output.exists() else ""

    def test_current_develop_revision_is_published(self):
        result, output = self.check_revision("refs/heads/develop", "new", "new")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output, "publish=true\n")

    def test_older_develop_build_finishing_later_is_skipped(self):
        self.check_revision("refs/heads/develop", "new", "new")
        result, output = self.check_revision("refs/heads/develop", "old", "new")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(output, "publish=false\n")
        self.assertIn("Skipping superseded", result.stdout)

    def test_tag_snapshots_do_not_query_develop(self):
        for tag in ("v3.0.0", "docs-test"):
            result, output = self.check_revision(f"refs/tags/{tag}", "old", "new", 1)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(output, "publish=true\n")

    def test_remote_lookup_failure_stops_deployment(self):
        result, output = self.check_revision("refs/heads/develop", "new", "", 2)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output, "")

    def test_every_publishing_step_checks_revision(self):
        self.assertTrue(self.following_steps)
        for step in self.following_steps:
            with self.subTest(step=step["name"]):
                self.assertIn("steps.revision.outputs.publish == 'true'", step["if"])


if __name__ == "__main__":
    unittest.main()
