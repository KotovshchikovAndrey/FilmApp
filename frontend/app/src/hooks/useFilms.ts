import {useEffect, useState} from "react"
import {ICountry, IFilm, IFilmFilter, IFilmFilters, IGenre, InitialFilter} from "../core/entities"
import {IGetFilmsParams} from "../api/films"
import api from "../api"
import {API_URL} from "../core/config"
import Endpoints from "../api/endpoints"
import {Simulate} from "react-dom/test-utils";
import error = Simulate.error;

export const useFilms = () => {
  const [films, setFilms] = useState<IFilm[]>([])
  const [filter, setFilter] = useState<IFilmFilter>(InitialFilter)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")

  const fetchFilms = async (data: IGetFilmsParams) => {
    try {
      setIsLoading(true)
      const response = await api.films.getFilms(data)
      const filmsWithPosters = setPosters(response.data.films)
      setFilms(filmsWithPosters)
    } catch (e: any) {
      setError(e.message)
    } finally {
      setIsLoading(false)
    }
  }

  const setPosters = (films: IFilm[]) => {
    films.map(film => {
      film.posterUrl = `${API_URL}${Endpoints.FILMS.GET_POSTER(film.id)}`
    })
    return films
  }

  const getFilter = (filter: IFilmFilter) => {
    setFilter(filter)
  }

  useEffect(() => {
    fetchFilms({limit: 20, genre: filter.genre, country: filter.country})
  }, [filter])

  return {films, isLoading, error, getFilter}
}
