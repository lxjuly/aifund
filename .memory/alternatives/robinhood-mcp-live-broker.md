---
id: robinhood-mcp-live-broker
type: alternative
status: proposed
question: adopt-robinhood-mcp
---

# Robinhood MCP As An Opt-In Live Broker

Add a `RobinhoodBroker` execution adapter that maps AIfund's broker interface
(`get_account`, `get_positions`, `submit_order`) onto Robinhood MCP order tools.

`review_equity_order` maps onto AIfund's existing dry-run policy evaluation, so
orders can be previewed before placement. `place_equity_order` performs the live
submission.

Because Robinhood agentic trading is live-only, this crosses
[[execution-safety-boundaries]]. It would be opt-in only, gated behind the hard
risk policy and explicit human approval, and never the default.

It does not replace [[moomoo-simulated-default-broker]]. It is an additional,
guarded live backend.

Open issue: consumption from Python is not a drop-in REST adapter. The OAuth and
MCP transport are designed for an MCP client, so the cleanest path is to let the
agent call the MCP tools directly.
