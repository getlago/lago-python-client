import base64
from http import HTTPStatus
import sys
from typing import Any, ClassVar, Optional, Type, Union
try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict

from pydantic import BaseModel
import requests
from requests import Response
import typeguard

from .base_client import BaseClient
from ..exceptions import LagoApiError
from ..services.request import make_url
from ..services.response import get_response_data

if sys.version_info >= (3, 9):
    from collections.abc import Mapping, Sequence
else:
    from typing import Mapping, Sequence

typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS


class _ResponseWithPublicKeyInside(TypedDict):
    public_key: str


class WebhookClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'webhooks'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = NotImplemented
    ROOT_NAME: ClassVar[str] = 'webhook'

    def public_key(self) -> bytes:
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, 'json_public_key'),
        )
        api_response: Response = requests.get(query_url, headers=self.headers())
        response_data: Optional[Union[Mapping[str, Any], Sequence[Any]]] = get_response_data(response=api_response, key=self.ROOT_NAME)

        try:
            checked_response_data: _ResponseWithPublicKeyInside = typeguard.check_type(response_data, _ResponseWithPublicKeyInside)
        except typeguard.TypeCheckError:
            raise LagoApiError(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,  # 500
                url=None,
                response=None,
                detail='Incorrect response data',
                headers=None,
            )

        return base64.b64decode(checked_response_data['public_key'])
