import uvicorn
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Mount

from app.api.api_v1 import auth_routes, film_routes, user_routes
from app.api.middlewares.auth_backend import JwtAuthBackend
from app.core import config
from app.core.server import StarletteServer

routes = [
    Mount("/auth", routes=auth_routes),
    Mount("/users", routes=user_routes),
    Mount("/films", routes=film_routes),
]

middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=config.ALLOW_ORIGINS,
        allow_methods=["*"],
        allow_credentials=True,
        allow_headers=["*"],
    ),
    Middleware(
        AuthenticationMiddleware,
        backend=JwtAuthBackend(),
    ),
]

server = StarletteServer(routes=routes, middlewares=middlewares)
app = server.get_app_instance()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
