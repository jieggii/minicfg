from minicfg.provider import AbstractProvider


class MockProvider(AbstractProvider):
    """
    A mock provider used for testing purposes.
    """

    def __init__(self, data: dict[str, str]):
        self._data = data

    def get(self, key: str) -> str | None:
        return self._data.get(key)
