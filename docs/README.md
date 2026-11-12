# Documentation development

The User Guide's [Docs section](user-guide/docs/index.md) explains how to build
the combined C++/Python site, publish it on GitHub Pages, and link to C++ API
entities from MyST pages. A real, importable pyMaCh3 build is required for the
Python API reference. The site includes a version selector for Sphinx releases
and archived Doxygen documentation; publishing details are in the same guide.
Run the publishing tests with
`python -B -m unittest discover -s .github/CIscripts -p 'test_*.py' -v`
from the repository root.

The bibliography is
shared with Doxygen from `Doc/MaCh3Web/bibliography.bib`; cite its entries in
MyST with `{cite:p}\`luengo2020survey\``. The [Bibliography](bibliography.md)
page lists all entries.
