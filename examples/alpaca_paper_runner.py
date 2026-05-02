from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.execution import RiskPolicy, RiskPolicyConfig
from tradingagents.execution.broker import AlpacaBroker
from tradingagents.execution.runner import TradingAgentRunner
from tradingagents.graph.trading_graph import TradingAgentsGraph


config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "ollama"
config["backend_url"] = "http://localhost:11434/v1"
config["deep_think_llm"] = "llama3.1:70b"
config["quick_think_llm"] = "llama3.1:70b"

graph = TradingAgentsGraph(debug=False, config=config)
policy = RiskPolicy(
    RiskPolicyConfig(
        allowed_symbols={"SPY", "QQQ", "NVDA"},
        min_confidence=0.55,
        max_notional_per_trade_usd=100.0,
        max_portfolio_allocation_pct=0.10,
        max_total_exposure_pct=0.30,
    )
)
broker = AlpacaBroker(paper=True)
runner = TradingAgentRunner(graph, risk_policy=policy, broker=broker)

result = runner.run("NVDA", "2026-04-20")
print(result.intent)
print(result.policy_decision)
print(result.broker_order)
