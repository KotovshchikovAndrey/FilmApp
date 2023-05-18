import uvicorn
from starlette.routing import Mount
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from app.api.api_v1 import auth_routes, user_routes, film_routes
from app.core.server import StarletteServer
from app.api.middlewares.auth_backend import JwtAuthBackend

routes = [
    Mount("/auth", routes=auth_routes),
    Mount("/users", routes=user_routes),
    Mount("/films", routes=film_routes),
]
middlewares = [
    Middleware(
        AuthenticationMiddleware,
        backend=JwtAuthBackend(),
    )
]

server = StarletteServer(routes=routes, middlewares=middlewares)
app = server.get_app_instance()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
