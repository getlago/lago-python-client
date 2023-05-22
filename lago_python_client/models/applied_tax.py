from typing import Optional

from pydantic import BaseModel

from ..base_model import BaseResponseModel


class AppliedTax(BaseModel):
    tax_code: str


class AppliedTaxResponse(BaseResponseModel):
    lago_id: str
    lago_customer_id: str
    lago_tax_id: str
    tax_code: str
    external_customer_id: str
    created_at: str
