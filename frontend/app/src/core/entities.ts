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
  production_companies?: ICompany[] | null
  production_countries?: ICountry[] | null
  is_favorite?: boolean
  rating?: number
  watch_status?: string
  posterUrl: string
  trailerUrl?: string
}

export interface IUser {
  id: string
  name: string
  surname: string
  email: string
  status: string
  avatar?: string
  role: string
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

export interface IFilmRating {
  film_id: number
  rating: number
}

export const InitialFilter: IFilmFilter = {
  genre: null,
  country: null,
}

export interface ICommentAuthor {
  name: string
  surname: string
  avatar: string | null
}

export interface IChildComment {
  comment_id: number
  author: ICommentAuthor
  text: string
}

export interface IComment {
  comment_id: number
  author: ICommentAuthor
  text: string
  child_comments: IChildComment[]
}
