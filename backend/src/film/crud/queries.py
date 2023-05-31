GET_MANY_FILMS = """SELECT id, title, imdb_id, is_adult, tagline FROM "film" OFFSET :offset LIMIT :limit;"""

FILTER_FILMS_BY_CONDITIONS = """SELECT id, title, is_adult, tagline FROM 
(SELECT 
id,
title,
is_adult,
tagline, 
jsonb_array_elements(genres) as genre, 
jsonb_array_elements(production_countries) as country 
FROM "film") as T WHERE """

GET_FILM_BY_ID = """SELECT
id,
title, 
description, 
release_date,  
genres,
time,
budget,
is_adult,
imdb_id,
language,
production_companies,
production_countries
FROM "film" WHERE id = :id;"""

GET_ALL_PRODUCTION_COUNTRIES = """SELECT
production_country -> 'iso_3166_1' as iso_3166_1, 
production_country -> 'name' as name 
FROM (SELECT DISTINCT JSONB_ARRAY_ELEMENTS(production_countries) as production_country FROM "film") as production_countries;"""

GET_ALL_GENRES = (
    """SELECT DISTINCT JSONB_ARRAY_ELEMENTS(genres) as genre FROM "film";"""
)

GET_IMDB_ID = """SELECT imdb_id FROM "film" WHERE id = :film_id;"""

SEARCH_FILMS_BY_TITLE = (
    """SELECT id, title, is_adult, tagline FROM "film" WHERE LOWER(title) LIKE :title"""
)

UPDATE_POSTER_URL = (
    """UPDATE "film" SET poster_url = :poster_url WHERE id = :film_id;"""
)

CREATE_NEW_FILM = """INSERT INTO "film" 
(
title, 
description, 
budget, 
is_adult, 
language, 
imdb_id,
release_date,
time, 
tagline, 
genres,
production_countries,
production_companies
) 
VALUES
(
	:title, 
    :description, 
    :budget, 
    :is_adult, 
    :language, 
    :imdb_id,
    :release_date,
    :time, 
    :tagline, 
    :genres,
    :production_countries,
    :production_companies
) RETURNING id;"""

UPDATE_FILM = """UPDATE "film" SET
title = COALESCE(:title, title),
description = COALESCE(:description, description),
budget = COALESCE(:budget, budget),
is_adult = COALESCE(:is_adult, is_adult),
language = COALESCE(:language, language),
imdb_id = COALESCE(:imdb_id, imdb_id),
release_date = COALESCE(:release_date, release_date),
time = COALESCE(:time, time),
tagline = COALESCE(:tagline, tagline),
genres = COALESCE(:genres, genres),
production_countries = COALESCE(:production_countries, production_countries),
production_companies = COALESCE(:production_companies, production_companies)
WHERE id = :film_id RETURNING id;"""

DELETE_FILM_BY_ID = """DELETE FROM "film" WHERE id = :film_id RETURNING id;"""

GET_FAVORITE_FILMS = """SELECT * FROM "film"
WHERE id IN (SELECT film_id from "favorite_user_film" WHERE user_id = :target_id)
"""

GET_USER_FAVORITE_FILMS = """SELECT 
film.id,
title,
is_adult,
tagline
FROM "film" as film JOIN "favorite_user_film" as user_film
ON film.id = user_film.film_id 
WHERE user_film.user_id = :user_id
ORDER BY 
"""

AGGREGATE_AVG_FILM_RATING = """SELECT film_id, AVG(value)::float as rating FROM "rating"
WHERE film_id = :film_id
GROUP BY film_id;"""

SET_FILM_RATING = """INSERT INTO "rating" (user_id, film_id, value)
VALUES (:user_id, :film_id, :value) ON CONFLICT (user_id, film_id) DO
UPDATE SET value = EXCLUDED.value;"""

RESET_FILM_RATING = """DELETE FROM "rating"
WHERE user_id = :user_id AND film_id = :film_id;"""


# Архив душевнобольного, не обращайте внимания :)

# UPDATE_FILM = """UPDATE "film" SET
# title = CASE WHEN :title IS NOT NULL THEN :title ELSE title END,
# description = CASE WHEN :description IS NOT NULL THEN :description ELSE description END,
# budget = CASE WHEN :budget IS NOT NULL THEN :budget ELSE budget END,
# is_adult = CASE WHEN :is_adult IS NOT NULL THEN :is_adult ELSE is_adult END,
# language = CASE WHEN :language IS NOT NULL THEN :language ELSE language END,
# imdb_id = CASE WHEN :imdb_id IS NOT NULL THEN :imdb_id ELSE imdb_id END,
# release_date = CASE WHEN :release_date IS NOT NULL THEN :release_date ELSE release_date END,
# time = CASE WHEN :time IS NOT NULL THEN :time ELSE time END,
# tagline = CASE WHEN :tagline IS NOT NULL THEN :tagline ELSE tagline END,
# genres = CASE WHEN :genres IS NOT NULL THEN :genres ELSE genres END,
# production_countries = CASE WHEN :production_countries IS NOT NULL THEN :production_countries ELSE production_countries END,
# production_companies = CASE WHEN :production_companies IS NOT NULL THEN :production_companies ELSE production_companies END
# WHERE id = :film_id RETURNING id;"""

# -- SELECT id, title, is_adult, tagline FROM "film"  WHERE ;
# -- SELECT DISTINCT ON (production_countries -> 0 -> 'iso_3166_1')
# -- production_countries -> 0 -> 'iso_3166_1' as alias_name,
# -- production_countries -> 0 -> 'name' as public_name
# -- FROM "film" WHERE production_countries -> 0 -> 'iso_3166_1' IS NOT NULL;
# -- SELECT id, title, is_adult, tagline
# -- WHERE DISTINCT ON (production_countries -> 0 -> 'iso_3166_1')
# -- FROM "film";
# -- SELECT DISTINCT ON (genres -> 0 -> 'name') genres -> 0 -> 'name' FROM "film"
# -- WHERE genres -> 0 -> 'name' IS NOT NULL;
# -- SELECT genres FROM "film" WHERE genres::text LIKE '%"Music"%';
# -- SELECT value -> 'name' FROM json_array_elements((SELECT genres FROM "film" LIMIT 1)::json);
# -- SELECT DISTINCT JSONB_ARRAY_ELEMENTS_TEXT(genres) FROM "film";

# -- SELECT genre -> 'name' FROM (SELECT DISTINCT JSONB_ARRAY_ELEMENTS(genres) as genre FROM "film") as genres;

# -- SELECT
# -- production_country -> 'iso_3166_1' as alias_name,
# -- production_country -> 'name' as public_name
# -- FROM (SELECT DISTINCT JSONB_ARRAY_ELEMENTS(production_countries) as production_country FROM "film") as production_countries;
