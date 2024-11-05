import typing

from .field import Field
from .provider import AbstractProvider, EnvProvider

_DEFAULT_PROVIDER = EnvProvider


class Minicfg:
    """
    Base class for configuration classes.
    """

    _prefix: str  # prefix used for all fields in the Minicfg instance

    def __init__(self):
        if not hasattr(self, "_prefix"):
            # if prefix is not set, set it to an empty string:
            self._prefix = ""

    @classmethod
    def populated(cls, provider: AbstractProvider | None = None):
        """
        Create an instance of the Minicfg class and populate it with the given provider.

        :param provider: provider used to populate the Minicfg instance.
        :return: populated Minicfg instance.
        """

        minicfg = cls()
        minicfg.populate(provider)
        return minicfg

    @property
    def prefix(self) -> str:
        return self._prefix

    @prefix.setter
    def prefix(self, value: str):
        self._prefix = value

    def populate(self, provider: AbstractProvider | None = None) -> None:
        """
        Populate the Minicfg instance using the given provider.
        All fields and child Minicfg instances will be populated recursively.

        :param provider: provider used to populate the Minicfg instance. If not provided, the default _DEFAULT_PROVIDER will be used.
        """

        if not provider:
            provider = _DEFAULT_PROVIDER()

        for attr_name, attr in self._iter_public_attrs():
            if isinstance(attr, type) and issubclass(attr, Minicfg):  # if attribute is a child Minicfg type
                # create an instance of the child minicfg:
                child_minicfg = attr()

                # use class name as a child minicfg prefix if it is not set:
                if child_minicfg.prefix == "":
                    child_minicfg.prefix = f"{child_minicfg.__class__.__name__}_"

                # prepend prefix from the parent minicfg instance:
                child_minicfg.prefix = f"{self._prefix}{child_minicfg._prefix}"

                # populate the child minicfg:
                child_minicfg.populate(provider)

                # replace the child minicfg class with its instance:
                self.__setattr__(attr_name, child_minicfg)

            elif isinstance(attr, Field):  # if attribute is an instance of a Field
                field = attr

                # if field name is not set, set it to the attribute name:
                if not field.name:
                    field.name = attr_name

                # populate field:
                field.populate(provider, self._prefix)

                # replace the field with its populated value:
                self.__setattr__(attr_name, field.populated_value)

    def _iter_public_attrs(self) -> typing.Generator[tuple[str, typing.Any], None, None]:
        """
        Iterate over public attributes of the Minicfg instance.

        :return: generator of tuples (attribute name, attribute).
        """

        for attr_name in dir(self):
            if attr_name.startswith("_"):
                continue

            attr = super().__getattribute__(attr_name)
            yield attr_name, attr


def minicfg_prefix(prefix: str):
    """
    Decorator for setting a prefix for the Minicfg class.
    Will be used as a prefix for all fields in the Minicfg class.

    Please note, that an "_" will be appended to the prefix. Use raw_prefix instead if you don't want it.
    :param prefix: prefix.
    """

    def decorator(cls: Minicfg):
        cls._prefix = f"{prefix}_"
        return cls

    return decorator
