from datetime import datetime
from enum import Enum
from hashlib import sha256
from typing import Optional, List

from vandarpy.models.base import BaseModel
from vandarpy.models.business.transaction import Port
from vandarpy.utils.helpers import is_valid_phone_number, is_valid_card_number, is_valid_national_code


class Payment(BaseModel):
    api_key: str
    amount: int
    callback_url: str
    mobile_number: Optional[str]
    factor_number: Optional[str]
    description: Optional[str]
    national_code: Optional[str]
    valid_card_numbers: Optional[List[str]]
    comment: Optional[str]
    port: Optional[Port]

    def __init__(self, api_key: str, amount: int, callback_url: str,
                 mobile_number: Optional[str] = None, factor_number: Optional[str] = None,
                 description: Optional[str] = None, national_code: Optional[str] = None,
                 valid_card_numbers: Optional[List[str]] = None, comment: Optional[str] = None,
                 port: Optional[Port] = None, **kwargs):
        super().__init__(api_key=api_key, amount=amount, callback_url=callback_url,
                         mobile_number=mobile_number, factor_number=factor_number, description=description,
                         national_code=national_code, valid_card_numbers=valid_card_numbers, comment=comment,
                         port=port, **kwargs)
        if self.mobile_number is not None and not is_valid_phone_number(self.mobile_number):
            raise ValueError("Invalid mobile number.")
        if self.national_code is not None and not is_valid_national_code(self.national_code):
            raise ValueError("Invalid national code.")
        if self.valid_card_numbers is not None:
            if not isinstance(self.valid_card_numbers, list):
                raise ValueError("Valid card numbers should be a list.")
            for card_number in self.valid_card_numbers:
                if not is_valid_card_number(card_number):
                    raise ValueError("Invalid card number.")
        if self.port is not None:
            self.port = Port(self.port)

        if 'factorNumber' in kwargs:
            self.factor_number = kwargs['factorNumber']

    def to_dict(self):
        d = {k: v for k, v in self.__dict__.items() if v is not None}
        if 'factor_number' in d:
            d['factorNumber'] = d.pop('factor_number')
        if 'port' in d:
            d['port'] = d['port'].value
        return d

    def __str__(self):
        return f"<Payment: {self.amount} ({self.callback_url})>"

    def __repr__(self):
        return f"<Payment: {self.amount}>"


class Transaction(BaseModel):
    class Code(Enum):
        INVALID = 0
        PENDING = 1
        SUCCESS = 2
        EXPIRED = 3
        FAILED = 4

    status: int
    amount: float
    real_amount: Optional[int]
    wage: int
    trans_id: Optional[int]
    ref_number: Optional[str]
    tracking_code: Optional[str]
    factor_number: Optional[str]
    description: str
    mobile: str
    card_number: Optional[str]
    created_at: Optional[datetime]
    payment_start: Optional[datetime]
    payment_date: Optional[datetime]
    cid: str
    code: Optional[Code]
    port: Optional[Port]
    message: str

    def __init__(self, status: int, amount: float, wage: int, description: str, mobile: str, cid: str, message: str,
                 code: Optional[Code] = None, port: Optional[Port] = None, real_amount: Optional[int] = None,
                 trans_id: Optional[int] = None, ref_number: Optional[str] = None, tracking_code: Optional[str] = None,
                 factor_number: Optional[str] = None, card_number: Optional[str] = None,
                 created_at: Optional[datetime] = None, payment_start: Optional[datetime] = None,
                 payment_date: Optional[datetime] = None,
                 **kwargs):
        super().__init__(status=status, amount=amount, real_amount=real_amount, wage=wage, trans_id=trans_id,
                         ref_number=ref_number, tracking_code=tracking_code, factor_number=factor_number,
                         description=description, mobile=mobile, card_number=card_number, created_at=created_at,
                         payment_start=payment_start, payment_date=payment_date, cid=cid, code=code, port=port,
                         message=message, **kwargs)
        self.amount = float(self.amount)
        if 'realAmount' in kwargs:
            self.real_amount = kwargs['realAmount']
        self.wage = int(self.wage)
        if 'transId' in kwargs:
            self.trans_id = kwargs['transId']
        if 'refnumber' in kwargs:
            self.ref_number = kwargs['refnumber']
        if 'trackingCode' in kwargs:
            self.tracking_code = kwargs['trackingCode']
        if 'factorNumber' in kwargs:
            self.factor_number = kwargs['factorNumber']
        if 'cardNumber' in kwargs:
            self.card_number = kwargs['cardNumber']
        if 'createdAt' in kwargs:
            self.created_at = datetime.strptime(kwargs['createdAt'], '%Y-%m-%d %H:%M:%S')
        if 'paymentStart' in kwargs:
            self.payment_start = datetime.strptime(kwargs['paymentStart'], '%a %b %d %Y %H:%M:%S GMT%z')
        if 'paymentDate' in kwargs:
            self.payment_date = datetime.strptime(kwargs['paymentDate'], '%Y-%m-%d %H:%M:%S')
        if code is not None:
            self.code = self.Code(code)
        if port is not None:
            self.port = Port(port)

    def is_card_number_valid(self, expected_card_number: str) -> bool:
        return self.cid == sha256(expected_card_number.encode()).hexdigest().upper()

    def is_invalid(self):
        if self.code is None:
            return self.status != 1
        return self.code == self.Code.INVALID

    def is_pending(self):
        if self.code is None:
            raise ValueError("Transaction code is not set.")
        return self.code == self.Code.PENDING

    def is_successful(self):
        if self.code is None:
            return self.status == 1 and self.message == "ok"
        return self.code == self.Code.SUCCESS

    def is_expired(self):
        if self.code is None:
            raise ValueError("Transaction code is not set.")
        return self.code == self.Code.EXPIRED

    def is_failed(self):
        if self.code is None:
            return self.status != 1 or self.message != "ok"
        return self.code == self.Code.FAILED

    def to_dict(self):
        d = {k: v for k, v in self.__dict__.items() if v is not None}
        d['amount'] = f"{d['amount']:.2f}"
        if 'real_amount' in d:
            d['realAmount'] = d.pop('real_amount')
        d['wage'] = str(d['wage'])
        if 'trans_id' in d:
            d['transId'] = d.pop('trans_id')
        if 'ref_number' in d:
            d['refnumber'] = d.pop('ref_number')
        if 'tracking_code' in d:
            d['trackingCode'] = d.pop('tracking_code')
        if 'factor_number' in d:
            d['factorNumber'] = d.pop('factor_number')
        if 'card_number' in d:
            d['cardNumber'] = d.pop('card_number')
        if 'created_at' in d:
            d['createdAt'] = d.pop('created_at').strftime('%Y-%m-%d %H:%M:%S')
        if 'payment_start' in d:
            d['paymentStart'] = d.pop('payment_start').strftime('%a %b %d %Y %H:%M:%S GMT%z')
        if 'payment_date' in d:
            d['paymentDate'] = d.pop('payment_date').strftime('%Y-%m-%d %H:%M:%S')
        if 'code' in d:
            d['code'] = d['code'].value
        if 'port' in d:
            d['port'] = d['port'].value
        return d

    def __str__(self):
        return f"<Transaction: {self.trans_id} ({self.status})>"

    def __repr__(self):
        return f"<Transaction: {self.trans_id}>"
