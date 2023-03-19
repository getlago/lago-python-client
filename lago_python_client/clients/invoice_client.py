import requests
from typing import ClassVar, Optional, Type, Union

from requests import Response

from .base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.invoice import InvoiceResponse
from ..services.request import make_url
from ..services.response import get_response_data, prepare_object_response


class InvoiceClient(
    CreateCommandMixin[InvoiceResponse],
    DestroyCommandMixin[InvoiceResponse],
    FindAllCommandMixin[InvoiceResponse],
    FindCommandMixin[InvoiceResponse],
    UpdateCommandMixin[InvoiceResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'invoices'
    RESPONSE_MODEL: ClassVar[Type[InvoiceResponse]] = InvoiceResponse
    ROOT_NAME: ClassVar[str] = 'invoice'

    def download(self, resource_id: str) -> Union[Optional[InvoiceResponse], bool]:
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

    def retry_payment(self, resource_id: str) -> InvoiceResponse:
        api_response: Response = requests.post(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, 'retry_payment'),
            ),
            headers=self.headers(),
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )

    def refresh(self, resource_id: str) -> InvoiceResponse:
        api_response: Response = requests.put(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, 'refresh'),
            ),
            headers=self.headers(),
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )

    def finalize(self, resource_id: str) -> InvoiceResponse:
        api_response: Response = requests.put(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, 'finalize'),
            ),
            headers=self.headers(),
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )
