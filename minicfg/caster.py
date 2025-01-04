import typing
from abc import ABC, abstractmethod
from collections.abc import Callable


class AbstractCaster(ABC):
    """
    Abstract caster class.
    """

    @abstractmethod
    def typename(self) -> str | None:
        """
        Get the type name of the caster.
        For example, "int", "float", "bool", etc. None if the type name is not available.
        """
        pass

    @abstractmethod
    def cast(self, value: str) -> typing.Any:
        """
        Cast the provided value to the desired type.
        :param value: value to be cast.
        :return: the cast value.
        """

        pass


class IntCaster(AbstractCaster):
    """
    Caster that casts the provided value to an integer.
    """

    @property
    def typename(self) -> str:
        return "int"

    def cast(self, value: str) -> int:
        return int(value)


class FloatCaster(AbstractCaster):
    """
    Caster that casts the provided value to a float.
    """

    @property
    def typename(self) -> str:
        return "float"

    def cast(self, value: str) -> float:
        return float(value)


class BoolCaster(AbstractCaster):
    """
    Caster that casts the provided value to a boolean.
    """

    true = {"true", "yes", "on", "enable", "enabled", "1"}
    false = {"false", "no", "off", "disable", "disabled", "0"}

    @property
    def typename(self) -> str:
        return "bool"

    def cast(self, value: str) -> bool:
        if value in self.true:
            return True
        elif value in self.false:
            return False

        raise ValueError("the provided value cannot be cast to bool")


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

    @property
    def typename(self) -> str:
        if self.item_caster:
            if self.item_caster.typename:
                return f"list[{self.item_caster.typename}]"
            else:
                return "list"
        return "list[str]"

    def cast(self, value: str) -> list[typing.Any]:
        str_items = value.split(self.sep)

        if self.item_caster:
            cast_items: list[typing.Any] = []
            for item in str_items:
                try:
                    cast_items.append(self.item_caster.cast(item))
                except Exception as e:
                    raise ValueError(
                        f'failed to cast list item "{item}" using item caster {self.item_caster.__class__.__name__}'
                    ) from e
            return cast_items

        return str_items


class JSONCaster(AbstractCaster):
    """
    Caster that casts the provided value to a JSON object.
    """

    _load: Callable[[str], dict[typing.Any, typing.Any]] | None

    def __init__(self, load: Callable[[str], dict[typing.Any, typing.Any]] | None = None):
        """
        Initialize JSONCaster.
        :param load: custom json load function. If set to None, standard json.load is used.
        """
        self._load = load

    @property
    def typename(self) -> str:
        return "json"

    def cast(self, value: str) -> dict[typing.Any, typing.Any] | list[typing.Any]:
        if self._load:
            return self._load(value)

        import json

        return json.loads(value)
