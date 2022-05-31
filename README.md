# Lago Python Client

This is a python wrapper for Lago API

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
from lago_python_client.models import Event

event = Event(
    customer_id="5eb02857-a71e-4ea2-bcf9-57d8885990ba",
    transaction_id="__UNIQUE_ID__",
    code="123",
    transaction_id="123",
    timestamp=1650893379,
    properties={"custom_field": "custom"}
)

client.events().create(event)
```

### Customers
[Api reference](https://doc.getlago.com/docs/api/customers/customer-object)

``` python
from lago_python_client.models import Customer

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
    zipcode=None
)
client.customers().create(customer)
```

### Subscriptions
[Api reference](https://doc.getlago.com/docs/api/subscriptions/subscription-object)

``` python
from lago_python_client.models import Subscription

subscription = Subscription(
    customer_id="5eb02857-a71e-4ea2-bcf9-57d8885990ba",
    plan_code="code"
)
client.subscriptions().create(subscription)

params_delete = {
    "customer_id": "5eb02857-a71e-4ea2-bcf9-57d8885990ba"
}
client.subscriptions().delete(params_delete)
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

The contribution documentation is available [here](https://github.com/getlago/lago-front/blob/main/CONTRIBUTING.md)

## License

Lago Node.js client is distributed under [AGPL-3.0](LICENSE).
