from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Iterable, Optional

from .risk_policy import RiskPolicy
from .schemas import (
    AccountSnapshot,
    ExecutionPolicyDecision,
    OrderRequest,
    PositionSnapshot,
    TradeIntent,
)
from .signal_parser import SignalParser

if TYPE_CHECKING:
    from tradingagents.graph.trading_graph import TradingAgentsGraph


@dataclass
class RunnerResult:
    final_state: dict[str, Any]
    rating: str
    intent: TradeIntent
    policy_decision: ExecutionPolicyDecision
    broker_order: Optional[dict[str, Any]] = None


class TradingAgentRunner:
    """Glue code that connects TradingAgents, risk policy, and a broker."""

    def __init__(
        self,
        graph: "TradingAgentsGraph",
        *,
        signal_parser: Optional[SignalParser] = None,
        risk_policy: Optional[RiskPolicy] = None,
        broker: Any = None,
        account_snapshot: Optional[AccountSnapshot] = None,
        existing_positions: Optional[Iterable[PositionSnapshot]] = None,
    ):
        self.graph = graph
        self.signal_parser = signal_parser or SignalParser()
        self.risk_policy = risk_policy
        self.broker = broker
        self.account_snapshot = account_snapshot or AccountSnapshot(
            equity=1000.0,
            cash=500.0,
            buying_power=500.0,
            portfolio_value=1000.0,
            pattern_day_trader=False,
        )
        self.existing_positions = list(existing_positions or [])

    def run(self, symbol: str, trade_date: str) -> RunnerResult:
        final_state, rating = self.graph.propagate(symbol, trade_date)
        intent = self.signal_parser.parse(
            symbol=symbol,
            raw_decision=final_state["final_trade_decision"],
        )

        if not self.risk_policy:
            return RunnerResult(
                final_state=final_state,
                rating=rating,
                intent=intent,
                policy_decision=ExecutionPolicyDecision(
                    approved=False,
                    reasons=["Risk policy is not configured."],
                    normalized_action=intent.action,
                ),
            )

        if self.broker:
            account = self.broker.get_account()
            positions = self.broker.get_positions()
        else:
            account = self.account_snapshot
            positions = self.existing_positions

        policy_decision = self.risk_policy.evaluate(
            intent,
            account,
            existing_positions=positions,
        )

        broker_order = None
        if self.broker and policy_decision.approved and policy_decision.suggested_notional_usd:
            broker_order = self.broker.submit_order(
                OrderRequest(
                    symbol=intent.symbol,
                    side="buy" if policy_decision.normalized_action == "buy" else "sell",
                    notional_usd=policy_decision.suggested_notional_usd,
                )
            )

        return RunnerResult(
            final_state=final_state,
            rating=rating,
            intent=intent,
            policy_decision=policy_decision,
            broker_order=broker_order,
        )
