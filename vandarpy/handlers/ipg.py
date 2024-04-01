from typing import TYPE_CHECKING, cast

from apiclient.exceptions import APIClientError

from vandarpy.exceptions import VandarError

if TYPE_CHECKING:  # pragma: no cover
    # Stupid way of getting around cyclic imports when
    # using type-hinting.
    from vandarpy.client import VandarClient
from vandarpy.endpoints.ipg import IPGEndpoint
from vandarpy.handlers.base import BaseHandler
from vandarpy.models.ipg import Payment, Transaction


class IPGHandler(BaseHandler):

    def __init__(self, client: "VandarClient", api_key: str):
        super().__init__(client)
        self._api_key = api_key

    def get_payment(self, amount: int, callback_url: str) -> Payment:
        """Create a new Payment object.
        By calling this method, you can create a new Payment object
        Be sure to fill the desired fields before calling get_token method.
        """
        return Payment(api_key=self._api_key, amount=amount, callback_url=callback_url)

    def get_token(self, payment: Payment) -> str:
        try:
            response = self._client.post(IPGEndpoint.token, payment.to_dict())
            if 'status' not in response or response['status'] != 1:
                raise VandarError(f"Failed to get token: {response['errors']}")
        except APIClientError as e:
            raise VandarError(e)

        return response['token']

    @staticmethod
    def get_redirect_url(token: str) -> str:
        return IPGEndpoint.redirect.format(token=token)

    def get_transaction_info(self, token: str) -> Transaction:
        return cast(
            Transaction,
            self._client.create_instance(IPGEndpoint.info,
                                         data={"token": token, "api_key": self._api_key}, model=Transaction)
        )

    def verify_transaction(self, token: str) -> Transaction:
        return cast(
            Transaction,
            self._client.create_instance(IPGEndpoint.verify,
                                         data={"token": token, "api_key": self._api_key}, model=Transaction)
        )
