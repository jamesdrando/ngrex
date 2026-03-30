"""Contracts for clarification questions and responses."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(UTC)


@dataclass(frozen=True, slots=True, kw_only=True)
class ClarificationQuestion:
    """A single clarification question surfaced during discovery."""

    key: str
    prompt: str
    required: bool = True
    context: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class ClarificationResponse:
    """A user-supplied answer to a clarification question."""

    key: str
    answer: str
    answered_at: datetime = field(default_factory=utc_now)


@dataclass(frozen=True, slots=True, kw_only=True)
class ClarificationPayload:
    """The clarification surface exchanged between discovery and later stages."""

    questions: tuple[ClarificationQuestion, ...] = field(default_factory=tuple)
    responses: tuple[ClarificationResponse, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "questions", tuple(self.questions))
        object.__setattr__(self, "responses", tuple(self.responses))

