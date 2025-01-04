from typing import Any

from .caster import AbstractCaster
from .provider import AbstractProvider


class CastingError(Exception):
    """
    Exception raised when an error occurs during casting.
    """

    def __init__(
        self,
        field_name: str,
        raw_value: str,
        caster: AbstractCaster,
    ):
        super().__init__(
            f'failed to cast raw value "{raw_value}" of the field {field_name} using {caster.__class__.__name__}',
        )


class FieldValueNotProvidedError(Exception):
    """
    Exception raised when a field value is not provided by the provider.
    """

    def __init__(self, field_name: str, provider: AbstractProvider):
        super().__init__(
            f"{field_name} was not provided by {provider.__class__.__name__}, but was expected",
        )


NO_DEFAULT_VALUE = object()


class Field:
    """
    Field class represents a configuration field.
    """

    _name: str  # name of the field

    _default: Any  # default value of the field
    _caster: AbstractCaster  # caster used to cast raw values
    _description: str  # description of the field in documentation purposes
    _file_field: "Field | None"  # file field attached to the field

    _value: Any  # value determined after field population

    def __init__(
        self,
        name: str | None = None,
        default: Any = NO_DEFAULT_VALUE,
        caster: AbstractCaster | None = None,
        description: str | None = None,
        attach_file_field: bool = False,
    ):
        """
        Initialize the field.
        :param name: name of the field. If not set, the name will be determined by the attribute name.
        :param default: default value of the field.
        :param caster: caster used to cast raw value to field value.
        :param description: description of the field in documentation purposes.
        :param attach_file_field: indicates whether file field should be attached to the field
        """

        self._name = name
        self._default = default
        self._caster = caster
        self._description = description
        self._file_field = Field(name=f"{self._name}_FILE" if self._name else None, description=f"{self._description} file" if self._description else None) if attach_file_field else None

        self._value = None

    @property
    def name(self) -> str | None:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def default(self) -> Any:
        """
        Return the default value of the field.
        """

        return self._default

    @property
    def caster(self) -> AbstractCaster:
        """
        Return the caster used to cast raw values to field
        """

        return self._caster

    @property
    def description(self) -> str:
        """
        Return the field description.
        """

        return self._description

    @property
    def value(self) -> Any:
        """
        Return the value of the field.
        """

        return self._value

    @property
    def file_field(self) -> "Field | None":
        """
        Return the attached file field.
        """

        return self._file_field

    def populate(self, provider: AbstractProvider) -> None:
        """
        Populate the field using the given provider.
        :param provider: provider to use to get the raw value of the field.
        """

        raw_value: str | None = provider.get(self._name)
        if raw_value is None:
            if self._file_field:
                # populate field using attached file field
                try:
                    self._file_field.populate(provider)
                except FieldValueNotProvidedError as e:
                    if self._default is not NO_DEFAULT_VALUE:
                        # use the default value if it is provided
                        self._value = self._default
                        return
                    raise FieldValueNotProvidedError(field_name=self._name, provider=provider) from e
                raw_value = _read_raw_value_from_file(self._file_field.value)
            elif self._default is not NO_DEFAULT_VALUE:
                # use the default value if it is provided
                self._value = self._default
                return
            else:
                # raise an error if the value is not provided and no default value is set
                raise FieldValueNotProvidedError(field_name=self._name, provider=provider)

        populated_value: Any = raw_value
        if self.caster:
            try:
                populated_value = self.caster.cast(raw_value)
            except Exception as e:
                raise CastingError(
                    field_name=self._name,
                    raw_value=raw_value,
                    caster=self._caster,
                ) from e

        self._value = populated_value


def _read_raw_value_from_file(path: str) -> str:
    """
    Read the raw value from the file at the given path.
    :param path: path to the file.
    :return: the raw value read from the file (with leading and trailing whitespaces removed).
    """

    with open(path, "r") as file:
        return file.read().strip()
