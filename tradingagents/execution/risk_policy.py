from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Optional

from .schemas import (
    AccountSnapshot,
    ExecutionPolicyDecision,
    PositionSnapshot,
    QuoteSnapshot,
    TradeIntent,
)


@dataclass
class RiskPolicyConfig:
    allowed_symbols: set[str] = field(default_factory=set)
    min_confidence: float = 0.55
    max_notional_per_trade_usd: float = 100.0
    max_portfolio_allocation_pct: float = 0.10
    max_total_exposure_pct: float = 0.30
    max_spread_pct: float = 0.01
    allow_short: bool = False
    allow_fractional: bool = True
    block_pattern_day_trader: bool = True


class RiskPolicy:
    """Hard controls that sit between the agent and a broker."""

    def __init__(self, config: RiskPolicyConfig):
        self.config = config

    def evaluate(
        self,
        intent: TradeIntent,
        account: AccountSnapshot,
        *,
        existing_positions: Iterable[PositionSnapshot] = (),
        quote: Optional[QuoteSnapshot] = None,
    ) -> ExecutionPolicyDecision:
        reasons: list[str] = []
        symbol = intent.symbol.upper()
        normalized_action = intent.action

        if self.config.allowed_symbols and symbol not in self.config.allowed_symbols:
            reasons.append(f"{symbol} is not in the allowlist.")

        if intent.confidence is not None and intent.confidence < self.config.min_confidence:
            reasons.append(
                f"Confidence {intent.confidence:.2f} is below the minimum {self.config.min_confidence:.2f}."
            )

        if normalized_action == "sell" and not self.config.allow_short:
            has_position = any(
                position.symbol.upper() == symbol and position.qty > 0
                for position in existing_positions
            )
            if not has_position:
                reasons.append("Sell signals are only allowed to reduce an existing long position.")

        if (
            self.config.block_pattern_day_trader
            and account.pattern_day_trader is True
            and normalized_action in {"buy", "sell"}
        ):
            reasons.append("Account is flagged as pattern day trader.")

        if quote and quote.spread_pct is not None and quote.spread_pct > self.config.max_spread_pct:
            reasons.append(
                f"Spread {quote.spread_pct:.4f} exceeds the maximum {self.config.max_spread_pct:.4f}."
            )

        current_exposure = sum(max(position.market_value, 0.0) for position in existing_positions)
        portfolio_value = account.portfolio_value or account.equity
        max_trade_notional = min(
            self.config.max_notional_per_trade_usd,
            account.buying_power,
            account.cash,
            portfolio_value * self.config.max_portfolio_allocation_pct,
        )
        requested_notional = intent.max_notional_usd or max_trade_notional
        suggested_notional = min(requested_notional, max_trade_notional)

        if normalized_action == "buy":
            if suggested_notional <= 0:
                reasons.append("No buying power is available for a new trade.")
            projected_exposure = current_exposure + suggested_notional
            max_total_exposure = portfolio_value * self.config.max_total_exposure_pct
            if projected_exposure > max_total_exposure:
                reasons.append(
                    f"Projected exposure {projected_exposure:.2f} exceeds the max {max_total_exposure:.2f}."
                )

        approved = not reasons and normalized_action != "hold"
        return ExecutionPolicyDecision(
            approved=approved,
            reasons=reasons or (["Hold signal does not place an order."] if normalized_action == "hold" else []),
            normalized_action=normalized_action,
            suggested_notional_usd=suggested_notional if approved else None,
        )
