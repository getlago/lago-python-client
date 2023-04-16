import sys
from typing import ClassVar, Type

from ..base_operation import BaseOperation
from ..models.organization import OrganizationResponse
from ..shared_operations import UpdateCommandMixin

if sys.version_info >= (3, 9):
    from collections.abc import Callable, Mapping
else:
    from typing import Callable, Mapping


class UpdateOrganization(UpdateCommandMixin[OrganizationResponse], BaseOperation):
    """Update an existing Organization."""

    API_RESOURCE: ClassVar[str] = 'organizations'
    RESPONSE_MODEL: ClassVar[Type[OrganizationResponse]] = OrganizationResponse
    ROOT_NAME: ClassVar[str] = 'organization'


organizations_operations_config: Mapping[str, Callable[..., Callable]] = {
    'update': UpdateOrganization,
}
