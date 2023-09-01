from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.add_on import AddOnResponse


class AddOnClient(
    CreateCommandMixin[AddOnResponse],
    DestroyCommandMixin[AddOnResponse],
    FindAllCommandMixin[AddOnResponse],
    FindCommandMixin[AddOnResponse],
    UpdateCommandMixin[AddOnResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'add_ons'
    RESPONSE_MODEL: ClassVar[Type[AddOnResponse]] = AddOnResponse
    ROOT_NAME: ClassVar[str] = 'add_on'
