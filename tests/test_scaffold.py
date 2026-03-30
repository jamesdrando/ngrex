"""Smoke tests for the initial project scaffold."""

from __future__ import annotations

import unittest

import ngrex
from ngrex.cli.main import build_parser, main


class ScaffoldTestCase(unittest.TestCase):
    """Validate that the base package layout is importable."""

    def test_version_is_exposed(self) -> None:
        self.assertEqual(ngrex.__version__, "0.1.0")

    def test_cli_parser_has_expected_program_name(self) -> None:
        self.assertEqual(build_parser().prog, "ngrex")

    def test_cli_main_returns_success_without_arguments(self) -> None:
        self.assertEqual(main([]), 0)


if __name__ == "__main__":
    unittest.main()
