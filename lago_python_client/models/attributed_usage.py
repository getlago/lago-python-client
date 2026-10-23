from typing import Dict, List, Optional

from ..base_model import BaseModel, BaseResponseModel


class AttributedChargeUsage(BaseModel):
    lago_charge_id: str
    charge_code: str
    billable_metric_code: str
    lago_charge_filter_id: Optional[str]
    charge_filter_values: Optional[Dict[str, List[str]]]
    charge_filter_invoice_display_name: Optional[str]
    units: str
    amount_cents: Optional[int]
    precise_amount_cents: Optional[str]
    events_count: int


class AttributedUsageAggregate(BaseModel):
    amount_cents: Optional[int]
    precise_amount_cents: Optional[str]
    events_count: int
    charges_usage: List[AttributedChargeUsage]


class AttributedUsageRow(AttributedUsageAggregate):
    value: Optional[str]
    rank: int


class AttributedUsageResponse(BaseResponseModel):
    lago_subscription_id: str
    external_subscription_id: str
    group_by: Optional[str]
    basis: str
    from_datetime: str
    to_datetime: str
    currency: str
    rows: List[AttributedUsageRow]
    unattributed: AttributedUsageAggregate
    totals: AttributedUsageAggregate
