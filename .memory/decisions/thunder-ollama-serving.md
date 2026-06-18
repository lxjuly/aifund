---
id: thunder-ollama-serving
type: decision
status: accepted
---

# Use Thunder Compute Plus Ollama For Model Serving

AIfund serves models through Thunder Compute running Ollama, exposed on an
OpenAI-compatible endpoint at `http://localhost:11434/v1`.

The local config uses a split model setup:

- deep model: `qwen2.5:14b`
- quick model: `llama3.1:8b`

This is preferred over paid AWS GPU infrastructure for model-serving
experiments. A first real end-to-end dry run succeeded against this path.
