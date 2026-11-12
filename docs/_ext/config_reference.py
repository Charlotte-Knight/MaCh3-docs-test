"""Render configuration schemas as readable, linked setting entries."""

import json
from pathlib import Path

import yaml
from docutils import nodes
from jsonschema import Draft7Validator
from sphinx.util.docutils import SphinxDirective


def type_label(schema):
    kind = schema.get("type", "any")
    if kind == "array":
        items = schema.get("items", {})
        if isinstance(items, list):
            return "tuple [" + ", ".join(type_label(item) for item in items) + "]"
        return "array of " + type_label(items)
    if kind == "object" and isinstance(schema.get("additionalProperties"), dict):
        return "map of " + type_label(schema["additionalProperties"])
    return kind


def constraints(schema):
    labels = []
    for key, label in (
        ("minimum", "Minimum"), ("maximum", "Maximum"),
        ("exclusiveMinimum", "Greater than"), ("exclusiveMaximum", "Less than"),
        ("minItems", "Minimum items"), ("maxItems", "Maximum items"),
        ("pattern", "Pattern"), ("default", "Default"),
    ):
        if key in schema:
            labels.append(f"{label}: {json.dumps(schema[key])}")
    if "enum" in schema:
        labels.append("Choices: " + ", ".join(json.dumps(value) for value in schema["enum"]))
    if "contains" in schema:
        contains = schema["contains"]
        labels.append("Must contain: " + json.dumps(contains.get("const", contains)))
    if "not" in schema:
        excluded = schema["not"]
        properties = excluded.get("properties", {})
        if properties and set(excluded.get("required", [])) == set(properties) and all(
            rule == {"minItems": 1} for rule in properties.values()
        ):
            labels.append("Cannot both be nonempty: " + ", ".join(properties))
        else:
            labels.append("Disallowed combination: " + json.dumps(excluded))
    if "required" in schema:
        labels.append("Required keys: " + ", ".join(schema["required"]))
    return labels


def example_yaml(path, value):
    for part in reversed(path):
        if part == "[]":
            value = [value]
        else:
            value = {"name" if part == "<name>" else part: value}
    return yaml.safe_dump(value, sort_keys=False, allow_unicode=False).rstrip()


def setting_section(path, schema):
    label = ".".join(path).replace(".[]", "[]")
    section = nodes.section(
        ids=["config-" + nodes.make_id(label.replace("[]", "-item"))],
        classes=["config-setting"],
    )
    title = nodes.title()
    title += nodes.literal(text=label)
    section += title
    metadata = nodes.paragraph(classes=["config-setting-metadata"])
    metadata += nodes.strong(text="Type: ")
    metadata += nodes.Text(type_label(schema))
    for constraint in constraints(schema):
        metadata += nodes.Text(" · " + constraint)
    section += metadata
    if schema.get("description"):
        section += nodes.paragraph(text=schema["description"])
    for value in schema.get("examples", []):
        section += nodes.paragraph("", "", nodes.emphasis(text="Example (not a default):"))
        output = example_yaml(path, value)
        section += nodes.literal_block(output, output, language="yaml")
    for name, child in schema.get("properties", {}).items():
        section += setting_section([*path, name], child)
    additional = schema.get("additionalProperties")
    if isinstance(additional, dict):
        section += setting_section([*path, "<name>"], additional)
    items = schema.get("items")
    if isinstance(items, dict) and (
        "properties" in items or isinstance(items.get("additionalProperties"), dict)
    ):
        section += setting_section([*path, "[]"], items)
    return section


class ConfigurationReference(SphinxDirective):
    required_arguments = 2

    def run(self):
        relative, filename = self.env.relfn2path(self.arguments[0])
        self.env.note_dependency(relative)
        schema = yaml.safe_load(Path(filename).read_text(encoding="utf-8"))
        Draft7Validator.check_schema(schema)
        key = self.arguments[1]
        if key not in schema.get("properties", {}):
            raise self.error(f"No configuration section {key!r} in {filename}")
        return [setting_section([key], schema["properties"][key])]


def setup(app):
    app.add_directive("config-reference", ConfigurationReference)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
