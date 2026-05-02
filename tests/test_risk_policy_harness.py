import json
import unittest
from pathlib import Path

from tradingagents.execution.risk_policy import RiskPolicy, RiskPolicyConfig
from tradingagents.execution.schemas import AccountSnapshot, PositionSnapshot, TradeIntent


FIXTURES = Path(__file__).parent / "harness_fixtures" / "risk_policy_cases.json"


class RiskPolicyHarnessTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads(FIXTURES.read_text(encoding="utf-8"))

    def test_risk_policy_fixture_cases(self):
        for case in self.cases:
            with self.subTest(case=case["name"]):
                config_data = dict(case["config"])
                if "allowed_symbols" in config_data:
                    config_data["allowed_symbols"] = set(config_data["allowed_symbols"])

                policy = RiskPolicy(RiskPolicyConfig(**config_data))
                intent = TradeIntent(**case["intent"], raw_decision=case["intent"]["thesis"])
                account = AccountSnapshot(**case["account"])
                positions = [PositionSnapshot(**position) for position in case["positions"]]

                result = policy.evaluate(intent, account, existing_positions=positions)

                self.assertEqual(result.approved, case["expected_approved"])
                self.assertEqual(result.normalized_action, case["expected_action"])

                expected_reason_substring = case.get("expected_reason_substring")
                if expected_reason_substring:
                    self.assertTrue(
                        any(expected_reason_substring in reason for reason in result.reasons),
                        msg=f"Expected reason containing '{expected_reason_substring}', got {result.reasons}",
                    )

    def test_sell_without_position_is_rejected_when_shorting_is_disabled(self):
        policy = RiskPolicy(
            RiskPolicyConfig(
                allowed_symbols={"NVDA"},
                allow_short=False,
            )
        )
        intent = TradeIntent(
            symbol="NVDA",
            action="sell",
            rating="SELL",
            confidence=0.9,
            thesis="Exit immediately.",
            thesis_excerpt="Exit immediately.",
            raw_decision="Exit immediately.",
        )
        account = AccountSnapshot(
            equity=1000.0,
            cash=1000.0,
            buying_power=1000.0,
            portfolio_value=1000.0,
            pattern_day_trader=False,
        )

        result = policy.evaluate(intent, account, existing_positions=[])

        self.assertFalse(result.approved)
        self.assertTrue(any("existing long position" in reason for reason in result.reasons))


if __name__ == "__main__":
    unittest.main()
