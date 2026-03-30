"""Shared models, contracts, and utilities live in this package."""

from ngrex.shared.artifacts import ArtifactMetadata, ArtifactRecord
from ngrex.shared.clarifications import (
    ClarificationPayload,
    ClarificationQuestion,
    ClarificationResponse,
)
from ngrex.shared.enums import ArtifactKind, DependencyLevel, RunStatus, StageName
from ngrex.shared.rendering import MarkdownDocument, MarkdownRenderer, MarkdownSection
from ngrex.shared.run_state import RunRecord, StageResult
from ngrex.shared.task_graph import ExecutionGroup, ExecutionPhase, TaskDefinition, TaskGraphDocument

__all__ = [
    "ArtifactKind",
    "ArtifactMetadata",
    "ArtifactRecord",
    "ClarificationPayload",
    "ClarificationQuestion",
    "ClarificationResponse",
    "DependencyLevel",
    "ExecutionGroup",
    "ExecutionPhase",
    "MarkdownDocument",
    "MarkdownRenderer",
    "MarkdownSection",
    "RunRecord",
    "RunStatus",
    "StageName",
    "StageResult",
    "TaskDefinition",
    "TaskGraphDocument",
]
