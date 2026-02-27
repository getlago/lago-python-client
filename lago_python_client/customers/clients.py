import json
from collections.abc import Mapping
from typing import Any, ClassVar, Optional, Type, Union

from ..base_client import BaseClient
from ..mixins import (
    CreateCommandMixin,
    DestroyCommandMixin,
    FindAllCommandMixin,
    FindCommandMixin,
)
from ..models.customer import CustomerResponse
from ..models.customer_projected_usage import CustomerProjectedUsageResponse
from ..models.customer_usage import CustomerUsageResponse
from ..services.request import QueryPairs, make_headers, make_url, send_get_request, send_post_request
from ..services.response import (
    Response,
    get_response_data,
    prepare_index_response,
    prepare_object_response,
)


class CustomerClient(
    CreateCommandMixin[CustomerResponse],
    DestroyCommandMixin[CustomerResponse],
    FindAllCommandMixin[CustomerResponse],
    FindCommandMixin[CustomerResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "customers"
    RESPONSE_MODEL: ClassVar[Type[CustomerResponse]] = CustomerResponse
    ROOT_NAME: ClassVar[str] = "customer"

    def current_usage(
        self,
        resource_id: str,
        external_subscription_id: str,
        apply_taxes: Optional[str] = None,
        filter_by_charge_id: Optional[str] = None,
        filter_by_charge_code: Optional[str] = None,
        filter_by_group: Optional[dict] = None,
        full_usage: Optional[bool] = None,
    ) -> CustomerUsageResponse:
        query_params: dict[str, Union[str, bool]] = {"external_subscription_id": external_subscription_id}
        if apply_taxes is not None:
            query_params["apply_taxes"] = apply_taxes
        if filter_by_charge_id is not None:
            query_params["filter_by_charge_id"] = filter_by_charge_id
        if filter_by_charge_code is not None:
            query_params["filter_by_charge_code"] = filter_by_charge_code
        if filter_by_group is not None:
            query_params["filter_by_group"] = json.dumps(filter_by_group)
        if full_usage is not None:
            query_params["full_usage"] = str(full_usage).lower()

        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, "current_usage"),
                query_pairs=query_params,
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=CustomerUsageResponse,
            data=get_response_data(response=api_response, key="customer_usage"),
        )

    def projected_usage(
        self, resource_id: str, external_subscription_id: str, apply_taxes: Optional[str] = None
    ) -> CustomerProjectedUsageResponse:
        query_params = {"external_subscription_id": external_subscription_id}
        if apply_taxes is not None:
            query_params["apply_taxes"] = apply_taxes

        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, "projected_usage"),
                query_pairs=query_params,
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=CustomerProjectedUsageResponse,
            data=get_response_data(response=api_response, key="customer_projected_usage"),
        )

    def past_usage(
        self,
        resource_id: str,
        external_subscription_id: str,
        options: QueryPairs = None,
    ) -> Mapping[str, Any]:
        if options is None:
            options = {}
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, "past_usage"),
                query_pairs={
                    "external_subscription_id": external_subscription_id,
                    **options,
                },
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_index_response(
            api_resource="usage_periods",
            response_model=CustomerUsageResponse,
            data=get_response_data(response=api_response),
        )

    def portal_url(self, resource_id: str) -> str:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, "portal_url"),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        response_data = get_response_data(response=api_response, key=self.ROOT_NAME)
        return response_data.get("portal_url", "") if isinstance(response_data, Mapping) else ""

    def checkout_url(self, resource_id: str) -> str:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, "checkout_url"),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        response_data = get_response_data(response=api_response, key=self.ROOT_NAME)
        return response_data.get("checkout_url", "") if isinstance(response_data, Mapping) else ""
