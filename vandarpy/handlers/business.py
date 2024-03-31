from typing import cast

from apiclient.exceptions import APIClientError

from vandarpy.exceptions import VandarError
from vandarpy.handlers.base import BaseHandler
from vandarpy.models.business import Business, Iam
from vandarpy.endpoints.buisiness import BusinessEndpoint


class BusinessHandler(BaseHandler):
    def info(self, name: str) -> Business:
        return cast(
            Business,
            self._client.get_instance(BusinessEndpoint.info.format(name=name), Business)
        )

    def iam(self, name: str) -> Iam:
        page = 1
        per_page = 10
        users = []
        while True:
            try:
                response = self._client.get(
                    BusinessEndpoint.iam.format(name=name),
                    params={'page': page, 'per_page': per_page}
                )
                if not response.get('data') or not response['data'].get('users'):
                    break
                users.extend(response['data']['users'])
                page += 1
            except APIClientError as e:
                raise VandarError(e)
            if page > response['data']['last_page']:
                break

        return Iam.from_dict({'users': users})
