from typing import Optional, List, Dict

from persiantools.jdatetime import JalaliDateTime

from vandarpy.models.base import BaseModel
from vandarpy.models.settlement.settlement import Status


class Refund(BaseModel):
    id: str
    retry_count: str
    gateway_transaction_id: int
    amount: int
    wage: int
    payment_number: Optional[str]
    status: Status
    description: str
    wallet: int
    refund_date: JalaliDateTime
    created_at: JalaliDateTime
    receipt_url: Optional[str]

    def __init__(self, id: str, retry_count: str, gateway_transaction_id: int, amount: int, wage: int,
                 payment_number: Optional[str], status: str, description: str, wallet: int,
                 refund_date: JalaliDateTime,
                 created_at: JalaliDateTime, receipt_url: Optional[str], **kwargs):
        super().__init__(id=id, retry_count=retry_count, gateway_transaction_id=gateway_transaction_id,
                         amount=amount,
                         wage=wage, payment_number=payment_number, status=status, description=description,
                         wallet=wallet,
                         refund_date=refund_date, created_at=created_at, receipt_url=receipt_url, **kwargs)
        self.wallet = int(wallet)
        self.status = Status(status)
        self.refund_date = JalaliDateTime.strptime(self.refund_date, '%Y/%m/%d %H:%M:%S')
        self.created_at = JalaliDateTime.strptime(self.created_at, '%Y/%m/%d %H:%M:%S')

    def to_dict(self) -> dict:
        d = {k: v for k, v in self.__dict__.items()}
        d['refund_date'] = d['refund_date'].strftime('%Y/%m/%d %H:%M:%S')
        d['created_at'] = d['created_at'].strftime('%Y/%m/%d %H:%M:%S')
        d['wallet'] = str(d['wallet'])
        d['status'] = d['status'].value
        return d

    def is_successful(self) -> bool:
        return self.status == Status.DONE

    def is_pending(self) -> bool:
        return self.status == Status.PENDING

    def is_failed(self) -> bool:
        return self.status == Status.FAILED

    def is_canceled(self) -> bool:
        return self.status == Status.CANCELED

    def __str__(self) -> str:
        return f"<Refund: {self.id} ({self.status})>"

    def __repr__(self) -> str:
        return f"<Refund: {self.id}>"