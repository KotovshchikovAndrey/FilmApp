from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

env_config = Config(".env")

DATABASE_URL = env_config("DATABASE_URL", cast=str)
