import {ILogin, IRegistration, IUser} from "../core/entities";
import {makeAutoObservable} from "mobx";
import AuthService from "../services/AuthService";
import axios, {AxiosError} from 'axios';

export default class Store {
    isAuth = false

    errors = {
        registerError: '',
        loginError: '',
        verificationError: '',
    }

    constructor() {
        makeAutoObservable(this)
    }

    setAuth(bool: boolean) {
        this.isAuth = bool
    }

    async register(data: IRegistration) {
        try {
            const response = await AuthService.register(data)
            console.log(response)
            localStorage.setItem('access_token', response.data.access_token)
            this.setAuth(true)
            this.errors.registerError = ""
        } catch (err: any | AxiosError) {
            if (axios.isAxiosError(err))  {
                const errMsg = err.response?.data.message
                console.log(errMsg)
                this.errors.registerError = errMsg
            } else {
                console.log(`not an axios error: ${err}` )
            }
        }
    }

    async login(data: ILogin) {
        try {
            const response = await AuthService.login(data)
            console.log(response.data)
            localStorage.setItem('token', response.data.access_token)
            this.setAuth(true)
            this.errors.registerError = ""
        } catch (err: any | AxiosError) {
            if (axios.isAxiosError(err))  {
                const errMsg = err.response?.data.message
                console.log(errMsg)
                this.errors.loginError = errMsg
            } else {
                console.log(`not an axios error: ${err}` )
            }
        }
    }

    async logOut() {
        try {
            const response = await AuthService.logOut()
            console.log(response)
            localStorage.removeItem('token')
            this.setAuth(false)
        } catch (err) {
            console.log(err)
        }
    }

    async checkAuth() {
        try {
            const response = await AuthService.checkAuth()
        } catch (e) {
            console.log(e)
        }
    }
}