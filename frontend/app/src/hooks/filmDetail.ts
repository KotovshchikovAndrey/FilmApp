import { useEffect, useState } from "react"
import { IFilm } from "../core/entities"
import api from "../api"
import { API_URL, POSTER_URL } from "../core/config"
import Endpoints from "../api/endpoints"

export const useFilmDetail = (filmId: number) => {
  const [film, setFilm] = useState<IFilm>({} as IFilm)
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState("")

  const token = localStorage.getItem("token") || undefined
  const fetchFilmDetail = async (filmId: number) => {
    setLoading(true)
    try {
      setErr("")
      const responseFilmDetail = await api.films.getFilmDetail(filmId, token)
      const responseTrailer = await api.films.getFilmTrailer(filmId)
      responseFilmDetail.data.posterUrl = `${API_URL}${Endpoints.FILMS.GET_POSTER(filmId)}`
      responseFilmDetail.data.trailerUrl = `${POSTER_URL}${responseTrailer.data.key}`
      setFilm(responseFilmDetail.data)
      console.log(responseFilmDetail.data)
      setLoading(false)
    } catch (e: any) {
      setErr(e.message)
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchFilmDetail(filmId)
  }, [])

  return { film, loading, err }
}
