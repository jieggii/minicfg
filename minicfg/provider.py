import os
from abc import ABC, abstractmethod


class AbstractProvider(ABC):
    """
    Abstract provider class.
    """

    @abstractmethod
    def get(self, key: str) -> str | None:
        """
        Get the value for the given key.
        :param key: key to get the value for.
        :return: value for the given key or None if the key is not found. Please note, that the return value is always a string.
        """
        pass


class EnvProvider(AbstractProvider):
    """
    A provider that reads values from environment variables.
    """

    def get(self, key: str) -> str | None:
        return os.getenv(key)
