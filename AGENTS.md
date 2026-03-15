# AGENTS.md

## Purpose

This repository implements a **multi-agent software delivery system** that turns a rough project idea into clarified requirements, a concrete spec, a parallel task graph, executable implementation tasks, and a validated integrated result.

The system is designed for:

- high parallelization
- strict task boundaries
- predictable artifact handoff
- minimal agent overlap
- human-in-the-loop clarification where needed

Planned future capabilities:

- a **mobile-friendly chat UI**
- a **runtime/orchestrator service**
- communication with a **remote VPS worker host** capable of executing builds/tests and running agents

This file defines how agents behave, what artifacts they produce, and how work flows through the system.

---

# System Goal

Build an agent pipeline that reliably executes this sequence:

```
Idea / user prompt
→ Discovery / Checklist
→ Spec generation
→ Planning / task decomposition
→ Parallel implementation
→ Integration / validation
→ Final output
```

The system prioritizes:

1. accuracy before speed
2. clarity before cleverness
3. parallelization where safe
4. contract-first execution
5. small task units
6. minimal assumptions
7. deterministic artifacts
8. auditability

---

# Core Principle

Every agent has **one role only**.

Agents must not blur responsibilities.

| Agent | Responsibility |
|------|----------------|
| Discovery Agent | find known and unknown requirements |
| Spec Agent | produce a structured project specification |
| Planner Agent | decompose work into parallel tasks |
| Implementation Agents | implement exactly one task |
| Integration Agent | combine results and validate |

Agents must **not perform the responsibilities of another agent**.

---

# Required Agent Roles

## Discovery / Checklist Agent

### Responsibility

Extract explicit facts from input and identify what is missing.

### Must do

- list confirmed facts
- list missing critical information
- list missing important information
- list required clarification questions
- identify what can safely be deferred

### Must not do

- assume missing facts
- recommend architecture
- choose technologies
- generate implementation plans

### Output

```
DISCOVERY_CHECKLIST.md
```

---

## Spec Agent

### Responsibility

Turn clarified requirements into a minimal planning specification.

### Must define

- problem definition
- success criteria
- MVP scope
- out-of-scope items
- core user flows
- interfaces
- core entities
- system constraints
- security model
- deployment target
- non-functional requirements
- deliverables

### Must not do

- design architecture
- write code
- introduce speculative features

### Output

```
SPEC.md
```

---

## Planner / Task Decomposition Agent

### Responsibility

Convert the specification into a **parallelizable task graph**.

### Must do

- maximize safe parallelization
- define contracts early
- minimize real dependencies
- split work into small tasks
- define execution groups
- identify the critical path

### Must not do

- write production code
- serialize work unnecessarily
- create oversized tasks

### Output

```
TASK_GRAPH.md
```

---

## Implementation Agent

### Responsibility

Execute **exactly one task**.

### Must do

- stay within scope
- respect defined contracts
- modify only necessary files
- produce minimal production-ready code

### Must not do

- redesign architecture
- expand scope
- refactor unrelated code
- introduce unnecessary frameworks

### Output

```
TASK_IMPLEMENTATION.md
```

---

## Integration / Validation Agent

### Responsibility

Integrate completed tasks and validate system behavior.

### Must do

- reconcile interface mismatches
- prefer adapters over rewrites
- verify integration through real validation
- list unresolved issues explicitly

### Must not do

- redesign architecture
- expand scope
- perform unrelated refactors

### Output

```
INTEGRATION_REPORT.md
```

---

# Artifact Chain

Artifacts must be produced in this order:

```
DISCOVERY_CHECKLIST.md
→ SPEC.md
→ TASK_GRAPH.md
→ TASK_IMPLEMENTATION.md (multiple)
→ INTEGRATION_REPORT.md
```

Optional artifacts:

```
ARCHITECTURE.md
CONTRACTS.md
API_SPEC.md
RUNBOOK.md
```

Optional artifacts must **not replace required artifacts**.

---

# Repository Structure

Suggested structure:

```
/docs
  /artifacts
  /contracts
  /architecture

/agent-system
  /agents
  /orchestrator
  /schemas
  /prompts

/apps
  /api
  /web
  /chatui

/workers
  /execution-runner
  /sandbox-runner
  /vps-bridge
```

This separation must remain clear.

---

# Golden Rules

1. Preserve role boundaries.
2. Be deterministic.
3. Prefer contracts over coordination.
4. Minimize task overlap.
5. Make uncertainty explicit.
6. Prefer minimal correct work.
7. Never silently expand scope.
8. Separate planning from implementation.
9. Validation claims must be real.
10. Optimize for auditability.

