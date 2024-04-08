from datetime import datetime
from enum import Enum
from typing import Optional

from vandarpy.models.base import BaseModel


class Status(Enum):
    PENDING = "PENDING"
    INITIATED = "INIT"
    SUBMITTED = "SUBMITTED"
    DONE = "DONE"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


class Settlement(BaseModel):
    id: str
    iban_id: Optional[int]
    gateway_transaction_id: int
    amount: int
    payment_number: Optional[int]
    status: Status
    wallet: int
    date: datetime
    done_time_prediction: datetime
    description: Optional[str]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status = Status(self.status)
        self.date = datetime.strptime(kwargs['settlement_date'], "%Y-%m-%d")
        self.done_time_prediction = datetime.strptime(kwargs['settlement_done_time_prediction'],
                                                      "%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        data = super().to_dict()
        data['settlement_date'] = data.pop('date').strftime("%Y-%m-%d")
        data['settlement_done_time_prediction'] = data.pop('done_time_prediction').strftime("%Y-%m-%d %H:%M:%S")
        return data

    def __str__(self):
        return f"<Settlement: {self.id} ({self.status})>"

    def __repr__(self):
        return f"<Settlement: {self.id}>"
