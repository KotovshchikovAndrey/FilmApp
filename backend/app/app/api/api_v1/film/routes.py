from starlette.routing import Route
from app.api.api_v1.film import controllers


routes = [
    Route("/", controllers.Film),
    Route("/{film_pk:int}", controllers.FilmDetail),
    Route("/filters", controllers.FilmFilter),
    Route("/search", controllers.FilmSearch),
]
