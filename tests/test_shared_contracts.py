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

