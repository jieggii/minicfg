from minicfg import minicfg_prefix, Field, Minicfg
from minicfg.provider import AbstractProvider
from minicfg.caster import IntCaster


class MyProvider(AbstractProvider):
    data = {
        "DATABASE_HOST_FILE": "/etc/hostname",
    }

    def get(self, key: str) -> str | None:
        return self.data.get(key)




class MyConfig(Minicfg):
    @minicfg_prefix("DATABASE")
    class Database(Minicfg):
        """
        A virtual HOST_FILE file field will be also created and attached to
        the HOST field below.
        If HOST_FILE is provided, the value of HOST will be read from the file.
        """
        HOST = Field(attach_file_field=True)

provider = MyProvider()
config = MyConfig.populated(provider)

print(f"{config.Database.HOST=}")
# >>> config.Database.HOST='<your hostname>'