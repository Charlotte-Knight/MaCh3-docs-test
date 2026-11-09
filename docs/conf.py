project = "MaCh3"
copyright = "MaCh3 Collaboration"
author = "MaCh3 Collaboration"

extensions = [
    "breathe",
    "exhale",
    "myst_parser",
    "sphinx.ext.mathjax",
]

root_doc = "index"
primary_domain = "cpp"
nitpicky = True

breathe_projects = {"MaCh3": "./xml"}
breathe_default_project = "MaCh3"

exhale_args = {
    "containmentFolder": "./api",
    "rootFileName": "library_root.rst",
    "rootFileTitle": "C++ API",
    "doxygenStripFromPath": "..",
    "createTreeView": True,
    "exhaleExecutesDoxygen": True,
    "exhaleDoxygenStdin": """
        PROJECT_NAME = MaCh3
        GENERATE_HTML = NO
        GENERATE_XML = YES
        GENERATE_TODOLIST = NO
        XML_OUTPUT = xml
        INPUT = ../CLI ../Doc/MaCh3Web/Definitions.dox ../Fitters ../Manager ../NuDock ../Parameters ../Samples ../Splines ../Utils/Plotting
        FILE_PATTERNS = *.h *.hh *.hpp *.hxx *.dox
        RECURSIVE = YES
        EXCLUDE_PATTERNS = */third_party/* */third-party/* */external/* */_deps/* */build/* */test/* */tests/* */detail/* */details/*
        EXCLUDE_SYMBOLS = std::* M3::detail::* *IsSubEventSelected* create_plugin_t destroy_plugin_t MakeVector MaCh3FitterFactory M3::MatrixVectorMulti M3::MatrixVectorMultiSingle
        EXTRACT_ALL = YES
        EXTRACT_PRIVATE = NO
        EXTRACT_STATIC = NO
        FULL_PATH_NAMES = YES
        HIDE_UNDOC_NAMESPACES = NO
        ENABLE_PREPROCESSING = YES
        MACRO_EXPANSION = YES
        PREDEFINED = _noexcept_:=noexcept _restrict_:= _MaCh3_Safe_Include_Start_:= _MaCh3_Safe_Include_End_:= ClassDef(name,version)= MULTITHREAD
        EXPAND_AS_DEFINED = _noexcept_ _restrict_ _MaCh3_Safe_Include_Start_ _MaCh3_Safe_Include_End_ ClassDef
        QUIET = YES
        HAVE_DOT = YES
    """,
}

myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    "colon_fence",
]

nitpick_ignore = [
    ("cpp:class", "std::string"),
    ("cpp:class", "std::vector"),
    ("cpp:class", "TObject"),
    ("cpp:identifier", "M3"),
    ("cpp:identifier", "M3::Utils"),
    ("cpp:identifier", "M3::Plotting"),
    ("cpp:identifier", "M3::rand"),
    ("std:ref", "_event_info_8h"),
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
html_static_path = ["_static"]
html_theme_options = {
    "logo": {
        "image_light": "_static/mach3logo.png",
        "image_dark": "_static/mach3logo.png",
    },
}
