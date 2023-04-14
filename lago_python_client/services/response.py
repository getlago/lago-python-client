from http import HTTPStatus
import sys
from typing import Any, Optional, Set, Type, TypeVar, Union
try:
    from typing import assert_never
except ImportError:  # Python 3.7, 3.8, 3.9, 3.10
    from typing_extensions import assert_never
try:
    from typing import Final
except ImportError:  # Python 3.7
    from typing_extensions import Final  # type: ignore

from httpx import Response as Response  # not a typo! implicit reexport
from pydantic import BaseModel
import typeguard

from ..exceptions import LagoApiError
from ..services.json import DeserializedData, from_json

if sys.version_info >= (3, 9):
    from collections.abc import Mapping, Sequence
else:
    from typing import Mapping, Sequence

_M = TypeVar("_M", bound=BaseModel)

typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS

RESPONSE_SUCCESS_CODES: Final[Set[int]] = {
    HTTPStatus.OK,  # 200
    HTTPStatus.CREATED,  # 201
    HTTPStatus.ACCEPTED,  # 202
    HTTPStatus.NO_CONTENT,  # 204
}

_MappingOrSequence = Union[Mapping[str, Any], Sequence[Any]]


def _is_status_code_successful(response: Response) -> bool:
    """Check status code."""
    return response.status_code in RESPONSE_SUCCESS_CODES


def _is_content_exists(response: Response) -> bool:
    """Check content is not empty."""
    return bool(response.content)


def verify_response(response: Response) -> Optional[Response]:
    """Verify response."""
    if not _is_status_code_successful(response):
        response_data: Any = from_json(response)  # type: ignore
        raise LagoApiError(
            status_code=response.status_code,
            url=str(response.request.url),
            response=response_data,
            detail=getattr(response_data, 'error', None),
            headers=response.headers,
        )

    if not _is_content_exists(response):
        return None

    return response


def get_response_data(*, response: Response, key: str = '') -> Optional[_MappingOrSequence]:
    """Return verified and unpacked response data."""
    response_or_None: Optional[Response] = verify_response(response)
    if not response_or_None:
        return None
    deserialized_data: DeserializedData = from_json(response_or_None)  # type: ignore

    # Ensure deserialized_data has correct type: sequence or mapping or raise LagoApiError
    try:
        mapping_or_sequence_data = typeguard.check_type(deserialized_data, _MappingOrSequence)
    except typeguard.TypeCheckError as exc:
        raise LagoApiError(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,  # 500
            url=None,
            response=None,
            detail=str(exc),
            headers=None,
        )

    if isinstance(mapping_or_sequence_data, Mapping):
        return mapping_or_sequence_data.get(key, {}) if key else mapping_or_sequence_data
    elif isinstance(mapping_or_sequence_data, Sequence):
        return mapping_or_sequence_data
    else:
        assert_never(mapping_or_sequence_data)


def prepare_object_response(response_model: Type[_M], data: Optional[_MappingOrSequence]) -> _M:
    """Return single object response - Pydantic model instance with provided data."""
    if not data:
        raise LagoApiError(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,  # 500
            url=None,
            response=None,
            detail='Data is required to create instance of {model}'.format(model=response_model),
            headers=None,
        )

    return response_model.parse_obj(data)


def prepare_index_response(api_resource: str, response_model: Type[_M], data: Optional[_MappingOrSequence]) -> Mapping[str, Any]:
    """Return index response with meta based on mapping data object."""
    # Ensure deserialized_data has correct type: mapping with mapping or sequence inside or raise LagoApiError

    try:
        response_data: Mapping[str, _MappingOrSequence] = typeguard.check_type(data, Mapping[str, _MappingOrSequence])
    except typeguard.TypeCheckError as exc:
        raise LagoApiError(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,  # 500
            url=None,
            response=None,
            detail=str(exc),
            headers=None,
        )

    return {
        api_resource: [
            prepare_object_response(response_model=response_model, data=el)
            for el in response_data[api_resource]
        ],
        'meta': response_data['meta'],
    }


def prepare_object_list_response(
        api_resource: str,
        response_model: Type[_M],
        data: Optional[Union[Mapping[str, object], Sequence[object]]],
) -> Mapping[str, Any]:
    """Return response based on sequence of data objects."""
    # The only usage - ``WalletTransactionClient.create``
    # Ensure deserialized_data has correct type: sequence with mapping or sequence inside or raise LagoApiError
    try:
        response_data: Sequence[_MappingOrSequence] = typeguard.check_type(data, Sequence[_MappingOrSequence])
    except typeguard.TypeCheckError as exc:
        raise LagoApiError(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,  # 500
            url=None,
            response=None,
            detail=str(exc),
            headers=None,
        )

    return {
        api_resource: [
            prepare_object_response(response_model=response_model, data=el)
            for el in response_data
        ],
    }
