from collections.abc import Mapping
from typing import Any, ClassVar, Optional, Type

import httpx

from lago_python_client.base_model import BaseModel

from ..base_client import BaseClient
from ..fees.clients import FeeClient
from ..mixins import FindCommandMixin
from ..models.event import EventResponse
from ..models.fee import FeeResponse
from ..services.json import to_json
from ..services.request import make_headers, make_url, send_post_request
from ..services.response import (
    Response,
    get_response_data,
    prepare_object_list_response,
    prepare_object_response,
    verify_response,
)


class EventClient(FindCommandMixin[EventResponse], BaseClient):
    API_RESOURCE: ClassVar[str] = "events"
    RESPONSE_MODEL: ClassVar[Type[EventResponse]] = EventResponse
    ROOT_NAME: ClassVar[str] = "event"

    def create(self, input_object: BaseModel, timeout: Optional[httpx.Timeout] = None) -> Optional[EventResponse]:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_ingest_url,
                path_parts=(self.API_RESOURCE,),
            ),
            content=to_json(
                {
                    self.ROOT_NAME: input_object.dict(),
                }
            ),
            headers=make_headers(api_key=self.api_key),
            timeout=timeout,
        )

        # Process response data
        response_data = get_response_data(response=api_response, key=self.ROOT_NAME)
        if not response_data:
            return None

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=response_data,
        )

    def batch_create(self, input_object: BaseModel) -> None:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, "batch"),
            ),
            content=to_json(input_object.dict()),
            headers=make_headers(api_key=self.api_key),
        )
        verify_response(api_response)

    def estimate_fees(self, input_object: BaseModel) -> Mapping[str, Any]:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, "estimate_fees"),
            ),
            content=to_json(
                {
                    self.ROOT_NAME: input_object.dict(),
                }
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_list_response(
            api_resource=FeeClient.API_RESOURCE,
            response_model=FeeResponse,
            data=get_response_data(response=api_response, key="fees"),
        )
