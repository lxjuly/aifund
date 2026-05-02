# TradingAgents Implementation Plan

> Historical note: this document reflects the earlier AWS + NVIDIA NIM direction.
> The currently recommended path is Thunder Compute + Ollama. See:
> - `docs/task-specs/thunder-ollama-workflow.md`
> - `docs/task-specs/backlog.md`

## Objective

Use the upstream `tauricresearch/tradingagents` project with a self-hosted NVIDIA NIM endpoint instead of Bedrock.

## Phase 1: Prove the model server

- launch the `g6e` instance
- start NIM automatically
- validate:
  - `/v1/health/ready`
  - `/v1/models`
  - `/v1/chat/completions`

Exit criteria:

- one manual request succeeds
- latency is acceptable
- model fits in `48 GB`

## Phase 2: Adapt TradingAgents to NIM

We need to inspect the repo and implement one of these:

### Preferred path

Add a provider mode like:

- `llm_provider = "openai_compatible"`
- `base_url`
- `api_key`
- `model`

This is ideal because NIM exposes an OpenAI-compatible API.

### Fallback path

If the repo already supports custom OpenAI-style endpoints, configure it without code changes.

## Phase 3: Minimal integration surface

The trading app should accept:

- `NIM_BASE_URL`
- `NIM_API_KEY` if required
- `NIM_MODEL`

and map those into the LLM client configuration.

## Phase 4: First end-to-end run

Use:

- one ticker
- one date
- shallow research depth
- low debate round count

Capture:

- runtime
- GPU memory pressure
- final recommendation output
- any compatibility gaps with the OpenAI schema

## Phase 5: Make it operational

- add artifact output location
- add repeatable run command
- add optional scheduler
- add output persistence to S3 or local files

## Likely code tasks in the repo

- inspect provider abstraction
- inspect OpenAI client initialization
- add custom `base_url` support if missing
- add env var plumbing
- add a documented config example for NIM

## Recommended order from here

1. Open AWS account and launch the no-SSH instance.
2. Pick the exact NIM model.
3. Clone and inspect TradingAgents locally.
4. Patch TradingAgents for NIM.
5. Run the first end-to-end experiment.
