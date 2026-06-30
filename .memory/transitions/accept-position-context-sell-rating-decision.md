---
id: accept-position-context-sell-rating-decision
type: transition
episode: add-position-context-to-sell-rating
operation: accept
target_type: decision
target_id: incorporate-optional-position-context-into-holdings-sell-rating
created: 2026-06-30
---

# Accept Position Context Sell Rating Decision

Accepted the decision to incorporate optional position context into holdings
sell-rating.

## Rationale

Position weight and unrealized gain or loss are material to sell review and make
the portfolio rating more actionable.

## Evidence

- `.memory/decisions/incorporate-optional-position-context-into-holdings-sell-rating.md`
- `tradingagents/discovery/rating.py`
- `tests/test_rating.py`
