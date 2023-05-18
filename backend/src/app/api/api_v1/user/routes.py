from starlette.routing import Route
from app.api.api_v1.user import controllers

routes = [
    Route("/{user_pk}/profile", controllers.Profile),
    Route("/{user_pk}/favoriteFilms", controllers.UserFavorite),
]
