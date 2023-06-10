import { AxiosPromise } from "axios/index"
import { axiosInstance } from "./instance"
import Endpoints from "./endpoints"
import { IUser, IFilm } from "../core/entities"
import { OrderByFavoriteFilm } from "./queryEnums"

interface IFilmsResponse {
  films: IFilm[]
}

export const getMyProfile = (): AxiosPromise<IUser> => {
  return axiosInstance.get(Endpoints.USERS.MY_PROFILE)
}

export const getMyFavoriteFilms = (orderBy?: OrderByFavoriteFilm): AxiosPromise<IFilmsResponse> => {
  return axiosInstance.get(Endpoints.USERS.MY_FAVORITE, { params: { order_by: orderBy } })
}

export const addToFavorite = (filmId: number): AxiosPromise<void> => {
  return axiosInstance.post(Endpoints.USERS.MY_FAVORITE, { film_id: filmId })
}

export const removeFromFavorite = (filmId: number): AxiosPromise<void> => {
  return axiosInstance.delete(Endpoints.USERS.MY_FAVORITE, { data: { film_id: filmId } })
}

export const setUserAvatar = (data: FormData): AxiosPromise<string> => {
  return axiosInstance.put(Endpoints.USERS.PROFILE_AVATAR, data, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  })
}
