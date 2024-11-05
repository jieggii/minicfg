# minicfg
📑 **minicfg** is a lightweight, minimalistic and easy-to-use configuration package for your Python services.

## Features
- **Lightweight**: minicfg is a small package with no dependencies.
- **Easy to use**: minicfg provides a simple API to define and populate configurations.
- **Type casting**: minicfg supports type casting for the fields.
- **File attachment**: minicfg supports attaching a file to a field.
- **Prefixing**: minicfg supports prefixing the fields with a custom name prefix.
- **Nested configurations**: minicfg supports nested configurations.
- **Custom providers**: minicfg supports custom providers to populate the configuration from different sources.

## Installation
Just install minicfg using your favorite package manager, for example:
```bash
pip install minicfg
```

## Usage
```python
from minicfg import Minicfg, Field, minicfg_prefix
from minicfg.caster import IntCaster

@minicfg_prefix("MYSERVICE")
class Env(Minicfg):
    @minicfg_prefix("BOT")
    class TelegramBot(Minicfg):
        # attach_file_field=True will read the value from the file provided in MYSERVICE_BOT_TOKEN_FILE env var
        # if no file is provided, it will read the value from MYSERVICE_BOT_TOKEN env var.
        TOKEN = Field(attach_file_field=True)
    
    class API1(Minicfg):  # <-- API1 class name will be used as a prefix for the fields inside it
        API_TOKEN = Field()  # API_TOKEN will be read from MYSERVICE_API1_API_TOKEN env var

    @minicfg_prefix("MONGO")
    class Mongo(Minicfg):
        HOST = Field()
        PORT = Field(caster=IntCaster())  # PORT will be casted to an integer type
        

# Populate the configuration from the environment variables:
env = Env.populated()

print(f"Bot token: {env.TelegramBot.TOKEN}")
print(f"Mongo settings: {env.Mongo.HOST}:{env.Mongo.PORT}")

"""
Try running the script with the following environment variables:
SERVICE_BOT_TOKEN=token SERVICE_MONGO_HOST=localhost SERVICE_MONGO_PORT=5432
And you will get

>>> Bot token: token
>>> Mongo settings: localhost:5432
"""
```

> More examples are available [here](/examples).

