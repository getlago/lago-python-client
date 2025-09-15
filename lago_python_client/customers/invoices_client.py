from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import FindAllChildrenCommandMixin
from ..models.invoice import InvoiceResponse
from ..client import CustomerClient


class CustomerInvoicesClient(FindAllChildrenCommandMixin, BaseClient):
    PARENT_API_RESOURCE: ClassVar[str] = CustomerClient.API_RESOURCE
    API_RESOURCE: ClassVar[str] = "invoices"
    RESPONSE_MODEL: ClassVar[Type[InvoiceResponse]] = InvoiceResponse
    ROOT_NAME: ClassVar[str] = "invoice"
