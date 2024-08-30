from typing import List, Optional

from lago_python_client.base_model import BaseModel

from .tax import TaxesResponse
from ..base_model import BaseResponseModel


class MinimumCommitment(BaseModel):
    amount_cents: Optional[int]
    invoice_display_name: Optional[str]
    tax_codes: Optional[List[str]]


class MinimumCommitmentResponse(BaseResponseModel):
    lago_id: str
    amount_cents: int
    invoice_display_name: Optional[str]
    interval: str
    taxes: Optional[TaxesResponse]
    created_at: Optional[str]
    updated_at: Optional[str]


class MinimumCommitmentOverrides(BaseModel):
    amount_cents: Optional[int]
    invoice_display_name: Optional[str]
    tax_codes: Optional[List[str]]
