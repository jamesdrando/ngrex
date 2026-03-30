# Task Summary

Implement `TASK-001` by establishing the Python project scaffold for the MVP artifact pipeline.

# Implementation Plan

- Create a `src`-based Python package named `ngrex`.
- Add package directories for agents, orchestrator, storage, shared models, and CLI.
- Add minimal project configuration so the package can be installed, invoked, and tested locally.
- Add a small smoke test that validates imports and basic CLI wiring.

# Files Created

- `.gitignore`
- `pyproject.toml`
- `src/ngrex/__init__.py`
- `src/ngrex/__main__.py`
- `src/ngrex/agents/__init__.py`
- `src/ngrex/cli/__init__.py`
- `src/ngrex/cli/main.py`
- `src/ngrex/orchestrator/__init__.py`
- `src/ngrex/shared/__init__.py`
- `src/ngrex/storage/__init__.py`
- `tests/test_scaffold.py`

# Files Modified

- None

# Code Implementation

FILE: .gitignore
```gitignore
__pycache__/
.pytest_cache/
.ruff_cache/
.venv/
*.pyc
*.pyo
*.pyd
*.egg-info/
build/
dist/
```

FILE: pyproject.toml
```toml
[build-system]
requires = ["hatchling>=1.25.0"]
build-backend = "hatchling.build"

[project]
name = "ngrex"
version = "0.1.0"
description = "Multi-agent software delivery system with a Python-first artifact pipeline."
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
  "langgraph>=0.2,<1.0",
]

[project.optional-dependencies]
dev = [
  "pytest>=8.0,<9.0",
  "ruff>=0.6,<1.0",
]

[project.scripts]
ngrex = "ngrex.cli.main:main"

[tool.hatch.build.targets.wheel]
packages = ["src/ngrex"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]

[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]
```

FILE: src/ngrex/__init__.py
```python
"""Top-level package for ngrex."""

__all__ = ["__version__"]

__version__ = "0.1.0"
```

FILE: src/ngrex/__main__.py
```python
"""Module entrypoint for ``python -m ngrex``."""

from ngrex.cli.main import main


if __name__ == "__main__":
    raise SystemExit(main())
```

FILE: src/ngrex/agents/__init__.py
```python
"""Agent role implementations live in this package."""
```

FILE: src/ngrex/cli/__init__.py
```python
"""CLI package for local operator entrypoints."""
```

FILE: src/ngrex/cli/main.py
```python
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
```

FILE: src/ngrex/orchestrator/__init__.py
```python
"""Orchestration workflows and state management live in this package."""
```

FILE: src/ngrex/shared/__init__.py
```python
"""Shared models, contracts, and utilities live in this package."""
```

FILE: src/ngrex/storage/__init__.py
```python
"""Persistence backends and repositories live in this package."""
```

FILE: tests/test_scaffold.py
```python
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
```

# Tests

- Added `tests/test_scaffold.py` to verify package importability and baseline CLI wiring.

# Integration Notes

- The `src/ngrex` layout maps directly to the task graph domains so later tasks can add implementation without restructuring the repository.
- The CLI entrypoint is intentionally minimal and can be extended in `TASK-009`.
- The package avoids importing LangGraph during scaffold setup so later workflow work can add it without affecting basic package imports.

# Task Completion Checklist

- task goal is satisfied
- interfaces are respected
- no unrelated files were modified
- implementation compiles or runs
- implementation stays within scope
