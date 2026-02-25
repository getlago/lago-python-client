from typing import ClassVar, Dict, Optional, Type

from ..base_client import BaseClient
from ..mixins import (
    CreateCommandMixin,
    DestroyCommandMixin,
    FindAllCommandMixin,
    FindCommandMixin,
    UpdateCommandMixin,
)
from ..models.plan import PlanResponse
from ..services.json import to_json
from ..services.request import (
    make_headers,
    make_url,
    send_delete_request,
    send_patch_request,
    send_post_request,
)
from ..services.response import Response, get_response_data


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
