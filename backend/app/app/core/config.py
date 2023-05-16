from starlette.config import Config
from starlette.datastructures import Secret

env_config = Config(".env")

SECRET_KEY = env_config("SECRET_KEY", cast=Secret)

DB_USER = env_config("DB_USER", cast=str)
DB_PASSWORD = env_config("DB_PASSWORD", cast=str)
DB_HOST = env_config("DB_HOST", cast=str)
DB_PORT = env_config("DB_PORT", cast=str)
DB_NAME = env_config("DB_NAME", cast=str)
CSV_DATASET_PATH = env_config("CSV_DATASET_PATH", cast=str)
# MAIL_LOGIN = env_config("MAIL_LOGIN", cast=str)
# MAIL_PASSWORD = env_config("MAIL_PASSWORD", cast=str)
