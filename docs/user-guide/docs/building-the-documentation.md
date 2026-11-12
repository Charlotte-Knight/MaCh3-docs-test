# Building the documentation

The documentation build needs Python 3.12 or newer, compiled pyMaCh3 bindings
and their ROOT/MaCh3 runtime libraries, Doxygen 1.9.8 or newer, Graphviz
(`dot`), BibTeX, and Perl. Doxygen 1.9.8 (Ubuntu 24.04) requires the
`bibtex` and `perl` executables to generate the API bibliography.
On Ubuntu, install the system dependencies with:

```sh
sudo apt-get install doxygen graphviz texlive-binaries perl
```

On macOS, install Doxygen, Graphviz, and a TeX distribution providing
BibTeX (Perl is supplied by macOS):

```sh
brew install doxygen graphviz
brew install --cask basictex
```

After installing BasicTeX, ensure `/Library/TeX/texbin` is on your `PATH`.

From the repository root, create a Python environment and install the Sphinx
extensions. Use the same Python interpreter to build the bindings and the
documentation:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install "cmake>=3.24,<4" numpy -r docs/requirements.txt
cmake -S . -B build-docs \
  -DMaCh3_PYTHON_ENABLED=ON \
  -DPython_EXECUTABLE="$VIRTUAL_ENV/bin/python" \
  -DMaCh3_GPU_ENABLED=OFF \
  -DNuFastLinear_ENABLED=ON
