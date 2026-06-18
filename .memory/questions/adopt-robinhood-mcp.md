---
id: adopt-robinhood-mcp
type: question
status: open
---

# Should AIfund Adopt Robinhood's Agentic Trading MCP?

Robinhood released an agentic trading MCP server (beta, May 2026) at
`https://agent.robinhood.com/mcp/trading`.

It exposes read tools (accounts, portfolio, positions, quotes, tradability,
search, watchlists) and order tools (`review_equity_order`, `place_equity_order`,
`cancel_equity_order`). Auth is interactive OAuth approval inside the Robinhood
app, consumed by an MCP client rather than REST API keys.

The open question is whether and how AIfund should use it.

Key tension: Robinhood agentic trading is live-only. There is no paper or
sandbox mode. This conflicts with [[execution-safety-boundaries]], which make
paper and simulated trading the default and forbid live trading by default.

Other constraints: US-only, equities-only in beta, desktop onboarding, max 10
self-directed accounts, requires a real-money dedicated account.

Resolving this question requires choosing among the recorded alternatives and,
for any live path, explicit human approval plus account setup.
