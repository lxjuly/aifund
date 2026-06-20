---
id: aifund-current-checkpoint
type: checkpoint
status: handed-off
actor: Claude
updated: 2026-06-19
---

# Current Checkpoint

## Focus

Run a real deep-research pass on equities through the TradingAgents graph, using
the Anthropic API as the model backend.

## Progress

- Installed a local `uv` env; harness suite green at 17 tests.
- Built the read-only `RobinhoodQuoteSource`.
- Chose Anthropic as a hosted research backend and configured `.env.local`
  (provider anthropic, deep `claude-sonnet-4-6`, quick `claude-haiku-4-5`,
  backend URL blanked).

## Next Action

Operator supplies `ANTHROPIC_API_KEY` in `.env.local` (billed to their account),
then run:

`uv run python -m cli.main exec paper <SYMBOL> <DATE>`

This runs the full debate graph and the execution dry run. Pick a symbol and date
(for example NVDA and a recent trading date).

## Open Loops

- Blocked only on `ANTHROPIC_API_KEY`; everything else is wired.
- Thunder + Ollama remains the low-cost default but is not reachable here.
- Robinhood quote source is built but not yet wired into the runner.
- Capture first replay fixture (TA-002) still needs a real run log; this Anthropic
  run can produce one.

## Working Context

- `.env.local` (gitignored) — backend config
- `tradingagents/graph/setup.py` — the debate graph
- `tradingagents/llm_clients/anthropic_client.py` — Anthropic client
- run: `uv run python -m cli.main exec paper <SYMBOL> <DATE>`

## Promotion Notes

After the run, capture the result as an Episode with Transitions, and consider
using the run log for the replay fixture (TA-002).
