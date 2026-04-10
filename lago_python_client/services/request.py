from typing import Any, Callable, Optional, TypeVar, Union

try:
    from typing import Final
except ImportError:  # Python 3.7
    from typing_extensions import Final  # type: ignore
from collections.abc import Mapping, Sequence
from urllib.parse import urlencode, urljoin

import httpx

from ..version import LAGO_VERSION
from .rate_limit import (
    RateLimitRetryConfig,
    handle_rate_limit_response,
    is_rate_limit_response,
    wait_for_retry,
)

T = TypeVar("T")

URI_TEMPLATE: Final[str] = "{uri_path}{uri_query}"
QUERY_TEMPLATE: Final[str] = "?{query}"

QueryPairs = Union[Mapping[str, Union[int, str, list[str]]], Sequence[tuple[str, Union[int, str]]]]


def make_url(
    *,
    origin: str,
    path_parts: Sequence[str],
    query_pairs: QueryPairs = None,
) -> str:
    """Return url."""
    if query_pairs is None:
        query_pairs = {}
    return urljoin(
        origin,
        URI_TEMPLATE.format(
            uri_path="/".join(path_parts),
            uri_query=QUERY_TEMPLATE.format(
                query=urlencode(query_pairs, doseq=True),
            )
            if query_pairs
            else "",
        ),
    )


def make_headers(*, api_key: str) -> Mapping[str, str]:
    """Return headers."""
    return {
        "Content-type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "User-agent": f"Lago Python v{LAGO_VERSION}",
    }


def _create_retry_wrapper(
    http_method: Callable[..., httpx.Response],
) -> Callable[..., httpx.Response]:
    """
    Create a wrapper around an httpx HTTP method that retries on rate limit (429).

    Args:
        http_method: The httpx HTTP method to wrap (e.g., httpx.get, httpx.post).

    Returns:
        A wrapped version of the HTTP method that handles rate limit retries.
    """

    def retry_wrapper(
        url: str,
        *,
        rate_limit_retry_config: Optional[RateLimitRetryConfig] = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """
        Execute HTTP request with automatic retry on rate limit (429) responses.

        Args:
            url: The request URL.
            rate_limit_retry_config: Configuration for rate limit retry behavior.
                Defaults to a configuration with max_retries=3.
            **kwargs: Additional arguments to pass to the underlying httpx method.

        Returns:
            The HTTP response.

        Raises:
            LagoRateLimitError: If rate limit is exceeded and retries exhausted.
            httpx.RequestError: For other HTTP errors.
        """
        if rate_limit_retry_config is None:
            rate_limit_retry_config = RateLimitRetryConfig()

        retry_attempt = 0
        while True:
            response = http_method(url, **kwargs)

            # If not rate limited, return the response
            if not is_rate_limit_response(response):
                return response

            # Handle rate limit - may raise LagoRateLimitError or return wait duration
            wait_duration = handle_rate_limit_response(
                response,
                rate_limit_retry_config,
                retry_attempt,
            )

            # Wait and retry
            wait_for_retry(wait_duration)
            retry_attempt += 1

    return retry_wrapper


# Create wrapped versions of httpx methods with rate limit retry support
send_get_request = _create_retry_wrapper(httpx.get)
send_post_request = _create_retry_wrapper(httpx.post)
send_put_request = _create_retry_wrapper(httpx.put)
send_patch_request = _create_retry_wrapper(httpx.patch)
send_delete_request = _create_retry_wrapper(httpx.delete)
