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

    def to_dict(self):
        data = {}
        for k, v in self.__dict__.items():
            if isinstance(v, BaseModel):
                data[k] = v.to_dict()
            elif isinstance(v, Enum):
                data[k] = v.value
            elif isinstance(v, list):
                data[k] = [i.to_dict() if isinstance(i, BaseModel) else i for i in v]
            else:
                data[k] = v
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
