from typing import Any, Dict, List, Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel


class QuoteVersionApprove(BaseModel):
    expires_at: Optional[str]


class QuoteBillingItemAddOnResponse(BaseResponseModel):
    id: Optional[str]
    localId: Optional[str]
    type: Optional[str]
    payload: Optional[Dict[str, Any]]
    overrides: Optional[Dict[str, Any]]


class QuoteBillingItemPlanResponse(BaseResponseModel):
    id: Optional[str]
    localId: Optional[str]
    type: Optional[str]
    payload: Optional[Dict[str, Any]]
    overrides: Optional[Dict[str, Any]]


class QuoteBillingItemCouponResponse(BaseResponseModel):
    id: Optional[str]
    localId: Optional[str]
    type: Optional[str]
    payload: Optional[Dict[str, Any]]
    overrides: Optional[Dict[str, Any]]


class QuoteBillingItemWalletCreditResponse(BaseResponseModel):
    localId: Optional[str]
    type: Optional[str]
    payload: Optional[Dict[str, Any]]


class QuoteBillingItemsResponse(BaseResponseModel):
    addOns: Optional[List[QuoteBillingItemAddOnResponse]]
    plans: Optional[List[QuoteBillingItemPlanResponse]]
    coupons: Optional[List[QuoteBillingItemCouponResponse]]
    walletCredits: Optional[List[QuoteBillingItemWalletCreditResponse]]


class QuoteVersionResponse(BaseResponseModel):
    lago_id: str
    lago_quote_id: str
    lago_organization_id: str
    version: int
    status: str
    currency: Optional[str]
    billing_entity_code: Optional[str]
    void_reason: Optional[str]
    approved_at: Optional[str]
    voided_at: Optional[str]
    created_at: str
    updated_at: str
    # Only returned when a single version is retrieved.
    content: Optional[str]
    billing_items: Optional[QuoteBillingItemsResponse]


class QuoteOwnerResponse(BaseResponseModel):
    lago_id: str
    email: Optional[str]


class QuoteResponse(BaseResponseModel):
    lago_id: str
    number: str
    order_type: str
    lago_customer_id: str
    lago_subscription_id: Optional[str]
    lago_organization_id: str
    created_at: str
    updated_at: str
    current_version: Optional[QuoteVersionResponse]
    # Only returned when a single quote is retrieved.
    owners: Optional[List[QuoteOwnerResponse]]
