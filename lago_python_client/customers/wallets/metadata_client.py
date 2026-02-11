import sys
from typing import Dict, Optional, ClassVar

from lago_python_client.base_model import BaseModel

from ...base_client import BaseClient
from ...services.json import to_json
from ...services.request import (
    make_headers,
    make_url,
    send_delete_request,
    send_patch_request,
    send_post_request,
    QueryPairs,
)
from ...services.response import (
    get_response_data,
    Response,
)


class CustomerWalletMetadataClient(BaseClient):
    API_RESOURCE: ClassVar[str] = "metadata"
    RESPONSE_MODEL: ClassVar[Dict] = Dict[str, Optional[str]]
    ROOT_NAME: ClassVar[str] = "metadata"

    def api_resource(self, customer_id: str, wallet_code: str) -> tuple:
        return ("customers", customer_id, "wallets", wallet_code, "metadata")

    def replace(
        self, customer_id: str, wallet_code: str, metadata: Dict[str, Optional[str]]
    ) -> Optional[Dict[str, Optional[str]]]:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=self.api_resource(customer_id, wallet_code),
            ),
            content=to_json({"metadata": metadata}),
            headers=make_headers(api_key=self.api_key),
        )

        return get_response_data(response=api_response, key="metadata")

    def merge(
        self, customer_id: str, wallet_code: str, metadata: Dict[str, Optional[str]]
    ) -> Optional[Dict[str, Optional[str]]]:
        api_response: Response = send_patch_request(
            url=make_url(
                origin=self.base_url,
                path_parts=self.api_resource(customer_id, wallet_code),
            ),
            content=to_json({"metadata": metadata}),
            headers=make_headers(api_key=self.api_key),
        )

        return get_response_data(response=api_response, key="metadata")

    def delete_all(self, customer_id: str, wallet_code: str) -> Optional[Dict[str, Optional[str]]]:
        api_response: Response = send_delete_request(
            url=make_url(
                origin=self.base_url,
                path_parts=self.api_resource(customer_id, wallet_code),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return get_response_data(response=api_response, key="metadata")

    def delete_key(self, customer_id: str, wallet_code: str, key: str) -> Optional[Dict[str, Optional[str]]]:
        api_response: Response = send_delete_request(
            url=make_url(
                origin=self.base_url,
                path_parts=self.api_resource(customer_id, wallet_code) + (key,),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return get_response_data(response=api_response, key="metadata")
