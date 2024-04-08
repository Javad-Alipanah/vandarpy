from typing import TYPE_CHECKING, Optional, List

from vandarpy.models.settlement.bank import Bank
from vandarpy.models.settlement.store import SettlementResponse, SettlementRequest

if TYPE_CHECKING:  # pragma: no cover
    # Stupid way of getting around cyclic imports when
    # using type-hinting.
    from vandarpy.client import VandarClient

from apiclient.exceptions import APIClientError

from vandarpy.endpoints.settlement import SettlementEndpoint
from vandarpy.exceptions import VandarError
from vandarpy.handlers.base import BaseHandler
from vandarpy.models.settlement.settlement import Settlement


class SettlementHandler(BaseHandler):
    def __init__(self, client: "VandarClient", business: str):
        super().__init__(client)
        self._business = business

    @property
    def settlements(self) -> list[Settlement]:
        settlements = []
        per_page = 10
        page = 1
        last_page = 1
        while page <= last_page:
            try:
                response = self._client.get(
                    SettlementEndpoint.list.format(business=self._business),
                    params={'page': page, 'per_page': per_page}
                )
                for settlement in response['data']['settlements']['data']:
                    settlements.append(Settlement.from_dict(settlement))
                last_page = response['data']['settlements']['last_page']
                page += 1
            except APIClientError as e:
                raise VandarError(e)
        return settlements

    @property
    def banks(self) -> list[Bank]:
        try:
            response = self._client.get(SettlementEndpoint.banks.format(business=self._business))
            return [Bank.from_dict(bank) for bank in response['data']]
        except APIClientError as e:
            raise VandarError(e)

    def create(self, request: SettlementRequest) -> List[SettlementResponse]:
        try:
            response = self._client.post(
                SettlementEndpoint.create.format(business=self._business),
                request.to_dict()
            )
            return [SettlementResponse.from_dict(settlement) for settlement in response['data']['settlement']]
        except APIClientError as e:
            raise VandarError(e)

    def get(self, settlement_id: str) -> SettlementResponse:
        try:
            response = self._client.get(
                SettlementEndpoint.get.format(business=self._business, settlement_id=settlement_id)
            )
            return SettlementResponse.from_dict(response['data']['settlement'])
        except APIClientError as e:
            raise VandarError(e)
