"""Minimal CLI wiring for the ngrex package."""

from __future__ import annotations

import argparse
from collections.abc import Sequence


def build_parser() -> argparse.ArgumentParser:
    """Create the base parser that later tasks will extend with subcommands."""
    parser = argparse.ArgumentParser(
        prog="ngrex",
        description="Python-first multi-agent delivery system.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Parse arguments and exit successfully for the scaffold stage."""
    build_parser().parse_args(argv)
    return 0
