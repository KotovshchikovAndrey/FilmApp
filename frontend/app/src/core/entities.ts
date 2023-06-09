export interface IGenre {
  id: number
  name: string
}

export interface ICompany {
  id: number
  name: string
}

export interface ICountry {
  name: string
  iso_3166_1: string
}

export interface ITrailer {
  key: string
  site: string
}

export interface IFilm {
  id: number
  title: string
  is_adult: boolean
  description?: string
  language?: string
  budget: number
  release_date?: string
  time?: number
  genres: IGenre[] | null
  productionCompanies?: ICompany[] | null
  productionCountries?: ICountry[] | null
  posterUrl: string
  trailerUrl?: string
  is_favorite?: boolean
  watch_status?: string
}

export interface IUser {
  id: string
  name: string
  surname: string
  email: string
  status: string
  role: string
  films: IFilm[]
}

export interface ILoginRequest {
  email: string
  password: string
}

export interface IAuthResponse {
  access_token: string
  refresh_token: string
}

export interface IRegisterRequest {
  name: string
  surname: string
  email: string
  password: string
}

export interface IFilmFilterOptions {
  genres: IGenre[]
  countries: ICountry[]
}

export interface IFilmFilter {
  genre: IGenre | null
  country: ICountry | null
}

export const InitialFilter: IFilmFilter = {
  genre: null,
  country: null,
}
