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
    name: string;
    surname: string;
    email: string;
    status: string;
    role: string;
    films: IFilm[];
}


export interface ILoginRequest {
    email: string;
    password: string;
}

export interface IAuthResponse {
    access_token: string;
    refresh_token: string;
}

export interface IRegisterRequest {
    name: string;
    surname: string;
    email: string;
    password: string;
}
