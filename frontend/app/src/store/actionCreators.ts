import {ILoginRequest, IRegisterRequest} from "../core/entities";
import {Dispatch} from "@reduxjs/toolkit";
import {
    loadProfileFailure,
    loadProfileStart, loadProfileSuccess,
    authFailure,
    authStart,
    authSuccess,
    logoutSuccess,
} from "./authReducer";
import api from "../api";
import {redirect} from "react-router-dom";
import {store} from "./index";

export const loginUser = (data: ILoginRequest) =>
    async (dispatch: Dispatch<any>): Promise<void> => {
        try {
            dispatch(authStart())
            const response = await api.auth.login(data)
            dispatch(getMyProfile())
            localStorage.setItem('token', response.data.access_token)
            dispatch(authSuccess(response.data.access_token))
        } catch (e: any) {
            console.error(e.message)
            dispatch(authFailure(e.response.data.message))
        }
    }
export const logoutUser = () =>
    async (dispatch: Dispatch): Promise<void> => {
        try {
            await api.auth.logout()
            localStorage.removeItem('token')
            dispatch(logoutSuccess())
            redirect("/")
        } catch (e: any) {
            console.error(e.message)
        }
    }
export const getMyProfile = () =>
    async (dispatch: Dispatch<any>): Promise<void> => {
        try {
            dispatch(loadProfileStart())
            const response = await api.users.getMyProfile()
            dispatch(loadProfileSuccess(response.data))
        } catch (e: any) {
            console.error(e.message)
            dispatch(loadProfileFailure(e.message))
        }
    }
// export const getAccessToken = () =>
//     async (dispatch: Dispatch): Promise<string | null> => {
//         try {
//             const accessToken = store.getState().auth.authData.accessToken
//             return accessToken
//         } catch (e: any) {
//             console.error(e.message)
//             return null
//         }
//     }
export const refreshToken = () =>
    async (dispatch: Dispatch<any>): Promise<void> => {
        try {
            dispatch(authStart())
            const response = await api.auth.refreshToken()
            localStorage.setItem('token', response.data.access_token)
            dispatch(getMyProfile())
            dispatch(authSuccess(response.data.access_token))
        } catch (e: any) {
            console.error(e.message)
            dispatch(authFailure(e.message))
        }
    }
export const registerUser = (data: IRegisterRequest) =>
    async (dispatch: Dispatch<any>): Promise<void> => {
        try {
            dispatch(authStart())
            const response = await api.auth.register(data)
            localStorage.setItem('token', response.data.access_token)
            dispatch(getMyProfile())
            dispatch(authSuccess(response.data.access_token))
        } catch (e: any) {
            console.log(e.message)
            dispatch(authFailure(e.response.data.message))
        }
    }