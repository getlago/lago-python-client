from typing import Any, Final, Optional, Sequence

from requests import Response

from ..exceptions import LagoApiError
from ..services.json import from_json

RESPONSE_SUCCESS_CODES: Final[Sequence[int]] = [200, 201, 202, 204]


def verify_response(response: Response) -> Optional[Response]:
    """Verify response. Return response on success. Raise exception otherwise."""
    if response.status_code in RESPONSE_SUCCESS_CODES:
        if response.content:
            return response
        else:
            return None
    else:
        if response.content:
            response_data: Any = from_json(response)
            detail: Optional[str] = getattr(response_data, 'error', None)
        else:
            response_data = None
            detail = None
        raise LagoApiError(
            status_code=response.status_code,
            url=response.request.url,
            response=response_data,
            detail=detail,
            headers=response.headers,
        )
