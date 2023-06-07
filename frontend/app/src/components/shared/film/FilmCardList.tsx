import React from "react"
import {IFilm} from "../../../core/entities"
import FilmCardItem from "./FilmCardItem"
import Grid from "@mui/material/Unstable_Grid2"
import FilmCardSkeleton from "./FilmCardSkeleton";

interface FilmCardListProps {
  films: IFilm[],
}

export default function FilmCardList({films}: FilmCardListProps) {
  return (
    <React.Fragment>
      <Grid container spacing={2}>
        {films.map((film: IFilm) => (
          <Grid xs={6} sm={4} md={3} key={film.id}>
            <FilmCardItem id={film.id} title={film.title} posterUrl={film.posterUrl}/>
          </Grid>
        ))}
      </Grid>
    </React.Fragment>
  )
}
