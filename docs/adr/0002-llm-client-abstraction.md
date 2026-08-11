#  0002 — Single LLM client interface

## Status
Accepted 

## Context
The project runs against a local model today; a hosted model may be used
later. Measured generation speed is ~6 tok/s, which makes repeated
evaluation runs impractical without caching.

## Decision
- Only `chat()` is responsible for communicating with the model.
- `chat()` returns a typed `LLMResponse`, not a plain dict, carrying token
  counts, latency and a cost field.
- Responses are cached on disk, not in memory, so they survive between runs.
- The cache key is a hash of the entire payload — messages, model,
  temperature, tools — not just the message content.
- Model name, base URL and cache settings are read from environment
  variables, never hardcoded.

## Alternatives considered
- Calling the SDK directly from every module: easier to implement with less code,
  but any future change — caching, tracing, switching provider — would have
  to touch every call site.
- In-memory caching: simpler to implement, but the cache is empty on every
  run, so it does not help the one case that matters — repeated eval runs.

## Consequences
- Cold call ~12.9s, cached call ~0.012s — roughly 1000x faster.
- Estimated: a 30-case eval at ~3 model calls per case takes ~20 minutes on a
  cold cache, and seconds on a warm one. This is what makes iterating on the
  eval set practical at all.
- The cache key encodes temperature and tools, so any change to either
  invalidates previous entries.
- Switching model or provider is a single environment variable change.
- Adding Langfuse tracing in week 7 means editing one function.
- `cost_usd` returns 0 at this stage. When a hosted model is added, the field
  is already there and already read by callers, so only that one method needs
  filling — no new field on the class, no changes at any call site.