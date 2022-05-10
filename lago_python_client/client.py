from lago_python_client.clients.subscription_client import SubscriptionClient
from lago_python_client.clients.customer_client import CustomerClient
from lago_python_client.clients.event_client import EventClient


class Client:
    BASE_URL = 'http://api.lago.dev/'
    API_PATH = 'api/v1/'

    def __init__(self, api_key: str = None, api_url: str = None):
        self.api_key = api_key
        self.api_url = api_url

    def base_api_url(self):
        if self.api_url is None:
            return Client.BASE_URL + Client.API_PATH
        else:
            return self.api_url + Client.API_PATH

    def events(self):
        return EventClient(self.base_api_url(), self.api_key)

    def subscriptions(self):
        return SubscriptionClient(self.base_api_url(), self.api_key)

    def customers(self):
        return CustomerClient(self.base_api_url(), self.api_key)
