# Fitter configuration

MaCh3 uses YAML configuration files to select fitters, load sample and
systematic models, and configure analysis tools. This page demonstrates
**schema-driven documentation**: the setting entries below are rendered
automatically from a JSON Schema written in YAML. Each entry has a linkable
full key path, type, constraints, description, and example where available.
`<name>` represents a user-chosen map key and `[]` represents an array item.

```{warning}
This is a proof of concept, not a complete MaCh3 configuration specification.
It is based on a supplied example from
[MaCh3Tutorial](https://github.com/mach3-software/MaCh3Tutorial), its comments,
and selected checks against MaCh3 source. Some descriptions and numeric bounds
are inferred. `TutorialSamples` is tutorial-specific, not a universal setting.

All properties are optional in this demonstration and unknown keys are allowed.
A successful validation does **not** mean a configuration will run: requirements
depend on the executable, algorithm, plugins, and experiment. File existence,
ROOT objects, parameter names, and ordering of numeric bounds are not checked.
Example values are **not runtime defaults**.
```

## Files and validation

Download the {download}`schema <../schemas/fitter-config.schema.yaml>` or
the {download}`sanitized example <../examples/FitterConfig.yaml>`.
The example preserves the supplied settings, replaces the machine-specific
spline path, and uses explicit `true`/`false` booleans. Input paths refer to
tutorial assets; this repository does not supply those assets.

The schema uses JSON Schema Draft 7. YAML is parsed into ordinary objects before
validation. From the repository root, with the documentation dependencies
installed:

```sh
python - <<'PY'
from pathlib import Path
import yaml
from jsonschema import Draft7Validator

schema = yaml.safe_load(Path("docs/schemas/fitter-config.schema.yaml").read_text())
config = yaml.safe_load(Path("docs/examples/FitterConfig.yaml").read_text())
Draft7Validator.check_schema(schema)
Draft7Validator(schema).validate(config)
print("Configuration matches the demonstration schema")
PY
```

Prefer `true` and `false` over YAML's legacy `Yes`/`No` spellings, whose
interpretation varies between YAML implementations. Keys are case-sensitive:
in particular, retain `AdaptionOptions`, `DoAdaption`, and `initial_scale`.

The schema captures types, descriptions, example values, selected numeric
bounds, and a few structural constraints. For example, `SigmaArray` must include
zero, range arrays contain two values, and the two predictive parameter
selection lists cannot both be nonempty.

## General

```{config-reference} ../schemas/fitter-config.schema.yaml General
```

## Predictive

```{config-reference} ../schemas/fitter-config.schema.yaml Predictive
```

## Likelihood scans

```{config-reference} ../schemas/fitter-config.schema.yaml LLHScan
```

## Sigma variations

```{config-reference} ../schemas/fitter-config.schema.yaml SigmaVar
```

## Adaptation

```{config-reference} ../schemas/fitter-config.schema.yaml AdaptionOptions
```

## Kinematic distribution plots

```{config-reference} ../schemas/fitter-config.schema.yaml KinematicDistributionPlots
```

## Example configuration

```{literalinclude} ../examples/FitterConfig.yaml
:language: yaml
```
