from typing import Optional

from pydantic import BaseModel

from ..base_model import BaseResponseModel


class AppliedTaxRate(BaseModel):
    tax_rate_code: str


class AppliedTaxRateResponse(BaseResponseModel):
    lago_id: str
    lago_customer_id: str
    lago_tax_rate_id: str
    tax_rate_code: str
    external_customer_id: str
    created_at: str
