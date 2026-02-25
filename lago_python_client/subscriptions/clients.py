from typing import Any, ClassVar, Mapping, Type

from ..base_client import BaseClient
from ..mixins import (
    CreateCommandMixin,
    DestroyCommandMixin,
    FindAllCommandMixin,
    FindCommandMixin,
    UpdateCommandMixin,
)
from ..models.alert import AlertResponse, AlertsList
from ..models.fixed_charge import FixedChargeResponse
from ..models.lifetime_usage import LifetimeUsageResponse
from ..models.subscription import SubscriptionResponse
from ..services.json import to_json
from ..services.request import (
    make_headers,
    make_url,
    send_delete_request,
    send_get_request,
    send_post_request,
    send_put_request,
)
from ..services.response import (
    Response,
    get_response_data,
    prepare_index_response,
    prepare_object_response,
    verify_response,
)


class SubscriptionClient(
    CreateCommandMixin[SubscriptionResponse],
    DestroyCommandMixin[SubscriptionResponse],
    FindAllCommandMixin[SubscriptionResponse],
    FindCommandMixin[SubscriptionResponse],
    UpdateCommandMixin[SubscriptionResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "subscriptions"
    RESPONSE_MODEL: ClassVar[Type[SubscriptionResponse]] = SubscriptionResponse
    ROOT_NAME: ClassVar[str] = "subscription"

    def lifetime_usage(self, resource_id: str) -> LifetimeUsageResponse:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, "lifetime_usage"),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=LifetimeUsageResponse,
            data=get_response_data(response=api_response, key="lifetime_usage"),
        )

    def update_lifetime_usage(
        self, resource_id: str, external_historical_usage_amount_cents: int
    ) -> LifetimeUsageResponse:
        api_response: Response = send_put_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, "lifetime_usage"),
            ),
            content=to_json(
                {"lifetime_usage": {"external_historical_usage_amount_cents": external_historical_usage_amount_cents}}
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=LifetimeUsageResponse,
            data=get_response_data(response=api_response, key="lifetime_usage"),
        )

    def create_alerts(self, external_id: str, input_object: AlertsList) -> Mapping[str, Any]:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, external_id, "alerts"),
            ),
            content=to_json(input_object.dict()),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_index_response(
            api_resource="alerts",
            response_model=AlertResponse,
            data=get_response_data(response=api_response),
        )

    def delete_alerts(self, external_id: str) -> None:
        api_response: Response = send_delete_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, external_id, "alerts"),
            ),
            headers=make_headers(api_key=self.api_key),
        )
        verify_response(api_response)

    def find_all_fixed_charges(self, external_id: str) -> Mapping[str, Any]:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, external_id, "fixed_charges"),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_index_response(
            api_resource="fixed_charges",
            response_model=FixedChargeResponse,
            data=get_response_data(response=api_response),
        )
