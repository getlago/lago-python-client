from typing import Any, ClassVar, Dict, Mapping, Optional, Type

from ..base_client import BaseClient
from ..base_model import BaseModel
from ..mixins import (
    CreateCommandMixin,
    DestroyCommandMixin,
    FindAllCommandMixin,
    FindCommandMixin,
    UpdateCommandMixin,
)
from ..models.charge import ChargeFilterResponse, ChargeResponse
from ..models.fixed_charge import FixedChargeResponse
from ..models.plan import PlanResponse
from ..services.json import to_json
from ..services.request import (
    make_headers,
    make_url,
    send_delete_request,
    send_get_request,
    send_patch_request,
    send_post_request,
    send_put_request,
)
from ..services.response import (
    Response,
    get_response_data,
    prepare_index_response,
    prepare_object_response,
)


class PlanClient(
    CreateCommandMixin[PlanResponse],
    DestroyCommandMixin[PlanResponse],
    FindAllCommandMixin[PlanResponse],
    FindCommandMixin[PlanResponse],
    UpdateCommandMixin[PlanResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "plans"
    RESPONSE_MODEL: ClassVar[Type[PlanResponse]] = PlanResponse
    ROOT_NAME: ClassVar[str] = "plan"

    def replace_metadata(
        self, resource_id: str, metadata: Dict[str, Optional[str]]
    ) -> Optional[Dict[str, Optional[str]]]:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, "metadata"),
            ),
            content=to_json({"metadata": metadata}),
            headers=make_headers(api_key=self.api_key),
        )

        return get_response_data(response=api_response, key="metadata")

    def merge_metadata(
        self, resource_id: str, metadata: Dict[str, Optional[str]]
    ) -> Optional[Dict[str, Optional[str]]]:
        api_response: Response = send_patch_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, "metadata"),
            ),
            content=to_json({"metadata": metadata}),
            headers=make_headers(api_key=self.api_key),
        )

        return get_response_data(response=api_response, key="metadata")

    def delete_all_metadata(self, resource_id: str) -> Optional[Dict[str, Optional[str]]]:
        api_response: Response = send_delete_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, "metadata"),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return get_response_data(response=api_response, key="metadata")

    def delete_metadata_key(self, resource_id: str, key: str) -> Optional[Dict[str, Optional[str]]]:
        api_response: Response = send_delete_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, "metadata", key),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return get_response_data(response=api_response, key="metadata")

    # Charges

    def find_all_charges(self, plan_code: str, options: dict = {}) -> Mapping[str, Any]:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, plan_code, "charges"),
                query_pairs=options,
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_index_response(
            api_resource="charges",
            response_model=ChargeResponse,
            data=get_response_data(response=api_response),
        )

    def find_charge(self, plan_code: str, charge_code: str) -> ChargeResponse:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, plan_code, "charges", charge_code),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=ChargeResponse,
            data=get_response_data(response=api_response, key="charge"),
        )

    def create_charge(self, plan_code: str, input_object: BaseModel) -> ChargeResponse:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, plan_code, "charges"),
            ),
            content=to_json({"charge": input_object.dict(exclude_none=True)}),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=ChargeResponse,
            data=get_response_data(response=api_response, key="charge"),
        )

    def update_charge(self, plan_code: str, charge_code: str, input_object: BaseModel) -> ChargeResponse:
        api_response: Response = send_put_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, plan_code, "charges", charge_code),
            ),
            content=to_json({"charge": input_object.dict(exclude_none=True)}),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=ChargeResponse,
            data=get_response_data(response=api_response, key="charge"),
        )

    def destroy_charge(self, plan_code: str, charge_code: str) -> ChargeResponse:
        api_response: Response = send_delete_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, plan_code, "charges", charge_code),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=ChargeResponse,
            data=get_response_data(response=api_response, key="charge"),
        )

    # Fixed Charges

    def find_all_fixed_charges(self, plan_code: str, options: dict = {}) -> Mapping[str, Any]:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, plan_code, "fixed_charges"),
                query_pairs=options,
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_index_response(
            api_resource="fixed_charges",
            response_model=FixedChargeResponse,
            data=get_response_data(response=api_response),
        )

    def find_fixed_charge(self, plan_code: str, fixed_charge_code: str) -> FixedChargeResponse:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, plan_code, "fixed_charges", fixed_charge_code),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=FixedChargeResponse,
            data=get_response_data(response=api_response, key="fixed_charge"),
        )

    def create_fixed_charge(self, plan_code: str, input_object: BaseModel) -> FixedChargeResponse:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, plan_code, "fixed_charges"),
            ),
            content=to_json({"fixed_charge": input_object.dict(exclude_none=True)}),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=FixedChargeResponse,
            data=get_response_data(response=api_response, key="fixed_charge"),
        )

    def update_fixed_charge(
        self, plan_code: str, fixed_charge_code: str, input_object: BaseModel
    ) -> FixedChargeResponse:
        api_response: Response = send_put_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, plan_code, "fixed_charges", fixed_charge_code),
            ),
            content=to_json({"fixed_charge": input_object.dict(exclude_none=True)}),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=FixedChargeResponse,
            data=get_response_data(response=api_response, key="fixed_charge"),
        )

    def destroy_fixed_charge(self, plan_code: str, fixed_charge_code: str) -> FixedChargeResponse:
        api_response: Response = send_delete_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, plan_code, "fixed_charges", fixed_charge_code),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=FixedChargeResponse,
            data=get_response_data(response=api_response, key="fixed_charge"),
        )

    # Charge Filters

    def find_all_charge_filters(self, plan_code: str, charge_code: str, options: dict = {}) -> Mapping[str, Any]:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, plan_code, "charges", charge_code, "filters"),
                query_pairs=options,
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_index_response(
            api_resource="filters",
            response_model=ChargeFilterResponse,
            data=get_response_data(response=api_response),
        )

    def find_charge_filter(self, plan_code: str, charge_code: str, filter_id: str) -> ChargeFilterResponse:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, plan_code, "charges", charge_code, "filters", filter_id),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=ChargeFilterResponse,
            data=get_response_data(response=api_response, key="filter"),
        )

    def create_charge_filter(self, plan_code: str, charge_code: str, input_object: BaseModel) -> ChargeFilterResponse:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, plan_code, "charges", charge_code, "filters"),
            ),
            content=to_json({"filter": input_object.dict(exclude_none=True)}),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=ChargeFilterResponse,
            data=get_response_data(response=api_response, key="filter"),
        )

    def update_charge_filter(
        self, plan_code: str, charge_code: str, filter_id: str, input_object: BaseModel
    ) -> ChargeFilterResponse:
        api_response: Response = send_put_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, plan_code, "charges", charge_code, "filters", filter_id),
            ),
            content=to_json({"filter": input_object.dict(exclude_none=True)}),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=ChargeFilterResponse,
            data=get_response_data(response=api_response, key="filter"),
        )

    def destroy_charge_filter(self, plan_code: str, charge_code: str, filter_id: str) -> ChargeFilterResponse:
        api_response: Response = send_delete_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, plan_code, "charges", charge_code, "filters", filter_id),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=ChargeFilterResponse,
            data=get_response_data(response=api_response, key="filter"),
        )
