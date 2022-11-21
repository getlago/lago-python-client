from pydantic import BaseModel, Field
from typing import Optional


class CustomerBillingConfiguration(BaseModel):
    payment_provider: Optional[str]
    provider_customer_id: Optional[str]
    sync: Optional[bool]
    vat_rate: Optional[float]


class Customer(BaseModel):
    external_id: str
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    country: Optional[str]
    currency: Optional[str]
    email: Optional[str]
    legal_name: Optional[str]
    legal_number: Optional[str]
    logo_url: Optional[str]
    name: str
    phone: Optional[str]
    state: Optional[str]
    url: Optional[str]
    zipcode: Optional[str]
    billing_configuration: Optional[CustomerBillingConfiguration]


class CustomerResponse(BaseModel):
    lago_id: str
    external_id: str
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    country: Optional[str]
    currency: Optional[str]
    email: Optional[str]
    created_at: str
    legal_name: Optional[str]
    legal_number: Optional[str]
    logo_url: Optional[str]
    name: str
    phone: Optional[str]
    state: Optional[str]
    url: Optional[str]
    zipcode: Optional[str]
    billing_configuration: Optional[CustomerBillingConfiguration]
