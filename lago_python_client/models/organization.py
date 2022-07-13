from pydantic import BaseModel, Field
from typing import Optional


class Organization(BaseModel):
    webhook_url: Optional[str]
    vat_rate: Optional[float]
    country: Optional[str]
    address_line1: Optional[str]
    address_line2: Optional[str]
    state: Optional[str]
    zipcode: Optional[str]
    email: Optional[str]
    city: Optional[str]
    legal_name: Optional[str]
    legal_number: Optional[str]
    invoice_footer: Optional[str]


class OrganizationResponse(BaseModel):
    name: str
    created_at: str
    webhook_url: Optional[str]
    vat_rate: Optional[float]
    country: Optional[str]
    address_line1: Optional[str]
    address_line2: Optional[str]
    state: Optional[str]
    zipcode: Optional[str]
    email: Optional[str]
    city: Optional[str]
    legal_name: Optional[str]
    legal_number: Optional[str]
    invoice_footer: Optional[str]
