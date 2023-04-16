import sys
from typing import ClassVar, Type

from ..base_operation import BaseOperation
from ..models.plan import PlanResponse
from ..shared_operations import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin

if sys.version_info >= (3, 9):
    from collections.abc import Callable, Mapping
else:
    from typing import Callable, Mapping


class CreatePlan(CreateCommandMixin[PlanResponse], BaseOperation):
    """Create a new plan."""

    API_RESOURCE: ClassVar[str] = 'plans'
    RESPONSE_MODEL: ClassVar[Type[PlanResponse]] = PlanResponse
    ROOT_NAME: ClassVar[str] = 'plan'


class DestroyPlan(DestroyCommandMixin[PlanResponse], BaseOperation):
    """Delete a plan."""

    API_RESOURCE: ClassVar[str] = 'plans'
    RESPONSE_MODEL: ClassVar[Type[PlanResponse]] = PlanResponse
    ROOT_NAME: ClassVar[str] = 'plan'


class FindAllPlans(FindAllCommandMixin[PlanResponse], BaseOperation):
    """Find plans."""

    API_RESOURCE: ClassVar[str] = 'plans'
    RESPONSE_MODEL: ClassVar[Type[PlanResponse]] = PlanResponse
    ROOT_NAME: ClassVar[str] = 'plan'


class FindPlan(FindCommandMixin[PlanResponse], BaseOperation):
    """Find plan by code."""

    API_RESOURCE: ClassVar[str] = 'plans'
    RESPONSE_MODEL: ClassVar[Type[PlanResponse]] = PlanResponse
    ROOT_NAME: ClassVar[str] = 'plan'


class UpdatePlan(UpdateCommandMixin[PlanResponse], BaseOperation):
    """Update an existing plan."""

    API_RESOURCE: ClassVar[str] = 'plans'
    RESPONSE_MODEL: ClassVar[Type[PlanResponse]] = PlanResponse
    ROOT_NAME: ClassVar[str] = 'plan'


plans_operations_config: Mapping[str, Callable[..., Callable]] = {
    'create': CreatePlan,
    'destroy': DestroyPlan,
    'find': FindPlan,
    'find_all': FindAllPlans,
    'update': UpdatePlan,
}
