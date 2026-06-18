---
id: create-robinhood-readonly-alternative
type: transition
episode: investigate-robinhood-mcp
operation: create
target_type: alternative
target_id: robinhood-mcp-readonly-source
---

# Create Robinhood Read-Only Alternative

## Rationale

Using only Robinhood's MCP read tools is a low-risk option that respects AIfund's
safety boundaries.

## Before

The Robinhood question had no recorded options.

## After

AIfund has an alternative to use Robinhood MCP as a read-only market-data and
portfolio-context source, placing no orders.

## Evidence

- `.memory/alternatives/robinhood-mcp-readonly-source.md`
- `tradingagents/execution/schemas.py` (`QuoteSnapshot`)
