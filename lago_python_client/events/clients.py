import sys
from typing import Any, ClassVar, Optional, Type

from pydantic import BaseModel

from ..base_client import BaseClient
from ..fees.clients import FeeClient
from ..mixins import CreateCommandMixin, FindCommandMixin
from ..models.event import EventResponse
from ..models.fee import FeeResponse
from ..services.json import to_json
from ..services.request import make_headers, make_url, send_post_request
from ..services.response import get_response_data, prepare_object_list_response, verify_response, Response

if sys.version_info >= (3, 9):
    from collections.abc import Mapping
else:
    from typing import Mapping


class EventClient(CreateCommandMixin[EventResponse], FindCommandMixin[EventResponse], BaseClient):
    API_RESOURCE: ClassVar[str] = 'events'
    RESPONSE_MODEL: ClassVar[Type[EventResponse]] = EventResponse
    ROOT_NAME: ClassVar[str] = 'event'

    def batch_create(self, input_object: BaseModel) -> None:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, 'batch'),
            ),
            content=to_json({
                self.ROOT_NAME: input_object.dict(),
            }),
            headers=make_headers(api_key=self.api_key),
        )
        verify_response(api_response)

        return None

    def estimate_fees(self, input_object: BaseModel) -> Mapping[str, Any]:
        api_response: Response = send_post_request(
            url= make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, 'estimate_fees'),
            ),
            content=to_json({
                self.ROOT_NAME: input_object.dict(),
            }),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_list_response(
            api_resource=FeeClient.API_RESOURCE,
            response_model=FeeResponse,
            data=get_response_data(response=api_response, key='fees'),
        )
