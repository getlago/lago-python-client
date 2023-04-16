import sys
from typing import ClassVar, Type

from ..base_operation import BaseOperation
from ..models.fee import FeeResponse
from ..shared_operations import FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin

if sys.version_info >= (3, 9):
    from collections.abc import Callable, Mapping
else:
    from typing import Callable, Mapping


class FindAllFees(FindAllCommandMixin[FeeResponse], BaseOperation):
    """Find all fees."""

    API_RESOURCE: ClassVar[str] = 'fees'
    RESPONSE_MODEL: ClassVar[Type[FeeResponse]] = FeeResponse
    ROOT_NAME: ClassVar[str] = 'fee'


class FindFee(FindCommandMixin[FeeResponse], BaseOperation):
    """Find fee by ID."""

    API_RESOURCE: ClassVar[str] = 'fees'
    RESPONSE_MODEL: ClassVar[Type[FeeResponse]] = FeeResponse
    ROOT_NAME: ClassVar[str] = 'fee'


class UpdateFee(UpdateCommandMixin[FeeResponse], BaseOperation):
    """Update an existing fee."""

    API_RESOURCE: ClassVar[str] = 'fees'
    RESPONSE_MODEL: ClassVar[Type[FeeResponse]] = FeeResponse
    ROOT_NAME: ClassVar[str] = 'fee'


fees_operations_config: Mapping[str, Callable[..., Callable]] = {
    'find': FindFee,
    'find_all': FindAllFees,
    'update': UpdateFee,
}
