from collections.abc import Mapping
from typing import Any, ClassVar, Dict, Optional, Type

from lago_python_client.base_model import BaseModel

from ..base_client import BaseClient
from ..mixins import (
    CreateCommandMixin,
    DestroyCommandMixin,
    FindAllCommandMixin,
    FindCommandMixin,
    UpdateCommandMixin,
)
from ..models.wallet import WalletResponse
from ..models.wallet_transaction import WalletTransactionResponse
from ..services.json import to_json
from ..services.request import (
    QueryPairs,
    make_headers,
    make_url,
    send_delete_request,
    send_get_request,
    send_patch_request,
    send_post_request,
)
from ..services.response import (
    Response,
    get_response_data,
    prepare_index_response,
    prepare_object_list_response,
)


class WalletClient(
    CreateCommandMixin[WalletResponse],
    DestroyCommandMixin[WalletResponse],
    FindAllCommandMixin[WalletResponse],
    FindCommandMixin[WalletResponse],
    UpdateCommandMixin[WalletResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "wallets"
    RESPONSE_MODEL: ClassVar[Type[WalletResponse]] = WalletResponse
    ROOT_NAME: ClassVar[str] = "wallet"

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


class WalletTransactionClient(BaseClient):
    API_RESOURCE: ClassVar[str] = "wallet_transactions"
    RESPONSE_MODEL: ClassVar[Type[WalletTransactionResponse]] = WalletTransactionResponse
    ROOT_NAME: ClassVar[str] = "wallet_transactions"

    def create(self, input_object: BaseModel) -> Mapping[str, Any]:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE,),
            ),
            content=to_json({"wallet_transaction": input_object.dict()}),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_list_response(
            api_resource=self.API_RESOURCE,
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )

    def find_all(self, wallet_id: str, options: QueryPairs = None) -> Mapping[str, Any]:
        if options is None:
            options = {}
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=("wallets", wallet_id, self.API_RESOURCE),
                query_pairs=options,
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_index_response(
            api_resource=self.API_RESOURCE,
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response),
        )

    def payment_url(self, resource_id: str) -> str:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, "payment_url"),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        response_data = get_response_data(response=api_response, key="wallet_transaction_payment_details")
        return response_data.get("payment_url", "") if isinstance(response_data, Mapping) else ""
