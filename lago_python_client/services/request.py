from typing import Any, Callable, Optional, Union
import time

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
    emit_rate_limit_info,
    handle_rate_limit_response,
    is_rate_limit_response,
    wait_for_retry,
)

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
    Create a wrapper around an httpx HTTP method that retries on rate limit (429)
    AND transient network/server errors (Exponential Backoff).
    """

    def retry_wrapper(
        url: str,
        *,
        rate_limit_retry_config: Optional[RateLimitRetryConfig] = None,
        **kwargs: Any,
    ) -> httpx.Response:
        if rate_limit_retry_config is None:
            rate_limit_retry_config = RateLimitRetryConfig()

        method_name = http_method.__name__.upper()
        retry_attempt = 0

        # --- ASHFIR V3 INSPIRED NETWORK RETRY CONFIG ---
        network_retry_attempt = 0
        max_network_retries = 3
        network_delay = 1.0  # İlk hata sonrası 1 saniye bekle
        # -----------------------------------------------

        while True:
            try:
                response = http_method(url, **kwargs)

                # Sunucu geçici hata verdiyse (502, 503, 504), manuel olarak HTTPStatusError fırlat
                if response.status_code in [502, 503, 504]:
                    raise httpx.HTTPStatusError(
                        message=f"Server error: {response.status_code}",
                        request=response.request,
                        response=response,
                    )

            except (httpx.RequestError, httpx.TimeoutException, httpx.HTTPStatusError) as e:
                # Eğer hata bir HTTPStatusError ise ve 429 (Rate Limit) ise üstteki mantığı bozma, aşağı pasla
                if isinstance(e, httpx.HTTPStatusError) and e.response.status_code == 429:
                    response = e.response
                else:
                    # Genel ağ hatası veya sunucu çökmesi durumu: Exponential Backoff'u tetikle!
                    if network_retry_attempt < max_network_retries:
                        time.sleep(network_delay)
                        network_delay *= 2  # Üstel geri çekilme (1s -> 2s -> 4s)
                        network_retry_attempt += 1
                        retry_attempt += 1  # Rate limit takibi istatistiklerini yanıltmamak için senkronize et
                        continue
                    else:
                        raise e  # Denemeler tükendiyse hatayı fırlat

            # If not rate limited, emit observability info and return the response
            if not is_rate_limit_response(response):
                emit_rate_limit_info(
                    response,
                    rate_limit_retry_config,
                    method=method_name,
                    url=url,
                )
                return response

            # Handle rate limit - may raise LagoRateLimitError or return wait duration
            wait_duration = handle_rate_limit_response(
                response,
                rate_limit_retry_config,
                retry_attempt,
            )

            # Wait and retry (Rate limit için)
            wait_for_retry(wait_duration)
            retry_attempt += 1

    return retry_wrapper


# Create wrapped versions of httpx methods with rate limit retry support
send_get_request = _create_retry_wrapper(httpx.get)
send_post_request = _create_retry_wrapper(httpx.post)
send_put_request = _create_retry_wrapper(httpx.put)
send_patch_request = _create_retry_wrapper(httpx.patch)
send_delete_request = _create_retry_wrapper(httpx.delete)
