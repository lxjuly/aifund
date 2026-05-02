import json
import unittest
from pathlib import Path

from tradingagents.execution.signal_parser import SignalParser


FIXTURES = Path(__file__).parent / "harness_fixtures" / "signal_parser_cases.json"


class SignalParserHarnessTests(unittest.TestCase):
    def setUp(self):
        self.parser = SignalParser()
        self.cases = json.loads(FIXTURES.read_text(encoding="utf-8"))

    def test_signal_parser_golden_cases(self):
        for case in self.cases:
            with self.subTest(case=case["name"]):
                intent = self.parser.parse(
                    symbol=case["symbol"],
                    raw_decision=case["raw_decision"],
                )
                self.assertEqual(intent.rating, case["expected_rating"])
                self.assertEqual(intent.action, case["expected_action"])
                self.assertEqual(intent.confidence, case["expected_confidence"])
                self.assertTrue(intent.thesis_excerpt)

    def test_signal_parser_rejects_unknown_decision_shape(self):
        with self.assertRaises(ValueError):
            self.parser.parse(
                symbol="NVDA",
                raw_decision="Executive Summary: interesting setup but no explicit rating is provided.",
            )


if __name__ == "__main__":
    unittest.main()
