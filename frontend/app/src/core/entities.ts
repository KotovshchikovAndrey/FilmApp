export interface IGenre {
    id: number
    name: string
}

export interface IFilm {
    id: number
    title: string
    description?: string
    isAdult: boolean
    genres: IGenre[] | null
    budget: number
    time: number
    posterUrl?: string
    backdropUrl?: string
}

export interface IUser {
    id: string;
    isActivated: boolean;
    email: string;
    name: string;
    surname: string;
}


export interface ILoginRequest {
    email: string;
    password: string;
}

export interface ILoginResponse {
    access_token: string;
    refresh_token: string;
}

export interface IRegisterRequest {
    name: string;
    surname: string;
    email: string;
    password: string;
}

export interface IRegisterResponse {
    access_token: string;
    refresh_token: string;
}