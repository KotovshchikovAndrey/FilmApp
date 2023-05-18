from alembic import op
import sqlalchemy as sa

from enum import Enum
from app.core import config

revision = "0eb9898f26d1"
down_revision = None
branch_labels = None
depends_on = None


def create_user_table() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(30), nullable=False),
        sa.Column("surname", sa.String(30), nullable=False),
        sa.Column("email", sa.String(50), nullable=False, unique=True),
        sa.Column("password", sa.TEXT(), nullable=False),
        sa.Column("avatar", sa.String(255), nullable=True),
        sa.Column("status", sa.String(15), nullable=False),
        sa.Column("role", sa.String(5), nullable=False),
        sa.Column(
            "refresh_tokens",
            sa.ARRAY(sa.TEXT()),
            nullable=False,
            server_default="{}",
        ),
        sa.Column(
            "reset_codes",
            sa.JSON(none_as_null=True),
            nullable=False,
            server_default="[]",
        ),
    )


def create_film_table() -> None:
    op.create_table(
        "film",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("budget", sa.Integer(), nullable=False),
        sa.Column("is_adult", sa.Boolean(), nullable=False),
        sa.Column("language", sa.String(255), nullable=True),
        sa.Column("imdb_id", sa.String(255), nullable=True),
        sa.Column("poster_path", sa.String(255), nullable=True),
        sa.Column("release_date", sa.DATE(), nullable=True),
        sa.Column("time", sa.Float(), nullable=True),
        sa.Column("tagline", sa.TEXT(), nullable=True),
        sa.Column("genres", sa.TEXT(), nullable=False),
        sa.Column("production_companies", sa.TEXT(), nullable=True),
        sa.Column("production_countries", sa.TEXT(), nullable=True),
    )


def create_raiting_table() -> None:
    op.create_table(
        "raiting",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("value", sa.NUMERIC(1, 1), nullable=False),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("user.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "film_id",
            sa.Integer(),
            sa.ForeignKey("film.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )


def create_favorite_user_film_table() -> None:
    op.create_table(
        "favorite_user_film",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("user.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "film_id",
            sa.Integer(),
            sa.ForeignKey("film.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )


def upgrade() -> None:
    create_user_table()
    create_film_table()
    create_favorite_user_film_table()
    create_raiting_table()

    op.execute(
        """
        COPY film
("title",
"description",
"budget",
"is_adult",
"language",
"imdb_id",
"poster_path",
"release_date",
"time",
"tagline",
"genres",
"production_companies",
"production_countries") FROM '%s' DELIMITERS ',' CSV HEADER;

ALTER TABLE "film" ALTER COLUMN genres TYPE jsonb USING genres::jsonb;


create or replace function is_valid_json(p_json text)
  returns boolean
as
$$
begin
  return (p_json::json is not null);
exception
  when others then
     return false;
end;
$$
language plpgsql
immutable;


UPDATE "film"
SET production_companies = NULL
WHERE is_valid_json(production_companies) = FALSE;

ALTER TABLE "film" ALTER COLUMN production_companies TYPE jsonb USING production_companies::jsonb;


UPDATE "film"
SET production_countries = NULL
WHERE is_valid_json(production_countries) = FALSE;

ALTER TABLE "film" ALTER COLUMN production_countries TYPE jsonb USING production_countries::jsonb;

ALTER TABLE "user" ALTER COLUMN reset_codes TYPE jsonb USING reset_codes::jsonb;


CREATE TYPE user_role AS ENUM('user', 'admin', 'owner');
CREATE TYPE user_status AS ENUM('active', 'not_verified', 'banned', 'muted');

ALTER TABLE "user" ALTER COLUMN role TYPE user_role USING role::user_role;
ALTER TABLE "user" ALTER COLUMN status TYPE user_status USING status::user_status;
"""
        % config.CSV_DATASET_PATH
    )


def downgrade() -> None:
    op.drop_table("raiting")
    op.drop_table("favorite_user_film")
    op.drop_table("user")
    op.drop_table("film")

    op.execute("""DROP TYPE "user_role"; DROP TYPE user_status;""")
