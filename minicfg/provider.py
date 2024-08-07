import os
from abc import ABC, abstractmethod


class AbstractProvider(ABC):
    @abstractmethod
    def get(self, key: str) -> str | None:
        pass


class EnvProvider(AbstractProvider):
    def get(self, key: str) -> str | None:
        return os.getenv(key)
