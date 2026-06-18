---
id: record-execution-separation-decision
type: transition
episode: bootstrap-aifund-project-memory
operation: create
target_type: decision
target_id: execution-outside-debate-graph
---

# Record Execution Separation Decision

## Rationale

Keeping execution and risk controls outside the debate graph is a core
architectural commitment that belonged in shared memory.

## Before

The separation was stated in `AGENTS.md` and reflected in code structure only.

## After

AIfund records that execution, broker access, and risk policy stay outside the
TradingAgents debate graph.

## Evidence

- `AGENTS.md`
- `tradingagents/execution/`
- `.memory/decisions/execution-outside-debate-graph.md`
