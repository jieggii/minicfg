import typing

from .field import Field
from .provider import AbstractProvider, EnvProvider

_DEFAULT_PROVIDER = EnvProvider
_DEFAULT_NAME_SEP = "_"


class Minicfg:
    """
    Base class for configuration classes.
    """

    """
    Name of the minicfg. None value means that the minicfg has no name.
    """
    _name: str | None = None

    """
    Separator used to separate the minicfg name (if any) and the field name.
    """
    _name_sep: str = _DEFAULT_NAME_SEP

    def __init__(self):
        """
        Initialize the Minicfg instance.
        Generates names for all fields and initialize child minicfgs.
        """

        # add the minicfg name prefix to all field names:
        for attr_name, field in self._iter_field_instances():
            if field.name is None:
                # use the attribute name as the field name if field name is not set:
                field.name = attr_name

            if self._name:
                # prepend the minicfg name to the field name the minicfg has a name:
                field.name = f"{self._name}{self._name_sep}{field.name}"

            if field.file_field:
                # update the field's attached file field name:
                field.file_field.name = f"{field.name}_FILE"

        # initialize the child minicfgs:
        for attr_name in dir(self.__class__):
            attr_value = getattr(self.__class__, attr_name)
            if not (isinstance(attr_value, type) and issubclass(attr_value, Minicfg)):
                continue

            child_minicfg_class = attr_value
            if self._name:
                # prepend the minicfg name to the child minicfg name if the minicfg has a name:
                if child_minicfg_class._name:
                    child_minicfg_class._name = f"{self._name}{self._name_sep}{child_minicfg_class._name}"
                else:
                    child_minicfg_class._name = self._name

            setattr(self, attr_name, child_minicfg_class())

    @classmethod
    def new_populated(cls, provider: AbstractProvider | None = None) -> "Minicfg":
        """
        Create an instance of the Minicfg class and populate it with the given provider.
        :param provider: provider used to populate the Minicfg instance.
        :return: populated Minicfg instance.
        """

        minicfg = cls()
        minicfg.populate(provider)
        return minicfg

    @property
    def name(self):
        """
        Name of the minicfg.
        """
        return self._name

    def populate(self, provider: AbstractProvider | None = None) -> None:
        """
        Populate the Minicfg instance using the given provider.
        All fields and child Minicfg instances will be populated recursively.

        :param provider: provider used to populate the Minicfg instance. If not provided, the default _DEFAULT_PROVIDER will be used.
        """

        if not provider:
            provider = _DEFAULT_PROVIDER()

        # populate all fields:
        for attr_name, field in self._iter_field_instances():
            field.populate(provider)
            setattr(
                self, attr_name, field.value
            )  #  replace the field attribute with the populated value. Original Field instances will be accessible only in self.__class__

        # populate all child minicfgs:
        for child_minicfg in self._iter_minicfg_instances():
            child_minicfg.populate(provider)

    def _iter_field_instances(self) -> typing.Generator[typing.Tuple[str, Field], None, None]:
        """
        Iterate over all field instances.
        """

        # (using self.__class__ to access the original Field instances even if minicfg is populated)
        for attr_name in dir(self.__class__):
            attr_value = getattr(self.__class__, attr_name)
            if isinstance(attr_value, Field):
                yield attr_name, attr_value

    def _iter_minicfg_instances(self) -> typing.Generator["Minicfg", None, None]:
        """
        Iterate over all child minicfg instances.
        """

        for attr_name in dir(self):
            attr_value = getattr(self, attr_name)
            if isinstance(attr_value, Minicfg):
                yield attr_value

    def __iter__(self):
        """
        Iterate over all fields and child minicfg instances.
        """
        for _, field in self._iter_field_instances():
            yield field
        for minicfg in self._iter_minicfg_instances():
            yield minicfg


def minicfg_name(name: str):
    """
    Decorator used to set the name of the mincfg.
    :param name: name of the minicfg.
    """

    def decorator(cls: Minicfg):
        cls._name = name
        return cls

    return decorator


def minicfg_name_sep(sep: str):
    """
    Decorator used to set the separator of the mincfg.
    :param sep: separator of the minicfg.
    """

    def decorator(cls: Minicfg):
        cls._name_sep = sep
        return cls

    return decorator
