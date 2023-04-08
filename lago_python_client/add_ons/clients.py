from typing import ClassVar, Optional, Type

from pydantic import BaseModel

from ..base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.add_on import AddOnResponse
from ..models.applied_add_on import AppliedAddOnResponse


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

    def __init__(self, base_url: str, api_key: str) -> None:
        """Initialize client instance with internal ``AppliedAddOnClient`` client instance."""
        super().__init__(base_url=base_url, api_key=api_key)
        self._applied_add_ons: AppliedAddOnClient = AppliedAddOnClient(base_url=base_url, api_key=api_key)

    def apply(self, input_object: BaseModel) -> Optional[AppliedAddOnResponse]:
        """Apply add-on."""
        return self._applied_add_ons.create(input_object=input_object)


class AppliedAddOnClient(CreateCommandMixin[AppliedAddOnResponse], BaseClient):
    """Applied add-ons collection client.

    Pending deprecation warning: class methods are not for public use. If you going to add new methods then register aliases in `AddOnClient`.
    """

    API_RESOURCE: ClassVar[str] = 'applied_add_ons'
    RESPONSE_MODEL: ClassVar[Type[AppliedAddOnResponse]] = AppliedAddOnResponse
    ROOT_NAME: ClassVar[str] = 'applied_add_on'
