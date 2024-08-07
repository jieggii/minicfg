import typing
from abc import ABC, abstractmethod


class AbstractCaster(ABC):
    @abstractmethod
    def cast(self, value: str) -> typing.Any:
        pass


class IntCaster(AbstractCaster):
    def cast(self, value: str) -> typing.Any:
        return int(value)

# todo: write more basic casters
