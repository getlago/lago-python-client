import sys
from typing import ClassVar, Optional, Type

from ..base_operation import BaseOperation
from ..models.invoice import InvoiceResponse
from ..services.request import make_headers, make_url, send_post_request, send_put_request
from ..services.response import get_response_data, prepare_object_response, Response
from ..shared_operations import FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin

if sys.version_info >= (3, 9):
    from collections.abc import Callable, Mapping
else:
    from typing import Callable, Mapping


class DownloadInvoice(BaseOperation):
    """Download an existing invoice."""

    API_RESOURCE: ClassVar[str] = 'invoices'
    RESPONSE_MODEL: ClassVar[Type[InvoiceResponse]] = InvoiceResponse
    ROOT_NAME: ClassVar[str] = 'invoice'

    def __call__(self, resource_id: str) -> Optional[InvoiceResponse]:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, 'download'),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        response_data = get_response_data(response=api_response, key=self.ROOT_NAME)
        if not response_data:
            return None

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=response_data,
        )


class FinalizeInvoice(BaseOperation):
    """Finalize a draft invoice."""

    API_RESOURCE: ClassVar[str] = 'invoices'
    RESPONSE_MODEL: ClassVar[Type[InvoiceResponse]] = InvoiceResponse
    ROOT_NAME: ClassVar[str] = 'invoice'

    def __call__(self, resource_id: str) -> InvoiceResponse:
        api_response: Response = send_put_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, 'finalize'),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )


class FindAllInvoices(FindAllCommandMixin[InvoiceResponse], BaseOperation):
    """Find all invoices."""

    API_RESOURCE: ClassVar[str] = 'invoices'
    RESPONSE_MODEL: ClassVar[Type[InvoiceResponse]] = InvoiceResponse
    ROOT_NAME: ClassVar[str] = 'invoice'


class FindInvoice(FindCommandMixin[InvoiceResponse], BaseOperation):
    """Find invoice by ID."""

    API_RESOURCE: ClassVar[str] = 'invoices'
    RESPONSE_MODEL: ClassVar[Type[InvoiceResponse]] = InvoiceResponse
    ROOT_NAME: ClassVar[str] = 'invoice'


class RefreshInvoice(BaseOperation):
    """Refresh a draft invoice."""

    API_RESOURCE: ClassVar[str] = 'invoices'
    RESPONSE_MODEL: ClassVar[Type[InvoiceResponse]] = InvoiceResponse
    ROOT_NAME: ClassVar[str] = 'invoice'

    def __call__(self, resource_id: str) -> InvoiceResponse:
        api_response: Response = send_put_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, 'refresh'),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )


class RetryPayment(BaseOperation):
    """Retry invoice payment."""

    API_RESOURCE: ClassVar[str] = 'invoices'
    RESPONSE_MODEL: ClassVar[Type[InvoiceResponse]] = InvoiceResponse
    ROOT_NAME: ClassVar[str] = 'invoice'

    def __call__(self, resource_id: str) -> InvoiceResponse:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, 'retry_payment'),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )


class UpdateInvoice(UpdateCommandMixin[InvoiceResponse], BaseOperation):
    """Update an existing invoice status."""

    API_RESOURCE: ClassVar[str] = 'invoices'
    RESPONSE_MODEL: ClassVar[Type[InvoiceResponse]] = InvoiceResponse
    ROOT_NAME: ClassVar[str] = 'invoice'


invoices_operations_config: Mapping[str, Callable[..., Callable]] = {
    'download': DownloadInvoice,
    'finalize': FinalizeInvoice,
    'find': FindInvoice,
    'find_all': FindAllInvoices,
    'refresh': RefreshInvoice,
    'retry_payment': RetryPayment,
    'update': UpdateInvoice,
}
