import { useEffect, useState } from "react"
import { IFilm } from "../core/entities"
import { IGetFilmsParams } from "../api/films"
import api from "../api"
import { API_URL } from "../core/config"
import Endpoints from "../api/endpoints"

export const useFilms = () => {
  const [films, setFilms] = useState<IFilm[]>([])
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState("")

  const fetchFilms = async (data: IGetFilmsParams) => {
    setLoading(true)
    try {
      setErr("")
      const response = await api.films.getFilms(data)
      // console.log(response.data)
      setPosters(response.data.films)
      setLoading(false)
    } catch (e: any) {
      setErr(e.message)
      setLoading(false)
    }
  }

  const setPosters = (films: IFilm[]) => {
    films.map((film: IFilm) => {
      film.posterUrl = `${API_URL}${Endpoints.FILMS.GET_POSTER(film.id)}`
      // console.log(film)
    })
    setFilms(films)
  }

  useEffect(() => {
    fetchFilms({ limit: 20, random: false })
  }, [])

  return { films, loading, err }
}
