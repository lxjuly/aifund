---
id: create-execution-safety-constraints
type: transition
episode: bootstrap-aifund-project-memory
operation: create
target_type: constraint
target_id: execution-safety-boundaries
---

# Create Execution Safety Constraints

## Rationale

AIfund's safety boundaries needed to be explicit so any agent can see what
requires human approval.

## Before

Safety boundaries lived only in `AGENTS.md` and `WORKFLOW.md`.

## After

AIfund has recorded execution safety boundaries: paper default, no live by
default, execution separate from the debate graph, risk policy before any broker
call.

## Evidence

- `AGENTS.md`
- `WORKFLOW.md`
- `.memory/constraints/execution-safety-boundaries.md`
