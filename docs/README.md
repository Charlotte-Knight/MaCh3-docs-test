# Building the documentation

The documentation build needs Python 3.12 or newer, Doxygen, and Graphviz
(`dot`). For example, on macOS install Doxygen and Graphviz with Homebrew:

```sh
brew install doxygen graphviz
```

From the repository root, create a Python environment, install the Sphinx
extensions, and build the HTML site:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r docs/requirements.txt
sphinx-build -W --keep-going -b html docs docs/_build/html
```

Exhale runs Doxygen during the Sphinx build and writes XML for Breathe to
consume. The generated API pages are written to `docs/api/` and are not
committed.

## Publishing with Read the Docs

The repository includes a Read the Docs configuration in `.readthedocs.yaml`.
To publish the site, sign in to [Read the Docs](https://readthedocs.org/), add
the MaCh3 repository from GitHub, and select the branch that should publish the
documentation. The GitHub integration installs the webhook and builds that
branch on pushes. Enable pull-request builds in the project's Admin settings
if you also want documentation previews and status checks on pull requests.

The project configuration installs `docs/requirements.txt`, installs Doxygen
and Graphviz, and points Sphinx at `docs/conf.py`. No GitHub Actions secret or
separate deployment workflow is required for Read the Docs to build and host
the site.

## Linking to C++ API entities

Use Sphinx's C++ domain roles in MyST Markdown:

```md
{cpp:class}`ParameterHandlerGeneric`
{cpp:func}`ParameterHandlerBase::GetNumParams`
```

For overloaded functions, include the full parameter types (and qualifiers) in
the role target so Sphinx can select the intended overload. Cross-reference
targets use the C++ name, not the header filename.

For example, the overload taking a group name and values is
{cpp:func}`void ParameterHandlerGeneric::SetGroupOnlyParameters(const std::string&, const std::vector<double>&)`.
