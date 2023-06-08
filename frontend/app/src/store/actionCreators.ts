import {AxiosError} from "axios"
import api from "../api"
import {IFilm, ILoginRequest, IRegisterRequest} from "../core/entities"
import {authActions} from "./authReducer"
import {Dispatch} from "@reduxjs/toolkit"
import {IGetFilmsParams} from "../api/films";
import {filmActions} from "./filmReducer";
import {API_URL} from "../core/config";
import Endpoints from "../api/endpoints";

export const registerUser = (data: IRegisterRequest) => {
  return async (dispatch: Dispatch) => {
    dispatch(authActions.setLoading(true))

    try {
      const response = await api.auth.register(data)
      const accessToken = response.data.access_token
      localStorage.setItem("token", accessToken)

      dispatch(authActions.setIsAuth(true))
      dispatch(authActions.setLoading(false))
    } catch (err) {
      if (err instanceof AxiosError) {
        const errorResponse = err.response
        if (errorResponse) {
          dispatch(authActions.setErrorMessage(errorResponse.data.message))
          dispatch(authActions.setLoading(false))

          return
        }

        dispatch(authActions.setErrorMessage("Internal error! Try again later"))
        dispatch(authActions.setLoading(false))
      }
    }
  }
}

export const loginUser = (data: ILoginRequest) => {
  return async (dispatch: Dispatch) => {
    dispatch(authActions.setLoading(true))

    try {
      const response = await api.auth.login(data)
      const accessToken = response.data.access_token
      localStorage.setItem("token", accessToken)

      dispatch(authActions.setIsAuth(true))
      dispatch(authActions.setLoading(false))
    } catch (err) {
      if (err instanceof AxiosError) {
        const errorResponse = err.response
        if (errorResponse) {
          dispatch(authActions.setErrorMessage(errorResponse.data.message))
          dispatch(authActions.setLoading(false))

          return
        }

        dispatch(authActions.setErrorMessage("Internal error! Try again later"))
        dispatch(authActions.setLoading(false))
      }
    }
  }
}

export const refreshToken = () => {
  return async (dispatch: Dispatch) => {
    try {
      const response = await api.auth.refreshToken()
      const accessToken = response.data.access_token
      localStorage.setItem("token", accessToken)
    } catch (err) {
      dispatch(authActions.setIsAuth(false))
    }
  }
}

export const authenticateUser = () => {
  return async (dispatch: Dispatch) => {
    try {
      const response = await api.users.getMyProfile()
      const user = response.data

      dispatch(authActions.setIsAuth(true))
      dispatch(authActions.setUser(user))
    } catch (err) {
      dispatch(authActions.setIsAuth(false))
      dispatch(authActions.setUser(null))
    }
  }
}

export const logoutUser = () => {
  return async (dispatch: Dispatch) => {
    await api.auth.logout()
    localStorage.removeItem("token")

    dispatch(authActions.setIsAuth(false))
    dispatch(authActions.setUser(null))
  }
}

export const fetchFilms = (data: IGetFilmsParams) => {
  return async (dispatch: Dispatch) => {
    try {
      dispatch(filmActions.setIsLoading(true))
      const response = await api.films.getFilms(data)
      const filmsWithPosters = setPosters(response.data.films)
      dispatch(filmActions.setFilms(filmsWithPosters))
    } catch (e: any) {
      if (e.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        dispatch(filmActions.setErrorMessage(e.response.data));
      } else {
        // Something happened in setting up the request that triggered an Error
        dispatch(filmActions.setErrorMessage("Unexpected error"));
        console.log('Unexpected error: ', e.message);
      }
    } finally {
      dispatch(filmActions.setIsLoading(false))
    }
  }
}
const setPosters = (films: IFilm[]) => {
  films.map(film => {
    film.posterUrl = `${API_URL}${Endpoints.FILMS.GET_POSTER(film.id)}`
  })
  return films
}

