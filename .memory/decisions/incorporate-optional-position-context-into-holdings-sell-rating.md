---
id: incorporate-optional-position-context-into-holdings-sell-rating
type: decision
status: accepted
created: 2026-06-30
accepted: 2026-06-30
---

# Incorporate Optional Position Context Into Holdings Sell-rating

The holdings sell-rating should accept optional per-holding position context and
use it when deciding whether a holding deserves sell or trim attention.

The first supported position fields are:

- `weight`
- `cost_basis`
- `market_price`

Position context adds concerns for concentration and unrealized loss while
preserving the existing absolute signal and relative-weakness logic.

## Rationale

A real portfolio is not only a list of tickers. Position size and unrealized
gain or loss affect what should be reviewed for selling.

## Evidence

- `tradingagents/discovery/rating.py`
- `scripts/rate_holdings.py`
- `tests/test_rating.py`
