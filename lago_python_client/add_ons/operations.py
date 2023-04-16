import sys
from typing import ClassVar, Type

from ..base_operation import BaseOperation
from ..models.add_on import AddOnResponse
from ..models.applied_add_on import AppliedAddOnResponse
from ..shared_operations import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin

if sys.version_info >= (3, 9):
    from collections.abc import Callable, Mapping
else:
    from typing import Callable, Mapping


class ApplyAddOn(CreateCommandMixin[AppliedAddOnResponse], BaseOperation):
    """Apply an add-on to a customer."""

    API_RESOURCE: ClassVar[str] = 'applied_add_ons'
    RESPONSE_MODEL: ClassVar[Type[AppliedAddOnResponse]] = AppliedAddOnResponse
    ROOT_NAME: ClassVar[str] = 'applied_add_on'


class CreateAddOn(CreateCommandMixin[AddOnResponse], BaseOperation):
    """Create a new add-on."""

    API_RESOURCE: ClassVar[str] = 'add_ons'
    RESPONSE_MODEL: ClassVar[Type[AddOnResponse]] = AddOnResponse
    ROOT_NAME: ClassVar[str] = 'add_on'


class DestroyAddOn(DestroyCommandMixin[AddOnResponse], BaseOperation):
    """Delete an add-on."""

    API_RESOURCE: ClassVar[str] = 'add_ons'
    RESPONSE_MODEL: ClassVar[Type[AddOnResponse]] = AddOnResponse
    ROOT_NAME: ClassVar[str] = 'add_on'


class FindAddOn(FindCommandMixin[AddOnResponse], BaseOperation):
    """Find add-on by code."""

    API_RESOURCE: ClassVar[str] = 'add_ons'
    RESPONSE_MODEL: ClassVar[Type[AddOnResponse]] = AddOnResponse
    ROOT_NAME: ClassVar[str] = 'add_on'


class FindAllAddOns(FindAllCommandMixin[AddOnResponse], BaseOperation):
    """Find add-ons."""

    API_RESOURCE: ClassVar[str] = 'add_ons'
    RESPONSE_MODEL: ClassVar[Type[AddOnResponse]] = AddOnResponse
    ROOT_NAME: ClassVar[str] = 'add_on'


class UpdateAddOn(UpdateCommandMixin[AddOnResponse], BaseOperation):
    """Update an existing add-on."""

    API_RESOURCE: ClassVar[str] = 'add_ons'
    RESPONSE_MODEL: ClassVar[Type[AddOnResponse]] = AddOnResponse
    ROOT_NAME: ClassVar[str] = 'add_on'


add_ons_operations_config: Mapping[str, Callable[..., Callable]] = {
    'create': CreateAddOn,
    'destroy': DestroyAddOn,
    'find': FindAddOn,
    'find_all': FindAllAddOns,
    'update': UpdateAddOn,
}

applied_add_ons_operations_config: Mapping[str, Callable[..., Callable]] = {
    'create': ApplyAddOn,
}
