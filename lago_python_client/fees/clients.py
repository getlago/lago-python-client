from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import FindCommandMixin, FindAllCommandMixin, UpdateCommandMixin, DestroyCommandMixin
from ..models.fee import FeeResponse


class FeeClient(
    FindCommandMixin[FeeResponse],
    FindAllCommandMixin[FeeResponse],
    UpdateCommandMixin[FeeResponse],
    DestroyCommandMixin[FeeResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'fees'
    RESPONSE_MODEL: ClassVar[Type[FeeResponse]] = FeeResponse
    ROOT_NAME: ClassVar[str] = 'fee'
