from datetime import datetime, date, time
from functools import singledispatch
from typing import Any, Dict, List, Tuple, Union
from uuid import UUID

import orjson
from requests import Response

Serializable = Union[str, Dict[Any, Any], List[Any], Tuple[Any], int, float, bool, datetime, date, time, UUID, None]  # And dataclass, TypedDict and ndarray
Deserializable = Union[bytes, bytearray, memoryview, str]
DeserializedData = Union[Dict[str, Any], List[Any], int, float, str, bool, None]


def to_json(data_container: Serializable) -> str:
    """Serialize data into json format."""
    return orjson.dumps(data_container, option=orjson.OPT_NON_STR_KEYS).decode('utf-8')


@singledispatch
def from_json(json_container) -> DeserializedData:
    """Deserialize data from json format."""
    raise TypeError('Type {0} is not supported'.format(type(json_container)))


@from_json.register
def _from_json_default(json_container: Deserializable) -> DeserializedData:
    """Deserialize json string."""
    return orjson.loads(json_container)


@from_json.register
def _from_json_requests_response_bytes(json_container: Response) -> DeserializedData:
    """Deserialize json from ``requests.Response`` class instances (from content bytes)."""
    return from_json(json_container.content)
