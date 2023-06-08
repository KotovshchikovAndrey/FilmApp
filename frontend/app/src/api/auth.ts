// import ky from "ky"
// import { IUser } from "../core/entities"
//
// interface IAuthService {
//   register: () => IUser
//   login: () => IUser
//   logout: () => void
//   resetPassword: () => void
// }
//
// // class Auth implements IAuthService {}

import { axiosInstance } from "./instance"
import { AxiosPromise } from "axios"
import { IAuthResponse, ILoginRequest, IRegisterRequest } from "../core/entities"
import Endpoints from "./endpoints"

// export default class Auth {

// static async register(data: IRegistration): Promise<AxiosResponse<AuthResponse>> {
//     return axiosInstance.post<AuthResponse>('/auth/register', {...data})
//
// }

// static login(data: ILoginRequest): AxiosPromise<ILoginResponse> {
//     return axiosInstance.post<ILoginResponse>('/auth/login', {...data})
// }

// static async logOut(): Promise<AxiosResponse> {
//     return axiosInstance.delete('/auth/logout')
// }
//
// static async checkAuth(): Promise<AxiosResponse<AuthResponse>> {
//     return axiosRefreshInstance.put('/auth/refresh-token')
// }

// }

export const login = (data: ILoginRequest): AxiosPromise<IAuthResponse> => {
  return axiosInstance.post<IAuthResponse>(Endpoints.AUTH.LOGIN, data)
}
export const logout = (): AxiosPromise => {
  return axiosInstance.delete(Endpoints.AUTH.LOGOUT)
}
export const refreshToken = (): AxiosPromise<IAuthResponse> => {
  return axiosInstance.put(Endpoints.AUTH.REFRESH_TOKEN)
}

export const register = (data: IRegisterRequest): AxiosPromise<IAuthResponse> => {
  return axiosInstance.post<IAuthResponse>(Endpoints.AUTH.REGISTER, data)
}

export const redeemCode = (code: string): AxiosPromise<void> => {
  return axiosInstance.put(Endpoints.AUTH.REDEEM_CODE, { code })
}

export const requestCode = (): AxiosPromise<void> => {
  return axiosInstance.post(Endpoints.AUTH.REQUEST_CODE)
}
