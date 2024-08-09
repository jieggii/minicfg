import typing
from abc import ABC, abstractmethod


class AbstractCaster(ABC):
    @abstractmethod
    def cast(self, value: str) -> typing.Any:
        pass


class IntCaster(AbstractCaster):
    def cast(self, value: str) -> int:
        return int(value)

class FloatCaster(AbstractCaster):
    def cast(self, value: str) -> float:
        return float(value)

class BoolCaster(AbstractCaster):
    def __init__(self):
        self.true = {"true", "yes", "on", "enable", "1"}
        self.false = {"false", "no", "off", "disable", "0"}

    def cast(self, value: str) -> bool:
        if value in self.true:
            return True
        elif value in self.false:
            return False

        raise ValueError("value provided cannot be casted to bool")


to_int = IntCaster()
to_float = FloatCaster()
to_bool = BoolCaster()

# todo: write more basic casters
