from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from tradingagents.execution.broker.alpaca import AlpacaBroker
from tradingagents.execution.config import load_execution_env
from tradingagents.execution.risk_policy import RiskPolicy
from tradingagents.execution.runner import TradingAgentRunner
from tradingagents.graph.trading_graph import TradingAgentsGraph


console = Console()
app = typer.Typer(
    name="exec",
    help="Non-interactive execution and paper-trading commands for TradingAgents.",
    add_completion=True,
)


def _build_runner(*, submit_orders: bool) -> TradingAgentRunner:
    env = load_execution_env()
    graph = TradingAgentsGraph(debug=False, config=env.build_graph_config())
    policy = RiskPolicy(env.risk_policy)
    broker = None

    if submit_orders:
        broker = AlpacaBroker(
            api_key=env.alpaca_api_key,
            secret_key=env.alpaca_secret_key,
            paper=env.alpaca_paper,
            base_url=env.alpaca_base_url,
        )

    return TradingAgentRunner(graph, risk_policy=policy, broker=broker)


def _render_result(result) -> None:
    summary = {
        "rating": result.rating,
        "intent": {
            "symbol": result.intent.symbol,
            "action": result.intent.action,
            "rating": result.intent.rating,
            "confidence": result.intent.confidence,
            "thesis_excerpt": result.intent.thesis_excerpt,
        },
        "policy": {
            "approved": result.policy_decision.approved,
            "normalized_action": result.policy_decision.normalized_action,
            "reasons": result.policy_decision.reasons,
            "suggested_notional_usd": result.policy_decision.suggested_notional_usd,
        },
        "broker_order": result.broker_order,
    }
    console.print(Panel.fit(json.dumps(summary, indent=2), title="Execution Summary"))


@app.command("paper")
def paper_trade(
    symbol: str = typer.Argument(..., help="Ticker symbol to analyze."),
    trade_date: str = typer.Argument(..., help="Trade date in YYYY-MM-DD format."),
    submit_orders: bool = typer.Option(
        False,
        "--submit-orders",
        help="Actually submit to Alpaca using configured credentials instead of dry-run mode.",
    ),
) -> None:
    """Run TradingAgents non-interactively and evaluate the result against the execution policy."""
    runner = _build_runner(submit_orders=submit_orders)
    result = runner.run(symbol, trade_date)
    _render_result(result)


@app.command("from-log")
def from_log(
    source_log: Path = typer.Argument(..., exists=True, readable=True, help="TradingAgents full state log JSON."),
) -> None:
    """Print the final decision from a saved log and the replay capture command to archive it."""
    payload = json.loads(source_log.read_text(encoding="utf-8"))
    symbol = payload["company_of_interest"]
    trade_date = payload["trade_date"]
    final_trade_decision = payload["final_trade_decision"]

    console.print(Panel.fit(final_trade_decision, title=f"{symbol} {trade_date} Final Decision"))
    console.print(
        "\n".join(
            [
                "Replay capture command:",
                f"python3 scripts/capture_replay_case.py --source-log {source_log}",
            ]
        )
    )
