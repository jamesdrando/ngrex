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

