"""
This example demonstrates how to attach a file field to another field.
"""

from minicfg import Field, Minicfg
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
    """
    My configuration class.
    """

    """
    A virtual DATABASE_HOST_FILE field will be also created and attached to the DATABASE_HOST field.
    
    - If only DATABASE_HOST_FILE is provided, the field value will be read from the file.
    - If only DATABASE_HOST is provided, the field value will be used directly from it.
    - If both DATABASE_HOST_FILE and DATABASE_HOST are provided, the value of DATABASE_HOST will be used.
    - If none of them are provided, the FieldValueNotProvidedError will be raised.
    """
    DATABASE_HOST = Field(attach_file_field=True)


"""
Try running `python file_field.py` and you should see the following output:
>>> config.DATABASE_HOST='<your hostname>'

If you don't have a hostname file, the FileNotFound exception will be raised.
"""
if __name__ == "__main__":
    provider = MyProvider()  # create a new instance of the custom provider

    config = MyConfig()  # create a new instance of the config
    config.populate(provider)  # populate the config using the custom provider

    print(f"{config.DATABASE_HOST=}")
    # >>> config.DATABASE_HOST='<your hostname>'
