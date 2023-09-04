import urllib3
import requests
from api.base_api.utils import write_log

# Suppress InsecureRequestWarning
# https://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning-unverified-https-request-is-being-made-in-pytho
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HttpClient:

    def __init__(self, api_host, timeout=10):
        self.api_host = api_host
        self.timeout = timeout
        self.session = requests.session()

    def get(self, url, params=None, **kwargs):
        return self.request('get', url, params=params, **kwargs)

    def head(self, url, **kwargs):
        return self.request('head', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.request('post', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, json=None, **kwargs):
        return self.request('put', url, data=data, json=json, **kwargs)

    def patch(self, url, data=None, json=None, **kwargs):
        return self.request('patch', url, data=data, json=json, **kwargs)

    def delete(self, url, data=None, json=None, **kwargs):
        return self.request('delete', url, data=data, json=json, **kwargs)

    def request(self, method, endpoint, **kwargs):
        url = self.api_host + endpoint if 'http' not in endpoint else endpoint
        response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        write_log(response)
        return response
