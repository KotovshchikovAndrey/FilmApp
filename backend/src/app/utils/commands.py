import typing as tp

import os
from alembic import command
from alembic.config import Config


def run_migrations() -> None:
    script_location = os.path.join(os.getcwd(), r"src\app\db\migrations")
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", script_location)
    command.upgrade(alembic_cfg, "head")


def drop_tables() -> None:
    script_location = os.path.join(os.getcwd(), r"src\app\db\migrations")
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", script_location)
    command.downgrade(alembic_cfg, "-1")
