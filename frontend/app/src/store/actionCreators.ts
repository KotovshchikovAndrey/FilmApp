import { AxiosError } from "axios"
import api from "../api"
import { ILoginRequest, IRegisterRequest } from "../core/entities"
import { authActions } from "./authReducer"
import { Dispatch } from "@reduxjs/toolkit"

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
