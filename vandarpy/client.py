import logging
from threading import Timer
from typing import Type, Optional

from apiclient import APIClient, JsonResponseHandler, JsonRequestFormatter
from apiclient.exceptions import APIClientError

from vandarpy.auth import RefreshTokenAuthentication
from vandarpy.exceptions import VandarError
from vandarpy.handlers.business import BusinessHandler
from vandarpy.models.base import BaseModel

LOG = logging.getLogger(__name__)


class VandarClient(APIClient):
    _authentication_method: RefreshTokenAuthentication
    _business: Optional[BusinessHandler]
    _scheduler: Timer

    def __init__(self, token: str, refresh_token: str, business_name: Optional[str] = None):
        super().__init__(
            authentication_method=RefreshTokenAuthentication(token=token, refresh_token=refresh_token),
            response_handler=JsonResponseHandler,
            request_formatter=JsonRequestFormatter,
        )
        self._scheduler = Timer(0.000001, self._authentication_method.refresh, (self,))
        self._scheduler.start()
        self._business = BusinessHandler(self, business_name) if business_name is not None else None

    def get_instance(self, url: str, model: Type[BaseModel], params: Optional[dict] = None) -> BaseModel:
        try:
            return model.from_dict(self.get(url, params=params))
        except APIClientError as e:
            LOG.error(f"Failed to get instance: {e}")
            raise VandarError(e)

    def get_instances(self, url: str, model: Type[BaseModel], params: Optional[dict] = None) -> list[BaseModel]:
        try:
            return [model.from_dict(data) for data in self.get(url, params=params)]
        except APIClientError as e:
            LOG.error(f"Failed to get instances: {e}")
            raise VandarError(e)

    def create_instance(self, url: str, data: dict,
                        model: Optional[Type[BaseModel]] = None,
                        params: Optional[dict] = None) -> Optional[BaseModel]:
        try:
            result = self.post(url, data, params=params)
            return model.from_dict(result) if model else None
        except APIClientError as e:
            LOG.error(f"Failed to create instance: {e}")
            raise VandarError(e)

    def put_instance(self, url: str, data: dict,
                     model: Optional[Type[BaseModel]] = None,
                     params: Optional[dict] = None) -> Optional[BaseModel]:
        try:
            result = self.put(url, data, params=params)
            return model.from_dict(result) if model else None
        except APIClientError as e:
            LOG.error(f"Failed to update instance: {e}")
            raise VandarError(e)

    @property
    def token(self) -> str:
        return self._authentication_method.token

    @property
    def business(self) -> BusinessHandler:
        if self._business is None:
            raise VandarError("Business name is not set.")
        return self._business

    @business.setter
    def business(self, name: str):
        self._business = BusinessHandler(self, name)

    def reschedule_token_refresh(self, seconds: int):
        if self._scheduler.is_alive():
            self._scheduler.cancel()
        self._scheduler = Timer(seconds, self._authentication_method.refresh, (self,))
        self._scheduler.start()
