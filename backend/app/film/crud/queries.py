GET_MANY_FILMS = """SELECT id, title, imdb_id, is_adult, tagline, poster_url FROM "film" OFFSET :offset LIMIT :limit;"""

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
poster_url,
production_companies,
production_countries
FROM "film" WHERE id = :id;"""

GET_ALL_PRODUCTION_COUNTRIES = """SELECT
production_country -> 'iso_3166_1' as iso_name, 
production_country -> 'name' as public_name 
FROM (SELECT DISTINCT JSONB_ARRAY_ELEMENTS(production_countries) as production_country FROM "film") as production_countries;"""

GET_ALL_GENRES = (
    """SELECT DISTINCT JSONB_ARRAY_ELEMENTS(genres) as genre FROM "film";"""
)

SEARCH_FILMS_BY_TITLE = (
    """SELECT id, title, is_adult, tagline FROM "film" WHERE LOWER(title) LIKE :title"""
)

UPDATE_POSTER_URL = (
    """UPDATE "film" SET poster_url = :poster_url WHERE id = :film_id;"""
)


# Архив душевнобольного, не обращайте внимания :)

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
