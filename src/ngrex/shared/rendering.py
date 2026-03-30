"""Rendering contracts for markdown artifacts."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Protocol, TypeVar


DocumentT = TypeVar("DocumentT", contravariant=True)


@dataclass(frozen=True, slots=True, kw_only=True)
class MarkdownSection:
    """A normalized markdown section used by artifact renderers."""

    heading: str
    lines: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "lines", tuple(self.lines))


@dataclass(frozen=True, slots=True, kw_only=True)
class MarkdownDocument:
    """Structured markdown document contract shared across artifact types."""

    title: str
    sections: tuple[MarkdownSection, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "sections", tuple(self.sections))

    @property
    def headings(self) -> tuple[str, ...]:
        """Return headings in their defined order."""
        return tuple(section.heading for section in self.sections)


class MarkdownRenderer(Protocol[DocumentT]):
    """Interface implemented by markdown renderers in later tasks."""

    def render(self, document: DocumentT) -> str:
        """Render a structured document as markdown text."""


def coerce_lines(lines: Sequence[str]) -> tuple[str, ...]:
    """Normalize arbitrary sequences into immutable line tuples."""
    return tuple(lines)

