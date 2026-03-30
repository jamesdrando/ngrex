# TASK_GRAPH.md

# Planning Goal

This plan is optimized for high parallel execution with controlled dependencies, using contract-first tasks to unlock independent Python and LangGraph implementation work as early as possible.

# Assumptions

- The initial build target is the Phase 1 artifact pipeline defined in the repository guidance.
- The MVP interface is a local CLI backed by an internal Python orchestration API.
- Filesystem persistence is acceptable for the first version.
- LangGraph is the selected orchestration framework for the MVP.

# Dependency Strategy

The plan creates a small set of foundation anchors first: Python project structure, shared contracts for run state and artifacts, and prompt or template interfaces for the agent roles. These anchors convert most downstream dependencies into soft dependencies. Agent implementations then proceed in parallel in isolated modules, while storage and CLI work advance on the shared contracts. Integration is held until the workflow graph, role agents, storage, and CLI all exist. Validation is separated from implementation so the end-to-end checks happen against the integrated pipeline instead of blocking parallel work early.

# Workstreams

- shared contracts and project foundation
- agent prompts and artifact rendering
- orchestration workflow
- artifact persistence and run state
- role-specific agent implementations
- CLI and configuration surface
- integration and validation

# Execution Phases

## Phase 1 — Foundation Anchors

- TASK-001
- TASK-002
- TASK-003

## Phase 2 — Parallel Implementation

- TASK-004
- TASK-005
- TASK-006
- TASK-007
- TASK-008
- TASK-009

## Phase 3 — Integration

- TASK-010

## Phase 4 — Hardening

- TASK-011
- TASK-012

# Task List

## TASK-001 — Create Python Project Foundation

**Goal**
- Establish the Python package, repository layout, and base tooling needed for the MVP artifact pipeline.

**Scope**
- Create package directories for orchestration, agents, storage, CLI, and shared models.
- Add project configuration files needed to run and test the code locally.
- Do not implement business logic beyond placeholder package wiring.

**Inputs**
- `AGENTS.md`
- `docs/artifacts/SPEC.md`
- Existing repository files

**Dependencies**
- None

**Outputs**
- Python project scaffold
- Package directory structure
- Baseline tooling configuration

**Parallelization Notes**
- Can start immediately and should avoid defining detailed runtime behavior that belongs to later tasks.

**Assigned Domain**
- shared

## TASK-002 — Define Shared Contracts and Data Models

**Goal**
- Define the core contracts that let orchestration, storage, CLI, and agent modules proceed independently.

**Scope**
- Define run status, stage identifiers, artifact metadata, clarification payloads, and task-graph document interfaces.
- Create shared model modules and markdown artifact rendering contracts.
- Do not implement agent logic or storage backends.

**Inputs**
- `AGENTS.md`
- `docs/artifacts/SPEC.md`
- `docs/artifacts/DISCOVERY_CHECKLIST.md`

**Dependencies**
- Soft
- TASK-001

**Outputs**
- Shared Python models
- Artifact and run-state contracts
- Rendering interface definitions

**Parallelization Notes**
- Unlocks nearly all downstream work; keep contracts minimal and stable to reduce churn.

**Assigned Domain**
- shared

## TASK-003 — Define Prompt Assets and Artifact Templates

**Goal**
- Centralize the role prompts and document templates used by discovery, specification, and planner agents.

**Scope**
- Create prompt-loading utilities or prompt assets.
- Define markdown template helpers for the required artifact section order.
- Do not wire prompts into the orchestration graph yet.

**Inputs**
- `system/DISCOVERY.AGENT.md`
- `system/SPECIFICATION.AGENT.md`
- `system/PLANNER.AGENT.md`
- `docs/artifacts/SPEC.md`

**Dependencies**
- Soft
- TASK-001

**Outputs**
- Prompt assets
- Artifact template helpers

**Parallelization Notes**
- Can run in parallel with TASK-002 as long as it does not redefine shared model shapes.

**Assigned Domain**
- shared

## TASK-004 — Implement Artifact Storage and Run Repository

**Goal**
- Provide local persistence for runs, artifacts, and stage results.

