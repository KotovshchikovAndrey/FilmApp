import { createSlice, PayloadAction } from "@reduxjs/toolkit"
import { IFilm, IFilmFilter } from "../core/entities"

export interface FilmsState {
  films: IFilm[]
  favoriteFilms: IFilm[]
  isLoading: boolean
  errorMessage: string
  filter: IFilmFilter
}

const initialState: FilmsState = {
  films: [],
  favoriteFilms: [],
  isLoading: false,
  errorMessage: "",
  filter: { genre: null, country: null },
}

export const filmSlice = createSlice({
  name: "film",
  initialState,
  reducers: {
    setFilms: (state, action: PayloadAction<IFilm[]>) => {
      state.films = action.payload
    },

    setFavoriteFilms: (state, action: PayloadAction<IFilm[]>) => {
      state.favoriteFilms = action.payload
    },

    setFilter: (state, action: PayloadAction<IFilmFilter>) => {
      state.filter = action.payload
    },

    setIsLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload
    },

    setErrorMessage: (state, action: PayloadAction<string>) => {
      state.errorMessage = action.payload
    },
  },
})

export default filmSlice.reducer
export const filmActions = filmSlice.actions
