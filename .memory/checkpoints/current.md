---
id: aifund-current-checkpoint
type: checkpoint
status: handed-off
actor: Claude
updated: 2026-06-20
---

# Current Checkpoint

## Focus

Portfolio decisions both ways: discover buys from a universe, and rate held
stocks to find sells.

## Progress

- Buy screen and a live research run on Anthropic (NVDA -> BUY).
- Added the sell-side rating: `rate_holdings` combines relative weakness with
  absolute concerns (negative momentum, below 200-day average, weak ROE) into
  sell / trim / hold verdicts, with a runnable `scripts/rate_holdings.py`.
- Suite green at 28 tests. Live run: DIS sell; PFE and INTC trim; rest hold.

## Next Action

Pick a thread:
- capture the NVDA run into replay fixtures (TA-002), now unblocked;
- deep-research the sell candidates (sell-side funnel, needs model backend);
- add position weight and cost basis to the sell-rating.

Run the sell-rating any time (no key):
`uv run python scripts/rate_holdings.py --portfolio NVDA,AAPL,INTC,PFE,DIS`

## Open Loops

- Both funnels (buy and sell) are only manual into research so far; automate.
- Robinhood quote source built but not wired into the runner.
- Rotate the Anthropic API key: it was pasted in chat.

## Working Context

- buy: `tradingagents/discovery/screener.py`, `scripts/screen_candidates.py`
- sell: `tradingagents/discovery/rating.py`, `scripts/rate_holdings.py`
- shared data: `tradingagents/discovery/yfinance_factors.py`
- research: `uv run python -m cli.main exec paper <SYMBOL> <DATE>`

## Promotion Notes

Durable residue for this session is recorded (goal, decision, episode,
transitions). Record future funnel automation as Episodes with Transitions.
