import sys
from urllib.parse import urljoin, urlencode
try:
    from typing import Final
except ImportError:  # Python 3.7
    from typing_extensions import Final  # type: ignore

import requests

if sys.version_info >= (3, 9):
    from collections.abc import Mapping, Sequence
else:
    from typing import Mapping, Sequence

URI_TEMPLATE: Final[str] = '{uri_path}{uri_query}'
QUERY_TEMPLATE: Final[str] = '?{query}'


def make_url(*, origin: str, path_parts: Sequence[str], query_pairs: Mapping[str, str] = {}) -> str:
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


send_get_request = requests.get
send_post_request = requests.post
send_put_request = requests.put
send_patch_request = requests.patch
send_delete_request = requests.delete
