from minicfg.minicfg import Minicfg, minicfg_prefix
from minicfg.field import Field
from minicfg.caster import to_int

# config with "SERVICE_" prefix:
@minicfg_prefix("SERVICE")
class Env(Minicfg):
    # subconfig without any prefix.
    # prefix will be inherited from parent ("SERVICE_"):
    class Meta(Minicfg):
        SOME_VAR: str = Field()
        SOME_OTHER_VAR: str = Field(default="this is default value")

    # subconfig with "BOT_" prefix (full prefix: "SERVICE_BOT_"):
    @minicfg_prefix("BOT")
    class Bot(Minicfg):
        TOKEN: str = Field()

    # subconfig with "MONGO_" prefix (full prefix: "SERVICE_MONGO_"):
    @minicfg_prefix("MONGO")
    class Mongo(Minicfg):
        HOST: str = Field()
        PORT: int = Field(caster=to_int)  # PORT will be cast to int


env = Env()
env.populate()  # populate the config using env vars (by default)

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

# Run SERVICE_SOME_VAR=xyz SERVICE_BOT_TOKEN=token SERVICE_MONGO_HOST=localhost SERVICE_MONGO_PORT=12 python prefixes.py
# Output:
# Meta:
# env.Meta.SOME_VAR='xyz'
# env.Meta.SOME_OTHER_VAR='this is default value'
#
# Bot:
# env.Bot.TOKEN='token'
#
# Mongo:
# env.Mongo.HOST='localhost'
# env.Mongo.PORT=12
