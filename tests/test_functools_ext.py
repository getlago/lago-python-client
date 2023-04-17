import sys

import pytest

from lago_python_client.functools_ext import callable_cached_property


class InternalCollectionClient:
    def method(self) -> int:
        return 1


class Client:
    @callable_cached_property
    def collection(self) -> InternalCollectionClient:
        return InternalCollectionClient()


@pytest.mark.filterwarnings("ignore:We are going to deprecate callable properties")  # we need test both cases to ensure we keep compatibility
def test_callable_cached_property():
    # Given `InternalCollectionClient` class
    # And `Client` class with `callable_cached_property` decorator on `collection` method
    # And `client` instance
    client = Client()

    # When we call collection as a method
    method_result = client.collection().method()
    # Or as a property
    property_result = client.collection.method()

    # Then both results are equal
    assert property_result == method_result
    if sys.version_info >= (3, 8):
        # And collection objects are stored in cache during first request
        assert client.collection() == client.collection()
        assert client.collection == client.collection
        # ... but only for same `Client` instance
        assert Client().collection() != Client().collection()
        assert Client().collection != Client().collection
