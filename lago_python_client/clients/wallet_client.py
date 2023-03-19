from typing import ClassVar, Type

from .base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.wallet import WalletResponse


class WalletClient(
    CreateCommandMixin[WalletResponse],
    DestroyCommandMixin[WalletResponse],
    FindAllCommandMixin[WalletResponse],
    FindCommandMixin[WalletResponse],
    UpdateCommandMixin[WalletResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'wallets'
    RESPONSE_MODEL: ClassVar[Type[WalletResponse]] = WalletResponse
    ROOT_NAME: ClassVar[str] = 'wallet'
