import unittest

from lago_python_client.functools_ext import callable_cached_property


class TestFunctoolsExt(unittest.TestCase):
    def test_callable_cached_property(self):
        # Given `InternalCollectionClient` class
        class InternalCollectionClient:
            def method(self) -> int:
                return 1

        # And `Client` class with `callable_cached_property` decorator on `collection` method
        class Client:
            @callable_cached_property
            def collection(self) -> InternalCollectionClient:
                return InternalCollectionClient()


        # And `client` instance
        client = Client()

        # When we call collection as a method
        method_result = client.collection().method()
        # Or as a property
        property_result = client.collection.method()

        # Then both results are equal
        self.assertEqual(property_result, method_result)
        # And collection objects are stored in cache during first request
        self.assertEqual(client.collection(), client.collection())
        self.assertEqual(client.collection, client.collection)
        # ... but only for same `Client` instance
        self.assertNotEqual(Client().collection(), Client().collection())
        self.assertNotEqual(Client().collection, Client().collection)


if __name__ == '__main__':
    unittest.main()
