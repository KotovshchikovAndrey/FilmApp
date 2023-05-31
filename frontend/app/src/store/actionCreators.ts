import {ILoginRequest} from "../core/entities";
import {Dispatch} from "@reduxjs/toolkit";
import {
    loadProfileFailure,
    loadProfileStart, loadProfileSuccess,
    loginFailure,
    loginStart,
    loginSuccess,
    logoutSuccess,
} from "./authReducer";
import api from "../api";
import {redirect} from "react-router-dom";
import {store} from "./index";

export const loginUser = (data: ILoginRequest) =>
    async (dispatch: Dispatch<any>): Promise<void> => {
        try {
            dispatch(loginStart())
            const response = await api.auth.login(data)
            dispatch(loginSuccess(response.data.access_token))
            dispatch(getMyProfile())
        } catch (e: any) {
            console.error(e.message)
            dispatch(loginFailure(e.response.data.message))
        }
    }
export const logoutUser = () =>
    async (dispatch: Dispatch): Promise<void> => {
        try {
            await api.auth.logout()
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
export const getAccessToken = () =>
    async (dispatch: Dispatch): Promise<string | null> => {
        try {
            const accessToken = store.getState().auth.authData.accessToken
            return accessToken
        } catch (e: any) {
            console.error(e.message)
            return null
        }
    }
export const refreshToken = () =>
    async (dispatch: Dispatch): Promise<void> => {
        try {
            const response = await api.auth.refreshToken()
            dispatch(loginSuccess(response.data.access_token))
        } catch (e: any) {
            console.error(e.message)
        }
    }