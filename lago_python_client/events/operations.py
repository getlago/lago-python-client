import sys
from typing import Any, ClassVar, Type

from pydantic import BaseModel

from ..base_operation import BaseOperation
from ..models.event import EventResponse
from ..models.fee import FeeResponse
from ..services.json import to_json
from ..services.request import make_headers, make_url, send_post_request
from ..services.response import get_response_data, prepare_object_list_response, verify_response, Response
from ..shared_operations import CreateCommandMixin, FindCommandMixin

if sys.version_info >= (3, 9):
    from collections.abc import Callable, Mapping
else:
    from typing import Callable, Mapping


class CreateBatchEvents(BaseOperation):
    """Create batch events."""

    API_RESOURCE: ClassVar[str] = 'events'
    RESPONSE_MODEL: ClassVar[Type[EventResponse]] = EventResponse
    ROOT_NAME: ClassVar[str] = 'event'

    def __call__(self, input_object: BaseModel) -> None:
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


class CreateEvent(CreateCommandMixin[EventResponse], BaseOperation):
    """Create a new event."""

    API_RESOURCE: ClassVar[str] = 'events'
    RESPONSE_MODEL: ClassVar[Type[EventResponse]] = EventResponse
    ROOT_NAME: ClassVar[str] = 'event'


class EventEstimateFees(BaseOperation):
    """Estimate fees for an instant charge."""

    API_RESOURCE: ClassVar[str] = 'events'
    RESPONSE_MODEL: ClassVar[Type[EventResponse]] = EventResponse
    ROOT_NAME: ClassVar[str] = 'event'

    def __call__(self, input_object: BaseModel) -> Mapping[str, Any]:
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
            api_resource='fees',
            response_model=FeeResponse,
            data=get_response_data(response=api_response, key='fees'),
        )


class FindEvent(FindCommandMixin[EventResponse], BaseOperation):
    """Find event by transaction ID."""

    API_RESOURCE: ClassVar[str] = 'events'
    RESPONSE_MODEL: ClassVar[Type[EventResponse]] = EventResponse
    ROOT_NAME: ClassVar[str] = 'event'


events_operations_config: Mapping[str, Callable[..., Callable]] = {
    'batch_create': CreateBatchEvents,
    'create': CreateEvent,
    'estimate_fees': EventEstimateFees,
    'find': FindEvent,
}
