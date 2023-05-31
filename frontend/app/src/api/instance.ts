import axios, {AxiosError} from 'axios'
import {API_URL} from "../core/config";
import Endpoints from "./endpoints";
import {store, useAppSelector} from "../store";
import {getAccessToken, logoutUser, refreshToken} from "../store/actionCreators";
import api from "./index";

export const axiosInstance = axios.create({
    withCredentials: true,
    baseURL: API_URL,
})

const urlsSkipAuth = [Endpoints.AUTH.LOGIN, Endpoints.AUTH.REGISTER, Endpoints.AUTH.REFRESH_TOKEN]

axiosInstance.interceptors.request.use(async (config) => {
    if (config.url && urlsSkipAuth.includes(config.url)) {
        return config
    }

    const accessToken = await store.dispatch(getAccessToken())
    if (accessToken) {
        config.headers.Authorization = `${accessToken}`
    }
    return config

})
axiosInstance.interceptors.response.use(
    (config) => config,
    async (error) => {
        const originalRequest = error.config
        if (error.response?.status == 401 && error.config && !originalRequest.isRetry) {
            originalRequest.isRetry = true
            try {
                await store.dispatch(refreshToken())
                return axiosInstance.request(originalRequest)
            } catch (e) {
                console.log('не авторизован')
            }

        }
        throw error
    })

// axiosInstance.interceptors.response.use(
//     (response) => response,
//     (error: AxiosError) => {
//         console.log('trying to refresh...')
//         // const isLoggedIn = !!store.getState().auth.authData.accessToken
//         //
//         // if ((error.response?.status === 401) && isLoggedIn && error.request.url !== Endpoints.AUTH.LOGOUT) {
//         //     store.dispatch(logoutUser())
//         // }
//         //
//         // throw error
//     }
// )

axiosInstance.interceptors.request.use(async (config) => {
    if (config.url === Endpoints.AUTH.REFRESH_TOKEN) {
        console.log('refredhing...')
        const accessToken = await store.dispatch(getAccessToken())
        config.headers['old_access'] = accessToken
    }
    return config
})
//
// axiosInstance.interceptors.response.use(
//     (response) => response,
//     (error: AxiosError) => {
//         const isLoggedIn = !!store.getState().auth.authData.accessToken
//
//         if ((error.response?.status === 401) && isLoggedIn && error.request.url !== Endpoints.AUTH.LOGOUT) {
//             store.dispatch(logoutUser())
//         }
//
//         throw error
//     }
// )
