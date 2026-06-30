---
id: add-position-context-to-sell-rating
type: episode
status: completed
created: 2026-06-30
---

# Add Position Context To Sell Rating

This Episode records adding optional position context to the holdings sell-rating
while dogfooding Chronelle's local HTTP agent service.

## Context

The AIfund plan had an active task to make sell-rating sharper by incorporating
position size and cost basis. Chronelle supplied the AIfund context for the
session and later proposed memory updates from the session summary.

## Participants

- project steward
- Codex
- Chronelle local agent service

## Inputs

- goal: portfolio-sell-review
- decision: holdings-sell-rating
- decision: incorporate-optional-position-context-into-holdings-sell-rating
- experiment: chronelle-local-agent-e2e-dogfood-on-aifund-position-context-task

## Outputs

- `rate_holdings()` accepts optional position context.
- Position context supports `weight`, `cost_basis`, and `market_price`.
- Sell-rating adds concerns for large position weight and unrealized loss.
- `scripts/rate_holdings.py` accepts repeatable `--position` inputs.
- Tests cover position-context concerns.

## Transitions

- accept-position-context-sell-rating-decision
- create-unrealized-return-price-assumption
- record-chronelle-e2e-dogfood-experiment
- complete-sell-rating-position-context-task
