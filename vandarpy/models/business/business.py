from typing import Optional, Dict

from vandarpy.models.base import BaseModel


class Business(BaseModel):
    class StatusBox(BaseModel):
        payment_required: bool
        national_card_photo: str
        official_newspaper: str
        introduction_letter: str

    class ToolStatus(BaseModel):
        is_enabled: Optional[bool]
        is_created: Optional[bool]
        status: str
        time: str
        viewable: Optional[bool]
        name_fa: str
        name_en: str

    class Address(BaseModel):
        province: str
        province_id: int
        province_code: str
        city: str
        city_id: int
        local: Optional[str]
        local_id: Optional[int]
        address: str

        @classmethod
        def from_dict(cls, data: dict):
            province = data.get('province', data.get('provinces', None))
            province_id = data.get('province_id', data.get('provinces_id', None))
            province_code = data.get('province_code', data.get('provinces_code', None))
            return cls(province=province, province_id=province_id, province_code=province_code, **data)

        def to_dict(self):
            d = super().to_dict()
            d['provinces'] = self.province
            d['provinces_id'] = self.province_id
            d['provinces_code'] = self.province_code
            del d['province']
            del d['province_id']
            del d['province_code']
            return d

    class Detail(BaseModel):
        _status_key: str
        status: Optional[str]
        message: str

        @classmethod
        def from_dict(cls, data: dict):
            for k, v in data.items():
                if 'status' in k:
                    status = v
                    break
            else:
                status = None
            return cls(status=status, **data)

        def to_dict(self):
            d = super().to_dict()
            del d['status']
            return d

    class OwnerDetail(BaseModel):
        birthdate: str
        birth_certificate_number: str
        national_code: str

    id: int
    uuid: str
    active: int
    business_name: str
    business_name_fa: str
    legal_business_name: Optional[str]
    business_owner_is_business_legal_owner: Optional[bool]
    national_id: Optional[str]
    business_type: str
    phone_number: str
    tax_code: Optional[str]
    tax_code_detail: Detail
    enamad_detail: Detail
    postal_code: str
    postal_code_detail: Detail
    national_code_detail: Detail
    address_detail: Address
    city_id: Optional[str]
    mcc_code: str
    address: str
    wallet: int
    deductible_amount: int
    payment_facilitator_wallet: int
    blocked_amount: int
    avatar: str
    automatic_settlement_tip: bool
    settlement_schedule: str
    default_iban: str
    ayandeh_default_iban: str
    statusBox: StatusBox
    status: int
    today_transactions: int
    today_settlements: int
    role_name: str
    role: str
    permissions: list[str]
    has_shaparak_terminal: bool
    tools: Dict[str, ToolStatus]
    ipg_status: Dict[str, Dict[str, Optional[str]]]
    accept_business_time_prediction: str
    has_rejection: bool
    rejects: Dict[str, Optional[str]]
    cash_in_contracts: Optional[str]
    cash_in_code: Optional[str]
    owner: OwnerDetail
    high_value_fee: float
    need_shaparak_iban: bool
    pic_suspicious_check: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tax_code_detail = self.Detail.from_dict(kwargs.get('tax_code_detail', {}))
        self.enamad_detail = self.Detail.from_dict(kwargs.get('enamad_detail', {}))
        self.postal_code_detail = self.Detail.from_dict(kwargs.get('postal_code_detail', {}))
        self.national_code_detail = self.Detail.from_dict(kwargs.get('national_code_detail', {}))
        self.address_detail = self.Address.from_dict(kwargs.get('address_detail', {}))
        self.statusBox = self.StatusBox.from_dict(kwargs.get('statusBox', {}))
        self.tools = {k: self.ToolStatus.from_dict(v) for k, v in kwargs.get('tools', {}).items()}
        self.owner = self.OwnerDetail.from_dict(kwargs.get('owner', {}))

    def __repr__(self):
        return f"<Business {self.id}>"

    def __str__(self):
        return f"{self.id} ({self.business_name}, {self.business_name_fa})"
