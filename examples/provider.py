"""
This example demonstrates how to use a custom provider to populate the configuration class.
"""

from minicfg import Field, Minicfg
from minicfg.caster import IntCaster
from minicfg.provider import AbstractProvider


class MockProvider(AbstractProvider):
    """
    A custom mock provider.
    """

    data = {"DATABASE_HOST": "example.com", "DATABASE_PORT": "5432"}

    def get(self, key: str) -> str | None:
        return self.data.get(key)


class MyConfig(Minicfg):
    """
    My configuration class.
    """

    DATABASE_HOST: str = Field()
    DATABASE_PORT: int = Field(caster=IntCaster())


"""
Try running `python provider.py` and you should see the following output:
>>> config.DATABASE_HOST='localhost'
>>> config.DATABASE_PORT=5432
"""
if __name__ == "__main__":
    mock_provider = MockProvider()  # create a new instance of the custom provider

    config = MyConfig()  # create a new instance of the config
    config.populate(mock_provider)  # populate the config using the custom provider

    print(f"{config.DATABASE_HOST=}")
    print(f"{config.DATABASE_PORT=}")
