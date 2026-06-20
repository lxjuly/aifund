---
id: aifund-current-checkpoint
type: checkpoint
status: handed-off
actor: Claude
updated: 2026-06-19
---

# Current Checkpoint

## Focus

Equity discovery ("what to buy") as a funnel: screen a universe to a shortlist,
then deep-research the top names.

## Progress

- Built `tradingagents/discovery/`: a deterministic multi-factor screener
  (momentum, value, quality) over a universe, with a runnable
  `scripts/screen_candidates.py` and a harness. Suite green at 23 tests.
- Ran a live screen over 30 names; top candidates included MA, CAT, AAPL, NVDA.
- Earlier: read-only Robinhood quote source; Anthropic backend configured
  (awaiting `ANTHROPIC_API_KEY`).

## Next Action

Close the funnel: feed the screener's top-N shortlist into the research graph and
rank the buy decisions. This is stage two and needs a model backend, so it waits
on `ANTHROPIC_API_KEY` in `.env.local` (or Thunder + Ollama).

Run discovery any time (no key needed):
`uv run python scripts/screen_candidates.py --top 10 --out shortlist.json`

## Open Loops

- Funnel stage two (research the shortlist) needs a model backend.
- Screener uses a curated 30-name universe and best-effort fundamentals; broaden
  and harden later.
- Robinhood quote source built but not wired into the runner.

## Working Context

- `tradingagents/discovery/screener.py` — pure scoring
- `tradingagents/discovery/yfinance_factors.py` — live data
- `scripts/screen_candidates.py` — runnable screen
- `.env.local` — Anthropic backend config (needs key)

## Promotion Notes

When the funnel is wired end-to-end, record it as an Episode with Transitions and
capture a real research run log for the replay fixture (TA-002).
