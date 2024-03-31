from enum import Enum


class BaseModel:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.__dict__}>"

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    @staticmethod
    def _recursive_to_dict(data):
        if isinstance(data, BaseModel):
            return data.to_dict()
        elif isinstance(data, Enum):
            return data.value
        elif isinstance(data, list):
            return [BaseModel._recursive_to_dict(i) for i in data]
        elif isinstance(data, dict):
            return {k: BaseModel._recursive_to_dict(v) for k, v in data.items()}
        return data

    def to_dict(self):
        data = {}
        for k, v in self.__dict__.items():
            data[k] = BaseModel._recursive_to_dict(v)
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
