"""Assemble a persistent Pages tree from one independently built Sphinx version."""

import argparse
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit


LEGACY_BASE = "https://mach3-software.github.io/MaCh3/"
RELEASE = re.compile(r"v(\d+)\.(\d+)\.(\d+)(?:-([A-Za-z0-9][A-Za-z0-9.-]*))?")


def release_key(version):
    match = RELEASE.fullmatch(version)
    if match is None:
        raise ValueError(f"Expected a vMAJOR.MINOR.PATCH[-PRERELEASE] tag: {version}")
    major, minor, patch, prerelease = match.groups()
    identifiers = tuple(
        (0, int(part)) if part.isdigit() else (1, part)
        for part in (prerelease or "").split(".")
    )
    return int(major), int(minor), int(patch), prerelease is None, identifiers


def assemble(
    source, destination, version, base_url, legacy_manifest,
    legacy_site=None, preserve_legacy=False,
):
    if version not in ("develop", "docs-test"):
        release_key(version)
    if urlsplit(base_url).scheme not in ("http", "https") or not urlsplit(base_url).netloc:
        raise ValueError("The Pages base URL must be an absolute HTTP(S) URL")
    base_url = base_url.rstrip("/") + "/"
    if not (source / "index.html").is_file():
        raise ValueError(f"No built documentation at {source}")
    if (
        source.resolve() == destination.resolve()
        or destination.resolve() in source.resolve().parents
        or source.resolve() in destination.resolve().parents
    ):
        raise ValueError("The build source must be outside the persistent site")
    legacy = json.loads(legacy_manifest.read_text())
    manifest_path = destination / "versions.json"
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else []
    legacy_by_version = {
        entry["version"]: entry for entry in previous if entry.get("legacy", False)
    }
    legacy_by_version.update({entry["version"]: entry for entry in legacy})
    legacy = list(legacy_by_version.values())
    destination.mkdir(parents=True, exist_ok=True)

    # Preserve the old root and archives when replacing the upstream Pages site.
    if preserve_legacy:
        snapshot = destination / "legacy" / "develop"
        if not (snapshot / "index.html").is_file():
            if legacy_site is None or not (legacy_site / "index.html").is_file():
                raise ValueError("The first upstream deployment needs a legacy gh-pages checkout")
            for entry in legacy:
                if entry["version"] != "legacy-develop":
                    archive = legacy_site / ".Archive" / entry["version"] / "index.html"
                    if not archive.is_file():
                        raise ValueError(f"Missing legacy archive: {archive}")
            shutil.copytree(
                legacy_site, snapshot,
                ignore=shutil.ignore_patterns(".git", ".Archive"),
            )
            shutil.copytree(legacy_site / ".Archive", destination / ".Archive", dirs_exist_ok=True)
        for entry in legacy:
            if entry["url"].startswith(LEGACY_BASE):
                path = entry["url"].removeprefix(LEGACY_BASE)
                entry["url"] = base_url + (path or "legacy/develop/index.html")

    target = destination / version
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)

    versions = {
        entry["version"]: entry for entry in previous if not entry.get("legacy", False)
    }
    versions[version] = {"version": version, "name": version, "url": base_url + version + "/"}
    for name, entry in versions.items():
        entry["url"] = base_url + name + "/"
        entry["name"] = name
        entry.pop("preferred", None)
    releases = sorted(
        (name for name in versions if name not in ("develop", "docs-test")),
        key=release_key, reverse=True,
    )
    stable = next((name for name in releases if RELEASE.fullmatch(name).group(4) is None), None)
    preferred = stable or (
        "develop" if "develop" in versions else releases[0] if releases else "docs-test"
    )
    versions[preferred]["preferred"] = True
    if stable:
        versions[preferred]["name"] = f"{preferred} (stable)"
    ordered = ([versions["develop"]] if "develop" in versions else []) + [
        versions[name] for name in releases
    ]
    if "docs-test" in versions:
        ordered.append(versions["docs-test"])
    ordered.extend(entry for entry in legacy if entry["version"] not in versions)
    manifest_path.write_text(json.dumps(ordered, indent=2) + "\n")
    url = html.escape(base_url + preferred + "/", quote=True)
    (destination / "index.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<title>MaCh3 documentation</title>'
        f'<meta http-equiv="refresh" content="0; url={url}"></head>'
        f'<body><a href="{url}">Open MaCh3 documentation</a></body></html>\n'
    )
    (destination / ".nojekyll").touch()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--legacy-manifest", type=Path, required=True)
    parser.add_argument("--legacy-site", type=Path)
    parser.add_argument("--preserve-legacy", action="store_true")
    assemble(**vars(parser.parse_args()))
