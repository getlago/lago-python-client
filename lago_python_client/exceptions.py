from collections.abc import MutableMapping
from http import HTTPStatus
from typing import Any, Optional


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
        super().__init__(self.response)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(response={self.response!r}"


class LagoRateLimitError(LagoApiError):
    """Exception raised when rate limit is exceeded (HTTP 429)."""

    def __init__(
        self,
        status_code: int,
        url: Optional[str],
        response: Any,
        detail: Optional[str] = None,
        headers: Optional[MutableMapping[str, str]] = None,
    ) -> None:
        super().__init__(
            status_code=status_code,
            url=url,
            response=response,
            detail=detail,
            headers=headers,
        )
        # Parse rate limit headers
        self.limit: Optional[int] = None
        self.remaining: Optional[int] = None
        self.reset: Optional[int] = None

        if headers:
            try:
                self.limit = int(headers["x-ratelimit-limit"])
            except (KeyError, ValueError, TypeError):
                pass
            try:
                self.remaining = int(headers["x-ratelimit-remaining"])
            except (KeyError, ValueError, TypeError):
                pass
            try:
                self.reset = int(headers["x-ratelimit-reset"])
            except (KeyError, ValueError, TypeError):
                pass

    def __repr__(self) -> str:
        return (
            f"LagoRateLimitError(limit={self.limit}, remaining={self.remaining}, "
            f"reset={self.reset}, url={self.url!r})"
        )
