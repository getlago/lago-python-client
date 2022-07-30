# Lago Python Client

This is a python wrapper for Lago API

[![PyPI version](https://badge.fury.io/py/lago-python-client.svg)](https://badge.fury.io/py/lago-python-client)

## Installation

Install the lago-python-client via pip from PyPI:

    $ pip install lago-python-client

## Usage

``` python
from lago_python_client import Client

client = Client(api_key = 'key')
```

### Events
[Api reference](https://doc.getlago.com/docs/api/events)

``` python
from lago_python_client.models import Event, BatchEvent

event = Event(
    customer_id="5eb02857-a71e-4ea2-bcf9-57d8885990ba",
    transaction_id="__UNIQUE_ID__",
    code="123",
    timestamp=1650893379,
    properties={"custom_field": "custom"}
)

client.events().create(event)

event = BatchEvent(
    subscription_ids=[
      "5eb02857-a71e-4ea2-bcf9-57d8885990ba", "8ztrg2857-a71e-4ea2-bcf9-57d8885990ba"],
    transaction_id="__UNIQUE_ID__",
    code="123",
    timestamp=1650893379,
    properties={"custom_field": "custom"}
)

client.events().batch_create(event)
```

``` python
transaction_id = "6afadc2a-f28c-40a4-a868-35636f229765"
event = client.events().find(transaction_id)
```

### Customers
[Api reference](https://doc.getlago.com/docs/api/customers/customer-object)

``` python
from lago_python_client.models import Customer, BillingConfiguration

customer = Customer(
    customer_id="5eb02857-a71e-4ea2-bcf9-57d8885990ba",
    address_line1=None,
    address_line2=None,
    city=None,
    country=None,
    email="test@example.com",
    legal_name=None,
    legal_number=None,
    logo_url=None,
    name="test name",
    phone=None,
    state=None,
    url=None,
    vat_rate=None,
    zipcode=None,
    billing_configuration=BillingConfiguration(
      payment_provider=None,
      provider_customer_id=None,
      sync=None
    )
)
client.customers().create(customer)
```

```python
customer_usage = client.customers().current_usage('customer_id', 'subscription_id')
```

### Invoices
[Api reference](https://doc.getlago.com/docs/api/invoices/invoice-object)

``` python
from lago_python_client.models import InvoiceStatusChange

status_change = InvoiceStatusChange(
    status="succeeded"
)
client.invoices().update(status_change, '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')

client.invoices().find('5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')

client.invoices().find_all({'per_page': 2, 'page': 1})
```

### Organizations
[Api reference](https://doc.getlago.com/docs/api/organizations/organization-object)

``` python
from lago_python_client.models import Organization

params = Organization(
    webhook_url="https://new.url",
    vat_rate=14.2
)
client.organizations().update(params)
```

#### Invoice Download

``` python
invoice = client.invoices().download('5eb02857-a71e-4ea2-bcf9-57d8885990ba')
```

### Subscriptions
[Api reference](https://doc.getlago.com/docs/api/subscriptions/subscription-object)

``` python
from lago_python_client.models import Subscription

subscription = Subscription(
    customer_id="5eb02857-a71e-4ea2-bcf9-57d8885990ba",
    plan_code="code",
    unique_id="12345",
    name="display name"
)
client.subscriptions().create(subscription)

update_params = Subscription(
    name='new name'
)
client.subscriptions().update(update_params, 'id')

client.subscriptions().destroy('id')

client.subscriptions().find_all({'customer_id': '123'})
```

### Applied coupons
[Api reference](https://doc.getlago.com/docs/api/applied_coupons/applied-coupon-object)

```python
from lago_python_client.models import AppliedCoupon

applied_coupon = AppliedCoupon(
  customer_id="5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba",
  coupon_code="code",
  amount_cents=123,
  amount_currency="EUR"
)

client.applied_coupons().create(applied_coupon)
```

### Applied add-ons
[Api reference](https://doc.getlago.com/docs/api/applied_add_ons/applied-add-on-object)

```python
from lago_python_client.models import AppliedAddOn

applied_add_on = AppliedAddOn(
  customer_id="5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba",
  add_on_code="code",
  amount_cents=123,
  amount_currency="EUR"
)

client.applied_add_ons().create(applied_add_on)
```

### Billable metrics
[Api reference](https://doc.getlago.com/docs/api/billable_metrics/billable-metric-object)

```python
from lago_python_client.models import BillableMetric

billable_metric = BillableMetric(
    name='name',
    code='code_first',
    description='desc',
    aggregation_type='sum_agg',
    field_name='amount_sum'
)
client.billable_metrics().create(billable_metric)

update_params = BillableMetric(
    name='new name'
)
client.billable_metrics().update(update_params, 'code')

client.billable_metrics().find('code')

client.billable_metrics().destroy('code')

client.billable_metrics().find_all({'per_page': 2, 'page': 1})
```

### Coupons
[Api reference](https://doc.getlago.com/docs/api/coupons/coupon-object)

```python
from lago_python_client.models import Coupon

coupon = Coupon(
    name='name',
    code='code_first',
    amount_cents=1000,
    amount_currency='EUR',
    expiration='no_expiration',
    expiration_duration=10
)
client.coupons().create(coupon)

update_params = Coupon(
    name='new name'
)
client.coupons().update(update_params, 'code')

client.coupons().find('code')

client.coupons().destroy('code')

client.coupons().find_all({'per_page': 2, 'page': 1})
```

### Add-ons
[Api reference](https://doc.getlago.com/docs/api/add_ons/add-on-object)

```python
from lago_python_client.models import AddOn

add_on = AddOn(
    name='name',
    code='code_first',
    amount_cents=1000,
    amount_currency='EUR',
    description='desc'
)
client.add_ons().create(add_on)

update_params = AddOn(
    name='new name'
)
client.add_ons().update(update_params, 'code')

client.add_ons().find('code')

client.add_ons().destroy('code')

client.add_ons().find_all({'per_page': 2, 'page': 1})
```

### Plans
[Api reference](https://doc.getlago.com/docs/api/plans/plan-object)

```python
from lago_python_client.models import Plan, Charges, Charge

charge = Charge(
    billable_metric_id='id',
    charge_model='standard',
    amount_currency='EUR',
    properties={
        'amount': '0.22'
    }
)
charges = Charges(__root__=[charge])

plan = Plan(
    name='name',
    code='code_first',
    amount_cents=1000,
    amount_currency='EUR',
    description='desc',
    interval='weekly',
    pay_in_advance=True,
    charges=charges
)
client.plans().create(plan)

update_params = Plan(
    name='new name'
)
client.plans().update(update_params, 'code')

client.plans().find('code')

client.plans().destroy('code')

client.plans().find_all({'per_page': 2, 'page': 1})
```

## Development

### Install the dependencies

```bash
pip install .
```

### Run tests

```bash
python3 -m unittest tests
```

## Documentation

The Lago documentation is available at [doc.getlago.com](https://doc.getlago.com/docs/api/intro).

## Contributing

The contribution documentation is available [here](https://github.com/getlago/lago-python-client/blob/main/CONTRIBUTING.md)

## License

Lago Python client is distributed under [AGPL-3.0](LICENSE).
