import {configureStore} from "@reduxjs/toolkit";
import {TypedUseSelectorHook, useDispatch, useSelector} from "react-redux";
import authReducer from "./authReducer";
import filmReducer from "./filmReducer";

export const store = configureStore({
    reducer: {
        auth: authReducer,
        film: filmReducer,
    },
})

export type IRootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
export const useAppDispatch: () => AppDispatch = useDispatch
export const useAppSelector: TypedUseSelectorHook<IRootState> = useSelector