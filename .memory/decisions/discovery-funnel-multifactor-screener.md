---
id: discovery-funnel-multifactor-screener
type: decision
status: accepted
---

# Discovery Funnel With A Multi-Factor Screener

AIfund implements [[equity-discovery]] as a funnel: a cheap, broad quantitative
screen over a universe shortlists candidates, then the expensive per-ticker
debate graph researches the top names.

The first screen is a deterministic multi-factor blend: momentum (recent return),
value (trailing P/E, lower is better), and quality (return on equity), combined
as weighted cross-sectional z-scores.

## Design

- Scoring is pure and testable (`tradingagents/discovery/screener.py`); data
  fetch is separate (`yfinance_factors.py`), mirroring the broker and quote-source
  adapters.
- Data comes from yfinance, so the screen needs network but no API key and runs
  locally now.
- Missing factors are skipped and weights renormalized, so partial data still
  ranks.

## Why A Funnel

It is cost-smart: a broad cheap screen narrows the universe before any
LLM-expensive research, consistent with the low-cost goal
[[reliable-low-cost-paper-trading]].

## Next

Wire the shortlist into the research graph (funnel stage two), broaden the
universe beyond the curated default, and optionally add an LLM idea-generation
variant once a model backend is available.
