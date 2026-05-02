from __future__ import annotations

import re
from typing import Optional

from .schemas import TradeIntent


_RATING_TO_ACTION = {
    "BUY": "buy",
    "OVERWEIGHT": "buy",
    "HOLD": "hold",
    "UNDERWEIGHT": "sell",
    "SELL": "sell",
}


class SignalParser:
    """Deterministically maps TradingAgents prose into a trade intent."""

    _rating_patterns = [
        re.compile(r"\*\*Rating\*\*:\s*(Buy|Overweight|Hold|Underweight|Sell)\b", re.IGNORECASE),
        re.compile(r"Rating:\s*(Buy|Overweight|Hold|Underweight|Sell)\b", re.IGNORECASE),
        re.compile(r"FINAL TRANSACTION PROPOSAL:\s*\*\*(BUY|HOLD|SELL)\*\*", re.IGNORECASE),
        re.compile(r"\b(BUY|OVERWEIGHT|HOLD|UNDERWEIGHT|SELL)\b", re.IGNORECASE),
    ]

    _confidence_patterns = [
        re.compile(r"\bconfidence\b[^0-9]{0,20}([01](?:\.\d+)?)", re.IGNORECASE),
        re.compile(r"\bconfidence\b[^0-9]{0,20}([1-9]\d?)\s*%", re.IGNORECASE),
    ]

    def parse(
        self,
        *,
        symbol: str,
        raw_decision: str,
        time_horizon: Optional[str] = None,
        max_notional_usd: Optional[float] = None,
    ) -> TradeIntent:
        rating = self._extract_rating(raw_decision)
        action = _RATING_TO_ACTION[rating]
        confidence = self._extract_confidence(raw_decision)
        thesis_excerpt = self._extract_thesis_excerpt(raw_decision)

        return TradeIntent(
            symbol=symbol.upper(),
            action=action,
            rating=rating,
            confidence=confidence,
            thesis=raw_decision.strip(),
            thesis_excerpt=thesis_excerpt,
            time_horizon=time_horizon,
            max_notional_usd=max_notional_usd,
            raw_decision=raw_decision,
            metadata={"parser": "deterministic_v1"},
        )

    def _extract_rating(self, text: str) -> str:
        for pattern in self._rating_patterns:
            match = pattern.search(text)
            if match:
                return match.group(1).upper()
        raise ValueError("Could not extract a supported rating from the final trade decision.")

    def _extract_confidence(self, text: str) -> Optional[float]:
        for idx, pattern in enumerate(self._confidence_patterns):
            match = pattern.search(text)
            if not match:
                continue
            value = float(match.group(1))
            if idx == 1:
                value /= 100.0
            return max(0.0, min(1.0, value))
        return None

    def _extract_thesis_excerpt(self, text: str) -> str:
        cleaned = " ".join(text.split())
        if not cleaned:
            return ""
        if len(cleaned) <= 280:
            return cleaned
        return cleaned[:277].rstrip() + "..."
