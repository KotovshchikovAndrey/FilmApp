import { AxiosPromise } from "axios/index"
import { axiosInstance } from "./instance"
import Endpoints from "./endpoints"
import { IUser, IFilm } from "../core/entities"

interface IFilmsResponse {
  films: IFilm[]
}

export const getMyProfile = (): AxiosPromise<IUser> => {
  return axiosInstance.get(Endpoints.USERS.MY_PROFILE)
}

export const getMyFavoriteFilms = (): AxiosPromise<IFilmsResponse> => {
  return axiosInstance.get(Endpoints.USERS.MY_FAVORITE)
}

export const addToFavorite = (filmId: number): AxiosPromise<void> => {
  return axiosInstance.post(Endpoints.USERS.MY_FAVORITE, { film_id: filmId })
}
