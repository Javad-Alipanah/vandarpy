from typing import Optional, Union, List, Dict

from vandarpy.models.base import BaseModel
from datetime import date
from persiantools.jdatetime import JalaliDate, JalaliDateTime
from enum import Enum


class Port(Enum):
    SAMAN = "SAMAN"
    BEHPARDAKHT = "BEHPARDAKHT"


class TransactionFilter(BaseModel):
    class StatusKind(Enum):
        SETTLEMENTS = 'settlements'
        TRANSACTIONS = 'transactions'

    class Status(Enum):
        SUCCESS = 'succeed'
        FAILED = 'failed'
        PENDING = 'pending'
        CANCELED = 'canceled'

    class Channel(Enum):
        IPG = 'ipg'
        FORM = 'form'
        REFUND = 'refund'
        SUBSCRIPTION = 'subscription'
        SETTLEMENTS = 'settlements'
        CASH_IN = 'cash-in'
        POS = 'pos'
        SHAPARAK_SETTLEMENT = 'shaparak-settlement'
        CASH_IN_BY_CODE = 'cash-in-by-code'

    from_date: Union[date, JalaliDate, str, None]
    to_date: Union[date, JalaliDate, str, None]
    status_kind: Optional[StatusKind]
    status: Optional[Status]
    channel: Optional[Channel]
    form_id: Optional[str]
    ref_id: Optional[str]
    tracking_code: Optional[str]
    id: Optional[str]
    track_id: Optional[str]
    factor_number: Optional[str]
    per_page: Optional[int]

    # id of the last transaction in the previous page
    start_after: Optional[str]
    query: Optional[str]
    search_field: Optional[str]

    def __init__(self, from_date: Union[date, JalaliDate, str, None] = None,
                 to_date: Union[date, JalaliDate, str, None] = None,
                 status_kind: Optional[StatusKind] = None,
                 status: Optional[Status] = None,
                 channel: Optional[Channel] = None,
                 form_id: Optional[str] = None,
                 ref_id: Optional[str] = None,
                 tracking_code: Optional[str] = None,
                 id: Optional[str] = None,
                 track_id: Optional[str] = None,
                 factor_number: Optional[str] = None,
                 per_page: Optional[int] = None,
                 start_after: Optional[str] = None,
                 query: Optional[str] = None,
                 search_field: Optional[str] = None):
        super().__init__(from_date=from_date, to_date=to_date, status_kind=status_kind, status=status,
                         channel=channel, form_id=form_id, ref_id=ref_id, tracking_code=tracking_code, id=id,
                         track_id=track_id, factor_number=factor_number, per_page=per_page, start_after=start_after,
                         query=query, search_field=search_field)

    def to_dict(self):
        d = {k: v for k, v in self.__dict__.items() if v is not None}
        for k, v in d.items():
            if isinstance(v, Enum):
                d[k] = v.value
            elif isinstance(v, date) or isinstance(v, JalaliDate):
                jdate = JalaliDate(v)
                if jdate.year < 1400:
                    d[k] = jdate.strftime('%y%m%d')
                else:
                    d[k] = jdate.strftime('%Y%m%d')

        return d


class Transaction(BaseModel):
    class Status(Enum):
        SUCCESSFUL_TRANSACTION = 1
        FAILED_TRANSACTION = -1
        SUCCESSFUL_SETTLEMENT = 2
        PENDING_SETTLEMENT = -2
        PENDING_TRANSACTION = 3
        FAILED_SETTLEMENT = -3
        CORRECTED_TRANSACTION = 4
        CANCELED_SETTLEMENT = -4
        INTERNAL_DEPOSIT = 5
        INTERNAL_WITHDRAW = -5
        SUBSCRIPTION = 6
        RETURNED_FROM_BANK_OR_VANDAR = -6

    class Person(BaseModel):
        ip: Optional[str]
        iban: Optional[str]
        name: str
        slug: Optional[str]
        avatar: Optional[str]
        legal_name: Optional[str]
        business_owner: Optional[str]
        email: Optional[str]
        phone: Optional[str]
        address: Optional[str]
        mobile: Optional[str]
        additional_fields: List[Dict[str, str]]
        description: Optional[str]

    class TimePrediction(BaseModel):
        is_admin_check_status: bool
        has_change_done_time_prediction: bool
        is_cancelable: bool
        has_change_port_to_paya: bool
        settlement_done_time_prediction: Optional[str]
        settlement_cancelable_time: Optional[str]
        is_settlement_paya_report_finally: Optional[str]
        settlement_paya_report_finally_time: Optional[str]
        is_after_time_prediction: Optional[str]
        is_after_cancelable: Optional[str]
        p2p_time_prediction: Optional[str]

    id: int
    track_id: Optional[str]
    amount: int
    wage: int
    status: Status
    ref_id: str
    tracking_code: str
    card_number: str
    cid: str
    verified: int
    channel: str
    payment_date: JalaliDateTime
    payment_number: Optional[str]
    created_at: JalaliDateTime
    effective_at_jalali: JalaliDateTime
    effective_time_stamp: int
    updated_at: JalaliDateTime
    wallet: int
    result: str
    description: Optional[str]
    factor_number: Optional[str]
    mobile: Optional[str]
    callback_url: Optional[str]
    form_id: Optional[int]
    form_title: Optional[str]
    settlement: Optional[str]
    settlement_port: Optional[str]
    port: Port
    comments: List[str]
    api_token: Optional[str]
    logs: List[str]
    revised_transaction_id: Optional[str]
    refund: Optional[str]
    refund_detail_ids: List[str]
    is_shaparak_port: bool
    payer: Person
    receiver: Person
    receipt_url: Optional[str]
    time_prediction: TimePrediction

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payment_date = JalaliDateTime.strptime(self.payment_date, "%H:%M:%S - %Y/%m/%d")
        self.created_at = JalaliDateTime.strptime(self.created_at, "%H:%M:%S - %Y/%m/%d")
        self.effective_at_jalali = JalaliDateTime.strptime(self.effective_at_jalali, "%H:%M:%S - %Y/%m/%d")
        self.updated_at = JalaliDateTime.strptime(self.updated_at, "%H:%M:%S - %Y/%m/%d")
        if 'time_prediction' in kwargs:
            self.time_prediction = self.TimePrediction(**kwargs['time_prediction'])
        if 'payer' in kwargs:
            self.payer = self.Person(**kwargs['payer'])
        if 'receiver' in kwargs:
            self.receiver = self.Person(**kwargs['receiver'])
        if 'port' in kwargs:
            self.port = Port(kwargs['port'])
        if 'status' in kwargs:
            self.status = self.Status(kwargs['status'])

        if 'factorNumber' in kwargs:
            self.factor_number = kwargs['factorNumber']

    def to_dict(self):
        d = {k: v for k, v in self.__dict__.items()}
        del d['factor_number']
        for k, v in d.items():
            if isinstance(v, Enum):
                d[k] = v.value
            elif isinstance(v, JalaliDateTime):
                d[k] = v.strftime('%H:%M:%S - %Y/%m/%d').replace('/0', '/')
            elif isinstance(v, BaseModel):
                d[k] = v.to_dict()
        return d

    def is_verified(self):
        return self.verified == 1
