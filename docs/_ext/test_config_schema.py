import copy
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft7Validator


DOCS = Path(__file__).resolve().parents[1]


class ConfigurationSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = yaml.safe_load((DOCS / "schemas/fitter-config.schema.yaml").read_text())
        cls.example = yaml.safe_load((DOCS / "examples/FitterConfig.yaml").read_text())
        cls.validator = Draft7Validator(cls.schema)

    def test_schema_is_valid_and_example_passes(self):
        Draft7Validator.check_schema(self.schema)
        self.validator.validate(self.example)

    def test_every_example_setting_has_an_explicit_schema(self):
        def visit(value, schema, path):
            if isinstance(value, dict):
                for key, child in value.items():
                    child_schema = schema.get("properties", {}).get(key)
                    if child_schema is None:
                        child_schema = schema.get("additionalProperties")
                    self.assertIsInstance(child_schema, dict, ".".join([*path, key]))
                    visit(child, child_schema, [*path, key])
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    items = schema["items"]
                    visit(child, items[index] if isinstance(items, list) else items, path)
        visit(self.example, self.schema, [])

    def test_types_and_selected_constraints_reject_invalid_settings(self):
        for path, invalid in (
            (["General", "Debug"], "false"),
            (["General", "MCMC", "NSteps"], -1),
            (["General", "MCMC", "DelayProbability"], 1.1),
            (["Predictive", "ParameterBounds"], [["delta_cp", [1]]]),
            (["LLHScan", "ScanRanges"], {"delta_cp": [1]}),
            (["SigmaVar", "SigmaArray"], [-3, -1, 1, 3]),
            (["AdaptionOptions", "Settings", "TargetAcceptance"], 1),
            (["KinematicDistributionPlots"], [{"KinematicCuts": [{"Range": [1]}]}]),
        ):
            with self.subTest(path=path):
                config = copy.deepcopy(self.example)
                target = config
                for key in path[:-1]:
                    target = target[key]
                target[path[-1]] = invalid
                self.assertFalse(self.validator.is_valid(config))

    def test_predictive_selection_lists_are_mutually_exclusive(self):
        config = copy.deepcopy(self.example)
        config["Predictive"]["ThrowParamGroupOnly"] = ["Xsec"]
        self.validator.validate(config)
        config["Predictive"]["ThrowSingleParams"] = ["delta_cp"]
        self.assertFalse(self.validator.is_valid(config))

    def test_dynamic_maps_and_bounds_examples_are_supported(self):
        config = copy.deepcopy(self.example)
        config["Predictive"]["ParameterBounds"] = [["delta_cp", [-3.14, 3.14]]]
        config["AdaptionOptions"]["Covariance"]["another_cov"] = {
            "DoAdaption": True, "ParametersToSkip": ["delta_cp"],
        }
        self.validator.validate(config)

    def test_partial_and_experiment_specific_configs_are_allowed(self):
        self.validator.validate({})
        self.validator.validate({"Experiment": {"custom": 1}, "General": {"Custom": True}})


if __name__ == "__main__":
    unittest.main()
