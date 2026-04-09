"""Retry transient HTTP/connection failures (extend RETRYABLE for other calls)."""
import logging
import ssl
from typing import Callable, Tuple, Type, TypeVar

import urllib3.exceptions

T = TypeVar("T")

# Add exception types here when wrapping more API calls.
RETRYABLE: Tuple[Type[BaseException], ...] = (
    urllib3.exceptions.ProtocolError,
    urllib3.exceptions.MaxRetryError,
    ConnectionError,
    TimeoutError,
    ssl.SSLError,
)


def with_http_retries(
    fn: Callable[[], T],
    max_attempts: int = 3,
    label: str = "Request",
) -> T:
    """Run fn up to max_attempts times; log each failure; re-raise the last error."""
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except RETRYABLE as exc:
            logging.error("%s failed (attempt %s/%s): %s", label, attempt, max_attempts, exc)
            if attempt == max_attempts:
                raise
