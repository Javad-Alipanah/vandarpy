from typing import TYPE_CHECKING
if TYPE_CHECKING:  # pragma: no cover
    # Stupid way of getting around cyclic imports when
    # using type-hinting.
    from vandarpy.client import VandarClient

from typing import cast
from apiclient.exceptions import APIClientError

from vandarpy.exceptions import VandarError
from vandarpy.handlers.base import BaseHandler
from vandarpy.models.business.business import Business
from vandarpy.models.business.iam import Iam
from vandarpy.endpoints.buisiness import BusinessEndpoint
from vandarpy.models.business.wallet import Wallet


class BusinessHandler(BaseHandler):

    def __init__(self, client: "VandarClient", name: str):
        super().__init__(client)
        self._name = name

    def info(self) -> Business:
        return cast(
            Business,
            self._client.get_instance(BusinessEndpoint.info.format(name=self._name), Business)
        )

    def iam(self) -> Iam:
        page = 1
        per_page = 10
        users = []
        while True:
            try:
                response = self._client.get(
                    BusinessEndpoint.iam.format(name=self._name),
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
