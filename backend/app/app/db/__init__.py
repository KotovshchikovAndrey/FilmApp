from app.core import config
from .connections.postgres import IDbConnection, PostgresConnection


def create_connection() -> IDbConnection:
    db_connection = PostgresConnection(
        db_user=config.DB_USER,
        db_password=config.DB_PASSWORD,
        db_host=config.DB_HOST,
        db_port=config.DB_PORT,
        db_name=config.DB_NAME,
    )

    return db_connection


db_connection = create_connection()
