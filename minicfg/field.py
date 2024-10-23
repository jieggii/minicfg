from typing import Any

from .caster import AbstractCaster
from .exceptions import CastingError, FieldValueNotProvidedError, FieldConflictError
from .provider import AbstractProvider


_NOT_SET = object()



def _read_raw_value_from_file(path: str) -> str:
    with open(path, "r") as file:
        return file.read().strip()


class Field:
    """
    Field class represents a configuration field.
    """

    _name: str  # name of the field

    _default: Any  # default value of the field
    _caster: AbstractCaster  # caster used to cast raw values
    _attach_file_field: bool  # indicates whether file field should be attached to the field

    _populated_value: Any  # value determined after field population

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

        self._populated_value = _NOT_SET

    @property
    def name(self) -> str | None:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def populated_value(self) -> Any:
        return self._populated_value

    def populate(self, provider: AbstractProvider, field_name_prefix: str | None = None):
        """
        Populate the field using the given provider.
        :param provider: provider used to get the field raw value.
        :param field_name_prefix: prefix to prepend to the field name.
        :return:
        """
        field_name = f"{field_name_prefix}{self._name}"  # name of the field
        file_field_name = f"{field_name_prefix}{self._name}_FILE"  # name of the corresponding file field

        raw_value_from_provider: str | None = provider.get(field_name)
        if raw_value_from_provider is not None:
            if provider.get(file_field_name) is not None:
                raise FieldConflictError(field_name, file_field_name, provider)

            try:
                self._populated_value = self._cast_raw_value_if_needed(raw_value_from_provider)
                return
            except Exception as e:
                raise CastingError(field_name=field_name, raw_value=raw_value_from_provider, caster=self._caster,
                                   exception=e) from e

        if self._attach_file_field:
            filepath = provider.get(file_field_name)
            if filepath is not None:
                raw_value_from_file = _read_raw_value_from_file(filepath)
                try:
                    self._populated_value = self._cast_raw_value_if_needed(raw_value_from_file)
                    return
                except Exception as e:
                    raise CastingError(field_name=field_name, raw_value=raw_value_from_file, caster=self._caster, exception=e, file_field_name=file_field_name, file_field_value=filepath) from e

            if self._default is not _NOT_SET:
                self._populated_value = self._default
                return

            raise FieldValueNotProvidedError(field_name, provider, file_field_name)

        if self._default is not _NOT_SET:
            self._populated_value = self._default
            return

        raise FieldValueNotProvidedError(field_name, provider)

    def _cast_raw_value_if_needed(self, raw_value: str) -> Any:
        """
        Cast the raw value using the caster if it is set.
        If no caster is set, return the raw value as is.
        :param raw_value: the raw value to be cast.
        :return:
        """
        if self._caster:
            return self._caster.cast(raw_value)
        return raw_value
