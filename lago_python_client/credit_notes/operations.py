import sys
from typing import ClassVar, Optional, Type

from ..base_operation import BaseOperation
from ..models.credit_note import CreditNoteResponse
from ..services.request import make_headers, make_url, send_post_request, send_put_request
from ..services.response import get_response_data, prepare_object_response, Response
from ..shared_operations import CreateCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin

if sys.version_info >= (3, 9):
    from collections.abc import Callable, Mapping
else:
    from typing import Callable, Mapping


class CreateCreditNote(CreateCommandMixin[CreditNoteResponse], BaseOperation):
    """Create a new Credit note."""

    API_RESOURCE: ClassVar[str] = 'credit_notes'
    RESPONSE_MODEL: ClassVar[Type[CreditNoteResponse]] = CreditNoteResponse
    ROOT_NAME: ClassVar[str] = 'credit_note'


class DownloadCreditNote(BaseOperation):
    """Download an existing credit note."""

    API_RESOURCE: ClassVar[str] = 'credit_notes'
    RESPONSE_MODEL: ClassVar[Type[CreditNoteResponse]] = CreditNoteResponse
    ROOT_NAME: ClassVar[str] = 'credit_note'

    def __call__(self, resource_id: str) -> Optional[CreditNoteResponse]:
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


class FindAllCreditNotes(FindAllCommandMixin[CreditNoteResponse], BaseOperation):
    """Find Credit notes."""

    API_RESOURCE: ClassVar[str] = 'credit_notes'
    RESPONSE_MODEL: ClassVar[Type[CreditNoteResponse]] = CreditNoteResponse
    ROOT_NAME: ClassVar[str] = 'credit_note'


class FindCreditNote(FindCommandMixin[CreditNoteResponse], BaseOperation):
    """Find credit note."""

    API_RESOURCE: ClassVar[str] = 'credit_notes'
    RESPONSE_MODEL: ClassVar[Type[CreditNoteResponse]] = CreditNoteResponse
    ROOT_NAME: ClassVar[str] = 'credit_note'


class UpdateCreditNote(UpdateCommandMixin[CreditNoteResponse], BaseOperation):
    """Update an existing credit note."""

    API_RESOURCE: ClassVar[str] = 'credit_notes'
    RESPONSE_MODEL: ClassVar[Type[CreditNoteResponse]] = CreditNoteResponse
    ROOT_NAME: ClassVar[str] = 'credit_note'


class VoidCreditNote(BaseOperation):
    """Void existing credit note."""

    API_RESOURCE: ClassVar[str] = 'credit_notes'
    RESPONSE_MODEL: ClassVar[Type[CreditNoteResponse]] = CreditNoteResponse
    ROOT_NAME: ClassVar[str] = 'credit_note'

    def __call__(self, resource_id: str) -> CreditNoteResponse:
        api_response: Response = send_put_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, 'void'),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )


credit_notes_operations_config: Mapping[str, Callable[..., Callable]] = {
    'create': CreateCreditNote,
    'download': DownloadCreditNote,
    'find': FindCreditNote,
    'find_all': FindAllCreditNotes,
    'update': UpdateCreditNote,
    'void': VoidCreditNote,
}
