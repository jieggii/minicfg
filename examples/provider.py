"""
This example demonstrates how to use a custom provider to populate the configuration.
"""

from minicfg import Field, Minicfg
from minicfg.caster import IntCaster
from minicfg.provider import AbstractProvider


class MockProvider(AbstractProvider):
    """
    A custom mock provider that provides the DATABASE_HOST value.
    """
    def __init__(self):
        self.data = {
            "DATABASE_HOST": "localhost",
        }

    def get(self, key: str) -> str | None:
        return self.data.get(key)


class MockConfig(Minicfg):
    DATABASE_HOST: str = Field()
    DATABASE_PORT: int = Field(default=1234, caster=IntCaster())


mock_provider = MockProvider()
config = MockConfig.populated(mock_provider)

print(f"{config.DATABASE_HOST=}")
print(f"{config.DATABASE_PORT=}")



"""
Try running `python provider.py` and you should see the following output:

>>> config.DATABASE_HOST='localhost'
>>> config.DATABASE_PORT=1234
"""