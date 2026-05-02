# Moomoo OpenAPI Broker Integration

## Recommendation

Use Moomoo OpenAPI as the preferred broker integration target, replacing Alpaca as the default path for new execution work.

## AI Skills

The official Moomoo OpenD skills are installed globally for Codex at:

```text
/Users/youmiss/.codex/skills/moomooapi
/Users/youmiss/.codex/skills/install-moomoo-opend
```

These skills came from Moomoo's official `opend-skills.zip` package and include:

- `moomooapi`: market data, account, order, position, subscription, and paper-trading helper scripts
- `install-moomoo-opend`: OpenD installation and SDK setup assistant

Future Moomoo adapter work should use these skills as the first reference before hand-writing SDK calls.

## Why Moomoo Fits

- It supports both quotation and trading APIs.
- It supports paper/simulated trading and live trading through the same API family.
- It provides a Python SDK, which fits the current TradingAgents codebase.
- It supports US stocks and ETFs, which matches the first low-risk execution scope.
- Its docs say there is no extra API trading fee; transaction fees follow the normal app fee schedule.

## Architecture Implication

Moomoo OpenAPI is not a pure HTTPS broker API. It requires `OpenD`, a gateway process that runs locally or on a server. The Python SDK talks to OpenD over TCP, and OpenD relays requests to Moomoo servers.

For this project, that means the broker path should be:

```text
TradingAgents execution runner
  -> Moomoo broker adapter
  -> local or hosted OpenD gateway
  -> Moomoo servers
```

## Safety Policy

- Keep dry-run mode as the default.
- Use paper/simulated trading first.
- Do not unlock or use live trading without explicit user approval.
- Store trade unlock credentials outside the repo.
- Keep the execution risk policy independent from the Moomoo adapter.
- Use long-only, allowlisted US stocks/ETFs for the first integration phase.

## Initial Adapter Scope

The first Moomoo adapter should implement only:

- account list or account selection
- account cash/equity query
- positions query
- open orders query, if needed by the policy layer
- paper/simulated order submission
- order normalization into the existing broker response schema

Live trading, options, short selling, margin, extended-hours orders, and multi-market support are out of scope until explicitly approved.

## Open Questions

- Where should OpenD run for operator use: local Mac, Thunder instance, or a small always-on host?
- Which Moomoo account region is the user using?
- Which exact market data permissions are available for the user's account?
- Does the Python package integrate cleanly with the current Python version used by `uv sync`?

## Sources

- Moomoo OpenAPI introduction: https://openapi.moomoo.com/moomoo-api-doc/en/intro/intro.html
- Moomoo authorities and quota: https://openapi.moomoo.com/moomoo-api-doc/en/intro/authority.html
- Moomoo fee docs: https://openapi.moomoo.com/moomoo-api-doc/en/intro/fee.html
- Moomoo trade overview: https://openapi.moomoo.com/moomoo-api-doc/en/trade/overview.html
- Moomoo place order docs: https://openapi.moomoo.com/moomoo-api-doc/en/trade/place-order.html
- Moomoo AI Integration & OpenClaw: https://openapi.moomoo.com/moomoo-api-doc/en/intro/ai.html
