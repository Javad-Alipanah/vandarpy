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
