---
id: build-discovery-screener
type: episode
status: completed
---

# Build Discovery Screener

This Episode records building and running the first discovery screen.

## Context

TradingAgents only analyzes a given ticker; it cannot surface candidates. The
steward wanted to try the "what to buy" use case. A quantitative multi-factor
screen was chosen as the runnable-now first stage.

## Participants

- project steward
- Claude

## Inputs

- `equity-discovery` goal
- yfinance data and the existing adapter and harness conventions

## Outputs

- `tradingagents/discovery/` package: pure `score_universe`, a curated default
  universe, and a yfinance factor fetch
- `scripts/screen_candidates.py` runnable screen
- a harness for the scoring logic; suite green at 23 tests
- a live run over a 30-name universe produced a ranked shortlist (top names
  included MA, CAT, AAPL, NVDA)

## Transitions

- create-discovery-goal
- create-discovery-decision
- create-screener-module
