import json
import tempfile
import unittest
from pathlib import Path

from publish_docs import LEGACY_BASE, assemble


class PublishingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "build"
        self.source.mkdir()
        (self.source / "index.html").write_text("new documentation")
        self.site = self.root / "site"
        self.legacy = Path(__file__).resolve().parents[2] / "docs/_static/legacy-versions.json"
        self.base = "https://example.github.io/MaCh3/"

    def publish(self, version, **options):
        assemble(self.source, self.site, version, self.base, self.legacy, **options)
        return json.loads((self.site / "versions.json").read_text())

    def test_development_default_and_legacy_entries(self):
        manifest = self.publish("develop")
        self.assertIn(self.base + "develop/", (self.site / "index.html").read_text())
        self.assertTrue(manifest[0]["preferred"])
        self.assertEqual(manifest[0]["name"], "develop")
        self.assertEqual(manifest[1:], json.loads(self.legacy.read_text()))
        self.assertTrue((self.site / ".nojekyll").is_file())

    def test_releases_are_preserved_and_default_is_highest_stable(self):
        self.publish("develop")
        self.publish("v3.9.0")
        (self.source / "index.html").write_text("v3.10")
        self.publish("v3.10.0")
        self.publish("v4.0.0-rc.1")
        manifest = self.publish("v3.8.0")
        self.assertIn(self.base + "v3.10.0/", (self.site / "index.html").read_text())
        self.assertEqual(sum(bool(entry.get("preferred")) for entry in manifest), 1)
        self.assertEqual((self.site / "v3.9.0/index.html").read_text(), "new documentation")
        self.assertEqual((self.site / "v3.10.0/index.html").read_text(), "v3.10")
        self.assertNotIn("(stable)", next(e["name"] for e in manifest if e["version"] == "v3.9.0"))

    def test_prereleases_do_not_replace_development_default(self):
        self.publish("develop")
        self.publish("v3.0.0-rc.10")
        manifest = self.publish("v3.0.0-rc.2")
        self.assertIn(self.base + "develop/", (self.site / "index.html").read_text())
        self.assertEqual(manifest[1]["version"], "v3.0.0-rc.10")

    def test_first_prerelease_is_browsable_without_development(self):
        self.publish("v3.0.0-rc.1")
        self.assertIn(self.base + "v3.0.0-rc.1/", (self.site / "index.html").read_text())

    def test_docs_test_snapshot_appears_without_replacing_development_default(self):
        self.publish("develop")
        manifest = self.publish("docs-test")
        self.assertEqual([entry["version"] for entry in manifest[:2]], ["develop", "docs-test"])
        snapshot = manifest[1]
        self.assertEqual(snapshot["name"], "docs-test")
        self.assertEqual(snapshot["url"], self.base + "docs-test/")
        self.assertFalse(snapshot.get("preferred", False))
        self.assertEqual((self.site / "docs-test/index.html").read_text(), "new documentation")
        self.assertIn(self.base + "develop/", (self.site / "index.html").read_text())

    def test_docs_test_survives_release_and_development_deployments(self):
        self.publish("docs-test")
        self.publish("v3.0.0")
        manifest = self.publish("develop")
        self.assertEqual(
            [entry["version"] for entry in manifest[:3]], ["develop", "v3.0.0", "docs-test"],
        )
        self.assertIn(self.base + "v3.0.0/", (self.site / "index.html").read_text())
        self.assertTrue((self.site / "docs-test/index.html").is_file())

    def test_docs_test_can_be_published_first(self):
        manifest = self.publish("docs-test")
        self.assertTrue(manifest[0]["preferred"])
        self.assertIn(self.base + "docs-test/", (self.site / "index.html").read_text())

    def test_republishing_replaces_only_the_selected_version(self):
        self.publish("v3.0.0")
        self.publish("develop")
        (self.site / "develop/removed.html").touch()
        (self.source / "index.html").write_text("updated")
        self.publish("develop")
        self.assertFalse((self.site / "develop/removed.html").exists())
        self.assertEqual((self.site / "v3.0.0/index.html").read_text(), "new documentation")

    def test_sphinx_release_supersedes_matching_legacy_entry(self):
        manifest = self.publish("v2.7.0")
        entries = [entry for entry in manifest if entry["version"] == "v2.7.0"]
        self.assertEqual(len(entries), 1)
        self.assertFalse(entries[0].get("legacy", False))

    def test_upstream_requires_complete_legacy_snapshot(self):
        self.base = LEGACY_BASE
        with self.assertRaisesRegex(ValueError, "legacy gh-pages checkout"):
            self.publish("develop", preserve_legacy=True)
        self.assertFalse((self.site / "develop").exists())

    def test_upstream_missing_archive_fails_before_copying(self):
        old_site = self.root / "old-site"
        old_site.mkdir()
        (old_site / "index.html").write_text("legacy")
        with self.assertRaisesRegex(ValueError, "Missing legacy archive"):
            self.publish("develop", preserve_legacy=True, legacy_site=old_site)
        self.assertFalse((self.site / "legacy/develop").exists())

    def test_newer_legacy_entries_survive_an_older_release_build(self):
        manifest = self.publish("develop")
        extra = {
            "version": "v1.0.0", "name": "v1.0.0 (Doxygen)",
            "url": "https://example.org/v1.0.0/", "legacy": True,
        }
        manifest.append(extra)
        (self.site / "versions.json").write_text(json.dumps(manifest))
        self.assertIn(extra, self.publish("v3.0.0"))

    def test_upstream_archives_survive_later_deployments(self):
        self.base = LEGACY_BASE
        old_site = self.root / "old-site"
        old_site.mkdir()
        (old_site / "index.html").write_text("old development")
        (old_site / "jquery.js").write_text("old asset")
        (old_site / ".git").write_text("must not copy")
        for entry in json.loads(self.legacy.read_text()):
            if entry["version"] != "legacy-develop":
                archive = old_site / ".Archive" / entry["version"]
                archive.mkdir(parents=True)
                (archive / "index.html").write_text(entry["version"])
        self.publish("develop", preserve_legacy=True, legacy_site=old_site)
        manifest = self.publish("v3.0.0", preserve_legacy=True)
        self.assertEqual((self.site / "legacy/develop/index.html").read_text(), "old development")
        self.assertTrue((self.site / "legacy/develop/jquery.js").is_file())
        self.assertFalse((self.site / "legacy/develop/.git").exists())
        self.assertEqual((self.site / ".Archive/v2.7.0/index.html").read_text(), "v2.7.0")
        legacy_develop = next(e for e in manifest if e["version"] == "legacy-develop")
        self.assertEqual(legacy_develop["url"], self.base + "legacy/develop/index.html")

    def test_invalid_versions_and_missing_build_fail_explicitly(self):
        for version in ("../escape", ".git", "v3", "v3.0.0/extra"):
            with self.subTest(version=version), self.assertRaises(ValueError):
                self.publish(version)
        (self.source / "index.html").unlink()
        with self.assertRaisesRegex(ValueError, "No built documentation"):
            self.publish("develop")

    def test_overlapping_source_and_destination_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            assemble(self.source, self.source, "develop", self.base, self.legacy)


if __name__ == "__main__":
    unittest.main()
