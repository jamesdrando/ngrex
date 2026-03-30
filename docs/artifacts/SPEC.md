# SPEC.md

# Problem Definition

Teams need a deterministic way to turn a rough software project idea into structured delivery artifacts that can be executed by specialized agents with clear boundaries.

The primary user for the MVP is a developer or operator initiating and reviewing runs.

The system delivers value by producing auditable planning artifacts, preserving role separation across agents, and preparing work for safe parallel implementation.

# Success Criteria

- A user can submit a project idea and receive `DISCOVERY_CHECKLIST.md`, `SPEC.md`, and `TASK_GRAPH.md` in the required order.
- Each artifact is persisted and tied to a run record that can be inspected later.
- The generated artifacts follow deterministic section structures suitable for downstream agents.
- The orchestrator enforces the defined artifact sequence and records run status.
- The MVP can be executed locally by a single operator without manual file editing between stages.

# MVP Scope

- Accept a project idea as input for a new run.
- Generate a discovery checklist artifact.
- Support capture of clarification inputs before specification generation.
- Generate a specification artifact from the clarified run context.
- Generate a task graph artifact from the specification.
- Persist artifacts and run metadata for later inspection.
- Provide a Python orchestration flow that enforces stage order.
- Expose a local operator interface for starting a run and retrieving generated artifacts.

# Out of Scope

- Mobile-friendly chat UI
- Multi-user collaboration features
- Remote VPS worker execution
- Parallel implementation task execution
- Integration-agent automation over completed task outputs
- Production-grade deployment automation
- Advanced observability beyond basic run and error records

# Core User Flows

Operator starts a new run with a project idea.

System creates `DISCOVERY_CHECKLIST.md` and stores it with run metadata.

Operator reviews the discovery output and provides any needed clarifications.

System generates `SPEC.md` from the run context and stores it.

System generates `TASK_GRAPH.md` from the specification and stores it.

Operator reviews the persisted artifacts and decides whether to continue into implementation tasks.

Operator can inspect a previous run and retrieve its generated artifacts.

# Interfaces

- Local CLI for starting runs, supplying clarification data, and retrieving artifacts
- Internal Python orchestration API used by the CLI

External integrations:

- LLM provider API for agent generation steps
- Local filesystem storage for artifact persistence in the MVP

# Core Entities

- Run
- Artifact
- Agent stage
- Clarification response
- Task definition
- Validation record

# System Constraints

- The project is Python-dominant.
- LangGraph is used as the workflow orchestration framework for the MVP.
- Required artifacts must preserve the mandated order and filenames.
- Agent responsibilities must remain separated by role.
- The system must favor deterministic artifacts and auditable execution over speculative automation.

# Security Model

- The MVP assumes a single trusted local operator.
- No end-user authentication is required for the initial CLI-only interface.
- Access to artifacts and run data is limited to the local execution environment.
- External provider credentials must be loaded from configuration rather than hard-coded.

# Deployment Target

- Local development environment for the MVP
- Structured so it can later be packaged for containerized or VPS-hosted deployment

# Non-Functional Requirements

- Artifact generation must be repeatable with a deterministic document structure.
- Run state and artifacts must remain inspectable after execution completes.
- The orchestrator must fail explicitly when a required stage cannot be completed.
- The codebase must preserve clear boundaries between orchestration, agent logic, storage, and interfaces.

# Deliverables

- Python package for the orchestration core
- LangGraph-based workflow for discovery, specification, and planning stages
- Agent modules for discovery, specification, and planner roles
- Artifact persistence layer
- CLI entrypoint for local operation
- Basic validation coverage for the end-to-end artifact pipeline

# Assumptions

- The first implementation target is Phase 1 from the repository guidance: artifact pipeline before execution runtime, VPS workers, or chat UI.
- The MVP is operated by a single developer or internal team member through a local CLI.
- Filesystem-backed persistence is sufficient for the first version.
- One LLM provider integration is enough for the initial artifact-generation workflow.
