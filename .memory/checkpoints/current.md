---
id: aifund-current-checkpoint
type: checkpoint
status: handed-off
actor: Claude
updated: 2026-06-20
---

# Current Checkpoint

## Focus

End-to-end equity research: discovery screen, then deep multi-agent research on a
top name, on the Anthropic backend.

## Progress

- Built the discovery screener; live screen ranked a 30-name universe.
- Configured the Anthropic backend; operator key in `.env.local`.
- Ran the first real research pass: `exec paper NVDA 2026-06-17` returned BUY,
  policy approved at 100 USD notional, dry run, full log saved. Suite green at 23
  tests.

## Next Action

Capture the NVDA run into replay fixtures (TA-002), now unblocked:
`uv run python scripts/capture_replay_case.py --source-log ~/.tradingagents/logs/NVDA/TradingAgentsStrategy_logs/full_states_log_2026-06-17.json`
then re-run `scripts/run_harnesses.py`.

## Open Loops

- Funnel stage two is only manual so far (we picked a top name by hand); automate
  screen -> research over a shortlist (`wire-discovery-into-research`).
- Robinhood quote source built but not wired into the runner.
- Rotate the Anthropic API key: it was pasted in chat.

## Working Context

- run: `uv run python -m cli.main exec paper <SYMBOL> <DATE>`
- discovery: `uv run python scripts/screen_candidates.py`
- run log: `~/.tradingagents/logs/NVDA/TradingAgentsStrategy_logs/full_states_log_2026-06-17.json`
- `.env.local` holds the Anthropic config and key (gitignored)

## Promotion Notes

The run's durable residue is recorded (episode, transition). After replay capture,
record that work as an Episode with Transitions.
