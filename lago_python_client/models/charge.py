from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .tax import TaxesResponse
from ..base_model import BaseResponseModel


class GroupProperties(BaseModel):
    group_id: Optional[str]
    values: Optional[Dict[str, Any]]
    invoice_display_name: Optional[str]


class GroupPropertiesList(BaseModel):
    __root__: List[GroupProperties]


class Charge(BaseModel):
    id: Optional[str]
    billable_metric_id: Optional[str]
    charge_model: Optional[str]
    pay_in_advance: Optional[bool]
    prorated: Optional[bool]
    invoiceable: Optional[bool]
    invoice_display_name: Optional[str]
    min_amount_cents: Optional[int]
    properties: Optional[Dict[str, Any]]
    group_properties: Optional[GroupPropertiesList]
    tax_codes: Optional[List[str]]


class Charges(BaseModel):
    __root__: List[Charge]


class ChargeResponse(BaseResponseModel):
    lago_id: Optional[str]
    lago_billable_metric_id: Optional[str]
    billable_metric_code: Optional[str]
    charge_model: Optional[str]
    pay_in_advance: Optional[bool]
    prorated: Optional[bool]
    invoiceable: Optional[bool]
    invoice_display_name: Optional[str]
    min_amount_cents: Optional[int]
    properties: Optional[Dict[str, Any]]
    group_properties: Optional[GroupPropertiesList]
    taxes: Optional[TaxesResponse]


class ChargesResponse(BaseResponseModel):
    __root__: List[ChargeResponse]


class ChargeOverrides(BaseModel):
    id: Optional[str]
    invoice_display_name: Optional[str]
    min_amount_cents: Optional[int]
    properties: Optional[Dict[str, Any]]
    group_properties: Optional[GroupPropertiesList]
    tax_codes: Optional[List[str]]


class ChargesOverrides(BaseModel):
    __root__: List[ChargeOverrides]