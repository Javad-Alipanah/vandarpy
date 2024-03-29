from threading import Timer
from typing import Type, cast

from apiclient import APIClient, JsonResponseHandler, JsonRequestFormatter
from apiclient.exceptions import APIClientError

from vandarpy.auth import RefreshTokenAuthentication
from vandarpy.endpoints.base import EndpointBase
from vandarpy.exceptions import VandarError
from vandarpy.models.auth import Token
from vandarpy.models.base import BaseModel


class VandarClient(APIClient):
    _authentication_method: RefreshTokenAuthentication

    def __init__(self, token: str, refresh_token: str):
        super().__init__(
            authentication_method=RefreshTokenAuthentication(token=token, refresh_token=refresh_token),
            response_handler=JsonResponseHandler,
            request_formatter=JsonRequestFormatter,
        )
        self._scheduler = Timer(0.000001, self._authentication_method.refresh, (self,))
        self._scheduler.start()

    def _get_instance(self, url: str, model: Type[BaseModel]) -> BaseModel:
        try:
            return model.from_dict(self.get(url))
        except APIClientError as e:
            raise VandarError(e)

    def _get_instances(self, url: str, model: Type[BaseModel]) -> list[BaseModel]:
        try:
            return [model.from_dict(data) for data in self.get(url)]
        except APIClientError as e:
            raise VandarError(e)

    def _create_instance(self, url: str, data: BaseModel) -> None:
        try:
            self.post(url, data.to_dict())
        except APIClientError as e:
            raise VandarError(e)

    def _put_instance(self, url: str, data: BaseModel) -> None:
        try:
            self.put(url, data.to_dict())
        except APIClientError as e:
            raise VandarError(e)

    def token(self, refresh_token: str) -> Token:
        try:
            return cast(
                Token,
                Token.from_dict(self.post(EndpointBase.refresh_token, {"refreshtoken": refresh_token}))
            )
        except APIClientError as e:
            raise VandarError(e)

    def reschedule_token_refresh(self, seconds: int):
        if self._scheduler.is_alive():
            self._scheduler.cancel()
        self._scheduler = Timer(seconds, self._authentication_method.refresh, (self,))
        self._scheduler.start()
