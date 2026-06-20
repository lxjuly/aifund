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


def _trend_from_closes(closes, symbol: str, window: int = 200) -> Optional[float]:
    """Percent the latest close sits above (positive) or below (negative) its
    moving average. A negative value means the stock is below its trend."""
    try:
        series = closes[symbol].dropna()
    except Exception:
        return None
    if len(series) < window:
        return None
    moving_average = float(series.iloc[-window:].mean())
    last = float(series.iloc[-1])
    if moving_average <= 0:
        return None
    return last / moving_average - 1.0


def fetch_factor_rows(
    tickers: Sequence[str],
    *,
    lookback_days: int = 126,
    trend_window: int = 200,
    period: str = "1y",
) -> list[dict]:
    """Return factor rows: momentum (return), value (P/E), quality (ROE), and
    trend (percent above the 200-day moving average)."""
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
        trend = _trend_from_closes(closes, symbol, trend_window)
        value: Optional[float] = None
        quality: Optional[float] = None
        try:
            info = yf.Ticker(symbol).info
            value = _safe_float(info.get("trailingPE"))
            quality = _safe_float(info.get("returnOnEquity"))
        except Exception:
            pass
        rows.append(
            {
                "symbol": symbol,
                "momentum": momentum,
                "value": value,
                "quality": quality,
                "trend": trend,
            }
        )
    return rows
