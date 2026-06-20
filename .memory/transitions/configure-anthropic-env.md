---
id: configure-anthropic-env
type: transition
episode: configure-anthropic-backend
operation: create
target_type: config
target_id: env-local-anthropic
---

# Configure Anthropic Env

## Rationale

Running the graph against Anthropic needs the provider, models, and key wired
into the supported config flow.

## Before

There was no `.env.local`; the default config pointed at OpenAI.

## After

`.env.local` (gitignored) sets provider anthropic, deep `claude-sonnet-4-6`,
quick `claude-haiku-4-5`, a blanked backend URL, and a placeholder
`ANTHROPIC_API_KEY` for the operator to supply.

## Evidence

- `.env.local`
- `tradingagents/execution/config.py`
