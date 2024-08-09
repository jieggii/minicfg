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

class ListCaster(AbstractCaster):
    def __init__(self, sep: str = ",", item_caster: AbstractCaster | None = None):
        self.sep = sep
        self.item_caster = item_caster

    def cast(self, value: str) -> list[typing.Any]:
        str_items = value.split(self.sep)

        if self.item_caster:
            casted_items: list[typing.Any] = []
            for item in str_items:
                try:
                    casted = self.item_caster.cast(item)
                    casted_items.append(casted)
                except Exception as e:
                    raise ValueError(f'failed to cast list item "{item}" using {self.item_caster.__class__.__name__}') from e
            return casted_items

        return str_items


to_int = IntCaster()
to_float = FloatCaster()
to_bool = BoolCaster()
to_list = ListCaster()

# todo: write more basic casters
