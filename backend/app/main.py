import uvicorn
from starlette.routing import Mount

from app.api.api_v1 import auth_routes, user_routes, film_routes
from app.core.server import StarletteServer

middlewares = []

routes = [
    Mount("/auth", routes=auth_routes),
    Mount("/user", routes=user_routes),
    Mount("/film", routes=film_routes),
]


server = StarletteServer(routes=routes, middlewares=middlewares)
app = server.get_app_instance()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
