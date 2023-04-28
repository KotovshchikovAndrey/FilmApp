from alembic import op
import sqlalchemy as sa

import uuid


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
            "reset_token",
            sa.String(255),
            nullable=False,
            default=uuid.uuid4(),
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
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(30), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("file", sa.String(255), nullable=False),
        sa.Column("poster", sa.String(255), nullable=False),
        sa.Column("trailer", sa.String(255), nullable=False),
        sa.Column("country", sa.String(30), nullable=False),
        sa.Column("release_date", sa.Date(), nullable=False),
        sa.Column("age_rating", sa.String(3), nullable=False, default="0+"),
        sa.Column("time", sa.String(30), nullable=False),
    )


def create_frame_table() -> None:
    op.create_table(
        "frame",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(30), nullable=False),
        sa.Column(
            "film_id",
            sa.Integer(),
            sa.ForeignKey("film.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )


def create_genre_table() -> None:
    op.create_table(
        "genre",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(30), nullable=False),
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


def create_film_genre_table() -> None:
    op.create_table(
        "film_genre",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "film_id",
            sa.Integer(),
            sa.ForeignKey("film.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "genre_id",
            sa.Integer(),
            sa.ForeignKey("genre.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )


def upgrade() -> None:
    create_user_table()
    create_token_table()
    create_film_table()
    create_frame_table()
    create_genre_table()
    create_favorite_user_film_table()
    create_film_genre_table()


def downgrade() -> None:
    op.drop_table("favorite_user_film")
    op.drop_table("film_genre")
    op.drop_table("token")
    op.drop_table("user")
    op.drop_table("frame")
    op.drop_table("film")
    op.drop_table("genre")
