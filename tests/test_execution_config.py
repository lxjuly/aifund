import unittest

from tradingagents.execution.config import load_execution_env


class ExecutionConfigTests(unittest.TestCase):
    def test_load_execution_env_uses_defaults_and_normalizes_allowlist(self):
        env = load_execution_env(
            {
                "TRADINGAGENTS_ALLOWED_SYMBOLS": "nvda, spy ",
                "TRADINGAGENTS_MAX_NOTIONAL_USD": "75",
                "ALPACA_PAPER": "false",
            }
        )

        self.assertEqual(env.allowed_symbols, {"NVDA", "SPY"})
        self.assertEqual(env.risk_policy.allowed_symbols, {"NVDA", "SPY"})
        self.assertEqual(env.risk_policy.max_notional_per_trade_usd, 75.0)
        self.assertFalse(env.alpaca_paper)


if __name__ == "__main__":
    unittest.main()
