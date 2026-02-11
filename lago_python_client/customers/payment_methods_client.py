from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import FindAllChildrenCommandMixin
from ..models.payment_method import PaymentMethodResponse
from ..services.request import make_headers, make_url, send_delete_request, send_put_request
from ..services.response import get_response_data, prepare_object_response, Response


class CustomerPaymentMethodsClient(FindAllChildrenCommandMixin[PaymentMethodResponse], BaseClient):
    PARENT_API_RESOURCE: ClassVar[str] = "customers"
    API_RESOURCE: ClassVar[str] = "payment_methods"
    RESPONSE_MODEL: ClassVar[Type[PaymentMethodResponse]] = PaymentMethodResponse
    ROOT_NAME: ClassVar[str] = "payment_method"

    def destroy(self, customer_external_id: str, payment_method_id: str) -> PaymentMethodResponse:
        api_response: Response = send_delete_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.PARENT_API_RESOURCE, customer_external_id, self.API_RESOURCE, payment_method_id),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )

    def set_as_default(self, customer_external_id: str, payment_method_id: str) -> PaymentMethodResponse:
        api_response: Response = send_put_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(
                    self.PARENT_API_RESOURCE,
                    customer_external_id,
                    self.API_RESOURCE,
                    payment_method_id,
                    "set_as_default",
                ),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )
