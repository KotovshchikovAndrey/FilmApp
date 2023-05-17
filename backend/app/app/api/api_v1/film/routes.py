from starlette.routing import Route
from app.api.api_v1.film import controllers


routes = [
    # Route("/test", controllers.Test),
    Route("/", controllers.Film),
    Route("/{film_id:int}", controllers.FilmDetail),
    Route("/{film_id:int}/poster", controllers.Poster),
    Route("/filters", controllers.FilmFilter),
    Route("/search", controllers.FilmSearch),
]
