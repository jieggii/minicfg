from minicfg.provider import AbstractProvider
from minicfg.field import FieldWrapper
from minicfg.naming_profile import AbstractNamingProfile


def _translate_config_name(config_name: str) -> str:
    return config_name.upper()

    # import re
    # return re.sub(r'(?<!^)(?=[A-Z])', '_', config_name).upper()


def populate(config: object, provider: AbstractProvider, naming_profile: AbstractNamingProfile , prefix: str = "", sep: str = "_", is_outer: bool = True) -> None:
    current_prefix = prefix
    if not is_outer:
        current_prefix += _translate_config_name(config.__name__)

    for attr_name in dir(config):
        if attr_name.startswith("_"):
            continue

        attr_val = getattr(config, attr_name)
        print(f"{current_prefix}{sep if current_prefix else ''}{attr_name} = {attr_val}")
        if isinstance(attr_val, type):
            # subconfig
            populate(attr_val, provider=provider, prefix=current_prefix, sep=sep, is_outer=False)

        elif isinstance(attr_val, FieldWrapper):
            # field
            _populate_field(attr_name, attr_val, provider, prefix=current_prefix, sep=sep)
        else:
            # skip unexpected attributes
            continue


def _populate_field(attr_name: str, field: FieldWrapper, provider: AbstractProvider, prefix: str, sep: str) -> None:
    pass
