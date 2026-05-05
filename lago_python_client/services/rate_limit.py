import logging
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:
    from httpx import Response

from ..exceptions import LagoRateLimitError

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RateLimitInfo:
    """
    Parsed rate limit headers from a Lago API response.

    Provided to ``on_rate_limit_info`` callbacks after every successful request
    so callers can build their own observability (metrics, logs, alerts).
    """

    limit: Optional[int]
    remaining: Optional[int]
    reset: Optional[int]
    url: str
    method: str

    @property
    def usage_pct(self) -> Optional[float]:
        """
        Fraction of the rate limit currently used, between 0.0 and 1.0.

        Returns None when the headers aren't usable (missing, zero limit, etc.).
        """
        if self.limit is None or self.remaining is None or self.limit <= 0:
            return None
        return 1.0 - (self.remaining / self.limit)


RateLimitCallback = Callable[[RateLimitInfo], None]


def parse_rate_limit_info(
    response: "Response",
    method: str,
    url: str,
) -> Optional[RateLimitInfo]:
    """
    Parse ``x-ratelimit-*`` headers from a response into a RateLimitInfo.

    Returns ``None`` when no rate limit headers are present (for example, on a
    self-hosted Lago instance that doesn't enforce limits) so callers can skip
    emission entirely.
    """
    headers = response.headers
    limit: Optional[int] = None
    remaining: Optional[int] = None
    reset: Optional[int] = None

    try:
        limit = int(headers["x-ratelimit-limit"])
    except (KeyError, ValueError, TypeError):
        pass
    try:
        remaining = int(headers["x-ratelimit-remaining"])
    except (KeyError, ValueError, TypeError):
        pass
    try:
        reset = int(headers["x-ratelimit-reset"])
    except (KeyError, ValueError, TypeError):
        pass

    if limit is None and remaining is None and reset is None:
        return None

    return RateLimitInfo(
        limit=limit,
        remaining=remaining,
        reset=reset,
        url=url,
        method=method,
    )


class RateLimitRetryConfig:
    """Configuration for rate limit retry behavior."""

    def __init__(
        self,
        max_retries: int = 3,
        retry_on_rate_limit: bool = True,
        base_backoff_seconds: float = 1.0,
        backoff_multiplier: float = 2.0,
        max_retry_delay: float = 20.0,
        on_rate_limit_info: Optional[RateLimitCallback] = None,
    ):
        """
        Initialize rate limit retry configuration.

        Args:
            max_retries: Maximum number of retry attempts (0 means no retries).
            retry_on_rate_limit: Whether to automatically retry on 429 responses.
            base_backoff_seconds: Initial backoff duration in seconds for exponential backoff.
            backoff_multiplier: Multiplier for exponential backoff between retries.
            max_retry_delay: Maximum delay in seconds before a retry (default: 20).
            on_rate_limit_info: Optional callback invoked after every successful
                response with parsed rate limit headers. Use this to build
                observability around the rate limit (warn at 80%, emit metrics,
                etc.). Exceptions raised from the callback are logged and
                swallowed so they never break the request flow.
        """
        self.max_retries = max_retries
        self.retry_on_rate_limit = retry_on_rate_limit
        self.base_backoff_seconds = base_backoff_seconds
        self.backoff_multiplier = backoff_multiplier
        self.max_retry_delay = max_retry_delay
        self.on_rate_limit_info = on_rate_limit_info

    def calculate_backoff(self, retry_attempt: int) -> float:
        """
        Calculate backoff duration for exponential backoff strategy.

        Args:
            retry_attempt: Current retry attempt number (0-based).

        Returns:
            Duration in seconds to wait before retrying.
        """
        return self.base_backoff_seconds * (self.backoff_multiplier**retry_attempt)


def emit_rate_limit_info(
    response: "Response",
    config: "RateLimitRetryConfig",
    method: str,
    url: str,
) -> None:
    """
    Invoke the ``on_rate_limit_info`` callback if configured.

    Parses rate limit headers off the response and hands them to the user's
    callback. Any exception raised from the callback is logged and swallowed so
    a buggy observer never breaks the underlying request.
    """
    if config.on_rate_limit_info is None:
        return

    info = parse_rate_limit_info(response, method=method, url=url)
    if info is None:
        return

    try:
        config.on_rate_limit_info(info)
    except Exception:
        logger.exception("on_rate_limit_info callback raised; suppressing")


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
        delay = float(reset_seconds)
    else:
        delay = config.calculate_backoff(retry_attempt)

    # Cap at max_retry_delay
    return min(delay, config.max_retry_delay)


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
