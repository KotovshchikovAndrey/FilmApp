from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from app.api.api_v1.film import controllers
from app.core import config

routes = [
    Route("/", controllers.Film),
    Route("/{film_id:int}", controllers.FilmDetail),
    Route("/{film_id:int}/poster", controllers.Poster),
    Route("/{film_id:int}/trailer", controllers.Trailer),
    Route("/{film_id:int}/rating", controllers.FilmRating),
    Route("/{film_id:int}/comments", controllers.FilmComment),
    Route("/{film_id:int}/comments/{comment_id:int}", controllers.FilmCommentDetail),
    Route("/filters", controllers.FilmFilter),
    Route("/search", controllers.FilmSearch),
    Route("/gigasearch", controllers.FilmGigaSearch),
    Mount(
        "/media",
        app=StaticFiles(directory=config.UPLOAD_DIR + "/posters"),
        name="static",
    ),
]
