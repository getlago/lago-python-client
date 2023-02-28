import requests

from .base_client import BaseClient
from lago_python_client.models.group import GroupResponse
from urllib.parse import urljoin, urlencode
from requests import Response
from ..services.json import from_json
from ..services.response import verify_response


class GroupClient(BaseClient):
    def api_resource(self):
        return 'groups'

    def root_name(self):
        return 'group'

    def prepare_response(self, data: dict):
        return GroupResponse.parse_obj(data)

    def find_all(self, metric_code: str, options: dict = {}):
        if options:
            api_resource = 'billable_metrics/' + metric_code + '/groups?' + urlencode(options)
        else:
            api_resource = 'billable_metrics/' + metric_code + '/groups'

        query_url = urljoin(self.base_url, api_resource)
        api_response = requests.get(query_url, headers=self.headers())
        data = from_json(verify_response(api_response))

        return self.prepare_index_response(data)
