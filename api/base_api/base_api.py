import allure

from api.base_api.client import HttpClient


class BaseApi:
    """
    Base class for api testing
    """

    def __init__(self, api_host=None, timeout=5):
        self._http_client = HttpClient(api_host=api_host, timeout=timeout)

    @allure.step('GET: {1}')
    def get(self, url, params=None, **kwargs):
        response = self._http_client.get(url, params=params, verify=False, **kwargs)
        return response

    @allure.step('POST: {1}')
    def post(self, url, data=None, json=None, **kwargs):
        response = self._http_client.post(url, data=data, json=json, verify=False, **kwargs)
        return response

    def upload(self, url, files, **kwargs):
        """
        Для загрузки бинарных файлов
        :param url: str
        :param files: dict {'file': (str, bytes)}
        :param kwargs:
        :return: Response
        """
        with allure.step(f'POST: {url}'):
            response = self._http_client.post(url, data=None, json=None, files=files, verify=False, **kwargs)
            return response

    @allure.step('PUT: {1}')
    def put(self, url, data=None, json=None, **kwargs):
        response = self._http_client.put(url, data=data, json=json, verify=False, **kwargs)
        return response

    @allure.step('PATCH: {1}')
    def patch(self, url, data=None, json=None, **kwargs):
        response = self._http_client.patch(url, data=data, json=json, verify=False, **kwargs)
        return response

    @allure.step('DELETE: {1}')
    def delete_(self, url, data=None, json=None, **kwargs):
        response = self._http_client.delete(url, data=data, json=json, verify=False, **kwargs)
        return response

    @staticmethod
    def status_code_should_be(response, code):
        assert response.status_code == code, f'actual response code is not equal to expected:\n' \
                                             f'{response.status_code} != {code}'