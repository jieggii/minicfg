# minicfg
📑 **minicfg** is a lightweight, minimalistic and easy-to-use configuration package for your Python services.

## Features
- **Lightweight**: minicfg is a small package with no dependencies.
- **Easy to use**: minicfg provides a simple API to define and populate configurations.
- **Documentation**: generate documentation for your configuration.
- **Type casting**: minicfg supports type casting for the fields. You can also define your own casters.
- **File field attachment**: minicfg supports attaching a virtual file field to a field.
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
from minicfg import Minicfg, Field, minicfg_name
from minicfg.caster import IntCaster


@minicfg_name("SERVICE")
class MyConfig(Minicfg):
    @minicfg_name("DATABASE")
    class Database(Minicfg):
        HOST = Field(attach_file_field=True)
        PORT = Field(caster=IntCaster())
    
    @minicfg_name("EXTERNAL_API")
    class ExternalAPI(Minicfg):
        KEY = Field()
        USER_ID = Field(caster=IntCaster())
    
if __name__ == '__main__':
    config = MyConfig()  # create an instance of the configuration
    config.populate()  # populate the configuration from the environment variables
    
    print(f"connect to database at {config.Database.HOST}:{config.Database.PORT}")
    print(f"external API key: {config.ExternalAPI.KEY}")
    print(f"external API user: {config.ExternalAPI.USER_ID}")
```

> Try running the script with the following environment variables:
> - `SERVICE_DATABASE_HOST=example.com`
> - `SERVICE_DATABASE_PORT=5432`
> - `SERVICE_EXTERNAL_API_KEY=token`
> - `SERVICE_EXTERNAL_API_USER_ID=123`
> And you should see the following output:
> ```
> connect to database at example.com:5432
> external API key: token
> external API user: 123
> ```

> More examples are available [here](/examples).

The documentation generated using minicfg for this class would look like this:
(use `$ minicifg --format markdown example.MyConfig` to generate docs).

**SERVICE**
| Name | Type | Default | Description |
| ---- | ---- | ------- | ----------- |

**SERVICE_DATABASE**
| Name                         | Type  | Default | Description   |
| ---------------------------- | ----- | ------- | ------------- |
| `SERVICE_DATABASE_HOST`      | `str` | N/A     | database host |
| `SERVICE_DATABASE_HOST_FILE` | `str` | N/A     |               |
| `SERVICE_DATABASE_PORT`      | `int` | N/A     | database port |


**SERVICE_EXTERNAL_API**
| Name                           | Type  | Default | Description          |
| ------------------------------ | ----- | ------- | -------------------- |
| `SERVICE_EXTERNAL_API_KEY`     | `str` | N/A     | external API key     |
| `SERVICE_EXTERNAL_API_USER_ID` | `int` | N/A     | external API user ID |

