import unittest

from lago_python_client.services.request import make_url


class TestRequestServices(unittest.TestCase):
    """Test request services."""

    def test_make_url(self):
        """Make url."""
        # Given
        api_url = 'https://api.getlago.com/api/v1/'
        some_path_parts = ('team', 'anhtho', 'congratulate')
        query_name_value = {
            'message': "The future belongs to those who believe in the beauty of their dreams. Happy International Women's Day!",
            'date': '08.03.2023',
        }

        # When service is applied
        # Then
        self.assertEqual(
            make_url(origin=api_url, path_parts=some_path_parts, query_pairs=query_name_value), 
            'https://api.getlago.com/api/v1/team/anhtho/congratulate?message=The+future+belongs+to+those+who+believe+in+the+beauty+of+their+dreams.+Happy+International+Women%27s+Day%21&date=08.03.2023',
        )

    def test_make_url_no_query(self):
        """Make url without query name-value pairs."""
        # Given
        api_url = 'https://api.getlago.com/api/v1/'
        some_path_parts = ('hello', )

        # When service is applied
        # Then
        self.assertEqual(
            make_url(origin=api_url, path_parts=some_path_parts), 
            'https://api.getlago.com/api/v1/hello',
        )


if __name__ == '__main__':
    unittest.main()
