from typing import ClassVar, Optional, Type

from pydantic import BaseModel

from .base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.event import EventResponse
from ..services.json import to_json
from ..services.request import make_url, send_post_request
from ..services.response import verify_response, Response


class EventClient(
    CreateCommandMixin[EventResponse],
    DestroyCommandMixin[EventResponse],
    FindAllCommandMixin[EventResponse],
    FindCommandMixin[EventResponse],
    UpdateCommandMixin[EventResponse],
    BaseClient
):
    API_RESOURCE: ClassVar[str] = 'events'
    RESPONSE_MODEL: ClassVar[Type[EventResponse]] = EventResponse
    ROOT_NAME: ClassVar[str] = 'event'

    def batch_create(self, input_object: BaseModel) -> Optional[bool]:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, 'batch'),
            ),
            data=to_json({
                self.ROOT_NAME: input_object.dict()
            }),
            headers=self.headers(),
        )
        verify_response(api_response)

        return True  # TODO: should return None
