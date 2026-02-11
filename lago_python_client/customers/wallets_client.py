from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import FindAllChildrenCommandMixin
from ..models.wallet import WalletResponse

from ..mixins import (
    NestedCreateCommandMixin,
    NestedUpdateCommandMixin,
    NestedDestroyCommandMixin,
    NestedFindCommandMixin,
    NestedFindAllCommandMixin,
)

class CustomerWalletsClient(
    NestedCreateCommandMixin[WalletResponse],
    NestedUpdateCommandMixin[WalletResponse],
    NestedDestroyCommandMixin[WalletResponse],
    NestedFindCommandMixin[WalletResponse],
    NestedFindAllCommandMixin[WalletResponse],
    BaseClient
):
    API_RESOURCE: ClassVar[str] = "wallets"
    PARENT_RESOURCES: ClassVar[tuple[str]] = ("customer_id")
    RESPONSE_MODEL: ClassVar[Type[WalletResponse]] = WalletResponse
    ROOT_NAME: ClassVar[str] = "wallet"

    def api_resource(self, customer_id: str) -> tuple[str]:
        return ("customers", customer_id, "wallets",)
