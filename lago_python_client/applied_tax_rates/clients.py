from typing import ClassVar, Type

from pydantic import BaseModel
from ..base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..services.json import to_json
from ..services.request import make_headers, make_url, send_post_request, send_delete_request
from ..models.applied_tax_rate import AppliedTaxRateResponse
from ..services.response import get_response_data, prepare_object_response, Response


class AppliedTaxRateClient(
    CreateCommandMixin[AppliedTaxRateResponse],
    DestroyCommandMixin[AppliedTaxRateResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'applied_tax_rates'
    RESPONSE_MODEL: ClassVar[Type[AppliedTaxRateResponse]] = AppliedTaxRateResponse
    ROOT_NAME: ClassVar[str] = 'applied_tax_rate'

    def create(self, external_customer_id: str, input_object: BaseModel) -> AppliedTaxRateResponse:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=('customers', external_customer_id, self.API_RESOURCE),
            ),
            content=to_json({
                self.ROOT_NAME: input_object.dict(),
            }),
            headers=make_headers(api_key=self.api_key),
        )
    
        response_data = get_response_data(response=api_response, key=self.ROOT_NAME)
        if not response_data:
            return None

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=response_data,
        )

    def destroy(self, external_customer_id: str, tax_rate_code: str) -> AppliedTaxRateResponse:
        api_response: Response = send_delete_request(
            url=make_url(
                origin=self.base_url,
                path_parts=('customers', external_customer_id, self.API_RESOURCE, tax_rate_code),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )
