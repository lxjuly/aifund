from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Literal, Optional


TradeAction = Literal["buy", "sell", "hold"]
OrderSide = Literal["buy", "sell"]
TimeInForce = Literal["day", "gtc"]


@dataclass
class TradeIntent:
    symbol: str
    action: TradeAction
    rating: str
    confidence: Optional[float]
    thesis: str
    thesis_excerpt: str
    time_horizon: Optional[str] = None
    max_notional_usd: Optional[float] = None
    raw_decision: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AccountSnapshot:
    equity: float
    cash: float
    buying_power: float
    portfolio_value: Optional[float] = None
    pattern_day_trader: Optional[bool] = None


@dataclass
class PositionSnapshot:
    symbol: str
    qty: float
    market_value: float
    side: Literal["long", "short"] = "long"


@dataclass
class QuoteSnapshot:
    symbol: str
    last_price: float
    bid_price: Optional[float] = None
    ask_price: Optional[float] = None
    spread_pct: Optional[float] = None
    as_of: Optional[datetime] = None


@dataclass
class ExecutionPolicyDecision:
    approved: bool
    reasons: list[str]
    normalized_action: TradeAction
    suggested_notional_usd: Optional[float] = None


@dataclass
class OrderRequest:
    symbol: str
    side: OrderSide
    notional_usd: float
    time_in_force: TimeInForce = "day"
    order_type: Literal["market"] = "market"
