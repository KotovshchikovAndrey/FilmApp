import { Alert, Box, Button, CircularProgress, Stack, Typography } from "@mui/material"
import * as React from "react"
import { useNavigate, useParams } from "react-router-dom"
import Grid from "@mui/material/Unstable_Grid2"
import { Chip } from "@mui/material"
import { Add } from "@mui/icons-material"
import AspectRatio from "@mui/joy/AspectRatio"
import ArrowHeader from "../components/shared/Header/ArrowHeader"
import { useFilmDetail } from "../hooks/filmDetail"
import { IGenre } from "../core/entities"
import { useAppDispatch, useAppSelector } from "../store"
import { addFilmToFavorite } from "../store/actionCreators"
import { authActions } from "../store/authReducer"

export default function FilmDetail() {
  const navigate = useNavigate()
  const dispatch = useAppDispatch()

  const isAuth = useAppSelector((state) => state.auth.isAuth)
  const userStatus = useAppSelector((state) => state.auth.status)
  const isLoading = useAppSelector((state) => state.auth.loading)

  const { id } = useParams()
  const filmId = parseInt(id!)

  // TODO разделить фетч фильма и трейлера на 2 useFetching
  const { film, loading, err } = useFilmDetail(filmId)

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
                {film.title}
              </Typography>
              <Typography variant="subtitle1">
                {film.release_date}, {film.time} мин, {film.isAdult ? "18+" : "0+"}
              </Typography>
              <Stack direction="row" spacing={1} useFlexGap flexWrap="wrap">
                {film.genres?.map((genre: IGenre) => (
                  <Chip label={genre.name} />
                ))}
              </Stack>
              {isAuth && userStatus === "active" && (
                <Button
                  variant="outlined"
                  startIcon={isLoading ? <CircularProgress size={20} /> : <Add />}
                  onClick={() => dispatch(addFilmToFavorite(filmId))}
                >
                  Add to collection
                </Button>
              )}
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
        </Grid>
      )}
    </React.Fragment>
  )
}
