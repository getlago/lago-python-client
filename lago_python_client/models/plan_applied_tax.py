from typing import Optional

from pydantic import BaseModel

from ..base_model import BaseResponseModel


class PlanAppliedTax(BaseModel):
    tax_code: str


class PlanAppliedTaxResponse(BaseResponseModel):
    lago_id: str
    lago_plan_id: str
    lago_tax_id: str
    plan_code: str
    tax_code: str
    created_at: str