**Scope**
- Implement filesystem-backed storage for run metadata and generated markdown artifacts.
- Support create, read, update, and list operations needed by the MVP CLI.
- Do not implement orchestration logic or CLI commands.

**Inputs**
- `docs/artifacts/SPEC.md`
- Shared contracts from TASK-002

**Dependencies**
- Hard
- TASK-002

**Outputs**
- Storage module
- Run repository implementation
- Persistence tests for storage behavior

**Parallelization Notes**
- Independent of agent behavior once contracts are fixed; should avoid editing workflow code.

**Assigned Domain**
- data

## TASK-005 — Build LangGraph Workflow Skeleton

**Goal**
- Create the orchestration graph that enforces stage order and passes state between stages.

**Scope**
- Implement the LangGraph state definition and stage transitions for discovery, specification, and planning.
- Provide extension points for clarification inputs and validation status.
- Do not implement the internal logic of each agent stage beyond callable interfaces.

**Inputs**
- `docs/artifacts/SPEC.md`
- Shared contracts from TASK-002

**Dependencies**
- Hard
- TASK-002

**Outputs**
- LangGraph workflow module
- Orchestration state wiring

**Parallelization Notes**
- Can proceed before role agents are complete by depending on stage interfaces and placeholders.

**Assigned Domain**
- backend

## TASK-006 — Implement Discovery Agent Stage

**Goal**
- Implement the discovery stage that produces `DISCOVERY_CHECKLIST.md` from run input.

**Scope**
- Build the discovery agent module using the shared prompt assets and artifact contracts.
- Return structured output compatible with workflow and storage layers.
- Do not implement specification or planning stages.

**Inputs**
- `system/DISCOVERY.AGENT.md`
- Shared contracts from TASK-002
- Prompt assets from TASK-003

**Dependencies**
- Hard
- TASK-002

**Outputs**
- Discovery agent module
- Discovery artifact rendering logic
- Stage-level tests

**Parallelization Notes**
- Can run in parallel with TASK-007 and TASK-008; should not modify shared workflow files except through defined interfaces.

**Assigned Domain**
- backend

## TASK-007 — Implement Specification Agent Stage

**Goal**
- Implement the specification stage that produces `SPEC.md` from clarified run context.

**Scope**
- Build the specification agent module using the shared prompt assets and artifact contracts.
- Support explicit assumptions when required by missing information.
- Do not implement discovery or planning logic.

**Inputs**
- `system/SPECIFICATION.AGENT.md`
- Shared contracts from TASK-002
- Prompt assets from TASK-003

**Dependencies**
- Hard
- TASK-002

**Outputs**
- Specification agent module
- Specification artifact rendering logic
- Stage-level tests

**Parallelization Notes**
- Parallel with TASK-006 and TASK-008 if it avoids touching shared state definitions.

**Assigned Domain**
- backend

## TASK-008 — Implement Planner Agent Stage

**Goal**
- Implement the planner stage that produces `TASK_GRAPH.md` from the specification artifact.

**Scope**
- Build the planner agent module using the shared prompt assets and artifact contracts.
- Ensure output supports explicit dependency classification and execution grouping.
- Do not implement execution of implementation tasks.

**Inputs**
- `system/PLANNER.AGENT.md`
- Shared contracts from TASK-002
- Prompt assets from TASK-003

**Dependencies**
- Hard
- TASK-002

**Outputs**
- Planner agent module
- Task-graph artifact rendering logic
- Stage-level tests

**Parallelization Notes**
- Parallel with TASK-006 and TASK-007; should avoid workflow and CLI file ownership.

**Assigned Domain**
- backend

## TASK-009 — Implement CLI and Configuration Surface

**Goal**
- Provide a local operator interface for creating runs, submitting clarifications, and retrieving artifacts.

**Scope**
- Implement CLI commands and configuration loading for the MVP.
- Connect CLI actions to workflow execution and run retrieval interfaces.
- Do not implement storage internals or role-agent logic.

**Inputs**
- `docs/artifacts/SPEC.md`
- Shared contracts from TASK-002
- Storage interfaces from TASK-004
- Workflow interfaces from TASK-005

**Dependencies**
- Hard
- TASK-004
- TASK-005

**Outputs**
- CLI module
- Configuration loader
- CLI-level tests

