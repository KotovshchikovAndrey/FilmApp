GET_MANY_FILMS = (
    """SELECT id, title, is_adult FROM "film" OFFSET :offset LIMIT :limit;"""
)
