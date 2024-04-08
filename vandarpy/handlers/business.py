from typing import TYPE_CHECKING, Optional, List

from vandarpy.endpoints.invoice import InvoiceEndpoint
from vandarpy.endpoints.refund import RefundEndpoint
from vandarpy.handlers.settlement import SettlementHandler
from vandarpy.models.business.refund import Refund
from vandarpy.models.business.transaction import TransactionFilter, Transaction
from vandarpy.models.settlement.bank import Bank
from vandarpy.models.settlement.settlement import Settlement
from vandarpy.models.settlement.store import SettlementRequest, SettlementResponse, Type

if TYPE_CHECKING:  # pragma: no cover
    # Stupid way of getting around cyclic imports when
    # using type-hinting.
    from vandarpy.client import VandarClient

from typing import cast
from apiclient.exceptions import APIClientError

from vandarpy.exceptions import VandarError
from vandarpy.handlers.base import BaseHandler
from vandarpy.models.business.business import Business
from vandarpy.models.business.iam import User
from vandarpy.endpoints.buisiness import BusinessEndpoint
from vandarpy.models.business.wallet import Wallet


class BusinessHandler(BaseHandler):

    def __init__(self, client: "VandarClient", name: str):
        super().__init__(client)
        self._name = name
        self._settlement_handler = SettlementHandler(client, name)

    @property
    def info(self) -> Business:
        return cast(
            Business,
            self._client.get_instance(BusinessEndpoint.info.format(business=self._name), Business)
        )

    @property
    def iam(self) -> List[User]:
        page = 1
        per_page = 10
        users: List[User] = []
        while True:
            try:
                response = self._client.get(
                    BusinessEndpoint.iam.format(business=self._name),
                    params={'page': page, 'per_page': per_page}
                )
                if not response.get('data') or not response['data'].get('users'):
                    break
                for user in response['data']['users']:
                    users.append(User.from_dict(user))
                page += 1
            except APIClientError as e:
                raise VandarError(e)
            if page > response['data']['last_page']:
                break

        return users

    @property
    def wallet(self) -> Wallet:
        return cast(
            Wallet,
            self._client.get_instance(InvoiceEndpoint.balance.format(business=self._name), Wallet)
        )

    def transactions(self, transaction_filter: Optional[TransactionFilter] = None) -> List[Transaction]:
        transactions: List[Transaction] = []
        transaction_filter = transaction_filter or TransactionFilter()
        has_more = True
        try:
            while has_more:
                response = self._client.get(
                    InvoiceEndpoint.transactions.format(business=self._name),
                    params=transaction_filter.to_dict()
                )
                if not response.get('data') or response.get('status') != 1:
                    raise VandarError(response)
                for transaction in response['data']:
                    transactions.append(Transaction.from_dict(transaction))
                has_more = response['has_more']
                if len(transactions) > 0:
                    transaction_filter.start_after = transactions[-1].id
        except APIClientError as e:
            raise VandarError(e)

        return transactions

    def refund(self,
               transaction_id: int,
               amount: Optional[int] = None,
               comment: Optional[str] = None,
               description: Optional[str] = None,
               notify_url: Optional[str] = None,
               payment_number: Optional[str] = None) -> List[Refund]:
        data = {
            'amount': f"{amount:.2f}" if amount is not None else amount,
            'comment': comment,
            'description': description,
            'notify_url': notify_url,
            'payment_number': payment_number
        }
        data = {k: v for k, v in data.items() if v is not None}
        try:
            response = self._client.post(
                RefundEndpoint.refund.format(business=self._name, transaction_id=transaction_id),
                data=data
            )
        except APIClientError as e:
            raise VandarError(e)
        return [Refund.from_dict(refund) for refund in response['data']['results']]

    @property
    def settlements(self) -> List[Settlement]:
        return self._settlement_handler.settlements

    @property
    def banks(self) -> List[Bank]:
        return self._settlement_handler.banks

    @property
    def healthy_banks(self) -> List[Bank]:
        return [bank for bank in self.banks if bank.a2a.is_active and bank.a2a.has_ability and bank.a2a.is_healthy]

    def request_settlement(self, amount: int, iban: str, payment_number: Optional[int] = None,
                           notify_url: Optional[str] = None, description: Optional[str] = None,
                           is_instant: Optional[bool] = False, type: Optional[Type] = Type.INSTANT
                           ) -> List[SettlementResponse]:
        return self._settlement_handler.create(
            SettlementRequest(amount=amount, iban=iban, payment_number=payment_number, notify_url=notify_url,
                              description=description, is_instant=is_instant, type=type
                              )
        )

    def get_settlement(self, settlement_id: str):
        return self._settlement_handler.get(settlement_id)
