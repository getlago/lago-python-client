from typing import Any, Dict, List, Optional

from lago_python_client.base_model import BaseModel

from .tax import TaxesResponse
from ..base_model import BaseResponseModel


class FixedChargeGraduatedRange(BaseModel):
    from_value: Optional[int]
    to_value: Optional[int]
    flat_amount: Optional[str]
    per_unit_amount: Optional[str]


class FixedChargeGraduatedRanges(BaseModel):
    __root__: List[FixedChargeGraduatedRange]


class FixedChargeProperties(BaseModel):
    amount: Optional[str]
    graduated_ranges: Optional[List[FixedChargeGraduatedRange]]
    volume_ranges: Optional[List[FixedChargeGraduatedRange]]


class FixedCharge(BaseModel):
    id: Optional[str]
    add_on_id: Optional[str]
    charge_model: Optional[str]
    code: Optional[str]
    invoice_display_name: Optional[str]
    units: Optional[float]
    pay_in_advance: Optional[bool]
    prorated: Optional[bool]
    properties: Optional[FixedChargeProperties]
    tax_codes: Optional[List[str]]
    apply_units_immediately: Optional[bool]


class FixedCharges(BaseModel):
    __root__: List[FixedCharge]


class FixedChargePropertiesResponse(BaseResponseModel):
    amount: Optional[str]
    graduated_ranges: Optional[List[FixedChargeGraduatedRange]]
    volume_ranges: Optional[List[FixedChargeGraduatedRange]]


class FixedChargeResponse(BaseResponseModel):
    lago_id: str
    lago_add_on_id: str
    invoice_display_name: str
    add_on_code: str
    created_at: str
    code: Optional[str]
    charge_model: str
    pay_in_advance: bool
    prorated: bool
    properties: Optional[FixedChargePropertiesResponse]
    units: Optional[float]
    lago_parent_id: Optional[str]
    taxes: Optional[TaxesResponse]


class FixedChargesResponse(BaseResponseModel):
    __root__: List[FixedChargeResponse]


class FixedChargeOverrides(BaseModel):
    id: Optional[str]
    invoice_display_name: Optional[str]
    units: Optional[float]
    apply_units_immediately: Optional[bool]
    properties: Optional[FixedChargeProperties]
    tax_codes: Optional[List[str]]


class FixedChargesOverrides(BaseModel):
    __root__: List[FixedChargeOverrides]
