from lago_python_client.clients.subscription_client import SubscriptionClient
from lago_python_client.clients.customer_client import CustomerClient
from lago_python_client.clients.event_client import EventClient
from urllib.parse import urljoin


class Client:
    BASE_URL = 'https://api.getlago.com/'
    API_PATH = 'api/v1/'

    def __init__(self, api_key: str = None, api_url: str = None):
        self.api_key = api_key
        self.api_url = api_url

    def base_api_url(self):
        if self.api_url is None:
            return urljoin(Client.BASE_URL, Client.API_PATH)
        else:
            return urljoin(self.api_url, Client.API_PATH)

    def events(self):
        return EventClient(self.base_api_url(), self.api_key)

    def subscriptions(self):
        return SubscriptionClient(self.base_api_url(), self.api_key)

    def customers(self):
        return CustomerClient(self.base_api_url(), self.api_key)