cmake --build build-docs --parallel 4
cmake --install build-docs
export PYTHONPATH="$PWD/build-docs${PYTHONPATH:+:$PYTHONPATH}"
export LD_LIBRARY_PATH="$PWD/build-docs/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export MACH3_EXECUTABLE="$PWD/build-docs/bin/mach3"
python -c "from pyMaCh3 import manager, samples, splines, fitters, parameters, plotting"
sphinx-build -W --keep-going -b html docs docs/_build/html
```

ROOT and the normal MaCh3 build prerequisites must already be installed.
Do not use a different Python version for the bindings and Sphinx.
The build deliberately fails if pyMaCh3 cannot be imported; the Python API
reference is generated from real bindings, not mocks.
The [CLI guide](../cli.md) also executes this build's `mach3 --help` and each
discovered subcommand's help. `MACH3_EXECUTABLE` selects the executable; otherwise
it must be available as `mach3` on `PATH`. `MACH3_PLUGINS` is removed from these
help subprocesses so the reference consistently documents built-in commands.
Missing executables, unsuccessful help commands, and runtime errors fail the
documentation build. On macOS, if the executable cannot locate its libraries,
also set `DYLD_LIBRARY_PATH` to the build's `lib` directory.

Exhale runs Doxygen during the Sphinx build and writes XML for Breathe to
consume. The generated API pages are written to `docs/api/` and are not
committed.

Doxygen records class inheritance and collaboration relationships in the XML.
Exhale adds Breathe's graph option to every generated class and struct page,
and Sphinx renders available diagrams with Graphviz. These diagrams are
regenerated automatically on every documentation build; no per-class pages
or diagram files need to be maintained by hand.
Diagrams use SVG with the same monospace font stack as PyData's API signatures,
so labels use the reader's available fonts rather than a font baked into a PNG.
The matching Graphviz font stack is configured in `docs/conf.py`.

## Automatic C++ API navigation

The left sidebar groups API entities by the directory containing their declaring
header, including nested source directories. For example, classes declared in
`Fitters/Algorithms/` appear beneath **C++ API > Fitters > Algorithms**.
Each directory has one overview page with section headings for classes, structs,
unions, enums, functions, variables, type aliases, and macros, rather than
separate category pages. Individual entries retain their own API pages.
Only nonempty sections appear,
and entries are sorted alphabetically within each category. Namespaces, Doxygen
pages, and the directory-grouped source-file index have separate sections.
Entities without a known declaring file appear under **Other API entities**.

The local `api_navigation` Sphinx extension runs after Exhale, using its parsed
Doxygen file locations and generated page names to create nested toctrees.
New entities and source directories appear automatically; no class lists need
maintenance. Existing API pages, cross-reference targets, diagrams, and the
landing page's hierarchy views are preserved. Generated navigation lives under
`docs/api/_navigation/` and is ignored along with the rest of `docs/api/`.

The normal `sphinx-build` command runs this step both locally and in CI.
To run its tests separately:

```sh
python -B -m unittest discover -s docs/_ext -p 'test_*.py' -v
```

## Schema-driven configuration reference

The [configuration reference](../configuration.md) is a proof of concept built
with the local `config_reference` extension. Its JSON Schema is written in
YAML at `docs/schemas/fitter-config.schema.yaml`; MyST `config-reference`
directives take a schema filename and a top-level property name. They render
linked setting entries with types, constraints, descriptions, and YAML examples,
including nested properties, dynamic map keys, and arrays of objects. Edit property
descriptions, types, and examples in the schema rather than maintaining
duplicate reference entries. Sphinx rebuilds the reference from that file.

The sanitized example at `docs/examples/FitterConfig.yaml` is validated with
`jsonschema` in the documentation extension tests, including CI. The tests also
check coverage of example fields and selected invalid configurations. This
does not add validation to MaCh3 itself or make the provisional schema an
authoritative specification. Review inferred constraints before production use.

## Automatic Python API reference

The [pyMaCh3 guides](../../pymach3/index.md) use Sphinx autodoc to import each
compiled module and document its classes, functions, and members. New public
members of the existing modules appear automatically when the bindings are
rebuilt. Add a guide and toctree entry when introducing an entirely new module.
Keep binding docstrings in `python/*.h` up to date; autodoc does not automatically
copy the underlying C++ Doxygen comments.

Use an `eval-rst` block when embedding autodoc in Markdown so its generated
reStructuredText is parsed correctly:

````markdown
```{eval-rst}
.. automodule:: pyMaCh3._pyMaCh3.manager
   :members:
   :undoc-members:
   :show-inheritance:
```
````

Reference Python entries using fully qualified roles, for example
`` {py:class}`pyMaCh3._pyMaCh3.manager.Manager` `` or
`` {py:meth}`pyMaCh3._pyMaCh3.manager.YamlNode.data` ``.

## Publishing with GitHub Pages

The Documentation workflow builds the checked-out MaCh3 revision and its Python
bindings in the MaCh3 container, then builds Sphinx using the same interpreter.
It builds Doxygen 1.9.8 because AlmaLinux's older Doxygen misparses C++17
attributes in some public headers.
The container supplies the build environment, not the version of pyMaCh3 to
document. Every successful build uploads a `SphinxHTML` artifact for review,
including on pull requests.

To enable deployment for a repository:

1. In **Settings > Pages**, choose **GitHub Actions** as the build source.
2. In **Settings > Secrets and variables > Actions > Variables**, create the
   repository variable `DOCS_PAGES_ENABLED` with the value `true`.
3. Push to `develop` or run the Documentation workflow manually on `develop`.

Successful non-PR builds of `develop` and release tags matching `v*` deploy,
using the `github-pages` environment. Tags must have the form `vMAJOR.MINOR.PATCH`
or `vMAJOR.MINOR.PATCH-PRERELEASE`, following the existing release convention.
Each tag builds its own C++ source and Python bindings; tags predating the Sphinx
migration are not rebuilt with today's guides. To retry a release that includes
this versioned workflow, run the Documentation workflow manually with that tag
selected. If the `github-pages`
environment restricts deployment branches, allow `develop` and release tags.
No personal access token is required. The deployment job reports the published
URL. For a project repository, the site is normally hosted at
`https://<owner>.github.io/<repository>/`.

### Versions and legacy documentation

Each Sphinx build is published under `develop/` or its release tag, for example
`v2.8.0/`. The site root redirects to the highest published stable Sphinx release,
or to development documentation until a stable release is available. Prereleases
appear in the selector but do not replace a stable release as the default.

The version selector combines Sphinx releases with all entries from the legacy
Doxygen site's selector. Legacy entries always open the Doxygen homepage for
that version; their URLs do not match Sphinx page paths. Switching between
Sphinx versions preserves the page and fragment when the page exists, otherwise
opens the selected version's homepage. Search is scoped to the selected version.

The manifest at the site root, `versions.json`, is shared by all Sphinx versions.
New releases appear in older Sphinx selectors without rebuilding those releases.
The legacy entries are maintained in `docs/_static/legacy-versions.json`; update
this list if additional historical Doxygen archives become available.

Published HTML and the manifest are persisted in the `docs-site` branch.
Deployments restore that branch, replace only the version being built, update
the manifest and root redirect, and deploy the complete tree. Do not delete this
branch: it stores the release snapshots, not the seven-day review artifacts.
The deployment job needs `contents: write` for this branch as well as Pages
permissions; repository rules must permit the Actions bot to update `docs-site`.
Deployments are serialized to prevent concurrent updates from losing versions.
The deployment queue retains pending releases rather than replacing them with
newer runs.

For the first deployment in the upstream `mach3-software/MaCh3` repository, CI
also preserves the existing Doxygen root under `legacy/develop/` and its
`.Archive/` directories at their original paths. This keeps historical URLs
working when Sphinx replaces the upstream homepage. Forks link directly to the
upstream legacy site instead of duplicating its archives.
The separate Doxygen navigation link and plotting-guide link use the existing
v2.7.0 archive so they also survive replacement of the upstream homepage.

For local builds, the selector shows the current development build and legacy
versions. Set `DOCS_VERSION` and `DOCS_VERSIONS_URL` when building to select a
different label and a shared manifest URL. Serve HTML over HTTP rather than
opening `file://` URLs so the browser can fetch the JSON manifest:

```sh
python -m http.server --directory docs/_build/html 8000
```

Deployment is opt-in so forks can review the new site without replacing the
upstream Doxygen site. The original Doxygen build remains available. When
`DOCS_PAGES_ENABLED=true`, its old publishing job is skipped to avoid competing
deployments, and TagDoxygen no longer archives stale `gh-pages` content for new
tags; the original documentation build jobs remain available. The existing
upstream Doxygen site is also linked from the Sphinx sidebar.

GitHub Pages serves the static site, including Sphinx's browser-side search.
Read the Docs' server-side search and page-ranking configuration are not used.
