from lago_python_client.client import Client


def test_base_url_when_api_url_is_given():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d',
                    api_url='https://example.com/')

    assert client.base_api_url == 'https://example.com/api/v1/'


def test_base_url_when_api_url_is_not_given():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    assert client.base_api_url == 'https://api.getlago.com/api/v1/'
