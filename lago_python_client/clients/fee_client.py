from typing import ClassVar, Type

from .base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.fee import FeeResponse

class FeeClient(
    FindCommandMixin[FeeResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'fees'
    RESPONSE_MODEL: ClassVar[Type[FeeResponse]] = FeeResponse
    ROOT_NAME: ClassVar[str] = 'fee'
