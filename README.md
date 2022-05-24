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

## Development

### Install the dependencies

```bash
pip install .
```

### Run tests

```bash
python3 -m unittest tests
```
