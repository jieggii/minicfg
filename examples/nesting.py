"""
This example demonstrates how to use prefixes with minicfg.
"""

from minicfg import Field, Minicfg, minicfg_name
from minicfg.caster import IntCaster
from minicfg.provider import AbstractProvider


class MockProvider(AbstractProvider):
    """
    A custom mock provider.
    Used to simulate the environment variables.
    """

    data = {
        "SERVICE_DATABASE_HOST": "example.com",
        "SERVICE_EXTERNAL_API_KEY": "api_key",
        "SERVICE_EXTERNAL_API_USER_ID": "user123",
    }

    def get(self, key: str) -> str | None:
        return self.data.get(key)


@minicfg_name("SERVICE")  # <-- The prefix for the main config (will be inherited by nested configs).
class MyConfig(Minicfg):
    """
    My configuration class.
    """

    @minicfg_name("DATABASE")  # <-- The prefix for the nested config.
    class Database(Minicfg):
        HOST: str = Field()
        PORT: int = Field(default=5432, caster=IntCaster())

    @minicfg_name("EXTERNAL_API")  # <-- The prefix for the nested config.
    class ExternalAPI(Minicfg):
        KEY: str = Field(description="external API key")
        USER_ID: str = Field(description="external API user ID")


"""
Try running `python nesting.py` and you should see the following output:
>>> config.Database.HOST='example.com'
>>> config.Database.PORT=5432
>>> config.ExternalAPI.KEY='api_key'
>>> config.ExternalAPI.USER_ID='user123'
"""
if __name__ == "__main__":
    provider = MockProvider()  # create a new instance of the custom provider

    config = MyConfig()  # create a new instance of the config
    config.populate(provider)  # populate the config using the custom provider

    print(f"{config.Database.HOST=}")
    print(f"{config.Database.PORT=}")
    print(f"{config.ExternalAPI.KEY=}")
    print(f"{config.ExternalAPI.USER_ID=}")
