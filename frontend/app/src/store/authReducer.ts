import { createSlice, PayloadAction } from "@reduxjs/toolkit"
import { IUser } from "../core/entities"

export interface AuthState {
  user: IUser | null
  isAuth: boolean
  loading: boolean
  errorMessage: string | null
}

const initialState: AuthState = {
  user: null,
  isAuth: false,
  loading: false,
  errorMessage: null,
}

export const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<IUser | null>) => {
      state.user = action.payload
    },

    setIsAuth: (state, action: PayloadAction<boolean>) => {
      state.isAuth = action.payload
    },

    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload
    },

    setErrorMessage: (state, action: PayloadAction<string | null>) => {
      state.errorMessage = action.payload
    },
  },
})

export default authSlice.reducer
export const authActions = authSlice.actions
