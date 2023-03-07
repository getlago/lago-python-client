from typing import Dict, Final, Sequence
from urllib.parse import urljoin, urlencode

URI_TEMPLATE: Final[str] = '{uri_path}{uri_query}'
QUERY_TEMPLATE: Final[str] = '?{query}'


def make_url(*, scheme_plus_authority: str, path_parts: Sequence[str], query_pairs: Dict[str, str] = {}) -> str:
    """Return url."""
    return urljoin(
        scheme_plus_authority,
        URI_TEMPLATE.format(
            uri_path='/'.join(path_parts),
            uri_query=QUERY_TEMPLATE.format(
                query=urlencode(query_pairs),
            ) if query_pairs else '',
        ),
    )
