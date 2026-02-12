from typing import ClassVar, Type

from ...base_client import BaseClient
from ...models.alert import AlertResponse

from ...mixins import (
    NestedCreateCommandMixin,
    NestedUpdateCommandMixin,
    NestedDestroyCommandMixin,
    NestedFindCommandMixin,
    NestedFindAllCommandMixin,
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
