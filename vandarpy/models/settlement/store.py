import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from persiantools.jdatetime import JalaliDateTime

from vandarpy.models.base import BaseModel
from vandarpy.models.settlement.settlement import Status


class Type(Enum):
    ACCOUNT_TO_ACCOUNT = "A2A"
    # Included for users not familiar with the term "A2A"
    INSTANT = "A2A"
    AUTOMATED_CLEARING_HOUSE = "ACH"
    # Included for users not familiar with the term "ACH"
    PAYA = "ACH"


class SettlementRequest(BaseModel):
    """
    SettlementRequest model
    Note: track_id is cannot be modified when creating this model and is automatically generated
    You can change it after creating the model, but it is not recommended
    Note: is_instant is optional and if not set, the settlement would be pending for at most 30 minutes,
    and then it will be sent to the bank; use it only if you want to send the settlement to the bank instantly
    """

    amount: int
    iban: str
    track_id: str
    payment_number: Optional[int]
    notify_url: Optional[str]
    description: Optional[str]
    is_instant: Optional[bool]
    type: Optional[Type]

    def __init__(self, amount: int, iban: str, payment_number: Optional[int] = None, notify_url: Optional[str] = None,
                 description: Optional[str] = None, is_instant: Optional[bool] = False,
                 type: Optional[Type] = Type.INSTANT, **kwargs):
        super().__init__(amount=amount, iban=iban, payment_number=payment_number, notify_url=notify_url,
                         description=description, is_instant=is_instant, type=type, **kwargs)
        self.type = Type(self.type)
        self.track_id = str(uuid.uuid4())

    def to_dict(self):
        data = super().to_dict()
        data = {k: v for k, v in data.items() if v is not None}
        return data

    def __str__(self):
        return f"<SettlementRequest: {self.id}>"

    def __repr__(self):
        return f"<SettlementRequest: {self.id}>"


class SettlementResponse(BaseModel):
    class Prediction(BaseModel):
        amount: int
        date: JalaliDateTime
        time: JalaliDateTime
        extra: str

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.date = JalaliDateTime.strptime(kwargs['date'], "%Y/%m/%d")
            self.time = JalaliDateTime.strptime(kwargs['time'], "%H:%M:%S")

        def to_dict(self):
            data = super().to_dict()
            data['date'] = data['date'].strftime("%Y/%m/%d").replace('/0', '/')
            data['time'] = data['time'].strftime("%H:%M:%S")
            return data

    id: str
    iban_id: str
    transaction_id: int
    amount: int
    amount_toman: int
    wage_toman: int
    payment_number: Optional[int]
    status: Status
    wallet: int
    description: Optional[str]
    date: datetime
    time: datetime
    date_jalali: JalaliDateTime
    done_time_prediction: JalaliDateTime
    is_instant: bool
    prediction: Prediction
    receipt_url: str
    type: Type
    source: str
    account: Optional[str]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status = Status(self.status)
        self.wallet = int(self.wallet)
        self.date = datetime.strptime(kwargs['settlement_date'], "%Y-%m-%d")
        self.time = datetime.strptime(kwargs['settlement_time'], "%H:%M:%S")
        self.date_jalali = JalaliDateTime.strptime(kwargs['settlement_date_jalali'], "%Y/%m/%d")
        self.done_time_prediction = JalaliDateTime.strptime(kwargs['settlement_done_time_prediction'],
                                                            "%Y/%m/%d %H:%M:%S")
        self.prediction = self.Prediction(**kwargs['prediction'])
        self.type = Type(self.type)

    def to_dict(self):
        data = super().to_dict().copy()
        del data['date']
        del data['time']
        del data['date_jalali']
        del data['done_time_prediction']
        data['wallet'] = str(data['wallet'])
        return data
