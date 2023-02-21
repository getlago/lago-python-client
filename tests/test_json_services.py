import unittest

from requests import Response

from lago_python_client.services.json import from_json, to_json


class TestJSONServices(unittest.TestCase):
    """Test JSON services."""

    def test_from_json(self):
        """Deserialize data from json string."""
        # Given some data
        expected_data = {'a': {'b': 'c'}}
        # And same data serialized in json format stored as string,
        json_string = '{"a":{"b":"c"}}'
        # ... or bytes,
        json_bytes = b'{"a":{"b":"c"}}'
        # ... or even available as ``content`` property of instanse of ``requests.Response`` class
        json_requests_response = Response()
        json_requests_response._content_consumed = True
        json_requests_response._content = json_bytes
        json_requests_response.status_code = 200

        # When service is applied
        # Then service result is equal to given data.
        self.assertEqual(from_json(json_string), expected_data)
        self.assertEqual(from_json(json_bytes), expected_data)
        self.assertEqual(from_json(json_requests_response), expected_data)

    def test_to_json(self):
        """Serialize data to json string."""
        # Given some data
        initial_data = {'a': {'b': 'c'}}
        # And same data serialized in json format
        expected_json_string = '{"a":{"b":"c"}}'

        # When service is applied
        # Then service result is equal to given serialized json string.
        self.assertEqual(to_json(initial_data), expected_json_string)


if __name__ == '__main__':
    unittest.main()
