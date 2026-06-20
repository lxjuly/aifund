"""Fetch screener factor rows from yfinance.

Kept separate from the scoring logic so the screener stays testable without a
network. Momentum comes from price history (one batch download); value and
quality come from per-ticker info and are best-effort.
"""

from __future__ import annotations

from typing import Optional, Sequence


def _safe_float(value) -> Optional[float]:
    try:
        if value is None:
            return None
        result = float(value)
        return result
    except (TypeError, ValueError):
        return None


def _momentum_from_closes(closes, symbol: str, lookback_days: int) -> Optional[float]:
    try:
        series = closes[symbol].dropna()
    except Exception:
        return None
    if len(series) <= lookback_days:
        return None
    start = float(series.iloc[-1 - lookback_days])
    end = float(series.iloc[-1])
    if start <= 0:
        return None
    return end / start - 1.0


def fetch_factor_rows(
    tickers: Sequence[str],
    *,
    lookback_days: int = 126,
    period: str = "9mo",
) -> list[dict]:
    """Return factor rows: momentum (return), value (trailing P/E), quality (ROE)."""
    import yfinance as yf

    data = yf.download(
        list(tickers),
        period=period,
        interval="1d",
        auto_adjust=True,
        progress=False,
        group_by="column",
    )
    closes = data["Close"] if "Close" in getattr(data, "columns", []) else data

    rows: list[dict] = []
    for symbol in tickers:
        momentum = _momentum_from_closes(closes, symbol, lookback_days)
        value: Optional[float] = None
        quality: Optional[float] = None
        try:
            info = yf.Ticker(symbol).info
            value = _safe_float(info.get("trailingPE"))
            quality = _safe_float(info.get("returnOnEquity"))
        except Exception:
            pass
        rows.append(
            {"symbol": symbol, "momentum": momentum, "value": value, "quality": quality}
        )
    return rows
