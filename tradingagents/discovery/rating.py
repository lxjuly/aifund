"""Rate a list of holdings to surface sell candidates.

This is the inverse of the buy screen. Given the stocks you already own, it rates
each one and flags what to consider selling. It combines two views:

- relative weakness: the same multi-factor composite, computed across the holdings
- absolute sell signals: per-stock concerns that do not depend on the peer set
  (declining momentum, price below its long-term trend, weak quality)

A holding's verdict (sell / trim / hold) is a transparent function of how many
concerns it triggers, so the reasons are always explainable and the thresholds
are tunable. The scoring stays pure and testable; data fetching lives elsewhere.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Sequence

from .screener import DEFAULT_FACTORS, Factor, _present, score_universe

# Defaults for the absolute sell signals.
WEAK_QUALITY_ROE = 0.0          # return on equity at or below this is a concern
RELATIVELY_WEAK_Z = -0.5        # composite below this is weak vs the rest


@dataclass
class HoldingRating:
    symbol: str
    verdict: str  # "sell" | "trim" | "hold"
    composite: Optional[float]
    concerns: list[str] = field(default_factory=list)
    raw: dict = field(default_factory=dict)


_VERDICT_ORDER = {"sell": 0, "trim": 1, "hold": 2}


def rate_holdings(
    rows: Sequence[dict],
    factors: Sequence[Factor] = DEFAULT_FACTORS,
    *,
    weak_quality_roe: float = WEAK_QUALITY_ROE,
    relatively_weak_z: float = RELATIVELY_WEAK_Z,
) -> list[HoldingRating]:
    """Rate each holding and sort weakest first (sell, then trim, then hold).

    Absolute concerns: negative momentum, price below its 200-day average, and
    non-positive return on equity. Two or more concerns is a sell; one concern or
    being relatively weak versus the rest is a trim; otherwise hold.
    """
    scored = {c.symbol: c for c in score_universe(rows, factors)}

    ratings: list[HoldingRating] = []
    for row in rows:
        symbol = row["symbol"]
        candidate = scored[symbol]
        concerns: list[str] = []

        momentum = row.get("momentum")
        trend = row.get("trend")
        quality = row.get("quality")

        if _present(momentum) and momentum < 0:
            concerns.append("negative 6-month momentum")
        if _present(trend) and trend < 0:
            concerns.append("price below its 200-day average")
        if _present(quality) and quality <= weak_quality_roe:
            concerns.append("weak return on equity")

        absolute_concerns = len(concerns)
        relatively_weak = (
            candidate.composite is not None and candidate.composite < relatively_weak_z
        )

        if absolute_concerns >= 2:
            verdict = "sell"
        elif absolute_concerns == 1 or relatively_weak:
            verdict = "trim"
        else:
            verdict = "hold"

        if relatively_weak:
            concerns.append("relatively weak vs the rest of the list")

        ratings.append(
            HoldingRating(
                symbol=symbol,
                verdict=verdict,
                composite=candidate.composite,
                concerns=concerns,
                raw=dict(row),
            )
        )

    ratings.sort(
        key=lambda r: (
            _VERDICT_ORDER[r.verdict],
            r.composite if r.composite is not None else float("inf"),
        )
    )
    return ratings
