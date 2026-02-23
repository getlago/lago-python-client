from typing import Any, ClassVar, Mapping, Type

from ..base_client import BaseClient
from ..base_model import BaseModel
from ..mixins import (
    CreateCommandMixin,
    DestroyCommandMixin,
    FindAllCommandMixin,
    FindCommandMixin,
    UpdateCommandMixin,
)
from ..models.alert import AlertResponse, AlertsList
from ..models.charge import ChargeFilterResponse, ChargeResponse
from ..models.fixed_charge import FixedChargeResponse
from ..models.lifetime_usage import LifetimeUsageResponse
from ..models.subscription import SubscriptionResponse
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

    def find_all_fixed_charges(self, external_id: str, options: dict = {}) -> Mapping[str, Any]:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, external_id, "fixed_charges"),
                query_pairs=options,
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_index_response(
            api_resource="fixed_charges",
            response_model=FixedChargeResponse,
            data=get_response_data(response=api_response),
        )

    def find_fixed_charge(self, external_id: str, fixed_charge_code: str) -> FixedChargeResponse:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, external_id, "fixed_charges", fixed_charge_code),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=FixedChargeResponse,
            data=get_response_data(response=api_response, key="fixed_charge"),
        )

    def update_fixed_charge(
        self, external_id: str, fixed_charge_code: str, input_object: BaseModel
    ) -> FixedChargeResponse:
        api_response: Response = send_put_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, external_id, "fixed_charges", fixed_charge_code),
            ),
            content=to_json({"fixed_charge": input_object.dict(exclude_none=True)}),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=FixedChargeResponse,
            data=get_response_data(response=api_response, key="fixed_charge"),
        )

    # Charges

    def find_all_charges(self, external_id: str, options: dict = {}) -> Mapping[str, Any]:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, external_id, "charges"),
                query_pairs=options,
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_index_response(
            api_resource="charges",
            response_model=ChargeResponse,
            data=get_response_data(response=api_response),
        )

    def find_charge(self, external_id: str, charge_code: str) -> ChargeResponse:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, external_id, "charges", charge_code),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=ChargeResponse,
            data=get_response_data(response=api_response, key="charge"),
        )

    def update_charge(self, external_id: str, charge_code: str, input_object: BaseModel) -> ChargeResponse:
        api_response: Response = send_put_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, external_id, "charges", charge_code),
            ),
            content=to_json({"charge": input_object.dict(exclude_none=True)}),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=ChargeResponse,
            data=get_response_data(response=api_response, key="charge"),
        )

    # Charge Filters

    def find_all_charge_filters(self, external_id: str, charge_code: str, options: dict = {}) -> Mapping[str, Any]:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, external_id, "charges", charge_code, "filters"),
                query_pairs=options,
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_index_response(
            api_resource="filters",
            response_model=ChargeFilterResponse,
            data=get_response_data(response=api_response),
        )

    def find_charge_filter(self, external_id: str, charge_code: str, filter_id: str) -> ChargeFilterResponse:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, external_id, "charges", charge_code, "filters", filter_id),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=ChargeFilterResponse,
            data=get_response_data(response=api_response, key="filter"),
        )

    def create_charge_filter(self, external_id: str, charge_code: str, input_object: BaseModel) -> ChargeFilterResponse:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, external_id, "charges", charge_code, "filters"),
            ),
            content=to_json({"filter": input_object.dict(exclude_none=True)}),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=ChargeFilterResponse,
            data=get_response_data(response=api_response, key="filter"),
        )

    def update_charge_filter(
        self, external_id: str, charge_code: str, filter_id: str, input_object: BaseModel
    ) -> ChargeFilterResponse:
        api_response: Response = send_put_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, external_id, "charges", charge_code, "filters", filter_id),
            ),
            content=to_json({"filter": input_object.dict(exclude_none=True)}),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=ChargeFilterResponse,
            data=get_response_data(response=api_response, key="filter"),
        )

    def destroy_charge_filter(self, external_id: str, charge_code: str, filter_id: str) -> ChargeFilterResponse:
        api_response: Response = send_delete_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, external_id, "charges", charge_code, "filters", filter_id),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=ChargeFilterResponse,
            data=get_response_data(response=api_response, key="filter"),
        )
