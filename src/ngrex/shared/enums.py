"""Stable enum contracts shared across orchestration components."""

from __future__ import annotations

from enum import StrEnum


class StageName(StrEnum):
    """High-level workflow stages used across the artifact pipeline."""

    DISCOVERY = "discovery"
    SPECIFICATION = "specification"
    PLANNING = "planning"
    IMPLEMENTATION = "implementation"
    INTEGRATION = "integration"


class RunStatus(StrEnum):
    """Lifecycle states for a run."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    NEEDS_CLARIFICATION = "needs_clarification"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


class ArtifactKind(StrEnum):
    """Canonical artifact identifiers and their required filenames."""

    DISCOVERY_CHECKLIST = "discovery_checklist"
    SPECIFICATION = "specification"
    TASK_GRAPH = "task_graph"
    TASK_IMPLEMENTATION = "task_implementation"
    INTEGRATION_REPORT = "integration_report"

    @property
    def filename(self) -> str:
        """Return the required persisted filename for this artifact kind."""
        return {
            ArtifactKind.DISCOVERY_CHECKLIST: "DISCOVERY_CHECKLIST.md",
            ArtifactKind.SPECIFICATION: "SPEC.md",
            ArtifactKind.TASK_GRAPH: "TASK_GRAPH.md",
            ArtifactKind.TASK_IMPLEMENTATION: "TASK_IMPLEMENTATION.md",
            ArtifactKind.INTEGRATION_REPORT: "INTEGRATION_REPORT.md",
        }[self]

    @property
    def default_stage(self) -> StageName:
        """Return the stage that normally owns this artifact kind."""
        return {
            ArtifactKind.DISCOVERY_CHECKLIST: StageName.DISCOVERY,
            ArtifactKind.SPECIFICATION: StageName.SPECIFICATION,
            ArtifactKind.TASK_GRAPH: StageName.PLANNING,
            ArtifactKind.TASK_IMPLEMENTATION: StageName.IMPLEMENTATION,
            ArtifactKind.INTEGRATION_REPORT: StageName.INTEGRATION,
        }[self]


class DependencyLevel(StrEnum):
    """Dependency classifications from the planning artifacts."""

    NONE = "none"
    SOFT = "soft"
    HARD = "hard"

