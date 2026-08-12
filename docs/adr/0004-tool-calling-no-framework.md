# 0004 - Tool Calling

## Status

Accepted

## Context

The intent-classification approach worked for routing, but the agent ultimately
needs to interact with store operations. We therefore introduced tool calling
with four tools:

- `get_low_stock`
- `get_sales_summary`
- `get_discount_query`
- `update_stock`

Tool descriptions and parameter schemas are provided to the model through the
OpenAI-compatible tool-calling interface.

We evaluated the local model on 16 test cases.

## Decision

- Use native tool calling rather than asking the model to emit tool names and
  arguments as ordinary JSON.
- Define each tool with a name, description, and JSON Schema parameter block.
- Keep business defaults in application code rather than asking the model to
  invent them.
- Make tool descriptions explicit about when a tool should and should not be
  selected.
- Preserve user-provided product names when extracting `item`.
- Treat tool selection and argument extraction as separate evaluation metrics.
- Do not continue tuning the local model indefinitely; remaining extraction
  errors can be revisited with a stronger hosted model and after the execution
  loop is implemented.

## Evaluation

| Metric | Result |
|---|---:|
| Tool selection | 16/16 (100%) |
| Argument accuracy | 14/16 (88%) |
| Fully correct calls | 14/16 (88%) |

## Interpretation

Tool selection is reliable on the current evaluation set.

The remaining failures are argument-extraction errors rather than tool-routing
errors. The 16-case evaluation set is too small to make claims about general
model performance.

The local model is sufficient for continuing implementation. Model quality
should be evaluated again with a stronger hosted model after the complete
tool-execution loop is implemented.

## Alternatives considered

### JSON classification without tool calling

Rejected because the application would need to interpret model-generated
intent JSON and translate it into tool operations itself.

### Application-side intent routing

Rejected because it would require maintaining increasingly complex linguistic
routing logic outside the model.

### Continue prompt tuning until 16/16

Deferred. Further tuning against a small fixed test set risks overfitting the
prompt to the evaluation cases.