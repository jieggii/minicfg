from minicfg.minicfg import Minicfg
from minicfg.field import Field
from minicfg.caster import to_int

class Env(Minicfg):
    DATABASE_HOST = Field()
    DATABASE_PORT = Field(caster=to_int)


env = Env()
env.populate()

print(f"{env.DATABASE_HOST=}")
print(f"{env.DATABASE_PORT=}")


# Try running DATABASE_HOST=localhost DATABASE_PORT=5432 python simple.py
# Output:
# >>> env.DATABASE_HOST='localhost'
# >>> env.DATABASE_PORT=5432
