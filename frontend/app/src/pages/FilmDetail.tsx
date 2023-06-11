import { Alert, Box, Button, CircularProgress, Stack, Typography } from "@mui/material"
import * as React from "react"
import { useNavigate, useParams } from "react-router-dom"
import Grid from "@mui/material/Unstable_Grid2"
import { Chip } from "@mui/material"
import { Add, Remove } from "@mui/icons-material"
import AspectRatio from "@mui/joy/AspectRatio"
import ArrowHeader from "../components/shared/Header/ArrowHeader"
import { IGenre } from "../core/entities"
import { useAppDispatch, useAppSelector } from "../store"
import { addFilmToFavorite, removeFilmFromFavorite } from "../store/actionCreators"
import { FilmCommentsList } from "../components/shared/film/FirmCommentsList"
import { IFilm } from "../core/entities"
import api from "../api"
import { API_URL, POSTER_URL } from "../core/config"
import Endpoints from "../api/endpoints"

let renderCount = 0
export default function FilmDetail() {
  renderCount += 1
  const dispatch = useAppDispatch()

  const isAuth = useAppSelector((state) => state.auth.isAuth)
  const userStatus = useAppSelector((state) => state.auth.status)
  const isLoading = useAppSelector((state) => state.auth.loading)

  const { id } = useParams()
  const filmId = parseInt(id!)

  const [film, setFilm] = React.useState<IFilm>({} as IFilm)
  const [isFilmFavorite, setIsFilmFavorite] = React.useState<boolean>(false)
  const [loading, setLoading] = React.useState(false)

  const token = localStorage.getItem("token") || undefined
  const fetchFilmDetail = async (filmId: number) => {
    setLoading(true)

    const responseFilmDetail = await api.films.getFilmDetail(filmId, token)
    const responseTrailer = await api.films.getFilmTrailer(filmId)

    const filmData = responseFilmDetail.data
    filmData.posterUrl = `${API_URL}${Endpoints.FILMS.GET_POSTER(filmId)}`
    filmData.trailerUrl = `${POSTER_URL}${responseTrailer.data.key}`

    setFilm(filmData)
    setIsFilmFavorite(filmData.is_favorite ?? false)
    setLoading(false)
  }

  React.useEffect(() => {
    fetchFilmDetail(filmId)
  }, [])

  const addFilmHandler = () => {
    dispatch(addFilmToFavorite(film.id))
    setIsFilmFavorite(true)
  }

  const removeFilmHandler = () => {
    dispatch(removeFilmFromFavorite(film.id))
    setIsFilmFavorite(false)
  }

  return (
    <React.Fragment>
      <ArrowHeader />
      {loading ? (
        <Box mt={20} display="flex" justifyContent="center">
          <CircularProgress size={100} />
        </Box>
      ) : (
        <Grid container spacing={5}>
          <Grid xs={12} sm={6}>
            {/*TODO Размер фото*/}
            <img style={{ maxWidth: "100%" }} src={film?.posterUrl} alt={film?.title} />
          </Grid>
          <Grid xs={12} sm={6}>
            <Stack spacing={2}>
              <Typography variant="h4" component="h1">
                {film.title} {renderCount}
              </Typography>
              <Typography variant="subtitle1">
                {film.release_date}, {film.time} мин, {film.is_adult ? "18+" : "0+"}
              </Typography>
              <Stack direction="row" spacing={1} useFlexGap flexWrap="wrap">
                {film.genres?.map((genre: IGenre) => (
                  <Chip label={genre.name} />
                ))}
              </Stack>
              {isAuth &&
                userStatus === "active" &&
                (isFilmFavorite ? (
                  <Button
                    variant="outlined"
                    color="error"
                    startIcon={isLoading ? <CircularProgress size={20} /> : <Remove />}
                    onClick={() => removeFilmHandler()}
                  >
                    Remove from collection
                  </Button>
                ) : (
                  <Button
                    variant="outlined"
                    startIcon={isLoading ? <CircularProgress size={20} /> : <Add />}
                    onClick={() => addFilmHandler()}
                  >
                    Add to collection
                  </Button>
                ))}
              <Typography variant="h5">Description</Typography>
              <Typography>{film.description}</Typography>
              <Typography variant="h5">Trailer</Typography>
              <AspectRatio>
                <iframe
                  src={film.trailerUrl}
                  title={film.title}
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                  allowFullScreen
                />
              </AspectRatio>
            </Stack>
          </Grid>
          <FilmCommentsList />
        </Grid>
      )}
    </React.Fragment>
  )
}
