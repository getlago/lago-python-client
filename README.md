# Lago Python Client

This is a python wrapper for Lago API

[![PyPI version](https://badge.fury.io/py/lago-python-client.svg)](https://badge.fury.io/py/lago-python-client)

## Installation

Install the lago-python-client via pip from PyPI:

    $ pip install lago-python-client

## Usage

Check the [lago API reference](https://doc.getlago.com/docs/api/intro)

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

## Changelog

* [#55](https://github.com/getlago/lago-python-client/pull/55) -- Error handling (`LagoApiError`)


Example, creating wallet: 

```
try:
    response = client.wallets().create(wallet)
except LagoApiError as error:
    do_something(status=error.status_code)
```
### Available properties:
```
>>> error.status_code
422

>>> error.detail
'Unprocessable Entity'

>>> error.headers
{'X-Frame-Options': 'SAMEORIGIN', 'X-XSS-Protection': '0', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Permitted-Cross-Domain-Policies': 'none', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-cache', 'X-Request-Id': '613e7542-b29e-4224-bd19-a16dd1bfa62b', 'X-Runtime': '1.024304', 'Vary': 'Origin', 'Transfer-Encoding': 'chunked'}

>>> error.response
{'status': 422, 'error': 'Unprocessable Entity', 'code': 'validation_errors', 'error_details': {'customer': ['wallet_already_exists']}}

>>> error.response['error_details']['customer'][0]
'wallet_already_exists'


>>> error.url
'http://localhost:3000/api/v1/wallets'
```


## Contributing

The contribution documentation is available [here](https://github.com/getlago/lago-python-client/blob/main/CONTRIBUTING.md)

## License

Lago Python client is distributed under [AGPL-3.0](LICENSE).
