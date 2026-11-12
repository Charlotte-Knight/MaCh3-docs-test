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
python -c "from pyMaCh3 import manager, samples, splines, fitters, parameters, plotting"
sphinx-build -W --keep-going -b html docs docs/_build/html
```

ROOT and the normal MaCh3 build prerequisites must already be installed.
Do not use a different Python version for the bindings and Sphinx.
The build deliberately fails if pyMaCh3 cannot be imported; the Python API
reference is generated from real bindings, not mocks.

Exhale runs Doxygen during the Sphinx build and writes XML for Breathe to
consume. The generated API pages are written to `docs/api/` and are not
committed.

Doxygen records class inheritance and collaboration relationships in the XML.
Exhale adds Breathe's graph option to every generated class and struct page,
and Sphinx renders available diagrams with Graphviz. These diagrams are
regenerated automatically on every documentation build; no per-class pages
or diagram files need to be maintained by hand.

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

Only successful non-PR builds of `develop` deploy, using the `github-pages`
environment. No personal access token is required. The deployment job reports
the published URL. For a project repository, the site is normally hosted at
`https://<owner>.github.io/<repository>/`.

Deployment is opt-in so forks can review the new site without replacing the
upstream Doxygen site. The original Doxygen build remains available. When
`DOCS_PAGES_ENABLED=true`, its old publishing job is skipped to avoid competing
deployments; its documentation artifacts are still built. The existing
upstream Doxygen site is also linked from the Sphinx sidebar.

GitHub Pages serves the static site, including Sphinx's browser-side search.
Read the Docs' server-side search and page-ranking configuration are not used.
