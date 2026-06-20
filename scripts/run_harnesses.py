#!/usr/bin/env python3
"""Run the local execution harness suite."""

import subprocess
import sys
from pathlib import Path


HARNESS_TESTS = [
    "tests.test_execution_config",
    "tests.test_signal_parser_harness",
    "tests.test_risk_policy_harness",
    "tests.test_runner_harness",
    "tests.test_replay_harness",
    "tests.test_replay_capture_script",
    "tests.test_robinhood_quote_source",
    "tests.test_screener",
]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    cmd = [sys.executable, "-m", "unittest", *HARNESS_TESTS]
    return subprocess.call(cmd, cwd=root)


if __name__ == "__main__":
    raise SystemExit(main())
