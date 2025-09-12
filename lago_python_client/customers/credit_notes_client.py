from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import FindAllChildrenCommandMixin
from ..models.credit_note import CreditNoteResponse
from ..client import CustomerClient


class CustomerCreditNotesClient(FindAllChildrenCommandMixin, BaseClient):
    PARENT_API_RESOURCE: ClassVar[str] = CustomerClient.API_RESOURCE
    API_RESOURCE: ClassVar[str] = "credit_notes"
    RESPONSE_MODEL: ClassVar[Type[CreditNoteResponse]] = CreditNoteResponse
    ROOT_NAME: ClassVar[str] = "credit_note"
