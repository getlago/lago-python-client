from typing import ClassVar, Type

from ...base_client import BaseClient
from ...models.alert import AlertResponse, AlertsList

from ...mixins import (
    NestedCreateCommandMixin,
    NestedUpdateCommandMixin,
    NestedDestroyCommandMixin,
    NestedFindCommandMixin,
    NestedFindAllCommandMixin,
)

from ...services.json import to_json
from ...services.request import (
    make_headers,
    make_url,
    send_delete_request,
    send_post_request,
)
from ...services.response import (
    get_response_data,
    prepare_index_response,
    verify_response,
    Response,
)


class CustomerWalletAlertClient(
    NestedCreateCommandMixin[AlertResponse],
    NestedUpdateCommandMixin[AlertResponse],
    NestedDestroyCommandMixin[AlertResponse],
    NestedFindCommandMixin[AlertResponse],
    NestedFindAllCommandMixin[AlertResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "alerts"
    RESPONSE_MODEL: ClassVar[Type[AlertResponse]] = AlertResponse
    ROOT_NAME: ClassVar[str] = "alert"

    def api_resource(self, customer_id: str, wallet_code: str) -> tuple[str]:
        return ("customers", customer_id, "wallets", wallet_code, "alerts")

    def create_batch(self, customer_id: str, wallet_code: str, input_object: AlertsList) -> None:
        api_response: Response = send_post_request(
            url=make_url(origin=self.base_url, path_parts=self.api_resource(customer_id, wallet_code)),
            content=to_json(input_object.dict()),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_index_response(
            api_resource="alerts",
            response_model=AlertResponse,
            data=get_response_data(response=api_response),
        )

    def destroy_all(self, customer_id: str, wallet_code: str) -> None:
        api_response: Response = send_delete_request(
            url=make_url(
                origin=self.base_url,
                path_parts=self.api_resource(customer_id, wallet_code),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        verify_response(api_response)
