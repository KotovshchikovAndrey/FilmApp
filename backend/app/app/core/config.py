from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

env_config = Config(".env")

SECRET_KEY = env_config("SECRET_KEY", cast=Secret)

# DATABASE_URL = env_config("DATABASE_URL", cast=str)

DB_USER = env_config("DB_USER", cast=str)
DB_PASSWORD = env_config("DB_PASSWORD", cast=str)
DB_HOST = env_config("DB_HOST", cast=str)
DB_PORT = env_config("DB_PORT", cast=str)
DB_NAME = env_config("DB_NAME", cast=str)
