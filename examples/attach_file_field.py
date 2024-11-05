"""
This example demonstrates how to attach a file field to another field.
"""

from minicfg import Field, Minicfg, minicfg_prefix
from minicfg.provider import AbstractProvider


class MyProvider(AbstractProvider):
    """
    A provider that reads the hostname from the /etc/hostname file.
    """

    data = {
        "DATABASE_HOST_FILE": "/etc/hostname",
    }

    def get(self, key: str) -> str | None:
        return self.data.get(key)


class MyConfig(Minicfg):
    @minicfg_prefix("DATABASE")
    class Database(Minicfg):
        """
        A virtual DATABASE_HOST_FILE file field will be also created and attached to
        the DATABASE_HOST field below.
        If DATABASE_HOST_FILE is provided, the value of DATABASE_HOST will be read from the file.
        """

        HOST = Field(attach_file_field=True)


provider = MyProvider()
config = MyConfig.populated(provider)

print(f"{config.Database.HOST=}")
# >>> config.Database.HOST='<your hostname>'
