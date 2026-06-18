---
id: create-robinhood-live-broker-alternative
type: transition
episode: investigate-robinhood-mcp
operation: create
target_type: alternative
target_id: robinhood-mcp-live-broker
---

# Create Robinhood Live Broker Alternative

## Rationale

A guarded live broker adapter is the other realistic way to use Robinhood MCP,
and its tradeoffs need to be recorded.

## Before

The Robinhood question had only the read-only alternative.

## After

AIfund has an alternative to add an opt-in `RobinhoodBroker` live execution
adapter, gated behind the risk policy and explicit human approval, never the
default.

## Evidence

- `.memory/alternatives/robinhood-mcp-live-broker.md`
- `tradingagents/execution/broker/alpaca.py` (adapter interface)
