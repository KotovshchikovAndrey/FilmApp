import {AxiosPromise} from "axios/index";
import {axiosInstance} from "./instance";
import Endpoints from "./endpoints";
import {IUser} from "../core/entities";

export const getMyProfile = (): AxiosPromise<IUser> => {
    return axiosInstance.get(Endpoints.USERS.MY_PROFILE)
}