import unittest

from tradingagents.discovery import rate_holdings


class RatingTests(unittest.TestCase):
    def _holdings(self):
        return [
            # Three concerns: negative momentum, below trend, weak ROE -> sell.
            {"symbol": "WEAK", "momentum": -0.15, "value": 50.0, "quality": -0.10, "trend": -0.08},
            # One concern: negative momentum only -> trim.
            {"symbol": "MID", "momentum": -0.03, "value": 25.0, "quality": 0.12, "trend": 0.04},
            # No concerns -> hold.
            {"symbol": "OK", "momentum": 0.08, "value": 20.0, "quality": 0.15, "trend": 0.06},
            {"symbol": "STRONG", "momentum": 0.25, "value": 18.0, "quality": 0.22, "trend": 0.12},
        ]

    def test_verdicts(self):
        ratings = {r.symbol: r for r in rate_holdings(self._holdings())}
        self.assertEqual(ratings["WEAK"].verdict, "sell")
        self.assertEqual(ratings["MID"].verdict, "trim")
        self.assertEqual(ratings["OK"].verdict, "hold")
        self.assertEqual(ratings["STRONG"].verdict, "hold")

    def test_weakest_sorts_first(self):
        ratings = rate_holdings(self._holdings())
        self.assertEqual(ratings[0].symbol, "WEAK")
        self.assertEqual(ratings[0].verdict, "sell")
        self.assertEqual(ratings[-1].verdict, "hold")

    def test_sell_lists_its_reasons(self):
        ratings = {r.symbol: r for r in rate_holdings(self._holdings())}
        reasons = ratings["WEAK"].concerns
        self.assertIn("negative 6-month momentum", reasons)
        self.assertIn("price below its 200-day average", reasons)
        self.assertIn("weak return on equity", reasons)

    def test_missing_data_is_not_flagged(self):
        rows = [
            {"symbol": "BLANK", "momentum": None, "value": None, "quality": None, "trend": None},
            {"symbol": "GOOD", "momentum": 0.2, "value": 18.0, "quality": 0.2, "trend": 0.1},
        ]
        ratings = {r.symbol: r for r in rate_holdings(rows)}
        # No usable signals means no concerns and a hold.
        self.assertEqual(ratings["BLANK"].concerns, [])
        self.assertEqual(ratings["BLANK"].verdict, "hold")

    def test_two_concerns_triggers_sell(self):
        rows = [
            {"symbol": "AAA", "momentum": -0.05, "value": 20.0, "quality": 0.15, "trend": -0.02},
            {"symbol": "BBB", "momentum": 0.10, "value": 20.0, "quality": 0.15, "trend": 0.05},
        ]
        ratings = {r.symbol: r for r in rate_holdings(rows)}
        # AAA: negative momentum + below trend = two concerns -> sell.
        self.assertEqual(ratings["AAA"].verdict, "sell")


if __name__ == "__main__":
    unittest.main()
