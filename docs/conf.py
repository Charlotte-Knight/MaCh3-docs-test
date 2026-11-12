project = "MaCh3"
copyright = "MaCh3 Collaboration"
author = "MaCh3 Collaboration"

import os
import re
import sys
from pathlib import Path

from exhale.utils import makeCustomSpecificationsMapping

sys.path.insert(0, str(Path(__file__).parent / "_ext"))

extensions = [
    "breathe",
    "exhale",
    "myst_parser",
    "sphinx.ext.graphviz",
    "sphinx.ext.mathjax",
    "sphinxcontrib.bibtex",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "api_navigation",
]

root_doc = "index"
primary_domain = "cpp"
nitpicky = True

breathe_projects = {"MaCh3": "./xml"}
breathe_default_project = "MaCh3"
bibtex_bibfiles = ["../Doc/MaCh3Web/bibliography.bib"]
autodoc_class_signature = "separated"
napoleon_use_rtype = False
napoleon_preprocess_types = True

# Match PyData's API signatures, resolving fonts in the reader's browser.
graphviz_output_format = "svg"
graphviz_font = (
    "ui-monospace, Cascadia Code, Source Code Pro, Menlo, Consolas, "
    "DejaVu Sans Mono, monospace"
)
graphviz_dot_args = [
    f"-Gfontname={graphviz_font}",
    f"-Nfontname={graphviz_font}",
    f"-Efontname={graphviz_font}",
]


def breathe_specifications(kind):
    if kind in ("class", "struct"):
        return [
            ":members:",
            ":protected-members:",
            ":undoc-members:",
            ":allow-dot-graphs:",
        ]
    return []


exhale_args = {
    "containmentFolder": "./api",
    "rootFileName": "library_root.rst",
    "rootFileTitle": "C++ API",
    "doxygenStripFromPath": "..",
    "createTreeView": True,
    "customSpecificationsMapping": makeCustomSpecificationsMapping(
        breathe_specifications
    ),
    "exhaleExecutesDoxygen": True,
    "exhaleDoxygenStdin": """
        PROJECT_NAME = MaCh3
        GENERATE_HTML = NO
        GENERATE_XML = YES
        GENERATE_TODOLIST = NO
        HAVE_DOT = YES
        CLASS_GRAPH = YES
        COLLABORATION_GRAPH = YES
        XML_OUTPUT = xml
        CITE_BIB_FILES = ../Doc/MaCh3Web/bibliography.bib
        INPUT = ../CLI ../Doc/MaCh3Web/Definitions.dox ../Fitters ../Manager ../NuDock ../Parameters ../Samples ../Splines ../Utils/Plotting
        FILE_PATTERNS = *.h *.hh *.hpp *.hxx *.dox
        RECURSIVE = YES
        EXCLUDE_PATTERNS = */third_party/* */third-party/* */external/* */_deps/* */build/* */test/* */tests/* */detail/* */details/*
        EXCLUDE_SYMBOLS = std::* M3::detail::* *IsSubEventSelected* create_plugin_t destroy_plugin_t MakeVector MaCh3FitterFactory M3::MatrixVectorMulti M3::MatrixVectorMultiSingle
        EXTRACT_ALL = YES
        EXTRACT_PRIVATE = NO
        EXTRACT_STATIC = NO
        FULL_PATH_NAMES = YES
        ENABLE_PREPROCESSING = YES
        MACRO_EXPANSION = YES
        PREDEFINED = _noexcept_:=noexcept _restrict_:= _MaCh3_Safe_Include_Start_:= _MaCh3_Safe_Include_End_:= ClassDef(name,version)= MULTITHREAD
        EXPAND_AS_DEFINED = _noexcept_ _restrict_ _MaCh3_Safe_Include_Start_ _MaCh3_Safe_Include_End_ ClassDef
        QUIET = YES
    """,
}

myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    "colon_fence",
]

nitpick_ignore = [
    ("py:class", "pybind11_builtins.pybind11_object"),
    ("py:class", "pyMaCh3._pyMaCh3.splines._ResponseFunctionBase"),
    ("py:class", "numpy.ndarray"),
    ("py:class", "numpy.float32"),
    ("py:class", "numpy.float64"),
    ("cpp:class", "std::string"),
    ("cpp:class", "std::vector"),
    ("cpp:class", "TObject"),
    ("cpp:identifier", "M3"),
    ("cpp:identifier", "M3::Utils"),
    ("cpp:identifier", "M3::Plotting"),
    ("cpp:identifier", "M3::rand"),
    ("std:ref", "_nu_dock_factory_8h_1a9e5eb57352d19ee0660059fafb4fffd1"),
    ("std:ref", "_get_penalty_term_module_8hpp"),
]
nitpick_ignore_regex = [
    (
        r"cpp:.*",
        r"^(?:std::|ROOT::|T[A-Z0-9][A-Za-z0-9_:]*)",
    ),
    (
        r"cpp:.*",
        r"^(?:YAML(?:::.*)?|nlohmann(?:::.*)?|NuDock|ArgumentParser|FLOAT_T|SplineMonolithGPU|spdlog(?:::.*)?|size_t|Color_t|Long64_t|Style_t|Width_t|ELineStyle|kCyan|kGreen|kDashed|kSolid|kDotted|kTSpline3)$",
    ),
]

exclude_patterns = ["_build", "README.md"]
html_theme = "pydata_sphinx_theme"
html_title = "MaCh3 documentation"
html_logo = "_static/mach3logo.png"
html_favicon = "_static/mach3logo.png"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
templates_path = ["_templates"]
html_js_files = ["version-switcher.js"]
html_context = {
    "docs_version": os.environ.get("DOCS_VERSION", "develop"),
    "docs_versions_url": os.environ.get("DOCS_VERSIONS_URL", ""),
}
html_theme_options = {
    "logo": {
        "image_light": "_static/mach3logo.png",
        "image_dark": "_static/mach3logo.png",
    },
    "github_url": "https://github.com/mach3-software/MaCh3",
    "navbar_start": ["navbar-logo"],
    "navbar_end": ["docs-version-switcher", "theme-switcher", "navbar-icon-links"],
    "show_nav_level": 1,
}


# Some pybind11 signatures retain C++ names for types registered later.
binding_type_aliases = {
    "pyMaCh3.m_parameters.SystematicType": "pyMaCh3._pyMaCh3.parameters.SystematicType",
    "pyMaCh3.samples.SampleHandlerInterface": "pyMaCh3._pyMaCh3.samples.SampleHandlerInterface",
    "M3::Plotting::InputManager": "pyMaCh3._pyMaCh3.plotting.InputManager",
    "M3::Plotting::StyleManager": "pyMaCh3._pyMaCh3.plotting.StyleManager",
    "SplineInterpolation": "pyMaCh3._pyMaCh3.splines.InterpolationType",
}


def normalize_binding_names(text):
    if text is not None:
        for original, target in binding_type_aliases.items():
            text = re.sub(r"(?<![\w.])" + re.escape(original) + r"(?!\w)", target, text)
    return text


def normalize_binding_docstrings(app, what, name, obj, options, lines):
    for index, line in enumerate(lines):
        lines[index] = normalize_binding_names(line)


def normalize_binding_signature(app, what, name, obj, options, signature, return_annotation):
    return normalize_binding_names(signature), normalize_binding_names(return_annotation)


def setup(app):
    app.connect("autodoc-process-docstring", normalize_binding_docstrings)
    app.connect("autodoc-process-signature", normalize_binding_signature)
