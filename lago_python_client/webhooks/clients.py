import base64
from http import HTTPStatus
import sys
from typing import Any, ClassVar, Optional, Type, Union
try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict

from pydantic import BaseModel
import typeguard

from ..base_client import BaseClient
from ..exceptions import LagoApiError
from ..services.request import make_headers, make_url, send_get_request
from ..services.response import get_response_data, Response

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
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, 'json_public_key'),
            ),
            headers=make_headers(api_key=self.api_key),
        )
        response_data: Optional[Union[Mapping[str, Any], Sequence[Any]]] = get_response_data(response=api_response, key=self.ROOT_NAME)

        try:
            checked_response_data: _ResponseWithPublicKeyInside = typeguard.check_type(response_data, _ResponseWithPublicKeyInside)  # type: ignore
        except typeguard.TypeCheckError:
            raise LagoApiError(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,  # 500
                url=None,
                response=None,
                detail='Incorrect response data',
                headers=None,
            )

        return base64.b64decode(checked_response_data['public_key'])
