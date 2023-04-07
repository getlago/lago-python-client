from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.plan import PlanResponse


class PlanClient(
    CreateCommandMixin[PlanResponse],
    DestroyCommandMixin[PlanResponse],
    FindAllCommandMixin[PlanResponse],
    FindCommandMixin[PlanResponse],
    UpdateCommandMixin[PlanResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'plans'
    RESPONSE_MODEL: ClassVar[Type[PlanResponse]] = PlanResponse
    ROOT_NAME: ClassVar[str] = 'plan'
