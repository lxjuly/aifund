from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, Optional, Protocol

from ..schemas import QuoteSnapshot


# Robinhood agentic-trading MCP read tools this source is allowed to call.
# Order tools (place/review/cancel) are deliberately absent so this source can
# never move real money. See the adopt-robinhood-mcp-readonly decision.
READ_ONLY_TOOLS = frozenset(
    {
        "get_equity_quotes",
        "get_equity_tradability",
        "search",
        "get_popular_lists",
        "get_portfolio",
        "get_equity_positions",
    }
)

# An MCP tool caller: invoked with a tool name and arguments, returns the tool's
# parsed result. This abstracts the actual MCP client so the source stays
# testable and is never bound to a live account by construction.
McpCall = Callable[[str, dict], Any]


class RobinhoodReadOnlyError(RuntimeError):
    """Raised on misuse of the read-only Robinhood source."""


class QuoteSource(Protocol):
    def get_quote(self, symbol: str) -> QuoteSnapshot: ...


class RobinhoodQuoteSource:
    """Read-only Robinhood MCP market-data source.

    Maps Robinhood agentic-trading MCP read tools onto ``QuoteSnapshot``. It only
    ever calls tools in ``READ_ONLY_TOOLS``; any attempt to call an order tool
    raises. It is an optional quote and context source and does not replace the
    default research data source.
    """

    def __init__(self, mcp_call: Optional[McpCall] = None):
        self._mcp_call = mcp_call

    @property
    def configured(self) -> bool:
        return self._mcp_call is not None

    def _call(self, tool: str, args: dict) -> Any:
        if tool not in READ_ONLY_TOOLS:
            raise RobinhoodReadOnlyError(
                f"{tool!r} is not a read-only tool; this source only reads."
            )
        if self._mcp_call is None:
            raise RobinhoodReadOnlyError(
                "RobinhoodQuoteSource has no MCP caller configured."
            )
        return self._mcp_call(tool, args)

    def get_quote(self, symbol: str) -> QuoteSnapshot:
        payload = self._call("get_equity_quotes", {"symbols": [symbol]})
        record = _match(_records(payload), symbol)
        if record is None:
            raise RobinhoodReadOnlyError(f"No quote returned for {symbol!r}.")
        return _to_quote_snapshot(symbol, record)

    def is_tradable(self, symbol: str) -> bool:
        payload = self._call("get_equity_tradability", {"symbols": [symbol]})
        record = _match(_records(payload), symbol)
        return _extract_tradable(record)


def _records(payload: Any) -> list[dict]:
    """Normalize a tool payload into a list of record dicts."""
    if isinstance(payload, dict):
        for key in ("quotes", "results", "data", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return [r for r in value if isinstance(r, dict)]
        return [payload]
    if isinstance(payload, list):
        return [r for r in payload if isinstance(r, dict)]
    return []


def _match(records: list[dict], symbol: str) -> Optional[dict]:
    target = symbol.upper()
    for record in records:
        record_symbol = str(
            record.get("symbol") or record.get("ticker") or record.get("instrument") or ""
        ).upper()
        if record_symbol == target:
            return record
    return records[0] if records else None


def _first_present(record: dict, keys: tuple[str, ...]) -> Any:
    for key in keys:
        if record.get(key) is not None:
            return record[key]
    return None


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _spread_pct(bid: Optional[float], ask: Optional[float]) -> Optional[float]:
    if bid is None or ask is None:
        return None
    mid = (bid + ask) / 2
    if mid <= 0:
        return None
    return abs(ask - bid) / mid


def _parse_time(value: Any) -> Optional[datetime]:
    if not isinstance(value, str) or not value:
        return None
    text = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _to_quote_snapshot(symbol: str, record: dict) -> QuoteSnapshot:
    last = _to_float(
        _first_present(record, ("last_trade_price", "last_price", "price", "mark_price"))
    )
    bid = _to_float(_first_present(record, ("bid_price", "bid")))
    ask = _to_float(_first_present(record, ("ask_price", "ask")))
    if last is None and bid is not None and ask is not None:
        last = (bid + ask) / 2
    if last is None:
        raise RobinhoodReadOnlyError(f"Quote for {symbol!r} has no usable price.")
    return QuoteSnapshot(
        symbol=symbol.upper(),
        last_price=last,
        bid_price=bid,
        ask_price=ask,
        spread_pct=_spread_pct(bid, ask),
        as_of=_parse_time(
            record.get("updated_at") or record.get("as_of") or record.get("timestamp")
        ),
    )


def _extract_tradable(record: Optional[dict]) -> bool:
    if not record:
        return False
    for key in ("tradable", "is_tradable", "tradeable"):
        if key in record:
            return bool(record[key])
    state = str(record.get("tradability") or record.get("state") or "").lower()
    return state in {"tradable", "active"}
