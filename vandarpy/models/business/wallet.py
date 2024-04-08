from vandarpy.models.base import BaseModel


class Wallet(BaseModel):
    balance: float
    balance_without_payment_facilitator: float
    payment_facilitator_balance: float
    currency: str

    def __init__(self, **kwargs):
        super().__init__()
        self.balance = kwargs.get('wallet', 0)
        self.balance_without_payment_facilitator = kwargs.get('wallet_without_payment_facilitator_wallet', 0)
        self.payment_facilitator_balance = kwargs.get('payment_facilitator_wallet', 0)
        self.currency = kwargs.get('currency', 'Toman')

    def to_dict(self):
        return {
            'wallet': self.balance,
            'wallet_without_payment_facilitator_wallet': self.balance_without_payment_facilitator,
            'payment_facilitator_wallet': self.payment_facilitator_balance,
            'currency': self.currency
        }

    def __str__(self):
        return f"<Wallet: {self.balance} ({self.currency})>"

    def __repr__(self):
        return f"<Wallet: {self.balance}>"