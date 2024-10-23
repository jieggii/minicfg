import typing

from .field import Field
from .provider import AbstractProvider, EnvProvider

_DEFAULT_PROVIDER = EnvProvider


class Minicfg:
    """
    Base class for configuration classes.
    """

    _prefix: str

    def __init__(self):
        if not hasattr(self, "_prefix"):
            self._prefix = ""

    @classmethod
    def populated(cls, provider: AbstractProvider | None = None):
        """
        Create an instance of the Minicfg class and populate it with the given provider.

        :param provider: provider used to populate the Minicfg instance.
        :return:
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
        Populate the Minicfg instance with the given provider.

        :param provider: provider used to populate the Minicfg instance.
        :return:
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

        :return:
        """
        for attr_name in dir(self):
            if attr_name.startswith("_"):
                continue

            attr = super().__getattribute__(attr_name)
            yield attr_name, attr

    # def __getattribute__(self, item: typing.Any) -> typing.Any:
    #     """
    #     Get attribute value.
    #     Aliases fields to their values.
    #
    #     :param item:
    #     :return:
    #     """
    #     cls = super().__getattribute__("__class__")
    #     attr = getattr(cls, item, None)
    #
    #     if isinstance(attr, Field):
    #         return attr.value
    #
    #     return super().__getattribute__(item) # default behavior for attributes that are not Fields


def minicfg_prefix(prefix: str):
    """
    Set a prefix for all fields in the Minicfg class.
    :param prefix: prefix.
    """

    def decorator(cls: Minicfg):
        cls._prefix = f"{prefix}_"
        return cls

    return decorator
