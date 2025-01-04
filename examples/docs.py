"""
This example demonstrates how to document the configuration class.
"""

from minicfg import Field, Minicfg, minicfg_name
from minicfg.caster import IntCaster
from minicfg.docs_generator import DocsGenerator
from minicfg.provider import AbstractProvider


class MockProvider(AbstractProvider):
    """
    A custom mock provider.
    Used to simulate the environment variables.
    """

    data = {"DATABASE_HOST": "example.com", "DATABASE_PORT": "5432", "EXTERNAL_API_KEY": "api_key"}

    def get(self, key: str) -> str | None:
        return self.data.get(key)


class MyConfig(Minicfg):
    @minicfg_name("DATABASE")
    class Database(Minicfg):
        HOST = Field(default="localhost", description="database host")
        PORT = Field(caster=IntCaster(), description="database port")

    @minicfg_name("EXTERNAL_API")
    class ExternalAPI(Minicfg):
        KEY = Field(description="external API key")


"""
Try running `python docs.py` or `python -m minicfg docs.MyConfig --format=plaintext` and you should see the following output:
MyConfig

DATABASE
 - DATABASE_HOST: str = localhost  # database host
 - DATABASE_PORT: int  # database port


EXTERNAL_API
 - EXTERNAL_API_KEY: str  # external API key
"""
if __name__ == "__main__":
    config = MyConfig()  # create a new instance of the config
    docs_generator = DocsGenerator(config)  # create a new instance of the docs generator
    print(docs_generator.as_plaintext())  # print the documentation as plain text
