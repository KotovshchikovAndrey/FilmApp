// import {ILogin, IRegistration, IUser} from "../core/entities";
// import {makeAutoObservable} from "mobx";
// import Auth from "../services/Auth";
// import axios, {AxiosError} from 'axios';
//
// export default class Store {
//     isAuth = false
//
//     errors = {
//         registerError: '',
//         loginError: '',
//         verificationError: '',
//     }
//
//     constructor() {
//         makeAutoObservable(this)
//     }
//
//     setAuth(bool: boolean) {
//         this.isAuth = bool
//     }
//
//     async register(data: IRegistration) {
//         try {
//             const response = await Auth.register(data)
//             console.log(response)
//             localStorage.setItem('access_token', response.data.access_token)
//             this.setAuth(true)
//             this.errors.registerError = ""
//         } catch (err: any | AxiosError) {
//             if (axios.isAxiosError(err))  {
//                 const errMsg = err.response?.data.message
//                 console.log(errMsg)
//                 this.errors.registerError = errMsg
//             } else {
//                 console.log(`not an axios error: ${err}` )
//             }
//         }
//     }
//
//     async login(data: ILogin) {
//         try {
//             const response = await Auth.login(data)
//             console.log(response)
//             localStorage.setItem('access_token', response.data.access_token)
//             this.setAuth(true)
//             this.errors.loginError = ""
//         } catch (err: any | AxiosError) {
//             if (axios.isAxiosError(err))  {
//                 const errMsg = err.response?.data.message
//                 console.log(errMsg)
//                 this.errors.loginError = errMsg
//             } else {
//                 console.log(`not an axios error: ${err}` )
//             }
//         }
//     }
//
//     async logOut() {
//         try {
//             const response = await Auth.logOut()
//             console.log(response)
//             localStorage.removeItem('access_token')
//             this.setAuth(false)
//         } catch (e: any) {
//             console.log(e.message)
//         }
//     }
//
//     async checkAuth() {
//         try {
//             const response = await Auth.checkAuth()
//             localStorage.setItem('access_token', response.data.access_token)
//             this.setAuth(true)
//             console.log(response)
//         } catch (e: any) {
//             console.log(e.message)
//         }
//     }
// }