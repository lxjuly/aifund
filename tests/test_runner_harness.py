import unittest

from tradingagents.execution.risk_policy import RiskPolicy, RiskPolicyConfig
from tradingagents.execution.runner import TradingAgentRunner
from tradingagents.execution.schemas import AccountSnapshot, PositionSnapshot


class FakeGraph:
    def __init__(self, final_trade_decision: str, rating: str):
        self.final_trade_decision = final_trade_decision
        self.rating = rating

    def propagate(self, symbol: str, trade_date: str):
        return {
            "symbol": symbol,
            "trade_date": trade_date,
            "final_trade_decision": self.final_trade_decision,
        }, self.rating


class FakeBroker:
    def __init__(self):
        self.orders = []

    def get_account(self):
        return AccountSnapshot(
            equity=1000.0,
            cash=500.0,
            buying_power=500.0,
            portfolio_value=1000.0,
            pattern_day_trader=False,
        )

    def get_positions(self):
        return [PositionSnapshot(symbol="SPY", qty=1.0, market_value=100.0, side="long")]

    def submit_order(self, order):
        payload = {
            "symbol": order.symbol,
            "side": order.side,
            "notional_usd": order.notional_usd,
        }
        self.orders.append(payload)
        return payload


class RunnerHarnessTests(unittest.TestCase):
    def test_runner_submits_order_when_policy_approves(self):
        graph = FakeGraph("**Rating**: Buy\n\nConfidence: 0.82", "BUY")
        broker = FakeBroker()
        runner = TradingAgentRunner(
            graph,
            risk_policy=RiskPolicy(
                RiskPolicyConfig(
                    allowed_symbols={"NVDA", "SPY"},
                    max_notional_per_trade_usd=100.0,
                    max_portfolio_allocation_pct=0.2,
                    max_total_exposure_pct=0.5,
                )
            ),
            broker=broker,
        )

        result = runner.run("NVDA", "2026-04-20")

        self.assertTrue(result.policy_decision.approved)
        self.assertIsNotNone(result.broker_order)
        self.assertEqual(result.broker_order["side"], "buy")
        self.assertEqual(len(broker.orders), 1)

    def test_runner_hold_signal_does_not_submit_order(self):
        graph = FakeGraph("FINAL TRANSACTION PROPOSAL: **HOLD**", "HOLD")
        broker = FakeBroker()
        runner = TradingAgentRunner(
            graph,
            risk_policy=RiskPolicy(RiskPolicyConfig(allowed_symbols={"NVDA"})),
            broker=broker,
        )

        result = runner.run("NVDA", "2026-04-20")

        self.assertFalse(result.policy_decision.approved)
        self.assertIsNone(result.broker_order)
        self.assertEqual(broker.orders, [])
        self.assertEqual(result.intent.action, "hold")

    def test_runner_evaluates_policy_in_dry_run_mode_without_broker(self):
        graph = FakeGraph("**Rating**: Buy\n\nConfidence: 0.82", "BUY")
        runner = TradingAgentRunner(
            graph,
            risk_policy=RiskPolicy(
                RiskPolicyConfig(
                    allowed_symbols={"NVDA", "SPY"},
                    max_notional_per_trade_usd=100.0,
                    max_portfolio_allocation_pct=0.2,
                    max_total_exposure_pct=0.5,
                )
            ),
        )

        result = runner.run("NVDA", "2026-04-20")

        self.assertTrue(result.policy_decision.approved)
        self.assertIsNone(result.broker_order)
        self.assertEqual(result.policy_decision.normalized_action, "buy")

    def test_runner_fails_closed_without_policy(self):
        graph = FakeGraph("**Rating**: Buy", "BUY")
        runner = TradingAgentRunner(graph)

        result = runner.run("NVDA", "2026-04-20")

        self.assertFalse(result.policy_decision.approved)
        self.assertIn("Risk policy is not configured.", result.policy_decision.reasons[0])


if __name__ == "__main__":
    unittest.main()
