---
id: run-nvda-research-pass
type: episode
status: completed
---

# Run NVDA Research Pass

This Episode records the first real TradingAgents research run on the Anthropic
backend.

## Context

After configuring the Anthropic backend and the operator supplying a key, the
goal was to run a real deep-research pass. NVDA was chosen as a top name from the
discovery screen, demonstrating the discovery-to-research funnel for one ticker.

## Participants

- project steward
- Claude

## Inputs

- decision `anthropic-research-backend`; `.env.local` with the operator key
- command `uv run python -m cli.main exec paper NVDA 2026-06-17`
- deep `claude-sonnet-4-6`, quick `claude-haiku-4-5`, depth 1

## Outputs

- final rating: BUY
- execution policy: approved, normalized action buy, suggested notional 100 USD
- broker order: none (dry run; no order submitted)
- full run log at
  `~/.tradingagents/logs/NVDA/TradingAgentsStrategy_logs/full_states_log_2026-06-17.json`

## Significance

The whole pipeline works on Anthropic: debate graph, signal parsing, and dry-run
policy. The run log unblocks replay capture (backlog TA-002).

## Transitions

- record-nvda-research-run
