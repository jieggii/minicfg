"""
This simple example demonstrates how to use minicfg to define a configuration class.
"""

from minicfg import Field, Minicfg
from minicfg.caster import IntCaster


class Env(Minicfg):
    """
    The main config.
    """

    # DATABASE HOST will be set to localhost if no value provided
    DATABASE_HOST: str = Field(default="localhost")

    # DATABASE_PORT value will be cast to int
    DATABASE_PORT: int = Field(caster=IntCaster())

# Populate the config using env vars (by default):
env = Env.populated()

print(f"{env.DATABASE_HOST=}")
print(f"{env.DATABASE_PORT=}")



"""
Try running `DATABASE_HOST=127.0.0.1 DATABASE_PORT=5432 python simple.py` and you should see the following output:
>>> env.DATABASE_HOST='127.0.0.1'
>>> env.DATABASE_PORT=5432
"""

"""
Try running `DATABASE_PORT=5432 python simple.py` and you should see the following output:
>>> env.DATABASE_HOST='localhost'  # default value is used
>>> env.DATABASE_PORT=5432
"""