from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from .caster import AbstractCaster
from .exceptions import CastingError
from .provider import AbstractProvider


@dataclass
class FieldPopulationResult:
    populated: bool
    default_value_used: bool = False


class AbstractField(ABC):
    @property
    @abstractmethod
    def name(self) -> str | None:
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str) -> None:
        pass

    @property
    @abstractmethod
    def value(self) -> Any:
        pass

    @value.setter
    @abstractmethod
    def value(self, value: Any) -> None:
        pass

    @property
    @abstractmethod
    def attach_file_field(self) -> bool:
        pass

    @abstractmethod
    def name_with_prefix(self, prefix: str | None) -> str:
        pass

    @abstractmethod
    def populate_using_raw_value(self, raw_value: str) -> FieldPopulationResult:
        pass

    @abstractmethod
    def populate_using_provider(self, provider: AbstractProvider, field_name: str) -> FieldPopulationResult:
        pass


_NOT_SET = object()


class Field(AbstractField):
    _name: str
    _name_prefix: str | None

    _default: Any
    _caster: AbstractCaster
    _attach_file_field: bool

    _value: Any

    def __init__(
        self,
        name: str | None = None,
        default: Any = _NOT_SET,
        caster: AbstractCaster | None = None,
        attach_file_field: bool = False,
    ):
        self._name = name

        self._default = default
        self._caster = caster
        self._attach_file_field = attach_file_field

        self._value = _NOT_SET

    @property
    def name(self) -> str | None:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        self._value = value

    @property
    def attach_file_field(self) -> bool:
        return self._attach_file_field

    def name_with_prefix(self, prefix: str | None) -> str:
        if not prefix:
            return self._name

        return f"{prefix}{self._name}"

    def populate_using_raw_value(self, raw_value: str) -> FieldPopulationResult:
        if self._caster:
            try:
                self._value = self._caster.cast(raw_value)
                return FieldPopulationResult(populated=True)
            except Exception as e:
                raise CastingError(field_name=self.name, raw_value=raw_value, caster=self._caster, exception=e)

        self._value = raw_value
        return FieldPopulationResult(populated=True)

    def populate_using_provider(self, provider: AbstractProvider, field_name: str) -> FieldPopulationResult:
        raw_value = provider.get(field_name)
        if raw_value is None:
            if self._default is not _NOT_SET:
                self._value = self._default
                return FieldPopulationResult(populated=True, default_value_used=True)
            return FieldPopulationResult(populated=False)

        return self.populate_using_raw_value(raw_value)
