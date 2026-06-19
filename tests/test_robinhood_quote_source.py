import unittest

from tradingagents.execution.market_data import (
    READ_ONLY_TOOLS,
    RobinhoodQuoteSource,
    RobinhoodReadOnlyError,
)


class FakeMcp:
    """Records calls and returns canned payloads keyed by tool name."""

    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def __call__(self, tool, args):
        self.calls.append((tool, args))
        return self.responses[tool]


class RobinhoodQuoteSourceTests(unittest.TestCase):
    def test_get_quote_maps_fields_and_computes_spread(self):
        fake = FakeMcp(
            {
                "get_equity_quotes": {
                    "quotes": [
                        {
                            "symbol": "NVDA",
                            "last_trade_price": "100.00",
                            "bid_price": "99.50",
                            "ask_price": "100.50",
                            "updated_at": "2026-04-24T15:30:00Z",
                        }
                    ]
                }
            }
        )
        source = RobinhoodQuoteSource(mcp_call=fake)

        quote = source.get_quote("nvda")

        self.assertEqual(quote.symbol, "NVDA")
        self.assertAlmostEqual(quote.last_price, 100.00)
        self.assertAlmostEqual(quote.bid_price, 99.50)
        self.assertAlmostEqual(quote.ask_price, 100.50)
        self.assertAlmostEqual(quote.spread_pct, 1.0 / 100.0)
        self.assertIsNotNone(quote.as_of)
        self.assertEqual(fake.calls[0][0], "get_equity_quotes")

    def test_get_quote_falls_back_to_mid_when_no_last_price(self):
        fake = FakeMcp(
            {"get_equity_quotes": [{"symbol": "AAPL", "bid": 9.0, "ask": 11.0}]}
        )
        source = RobinhoodQuoteSource(mcp_call=fake)

        quote = source.get_quote("AAPL")

        self.assertAlmostEqual(quote.last_price, 10.0)
        self.assertAlmostEqual(quote.spread_pct, 2.0 / 10.0)

    def test_get_quote_matches_symbol_among_many(self):
        fake = FakeMcp(
            {
                "get_equity_quotes": {
                    "results": [
                        {"symbol": "MSFT", "last_price": 1.0},
                        {"symbol": "NVDA", "last_price": 100.0},
                    ]
                }
            }
        )
        source = RobinhoodQuoteSource(mcp_call=fake)

        quote = source.get_quote("NVDA")

        self.assertEqual(quote.symbol, "NVDA")
        self.assertAlmostEqual(quote.last_price, 100.0)

    def test_is_tradable_reads_flag_and_state(self):
        source_true = RobinhoodQuoteSource(
            mcp_call=FakeMcp(
                {"get_equity_tradability": [{"symbol": "NVDA", "tradable": True}]}
            )
        )
        source_state = RobinhoodQuoteSource(
            mcp_call=FakeMcp(
                {"get_equity_tradability": [{"symbol": "NVDA", "state": "active"}]}
            )
        )
        source_false = RobinhoodQuoteSource(
            mcp_call=FakeMcp(
                {"get_equity_tradability": [{"symbol": "NVDA", "tradable": False}]}
            )
        )

        self.assertTrue(source_true.is_tradable("NVDA"))
        self.assertTrue(source_state.is_tradable("NVDA"))
        self.assertFalse(source_false.is_tradable("NVDA"))

    def test_unconfigured_source_raises(self):
        source = RobinhoodQuoteSource()
        self.assertFalse(source.configured)
        with self.assertRaises(RobinhoodReadOnlyError):
            source.get_quote("NVDA")

    def test_order_tools_are_unreachable(self):
        # The read-only allowlist must never include order tools.
        for tool in ("place_equity_order", "review_equity_order", "cancel_equity_order"):
            self.assertNotIn(tool, READ_ONLY_TOOLS)

        # And the source refuses to call anything outside the allowlist.
        source = RobinhoodQuoteSource(mcp_call=FakeMcp({}))
        with self.assertRaises(RobinhoodReadOnlyError):
            source._call("place_equity_order", {"symbol": "NVDA"})


if __name__ == "__main__":
    unittest.main()
