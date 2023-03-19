import requests
from typing import ClassVar, Optional, Type, Union

from requests import Response

from .base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.credit_note import CreditNoteResponse
from ..services.request import make_url
from ..services.response import get_response_data, prepare_object_response


class CreditNoteClient(
    CreateCommandMixin[CreditNoteResponse],
    DestroyCommandMixin[CreditNoteResponse],
    FindAllCommandMixin[CreditNoteResponse],
    FindCommandMixin[CreditNoteResponse],
    UpdateCommandMixin[CreditNoteResponse],
    BaseClient
):
    API_RESOURCE: ClassVar[str] = 'credit_notes'
    RESPONSE_MODEL: ClassVar[Type[CreditNoteResponse]] = CreditNoteResponse
    ROOT_NAME: ClassVar[str] = 'credit_note'

    def download(self, resource_id: str) -> Union[Optional[CreditNoteResponse], bool]:
        api_response: Response = requests.post(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, 'download'),
            ),
            headers=self.headers(),
        )

        response_data = get_response_data(response=api_response, key=self.ROOT_NAME)
        if not response_data:
            return True  # TODO: should return None

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=response_data,
        )

    def void(self, resource_id: str) -> CreditNoteResponse:
        api_response: Response = requests.put(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, 'void'),
            ),
            headers=self.headers(),
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )
