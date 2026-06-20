---
id: build-holdings-sell-rating
type: episode
status: completed
---

# Build Holdings Sell Rating

This Episode records adding the sell-side rating to the screener.

## Context

The steward holds a portfolio and wanted to rate each stock to find what to sell.
The buy screen only ranks a universe, so a sell-oriented rating with absolute
signals was added.

## Participants

- project steward
- Claude

## Inputs

- `portfolio-sell-review` goal
- the existing screener scoring and yfinance fetch

## Outputs

- a trend factor (percent above the 200-day average) added to the data fetch
- `tradingagents/discovery/rating.py` with `rate_holdings` and verdicts
- `scripts/rate_holdings.py` to rate a portfolio
- a harness for the verdict logic; suite green at 28 tests
- a live run rated a 7-name portfolio: DIS sell; PFE and INTC trim; rest hold

## Transitions

- create-sell-review-goal
- create-sell-rating-decision
- create-rating-module
