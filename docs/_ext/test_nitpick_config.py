import re
import runpy
import unittest
from pathlib import Path


class NitpickConfigurationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = runpy.run_path(str(Path(__file__).resolve().parents[1] / "conf.py"))
        cls.ignores = config["nitpick_ignore_regex"]

    def ignored(self, role, target):
        return any(
            re.fullmatch(role_pattern, role) and re.fullmatch(target_pattern, target)
            for role_pattern, target_pattern in self.ignores
        )

    def test_external_cpp_names_match_sphinx_fullmatch_semantics(self):
        for role in ("cpp:identifier", "cpp:class"):
            for target in (
                "ROOT", "ROOT::RDataFrame", "ROOT::RDF::RNode",
                "std", "std::string", "std::vector<double>", "TObject", "TH1D",
            ):
                with self.subTest(role=role, target=target):
                    self.assertTrue(self.ignored(role, target))

    def test_project_and_python_references_are_not_hidden(self):
        for role, target in (
            ("cpp:identifier", "M3::MissingType"),
            ("cpp:class", "ParameterHandlerGeneric"),
            ("cpp:identifier", "ROOTTypo"),
            ("cpp:identifier", "stdTypo"),
            ("py:class", "ROOT::RDataFrame"),
        ):
            with self.subTest(role=role, target=target):
                self.assertFalse(self.ignored(role, target))


if __name__ == "__main__":
    unittest.main()
