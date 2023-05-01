# # import typing as tp

# # import pydantic
# # from pydantic import validator
# # import json
# # import databases


# # class Film(pydantic.BaseModel):
# #     id: int
# #     original_title: str
# #     overview: tp.Optional[str] = None
# #     genres: str
# #     original_language: str
# #     production_companies: tp.Optional[str] = None
# #     production_countries: tp.Optional[str] = None
# #     poster_path: tp.Optional[str]
# #     imdb_id: str
# #     release_date: tp.Optional[str] = None
# #     adult: tp.Optional[bool] = None
# #     runtime: tp.Optional[float] = 0
# #     budget: int
# #     tagline: tp.Optional[str]

# #     @validator(
# #         "original_title",
# #         "overview",
# #         "original_language",
# #         "poster_path",
# #         "imdb_id",
# #         "release_date",
# #         "tagline",
# #     )
# #     def validate_all(cls, value: str):
# #         if value is not None:
# #             return value.replace("'", '"').replace('d"', '"')

# #     @validator("runtime")
# #     def validate_p(cls, value):
# #         if value is None:
# #             return float(0)

# #         return value

# #     @validator("release_date")
# #     def validate_d(cls, value):
# #         if value is None:
# #             return "null"

# #         return value

# #     @validator(
# #         "genres",
# #         "production_companies",
# #         "production_countries",
# #     )
# #     def validate_j(cls, value: str):
# #         if value is not None:
# #             value = value.replace("'", '"').replace('d"', '"')
# #             try:
# #                 j = json.loads(value.strip())
# #                 s = json.dumps(j)
# #                 return s
# #             except Exception as e:
# #                 print(value, e)
# #                 return "null"

# #     class Config:
# #         orm_mode = True


# # async def parse_from_test_db(connection, offset: int = 0):
# #     old_db = databases.Database(
# #         url="postgresql+psycopg2://postgres:12345@127.0.0.1:5432/film_db",
# #     )

# #     await old_db.connect()

# #     select_query = """
# #     SELECT
# #         id,
# #         original_title,
# #         overview,
# #         genres,
# #         original_language,
# #         production_companies,
# #         production_countries,
# #         poster_path,
# #         imdb_id,
# #         release_date,
# #         adult,
# #         runtime,
# #         budget,
# #         tagline
# #     FROM "film" ORDER BY id OFFSET 5
# #     """

# #     results = await old_db.fetch_all(select_query)
# #     for result in results:
# #         Film.update_forward_refs()
# #         film = Film(**result)

# #         insert_query = """
# #         INSERT INTO "film"
# #         (title, description, genres, language, production_companies, production_countries, poster_path, trailer_path, release_date, is_adult, time, budget, tagline)
# #         VALUES
# #         ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', {8}, '{9}', {10}, {11}, '{12}');
# #         """.format(
# #             film.original_title,
# #             film.overview,
# #             film.genres,
# #             film.original_language,
# #             film.production_companies,
# #             film.production_countries,
# #             film.poster_path,
# #             film.imdb_id,
# #             film.release_date,
# #             film.adult,
# #             film.runtime,
# #             film.budget,
# #             film.tagline,
# #         )

# #         print(f"Запись с id={film.id}")
# #         print(insert_query)
# #         raise

# #         await connection.execute_query(insert_query)


# # async def get_offset_by_id(id: int):
# #     ...

import pandas as pd
import json
from pprint import pprint


file_path = r"C:\Users\Andrey\Downloads/Gold.csv"
writable_file = r"C:\Users\Andrey\Downloads\sex2.csv"
ids = set()
with open(writable_file, "w", encoding="UTF-8") as file:
    df = pd.read_csv(file_path, low_memory=False)
    length = len(df.get("id"))
    conuter = 0
    for index in range(length):
        id = df.get("id")[index]
        if id in ids:
            continue

        title = df.get("original_title")[index]
        description = df.get("overview")[index]
        language = df.get("original_language")[index]
        poster_path = df.get("poster_path")[index]
        trailer_path = df.get("imdb_id")[index]
        release_date = df.get("release_date")[index]
        is_adult = df.get("adult")[index]
        time = df.get("runtime")[index]
        budget = df.get("budget")[index]
        tagline = df.get("tagline")[index]

        try:
            production_companies = df.get("production_companies")[index]
            json.loads(production_companies.replace("'", '"'))
        except:
            production_companies = ""

        try:
            production_countries = df.get("production_countries")[index]
            json.loads(production_countries.replace("'", '"'))
        except:
            production_countries = ""

        try:
            genres = df.get("genres")[index].strip()
            json.loads(genres.replace("'", '"'))
        except:
            genres = ""

        ids.add(id)
        (
            file.write(
                "|".join(
                    map(
                        str,
                        [
                            title,
                            description,
                            genres,
                            language,
                            production_companies,
                            production_countries,
                            poster_path,
                            trailer_path,
                            release_date,
                            is_adult,
                            time,
                            budget,
                            tagline,
                        ],
                    )
                )
                + ";"
            )
        )

import pathlib

filepath = pathlib.Path(writable_file)
pd.DataFrame.to_csv(writable_file, encoding="UTF-8")
# pd.read_f
# # print(
# #     """SELECT SELECT * FROM "film" WHERE imdb_id = %(sex)s"""
# #     % {"sex": '(SELECT imdb_id FROM "film" LIMIT 1)'}
# # )
# print(conuter)
# # print(json.loads(production_country))
# # j = pd.json_normalize()
# # print(j)
# # for row in file:
# #     _, genres, *_ = row.split(",")
# #     print(genres)
