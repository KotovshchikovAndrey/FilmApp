import os

import sqlalchemy as sa
from alembic import op

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
        sa.Column("is_public", sa.Boolean(), nullable=False, server_default="false"),
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


def create_rating_table() -> None:
    op.create_table(
        "rating",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("value", sa.NUMERIC(2, 1), nullable=False, server_default="0"),
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

    op.execute("""create unique index unique_rating on rating (user_id, film_id);""")


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
        sa.Column("added_date", sa.TIMESTAMP(), nullable=False),
    )

    op.execute(
        """create unique index unique_favorite_film on favorite_user_film (user_id, film_id);"""
    )


def create_watchstatus_user_film_table() -> None:
    op.create_table(
        "watchstatus_user_film",
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
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("updated_date", sa.TIMESTAMP(), nullable=True),
    )

    op.execute(
        """create unique index unique_watchstatus on watchstatus_user_film (user_id, film_id);"""
    )


def create_comment_table() -> None:
    op.create_table(
        "comment",
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
        sa.Column(
            "parent_comment",
            sa.ForeignKey("comment.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("text", sa.TEXT(), nullable=False),
        sa.Column("added_date", sa.TIMESTAMP(), nullable=False),
    )


def create_set_updated_date_function() -> None:
    op.execute(
        f"""
    CREATE FUNCTION set_updated_date()
RETURNS trigger AS $$
BEGIN
  IF NEW.status != OLD.status THEN
    NEW.updated_date := (SELECT NOW()::timestamp);
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;"""
    )


def create_set_added_date_function() -> None:
    op.execute(
        f"""
    CREATE FUNCTION set_added_date()
RETURNS trigger AS $$
BEGIN
  IF NEW.added_date IS NULL THEN
    NEW.added_date := (SELECT NOW()::timestamp);
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;"""
    )


def create_set_added_date_trigger_for_table(table: str):
    op.execute(
        f"""CREATE TRIGGER set_added_date
BEFORE INSERT
ON {table}
FOR EACH ROW
EXECUTE PROCEDURE set_added_date();"""
    )


def create_set_updated_date_trigger_for_table(table: str):
    op.execute(
        f"""CREATE TRIGGER set_updated_date
BEFORE UPDATE
ON {table}
FOR EACH ROW
EXECUTE PROCEDURE set_updated_date();"""
    )


def normolize_json_fields_in_csv_data() -> None:
    op.execute(
        """ALTER TABLE "film" ALTER COLUMN genres TYPE jsonb USING genres::jsonb;

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
SET production_companies = '[]'
WHERE is_valid_json(production_companies) = FALSE;


ALTER TABLE "film" ALTER COLUMN production_companies TYPE jsonb USING production_companies::jsonb;


UPDATE "film"
SET production_countries = '[]'
WHERE is_valid_json(production_countries) = FALSE;


ALTER TABLE "film" ALTER COLUMN production_countries TYPE jsonb USING production_countries::jsonb;
ALTER TABLE "user" ALTER COLUMN reset_codes TYPE jsonb USING reset_codes::jsonb;"""
    )


def load_csv_data() -> None:
    csv_data = config.CSV_DATASET_PATH
    if os.environ.get("IS_TESTING", False):
        csv_data = config.CSV_TESTING_DATA_PATH or csv_data

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
"production_countries") FROM '%s' DELIMITERS ',' CSV HEADER;"""
        % csv_data
    )

    normolize_json_fields_in_csv_data()

    # Пока захардкодил. Если нужно будет, полностью удалим из датасет файла,
    # так как не используем данное поле
    op.execute("""ALTER TABLE "film" DROP COLUMN poster_path;""")


def create_custom_types() -> None:
    op.execute(
        """CREATE TYPE user_role AS ENUM('user', 'admin', 'owner');
CREATE TYPE user_status AS ENUM('active', 'not_verified', 'banned', 'muted');
CREATE TYPE watch_status AS ENUM('not_watching', 'watching', 'in_plans', 'scheduled', 'watched', 'postponed', 'abandoned');


ALTER TABLE "user" ALTER COLUMN role TYPE user_role USING role::user_role;
ALTER TABLE "user" ALTER COLUMN status TYPE user_status USING status::user_status;

ALTER TABLE "watchstatus_user_film" ALTER COLUMN status TYPE watch_status USING status::watch_status;"""
    )


def upgrade() -> None:
    create_user_table()
    create_film_table()
    create_comment_table()
    create_favorite_user_film_table()
    create_rating_table()
    create_watchstatus_user_film_table()

    create_set_added_date_function()
    create_set_updated_date_function()

    create_set_added_date_trigger_for_table("favorite_user_film")
    create_set_added_date_trigger_for_table("comment")
    create_set_updated_date_trigger_for_table("watchstatus_user_film")

    load_csv_data()
    create_custom_types()


def downgrade() -> None:
    op.drop_table("rating")
    op.drop_table("favorite_user_film")
    op.drop_table("watchstatus_user_film")
    op.drop_table("comment")
    op.drop_table("user")
    op.drop_table("film")

    op.execute(
        """DROP TYPE "user_role"; DROP TYPE user_status; DROP TYPE watch_status;"""
    )
    op.execute("""drop function set_added_date() cascade;""")
    op.execute("""drop function set_updated_date() cascade;""")
