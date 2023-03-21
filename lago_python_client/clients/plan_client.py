from typing import ClassVar, Type

from pydantic import BaseModel

from .base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.plan import PlanResponse


class PlanClient(CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin, BaseClient):
    API_RESOURCE: ClassVar[str] = 'plans'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = PlanResponse
    ROOT_NAME: ClassVar[str] = 'plan'
