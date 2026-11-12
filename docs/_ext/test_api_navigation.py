import re
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from sphinx.errors import ExtensionError

from api_navigation import ENTITY_TITLES, generate_navigation


class NavigationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.api = Path(self.temporary.name)
        self.nodes = []
        self.listing = self.api / "unabridged_api.rst.include"
        self.orphan = self.api / "unabridged_orphan.rst"
        self.root_page = self.api / "library_root.rst"
        self.app = SimpleNamespace(exhale_root=SimpleNamespace(
            root_directory=str(self.api),
            full_root_file_path=str(self.root_page),
            unabridged_api_file=str(self.listing),
            unabridged_orphan_file=str(self.orphan),
            all_nodes=self.nodes,
        ))

    def node(self, name, kind="class", location=None):
        filename = f"{kind}_{len(self.nodes)}.rst"
        node = SimpleNamespace(
            name=name, kind=kind, file_name=filename,
            def_in_file=SimpleNamespace(location=location) if location else None,
        )
        if kind == "file":
            node.location = location
        self.nodes.append(node)
        (self.api / filename).write_text(f"{name}\n{'=' * len(name)}\n")
        return node

    def generate(self):
        self.root_page.write_text(
            "C++ API\n=======\n\n"
            ".. include:: page_view_hierarchy.rst.include\n\n"
            ".. include:: class_view_hierarchy.rst.include\n\n"
            ".. include:: file_view_hierarchy.rst.include\n\n"
            ".. include:: unabridged_api.rst.include\n"
        )
        self.listing.write_text(".. toctree::\n\n" + "".join(
            f"   {node.file_name}\n" for node in self.nodes if node.kind not in ("file", "dir")
        ))
        self.orphan.write_text(":orphan:\n\n.. toctree::\n\n" + "".join(
            f"   {node.file_name}\n" for node in self.nodes if node.kind in ("file", "dir")
        ))
        generate_navigation(self.app)

    def test_source_directory_section_precedes_preserved_hierarchies(self):
        self.node("Handler", location="Samples/Handler.h")
        self.generate()
        content = self.root_page.read_text()
        includes = re.findall(r"^\.\. include:: (.+)$", content, re.MULTILINE)
        self.assertEqual(includes, [
            self.listing.name,
            "page_view_hierarchy.rst.include",
            "class_view_hierarchy.rst.include",
            "file_view_hierarchy.rst.include",
        ])
        self.assertTrue(content.startswith("C++ API\n=======\n\n"))

    def test_nested_directories_and_alphabetical_entities(self):
        zeta = self.node("Zeta", location="Fitters/Algorithms/Zeta.h")
        alpha = self.node("Alpha", location="Fitters/Algorithms/Alpha.h")
        self.node("Handler", location="Parameters/Handler.h")
        self.generate()
        self.assertIn("_navigation/symbols/Fitters/index.rst", self.listing.read_text())
        fitters = self.api / "_navigation/symbols/Fitters/index.rst"
        self.assertIn("Algorithms/index.rst", fitters.read_text())
        algorithms = fitters.parent / "Algorithms/index.rst"
        self.assertIn("Classes\n-------", algorithms.read_text())
        self.assertLess(algorithms.read_text().index(alpha.file_name), algorithms.read_text().index(zeta.file_name))
        self.assertNotIn("class_", self.listing.read_text())

    def test_entity_types_are_separate_and_empty_categories_are_omitted(self):
        examples = [
            self.node("AClass", kind="class", location="Samples/A.h"),
            self.node("AStruct", kind="struct", location="Samples/A.h"),
            self.node("AFunction", kind="function", location="Samples/A.h"),
            self.node("AVariable", kind="variable", location="Samples/A.h"),
            self.node("AnEnum", kind="enum", location="Samples/A.h"),
            self.node("AnAlias", kind="typedef", location="Samples/A.h"),
            self.node("AMacro", kind="define", location="Samples/A.h"),
            self.node("AUnion", kind="union", location="Samples/A.h"),
        ]
        self.generate()
        folder = self.api / "_navigation/symbols/Samples"
        content = (folder / "index.rst").read_text()
        for node in examples:
            title = ENTITY_TITLES[node.kind]
            self.assertIn(f"{title}\n{'-' * len(title)}", content)
            self.assertIn(node.file_name, content)
        self.assertEqual(list(folder.glob("*.rst")), [folder / "index.rst"])
        self.nodes.clear()
        self.node("OnlyClass", location="Samples/A.h")
        self.generate()
        content = (folder / "index.rst").read_text()
        self.assertIn("Classes\n-------", content)
        self.assertNotIn("Functions\n---------", content)

    def test_all_pages_have_exactly_one_navigation_parent(self):
        self.node("Handler", location="Samples/Handler.h")
        self.node("Sample", kind="file", location="Samples/Handler.h")
        self.node("Samples", kind="dir")
        self.node("M3", kind="namespace")
        self.node("Definitions", kind="page")
        self.generate()
        links = []
        for path in [self.listing, *self.api.glob("_navigation/**/*.rst")]:
            links.extend((path.parent / entry).resolve() for entry in re.findall(
                r"^   (\S+\.rst)$", path.read_text(), re.MULTILINE,
            ))
        for node in self.nodes:
            self.assertEqual(links.count((self.api / node.file_name).resolve()), 1, node.name)
        self.assertNotIn("toctree", self.orphan.read_text())

    def test_root_level_header_and_unlocated_entity_are_reachable(self):
        top = self.node("Top", location="Top.h")
        unknown = self.node("Unknown")
        self.generate()
        self.assertIn(top.file_name, self.listing.read_text())
        fallback = self.api / "_navigation/symbols/Other API entities/index.rst"
        self.assertIn(unknown.file_name, fallback.read_text())

    def test_old_generated_indexes_are_removed(self):
        self.node("Old", location="Old/Old.h")
        self.generate()
        self.nodes.clear()
        self.node("New", location="New/New.h")
        self.generate()
        self.assertFalse((self.api / "_navigation/symbols/Old/index.rst").exists())
        self.assertTrue((self.api / "_navigation/symbols/New/index.rst").exists())

    def test_missing_exhale_mapping_fails_explicitly(self):
        self.listing.write_text(".. toctree::\n\n   unknown.rst\n")
        self.orphan.write_text(":orphan:\n")
        with self.assertRaisesRegex(ExtensionError, "cannot identify"):
            generate_navigation(self.app)

    def test_missing_page_fails_explicitly(self):
        node = self.node("Missing", location="Samples/Missing.h")
        (self.api / node.file_name).unlink()
        with self.assertRaisesRegex(ExtensionError, "does not exist"):
            self.generate()

    def test_absolute_or_parent_source_paths_fail_explicitly(self):
        for location in ("/outside/Header.h", "../outside/Header.h"):
            with self.subTest(location=location):
                self.nodes.clear()
                self.node("Outside", location=location)
                with self.assertRaisesRegex(ExtensionError, "repository-relative"):
                    self.generate()


if __name__ == "__main__":
    unittest.main()
