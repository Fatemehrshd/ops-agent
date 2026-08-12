# 0003 - Constrained Decoding

## Status

Accepted

## Context

The intent-classification model must produce machine-readable output that
downstream code can reliably consume.

With a vague prompt, the model produced valid JSON in only 8/10 cases and
did not reliably follow the expected output structure. The model sometimes
invented different field names or output shapes.

The output contract is defined once using a Pydantic model. Its JSON Schema
can then be used either as prompt content or as a structured-output
constraint.

## Decision

Use the Pydantic model as the single source of truth for the output contract.

1. Generate JSON Schema from the Pydantic model rather than duplicating the
   schema manually.
2. Include semantic intent definitions and classification rules in the
   system prompt so the model understands the meaning of each intent.
3. Use constrained decoding at the API level to enforce the JSON Schema
   during generation.
4. Validate the generated response against the Pydantic model and propagate
   validation failures rather than silently returning `None`.

The raw LLM response remains available for debugging, while downstream code
can consume the validated Pydantic object.

## Alternatives Considered

### Regex / string cleaning

Tempting because it can remove common formatting problems such as Markdown
code fences, but it does not reliably enforce the complete schema or field
semantics.

### Retry until valid

Tempting because a second LLM call may produce valid output, but it adds
latency and cost and does not guarantee semantic correctness.

### Schema only via constrained decoding

Provides strong structural guarantees, but in testing it did not provide
sufficient semantic guidance by itself.

### Schema only in the prompt

Works well for this model, but structural correctness depends entirely on
the model following the instructions and therefore provides no generation-time
guarantee.

## Evaluation

| Method | Valid JSON | Valid Schema | Correct Intent |
|---|---:|---:|---:|
| Vague prompt | 8/10 | 0/10 | — |
| Schema in prompt | 10/10 | 10/10 | 8/10 |
| Constrained decoding | 10/10 | 10/10 | 7/10 |
| Semantic definitions + constrained decoding | 10/10 | 10/10 | 9/10 |

The evaluation used 10 test cases. Therefore, differences of one case
between rows are not statistically meaningful and should not be interpreted
as evidence that constrained decoding reduces accuracy. The test set is too
small to reliably rank the three structured-output approaches by semantic
accuracy.

## Interpretation

The experiment separates three different concerns:

- **Formatting:** constrained decoding provides reliable structural output.
- **Semantic classification:** the model needs explicit descriptions of
  what each intent means.
- **Intent coverage:** some requests cannot be represented by the current
  intent taxonomy and should not automatically be treated as model errors.

The key observation is that constrained decoding provides a **guarantee of
structural validity**, not necessarily better average semantic accuracy.

For this model, including semantic intent definitions in the prompt provides
useful classification guidance. The final approach therefore combines
semantic definitions in the prompt with constrained decoding as a structural
guarantee.

Two of the remaining classification failures correspond to requests for
capabilities that are not represented by the current intent taxonomy. These
should be treated as missing intent coverage rather than automatically
classified as model failures.

## Consequences

### Positive

- Pydantic remains the single source of truth for the output contract.
- JSON Schema is generated rather than manually duplicated.
- Constrained decoding provides reliable structural output.
- Validation failures are explicit rather than silently ignored.
- Downstream code can rely on a validated Pydantic object.

### Trade-offs

- Semantic accuracy depends on the quality of the intent definitions in the
  prompt, making the prompt load-bearing.
- Intent definitions should therefore have their own regression tests.
- The current intent taxonomy must evolve when legitimate store requests
  cannot be represented by an existing intent.
- Constrained decoding may introduce additional latency depending on the
  backend and model.