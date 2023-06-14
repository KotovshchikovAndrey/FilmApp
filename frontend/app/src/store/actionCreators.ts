import { AxiosError } from "axios"
import api from "../api"
import { IChildComment, IComment, IFilm, ILoginRequest, IRegisterRequest } from "../core/entities"
import { authActions } from "./authReducer"
import { Dispatch } from "@reduxjs/toolkit"
import { IGetFilmsParams } from "../api/films"
import { filmActions } from "./filmReducer"
import { API_URL } from "../core/config"
import Endpoints from "../api/endpoints"
import Cookies from "js-cookie"
import { useNavigate } from "react-router-dom"
import { OrderByFavoriteFilm } from "../api/queryEnums"

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
      const userStatus = Cookies.get("status")

      dispatch(authActions.setIsAuth(true))
      dispatch(authActions.setUser(user))
      dispatch(authActions.setStatus(userStatus ?? null))
    } catch (err) {
      dispatch(authActions.setIsAuth(false))
      dispatch(authActions.setUser(null))
    }
  }
}

export const verifyUser = (code: string) => {
  return async (dispatch: Dispatch) => {
    dispatch(authActions.setLoading(true))

    try {
      await api.auth.redeemCode(code)

      const userStatus = Cookies.get("status")
      dispatch(authActions.setStatus(userStatus ?? null))
    } catch (err) {
      if (err instanceof AxiosError) {
        const errorResponse = err.response
        if (errorResponse) dispatch(authActions.setErrorMessage(errorResponse.data.message))
        else dispatch(authActions.setErrorMessage("Internal error! Try again later"))
      }
    } finally {
      dispatch(authActions.setLoading(false))
    }
  }
}

export const logoutUser = () => {
  return async (dispatch: Dispatch) => {
    await api.auth.logout()
    localStorage.removeItem("token")

    dispatch(authActions.setIsAuth(false))
    dispatch(authActions.setStatus(null))
    dispatch(authActions.setUser(null))
  }
}

export const fetchFilms = (data: IGetFilmsParams) => {
  return async (dispatch: Dispatch) => {
    if (data.filter) dispatch(filmActions.setFilter(data.filter))

    try {
      dispatch(filmActions.setIsLoading(true))
      const response = await api.films.getFilms(data)
      const filmsWithPosters = setPosters(response.data.films)
      dispatch(filmActions.setFilms(filmsWithPosters))
    } catch (e: any) {
      if (e.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        dispatch(filmActions.setErrorMessage(e.response.data))
      } else {
        // Something happened in setting up the request that triggered an Error
        dispatch(filmActions.setErrorMessage("Unexpected error"))
        console.log("Unexpected error: ", e.message)
      }
    } finally {
      dispatch(filmActions.setIsLoading(false))
    }
  }
}

const setPosters = (films: IFilm[]) => {
  films.map((film) => {
    film.posterUrl = `${API_URL}${Endpoints.FILMS.GET_POSTER(film.id)}`
  })
  return films
}

export const fetchUserFavoriteFilms = () => {
  return async (dispatch: Dispatch) => {
    dispatch(filmActions.setIsLoading(true))

    try {
      const response = await api.users.getMyFavoriteFilms(OrderByFavoriteFilm.date)
      const films = setPosters(response.data.films)

      dispatch(filmActions.setFavoriteFilms(films))
    } catch (err) {
      dispatch(filmActions.setErrorMessage("Failed to download favorite films"))
    } finally {
      dispatch(filmActions.setIsLoading(false))
    }
  }
}

export const addFilmToFavorite = (filmId: number) => {
  return async (dispatch: Dispatch) => {
    dispatch(authActions.setLoading(true))
    await api.users.addToFavorite(filmId)
    dispatch(authActions.setLoading(false))
  }
}

export const removeFilmFromFavorite = (filmId: number) => {
  return async (dispatch: Dispatch) => {
    dispatch(authActions.setLoading(true))
    await api.users.removeFromFavorite(filmId)
    dispatch(authActions.setLoading(false))
  }
}

export const setUserAvatar = (data: FormData) => {
  return async (dispatch: Dispatch) => {
    dispatch(authActions.setLoading(true))

    const response = await api.users.setUserAvatar(data)
    const avatar = response.data

    dispatch(authActions.setUserAvatar(avatar))
    dispatch(authActions.setLoading(false))
  }
}

export const getFilmComments = (filmId: number) => {
  return async (dispatch: Dispatch) => {
    dispatch(filmActions.setIsLoading(true))

    const response = await api.films.getFilmComments(filmId)
    const comments = response.data.comments

    dispatch(filmActions.setComments(comments))
    dispatch(filmActions.setIsLoading(false))
  }
}

export const addFilmComment = (
  filmId: number,
  comment: Omit<IComment, "comment_id" | "child_comments">
) => {
  return async (dispatch: Dispatch) => {
    dispatch(filmActions.setIsLoading(true))
    const accessToken = localStorage.getItem("token") as string

    try {
      const response = await api.films.addFilmComment(filmId, comment.text, accessToken)
      const addedCommentId = response.data
      const newComment: IComment = {
        comment_id: addedCommentId,
        child_comments: [],
        ...comment,
      }

      dispatch(filmActions.addComment(newComment))
    } catch (err) {
    } finally {
      dispatch(filmActions.setIsLoading(false))
    }
  }
}

export const addChildFilmComment = (
  filmId: number,
  comment: Omit<IChildComment, "comment_id">,
  parentCommentId: number
) => {
  return async (dispatch: Dispatch) => {
    dispatch(filmActions.setIsLoading(true))
    const accessToken = localStorage.getItem("token") as string

    try {
      const response = await api.films.addFilmComment(
        filmId,
        comment.text,
        accessToken,
        parentCommentId
      )

      const addedCommentId = response.data
      const newChildComment = {
        comment_id: addedCommentId,
        parentCommentId,
        ...comment,
      }

      dispatch(filmActions.addChildComment(newChildComment))
    } catch (err) {
    } finally {
      dispatch(filmActions.setIsLoading(false))
    }
  }
}

export const searchFilm = (title: string, useSmartSearch: boolean) => {
  return async (dispatch: Dispatch) => {
    dispatch(filmActions.clearFilters())
    dispatch(filmActions.setIsLoading(true))

    const response = useSmartSearch
      ? await api.films.searchFilmSmart(title)
      : await api.films.searchFilm(title)

    const filmsWithPosters = setPosters(response.data.films)
    dispatch(filmActions.setFilms(filmsWithPosters))
    dispatch(filmActions.setIsLoading(false))
  }
}
