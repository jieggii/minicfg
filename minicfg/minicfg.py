import typing

from .exceptions import FieldConflictError, FieldValueNotProvidedError
from .field import AbstractField, Field, FieldPopulationResult
from .provider import AbstractProvider, EnvProvider


def _read_raw_value_from_file(path: str) -> str:
    with open(path, "r") as file:
        return file.read().strip()


class Minicfg:
    _prefix_attr_name = "_prefix"
    _default_provider_attr_name = "_default_provider"

    _prefix: str | None
    _default_provider: AbstractProvider | None

    _is_populated: bool

    def __init__(self, prefix: str | None = None, provider: AbstractProvider | None = None):
        # setup field names prefix:
        if prefix:
            self._prefix = prefix
        elif not hasattr(self, self._prefix_attr_name):
            # if prefix was not set by class decorator earlier:
            self._prefix = None

        # setup default provider:
        if provider:
            self._default_provider = provider
        elif not hasattr(self, self._default_provider_attr_name):
            # if default provider was not set by class decorator earlier:
            self._default_provider = None

        self._is_populated = False

    def __getattribute__(self, item: typing.Any):
        cls = super().__getattribute__("__class__")
        attr = getattr(cls, item, None)

        if isinstance(attr, AbstractField):
            return attr.value

        # default behavior for attributes that are not Fields
        return super().__getattribute__(item)

    @property
    def is_populated(self) -> bool:
        return self._is_populated

    def dict(self) -> dict[str, typing.Any]:
        if not self._is_populated:
            raise RuntimeError("config is not populated yet")

        result = {}
        for attr_name, attr in self._iter_public_attrs():
            if isinstance(attr, AbstractField):
                result[attr_name] = attr.value

            elif isinstance(attr, Minicfg):
                result[attr_name] = attr.dict()

        return result

    def populate(self) -> None:
        provider = self._default_provider or EnvProvider()

        for attr_name, attr in self._iter_public_attrs():
            if isinstance(attr, type) and issubclass(attr, Minicfg):  # if attr is a child Minicfg type
                child_minicfg = attr()

                # inherit prefix if needed:
                if self._prefix:
                    if child_minicfg._prefix:
                        child_minicfg._prefix = f"{self._prefix}{child_minicfg._prefix}"
                    else:
                        child_minicfg._prefix = self._prefix

                # inherit default provider if needed:
                if not child_minicfg._default_provider:
                    child_minicfg._default_provider = provider

                self.__setattr__(attr_name, child_minicfg)
                child_minicfg.populate()

            elif isinstance(attr, Field):  # if attr is field
                field = attr
                if not field.name:
                    field.name = attr_name

                file_field: Field | None = None
                file_field_result: FieldPopulationResult | None = None
                if field.attach_file_field:
                    file_field = Field(f"{field.name}_FILE")
                    file_field_result = file_field.populate_using_provider(
                        provider, file_field.name_with_prefix(self._prefix)
                    )

                field_result = field.populate_using_provider(provider, field.name_with_prefix(self._prefix))

                if field_result.populated and not field_result.default_value_used:
                    if file_field_result and file_field_result.populated:
                        raise FieldConflictError(
                            field_name=field.name_with_prefix(self._prefix),
                            file_field_name=file_field.name_with_prefix(self._prefix),
                            provider=provider,
                        )

                if file_field:  # if file field is attached to the original field
                    if file_field_result.populated:
                        file_field_raw_value = _read_raw_value_from_file(file_field.value)
                        field.populate_using_raw_value(file_field_raw_value)
                    else:
                        if not field_result.populated:
                            raise FieldValueNotProvidedError(field.name_with_prefix(self._prefix), provider)
                else:
                    if not field_result.populated:
                        raise FieldValueNotProvidedError(field.name_with_prefix(self._prefix), provider)

        self._is_populated = True

    def _iter_public_attrs(self):
        for attr_name in dir(self):
            if attr_name.startswith("_"):
                continue

            attr = super().__getattribute__(attr_name)
            yield attr_name, attr


def minicfg_provider(provider: AbstractProvider):
    def decorator(cls: Minicfg):
        cls._default_provider = provider
        return cls

    return decorator


def minicfg_prefix(prefix: str):
    def decorator(cls: Minicfg):
        cls._prefix = f"{prefix}_"
        return cls

    return decorator
