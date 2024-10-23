from minicfg.caster import IntCaster
from minicfg import Minicfg, Field
from minicfg.provider import AbstractProvider


class MockProvider(AbstractProvider):
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

# Try running python provider.py
# Output:
# config.DATABASE_HOST='localhost'
# config.DATABASE_PORT=1234
