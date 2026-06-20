---
id: holdings-sell-rating
type: decision
status: accepted
---

# Rate Holdings With Absolute Signals Plus Relative Weakness

AIfund rates a list of holdings to find sells, implementing
[[portfolio-sell-review]] by reusing the multi-factor screener.

## Two Layers

- Relative weakness: the same cross-sectional composite from
  [[discovery-funnel-multifactor-screener]], computed across the holdings.
- Absolute concerns, independent of the peer set: negative 6-month momentum,
  price below its 200-day average, and non-positive return on equity.

## Verdict

- two or more absolute concerns: sell
- one absolute concern, or relatively weak versus the rest: trim
- otherwise: hold

The verdict is a transparent function of the concerns, so reasons are always
explainable and the thresholds are tunable.

## Why Absolute Signals Matter

Relative rank alone is misleading for selling: every list has a bottom name. The
absolute layer fires regardless of rank, so a strong-momentum holding with weak
quality can still be flagged to trim. A live run flagged DIS to sell and PFE and
INTC to trim while leaving the rest on hold.

## Funnel

This mirrors discovery on the sell side: the cheap rating shortlists sell
candidates that the per-ticker research graph can then study, parallel to
[[equity-discovery]].
