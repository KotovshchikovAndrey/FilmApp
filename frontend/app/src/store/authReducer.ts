import {createAsyncThunk, createSlice, PayloadAction} from "@reduxjs/toolkit";
import {ILoginRequest, IUser} from "../core/entities";
import {useSelector} from "react-redux";
import {IRootState, useAppSelector} from "./index";
import api from "../api";
import exp from "constants";

export interface AuthState {
    authData: {
        accessToken: string | null;
        status: 'idle' | 'loading' | 'succeeded' | 'failed';
        error: string | null;
    }
    profileData: {
        profile: IUser | null,
        status: 'idle' | 'loading' | 'succeeded' | 'failed';
        error: string | null,
    }
}

const initialState: AuthState = {
    authData: {
        accessToken: null,
        status: 'idle',
        error: null,
    },
    profileData: {
        profile: null,
        status: 'idle',
        error: null,
    }
}

// export const fetchLogin = createAsyncThunk(
//     'auth/fetchLogin',
//     async (data: ILoginRequest) => {
//         const response = await api.auth.login(data)
//         return response.data
//     }
// )

export const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers: {
        // loginStart: (state): AuthState => ({
        //     ...state,
        //     authData: {
        //         ...state.authData,
        //         isLoading: true,
        //     }
        // }),
        loginStart: (state) => {
            state.authData.status = 'loading'
        },
        // loginSuccess: (state, action: PayloadAction<string>): AuthState => ({
        //     ...state,
        //     authData: {
        //         ...state.authData,
        //         accessToken: action.payload,
        //         isLoading: false,
        //         error: null,
        //     },
        // }),
        loginSuccess: (state, action: PayloadAction<string>) => {
            state.authData.status = 'succeeded'
            state.authData.accessToken = action.payload
            state.authData.error = null
        },
        // loginFailure: (state, action: PayloadAction<string>): AuthState => ({
        //     ...state,
        //     authData: {
        //         ...state.authData,
        //         isLoading: false,
        //         error: action.payload,
        //     }
        // }),
        loginFailure: (state, action: PayloadAction<string>) => {
            state.authData.status = 'failed'
            state.authData.error = action.payload
        },

        logoutSuccess: () => initialState,

        // loadProfileStart: (state): AuthState => ({
        //     ...state,
        //     profileData: {
        //         ...state.profileData,
        //         isLoading: true,
        //     }
        // }),
        loadProfileStart: (state) => {
            state.profileData.status = 'loading'
        },
        // loadProfileSuccess: (state, action: PayloadAction<IUser>): AuthState => ({
        //     ...state,
        //     profileData: {
        //         ...state.profileData,
        //         profile: action.payload,
        //         isLoading: false,
        //         error: null,
        //     }
        // }),
        loadProfileSuccess: (state, action: PayloadAction<IUser>) => {
            state.profileData.status = 'succeeded'
            state.profileData.profile = action.payload
            state.profileData.error = null
        },
        // loadProfileFailure: (state, action: PayloadAction<string>): AuthState => ({
        //     ...state,
        //     profileData: {
        //         ...state.profileData,
        //         isLoading: false,
        //         error: action.payload,
        //     }
        // }),
        loadProfileFailure: (state, action: PayloadAction<string>) => {
            state.profileData.status = 'failed'
            state.profileData.error = action.payload
        },
    },
    // extraReducers(builder) {
    //     builder
    //         .addCase(fetchLogin.pending, (state, action) => {
    //             state.authData.status = 'loading'
    //         })
    //         .addCase(fetchLogin.fulfilled, (state, action) => {
    //             state.authData.status = 'succeeded'
    //             state.authData.accessToken = action.payload.access_token
    //         })
    //         .addCase(fetchLogin.rejected, (state, action) => {
    //             state.authData.status = 'failed'
    //             state.authData.error = action.error.message
    //         })
    // }
})

export const {
    loginStart,
    loginSuccess,
    loginFailure,
    logoutSuccess,
    loadProfileStart,
    loadProfileSuccess,
    loadProfileFailure,
} = authSlice.actions

export const selectIsLoggedIn = (state: IRootState) => !!state.auth.authData.accessToken

export default authSlice.reducer