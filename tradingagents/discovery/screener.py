"""Multi-factor candidate screening.

This is the discovery stage that answers "what to look at?" rather than
"should I buy X?". It ranks a universe by a blend of factors so a cheap, broad
screen can shortlist names for the expensive per-ticker debate graph.

The scoring is pure and deterministic: it takes already-fetched factor rows and
produces a ranking. Data fetching lives separately so this logic stays testable
without a network.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from statistics import mean, pstdev
from typing import Optional, Sequence


@dataclass(frozen=True)
class Factor:
    """One ranking factor and how it is interpreted."""

    key: str
    weight: float
    higher_is_better: bool


# Momentum: recent return, higher is better.
# Value: trailing P/E, lower is better.
# Quality: return on equity, higher is better.
DEFAULT_FACTORS: tuple[Factor, ...] = (
    Factor("momentum", 0.40, True),
    Factor("value", 0.30, False),
    Factor("quality", 0.30, True),
)


@dataclass
class ScoredCandidate:
    symbol: str
    composite: Optional[float]
    coverage: int
    factor_z: dict = field(default_factory=dict)
    raw: dict = field(default_factory=dict)


def _present(value) -> bool:
    return value is not None and not (isinstance(value, float) and math.isnan(value))


def score_universe(
    rows: Sequence[dict],
    factors: Sequence[Factor] = DEFAULT_FACTORS,
) -> list[ScoredCandidate]:
    """Rank candidates by a weighted blend of cross-sectional factor z-scores.

    Each factor is standardized across the universe, flipped when lower is
    better, then combined with its weight. A name is scored on whatever factors
    it has; missing factors are skipped and the remaining weights renormalized.
    Names with no usable factor sort last.
    """
    # Cross-sectional mean/std per factor over present values only.
    stats: dict[str, Optional[tuple[float, float]]] = {}
    for factor in factors:
        values = [row.get(factor.key) for row in rows]
        present = [v for v in values if _present(v)]
        if len(present) >= 2:
            spread = pstdev(present)
            stats[factor.key] = (mean(present), spread) if spread > 0 else None
        else:
            stats[factor.key] = None

    scored: list[ScoredCandidate] = []
    for row in rows:
        factor_z: dict[str, float] = {}
        weighted_sum = 0.0
        weight_total = 0.0
        for factor in factors:
            stat = stats.get(factor.key)
            value = row.get(factor.key)
            if stat is None or not _present(value):
                continue
            mu, sd = stat
            z = (value - mu) / sd
            if not factor.higher_is_better:
                z = -z
            factor_z[factor.key] = z
            weighted_sum += factor.weight * z
            weight_total += factor.weight

        composite = weighted_sum / weight_total if weight_total > 0 else None
        scored.append(
            ScoredCandidate(
                symbol=row["symbol"],
                composite=composite,
                coverage=len(factor_z),
                factor_z=factor_z,
                raw={factor.key: row.get(factor.key) for factor in factors},
            )
        )

    scored.sort(
        key=lambda c: (c.composite is not None, c.composite if c.composite is not None else 0.0),
        reverse=True,
    )
    return scored
