from pydantic import BaseModel, Field
from typing import Optional


class OrganizationBillingConfiguration(BaseModel):
    invoice_footer: Optional[str]
    vat_rate: Optional[float]


class Organization(BaseModel):
    webhook_url: Optional[str]
    country: Optional[str]
    address_line1: Optional[str]
    address_line2: Optional[str]
    state: Optional[str]
    zipcode: Optional[str]
    email: Optional[str]
    city: Optional[str]
    legal_name: Optional[str]
    legal_number: Optional[str]
    billing_configuration: Optional[OrganizationBillingConfiguration]


class OrganizationResponse(BaseModel):
    name: str
    created_at: str
    webhook_url: Optional[str]
    country: Optional[str]
    address_line1: Optional[str]
    address_line2: Optional[str]
    state: Optional[str]
    zipcode: Optional[str]
    email: Optional[str]
    city: Optional[str]
    legal_name: Optional[str]
    legal_number: Optional[str]
    billing_configuration: Optional[OrganizationBillingConfiguration]
