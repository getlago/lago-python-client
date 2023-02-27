from http import HTTPStatus
import sys
from typing import Any, Optional

if sys.version_info < (3, 9):
    from typing import MutableMapping
else:
    from collections.abc import MutableMapping


class LagoApiError(Exception):
    def __init__(
        self,
        status_code: int,
        url: Optional[str],
        response: Any,
        detail: Optional[str] = None,
        headers: Optional[MutableMapping[str, str]] = None,
    ) -> None:
        if detail is None:
            detail = HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.url = url
        self.response = response
        self.detail = detail
        self.headers = headers

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})"
