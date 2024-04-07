from enum import Enum


class Status(Enum):
    PENDING = "PENDING"
    INITIATED = "INIT"
    DONE = "DONE"
    FAILED = "FAILED"
    CANCELED = "CANCELED"
