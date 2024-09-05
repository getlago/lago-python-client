from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import (
    CreateCommandMixin,
    DestroyCommandMixin,
    FindAllCommandMixin,
    FindCommandMixin,
    UpdateCommandMixin,
)
from ..models.lifetime_usage import LifetimeUsageResponse
from ..models.subscription import SubscriptionResponse
from ..services.request import (
    make_headers,
    make_url,
    send_get_request,
    send_put_request,
)
from ..services.response import (
    Response,
    get_response_data,
    prepare_object_response,
)
from ..services.json import to_json


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
