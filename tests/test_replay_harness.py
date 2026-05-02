import json
import unittest
from pathlib import Path

from tradingagents.execution.risk_policy import RiskPolicy, RiskPolicyConfig
from tradingagents.execution.runner import TradingAgentRunner
from tradingagents.execution.schemas import AccountSnapshot, PositionSnapshot


FIXTURES = Path(__file__).parent / "harness_fixtures" / "replay_cases.json"


class ReplayGraph:
    def __init__(self, final_trade_decision: str, expected_rating: str):
        self.final_trade_decision = final_trade_decision
        self.expected_rating = expected_rating

    def propagate(self, symbol: str, trade_date: str):
        return {
            "symbol": symbol,
            "trade_date": trade_date,
            "final_trade_decision": self.final_trade_decision,
        }, self.expected_rating


class ReplayBroker:
    def __init__(self, account: AccountSnapshot, positions: list[PositionSnapshot]):
        self.account = account
        self.positions = positions
        self.orders = []

    def get_account(self):
        return self.account

    def get_positions(self):
        return list(self.positions)

    def submit_order(self, order):
        payload = {
            "symbol": order.symbol,
            "side": order.side,
            "notional_usd": order.notional_usd,
        }
        self.orders.append(payload)
        return payload


class ReplayHarnessTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads(FIXTURES.read_text(encoding="utf-8"))

    def test_replay_corpus(self):
        for case in self.cases:
            with self.subTest(case=case["name"]):
                config_data = dict(case["risk_policy"])
                config_data["allowed_symbols"] = set(config_data["allowed_symbols"])

                broker = ReplayBroker(
                    account=AccountSnapshot(**case["account"]),
                    positions=[PositionSnapshot(**position) for position in case["positions"]],
                )
                runner = TradingAgentRunner(
                    ReplayGraph(case["final_trade_decision"], case["expected_rating"]),
                    risk_policy=RiskPolicy(RiskPolicyConfig(**config_data)),
                    broker=broker,
                )

                result = runner.run(case["symbol"], case["trade_date"])

                self.assertEqual(result.intent.rating, case["expected_rating"])
                self.assertEqual(result.intent.action, case["expected_action"])
                self.assertEqual(result.policy_decision.approved, case["expected_approved"])

                expected_order_side = case.get("expected_order_side")
                if expected_order_side:
                    self.assertIsNotNone(result.broker_order)
                    self.assertEqual(result.broker_order["side"], expected_order_side)
                else:
                    self.assertIsNone(result.broker_order)

                expected_reason_substring = case.get("expected_reason_substring")
                if expected_reason_substring:
                    self.assertTrue(
                        any(expected_reason_substring in reason for reason in result.policy_decision.reasons),
                        msg=f"Expected reason containing '{expected_reason_substring}', got {result.policy_decision.reasons}",
                    )


if __name__ == "__main__":
    unittest.main()
