from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    # Stupid way of getting around cyclic imports when
    # using type-hinting.
    from vandarpy.client import VandarClient


class BaseHandler:
    def __init__(self, client: "VandarClient"):
        self._client = client
