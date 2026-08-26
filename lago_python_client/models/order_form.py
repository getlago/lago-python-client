from typing import Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel


class OrderFormMarkAsSigned(BaseModel):
    signed_document: Optional[str]
    execution_mode: Optional[str]
    execute_at: Optional[str]


class OrderFormResponse(BaseResponseModel):
    lago_id: str
    number: str
    status: str
    void_reason: Optional[str]
    expires_at: Optional[str]
    signed_at: Optional[str]
    voided_at: Optional[str]
    signed_document_url: Optional[str]
    lago_organization_id: str
    lago_customer_id: str
    lago_quote_id: str
    lago_quote_version_id: str
    created_at: str
    updated_at: str
