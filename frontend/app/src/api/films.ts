import {IAuthResponse, IFilm, ILoginRequest} from "../core/entities";
import {AxiosPromise} from "axios";
import {axiosInstance} from "./instance";
import Endpoints from "./endpoints";

export interface IGetFilmsParams {
    limit: number;
    offset: number;
    genre?: string;
    country?: string;
}

interface IFilmsResponse {
    films: IFilm[],
}

export const getFilms = (data: IGetFilmsParams): AxiosPromise<IFilmsResponse> => {
    return axiosInstance.get<IFilmsResponse>(Endpoints.FILMS.GET_FILMS,
        {
            params:
                {
                    limit: data.limit,
                    offset: data.offset,
                    genre: data.genre,
                    county: data.country
                }
        })
}