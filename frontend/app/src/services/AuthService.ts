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
// // class AuthService implements IAuthService {}

import {axiosInstance, axiosRefreshInstance} from "../http";
import axios, {AxiosResponse} from "axios";
import {AuthResponse, ILogin, IRegistration} from "../core/entities";

export default class AuthService {

    static async register(data: IRegistration): Promise<AxiosResponse<AuthResponse>> {
        return axiosInstance.post<AuthResponse>('/auth/register', {...data})

    }

    static async login(data: ILogin): Promise<AxiosResponse<AuthResponse>> {
        return await axiosInstance.post<AuthResponse>('/auth/login', {...data})
    }

    static async logOut(): Promise<AxiosResponse> {
        return axiosInstance.delete('/auth/logout')
    }

    static async checkAuth(): Promise<AxiosResponse<AuthResponse>> {
        return axiosRefreshInstance.put('/auth/refresh-token')
    }

}
