import typing
from abc import ABC, abstractmethod


class AbstractCaster(ABC):
    """
    Abstract caster class.
    """

    @abstractmethod
    def cast(self, value: str) -> typing.Any:
        """
        Cast the provided value to the desired type.
        :param value: value to be casted.
        :return: the casted value.
        """

        pass


class IntCaster(AbstractCaster):
    """
    Caster that casts the provided value to an integer.
    """

    def cast(self, value: str) -> int:
        return int(value)


class FloatCaster(AbstractCaster):
    """
    Caster that casts the provided value to a float.
    """

    def cast(self, value: str) -> float:
        return float(value)


class BoolCaster(AbstractCaster):
    """
    Caster that casts the provided value to a boolean.
    """

    true = {"true", "yes", "on", "enable", "1"}
    false = {"false", "no", "off", "disable", "0"}

    def __init__(self):
        pass

    def cast(self, value: str) -> bool:
        if value in self.true:
            return True
        elif value in self.false:
            return False

        raise ValueError("the provided value cannot be casted to bool")


class ListCaster(AbstractCaster):
    """
    Caster that casts the provided value to a list.
    """

    def __init__(self, sep: str = ",", item_caster: AbstractCaster | None = None):
        """
        Initialize the list caster.
        :param sep: separator used to split the provided value.
        :param item_caster: caster used to cast list items.
        """

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
                    raise ValueError(
                        f'failed to cast list item "{item}" using {self.item_caster.__class__.__name__}'
                    ) from e
            return casted_items

        return str_items
