import typing as tp
import punq

from film.crud import reporitories as film_repositories
from film import services as film_services

container = punq.Container()


# Repositories
container.register(
    film_repositories.IFilmReporitory,
    film_repositories.FilmPostgresRepository,
    scope=punq.Scope.singleton,
)


# Services
container.register(
    film_services.IFilmService,
    film_services.FilmService,
    scope=punq.Scope.singleton,
)
