# MVP Goal

ngrex should allow users to create exactly what they want, very quickly. It should behave like a normal LLM chat, but should follow the flow outlined below.

## Process Flow

User
-> prompts agent

Discovery Agent
-> produces DISCOVERY_CHECKLIST.md

Spec Agent
-> produces SPEC.md

Planner Agent
-> produces TASK_GRAPH.md

Worker Agents (many in parallel)
-> produce TASK_IMPLEMENTATION.md

Integration Agent 
-> merges components and verifies system behavior

## Missing Pieces



