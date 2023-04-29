export interface Genre {
  id: number
  name: string
}

export interface Film {
  id: number
  name: string
  genre: Genre[]
  budget: number
  runtime: number
  posterUrl?: string
  backdropUrl?: string
}

export interface User {}

export interface Token {}
