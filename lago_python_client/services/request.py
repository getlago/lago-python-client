from typing import Union

try:
    from typing import Final
except ImportError:  # Python 3.7
    from typing_extensions import Final  # type: ignore
from collections.abc import Mapping, Sequence
from urllib.parse import urlencode, urljoin

import httpx

from ..version import LAGO_VERSION

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


send_get_request = httpx.get
send_post_request = httpx.post
send_put_request = httpx.put
send_patch_request = httpx.patch
send_delete_request = httpx.delete
