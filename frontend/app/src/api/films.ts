import { IAuthResponse, IFilm, IFilmFilters, ILoginRequest, ITrailer } from "../core/entities"
import { AxiosPromise } from "axios"
import { axiosInstance } from "./instance"
import Endpoints from "./endpoints"

export interface IGetFilmsParams {
  limit: number
  offset?: number
  genre?: string | null
  country?: string | null
}

interface IFilmsResponse {
  films: IFilm[]
}
//TODO значения параметров по умолчанию
export const getFilms = (data: IGetFilmsParams): AxiosPromise<IFilmsResponse> => {
  return axiosInstance.get<IFilmsResponse>(Endpoints.FILMS.GET_FILMS, {
    params: {
      limit: data.limit,
      offset: data.offset,
      genre: data.genre,
      country: data.country,
    },
  })
}

export const getFilmDetail = (filmId: number): AxiosPromise<IFilm> => {
  return axiosInstance.get<IFilm>(Endpoints.FILMS.GET_FILM_DETAIL(filmId))
}

export const getFilmTrailer = (filmId: number): AxiosPromise<ITrailer> => {
  return axiosInstance.get<ITrailer>(Endpoints.FILMS.GET_FILM_TRAILER(filmId))
}

export const getFilmFilters = (): AxiosPromise<IFilmFilters> => {
  return axiosInstance.get<IFilmFilters>(Endpoints.FILMS.GET_FILM_FILTERS)
}

export const searchFilmSmart = (title: string): AxiosPromise<IFilm> => {
  return axiosInstance.post<IFilm>(Endpoints.FILMS.SEARCH_FILM_SMART, { title })
}
