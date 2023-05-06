from alembic import op
import sqlalchemy as sa

import uuid

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
        sa.Column("email", sa.String(30), nullable=False, unique=True),
        sa.Column("password", sa.String(255), nullable=False),
        sa.Column("avatar", sa.String(255), nullable=True),
        sa.Column(
            "roles",
            sa.ARRAY(sa.TEXT),
            nullable=False,
            server_default="{}",
        ),
        sa.Column(
            "reset_code",
            sa.String(255),
            nullable=False,
            server_default=sa.func.gen_random_uuid(),
        ),
    )


def create_token_table() -> None:
    op.create_table(
        "token",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("value", sa.String(255), nullable=False),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("user.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )


def create_film_table() -> None:
    op.create_table(
        "film",
        sa.Column("is_adult", sa.Boolean(), nullable=False),
        sa.Column("nax1", sa.TEXT(), nullable=True),
        sa.Column("budget", sa.Integer(), nullable=False),
        sa.Column("genres", sa.TEXT(), nullable=False),
        sa.Column("nax2", sa.TEXT(), nullable=True),
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("imdb_id", sa.String(255), nullable=True),
        sa.Column("language", sa.String(255), nullable=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("nax3", sa.TEXT(), nullable=True),
        sa.Column("poster_path", sa.String(255), nullable=True),
        sa.Column("production_companies", sa.TEXT(), nullable=True),
        sa.Column("production_countries", sa.TEXT(), nullable=True),
        sa.Column("release_date", sa.String(15), nullable=True),
        sa.Column("nax4", sa.TEXT(), nullable=True),
        sa.Column("time", sa.Float(), nullable=True),
        sa.Column("nax5", sa.TEXT(), nullable=True),
        sa.Column("nax6", sa.TEXT(), nullable=True),
        sa.Column("tagline", sa.TEXT(), nullable=True),
        sa.Column("nax7", sa.String(255), nullable=True),
        sa.Column("nax8", sa.TEXT(), nullable=True),
        sa.Column("nax9", sa.TEXT(), nullable=True),
        sa.Column("nax10", sa.TEXT(), nullable=True),
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
    create_token_table()
    create_film_table()
    create_favorite_user_film_table()
    create_raiting_table()

    op.execute(
        """
        COPY film
(is_adult,
nax1,
budget,
genres,
nax2,
id,
imdb_id,
language,
title,
description,
nax3,
poster_path,
production_companies,
production_countries,
release_date,
nax4,
time,
nax5,
nax6,
tagline,
nax7,
nax8,
nax9,
nax10) FROM '%s' DELIMITERS ',' CSV HEADER;

UPDATE "film"
SET genres = replace(replace(genres, '"', ''), '''', '"')::json;

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
SET production_companies = replace(replace(production_companies, '"', ''), '''', '"');

UPDATE "film"
SET production_companies = NULL
WHERE is_valid_json(production_companies) = FALSE;

ALTER TABLE "film" ALTER COLUMN production_companies TYPE jsonb USING production_companies::jsonb;


UPDATE "film"
SET production_countries = replace(replace(production_countries, '"', ''), '''', '"');

UPDATE "film"
SET production_countries = NULL
WHERE is_valid_json(production_countries) = FALSE;

ALTER TABLE "film" ALTER COLUMN production_countries TYPE jsonb USING production_countries::jsonb;

ALTER TABLE "film" 
DROP COLUMN nax1, 
DROP COLUMN nax2, 
DROP COLUMN nax3, 
DROP COLUMN nax4, 
DROP COLUMN nax5, 
DROP COLUMN nax6, 
DROP COLUMN nax7, 
DROP COLUMN nax8, 
DROP COLUMN nax9, 
DROP COLUMN nax10;
"""
        % config.CSV_DATASET_PATH
    )


def downgrade() -> None:
    op.drop_table("raiting")
    op.drop_table("favorite_user_film")
    op.drop_table("token")
    op.drop_table("user")
    op.drop_table("film")
