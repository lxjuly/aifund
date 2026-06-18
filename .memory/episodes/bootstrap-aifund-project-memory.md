---
id: bootstrap-aifund-project-memory
type: episode
status: completed
---

# Bootstrap AIfund Project Memory

This Episode records standing up AIfund's `.memory/` directory and importing
AIfund's existing organizational state into it.

## Context

AIfund had accumulated steering docs, decisions, and a backlog across prior
sessions, but no shared memory layer. The request was to manage AIfund with the
Chronelle ontology, with each project owning its memory in a `.memory/`
directory inside its own repository.

## Participants

- project steward
- Claude

## Inputs

- AIfund `AGENTS.md`, `WORKFLOW.md`, `SESSION_HANDOFF.md`
- AIfund `docs/task-specs/backlog.md`
- AIfund execution layer (`tradingagents/execution/`)

## Outputs

- AIfund `.memory/` directory
- project goal, constraints, and assumptions
- decisions already landed, recorded as Chronelle primitives
- current AIfund plan as a task-planning projection

## Transitions

- create-reliable-paper-trading-goal
- create-execution-safety-constraints
- record-thunder-ollama-decision
- record-moomoo-default-broker-decision
- record-execution-separation-decision
- record-cloudflare-pages-decision
