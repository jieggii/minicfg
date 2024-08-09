from minicfg.caster import to_int
from minicfg.field import Field
from minicfg.minicfg import Minicfg


class Env(Minicfg):
    # DATABASE HOST will be set to localhost if no value provided
    DATABASE_HOST: str = Field(default="localhost")

    # DATABASE_PORT value will be cast to int
    DATABASE_PORT: int = Field(caster=to_int)


env = Env()
env.populate()

print(f"{env.DATABASE_HOST=}")
print(f"{env.DATABASE_PORT=}")

# Try running DATABASE_HOST=127.0.0.1 DATABASE_PORT=5432 python simple.py
# Output:
# >>> env.DATABASE_HOST='127.0.0.1'
# >>> env.DATABASE_PORT=5432

# Or DATABASE_PORT=5432 python simple.py
# Output:
# >>> env.DATABASE_HOST='localhost'  # default value is used
# >>> env.DATABASE_PORT=5432
