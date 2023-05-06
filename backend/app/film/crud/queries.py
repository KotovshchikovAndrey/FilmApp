GET_MANY_FILMS = (
    """SELECT id, title, is_adult FROM "film" OFFSET :offset LIMIT :limit;"""
)

GET_FILM_BY_ID = """SELECT
title, 
overview as description, 
release_date,  
genres,
time,
is_adult,
imdb_id,
language,
poster_path,
production_companies,
production_countries
FROM "film" WHERE id = :id;"""
