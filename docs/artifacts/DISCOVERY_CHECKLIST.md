# DISCOVERY_CHECKLIST.md

# Known Information

- The repository is intended to implement a multi-agent software delivery system.
- The intended workflow is: idea or user prompt -> discovery or checklist -> spec generation -> planning or task decomposition -> parallel implementation -> integration or validation -> final output.
- The system prioritizes accuracy before speed, clarity before cleverness, safe parallelization, contract-first execution, small task units, minimal assumptions, deterministic artifacts, and auditability.
- The required agent roles are Discovery Agent, Spec Agent, Planner Agent, Implementation Agent, and Integration Agent.
- Required artifacts must be produced in this order: `DISCOVERY_CHECKLIST.md` -> `SPEC.md` -> `TASK_GRAPH.md` -> `TASK_IMPLEMENTATION.md` (multiple allowed) -> `INTEGRATION_REPORT.md`.
- Planned future capabilities include a mobile-friendly chat UI, a runtime or orchestrator service, and communication with a remote VPS worker host.
- The orchestrator is expected to manage workflow state, artifact sequencing, dependency scheduling, task assignment, retries, run history, validation tracking, and worker coordination.
- The system must support parallel task execution, resumable runs, failure recovery, artifact persistence, and human approval gates.
- The execution layer is expected to support local workers and VPS workers.
- The user stated that LangGraph was recommended for this project.
- The user stated that this should be a Python-dominant project.

# Missing Critical Information

- The exact MVP boundary for the first deliverable is unknown.
- The primary user or operator for the system is unknown.
- The concrete problem statement for the first usable version is unknown.
- The required MVP interfaces are unknown.
- It is unknown whether LangGraph is a hard requirement or a preferred option.
- The deployment target for the MVP orchestrator and supporting services is unknown.
- The required persistence model for runs, artifacts, task state, and logs is unknown.
- The authentication and authorization model for the UI, API, and workers is unknown.
- The expected execution model for implementation tasks is unknown.
- The validation requirements for declaring a run complete are not concretely defined for the MVP.
- The first-class external integrations are unknown.
- The boundary between autonomous behavior and required human approval is unknown.

# Missing Important Information

- Expected scale for concurrent runs, agents, and workers is unknown.
- The preferred Python version and packaging approach are unknown.
- The preferred API style for orchestration and worker communication is unknown.
- The expected artifact storage location and retention policy are unknown.
- Observability requirements for logs, traces, metrics, and audit history are unknown.
- Retry, timeout, cancellation, and failure-handling expectations are unknown.
- Multi-user or multi-tenant requirements are unknown.
- Compliance or data-handling constraints are unknown.
- Cost controls for model usage and task execution are unknown.
- The desired timeline or milestone sequence across the documented development phases is unknown.

# Questions That MUST Be Answered Before Planning

- What is the MVP for the first implementation phase: artifact generation only, full orchestration of agents, task execution, or the complete end-to-end system?
- Who is the primary user of the system in the MVP: a single developer, an internal team, or multiple authenticated users?
- Which interfaces must exist in the MVP: CLI, API, web UI, mobile-friendly chat UI, or some subset?
- Is LangGraph a required framework for orchestration, or is it currently a recommendation that can be changed?
- What deployment target should be assumed for the MVP: local development only, containerized local deployment, VPS, or cloud infrastructure?
- What data must be persisted in the MVP: artifacts only, workflow state, run history, logs, execution results, or all of these?
- What execution environments must the system support in the MVP: local commands only, sandboxed local workers, remote VPS workers, or both local and remote workers?
- What authentication and authorization are required for the MVP across users, agents, and workers?
- What validation thresholds must be met before a run can be marked complete in the MVP?
- Which external services are in scope for the MVP, such as LLM providers, source control systems, object storage, or queueing systems?

# Questions That SHOULD Be Answered Before Planning

- What Python version should be standardized for the project?
- What database or persistence technologies are preferred, if any?
- What level of observability is expected in early versions?
- What concurrency level should the scheduler be designed to support initially?
- What audit trail retention is expected for artifacts, logs, and approvals?
- Should the MVP support resumable runs across process restarts?
- Should human approval gates be configurable per workflow stage or fixed?
- Are there compliance, privacy, or data residency requirements?
- What is the preferred release order for the documented phases after the MVP is defined?

# Information That Can Safely Be Deferred

- Exact logging and tracing frameworks
- CI/CD tooling choices
- UI design system and visual styling details
- Exact VPS provider choice
- Exact queue technology
- Exact database engine, if persistence requirements are first clarified conceptually
- Test framework choice
- Deployment automation tooling
- Non-essential optimization and performance tuning decisions
