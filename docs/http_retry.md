# HTTP retries for test run creation

## Why

In CI (e.g. GitHub Actions), calls to the Test IT API sometimes fail during TLS or the TCP connection (`Connection reset by peer`, `urllib3.exceptions.ProtocolError`). Retries on empty test run creation reduce flakiness from short-lived network issues.

## What changed

| Piece | Description |
|-------|-------------|
| `src/testit_cli/http_retry.py` | `RETRYABLE` tuple (exception types worth retrying) and `with_http_retries`. |
| `src/testit_cli/apiclient.py` | `create_empty` is wrapped in `with_http_retries` with label `Create test run`. |

## Behaviour

- Up to **3** attempts (initial call + two retries).
- Each failure is logged at **ERROR** (operation label, attempt number, exception).
- After the third failure the exception is **re-raised**; CLI exits with an error as before.
- **4xx/5xx** and exceptions **not** in `RETRYABLE` are **not** retried.

## Where it applies

Any code path that uses `ApiClient.create_test_run`:

- `testit testrun create`
- import flow when a test run is auto-created (no `testrun_id`)

## Extending to other API calls

1. Add exception types to **`RETRYABLE`** in `http_retry.py` if needed.
2. Wrap the call:

```python
with_http_retries(
    lambda: self.__some_api.some_method(...),
    label="Human-readable operation name",
)
```

`max_attempts` defaults to `3`; pass it explicitly if you need a different value.
