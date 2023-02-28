from http import HTTPStatus
from typing import Any, Final, Optional, Set

from requests import Response

from ..exceptions import LagoApiError
from ..services.json import from_json

RESPONSE_SUCCESS_CODES: Final[Set[int]] = {
    HTTPStatus.OK,  # 200
    HTTPStatus.CREATED,  # 201
    HTTPStatus.ACCEPTED,  # 202
    HTTPStatus.NO_CONTENT,  # 204
}


def _is_status_code_successful(response: Response) -> bool:
    """Check status code."""
    return response.status_code in RESPONSE_SUCCESS_CODES


def _is_content_exists(response: Response) -> bool:
    """Check content is not empty."""
    return bool(response.content)


def verify_response(response: Response) -> Optional[Response]:
    """Verify response."""
    if not _is_status_code_successful(response):
        response_data: Any = from_json(response)
        raise LagoApiError(
            status_code=response.status_code,
            url=response.request.url,
            response=response_data,
            detail=getattr(response_data, 'error', None),
            headers=response.headers,
        )

    if not _is_content_exists(response):
        return None

    return response