---

# Parallelization Rules

The system must support **aggressive safe parallelization**.

Preferred workflow:

```
contract definition
→ parallel component work
→ integration
→ hardening
```

Avoid:

```
giant sequential implementation tasks
```

Planner agents should split tasks by:

- bounded context
- API surface
- UI surface
- entity domain
- infrastructure
- testing
- integration boundaries

---

# Dependency Rules

Dependencies must be classified as:

| Type | Meaning |
|-----|--------|
| None | task can start immediately |
| Soft | benefits from another task but can proceed |
| Hard | must wait for another task |

Hard dependencies should be minimized.

Contracts should be used to convert **hard dependencies → soft dependencies**.

---

# Contract-First Development

Contracts unlock parallel work.

Examples:

- API schemas
- request/response types
- DB entity definitions
- DTOs
- route definitions
- event payloads
- permission models

Contracts must be defined **before parallel implementation begins**.

---

# Human-in-the-loop Operation

The system supports two modes.

## Interactive Mode

Human answers discovery questions.

```
Discovery → Questions → Human answers → Spec
```

## Autonomous Mode

Allowed only if assumptions are explicitly permitted.

All assumptions must be documented.

---

# Integration Rules

Integration agent must:

- preserve architecture
- prefer adapters
- minimize changes
- verify real system behavior

Conflict resolution priority:

1. SPEC.md
2. planning artifacts
3. explicit contracts
4. shared schemas
5. worker implementations

---

# Validation Rules

The system must clearly distinguish:

- implemented
- integrated
- validated
- assumed

Valid validation methods:

- build success
- tests
- startup verification
- endpoint checks
- integration tests
- runtime verification

Invalid validation:

- “looks correct”
- “should work”

---

# Orchestrator Responsibilities

The orchestrator manages:

- workflow state
- artifact sequencing
- dependency scheduling
- task assignment
- retries
- run history
- validation tracking
- worker coordination

It must support:

- parallel task execution
- resumable runs
- failure recovery
- artifact persistence
- human approval gates

---

# VPS Worker Communication

The system must support **remote execution nodes**.

A VPS worker must be able to:

- receive tasks
- pull or receive workspace snapshots
- run builds/tests/commands
- stream logs
- return structured results
- support cancellation/timeouts
- report environment metadata

Recommended architecture:

```
Chat/UI
→ Orchestrator API
→ Task Queue
→ Local Workers / VPS Workers
→ Results + Logs
```

VPS communication must be treated as a **dedicated subsystem**, not a helper script.

---

# Mobile-Friendly Chat UI

The chat UI is a **client of the orchestration API**, not the orchestrator itself.

Capabilities:

- view run status
- view task graph
- answer discovery questions
- approve decisions
- view artifacts
- view logs
- retry tasks
- cancel runs

The UI must remain **decoupled from agent logic**.

---

# System Components

The platform consists of four logical systems:

## 1. Orchestration Core

Workflow engine and state management.

## 2. Agent Runtime

LLM invocation and structured artifact generation.

## 3. Execution Layer

Local/VPS task execution and sandboxing.

## 4. User Interface

Chat UI and run visibility.

---

# Recommended Development Phases

## Phase 1 — Artifact Pipeline

Implement:

- discovery agent
- spec agent
- planner agent
- artifact storage
- basic orchestrator

Goal: produce artifacts reliably.

---

## Phase 2 — Parallel Task Execution

Implement:

- task scheduler
- implementer agents
- integration agent

Goal: execute full agent pipeline.

---

## Phase 3 — Execution Runtime

Implement:

- command runner
- local workspace execution
- structured execution results

Goal: run builds/tests automatically.

---

## Phase 4 — VPS Worker Bridge

Implement:

- worker registration
- remote task dispatch
- log streaming
- artifact return

Goal: distributed execution.

---

## Phase 5 — Mobile Chat UI

Implement:

- responsive chat interface
- artifact viewer
- run dashboard
- log streaming

Goal: mobile-friendly control surface.

---

# Definition of Done

A run is complete when:

- discovery questions are resolved
- spec is complete
- task graph is produced
- tasks are implemented
- integration is performed
- validation results are recorded
- unresolved issues are documented
- artifacts are persisted
- the system is inspectable

---

# Final Instruction

Agents must:

- perform their role only
- preserve system boundaries
- prefer contracts
- prefer small tasks
- enable parallel work
- minimize changes
- perform real validation
- make uncertainty explicit
- maintain deterministic artifacts
