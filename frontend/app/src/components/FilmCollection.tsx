import React from 'react';
import FilmFilters from "./shared/film/FilmFilters";
import FilmCardList from "./shared/film/FilmCardList";
import {useFilms} from "../hooks/useFilms";
import FilmCardListSkeleton from "./shared/film/FilmCardSkeleton";

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