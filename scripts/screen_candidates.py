#!/usr/bin/env python3
"""Run the multi-factor discovery screen over a universe.

Stage one of the discovery funnel: rank a universe by a blend of momentum,
value, and quality, and print a shortlist. Uses yfinance, so it needs network
but no API key.

Examples:
  uv run python scripts/screen_candidates.py
  uv run python scripts/screen_candidates.py --top 5 --universe NVDA,AMD,AAPL,MSFT
  uv run python scripts/screen_candidates.py --out shortlist.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tradingagents.discovery import DEFAULT_UNIVERSE, score_universe
from tradingagents.discovery.yfinance_factors import fetch_factor_rows


def _fmt(value, spec="+.2f"):
    return format(value, spec) if isinstance(value, (int, float)) else "  n/a"


def main() -> int:
    parser = argparse.ArgumentParser(description="Multi-factor discovery screen.")
    parser.add_argument("--top", type=int, default=10, help="Shortlist size.")
    parser.add_argument(
        "--universe",
        type=str,
        default="",
        help="Comma-separated tickers. Defaults to the built-in universe.",
    )
    parser.add_argument("--out", type=str, default="", help="Optional JSON output path.")
    args = parser.parse_args()

    universe = (
        [t.strip().upper() for t in args.universe.split(",") if t.strip()]
        if args.universe
        else list(DEFAULT_UNIVERSE)
    )

    print(f"Screening {len(universe)} tickers ...", file=sys.stderr)
    rows = fetch_factor_rows(universe)
    ranked = score_universe(rows)

    print(f"\n{'rank':>4}  {'sym':<6}{'composite':>11}{'momentum':>11}{'value(PE)':>11}{'quality':>10}  cov")
    print("-" * 64)
    for i, c in enumerate(ranked[: args.top], start=1):
        comp = _fmt(c.composite) if c.composite is not None else "  n/a"
        print(
            f"{i:>4}  {c.symbol:<6}{comp:>11}"
            f"{_fmt(c.raw.get('momentum')):>11}"
            f"{_fmt(c.raw.get('value'), '.1f'):>11}"
            f"{_fmt(c.raw.get('quality'), '.2f'):>10}"
            f"  {c.coverage}/3"
        )

    if args.out:
        payload = [
            {
                "rank": i,
                "symbol": c.symbol,
                "composite": c.composite,
                "coverage": c.coverage,
                "factor_z": c.factor_z,
                "raw": c.raw,
            }
            for i, c in enumerate(ranked, start=1)
        ]
        Path(args.out).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"\nWrote {len(payload)} rows to {args.out}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
