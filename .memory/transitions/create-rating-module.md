---
id: create-rating-module
type: transition
episode: build-holdings-sell-rating
operation: create
target_type: module
target_id: holdings-rating
---

# Create Rating Module

## Rationale

The sell-rating decision needed a tested, runnable implementation.

## Before

The discovery package only had the buy screen.

## After

The discovery package has `rating.py` with `rate_holdings`, a trend factor in the
yfinance fetch, a runnable `scripts/rate_holdings.py`, and a harness. The suite
passes at 28 tests and a live run produced sell, trim, and hold verdicts.

## Evidence

- `tradingagents/discovery/rating.py`
- `tradingagents/discovery/yfinance_factors.py`
- `scripts/rate_holdings.py`
- `tests/test_rating.py`
