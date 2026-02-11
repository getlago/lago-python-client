from typing import ClassVar, Type

from ..functools_ext import callable_cached_property
from ..base_client import BaseClient
from ..models.wallet import WalletResponse

from ..mixins import (
    NestedCreateCommandMixin,
    NestedUpdateCommandMixin,
    NestedDestroyCommandMixin,
    NestedFindCommandMixin,
    NestedFindAllCommandMixin,
)

from .wallets.metadata_client import CustomerWalletMetadataClient


class CustomerWalletClient(
    NestedCreateCommandMixin[WalletResponse],
    NestedUpdateCommandMixin[WalletResponse],
    NestedDestroyCommandMixin[WalletResponse],
    NestedFindCommandMixin[WalletResponse],
    NestedFindAllCommandMixin[WalletResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "wallets"
    RESPONSE_MODEL: ClassVar[Type[WalletResponse]] = WalletResponse
    ROOT_NAME: ClassVar[str] = "wallet"

    def api_resource(self, customer_id: str) -> tuple[str]:
        return (
            "customers",
            customer_id,
            "wallets",
        )

    @callable_cached_property
    def metadata(self) -> CustomerWalletMetadataClient:
        return CustomerWalletMetadataClient(self.base_url, self.api_key)
