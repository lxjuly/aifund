---
id: resolve-robinhood-mcp-question
type: episode
status: completed
---

# Resolve Robinhood MCP Question

This Episode records resolving whether AIfund should adopt Robinhood's
agentic-trading MCP.

## Context

The investigation episode had left an open question with two alternatives:
read-only data source, and opt-in live broker. The steward chose to resolve it.
The read-only path was selected because it respects the safety boundaries and
needs no account action, while the live-broker path remains deferred behind
explicit approval.

## Participants

- project steward
- Claude

## Inputs

- question `adopt-robinhood-mcp` and its two alternatives
- `execution-safety-boundaries` constraint

## Outputs

- decision to adopt Robinhood MCP read-only
- `robinhood-mcp-readonly-source` accepted; `robinhood-mcp-live-broker` deferred
- `adopt-robinhood-mcp` question resolved

## Transitions

- accept-robinhood-readonly-alternative
- create-robinhood-readonly-decision
- resolve-adopt-robinhood-mcp-question
