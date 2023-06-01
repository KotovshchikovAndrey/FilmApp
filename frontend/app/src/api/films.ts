import {IAuthResponse, IFilm, ILoginRequest, ITrailer} from "../core/entities";
import {AxiosPromise} from "axios";
import {axiosInstance} from "./instance";
import Endpoints from "./endpoints";

export interface IGetFilmsParams {
    limit: number;
    random: boolean;
    offset?: number;
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
                    county: data.country,
                    random: data.random,
                }
        })
}
export const getFilmDetail = (filmId: number): AxiosPromise<IFilm> => {
    return axiosInstance.get<IFilm>(Endpoints.FILMS.GET_FILM_DETAIL(filmId))

}
export const getFilmTrailer = (filmId: number): AxiosPromise<ITrailer> => {
    return axiosInstance.get<ITrailer>(Endpoints.FILMS.GET_FILM_TRAILER(filmId))

}
