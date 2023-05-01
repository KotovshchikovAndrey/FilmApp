from app.api.api_v1.film import controllers
from starlette.routing import Route

routes = [
    Route("/", controllers.Film),
]
