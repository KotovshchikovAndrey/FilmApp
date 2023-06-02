import typing as tp

import punq

from film import services as film_services
from film.crud import reporitories as film_repositories
from user import services as user_services
from user.crud import reporitories as user_repositories

container = punq.Container()


# Repositories
container.register(
    film_repositories.ICommentRepository,
    film_repositories.CommentPostgresRepository,
    scope=punq.Scope.singleton,
)

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
    film_services.ICommentService,
    film_services.CommentService,
    scope=punq.Scope.singleton,
)

container.register(
    film_services.IFilmService,
    film_services.FilmService,
    scope=punq.Scope.singleton,
)

container.register(
    user_services.ITokenService,
    user_services.TokenService,
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
    scope=punq.Scope.singleton,
)
