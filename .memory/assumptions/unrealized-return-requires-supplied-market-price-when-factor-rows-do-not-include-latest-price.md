---
id: unrealized-return-requires-supplied-market-price-when-factor-rows-do-not-include-latest-price
type: assumption
status: active
created: 2026-06-30
---

# Unrealized Return Requires Supplied Market Price When Factor Rows Do Not Include Latest Price

AIfund currently assumes unrealized return can only be computed when position
context includes both `cost_basis` and `market_price`.

The existing factor rows do not include latest market price, and this task kept
the sell-rating change local to scoring and CLI behavior rather than expanding
the yfinance dataflow.

If a future dataflow adds latest price to factor rows, this assumption should be
revisited.
