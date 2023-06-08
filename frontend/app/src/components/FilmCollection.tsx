import React from 'react';
import FilmFilters from "./shared/film/FilmFilters";
import FilmCardList from "./shared/film/FilmCardList";
import FilmCardListSkeleton from "./shared/film/FilmCardListSkeleton";
import {Alert} from "@mui/material";
import {useAppSelector} from "../store";

function FilmCollection() {

  return (
    <React.Fragment>
      <FilmFilters/>
      <FilmCardList/>
    </React.Fragment>
  );
}

export default FilmCollection;