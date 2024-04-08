from typing import List

from vandarpy.models.base import BaseModel


class Bank(BaseModel):
    class A2A(BaseModel):
        class Limit(BaseModel):
            class TimeLimit(BaseModel):
                start: str
                end: str

                def __init__(self, **kwargs):
                    super().__init__(**kwargs)
                    self.start = kwargs.get('start_time')
                    self.end = kwargs.get('end_time')

                def to_dict(self):
                    return {
                        'start_time': self.start,
                        'end_time': self.end
                    }

            class AmountLimit(BaseModel):
                total: int
                used: int
                remained: int

            time: List[TimeLimit]
            amount: AmountLimit

            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.time = [self.TimeLimit(**time) for time in kwargs.get('time_limit')]
                self.amount = self.AmountLimit(**kwargs.get('amount_limit'))

            def to_dict(self):
                return {
                    'time_limit': [time.to_dict() for time in self.time],
                    'amount_limit': self.amount.to_dict()
                }
        limit: Limit
        is_active: bool
        has_ability: bool
        is_healthy: bool

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.limit = self.Limit(**kwargs.get('limit'))

    name: str
    code: str
    a2a: A2A

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.a2a = self.A2A(**kwargs.get('a2a'))

    def __str__(self):
        return f"<Bank: {self.name} ({self.code})>"

    def __repr__(self):
        return f"<Bank: {self.name}>"
