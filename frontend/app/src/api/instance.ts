import axios from "axios"
import { API_URL } from "../core/config"
import Endpoints from "./endpoints"
import { store } from "../store"
import { refreshToken } from "../store/actionCreators"

import jwt_decode from "jwt-decode"

export const axiosInstance = axios.create({
  withCredentials: true,
  baseURL: API_URL,
})

const urlsAuth = [
  Endpoints.AUTH.LOGOUT,
  Endpoints.USERS.MY_PROFILE,
  Endpoints.AUTH.REDEEM_CODE,
  Endpoints.USERS.MY_FAVORITE,
]

interface ITokenPayload {
  id: number
  exp: number
}

axiosInstance.interceptors.request.use(async (request) => {
  if (request.url && urlsAuth.includes(request.url)) {
    let accessToken = localStorage.getItem("token")
    if (accessToken) {
      const payload: ITokenPayload = jwt_decode(accessToken)

      const expiration = new Date(payload.exp * 1000)
      const nowDate = new Date()

      const isTokenExpire = expiration.getTime() - nowDate.getTime() < 0
      if (!isTokenExpire) {
        request.headers.Authorization = `${accessToken}`
        return request
      }
    }

    await store.dispatch(refreshToken())
    accessToken = localStorage.getItem("token")
    request.headers.Authorization = `${accessToken}`

    return request
  }

  return request
})

axiosInstance.interceptors.request.use((config) => {
  if (config.url === Endpoints.AUTH.REFRESH_TOKEN) {
    const accessToken = localStorage.getItem("token")
    config.headers["old_access"] = accessToken
  }
  return config
})
