from typing import Optional, List

from pydantic import BaseModel

from ..base_model import BaseResponseModel


class OrganizationBillingConfiguration(BaseModel):
    invoice_footer: Optional[str]
    invoice_grace_period: Optional[int]
    vat_rate: Optional[float]
    document_locale: Optional[str]


class Organization(BaseModel):
    webhook_url: Optional[str]
    webhook_urls: Optional[List[str]]
    country: Optional[str]
    default_currency: str
    address_line1: Optional[str]
    address_line2: Optional[str]
    state: Optional[str]
    zipcode: Optional[str]
    email: Optional[str]
    city: Optional[str]
    legal_name: Optional[str]
    legal_number: Optional[str]
    document_numbering: Optional[str]
    document_number_prefix: Optional[str]
    net_payment_term: Optional[int]
    tax_identification_number: Optional[str]
    timezone: Optional[str]
    email_settings: Optional[List[str]]
    billing_configuration: Optional[OrganizationBillingConfiguration]


class OrganizationResponse(BaseResponseModel):
    name: str
    created_at: str
    webhook_url: Optional[str]
    webhook_urls: Optional[List[str]]
    country: Optional[str]
    address_line1: Optional[str]
    address_line2: Optional[str]
    state: Optional[str]
    zipcode: Optional[str]
    email: Optional[str]
    city: Optional[str]
    legal_name: Optional[str]
    legal_number: Optional[str]
    net_payment_term: Optional[int]
    document_numbering: Optional[str]
    document_number_prefix: Optional[str]
    tax_identification_number: Optional[str]
    timezone: Optional[str]
    email_settings: Optional[List[str]]
    billing_configuration: Optional[OrganizationBillingConfiguration]
