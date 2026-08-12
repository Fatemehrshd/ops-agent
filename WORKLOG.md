## 2026-08-11 — Day 1

- Set up project with uv, structure, gitignore, env template.
- Verified Ollama exposes an OpenAI-compatible /v1 endpoint.
- Measured local throughput: ~6 tok/s on CPU.
- Confirmed Persian text costs ~1.6x more tokens than English.
- ADR 0001: local-model-first.

## 2026-08-12 — Day 2

- Found that the model resolves ambiguity by guessing rather than returning
  `unknown`; prompt examples cover out-of-scope requests but not ambiguous
  in-scope requests.
- Compared Ollama's `chat()` formatting with schema-in-prompt structured
  output.
- Ran a four-row experiment comparing vague prompts, schema in prompt,
  constrained decoding, and semantic definitions + constrained decoding.
- Best result: semantic intent definitions + constrained decoding achieved
  9/10 intent accuracy, with 10/10 valid JSON and 10/10 valid schemas.
- Found that two remaining failures are better explained by missing intents
  in the taxonomy rather than model errors.
- ADR 0003: constrained decoding.