#!/usr/bin/env python3
"""Capture a TradingAgents decision into the replay harness corpus."""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tradingagents.execution.risk_policy import RiskPolicy, RiskPolicyConfig
from tradingagents.execution.schemas import AccountSnapshot, PositionSnapshot
from tradingagents.execution.signal_parser import SignalParser


DEFAULT_ACCOUNT = {
    "equity": 1000.0,
    "cash": 500.0,
    "buying_power": 500.0,
    "portfolio_value": 1000.0,
    "pattern_day_trader": False,
}

DEFAULT_POLICY = {
    "max_notional_per_trade_usd": 100.0,
    "max_portfolio_allocation_pct": 0.2,
    "max_total_exposure_pct": 0.5,
    "min_confidence": 0.55,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--source-log", type=Path, help="Path to a TradingAgents full state log JSON.")
    source_group.add_argument("--source-text", type=Path, help="Path to a plain text file containing final_trade_decision.")

    parser.add_argument("--symbol", help="Ticker symbol override when not available in the source.")
    parser.add_argument("--trade-date", help="Trade date override when not available in the source.")
    parser.add_argument("--name", help="Fixture name override.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tests/harness_fixtures/replay_cases.json"),
        help="Replay corpus JSON file to update.",
    )
    parser.add_argument(
        "--allow-symbols",
        help="Comma-separated allowlist for the generated risk policy. Defaults to the captured symbol only.",
    )
    parser.add_argument(
        "--position",
        action="append",
        default=[],
        help="Optional existing position in the form SYMBOL:QTY:MARKET_VALUE[:SIDE]. Can be passed multiple times.",
    )
    return parser.parse_args()


def load_source(args: argparse.Namespace) -> Dict[str, Any]:
    if args.source_log:
        payload = json.loads(args.source_log.read_text(encoding="utf-8"))
        return {
            "symbol": args.symbol or payload.get("company_of_interest"),
            "trade_date": args.trade_date or payload.get("trade_date"),
            "final_trade_decision": payload.get("final_trade_decision", ""),
        }

    return {
        "symbol": args.symbol,
        "trade_date": args.trade_date,
        "final_trade_decision": args.source_text.read_text(encoding="utf-8"),
    }


def parse_positions(raw_positions: List[str]) -> List[Dict[str, Any]]:
    positions: List[Dict[str, Any]] = []
    for item in raw_positions:
        parts = item.split(":")
        if len(parts) not in {3, 4}:
            raise ValueError(f"Invalid --position '{item}'. Expected SYMBOL:QTY:MARKET_VALUE[:SIDE].")
        symbol, qty, market_value = parts[:3]
        side = parts[3] if len(parts) == 4 else "long"
        positions.append(
            {
                "symbol": symbol.upper(),
                "qty": float(qty),
                "market_value": float(market_value),
                "side": side,
            }
        )
    return positions


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def build_case(args: argparse.Namespace) -> Dict[str, Any]:
    payload = load_source(args)
    symbol = (payload.get("symbol") or "").upper()
    trade_date = payload.get("trade_date")
    final_trade_decision = (payload.get("final_trade_decision") or "").strip()

    if not symbol:
        raise ValueError("A symbol is required. Pass --symbol or provide a log with company_of_interest.")
    if not trade_date:
        raise ValueError("A trade date is required. Pass --trade-date or provide a log with trade_date.")
    if not final_trade_decision:
        raise ValueError("No final_trade_decision content was found in the source.")

    parser = SignalParser()
    intent = parser.parse(symbol=symbol, raw_decision=final_trade_decision)

    allowed_symbols = (
        [part.strip().upper() for part in args.allow_symbols.split(",") if part.strip()]
        if args.allow_symbols
        else [symbol]
    )
    positions = parse_positions(args.position)
    policy_config = {
        "allowed_symbols": allowed_symbols,
        **DEFAULT_POLICY,
    }
    policy = RiskPolicy(RiskPolicyConfig(allowed_symbols=set(allowed_symbols), **DEFAULT_POLICY))
    account = AccountSnapshot(**DEFAULT_ACCOUNT)
    evaluation = policy.evaluate(
        intent,
        account,
        existing_positions=[PositionSnapshot(**position) for position in positions],
    )

    case: Dict[str, Any] = {
        "name": args.name or f"{slugify(symbol)}_{slugify(trade_date)}_{slugify(intent.rating)}",
        "symbol": symbol,
        "trade_date": trade_date,
        "final_trade_decision": final_trade_decision,
        "expected_rating": intent.rating,
        "expected_action": intent.action,
        "risk_policy": policy_config,
        "account": DEFAULT_ACCOUNT,
        "positions": positions,
        "expected_approved": evaluation.approved,
    }

    if evaluation.approved and evaluation.normalized_action in {"buy", "sell"}:
        case["expected_order_side"] = evaluation.normalized_action
    elif evaluation.reasons:
        case["expected_reason_substring"] = evaluation.reasons[0].split(".")[0]

    return case


def append_case(output_path: Path, case: Dict[str, Any]) -> None:
    if output_path.exists():
        data = json.loads(output_path.read_text(encoding="utf-8"))
    else:
        data = []

    existing_names = {item["name"] for item in data}
    if case["name"] in existing_names:
        raise ValueError(f"A replay case named '{case['name']}' already exists in {output_path}.")

    data.append(case)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    try:
        case = build_case(args)
        append_case(args.output, case)
    except Exception as exc:  # pragma: no cover - CLI error path
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Added replay case '{case['name']}' to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
