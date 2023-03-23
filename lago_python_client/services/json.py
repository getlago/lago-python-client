from datetime import datetime, date, time
from http import HTTPStatus
import sys
from typing import Any, NoReturn, Tuple, Union
from uuid import UUID

from classes import typeclass
import orjson
from requests import Response

from ..exceptions import LagoApiError

if sys.version_info >= (3, 9):
    from collections.abc import Mapping, Sequence
else:
    from typing import Mapping, Sequence

Serializable = Union[
    str, Mapping[Any, Any], Sequence[Any], Tuple[Any], int, float, bool, datetime, date, time, UUID, None,
]  # And dataclass, TypedDict and ndarray
Deserializable = Union[bytes, bytearray, memoryview, str]
DeserializedData = Union[Mapping[str, Any], Sequence[Any], int, float, str, bool, None]


def to_json(data_container: Serializable) -> str:
    """Serialize data into json format."""
    return orjson.dumps(data_container, option=orjson.OPT_NON_STR_KEYS).decode('utf-8')


@typeclass  # type: ignore
def from_json(json_container) -> DeserializedData:
    """Deserialize data from json format."""
    raise TypeError('Type {0} is not supported'.format(type(json_container)))


@from_json.instance(bytes)  # type: ignore
@from_json.instance(bytearray)
@from_json.instance(memoryview)
@from_json.instance(str)
def _from_json_default(json_container: Deserializable) -> DeserializedData:
    """Deserialize json string."""
    try:
        return orjson.loads(json_container)
    except orjson.JSONDecodeError as exc:
        raise LagoApiError(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,  # 500
            url=None,
            response=None,
            detail=exc.msg,
            headers=None,
        )


@from_json.instance(None)  # type: ignore
def _from_json_none(json_container: None) -> NoReturn:
    """Deserialize json from ``None``."""
    raise LagoApiError(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,  # 500
        url=None,
        response=None,
        detail='Input must be bytes, bytearray, memoryview, or str',
        headers=None,
    )


@from_json.instance(Response)  # type: ignore
def _from_json_requests_response_bytes(json_container: Response) -> DeserializedData:
    """Deserialize json from ``requests.Response`` class instances (from content bytes)."""
    return from_json(json_container.content)  # type: ignore
