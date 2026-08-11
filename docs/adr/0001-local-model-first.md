# 0001 — Local model first

## Status
Accepted

## Context
Hosted LLM provider APIs are not reachable from the current network.
The roadmap depends on high-volume model calls, so this
blocks everything if unresolved.
Hardware: 16 GB RAM, integrated GPU only, so inference runs on CPU.

## Decision
Serve Qwen locally through Ollama's OpenAI-compatible endpoint at /v1.
All application code talks to an internal client interface, never to a
provider SDK directly. Model name and base URL come from environment
variables.

## Alternatives considered
- Waiting for hosted API access: blocks all work indefinitely.
- Calling the Ollama client directly throughout the codebase: simpler
  today, but makes a later switch to a hosted model expensive.

## Consequences
- Measured throughput: ~6 tok/s generation, ~1.5s fixed overhead per call.
- A full 30-case eval run takes 20-30 minutes, so model responses must be
  cached on disk during tests. This is a hard requirement, not an optimisation.
- Tool chains must stay short (max 3 steps) and responses must be capped.
- Persian input costs ~1.6x more tokens than English (measured: 65 vs 41).
  System prompts and tool descriptions stay in English; user-facing text
  stays Persian.
- Switching to a hosted model later is a one-variable change.