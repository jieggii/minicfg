from enum import Enum
from abc import ABC, abstractmethod

class AbstractNamingProfile(ABC):
    @property
    @abstractmethod
    def sep(self) -> str:
        pass

    @abstractmethod
    def translate_config_name(self, config_name: str) -> str:
        pass

    @abstractmethod
    def translate_field_name(self, field_name: str) -> str:
        pass


class ScreamingSnakeCaseNamingProfile(AbstractNamingProfile):
    def translate_config_name(self, config_name: str) -> str:
        return config_name.upper()

    def translate_field_name(self, field_name: str) -> str:
        return field_name.upper()


class AsIsNamingProfile(AbstractNamingProfile):
    def translate_field_name(self, field_name: str) -> str:
        pass

    def translate_config_name(self, config_name: str) -> str:
        pass


class NamingProfile(Enum):
    AS_IS = "AS_IS"
    SCREAMING_SNAKE_CASE = "SCREAMING_SNAKE_CASE"
