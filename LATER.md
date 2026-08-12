# Later

## Intent coverage

- Add `product_search` and `discount_query` intents, then re-measure intent
  accuracy to determine how much of the remaining error is caused by missing
  intent coverage.

## Ambiguity handling

- Add an explicit ambiguous → `unknown` example to the system prompt and
  test whether it improves classification of ambiguous in-scope requests.

## Evaluation

- Replace the 10-case manual evaluation with a proper evaluation harness on
  Day 15, including a larger test set, per-intent metrics, and regression
  tracking.