# Later

## Intent coverage

- Add `product_search` and `discount_query` intents, then re-measure intent
  accuracy to determine how much of the remaining error is caused by missing
  intent coverage.

## Evaluation

- Replace the 10-case manual evaluation with a proper evaluation harness on
  Day 15, including a larger test set, per-intent metrics, and regression
  tracking.


## Deferred

- Re-evaluate remaining tool-argument failures with a stronger hosted model.
- Re-run the tool-calling evaluation after implementing the complete
  tool-execution loop.
- Expand the 16-case tool-calling evaluation into a proper evaluation harness.
- Add more ambiguous and adversarial tool-selection cases.
- Measure tool-calling latency and token usage across local and hosted models.


- Clarify in `GET_UPDATE_STOCK_SCHEMA` that the tool modifies inventory data and should only be called for explicit stock-change requests.

- Improve tool result schemas so the model has enough information to produce grounded final answers. For example, `update_stock` currently returns only `quantity_change`, which can cause the model to infer an incorrect current quantity. Return `previous_quantity` and `new_quantity` once real database-backed tools are implemented.