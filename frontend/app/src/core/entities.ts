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

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
}

export interface IRegistration {
  name: string;
  surname: string;
  email: string;
  password: string;
}

export interface ILogin {
  email: string;
  password: string;
}

export interface IRegisterResponse {
  refreshToken: string;
  accessToken: string;
}