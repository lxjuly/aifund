import math
import unittest

from tradingagents.discovery import DEFAULT_FACTORS, Factor, score_universe


class ScreenerTests(unittest.TestCase):
    def _rows(self):
        # AAA dominates every factor; DDD is worst on every factor.
        return [
            {"symbol": "AAA", "momentum": 0.30, "value": 15.0, "quality": 0.25},
            {"symbol": "BBB", "momentum": 0.10, "value": 25.0, "quality": 0.10},
            {"symbol": "CCC", "momentum": 0.20, "value": 20.0, "quality": 0.18},
            {"symbol": "DDD", "momentum": -0.05, "value": 40.0, "quality": 0.05},
        ]

    def test_best_on_all_factors_ranks_first(self):
        ranked = score_universe(self._rows())
        self.assertEqual(ranked[0].symbol, "AAA")
        self.assertEqual(ranked[-1].symbol, "DDD")
        self.assertEqual(ranked[0].coverage, 3)

    def test_value_is_lower_is_better(self):
        # Two names identical except P/E; the cheaper one must score higher.
        rows = [
            {"symbol": "CHEAP", "momentum": 0.1, "value": 10.0, "quality": 0.15},
            {"symbol": "RICH", "momentum": 0.1, "value": 30.0, "quality": 0.15},
        ]
        ranked = {c.symbol: c for c in score_universe(rows)}
        self.assertGreater(ranked["CHEAP"].composite, ranked["RICH"].composite)
        # Lower P/E yields a positive (good) value z-score.
        self.assertGreater(ranked["CHEAP"].factor_z["value"], 0)

    def test_missing_factor_is_skipped_and_weights_renormalize(self):
        rows = [
            {"symbol": "AAA", "momentum": 0.30, "value": None, "quality": 0.25},
            {"symbol": "BBB", "momentum": 0.10, "value": 25.0, "quality": 0.10},
            {"symbol": "CCC", "momentum": 0.20, "value": 20.0, "quality": 0.18},
        ]
        ranked = {c.symbol: c for c in score_universe(rows)}
        # AAA was scored on the two available factors only.
        self.assertEqual(ranked["AAA"].coverage, 2)
        self.assertNotIn("value", ranked["AAA"].factor_z)
        self.assertIsNotNone(ranked["AAA"].composite)

    def test_nan_is_treated_as_missing(self):
        rows = [
            {"symbol": "AAA", "momentum": float("nan"), "value": 15.0, "quality": 0.25},
            {"symbol": "BBB", "momentum": 0.10, "value": 25.0, "quality": 0.10},
        ]
        ranked = {c.symbol: c for c in score_universe(rows)}
        self.assertNotIn("momentum", ranked["AAA"].factor_z)

    def test_no_usable_factors_sorts_last(self):
        rows = [
            {"symbol": "GOOD", "momentum": 0.30, "value": 15.0, "quality": 0.25},
            {"symbol": "BLANK", "momentum": None, "value": None, "quality": None},
            {"symbol": "OK", "momentum": 0.10, "value": 25.0, "quality": 0.10},
        ]
        ranked = score_universe(rows)
        self.assertEqual(ranked[-1].symbol, "BLANK")
        self.assertIsNone(ranked[-1].composite)

    def test_custom_factor_weights(self):
        rows = [
            {"symbol": "MOM", "momentum": 0.40, "value": 30.0, "quality": 0.05},
            {"symbol": "VAL", "momentum": 0.05, "value": 10.0, "quality": 0.20},
        ]
        momentum_only = (Factor("momentum", 1.0, True),)
        ranked = score_universe(rows, factors=momentum_only)
        self.assertEqual(ranked[0].symbol, "MOM")


if __name__ == "__main__":
    unittest.main()
