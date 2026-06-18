# Foundational Assumptions

## Decision Engine Is Separable From Execution

The TradingAgents debate graph can produce decisions independently of how trades
are executed, so the broker layer can change without changing the decision
engine.

## Low-Cost Serving Is Sufficient For Research

Thunder Compute plus Ollama can serve models well enough for real research runs,
so paid cloud GPU infrastructure is not required for near-term work.

## Replay Fixtures Make Autonomy Safe

Captured real runs and harnesses are the safety layer that lets agents develop
AIfund autonomously without live-trading risk.

## Paper First, Live Later

Value can be validated entirely in paper and simulated environments before any
real-money execution is considered.
