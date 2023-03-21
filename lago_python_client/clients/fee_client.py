from typing import ClassVar, Type

from pydantic import BaseModel

from .base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.fee import FeeResponse

class FeeClient(CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin, BaseClient):
    API_RESOURCE: ClassVar[str] = 'fees'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = FeeResponse
    ROOT_NAME: ClassVar[str] = 'fee'
