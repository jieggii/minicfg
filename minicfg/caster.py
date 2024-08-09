import typing
from abc import ABC, abstractmethod


class AbstractCaster(ABC):
    @abstractmethod
    def cast(self, value: str) -> typing.Any:
        pass


class IntCaster(AbstractCaster):
    def cast(self, value: str) -> typing.Any:
        return int(value)

class FloatCaster(AbstractCaster):
    def cast(self, value: str) -> typing.Any:
        return float(value)


to_int = IntCaster()
to_float = FloatCaster()

# todo: write more basic casters
