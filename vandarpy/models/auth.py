from enum import Enum

from vandarpy.models.base import BaseModel


class Token(BaseModel):
    class Type(Enum):
        BEARER = "Bearer"
        TOKEN = "Token"
        COOKIE = "Cookie"

    token_type: Type
    expires_in: int
    access_token: str
    refresh_token: str

    def __init__(self, token_type: Type, expires_in: int, access_token: str, refresh_token: str, **kwargs):
        super().__init__(token_type=token_type, expires_in=expires_in, access_token=access_token,
                         refresh_token=refresh_token, **kwargs)

    @classmethod
    def from_dict(cls, data: dict):
        return Token(
            token_type=Token.Type(data["token_type"]),
            expires_in=data["expires_in"],
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
        )

    def __str__(self):
        return f"{self.token_type} token with {self.expires_in} seconds expiration"

    def __repr__(self):
        return f"<{self.token_type} ({self.expires_in})>"
