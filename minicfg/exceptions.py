from .caster import AbstractCaster
from .provider import AbstractProvider


class CastingError(Exception):
    field_name: str
    raw_value: str
    caster: AbstractCaster
    exception: Exception

    def __init__(self, field_name: str, raw_value: str, caster: AbstractCaster, exception: Exception, file_field_name: str | None = None, file_field_value: str | None = None):
        self.field_name = field_name
        self.raw_value = raw_value
        self.caster = caster
        self.exception = exception

        caster_name = caster.__class__.__name__

        if file_field_name:
            msg = (
                f'exception occurred when casting {field_name} raw value "{raw_value}" '
                f"using {caster_name}: {exception} (the raw value was read from {file_field_value}, which was provided by the attached file field {file_field_name})"
            )
        else:
            msg = (
                f'exception occurred when casting {field_name} raw value "{raw_value}" '
                f"using {caster_name}: {exception}"
            )
        super().__init__(msg)


class FieldValueNotProvidedError(Exception):
    field_name: str
    provider: AbstractProvider
    file_field_name: str | None

    def __init__(self, field_name: str, provider: AbstractProvider, file_field_name: str | None = None):
        self.field_name = field_name
        self.provider = provider
        self.file_field_name = file_field_name

        provider_name = provider.__class__.__name__
        if file_field_name is not None:
            msg = f"neither {field_name} nor {file_field_name} were provided by {provider_name}, at least one was expected"
        else:
            msg = f"{field_name} was not provided by {provider_name}, but was expected"

        super().__init__(msg)


class FieldConflictError(Exception):
    field_name: str
    file_field_name: str

    def __init__(self, field_name: str, file_field_name: str, provider: AbstractProvider):
        self.field_name = field_name
        self.file_field_name = file_field_name

        provider_name = provider.__class__.__name__
        super().__init__(
            f"values for both {field_name} and {file_field_name} "
            f"fields were provided by {provider_name}, "
            "expected only value for one of them"
        )
