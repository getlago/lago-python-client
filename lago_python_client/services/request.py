from typing import Dict, Sequence
from urllib.parse import urljoin, urlencode
try:
    from typing import Final
except ImportError:  # Python 3.7
    from typing_extensions import Final

URI_TEMPLATE: Final[str] = '{uri_path}{uri_query}'
QUERY_TEMPLATE: Final[str] = '?{query}'


def make_url(*, origin: str, path_parts: Sequence[str], query_pairs: Dict[str, str] = {}) -> str:
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
