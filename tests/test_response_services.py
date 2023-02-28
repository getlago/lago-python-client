from copy import deepcopy
import unittest

from requests import Request, Response

from lago_python_client.exceptions import LagoApiError
from lago_python_client.services.response import RESPONSE_SUCCESS_CODES, _is_status_code_successful, _is_content_exists, verify_response


class TestResponseServices(unittest.TestCase):
    """Test response services."""

    def test_success_status_codes_exists(self):
        """Ensure ``RESPONSE_SUCCESS_CODES`` is set."""
        self.assertTrue(len(RESPONSE_SUCCESS_CODES) >= 4)

    def test_is_status_code_successful(self):
        """Check status code is successful."""
        # Given instanse of ``requests.Response`` class with successful status code
        response = Response()
        response._content_consumed = True
        response._content = b'{"a":{"b":"c"}}'
        response.status_code = 200
        # ... and with error status code
        response404 = deepcopy(response)
        response404._content = b''
        response404.status_code = 404

        # When check helper function is applied
        # Then verification passes.
        self.assertEqual(_is_status_code_successful(response), True)
        # ... or not
        self.assertEqual(_is_status_code_successful(response404), False)

    def test_is_content_exists(self):
        """Check content exists."""
        # Given instanse of ``requests.Response`` class with content
        response = Response()
        response._content_consumed = True
        response._content = b'{"a":{"b":"c"}}'
        response.status_code = 200
        # ... and with empty content
        response204 = deepcopy(response)
        response204._content = b''
        response204.status_code = 204

        # When check helper function is applied
        # Then verification passes.
        self.assertEqual(_is_content_exists(response), True)
        # ... or not
        self.assertEqual(_is_content_exists(response204), False)

    def test_verify_response(self):
        """Verify response."""
        # Given instanse of ``requests.Response`` class with successful status code and content
        response = Response()
        response._content_consumed = True
        response._content = b'{"a":{"b":"c"}}'
        response.status_code = 200
        # ... and with successful status code and empty content
        response204 = deepcopy(response)
        response204._content = b''
        response204.status_code = 204
        # ... and with error status code
        response404 = deepcopy(response)
        response404.status_code = 404
        response404.request = Request(url='')

        # When service is applied
        # Then
        self.assertEqual(verify_response(response), response)
        self.assertEqual(verify_response(response204), None)
        with self.assertRaises(LagoApiError):
            verify_response(response404)


if __name__ == '__main__':
    unittest.main()
