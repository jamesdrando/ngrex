# Task Summary

Implement `TASK-002` by defining shared contracts for run state, artifacts, clarifications, task-graph documents, and markdown rendering.

# Implementation Plan

- Add stable shared enums for workflow stages, run status, artifact kinds, and dependency levels.
- Add frozen dataclass models for artifacts, clarification payloads, task-graph structures, stage results, and run records.
- Add a generic markdown renderer protocol plus normalized section and document contracts.
- Export the shared contract surface through `ngrex.shared`.
- Add tests that validate the key contract behaviors used by downstream tasks.

# Files Created

- `src/ngrex/shared/enums.py`
- `src/ngrex/shared/rendering.py`
- `src/ngrex/shared/clarifications.py`
- `src/ngrex/shared/artifacts.py`
- `src/ngrex/shared/task_graph.py`
- `src/ngrex/shared/run_state.py`
- `tests/test_shared_contracts.py`

# Files Modified

- `src/ngrex/shared/__init__.py`

# Code Implementation

FILE: src/ngrex/shared/enums.py
```python
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
```

FILE: src/ngrex/shared/rendering.py
```python
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
```

FILE: src/ngrex/shared/clarifications.py
```python
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
```

FILE: src/ngrex/shared/artifacts.py
```python
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
```

FILE: src/ngrex/shared/task_graph.py
```python
"""Task graph document contracts for planner output."""

from __future__ import annotations

from dataclasses import dataclass, field

from ngrex.shared.enums import DependencyLevel


@dataclass(frozen=True, slots=True, kw_only=True)
class TaskDefinition:
    """A single executable task within a task graph."""

    task_id: str
    name: str
    goal: str
    scope: tuple[str, ...] = field(default_factory=tuple)
    inputs: tuple[str, ...] = field(default_factory=tuple)
    dependency_level: DependencyLevel = DependencyLevel.NONE
    dependencies: tuple[str, ...] = field(default_factory=tuple)
    outputs: tuple[str, ...] = field(default_factory=tuple)
    parallelization_notes: tuple[str, ...] = field(default_factory=tuple)
    assigned_domain: str = "shared"

    def __post_init__(self) -> None:
        object.__setattr__(self, "scope", tuple(self.scope))
        object.__setattr__(self, "inputs", tuple(self.inputs))
        object.__setattr__(self, "dependencies", tuple(self.dependencies))
        object.__setattr__(self, "outputs", tuple(self.outputs))
        object.__setattr__(self, "parallelization_notes", tuple(self.parallelization_notes))


@dataclass(frozen=True, slots=True, kw_only=True)
class ExecutionPhase:
    """A named planning phase and the tasks that belong to it."""

    name: str
    task_ids: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "task_ids", tuple(self.task_ids))


@dataclass(frozen=True, slots=True, kw_only=True)
class ExecutionGroup:
    """A concurrently executable group of tasks."""

    name: str
    task_ids: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "task_ids", tuple(self.task_ids))


@dataclass(frozen=True, slots=True, kw_only=True)
class TaskGraphDocument:
    """Structured planner output that can later be rendered to markdown."""

    planning_goal: str
    assumptions: tuple[str, ...] = field(default_factory=tuple)
    dependency_strategy: str = ""
    workstreams: tuple[str, ...] = field(default_factory=tuple)
    execution_phases: tuple[ExecutionPhase, ...] = field(default_factory=tuple)
    tasks: tuple[TaskDefinition, ...] = field(default_factory=tuple)
    execution_groups: tuple[ExecutionGroup, ...] = field(default_factory=tuple)
    critical_path: tuple[str, ...] = field(default_factory=tuple)
    merge_risk_notes: tuple[str, ...] = field(default_factory=tuple)
    agent_assignment_strategy: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "assumptions", tuple(self.assumptions))
        object.__setattr__(self, "workstreams", tuple(self.workstreams))
        object.__setattr__(self, "execution_phases", tuple(self.execution_phases))
        object.__setattr__(self, "tasks", tuple(self.tasks))
        object.__setattr__(self, "execution_groups", tuple(self.execution_groups))
        object.__setattr__(self, "critical_path", tuple(self.critical_path))
        object.__setattr__(self, "merge_risk_notes", tuple(self.merge_risk_notes))
        object.__setattr__(self, "agent_assignment_strategy", tuple(self.agent_assignment_strategy))

    @property
    def task_ids(self) -> tuple[str, ...]:
        """Return task identifiers in document order."""
        return tuple(task.task_id for task in self.tasks)
```

FILE: src/ngrex/shared/run_state.py
```python
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
```

FILE: src/ngrex/shared/__init__.py
```python
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
```

