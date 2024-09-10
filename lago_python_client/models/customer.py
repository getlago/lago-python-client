from typing import List, Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel

from .tax import TaxesResponse


class CustomerBillingConfiguration(BaseModel):
    invoice_grace_period: Optional[int]
    payment_provider: Optional[str]
    payment_provider_code: Optional[str]
    provider_customer_id: Optional[str]
    sync: Optional[bool]
    sync_with_provider: Optional[bool]
    document_locale: Optional[str]
    provider_payment_methods: Optional[List[str]]


class Address(BaseModel):
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    zipcode: Optional[str]
    state: Optional[str]
    country: Optional[str]


class IntegrationCustomer(BaseModel):
    id: Optional[str]
    external_customer_id: Optional[str]
    integration_type: Optional[str]
    integration_code: Optional[str]
    subsidiary_id: Optional[str]
    sync_with_provider: Optional[bool]


class IntegrationCustomerResponse(BaseModel):
    lago_id: Optional[str]
    external_customer_id: Optional[str]
    type: Optional[str]
    integration_code: Optional[str]
    subsidiary_id: Optional[str]
    sync_with_provider: Optional[bool]


class IntegrationCustomersList(BaseModel):
    __root__: List[IntegrationCustomer]


class IntegrationCustomersResponseList(BaseModel):
    __root__: List[IntegrationCustomerResponse]


class Metadata(BaseModel):
    id: Optional[str]
    key: Optional[str]
    value: Optional[str]
    display_in_invoice: Optional[bool]


class MetadataResponse(BaseModel):
    lago_id: Optional[str]
    key: Optional[str]
    value: Optional[str]
    display_in_invoice: Optional[bool]


class MetadataList(BaseModel):
    __root__: List[Metadata]


class MetadataResponseList(BaseModel):
    __root__: List[MetadataResponse]


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
    net_payment_term: Optional[int]
    tax_identification_number: Optional[str]
    logo_url: Optional[str]
    name: Optional[str]
    firstname: Optional[str]
    lastname: Optional[str]
    customer_type: Optional[str]
    phone: Optional[str]
    state: Optional[str]
    timezone: Optional[str]
    url: Optional[str]
    zipcode: Optional[str]
    metadata: Optional[MetadataList]
    finalize_zero_amount_invoice: Optional[str]
    billing_configuration: Optional[CustomerBillingConfiguration]
    shipping_address: Optional[Address]
    integration_customers: Optional[IntegrationCustomersList]
    tax_codes: Optional[List[str]]


class CustomerResponse(BaseResponseModel):
    lago_id: str
    external_id: str
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: Optional[str]
    country: Optional[str]
    currency: Optional[str]
    email: Optional[str]
    created_at: str
    updated_at: str
    legal_name: Optional[str]
    legal_number: Optional[str]
    net_payment_term: Optional[int]
    tax_identification_number: Optional[str]
    logo_url: Optional[str]
    name: Optional[str]
    firstname: Optional[str]
    lastname: Optional[str]
    customer_type: Optional[str]
    phone: Optional[str]
    state: Optional[str]
    timezone: Optional[str]
    applicable_timezone: str
    url: Optional[str]
    zipcode: Optional[str]
    metadata: Optional[MetadataResponseList]
    finalize_zero_amount_invoice: Optional[str]
    billing_configuration: Optional[CustomerBillingConfiguration]
    shipping_address: Optional[Address]
    integration_customers: Optional[IntegrationCustomersResponseList]
    taxes: Optional[TaxesResponse]
