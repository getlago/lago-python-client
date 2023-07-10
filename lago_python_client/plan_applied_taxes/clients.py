from typing import ClassVar, Type

from pydantic import BaseModel
from ..base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin
from ..services.json import to_json
from ..services.request import make_headers, make_url, send_post_request, send_delete_request
from ..models.plan_applied_tax import PlanAppliedTax, PlanAppliedTaxResponse
from ..services.response import get_response_data, prepare_object_response, Response


class PlanAppliedTaxClient(
    CreateCommandMixin[PlanAppliedTaxResponse],
    DestroyCommandMixin[PlanAppliedTaxResponse],
    BaseClient
):
    API_RESOURCE: ClassVar[str] = 'applied_taxes'
    RESPONSE_MODEL: ClassVar[Type[PlanAppliedTaxResponse]] = PlanAppliedTaxResponse
    ROOT_NAME: ClassVar[str] = 'applied_tax'

    def create(self, plan_code: str, input_object: PlanAppliedTax) -> PlanAppliedTaxResponse:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=('plans', plan_code, self.API_RESOURCE),
            ),
            content=to_json({
                self.ROOT_NAME: input_object.dict(),
            }),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )

    def destroy(self, plan_code: str, tax_code: str) -> PlanAppliedTaxResponse:
        api_response: Response = send_delete_request(
            url=make_url(
                origin=self.base_url,
                path_parts=('plans', plan_code, self.API_RESOURCE, tax_code),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )
