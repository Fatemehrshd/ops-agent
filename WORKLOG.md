## 2026-08-11 — Day 1
- Set up project with uv, structure, gitignore, env template.
- Verified Ollama exposes an OpenAI-compatible /v1 endpoint.
- Measured local throughput: ~6 tok/s on CPU.
- Confirmed Persian text costs ~1.6x more tokens than English.
- ADR 0001: local-model-first.

## 2026-08-12 - Day 2
- model resolves ambiguity by guessing rather than returning unknown; prompt examples cover out-of-scope but not ambiguous-in-scope.
- Compared ollama's chat() and the one is written.