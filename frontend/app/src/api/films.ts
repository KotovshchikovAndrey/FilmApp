import {
  IAuthResponse,
  IComment,
  IFilm,
  IFilmFilterOptions,
  ILoginRequest,
  ITrailer,
} from "../core/entities"
import { AxiosPromise } from "axios"
import { axiosInstance } from "./instance"
import Endpoints from "./endpoints"

export interface IGetFilmsParams {
  limit: number
  offset?: number
  genreId?: number | null
  countryIso?: string | null
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
      genre: data.genreId,
      country: data.countryIso,
    },
  })
}

export const getFilmDetail = (filmId: number, accessToken?: string): AxiosPromise<IFilm> => {
  return axiosInstance.get<IFilm>(Endpoints.FILMS.GET_FILM_DETAIL(filmId), {
    headers: { Authorization: accessToken },
  })
}

export const getFilmTrailer = (filmId: number): AxiosPromise<ITrailer> => {
  return axiosInstance.get<ITrailer>(Endpoints.FILMS.GET_FILM_TRAILER(filmId))
}

export const getFilmFilterOptions = (): AxiosPromise<IFilmFilterOptions> => {
  return axiosInstance.get<IFilmFilterOptions>(Endpoints.FILMS.GET_FILM_FILTER_OPTIONS)
}

export const searchFilm = (title: string, limit: number = 20): AxiosPromise<{ films: IFilm[] }> => {
  return axiosInstance.get(Endpoints.FILMS.SEARCH_FILM, {
    params: {
      title,
      limit,
    },
  })
}

export const searchFilmSmart = (
  title: string,
  limit: number = 20
): AxiosPromise<{ films: IFilm[] }> => {
  return axiosInstance.post(Endpoints.FILMS.SEARCH_FILM_SMART, { title, limit })
}

export const getFilmComments = (filmId: number): AxiosPromise<{ comments: IComment[] }> => {
  return axiosInstance.get(Endpoints.FILMS.FILM_COMMENTS(filmId))
}

export const addFilmComment = (
  filmId: number,
  text: string,
  accessToken: string,
  parentComment?: number
): AxiosPromise<number> => {
  return axiosInstance.post(
    Endpoints.FILMS.FILM_COMMENTS(filmId),
    { text, parent_comment: parentComment },
    {
      headers: {
        Authorization: accessToken,
      },
    }
  )
}
