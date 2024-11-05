"""
This example demonstrates how to use prefixes with minicfg.
"""

from minicfg import Field, Minicfg, minicfg_prefix
from minicfg.caster import IntCaster


@minicfg_prefix("SERVICE")  # <-- The prefix for the main config.
class Env(Minicfg):
    """
    The main config with the "SERVICE_" prefix.
    """

    # Sub minicfg without any prefix indicated.
    # prefix will be inherited from the parent minicfg and prepended to the class name.
    # The full prefix: "SERVICE_Meta_".
    class Meta(Minicfg):
        SOME_VAR: str = Field()
        SOME_OTHER_VAR: str = Field(default="this is default value")

    # Sub minicfg with "BOT" prefix indicated.
    # The full prefix: "SERVICE_BOT_".
    @minicfg_prefix("BOT")  # <-- The prefix for the sub config.
    class Bot(Minicfg):
        TOKEN: str = Field()

    # Sub minicfg with "MONGO" prefix indicated.
    # The full prefix: "SERVICE_MONGO_".
    @minicfg_prefix("MONGO")  # <-- The prefix for the sub config.
    class Mongo(Minicfg):
        HOST: str = Field()
        PORT: int = Field(caster=IntCaster())  # PORT will be cast to int


env = Env.populated()  # populate the config using env vars (by default)

print("Meta:")
print(f"{env.Meta.SOME_VAR=}")
print(f"{env.Meta.SOME_OTHER_VAR=}")
print()

print("Bot:")
print(f"{env.Bot.TOKEN=}")
print()

print("Mongo:")
print(f"{env.Mongo.HOST=}")
print(f"{env.Mongo.PORT=}")

"""
Try running `SERVICE_Meta_SOME_VAR=xyz SERVICE_BOT_TOKEN=token SERVICE_MONGO_HOST=localhost SERVICE_MONGO_PORT=12 python prefixes.py` and you should see the following output:

>>> Meta:
>>> env.Meta.SOME_VAR='xyz'
>>> env.Meta.SOME_OTHER_VAR='this is default value'

>>> Bot:
>>> env.Bot.TOKEN='token'

>>> Mongo:
>>> env.Mongo.HOST='localhost'
>>> env.Mongo.PORT=12
"""
