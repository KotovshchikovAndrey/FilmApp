import axios from 'axios'
import {API_URL} from "../core/config";

export const axiosAuthInstance = axios.create({
    withCredentials: false,
    baseURL: API_URL,
})

axiosAuthInstance.interceptors.request.use((config) => {
    config.headers.Authorization = `Bearer ${localStorage.getItem('token')})`
    return config
})

export const axiosInstance = axios.create({
    withCredentials: false,
    baseURL: API_URL,
})

export const axiosRefreshInstance = axios.create({
    withCredentials: false,
    baseURL: API_URL,
})

axiosRefreshInstance.interceptors.request.use((config) => {
    config.headers["old_access"] = `${localStorage.getItem('token')})`
    return config
})
