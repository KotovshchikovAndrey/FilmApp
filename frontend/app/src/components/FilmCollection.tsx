import React, {useEffect, useState} from 'react';
import {Box, CircularProgress, Typography} from "@mui/material";
import FilmFilters from "./shared/film/FilmFilters";
import FilmCardList from "./shared/film/FilmCardList";
import {useFilms} from "../hooks/useFilms";
import api from "../api";
import {IFilm} from "../core/entities";
import FilmCardListSkeleton from "./shared/film/FilmCardSkeleton";
import {getFilmFilters} from "../api/films";

function FilmCollection() {
  const {films, isLoading, error, getFilter} = useFilms()


  return (
    <React.Fragment>
      <FilmFilters getFilter={getFilter}/>
      {isLoading ? <FilmCardListSkeleton/> :
        <FilmCardList films={films}/>}
    </React.Fragment>
  );
}

export default FilmCollection;