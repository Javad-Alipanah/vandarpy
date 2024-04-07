from typing import TYPE_CHECKING, Optional, cast

from apiclient.authentication_methods import HeaderAuthentication

from vandarpy.endpoints.auth import AuthEndpoint
from vandarpy.exceptions import VandarError
from vandarpy.models.auth import Token

if TYPE_CHECKING:  # pragma: no cover
    # Stupid way of getting around cyclic imports when
    # using type-hinting.
    from vandarpy.client import VandarClient

DEFAULT_REFRESH_TOKEN_BACKOFF = 60 * 10  # 10 minutes


class RefreshTokenAuthentication(HeaderAuthentication):
    def __init__(self, token: str, refresh_token: str):
        super().__init__(token=token)
        self._refresh_token = refresh_token

    def refresh(self, client: "VandarClient"):
        token: Optional[Token] = None
        try:
            token = cast(
                Token,
                client.create_instance(AuthEndpoint.refresh_token, {"refreshtoken": self._refresh_token}, Token)
            )
        except VandarError:
            pass
        else:
            self._token = token.access_token
            self._refresh_token = token.refresh_token
        finally:
            return client.reschedule_token_refresh(
                DEFAULT_REFRESH_TOKEN_BACKOFF if token is None else token.expires_in // 10
            )

    @property
    def token(self) -> str:
        return self._token

    @property
    def refresh_token(self) -> str:
        return self._refresh_token