FILE: tests/test_shared_contracts.py
```python
"""Tests for shared contract models introduced in TASK-002."""

from __future__ import annotations

import unittest

from ngrex.shared import (
    ArtifactKind,
    ArtifactMetadata,
    ClarificationPayload,
    ClarificationQuestion,
    ClarificationResponse,
    DependencyLevel,
    ExecutionGroup,
    ExecutionPhase,
    MarkdownDocument,
    MarkdownSection,
    RunRecord,
    RunStatus,
    StageName,
    StageResult,
    TaskDefinition,
    TaskGraphDocument,
)


class SharedContractsTestCase(unittest.TestCase):
    """Verify the contract surface used by downstream tasks."""

    def test_artifact_kind_exposes_required_filename_and_stage(self) -> None:
        self.assertEqual(ArtifactKind.DISCOVERY_CHECKLIST.filename, "DISCOVERY_CHECKLIST.md")
        self.assertEqual(ArtifactKind.TASK_GRAPH.default_stage, StageName.PLANNING)

    def test_run_record_helpers_preserve_history(self) -> None:
        run = RunRecord(run_id="run-001", prompt="Build a planning system")
        payload = ClarificationPayload(
            questions=(ClarificationQuestion(key="mvp", prompt="What is the MVP?"),),
            responses=(ClarificationResponse(key="mvp", answer="Artifact pipeline"),),
        )
        artifact = ArtifactMetadata(
            kind=ArtifactKind.DISCOVERY_CHECKLIST,
            stage=StageName.DISCOVERY,
        )
        stage_result = StageResult(
            stage=StageName.DISCOVERY,
            status=RunStatus.COMPLETED,
        )

        updated = (
            run.with_status(RunStatus.IN_PROGRESS, current_stage=StageName.DISCOVERY)
            .with_clarification_payload(payload)
            .append_stage_result(stage_result)
            .append_artifact(artifact)
        )

        self.assertEqual(run.status, RunStatus.PENDING)
        self.assertEqual(updated.status, RunStatus.IN_PROGRESS)
        self.assertEqual(updated.current_stage, StageName.DISCOVERY)
        self.assertEqual(len(updated.clarification_payload.questions), 1)
        self.assertEqual(len(updated.stage_results), 1)
        self.assertEqual(updated.artifacts[0].kind, ArtifactKind.DISCOVERY_CHECKLIST)

    def test_task_graph_document_keeps_document_order(self) -> None:
        first = TaskDefinition(
            task_id="TASK-001",
            name="Create scaffold",
            goal="Set up the repo",
            dependency_level=DependencyLevel.NONE,
        )
        second = TaskDefinition(
            task_id="TASK-002",
            name="Define contracts",
            goal="Create shared models",
            dependency_level=DependencyLevel.SOFT,
            dependencies=("TASK-001",),
        )
        document = TaskGraphDocument(
            planning_goal="Optimize for safe parallelism",
            assumptions=("CLI MVP",),
            dependency_strategy="Use shared contracts first.",
            workstreams=("shared", "backend"),
            execution_phases=(ExecutionPhase(name="Phase 1", task_ids=("TASK-001", "TASK-002")),),
            tasks=(first, second),
            execution_groups=(ExecutionGroup(name="Start Immediately", task_ids=("TASK-001",)),),
            critical_path=("TASK-001", "TASK-002"),
        )

        self.assertEqual(document.task_ids, ("TASK-001", "TASK-002"))
        self.assertEqual(document.execution_phases[0].task_ids[1], "TASK-002")

    def test_markdown_document_normalizes_section_containers(self) -> None:
        document = MarkdownDocument(
            title="SPEC.md",
            sections=[MarkdownSection(heading="Problem Definition", lines=["Line 1", "Line 2"])],
        )

        self.assertEqual(document.headings, ("Problem Definition",))
        self.assertEqual(document.sections[0].lines, ("Line 1", "Line 2"))


if __name__ == "__main__":
    unittest.main()
```

# Tests

- Added `tests/test_shared_contracts.py` to verify enum mappings, immutable run updates, task-graph ordering, and markdown document normalization.

# Integration Notes

- `RunRecord` is immutable and uses helper methods to support safe state transitions across workflow and storage layers.
- `ArtifactKind` now centralizes required filenames and stage ownership so downstream tasks do not duplicate that mapping.
- `TaskGraphDocument` and `MarkdownRenderer` provide the planning and rendering interfaces that later workflow and agent tasks can build against without revisiting the shared contract surface.

# Task Completion Checklist

- task goal is satisfied
- interfaces are respected
- no unrelated files were modified
- implementation compiles or runs
- implementation stays within scope
