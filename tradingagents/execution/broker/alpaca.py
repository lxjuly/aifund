from __future__ import annotations

import os
from typing import Any, Optional

import requests

from ..schemas import AccountSnapshot, OrderRequest, PositionSnapshot


class AlpacaBroker:
    """Small Alpaca adapter for paper or live cash-equity workflows."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        *,
        paper: bool = True,
        base_url: Optional[str] = None,
        session: Optional[requests.Session] = None,
    ):
        self.api_key = api_key or os.getenv("ALPACA_API_KEY")
        self.secret_key = secret_key or os.getenv("ALPACA_SECRET_KEY")
        self.base_url = base_url or (
            "https://paper-api.alpaca.markets" if paper else "https://api.alpaca.markets"
        )
        self.session = session or requests.Session()

        if not self.api_key or not self.secret_key:
            raise ValueError("ALPACA_API_KEY and ALPACA_SECRET_KEY are required.")

        self.session.headers.update(
            {
                "APCA-API-KEY-ID": self.api_key,
                "APCA-API-SECRET-KEY": self.secret_key,
                "accept": "application/json",
                "content-type": "application/json",
            }
        )

    def get_account(self) -> AccountSnapshot:
        payload = self._request("GET", "/v2/account")
        return AccountSnapshot(
            equity=float(payload["equity"]),
            cash=float(payload["cash"]),
            buying_power=float(payload["buying_power"]),
            portfolio_value=float(payload.get("portfolio_value") or payload["equity"]),
            pattern_day_trader=payload.get("pattern_day_trader"),
        )

    def get_positions(self) -> list[PositionSnapshot]:
        payload = self._request("GET", "/v2/positions")
        return [
            PositionSnapshot(
                symbol=item["symbol"],
                qty=float(item["qty"]),
                market_value=float(item["market_value"]),
                side=item.get("side", "long"),
            )
            for item in payload
        ]

    def submit_order(self, order: OrderRequest) -> dict[str, Any]:
        body = {
            "symbol": order.symbol,
            "side": order.side,
            "type": order.order_type,
            "time_in_force": order.time_in_force,
            "notional": round(order.notional_usd, 2),
        }
        return self._request("POST", "/v2/orders", json=body)

    def _request(self, method: str, path: str, **kwargs) -> Any:
        response = self.session.request(method, f"{self.base_url}{path}", timeout=30, **kwargs)
        response.raise_for_status()
        return response.json()
