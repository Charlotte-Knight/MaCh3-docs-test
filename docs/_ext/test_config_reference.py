import unittest

import yaml
from docutils import nodes

from config_reference import constraints, example_yaml, setting_section, type_label


class ConfigurationReferenceTests(unittest.TestCase):
    def test_entries_have_full_paths_descriptions_and_yaml_examples(self):
        section = setting_section(["General", "MCMC", "NSteps"], {
            "type": "integer", "minimum": 1,
            "description": "Number of steps.", "examples": [10000],
        })
        self.assertEqual(section["ids"], ["config-general-mcmc-nsteps"])
        self.assertIn("General.MCMC.NSteps", section.astext())
        self.assertIn("Minimum: 1", section.astext())
        self.assertIn("Number of steps.", section.astext())
        example = next(section.findall(nodes.literal_block))
        self.assertEqual(yaml.safe_load(example.astext()), {
            "General": {"MCMC": {"NSteps": 10000}},
        })
        self.assertIn("not a default", section.astext())

    def test_nested_maps_and_array_objects_are_documented(self):
        section = setting_section(["Plots"], {
            "type": "array", "items": {
                "type": "object", "properties": {
                    "Range": {"type": "array", "items": {"type": "number"}},
                },
            },
        })
        self.assertIn("Plots[].Range", section.astext())
        ids = [node["ids"][0] for node in section.findall(nodes.section)]
        self.assertEqual(len(ids), len(set(ids)))
        mapping = setting_section(["Covariance"], {
            "type": "object", "additionalProperties": {
                "type": "object", "properties": {
                    "Enabled": {"type": "boolean", "examples": [False]},
                },
            },
        })
        self.assertIn("Covariance.<name>.Enabled", mapping.astext())
        example = next(mapping.findall(nodes.literal_block))
        self.assertEqual(yaml.safe_load(example.astext()), {
            "Covariance": {"name": {"Enabled": False}},
        })

    def test_example_wrapping_preserves_lists_and_boolean_values(self):
        example = example_yaml(["Plots", "[]", "Enabled"], False)
        self.assertEqual(yaml.safe_load(example), {"Plots": [{"Enabled": False}]})

    def test_constraints_distinguish_defaults_from_examples(self):
        labels = constraints({
            "exclusiveMinimum": 0, "maximum": 1, "examples": [0.5], "default": 0.1,
        })
        self.assertEqual(labels, ["Maximum: 1", "Greater than: 0", "Default: 0.1"])
        self.assertEqual(constraints({"contains": {"const": 0}}), ["Must contain: 0"])
        labels = constraints({"not": {
            "required": ["A", "B"],
            "properties": {"A": {"minItems": 1}, "B": {"minItems": 1}},
        }})
        self.assertEqual(labels, ["Cannot both be nonempty: A, B"])

    def test_nested_types_and_tuples_are_readable(self):
        self.assertEqual(type_label({
            "type": "array", "items": [
                {"type": "string"}, {"type": "array", "items": {"type": "number"}},
            ],
        }), "tuple [string, array of number]")
        self.assertEqual(type_label({
            "type": "object", "additionalProperties": {"type": "boolean"},
        }), "map of boolean")


if __name__ == "__main__":
    unittest.main()
