---
id: investigate-robinhood-mcp
type: episode
status: completed
---

# Investigate Robinhood Agentic Trading MCP

This Episode records investigating whether AIfund can use Robinhood's new
agentic trading MCP.

## Context

Robinhood released an agentic trading MCP server in beta (May 2026). The steward
asked whether AIfund could use it.

## Participants

- project steward
- Claude

## Inputs

- Robinhood agentic trading documentation
- AIfund execution layer and broker adapter interface

## Outputs

- Question on whether to adopt Robinhood MCP
- two alternatives: read-only data source, and opt-in live broker
- finding that Robinhood agentic trading is live-only, conflicting with AIfund's
  paper-default safety boundaries

## Transitions

- create-adopt-robinhood-mcp-question
- create-robinhood-readonly-alternative
- create-robinhood-live-broker-alternative
