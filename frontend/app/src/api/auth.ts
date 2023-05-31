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

import {axiosInstance} from "./instance";
import {AxiosPromise} from "axios";
import {ILoginRequest, ILoginResponse} from "../core/entities";
import Endpoints from "./endpoints";

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

export const login = (data: ILoginRequest): AxiosPromise<ILoginResponse> => {
    return axiosInstance.post<ILoginResponse>(Endpoints.AUTH.LOGIN, data)
}
export const logout = (): AxiosPromise => {
    return axiosInstance.delete(Endpoints.AUTH.LOGOUT)
}
export const refreshToken = (): AxiosPromise<ILoginResponse> => {
    return axiosInstance.put(Endpoints.AUTH.REFRESH_TOKEN)
}