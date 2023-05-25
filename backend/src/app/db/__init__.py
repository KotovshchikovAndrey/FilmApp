import os

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


def create_testing_connection() -> IDbConnection:
    db_connection = PostgresConnection(
        db_user=config.TEST_DB_USER,
        db_password=config.TEST_DB_PASSWORD,
        db_host=config.TEST_DB_HOST,
        db_port=config.TEST_DB_PORT,
        db_name=config.TEST_DB_NAME,
    )

    return db_connection


if os.environ.get("IS_TESTING", False):
    print("connection to testing database")
    db_connection = create_testing_connection()
else:
    print("connection to production database")
    db_connection = create_connection()
