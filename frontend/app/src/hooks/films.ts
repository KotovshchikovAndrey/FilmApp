import {useEffect, useState} from "react";
import {IFilm} from "../core/entities";
import {IGetFilmsParams} from "../api/films";
import api from "../api";
import {API_URL} from "../core/config";
import Endpoints from "../api/endpoints";
import {useSelector} from "react-redux";
import {useAppDispatch, useAppSelector} from "../store";
import {setFilmFetchState} from "../store/authReducer";

export const useFilms = () => {
    const isFilmFetched = useAppSelector(state => state.auth.isFilmFetched)
    const dispatch = useAppDispatch()
    const [films, setFilms] = useState<IFilm[]>([])
    const [loading, setLoading] = useState(false)
    const [err, setErr] = useState('')

    const fetchFilms = async (data: IGetFilmsParams) => {
        setLoading(true)
        try {
            setErr('')
            const response = await api.films.getFilms(data)
            // console.log(response.data)
            setPosters(response.data.films)
            setLoading(false)

        } catch (e: any) {
            setErr(e.message)
            setLoading(false)
            dispatch(setFilmFetchState(false))
        }
    }

    const setPosters = (films: IFilm[]) => {
        films.map((film: IFilm) => {
            film.posterUrl = `${API_URL}${Endpoints.FILMS.GET_POSTER(film.id)}`
            // console.log(film)
        })
        setFilms(films)
        dispatch(setFilmFetchState(true))
    }


    useEffect(() => {
        fetchFilms({limit: 20, random: false})
    }, [isFilmFetched])


    return {films, loading, err}
}