**Parallelization Notes**
- Can progress with interface stubs once TASK-004 and TASK-005 define their public surfaces; avoid editing role-agent files.

**Assigned Domain**
- backend

## TASK-010 — Integrate End-to-End Artifact Pipeline

**Goal**
- Wire the workflow, agent stages, storage, and CLI into a functioning Phase 1 system.

**Scope**
- Connect stage implementations into the LangGraph workflow.
- Connect workflow outputs to persistence and CLI commands.
- Resolve interface mismatches with minimal adapters.

**Inputs**
- Outputs from TASK-004 through TASK-009
- `docs/artifacts/SPEC.md`
- `docs/artifacts/TASK_GRAPH.md`

**Dependencies**
- Hard
- TASK-004
- TASK-005
- TASK-006
- TASK-007
- TASK-008
- TASK-009

**Outputs**
- Integrated artifact pipeline
- Minimal integration adapters
- Integration report inputs

**Parallelization Notes**
- Should begin only after component interfaces stabilize; keep changes localized to wiring boundaries.

**Assigned Domain**
- integration

## TASK-011 — Validate the MVP Artifact Pipeline

**Goal**
- Verify that the integrated system can produce and persist the required artifact chain.

**Scope**
- Add and run targeted end-to-end validation for run creation, artifact generation order, and artifact retrieval.
- Record what is and is not validated.
- Do not add broad non-MVP test coverage.

**Inputs**
- Integrated system from TASK-010
- `docs/artifacts/SPEC.md`

**Dependencies**
- Hard
- TASK-010

**Outputs**
- End-to-end validation tests
- Validation results documentation

**Parallelization Notes**
- Independent from documentation polish; keep focus on real behavioral verification.

**Assigned Domain**
- testing

## TASK-012 — Document Local Operation and Next-Phase Extension Points

**Goal**
- Add concise operator documentation for using the MVP and identify extension points for later phases.

**Scope**
- Document local setup, run execution, artifact locations, and known MVP limitations.
- Document extension seams for future execution runtime, VPS workers, and chat UI.
- Do not add new runtime functionality.

**Inputs**
- `docs/artifacts/SPEC.md`
- Outputs from TASK-009, TASK-010, and TASK-011

**Dependencies**
- Hard
- TASK-011

**Outputs**
- Updated README or runbook
- Phase-transition notes

**Parallelization Notes**
- Can start drafting earlier, but final completion should wait for validated behavior.

**Assigned Domain**
- shared

# Parallel Execution Groups

## Group A — Start Immediately

- TASK-001
- TASK-002
- TASK-003

## Group B — Starts After Shared Contracts

- TASK-004
- TASK-005
- TASK-006
- TASK-007
- TASK-008

## Group C — Starts After Workflow and Storage Interfaces

- TASK-009

## Group D — Integration

- TASK-010

## Group E — Validation and Hardening

- TASK-011
- TASK-012

# Critical Path

TASK-001 -> TASK-002 -> TASK-005 -> longest of TASK-006/TASK-007/TASK-008 -> TASK-010 -> TASK-011 -> TASK-012

# Merge Risk Notes

- Shared contract files are the highest collision point between storage, workflow, CLI, and agent tasks. Reduce risk by assigning one owner to shared models and treating changes after TASK-002 as integration-only.
- The LangGraph workflow module can collide with stage implementations if agents edit registration directly. Reduce risk by exposing stage callables through isolated modules and reserving graph wiring for TASK-005 and TASK-010.
- CLI and configuration files may drift from storage or workflow interfaces. Reduce risk by freezing public method signatures before TASK-009 begins.
- Prompt assets can become a hidden shared dependency across role-agent tasks. Reduce risk by centralizing prompt loading in TASK-003 and avoiding per-agent prompt duplication.

# Recommended Agent Assignment Strategy

- Assign one agent to foundation and contracts work: TASK-001 through TASK-003.
- Assign one agent each to the discovery, specification, and planner stage implementations: TASK-006, TASK-007, and TASK-008.
- Assign one agent to storage and one agent to workflow and CLI surfaces: TASK-004, TASK-005, and TASK-009, split by file ownership.
- Reserve a separate integration and validation agent for TASK-010 through TASK-012.
