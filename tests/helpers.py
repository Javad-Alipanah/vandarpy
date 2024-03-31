import json
from typing import Callable

import requests
from apiclient.exceptions import UnexpectedError
from apiclient.request_strategies import RequestStrategy
from apiclient.response import RequestsResponse, Response
from apiclient.utils.typing import OptionalDict


class MockRequestStrategy(RequestStrategy):
    def __init__(self):
        with open("tests/endpoints.json", 'r', encoding="utf-8") as f:
            self.endpoints = json.load(f)

    def _make_request(
            self,
            request_method: Callable,
            endpoint: str,
            params: OptionalDict = None,
            headers: OptionalDict = None,
            data: OptionalDict = None,
            **kwargs,
    ) -> Response:
        """Make the request with the given method.

        Delegates response parsing to the response handler.
        """
        method = getattr(self, request_method.__name__.lower() + "_mock")
        try:
            response = RequestsResponse(
                method(
                    endpoint,
                    params=self._get_request_params(params),
                    headers=self._get_request_headers(headers),
                    auth=self._get_username_password_authentication(),
                    data=self._get_formatted_data(data),
                    timeout=self._get_request_timeout(),
                    **kwargs,
                )
            )
        except Exception as error:
            raise UnexpectedError(f"Error when contacting '{endpoint}'") from error
        else:
            self._check_response(response)
        return self._decode_response_data(response)

    def get_mock(self, url, params=None, **kwargs):
        r = requests.Response()
        r.status_code = 200
        r._content = json.dumps(self.endpoints[url]["GET"]["response"]).encode()
        return r

    def post_mock(self, url, data=None, **kwargs):
        r = requests.Response()
        r.status_code = 200
        r._content = json.dumps(self.endpoints[url]["POST"]["response"]).encode()
        return r

    def put_mock(self, url, data=None, **kwargs):
        r = requests.Response()
        r.status_code = 200
        r._content = json.dumps(self.endpoints[url]["PUT"]["response"]).encode()
        return r

    def delete_mock(self, url, **kwargs):
        r = requests.Response()
        r.status_code = 200
        r._content = json.dumps(self.endpoints[url]["DELETE"]["response"]).encode()
        return r
