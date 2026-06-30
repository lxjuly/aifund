#!/usr/bin/env python3
"""Rate a portfolio of holdings to surface what to sell.

The inverse of the buy screen: pass the stocks you own and get a per-stock
verdict (sell / trim / hold) with reasons, weakest first. Uses yfinance, so it
needs network but no API key.

Examples:
  uv run python scripts/rate_holdings.py --portfolio NVDA,AAPL,INTC,PFE,DIS
  uv run python scripts/rate_holdings.py --portfolio NVDA,AAPL --position NVDA:0.22:95:80
  uv run python scripts/rate_holdings.py --portfolio-file my_holdings.txt --out ratings.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tradingagents.discovery import rate_holdings
from tradingagents.discovery.yfinance_factors import fetch_factor_rows

# A small sample portfolio used only when none is supplied.
SAMPLE_PORTFOLIO = ["NVDA", "AAPL", "INTC", "PFE", "DIS", "KO"]


def _fmt(value, spec="+.2f"):
    return format(value, spec) if isinstance(value, (int, float)) else "  n/a"


def _load_portfolio(args) -> list[str]:
    if args.portfolio:
        return [t.strip().upper() for t in args.portfolio.split(",") if t.strip()]
    if args.portfolio_file:
        text = Path(args.portfolio_file).read_text(encoding="utf-8")
        return [line.strip().upper() for line in text.splitlines() if line.strip()]
    print("No portfolio given; using a sample portfolio.", file=sys.stderr)
    return list(SAMPLE_PORTFOLIO)


def _load_positions(raw_positions: list[str]) -> dict[str, dict]:
    positions: dict[str, dict] = {}
    for raw in raw_positions:
        parts = [part.strip() for part in raw.split(":")]
        if len(parts) not in {3, 4}:
            raise ValueError(
                f"Invalid --position '{raw}'. Expected SYMBOL:WEIGHT:COST_BASIS[:MARKET_PRICE]."
            )
        symbol = parts[0].upper()
        positions[symbol] = {
            "weight": float(parts[1]),
            "cost_basis": float(parts[2]),
        }
        if len(parts) == 4:
            positions[symbol]["market_price"] = float(parts[3])
    return positions


def main() -> int:
    parser = argparse.ArgumentParser(description="Rate holdings to find sells.")
    parser.add_argument("--portfolio", type=str, default="", help="Comma-separated tickers.")
    parser.add_argument("--portfolio-file", type=str, default="", help="File with one ticker per line.")
    parser.add_argument(
        "--position",
        action="append",
        default=[],
        help="Optional position context as SYMBOL:WEIGHT:COST_BASIS[:MARKET_PRICE]. Can repeat.",
    )
    parser.add_argument("--out", type=str, default="", help="Optional JSON output path.")
    args = parser.parse_args()

    holdings = _load_portfolio(args)
    positions = _load_positions(args.position)
    print(f"Rating {len(holdings)} holdings ...", file=sys.stderr)
    rows = fetch_factor_rows(holdings)
    ratings = rate_holdings(rows, positions=positions)

    print(
        f"\n{'sym':<6}{'verdict':<8}{'composite':>11}{'weight':>8}"
        f"{'unrlzd':>9}{'momentum':>10}{'trend':>9}{'value(PE)':>11}{'quality':>9}  concerns"
    )
    print("-" * 116)
    for r in ratings:
        concerns = "; ".join(r.concerns) if r.concerns else "-"
        comp = _fmt(r.composite) if r.composite is not None else "  n/a"
        unrealized = r.position.get("unrealized_return")
        print(
            f"{r.symbol:<6}{r.verdict.upper():<8}{comp:>11}"
            f"{_fmt(r.position.get('weight'), '.1%'):>8}"
            f"{_fmt(unrealized, '+.1%'):>9}"
            f"{_fmt(r.raw.get('momentum')):>10}"
            f"{_fmt(r.raw.get('trend')):>9}"
            f"{_fmt(r.raw.get('value'), '.1f'):>11}"
            f"{_fmt(r.raw.get('quality'), '.2f'):>9}"
            f"  {concerns}"
        )

    sells = [r.symbol for r in ratings if r.verdict == "sell"]
    trims = [r.symbol for r in ratings if r.verdict == "trim"]
    print(f"\nSell candidates: {', '.join(sells) or 'none'}", file=sys.stderr)
    print(f"Trim candidates: {', '.join(trims) or 'none'}", file=sys.stderr)

    if args.out:
        payload = [
            {
                "symbol": r.symbol,
                "verdict": r.verdict,
                "composite": r.composite,
                "concerns": r.concerns,
                "raw": r.raw,
                "position": r.position,
            }
            for r in ratings
        ]
        Path(args.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"Wrote {len(payload)} ratings to {args.out}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
