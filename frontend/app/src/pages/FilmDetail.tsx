import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Box,
  Button,
  CircularProgress, IconButton, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Paper, Skeleton,
  Stack, Table, TableBody, TableCell, TableContainer, TableRow, ToggleButton,
  Typography
} from "@mui/material"
import * as React from "react"
import {useParams} from "react-router-dom"
import Grid from "@mui/material/Unstable_Grid2"
import {Chip} from "@mui/material"
import {Add, Remove} from "@mui/icons-material"
import AspectRatio from "@mui/joy/AspectRatio"
import ArrowHeader from "../components/shared/Header/ArrowHeader"
import {IGenre} from "../core/entities"
import {useAppDispatch, useAppSelector} from "../store"
import {addFilmToFavorite, refreshToken, removeFilmFromFavorite} from "../store/actionCreators"
import {FilmCommentsList} from "../components/shared/film/FirmCommentsList"
import {IFilm} from "../core/entities"
import api from "../api"
import {API_URL, POSTER_URL} from "../core/config"
import Endpoints from "../api/endpoints"
import {FilmStarRating} from "../components/shared/film/FilmStarRating"
import FavoriteIcon from '@mui/icons-material/Favorite';
import HeartBrokenIcon from '@mui/icons-material/HeartBroken';

export default function FilmDetail() {
  const dispatch = useAppDispatch()

  const isAuth = useAppSelector((state) => state.auth.isAuth)
  const userStatus = useAppSelector((state) => state.auth.status)
  const isLoading = useAppSelector((state) => state.auth.loading)

  const {id} = useParams()
  const filmId = parseInt(id!)

  const [film, setFilm] = React.useState<IFilm>({} as IFilm)
  const [isFilmFavorite, setIsFilmFavorite] = React.useState<boolean>(false)
  const [userRating, setUserRating] = React.useState<number>(0)
  const [loading, setLoading] = React.useState(false)

  const token = localStorage.getItem("token") || undefined
  const fetchFilmDetail = async (filmId: number) => {
    setLoading(true)

    let responseFilmDetail
    try {
      responseFilmDetail = await api.films.getFilmDetail(filmId, token)
    } catch (err) {
      responseFilmDetail = await api.films.getFilmDetail(filmId)
      dispatch(refreshToken())
    }

    const responseTrailer = await api.films.getFilmTrailer(filmId)
    const filmData = responseFilmDetail.data

    filmData.posterUrl = `${API_URL}${Endpoints.FILMS.GET_POSTER(filmId)}`
    filmData.trailerUrl = `${POSTER_URL}${responseTrailer.data.key}`

    setFilm(filmData)
    setIsFilmFavorite(filmData.is_favorite ?? false)
    setUserRating(filmData.rating ?? 0)
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

  console.log(film)

  return (
    <React.Fragment>
      <ArrowHeader/>
      {/*{loading ? (*/}
      {/*  <Box mt={20} display="flex" justifyContent="center">*/}
      {/*    <CircularProgress size={100}/>*/}
      {/*  </Box>*/}
      {/*) : (*/}
      <Grid container spacing={5}>
        <Grid xs={12} sm={6}>
          <AspectRatio ratio={2 / 3}>
            {loading ? <Skeleton variant="rectangular" width="100%" height="100%"/> :
              <img style={{width: "100%", height: "100%"}} src={film?.posterUrl} alt={film?.title}/>}
          </AspectRatio>
        </Grid>
        <Grid xs={12} sm={6}>
          <Stack spacing={2}>

            <Typography variant="h3">
              {loading ? <Skeleton height={100}/> : film.title}
            </Typography>
            <Stack direction="row" spacing={5} justifyContent="space-between">

              {loading ? <Skeleton variant="rectangular" width={260} height={75}/> :
                (isAuth && userStatus === "active" &&
                    <FilmStarRating key={filmId} filmId={filmId} userRating={userRating}/>)}
              {loading ? <Skeleton variant="circular" width={75} height={75}/> :
                (isAuth &&
                  userStatus === "active" &&
                  (isFilmFavorite ? (
                    <IconButton sx={{width: 75, height: 75}} color="error" onClick={() => removeFilmHandler()}>
                      {isLoading ? <CircularProgress size={40}/> : <FavoriteIcon sx={{fontSize: 40}}/>}

                    </IconButton>
                  ) : (
                    <IconButton sx={{width: 75, height: 75}} onClick={() => addFilmHandler()}>
                      {isLoading ? <CircularProgress size={40}/> : <FavoriteIcon sx={{fontSize: 40}}/>}
                    </IconButton>
                  )))
              }
            </Stack>

            <TableContainer component={Paper} elevation={0}>
              {loading ? <Skeleton variant="rectangular" height={380}/> :
                <Table>
                  <TableBody>
                    <TableRow>
                      <TableCell>Release year</TableCell>
                      <TableCell>{film.release_date ? film.release_date.split("-")[0] : "—"}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Countries</TableCell>
                      <TableCell>{film.production_countries ? film.production_countries.map(country => country.name).join(", ") : "—"}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Genres</TableCell>
                      <TableCell>{film.genres ? film.genres.map(genre => genre.name).join(", ") : "—"}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Production companies</TableCell>
                      <TableCell>{film.production_companies ? film.production_companies.map(company => company.name).join(", ") : "—"}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Running time</TableCell>
                      <TableCell>{film.time ? `${film.time} minutes` : "—"}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Age Rating</TableCell>
                      <TableCell>{film.is_adult ? "18+" : "0+"}</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>Budget</TableCell>
                      <TableCell>{film.budget ? `$${film.budget}` : "—"}</TableCell>
                    </TableRow>
                  </TableBody>
                </Table>}
            </TableContainer>

            <Typography variant="h5">{loading ? <Skeleton height={50}/> : "Description"}</Typography>
            <Typography>{loading ? <Skeleton height={200}/> : film.description}</Typography>
            <Typography variant="h5">{loading ? <Skeleton height={50}/> : "Trailer"}</Typography>
            <AspectRatio>
              {loading ? <Skeleton variant="rectangular"/> :
                <iframe
                  src={film.trailerUrl}
                  title={film.title}
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                  allowFullScreen
                />}
            </AspectRatio>
          </Stack>
        </Grid>
      </Grid>
      <FilmCommentsList key={filmId} filmId={filmId}/>
    </React.Fragment>
  )
}
