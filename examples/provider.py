from minicfg.minicfg import Minicfg, minicfg_provider
from minicfg.provider import AbstractProvider
from minicfg.field import Field
from minicfg.caster import to_int


class MockProvider(AbstractProvider):
    def __init__(self):
        self.data = {
            "DATABASE_HOST": "localhost",
        }

    def get(self, key: str) -> str | None:
        return self.data.get(key)


@minicfg_provider(MockProvider())
class MockConfig(Minicfg):
    DATABASE_HOST: str = Field()
    DATABASE_PORT: int = Field(default=1234, caster=to_int)


config = MockConfig()
config.populate()

print(f"{config.DATABASE_HOST=}")
print(f"{config.DATABASE_PORT=}")

# Try running python provider.py
# Output:
# config.DATABASE_HOST='localhost'
# config.DATABASE_PORT=1234
