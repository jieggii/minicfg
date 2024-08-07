from .caster import AbstractCaster
from .provider import AbstractProvider


class CastingError(Exception):
    field_name: str
    caster: AbstractCaster
    exception: Exception

    def __init__(self, field_name: str, raw_value: str, caster: AbstractCaster, exception: Exception):
        self.field_name = field_name
        self.raw_value = raw_value
        self.caster = caster
        self.exception = exception

        super().__init__(
            f'exception occurred when casting {field_name} value "{raw_value}" '
            f"using {caster.__class__.__name__}: {exception}"
        )


class FieldValueNotProvidedError(Exception):
    def __init__(self, field_name: str, provider: AbstractProvider):
        self.field_name = field_name
        self.provider = provider

        super().__init__(f"{field_name} was not provided by {provider.__class__.__name__}, but was expected")


class FieldConflictError(Exception):
    field_name: str
    file_field_name: str

    def __init__(self, field_name: str, file_field_name: str, provider: AbstractProvider):
        self.field_name = field_name
        self.file_field_name = file_field_name

        super().__init__(
            f"values for both {field_name} and {file_field_name} "
            f"fields were provided by {provider.__class__.__name__}, "
            "expected only value for one of them"
        )
