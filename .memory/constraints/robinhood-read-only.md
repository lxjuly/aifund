---
id: robinhood-read-only
type: constraint
status: active
---

# Robinhood Integration Is Read-Only

The Robinhood MCP integration calls read tools only. Order tools (place, review,
cancel) are never wired.

This is enforced in code by an allowlist and is a hard boundary until a
live-broker path is explicitly approved.

Implements part of [[adopt-robinhood-mcp-readonly]] and extends
[[execution-safety-boundaries]].
