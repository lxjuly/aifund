from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping, Optional

from tradingagents.default_config import DEFAULT_CONFIG

from .risk_policy import RiskPolicyConfig


def _load_dotenv_if_available() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return

    load_dotenv()
    load_dotenv(".env.local", override=False)
    load_dotenv(".env.enterprise", override=False)


def _get_bool(environ: Mapping[str, str], key: str, default: bool) -> bool:
    value = environ.get(key)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _get_float(environ: Mapping[str, str], key: str, default: float) -> float:
    value = environ.get(key)
    return float(value) if value not in (None, "") else default


def _get_csv_set(environ: Mapping[str, str], key: str) -> set[str]:
    value = environ.get(key, "")
    return {item.strip().upper() for item in value.split(",") if item.strip()}


@dataclass
class ExecutionEnvConfig:
    llm_provider: str
    backend_url: str
    deep_think_llm: str
    quick_think_llm: str
    output_language: str
    max_debate_rounds: int
    max_risk_discuss_rounds: int
    google_thinking_level: Optional[str]
    openai_reasoning_effort: Optional[str]
    anthropic_effort: Optional[str]
    alpaca_api_key: Optional[str]
    alpaca_secret_key: Optional[str]
    alpaca_base_url: Optional[str]
    alpaca_paper: bool
    submit_orders: bool
    results_dir: str
    cache_dir: str
    allowed_symbols: set[str]
    risk_policy: RiskPolicyConfig

    def build_graph_config(self) -> dict:
        config = DEFAULT_CONFIG.copy()
        config["llm_provider"] = self.llm_provider
        config["backend_url"] = self.backend_url
        config["deep_think_llm"] = self.deep_think_llm
        config["quick_think_llm"] = self.quick_think_llm
        config["output_language"] = self.output_language
        config["max_debate_rounds"] = self.max_debate_rounds
        config["max_risk_discuss_rounds"] = self.max_risk_discuss_rounds
        config["google_thinking_level"] = self.google_thinking_level
        config["openai_reasoning_effort"] = self.openai_reasoning_effort
        config["anthropic_effort"] = self.anthropic_effort
        config["results_dir"] = self.results_dir
        config["data_cache_dir"] = self.cache_dir
        return config


def load_execution_env(environ: Optional[Mapping[str, str]] = None) -> ExecutionEnvConfig:
    _load_dotenv_if_available()
    environ = environ or os.environ

    llm_provider = environ.get("TRADINGAGENTS_LLM_PROVIDER", DEFAULT_CONFIG["llm_provider"])
    backend_url = environ.get("TRADINGAGENTS_BACKEND_URL", DEFAULT_CONFIG["backend_url"])
    deep_think_llm = environ.get("TRADINGAGENTS_DEEP_MODEL", DEFAULT_CONFIG["deep_think_llm"])
    quick_think_llm = environ.get("TRADINGAGENTS_QUICK_MODEL", DEFAULT_CONFIG["quick_think_llm"])
    output_language = environ.get("TRADINGAGENTS_OUTPUT_LANGUAGE", DEFAULT_CONFIG["output_language"])
    max_debate_rounds = int(environ.get("TRADINGAGENTS_RESEARCH_DEPTH", DEFAULT_CONFIG["max_debate_rounds"]))
    max_risk_discuss_rounds = int(
        environ.get("TRADINGAGENTS_RISK_DEPTH", DEFAULT_CONFIG["max_risk_discuss_rounds"])
    )

    allowed_symbols = _get_csv_set(environ, "TRADINGAGENTS_ALLOWED_SYMBOLS")
    risk_policy = RiskPolicyConfig(
        allowed_symbols=allowed_symbols,
        min_confidence=_get_float(environ, "TRADINGAGENTS_MIN_CONFIDENCE", 0.55),
        max_notional_per_trade_usd=_get_float(environ, "TRADINGAGENTS_MAX_NOTIONAL_USD", 100.0),
        max_portfolio_allocation_pct=_get_float(
            environ, "TRADINGAGENTS_MAX_PORTFOLIO_ALLOCATION_PCT", 0.10
        ),
        max_total_exposure_pct=_get_float(environ, "TRADINGAGENTS_MAX_TOTAL_EXPOSURE_PCT", 0.30),
        max_spread_pct=_get_float(environ, "TRADINGAGENTS_MAX_SPREAD_PCT", 0.01),
        allow_short=_get_bool(environ, "TRADINGAGENTS_ALLOW_SHORT", False),
        allow_fractional=_get_bool(environ, "TRADINGAGENTS_ALLOW_FRACTIONAL", True),
        block_pattern_day_trader=_get_bool(environ, "TRADINGAGENTS_BLOCK_PDT", True),
    )

    return ExecutionEnvConfig(
        llm_provider=llm_provider,
        backend_url=backend_url,
        deep_think_llm=deep_think_llm,
        quick_think_llm=quick_think_llm,
        output_language=output_language,
        max_debate_rounds=max_debate_rounds,
        max_risk_discuss_rounds=max_risk_discuss_rounds,
        google_thinking_level=environ.get("TRADINGAGENTS_GOOGLE_THINKING_LEVEL"),
        openai_reasoning_effort=environ.get("TRADINGAGENTS_OPENAI_REASONING_EFFORT"),
        anthropic_effort=environ.get("TRADINGAGENTS_ANTHROPIC_EFFORT"),
        alpaca_api_key=environ.get("ALPACA_API_KEY"),
        alpaca_secret_key=environ.get("ALPACA_SECRET_KEY"),
        alpaca_base_url=environ.get("ALPACA_BASE_URL"),
        alpaca_paper=_get_bool(environ, "ALPACA_PAPER", True),
        submit_orders=_get_bool(environ, "TRADINGAGENTS_SUBMIT_ORDERS", False),
        results_dir=environ.get("TRADINGAGENTS_RESULTS_DIR", DEFAULT_CONFIG["results_dir"]),
        cache_dir=environ.get("TRADINGAGENTS_CACHE_DIR", DEFAULT_CONFIG["data_cache_dir"]),
        allowed_symbols=allowed_symbols,
        risk_policy=risk_policy,
    )
