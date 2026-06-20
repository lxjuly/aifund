---
id: create-sell-rating-decision
type: transition
episode: build-holdings-sell-rating
operation: create
target_type: decision
target_id: holdings-sell-rating
---

# Create Sell Rating Decision

## Rationale

The rating approach combining absolute signals with relative weakness needed a
recorded decision.

## Before

AIfund had only the buy-side multi-factor screen.

## After

AIfund records the decision to rate holdings with absolute sell signals plus
relative weakness, yielding sell, trim, or hold verdicts.

## Evidence

- `.memory/decisions/holdings-sell-rating.md`
- `tradingagents/discovery/rating.py`
