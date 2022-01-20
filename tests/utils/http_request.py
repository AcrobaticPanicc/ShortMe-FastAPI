import json


class HttpRequest:
    """
    Helper function used to send http requests
    """

    def __init__(self, base_url, client):
        self.base_url = base_url
        self.client = client

    def _api_request(self, http_method, url, data=None, headers=None, timeout=360, **kwargs):
        response = self.client.request(method=http_method, url=url, headers=headers, data=data, timeout=timeout, **kwargs)
        return response

    def get(self, path, headers=None, **kwargs):
        return self._api_request('get', path, headers=headers, **kwargs)

    def post(self, path, data=None, json=None, files=None, headers=None, **kwargs):
        return self._api_request('post', path, data=data, json=json, files=files, headers=headers, **kwargs)

    def put(self, path, data=None, headers=None, **kwargs):
        return self._api_request('put', path, data=data, headers=headers, **kwargs)

    def delete(self, path, data=None, headers=None, **kwargs):
        return self._api_request('delete', path, data=data, headers=headers, **kwargs)

