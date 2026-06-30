---
id: create-unrealized-return-price-assumption
type: transition
episode: add-position-context-to-sell-rating
operation: create
target_type: assumption
target_id: unrealized-return-requires-supplied-market-price-when-factor-rows-do-not-include-latest-price
created: 2026-06-30
---

# Create Unrealized Return Price Assumption

Created the assumption that unrealized return requires supplied market price
unless factor rows include latest price.

## Rationale

The position-context task intentionally avoided expanding factor fetching and
kept market price as optional caller-supplied context.
