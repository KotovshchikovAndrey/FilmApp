import React from "react"
import {IFilm} from "../../../core/entities"
import FilmCardItem from "./FilmCardItem"
import Grid from "@mui/material/Unstable_Grid2"
import {useAppSelector} from "../../../store";
import {Alert, Typography} from "@mui/material";
import FilmCardListSkeleton from "./FilmCardListSkeleton";


export default function FilmCardList() {
  const films = useAppSelector(state => state.film.films)
  const isLoading = useAppSelector(state => state.film.isLoading)
  const error = useAppSelector(state => state.film.errorMessage)
  return (
    <React.Fragment>
      {isLoading ? <FilmCardListSkeleton/> :

        <>{error ? <Alert severity="error">{error}</Alert> :
          <>{films.length ?
            <Grid container spacing={2}>
              {films.map((film: IFilm) => (
                <Grid xs={6} sm={4} md={3} key={film.id}>
                  <FilmCardItem id={film.id} title={film.title} posterUrl={film.posterUrl}/>
                </Grid>
              ))}
            </Grid>
            : <Alert severity="info">No results found</Alert>
          }</>}
        </>
      }

    </React.Fragment>
  )
}
