from typing import ClassVar, Optional, Type, Union

from ..base_client import BaseClient
from ..mixins import CreateCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.credit_note import CreditNoteResponse, CreditNoteEstimatedResponse, CreditNoteEstimate
from ..services.json import to_json
from ..services.request import make_headers, make_url, send_post_request, send_put_request
from ..services.response import get_response_data, prepare_object_response, Response


class CreditNoteClient(
    CreateCommandMixin[CreditNoteResponse],
    FindAllCommandMixin[CreditNoteResponse],
    FindCommandMixin[CreditNoteResponse],
    UpdateCommandMixin[CreditNoteResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'credit_notes'
    ESTIMATE_API_RESOURCE: ClassVar[str] = 'estimated_credit_note'
    RESPONSE_MODEL: ClassVar[Type[CreditNoteResponse]] = CreditNoteResponse
    ROOT_NAME: ClassVar[str] = 'credit_note'

    def download(self, resource_id: str) -> Optional[CreditNoteResponse]:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, 'download'),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        response_data = get_response_data(response=api_response, key=self.ROOT_NAME)
        if not response_data:
            return None

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=response_data,
        )

    def void(self, resource_id: str) -> CreditNoteResponse:
        api_response: Response = send_put_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, 'void'),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )

    def estimate(self, input_object: CreditNoteEstimate) -> CreditNoteEstimatedResponse:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, 'estimate'),
            ),
            content=to_json({
                self.ROOT_NAME: input_object.dict(),
            }),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=CreditNoteEstimatedResponse,
            data=get_response_data(response=api_response, key=self.ESTIMATE_API_RESOURCE),
        )
