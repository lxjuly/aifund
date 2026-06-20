---
id: anthropic-research-backend
type: decision
status: accepted
---

# Use Anthropic API As A Hosted Research Backend

AIfund uses the Anthropic API as a hosted model backend to run the TradingAgents
research graph now, while the Thunder + Ollama runtime is not reachable on the
current machine.

## Configuration

- `TRADINGAGENTS_LLM_PROVIDER=anthropic`
- deep model: `claude-sonnet-4-6` (Research Manager, Portfolio Manager)
- quick model: `claude-haiku-4-5` (analysts, debators, trader, signal/reflection)
- `TRADINGAGENTS_BACKEND_URL` is blanked so the Anthropic client uses its default
  API base rather than the OpenAI default in `DEFAULT_CONFIG`.

The split puts the strong model on the two deep judgments and the fast, cheaper
model on the high-volume agents, to control spend.

## Relationship To The Default

This does not replace [[thunder-ollama-serving]], which remains the low-cost
default serving path. Anthropic is an additional hosted option to get real
research runs working now and may stay useful for quality comparisons.

## Cost And Secrets

- This path bills API tokens to the operator's Anthropic account.
- `ANTHROPIC_API_KEY` is operator-supplied, stored only in the gitignored
  `.env.local`, never in source or in memory.
- Research depth is kept minimal for a first run.
