"""Artifact metadata contracts shared across the system."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from ngrex.shared.clarifications import utc_now
from ngrex.shared.enums import ArtifactKind, StageName


@dataclass(frozen=True, slots=True, kw_only=True)
class ArtifactMetadata:
    """Metadata that identifies a persisted markdown artifact."""

    kind: ArtifactKind
    stage: StageName
    path: Path | None = None
    content_type: str = "text/markdown"
    created_at: datetime = field(default_factory=utc_now)


@dataclass(frozen=True, slots=True, kw_only=True)
class ArtifactRecord:
    """Persistable artifact payload plus identifying metadata."""

    metadata: ArtifactMetadata
    title: str
    body: str

