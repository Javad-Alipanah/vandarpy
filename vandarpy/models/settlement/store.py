import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, Union

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
    done_time_prediction: Union[JalaliDateTime, datetime]
    is_instant: bool
    prediction: Prediction
    receipt_url: str
    type: Type
    source: str
    account: Optional[str]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status = Status(self.status)
        if isinstance(self.wallet, str):
            self.wallet = int(self.wallet)
            self.convert_wallet = True
        self.date = datetime.strptime(kwargs['settlement_date'], "%Y-%m-%d")
        if 'settlement_time' in kwargs:
            self.time = datetime.strptime(kwargs['settlement_time'], "%H:%M:%S")
        if 'settlement_date_jalali' in kwargs:
            self.date_jalali = JalaliDateTime.strptime(kwargs['settlement_date_jalali'], "%Y/%m/%d")
        if 'settlement_done_time_prediction' in kwargs:
            try:
                self.done_time_prediction = JalaliDateTime.strptime(kwargs['settlement_done_time_prediction'],
                                                                    "%Y/%m/%d %H:%M:%S")
            except ValueError:
                self.done_time_prediction = datetime.strptime(kwargs['settlement_done_time_prediction'],
                                                              "%Y-%m-%d %H:%M:%S")
        if 'prediction' in kwargs:
            self.prediction = self.Prediction(**kwargs['prediction'])
        if 'type' in kwargs:
            self.type = Type(self.type)

    def to_dict(self):
        data = super().to_dict().copy()
        del data['date']
        if 'convert_wallet' in data and data['convert_wallet']:
            data['wallet'] = str(data['wallet'])
            del data['convert_wallet']
        if 'time' in data:
            del data['time']
        if 'date_jalali' in data:
            del data['date_jalali']
        if 'done_time_prediction' in data:
            del data['done_time_prediction']
        return data


class BatchSettlementResponse(BaseModel):
    class Status(BaseModel):
        total_count: int
        total_amount: int
        init_count: int
        init_amount: int
        submitted_count: int
        submitted_amount: int
        failed_count: int
        failed_amount: int
        pending_count: int
        pending_amount: int
        canceled_count: int
        canceled_amount: int

    batch_id: str
    status: Status
    total_amount: int
    created_at: datetime
    cancelable: bool
    cancelable_datetime: Optional[datetime]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.created_at = datetime.fromtimestamp(kwargs['created_at'])
        if 'cancelable_datetime' in kwargs and kwargs['cancelable_datetime'] is not None:
            self.cancelable_datetime = datetime.fromtimestamp(kwargs['cancelable_datetime'])
        self.status = self.Status(**kwargs['status'])

    def to_dict(self):
        data = super().to_dict()
        data['created_at'] = int(data['created_at'].timestamp())
        if 'cancelable_datetime' in data and data['cancelable_datetime'] is not None:
            data['cancelable_datetime'] = int(data['cancelable_datetime'].timestamp())
        return data


class BatchSettlementDetail(BaseModel):
    id: str
    track_id: str
    payment_number: int
    amount: int
    iban: str
    status: Status
    type: Type
    transaction_id: int
    error_message: Optional[str]
    description: Optional[str]

    def __init__(self, id: str, track_id: str, payment_number: int, amount: int, iban: str, status: Status,
                 transaction_id: int, error_message: Optional[str] = None, description: Optional[str] = None, **kwargs):
        super().__init__(id=id, track_id=track_id, payment_number=payment_number, amount=amount, iban=iban,
                         status=status, transaction_id=transaction_id, error_message=error_message,
                         description=description, **kwargs)
        self.status = Status(self.status)
        self.payment_number = int(self.payment_number)
        self.amount = int(self.amount)
        self.transaction_id = int(self.transaction_id)

    def to_dict(self):
        data = super().to_dict().copy()
        data['payment_number'] = str(data['payment_number'])
        data['amount'] = str(data['amount'])
        if data['description'] is None:
            del data['description']
        return data
