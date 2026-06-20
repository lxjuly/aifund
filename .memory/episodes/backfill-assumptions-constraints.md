---
id: backfill-assumptions-constraints
type: episode
status: completed
---

# Backfill Assumptions And Constraints

This Episode records capturing the assumptions and constraints that recent
decisions relied on but had not been written as primitives.

## Context

An audit found that decisions were well captured while assumptions and constraints
were stale since bootstrap. The discovery, sell-rating, Robinhood, and Anthropic
work rested on unrecorded beliefs and boundaries.

## Participants

- project steward
- Claude

## Inputs

- the eight recorded decisions
- the screener, rating, Robinhood source, and backend configuration

## Outputs

- assumptions: factor-signals-informative, yfinance-data-adequate,
  hosted-llm-sufficient, funnel-preserves-candidates
- constraints: robinhood-read-only, decision-support-not-advice,
  hosted-llm-cost-control
- a convention in `AGENTS.md` and `.memory/README.md` to capture assumptions and
  constraints alongside decisions

## Transitions

- backfill-research-assumptions
- backfill-embedded-constraints
- codify-assumption-constraint-convention
