"""Include help from the compiled MaCh3 CLI and its registered subcommands."""

import os
import re
import shutil
import subprocess

from docutils import nodes
from sphinx.errors import ExtensionError
from sphinx.util.docutils import SphinxDirective


def read_help(executable, arguments):
    command = [executable, *arguments, "--help"]
    environment = os.environ.copy()
    # Document only built-in commands, independent of the builder's plugins.
    environment.pop("MACH3_PLUGINS", None)
    environment["NO_COLOR"] = "1"
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=True,
            timeout=30, env=environment,
        )
    except subprocess.CalledProcessError as error:
        raise ExtensionError(
            f"CLI documentation command {command!r} exited with {error.returncode}:\n"
            f"{error.stdout}\n{error.stderr}"
        ) from error
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ExtensionError(f"Cannot generate CLI help with {command!r}: {error}") from error
    if result.stderr.strip():
        raise ExtensionError(f"CLI help reported errors for {command!r}:\n{result.stderr}")
    if not result.stdout.startswith("Usage:"):
        raise ExtensionError(f"CLI help has no Usage header for {command!r}:\n{result.stdout}")
    return result.stdout.rstrip()


def subcommands(help_text):
    commands = []
    in_commands = False
    for line in help_text.splitlines():
        if line == "Subcommands:":
            in_commands = True
        elif in_commands and line.strip():
            if not line.startswith(" "):
                break
            match = re.match(r"^\s+([A-Za-z0-9][A-Za-z0-9_-]*)(?:\s|$)", line)
            if match is None:
                raise ExtensionError(f"Cannot parse CLI subcommand entry: {line!r}")
            commands.append(match.group(1))
    return commands


class Mach3Help(SphinxDirective):
    def run(self):
        executable = shutil.which(self.config.mach3_executable)
        if executable is None:
            raise ExtensionError(
                f"Cannot find MaCh3 CLI: {self.config.mach3_executable!r}. "
                "Build and install MaCh3, then set MACH3_EXECUTABLE to its executable."
            )
        self.env.note_dependency(executable)

        def section(arguments):
            output = read_help(executable, arguments)
            title = "mach3" + "".join(f" {argument}" for argument in arguments)
            result = nodes.section(ids=[nodes.make_id(title)])
            result += nodes.title(text=title)
            result += nodes.literal_block(output, output, language="text")
            for command in subcommands(output):
                result += section([*arguments, command])
            return result

        root = section([])
        # Root help and subcommand headings are peers on the guide page.
        children = list(root.findall(nodes.section, include_self=False, descend=False))
        for child in children:
            root.remove(child)
        return [root, *children]


def setup(app):
    app.add_config_value("mach3_executable", "mach3", "env", types=[str])
    app.add_directive("mach3-help", Mach3Help)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
