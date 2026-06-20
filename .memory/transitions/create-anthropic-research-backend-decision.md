---
id: create-anthropic-research-backend-decision
type: transition
episode: configure-anthropic-backend
operation: create
target_type: decision
target_id: anthropic-research-backend
---

# Create Anthropic Research Backend Decision

## Rationale

Choosing a hosted model backend affects spend and needed a recorded decision.

## Before

AIfund's only recorded serving path was Thunder + Ollama, which was not reachable
on the current machine.

## After

AIfund records the decision to use the Anthropic API as a hosted research
backend, with a cost-aware deep/quick model split, while Thunder + Ollama remains
the low-cost default.

## Evidence

- `.memory/decisions/anthropic-research-backend.md`
