import typing as tp
import punq

from film.crud import reporitories as film_repositories
from user.crud import reporitories as user_repositories
from film import services as film_services
from user import services as user_services

container = punq.Container()


# Repositories
container.register(
    film_repositories.IFilmReporitory,
    film_repositories.FilmPostgresRepository,
    scope=punq.Scope.singleton,
)

container.register(
    user_repositories.IUserRepository,
    user_repositories.UserPostgresRepository,
    scope=punq.Scope.singleton,
)


# Services
container.register(
    film_services.IFilmService,
    film_services.FilmService,
    scope=punq.Scope.singleton,
)

container.register(
    user_services.IUserService,
    user_services.UserService,
    scope=punq.Scope.singleton,
)

container.register(
    user_services.IAuthService,
    user_services.JwtAuthService,
    scope=punq.Scope.singleton
)

container.register(
    user_services.ITokenService,
    user_services.TokenService,
    scope=punq.Scope.singleton
)