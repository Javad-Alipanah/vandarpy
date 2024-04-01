from enum import Enum
from typing import Optional, List

from vandarpy.models.base import BaseModel


class User(BaseModel):
    class Status(Enum):
        INACTIVE = 0
        ACTIVE = 1

    class Role(Enum):
        OWNER = 0
        ADMIN = 1
        ACCOUNTANT = 2
        DEVELOPER = 3
        REPORTER = 4

    id: Optional[int]
    user_id: Optional[int]
    name: str
    avatar: str
    role: str
    role_id: Role
    status: Status
    is_two_factor: Optional[bool]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role_id = self.Role(self.role_id)
        self.status = self.Status(self.status)

    def is_active(self):
        return self.status == self.Status.ACTIVE

    def is_owner(self):
        return self.role_id == self.Role.OWNER

    def is_admin(self):
        return self.role_id == self.Role.ADMIN

    def is_accountant(self):
        return self.role_id == self.Role.ACCOUNTANT

    def is_developer(self):
        return self.role_id == self.Role.DEVELOPER

    def is_reporter(self):
        return self.role_id == self.Role.REPORTER
