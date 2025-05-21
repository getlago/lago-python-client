from typing import Optional, List
from ..base_model import BaseModel, BaseResponseModel
from .tax import TaxesResponse
from datetime import datetime


class BillingEntityBillingConfiguration(BaseModel):
    invoice_footer: Optional[str]
    invoice_grace_period: Optional[int]
    document_locale: Optional[str]


class BillingEntity(BaseModel):
    code: str
    name: str
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zipcode: Optional[str]
    country: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    default_currency: Optional[str]
    timezone: Optional[str]
    document_numbering: Optional[str]
    document_number_prefix: Optional[str]
    finalize_zero_amount_invoice: Optional[bool]
    net_payment_term: Optional[int]
    eu_tax_management: Optional[bool]
    logo_url: Optional[str]
    legal_name: Optional[str]
    legal_number: Optional[str]
    tax_identification_number: Optional[str]
    email_settings: Optional[List[str]]
    billing_configuration: Optional[BillingEntityBillingConfiguration]


class BillingEntityUpdate(BaseModel):
    name: str
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zipcode: Optional[str]
    country: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    default_currency: Optional[str]
    timezone: Optional[str]
    document_numbering: Optional[str]
    document_number_prefix: Optional[str]
    finalize_zero_amount_invoice: Optional[bool]
    net_payment_term: Optional[int]
    eu_tax_management: Optional[bool]
    logo_url: Optional[str]
    legal_name: Optional[str]
    legal_number: Optional[str]
    tax_identification_number: Optional[str]
    tax_codes: Optional[List[str]]
    email_settings: Optional[List[str]]
    billing_configuration: Optional[BillingEntityBillingConfiguration]


class BillingEntityResponse(BaseResponseModel):
    lago_id: str
    code: str
    name: str
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zipcode: Optional[str]
    country: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    default_currency: Optional[str]
    timezone: Optional[str]
    document_numbering: Optional[str]
    document_number_prefix: Optional[str]
    finalize_zero_amount_invoice: Optional[bool]
    net_payment_term: Optional[int]
    eu_tax_management: Optional[bool]
    logo_url: Optional[str]
    legal_name: Optional[str]
    legal_number: Optional[str]
    tax_identification_number: Optional[str]
    is_default: bool
    logo_url: Optional[str]
    document_locale: Optional[str]
    invoice_footer: Optional[str]
    invoice_grace_period: Optional[int]
    email_settings: Optional[List[str]]
    taxes: Optional[TaxesResponse]
    created_at: datetime
    updated_at: datetime
