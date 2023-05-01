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

export interface IUser {}

export interface IToken {}
