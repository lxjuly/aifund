---
id: robinhood-mcp-readonly-source
type: alternative
status: accepted
question: adopt-robinhood-mcp
---

# Robinhood MCP As A Read-Only Data Source

Use only Robinhood's MCP read tools as a market-data and portfolio-context
source for TradingAgents.

Tools used: `get_equity_quotes`, `get_equity_tradability`, `search`,
`get_popular_lists`, `get_portfolio`, `get_equity_positions`, watchlists.

The existing `QuoteSnapshot` schema already fits quote data.

This places no real-money orders, so it respects
[[execution-safety-boundaries]]. It is the lowest-risk way to use Robinhood and
does not require resolving the live-trading tension.

It does not replace the simulated broker path. It only adds data and context.
