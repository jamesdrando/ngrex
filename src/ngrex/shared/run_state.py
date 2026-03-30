"""Run-state contracts shared by workflow, storage, and CLI layers."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime

from ngrex.shared.artifacts import ArtifactMetadata
from ngrex.shared.clarifications import ClarificationPayload, utc_now
from ngrex.shared.enums import RunStatus, StageName


@dataclass(frozen=True, slots=True, kw_only=True)
class StageResult:
    """The recorded outcome of a single pipeline stage."""

    stage: StageName
    status: RunStatus
    started_at: datetime = field(default_factory=utc_now)
    finished_at: datetime | None = None
    error_message: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class RunRecord:
    """Immutable run-state record shared across persistence and workflow layers."""

    run_id: str
    prompt: str
    status: RunStatus = RunStatus.PENDING
    current_stage: StageName | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    clarification_payload: ClarificationPayload = field(default_factory=ClarificationPayload)
    stage_results: tuple[StageResult, ...] = field(default_factory=tuple)
    artifacts: tuple[ArtifactMetadata, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "stage_results", tuple(self.stage_results))
        object.__setattr__(self, "artifacts", tuple(self.artifacts))

    def with_status(
        self,
        status: RunStatus,
        *,
        current_stage: StageName | None = None,
    ) -> RunRecord:
        """Return a new record with updated run status metadata."""
        return replace(
            self,
            status=status,
            current_stage=current_stage,
            updated_at=utc_now(),
        )

    def with_clarification_payload(self, payload: ClarificationPayload) -> RunRecord:
        """Return a new record with updated clarification data."""
        return replace(
            self,
            clarification_payload=payload,
            updated_at=utc_now(),
        )

    def append_stage_result(self, stage_result: StageResult) -> RunRecord:
        """Return a new record with an additional stage result."""
        return replace(
            self,
            stage_results=(*self.stage_results, stage_result),
            updated_at=utc_now(),
        )

    def append_artifact(self, artifact: ArtifactMetadata) -> RunRecord:
        """Return a new record with an additional artifact reference."""
        return replace(
            self,
            artifacts=(*self.artifacts, artifact),
            updated_at=utc_now(),
        )

