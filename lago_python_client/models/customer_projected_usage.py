from typing import Dict, List, Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel


class Metric(BaseModel):
    lago_id: str
    name: str
    code: str
    aggregation_type: str


class PricingUnitDetails(BaseModel):
    amount_cents: int
    short_name: str
    conversion_rate: float


class ProjectedChargeFilterUsage(BaseModel):
    invoice_display_name: Optional[str]
    values: Dict[str, List[str]]
    units: str
    projected_units: str
    amount_cents: int
    projected_amount_cents: int
    events_count: int
    pricing_unit_details: Optional[PricingUnitDetails]


class ChargeObject(BaseModel):
    lago_id: str
    charge_model: str
    invoice_display_name: Optional[str]


class ProjectedGroupedUsage(BaseModel):
    amount_cents: int
    projected_amount_cents: int
    events_count: int
    units: str
    projected_units: str
    grouped_by: Dict[str, str]
    filters: List[ProjectedChargeFilterUsage]
    pricing_unit_details: Optional[PricingUnitDetails]


class ProjectedChargeUsage(BaseModel):
    units: str
    projected_units: str
    events_count: int
    amount_cents: int
    projected_amount_cents: int
    amount_currency: str
    charge: ChargeObject
    billable_metric: Metric
    filters: List[ProjectedChargeFilterUsage]
    grouped_usage: Optional[List[ProjectedGroupedUsage]]
    pricing_unit_details: Optional[PricingUnitDetails]


class CustomerProjectedUsageResponse(BaseResponseModel):
    from_datetime: str
    to_datetime: str
    issuing_date: str
    invoice_id: Optional[str]
    currency: str
    amount_cents: int
    projected_amount_cents: int
    total_amount_cents: int
    taxes_amount_cents: int
    charges_usage: List[ProjectedChargeUsage]
