import ast
import runpy
import unittest
from pathlib import Path


class SearchConfigurationTests(unittest.TestCase):
    def test_scorer_path_resolves_from_the_configuration_file(self):
        config_path = Path(__file__).resolve().parents[1] / "conf.py"
        config_tree = ast.parse(config_path.read_text(encoding="utf-8"))
        assignment = next(
            node for node in config_tree.body
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "html_search_scorer"
                for target in node.targets
            )
        )
        scorer = Path(eval(
            compile(ast.Expression(assignment.value), str(config_path), "eval"),
            {"Path": Path, "__file__": str(config_path)},
        ))

        self.assertTrue(scorer.is_absolute())
        self.assertEqual(scorer, config_path.parent / "_static/search-scorer.js")
        self.assertTrue(scorer.is_file())


if __name__ == "__main__":
    unittest.main()
