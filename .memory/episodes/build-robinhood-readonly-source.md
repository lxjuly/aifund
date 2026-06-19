---
id: build-robinhood-readonly-source
type: episode
status: completed
---

# Build Robinhood Read-Only Source

This Episode records building the Robinhood read-only data source decided in
[[adopt-robinhood-mcp-readonly]].

## Context

After installing a local `uv` environment, the Python track was unblocked. The
active task was to implement the read-only Robinhood MCP source.

## Participants

- project steward
- Claude

## Inputs

- decision `adopt-robinhood-mcp-readonly`
- `QuoteSnapshot` schema and the existing adapter and harness conventions

## Outputs

- `tradingagents/execution/market_data/` package with `RobinhoodQuoteSource`
- read-only enforcement: only `READ_ONLY_TOOLS` may be called; order tools are
  structurally unreachable
- a unit harness, added to the harness suite; suite green at 17 tests

## Design Notes

- The source takes an injected MCP caller, so it is testable and never bound to a
  live account by construction.
- It maps `get_equity_quotes` onto `QuoteSnapshot` and exposes `is_tradable`.
- It lives in the execution layer because it produces `QuoteSnapshot` for
  pre-trade context; a future research-layer text adapter could come later.

## Transitions

- create-robinhood-quote-source
