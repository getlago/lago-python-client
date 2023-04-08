import sys
from typing import Union
try:
    from typing import Final
except ImportError:  # Python 3.7
    from typing_extensions import Final  # type: ignore
from urllib.parse import urljoin, urlencode

import httpx

from ..version import LAGO_VERSION

if sys.version_info >= (3, 9):
    from collections.abc import Mapping, Sequence
else:
    from typing import Mapping, Sequence

URI_TEMPLATE: Final[str] = '{uri_path}{uri_query}'
QUERY_TEMPLATE: Final[str] = '?{query}'


def make_url(*, origin: str, path_parts: Sequence[str], query_pairs: Mapping[str, Union[int, str]] = {}) -> str:
    """Return url."""
    return urljoin(
        origin,
        URI_TEMPLATE.format(
            uri_path='/'.join(path_parts),
            uri_query=QUERY_TEMPLATE.format(
                query=urlencode(query_pairs),
            ) if query_pairs else '',
        ),
    )


def make_headers(*, api_key: str) -> Mapping[str, str]:
    """Return headers."""
    return {
        'Content-type': 'application/json',
        'Authorization': "Bearer {api_key}".format(api_key=api_key),
        'User-agent': 'Lago Python v{version}'.format(version=LAGO_VERSION),
    }


send_get_request = httpx.get
send_post_request = httpx.post
send_put_request = httpx.put
send_delete_request = httpx.delete
