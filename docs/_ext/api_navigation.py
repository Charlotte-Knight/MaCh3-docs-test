"""Group Exhale's generated API pages by their source directories."""

import os
import re
import shutil
from pathlib import Path

from sphinx.errors import ExtensionError
from sphinx.util import logging


logger = logging.getLogger(__name__)

ENTITY_TITLES = {
    "class": "Classes",
    "struct": "Structs",
    "union": "Unions",
    "enum": "Enums",
    "function": "Functions",
    "variable": "Variables",
    "typedef": "Type aliases",
    "define": "Macros",
}


def toctree(path, pages):
    entries = [
        "   " + Path(os.path.relpath(page, path.parent)).as_posix()
        for page in pages
    ]
    return ".. toctree::\n   :maxdepth: 1\n\n" + "\n".join(entries) + "\n"


def write_index(path, title, pages, heading="=", sections=()):
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"{title}\n{heading * len(title)}\n\n"
    if pages:
        content += toctree(path, pages)
    for section, entries in sections:
        content += f"\n{section}\n{'-' * len(section)}\n\n"
        content += toctree(path, entries)
    path.write_text(
        content,
        encoding="utf-8",
    )


def directory_tree(folder, title, groups, group_entities=False):
    directories = {()}
    for parts in groups:
        directories.update(parts[:depth] for depth in range(1, len(parts) + 1))
    for parts in sorted(directories, key=lambda parts: (-len(parts), parts)):
        children = sorted(
            (child for child in directories if len(child) == len(parts) + 1 and child[:-1] == parts),
            key=lambda child: child[-1].casefold(),
        )
        pages = [folder.joinpath(*child, "index.rst") for child in children]
        entities = sorted(
            groups.get(parts, []), key=lambda entry: (entry[0].casefold(), str(entry[1])),
        )
        sections = []
        if group_entities:
            kinds = {}
            for name, page, kind in entities:
                if kind not in ENTITY_TITLES:
                    raise ExtensionError(f"Unsupported API entity kind: {kind}")
                kinds.setdefault(kind, []).append(page)
            sections = [
                (label, kinds[kind]) for kind, label in ENTITY_TITLES.items() if kind in kinds
            ]
        else:
            pages.extend(page for name, page in entities)
        write_index(
            folder.joinpath(*parts, "index.rst"),
            parts[-1] if parts else title,
            pages,
            sections=sections,
        )
    return [folder / child[0] / "index.rst" for child in sorted(
        (parts for parts in directories if len(parts) == 1),
        key=lambda parts: parts[0].casefold(),
    )] + [entry[1] for entry in sorted(groups.get((), []))]


def generate_navigation(app):
    root = app.exhale_root
    api = Path(root.root_directory)
    listing = Path(root.unabridged_api_file)
    orphan = Path(root.unabridged_orphan_file)
    filenames = set(re.findall(
        r"^   (\S+\.rst)\s*$",
        listing.read_text(encoding="utf-8") + "\n" + orphan.read_text(encoding="utf-8"),
        flags=re.MULTILINE,
    ))
    nodes = {
        Path(node.file_name).name: node
        for node in root.all_nodes if node.file_name
    }
    missing = filenames - nodes.keys()
    if missing:
        raise ExtensionError(f"API navigation cannot identify Exhale pages: {sorted(missing)}")
    navigation = api / "_navigation"
    if navigation.exists():
        shutil.rmtree(navigation)
    symbols = {}
    files = {}
    indexes = {"namespace": [], "page": []}
    for filename in sorted(filenames):
        node = nodes[filename]
        page = api / filename
        if not page.is_file():
            raise ExtensionError(f"API navigation page does not exist: {page}")
        if node.kind in indexes:
            indexes[node.kind].append((node.name, page))
            continue
        if node.kind == "dir":
            parts = Path(node.name).parts
            files.setdefault(parts, []).append((node.name, page))
            continue
        source = node if node.kind == "file" else node.def_in_file
        if source is None:
            parts = ("Other API entities",)
        else:
            location = Path(source.location)
            if location.is_absolute() or ".." in location.parts:
                raise ExtensionError(f"Expected repository-relative API source path: {location}")
            parts = location.parent.parts
        if node.kind == "file":
            files.setdefault(parts, []).append((node.name, page))
        else:
            symbols.setdefault(parts, []).append((node.name, page, node.kind))

    symbol_folder = navigation / "symbols"
    top_level = directory_tree(
        symbol_folder, "By source directory", symbols, group_entities=True,
    )
    # The root symbol index is included, not linked, to avoid an extra sidebar level.
    (navigation / "symbols/index.rst").unlink()
    for kind, title in (("namespace", "Namespaces"), ("page", "Doxygen pages")):
        if indexes[kind]:
            index = navigation / f"{kind}.rst"
            write_index(index, title, [page for name, page in sorted(indexes[kind])])
            top_level.append(index)
    directory_tree(navigation / "files", "Source files", files)
    top_level.append(navigation / "files/index.rst")
    write_index(listing, "By source directory", top_level, heading="-")
    root_page = Path(root.full_root_file_path)
    content = root_page.read_text(encoding="utf-8")
    listing_include = f".. include:: {listing.name}"
    if content.count(listing_include) != 1:
        raise ExtensionError("Expected one full API listing include in Exhale's root page")
    content = content.replace(listing_include, "").rstrip() + "\n"
    first_include = content.find(".. include:: ")
    if first_include < 0:
        raise ExtensionError("Expected hierarchy includes in Exhale's root page")
    content = (
        content[:first_include] + listing_include + "\n\n" + content[first_include:]
    )
    root_page.write_text(content, encoding="utf-8")
    orphan.write_text(
        ":orphan:\n\nFull API\n========\n\n"
        "See :doc:`library_root` for the directory-grouped API reference.\n",
        encoding="utf-8",
    )
    logger.info("Grouped %d API pages by source directory", len(filenames))


def setup(app):
    # Exhale generates its pages at the default priority (500).
    app.connect("builder-inited", generate_navigation, priority=600)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
