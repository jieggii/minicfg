# minicfg
Lightweight and opinionated config library for your Python services.

```python
from minicfg.minicfg import Minicfg, minicfg_prefix
from minicfg.field import Field
from minicfg.caster import IntCaster

@minicfg_prefix("SERVICE")
class Env(Minicfg):
    @minicfg_prefix("BOT")
    class Bot(Minicfg):
        # SERVICE_BOT_TOKEN or SERVICE_BOT_TOKEN_FILE env var
        # will be used to populate TOKEN field value:
        TOKEN = Field(attach_file_field=True)

    @minicfg_prefix("MONGO")
    class Mongo(Minicfg):
        HOST = Field()
        PORT = Field(caster=IntCaster())  # PORT will be cast to int


env = Env()
env.populate()  # populate the config using env vars (by default)

print(f"Bot token: {env.Bot.TOKEN}")
print(f"Mongo settings: {env.Mongo.HOST}:{env.Mongo.PORT}")

# Run SERVICE_BOT_TOKEN=token SERVICE_MONGO_HOST=localhost SERVICE_MONGO_PORT=5432 python example.py
# Output:
# >>> Bot token: token
# >>> Mongo settings: localhost:5432
```
