import pathlib
from starlette.config import Config
from starlette.datastructures import Secret

env_config = Config(".env")

SECRET_KEY = env_config("SECRET_KEY", cast=Secret)

# Production Database
DB_USER = env_config("DB_USER", cast=str)
DB_PASSWORD = env_config("DB_PASSWORD", cast=str)
DB_HOST = env_config("DB_HOST", cast=str)
DB_PORT = env_config("DB_PORT", cast=str)
DB_NAME = env_config("DB_NAME", cast=str)


# Testing Database
TEST_DB_USER = env_config("TEST_DB_USER", cast=str)
TEST_DB_PASSWORD = env_config("TEST_DB_PASSWORD", cast=str)
TEST_DB_HOST = env_config("TEST_DB_HOST", cast=str)
TEST_DB_PORT = env_config("TEST_DB_PORT", cast=str)
TEST_DB_NAME = env_config("TEST_DB_NAME", cast=str)


CSV_DATASET_PATH = env_config("CSV_DATASET_PATH", cast=str)

UPLOAD_URL = "/media"
UPLOAD_DIR = str((pathlib.Path("app") / "media").absolute())

TMDB_API_KEY = env_config("TMDB_API_KEY", cast=str)
# MAIL_LOGIN = env_config("MAIL_LOGIN", cast=str)
# MAIL_PASSWORD = env_config("MAIL_PASSWORD", cast=str)

# CORS
ALLOW_ORIGINS = ["*"]  # Потом впишем адрес нашего сервера, откуда рендериться frontend
