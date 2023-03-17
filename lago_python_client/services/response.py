from http import HTTPStatus
import sys
from typing import Any, Optional, Set, Type
try:
    from typing import Final
except ImportError:  # Python 3.7
    from typing_extensions import Final

from pydantic import BaseModel
from requests import Response

from ..exceptions import LagoApiError
from ..services.json import from_json

if sys.version_info >= (3, 9):
    from collections.abc import Mapping, Sequence
else:
    from typing import Mapping, Sequence

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


def prepare_object_response(response_model: Type[BaseModel], data: Mapping[Any, Any]) -> BaseModel:
    """Return single object response - Pydantic model instance with provided data."""
    return response_model.parse_obj(data)


def prepare_index_response(api_resourse: str, response_model: Type[BaseModel], data: Mapping[str, Any]) -> Mapping[str, Any]:
    """Return index response with meta based on mapping data object."""
    return {
        api_resourse: [
            prepare_object_response(response_model=response_model, data=el)
            for el in data[api_resourse]
        ],
        'meta': data['meta'],
    }


def prepare_create_response(api_resource: str, response_model: Type[BaseModel], data: Sequence[Mapping[Any, Any]]) -> Mapping[str, Any]:
    """Return response based on sequence of data objects."""
    # The only usage - ``WalletTransactionClient.create``
    return {
        api_resource: [
            prepare_object_response(response_model=response_model, data=el)
            for el in data
        ],
    }
