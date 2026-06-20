---
id: backfill-embedded-constraints
type: transition
episode: backfill-assumptions-constraints
operation: create
target_type: constraint
target_id: embedded-constraints
---

# Backfill Embedded Constraints

## Rationale

Recent decisions embedded boundaries that lived only in code or prose.

## Before

Only execution-safety-boundaries existed.

## After

Three constraints are recorded: Robinhood is read-only, outputs are decision
support not advice, and hosted-LLM cost is controlled.

## Evidence

- `.memory/constraints/robinhood-read-only.md`
- `.memory/constraints/decision-support-not-advice.md`
- `.memory/constraints/hosted-llm-cost-control.md`
