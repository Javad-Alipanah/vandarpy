import logging
from typing import TYPE_CHECKING, Optional

from apiclient.authentication_methods import HeaderAuthentication

from vandarpy.exceptions import VandarError
from vandarpy.models.auth import Token

if TYPE_CHECKING:  # pragma: no cover
    # Stupid way of getting around cyclic imports when
    # using type-hinting.
    from vandarpy.client import VandarClient

LOG = logging.getLogger(__name__)
DEFAULT_REFRESH_TOKEN_BACKOFF = 60 * 10  # 10 minutes


class RefreshTokenAuthentication(HeaderAuthentication):
    def __init__(self, token: str, refresh_token: str):
        super().__init__(token=token)
        self._refresh_token = refresh_token

    def refresh(self, client: "VandarClient"):
        token: Optional[Token] = None
        try:
            token: Token = client.token(self._refresh_token)
        except VandarError as e:
            LOG.error(f"Failed to refresh token: {e}")
        else:
            self._token = token.access_token
            self._refresh_token = token.refresh_token
        finally:
            return client.reschedule_token_refresh(
                DEFAULT_REFRESH_TOKEN_BACKOFF if token is None else token.expires_in // 10
            )
