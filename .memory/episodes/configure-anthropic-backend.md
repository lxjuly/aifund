---
id: configure-anthropic-backend
type: episode
status: completed
---

# Configure Anthropic Backend

This Episode records configuring the Anthropic API as a hosted research backend
so AIfund can run the TradingAgents graph.

## Context

The steward wanted to run a real deep-research pass on equities now. Thunder +
Ollama was not reachable on the current machine, so a hosted backend was needed.
Anthropic was chosen.

## Participants

- project steward
- Claude

## Inputs

- the TradingAgents graph and `llm_clients/anthropic_client.py`
- `execution/config.py` env handling and the model catalog

## Outputs

- decision `anthropic-research-backend`
- `.env.local` configured for provider anthropic with deep `claude-sonnet-4-6`
  and quick `claude-haiku-4-5`, backend URL blanked
- a plan task to run the first Anthropic-backed research pass

## Transitions

- create-anthropic-research-backend-decision
- configure-anthropic-env
