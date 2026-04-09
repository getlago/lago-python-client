from typing import List, Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel


class InvoiceCustomSectionInput(BaseModel):
    skip_invoice_custom_sections: Optional[bool]
    invoice_custom_section_codes: Optional[List[str]]


class InvoiceCustomSectionResponse(BaseResponseModel):
    lago_id: Optional[str]
    code: Optional[str]
    name: Optional[str]
    description: Optional[str]
    details: Optional[str]
    display_name: Optional[str]
    applied_to_organization: Optional[bool]  # Deprecated


class AppliedInvoiceCustomSection(BaseResponseModel):
    lago_id: Optional[str]
    created_at: Optional[str]
    invoice_custom_section: Optional[InvoiceCustomSectionResponse]


class AppliedInvoiceCustomSections(BaseResponseModel):
    __root__: List[AppliedInvoiceCustomSection]


class InvoiceCustomSectionsResponseList(BaseResponseModel):
    __root__: List[InvoiceCustomSectionResponse]
