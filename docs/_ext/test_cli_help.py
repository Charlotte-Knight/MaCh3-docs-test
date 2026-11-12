import subprocess
import unittest
from unittest.mock import patch

from sphinx.errors import ExtensionError

from cli_help import read_help, subcommands


class CliHelpTests(unittest.TestCase):
    def test_discovers_commands_from_help_not_a_fixed_list(self):
        output = (
            "Usage: mach3 [--help] {diag,new-command}\n\n"
            "Subcommands:\n"
            "  diag         Diagnostics\n"
            "  new-command  A newly registered command\n\n"
            "Other heading:\n"
            "  not-a-command\n"
        )
        self.assertEqual(subcommands(output), ["diag", "new-command"])

    def test_leaf_help_has_no_commands(self):
        self.assertEqual(subcommands("Usage: mach3 diag [--help] CONFIG"), [])

    def test_invalid_subcommand_entry_fails(self):
        with self.assertRaisesRegex(ExtensionError, "Cannot parse"):
            subcommands("Subcommands:\n  --invalid  Not a command")

    @patch("cli_help.subprocess.run")
    def test_invocation_is_help_only_and_plugins_are_removed(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, "Usage: mach3 diag\n\n", "")
        with patch.dict("os.environ", {"MACH3_PLUGINS": "/some/plugin.so"}):
            output = read_help("/build/bin/mach3", ["diag"])
        self.assertEqual(output, "Usage: mach3 diag")
        args, kwargs = run.call_args
        self.assertEqual(args[0], ["/build/bin/mach3", "diag", "--help"])
        self.assertNotIn("MACH3_PLUGINS", kwargs["env"])
        self.assertEqual(kwargs["timeout"], 30)
        self.assertTrue(kwargs["check"])

    @patch("cli_help.subprocess.run")
    def test_nonzero_exit_reports_command_and_diagnostics(self, run):
        run.side_effect = subprocess.CalledProcessError(
            3, ["mach3", "--help"], output="partial output", stderr="missing library",
        )
        with self.assertRaisesRegex(ExtensionError, "missing library"):
            read_help("mach3", [])

    @patch("cli_help.subprocess.run")
    def test_timeout_and_execution_errors_fail_explicitly(self, run):
        for error in (subprocess.TimeoutExpired("mach3", 30), FileNotFoundError("missing")):
            with self.subTest(error=error):
                run.side_effect = error
                with self.assertRaisesRegex(ExtensionError, "Cannot generate CLI help"):
                    read_help("mach3", [])

    @patch("cli_help.subprocess.run")
    def test_empty_output_and_stderr_are_not_accepted(self, run):
        for stdout, stderr in (("", ""), ("Usage: mach3", "runtime error")):
            with self.subTest(stdout=stdout, stderr=stderr):
                run.return_value = subprocess.CompletedProcess([], 0, stdout, stderr)
                with self.assertRaises(ExtensionError):
                    read_help("mach3", [])


if __name__ == "__main__":
    unittest.main()
