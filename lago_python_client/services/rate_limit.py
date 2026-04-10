import time
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from httpx import Response

from ..exceptions import LagoRateLimitError


class RateLimitRetryConfig:
    """Configuration for rate limit retry behavior."""

    def __init__(
        self,
        max_retries: int = 3,
        retry_on_rate_limit: bool = True,
        base_backoff_seconds: float = 1.0,
        backoff_multiplier: float = 2.0,
    ):
        """
        Initialize rate limit retry configuration.

        Args:
            max_retries: Maximum number of retry attempts (0 means no retries).
            retry_on_rate_limit: Whether to automatically retry on 429 responses.
            base_backoff_seconds: Initial backoff duration in seconds for exponential backoff.
            backoff_multiplier: Multiplier for exponential backoff between retries.
        """
        self.max_retries = max_retries
        self.retry_on_rate_limit = retry_on_rate_limit
        self.base_backoff_seconds = base_backoff_seconds
        self.backoff_multiplier = backoff_multiplier

    def calculate_backoff(self, retry_attempt: int) -> float:
        """
        Calculate backoff duration for exponential backoff strategy.

        Args:
            retry_attempt: Current retry attempt number (0-based).

        Returns:
            Duration in seconds to wait before retrying.
        """
        return self.base_backoff_seconds * (self.backoff_multiplier ** retry_attempt)


def handle_rate_limit_response(
    response: "Response",
    config: RateLimitRetryConfig,
    retry_attempt: int,
) -> float:
    """
    Determine if and how long to wait before retrying a rate-limited request.

    Args:
        response: The HTTP response object (should be 429).
        config: Rate limit retry configuration.
        retry_attempt: Current retry attempt number (0-based).

    Returns:
        Duration in seconds to wait before retrying, or raises LagoRateLimitError.

    Raises:
        LagoRateLimitError: If retry is not configured or max retries exceeded.
    """
    # Check if retries are enabled
    if not config.retry_on_rate_limit:
        raise LagoRateLimitError(
            status_code=response.status_code,
            url=str(response.request.url),
            response=None,
            headers=response.headers,
        )

    # Check if we've exceeded max retries
    if retry_attempt >= config.max_retries:
        raise LagoRateLimitError(
            status_code=response.status_code,
            url=str(response.request.url),
            response=None,
            headers=response.headers,
        )

    # Try to get reset time from header
    reset_seconds: Optional[int] = None
    if "x-ratelimit-reset" in response.headers:
        try:
            reset_seconds = int(response.headers["x-ratelimit-reset"])
        except (ValueError, TypeError):
            pass

    # Use header value if available, otherwise use exponential backoff
    if reset_seconds is not None:
        return float(reset_seconds)
    else:
        return config.calculate_backoff(retry_attempt)


def is_rate_limit_response(response: "Response") -> bool:
    """
    Check if a response indicates rate limit exceeded.

    Args:
        response: The HTTP response to check.

    Returns:
        True if response is a 429 Too Many Requests, False otherwise.
    """
    return response.status_code == 429


def wait_for_retry(duration: float) -> None:
    """
    Sleep for the specified duration before retrying.

    Args:
        duration: Number of seconds to wait.
    """
    if duration > 0:
        time.sleep(duration)
