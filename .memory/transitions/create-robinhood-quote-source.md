---
id: create-robinhood-quote-source
type: transition
episode: build-robinhood-readonly-source
operation: create
target_type: module
target_id: robinhood-quote-source
---

# Create Robinhood Quote Source

## Rationale

The accepted read-only decision needed a concrete, tested implementation.

## Before

AIfund had the decision to adopt Robinhood MCP read-only but no code.

## After

AIfund has `RobinhoodQuoteSource` in `tradingagents/execution/market_data/`,
read-only by construction, mapping MCP quotes onto `QuoteSnapshot`, covered by a
harness. The full suite passes at 17 tests.

## Evidence

- `tradingagents/execution/market_data/robinhood.py`
- `tests/test_robinhood_quote_source.py`
- `scripts/run_harnesses.py`
