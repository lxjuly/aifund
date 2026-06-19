---
id: adopt-robinhood-mcp-readonly
type: decision
status: accepted
resolves: adopt-robinhood-mcp
---

# Adopt Robinhood MCP As A Read-Only Data Source

AIfund adopts Robinhood's agentic-trading MCP as a read-only market-data and
portfolio-context source for TradingAgents.

This resolves [[adopt-robinhood-mcp]] by accepting
[[robinhood-mcp-readonly-source]]. The live-broker path
[[robinhood-mcp-live-broker]] is deferred, not rejected, and remains behind
explicit human approval and account setup.

## Scope

- Use read tools only: `get_equity_quotes`, `get_equity_tradability`, `search`,
  `get_popular_lists`, `get_portfolio`, `get_equity_positions`, watchlists.
- Do not wire any order tool (`place_equity_order` and similar).
- Map quote data onto the existing `QuoteSnapshot` schema.

## Why This Respects The Boundaries

It places no orders and touches no real-money write path, so it stays inside
[[execution-safety-boundaries]]. It does not change the default broker; Moomoo
simulated remains the default execution path per
[[moomoo-simulated-default-broker]].

## Integration Outline

- Robinhood MCP is consumed through an MCP client, not REST keys. The agent can
  attach it with `claude mcp add robinhood-trading`.
- Add an optional Robinhood read-only data source in the research/data layer.
  Default research data stays Yahoo/yfinance; Robinhood is an opt-in quote and
  context source.
- Keep it outside the debate graph, consistent with
  [[execution-outside-debate-graph]].

## Constraints Carried Forward

- US-only, equities-only while Robinhood's MCP is in beta.
- Reads cover the user's own Robinhood accounts; treat account/position data as
  private and never publish it.
