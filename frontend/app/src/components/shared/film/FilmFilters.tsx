import {Autocomplete, TextField} from "@mui/material"
import React, {useEffect, useState} from "react"
import Grid from "@mui/material/Unstable_Grid2"

import api from "../../../api"
import {IFilmFilter, IFilmFilters, IGenre, InitialFilter} from "../../../core/entities"

interface FilmFiltersProps {
  getFilter: (filter: IFilmFilter) => void;
}


export default function FilmFilters({getFilter}: FilmFiltersProps) {
  const [filters, setFilters] = useState<IFilmFilters>()
  const [filterValue, setFilterValue] = useState<IFilmFilter>(InitialFilter)

  useEffect(() => {
    const fetchFilmFilters = async () => {
      const response = await api.films.getFilmFilters()
      setFilters(response.data)
    }

    fetchFilmFilters()
  }, [])

  useEffect(()=> {
    getFilter(filterValue)
  }, [filterValue])

  return (
    <React.Fragment>
      <Grid container spacing={2}>
        <Grid xs={12} md>
          <Autocomplete
            size="small"
            disablePortal
            options={filters ? filters.genres.map((genre) => genre.name) : []}
            // onSelect={(event: React.ChangeEvent<HTMLInputElement>) =>
            //   console.log(event.target.value)
            // }
            renderInput={(params) => <TextField {...params} label="Жанр"/>}
            value={filterValue.genre}
            onChange={(event: any, newValue, reason) => {
              setFilterValue({...filterValue, genre: newValue});
            }}
          />
        </Grid>
        <Grid xs={12} md>
          <Autocomplete
            size="small"
            disablePortal
            options={filters ? filters.countries.map((country) => country.name) : []}
            renderInput={(params) => <TextField {...params} label="Страна"/>}
            value={filterValue.country}
            onChange={(event: any, newValue, reason) => {
              setFilterValue({...filterValue, country: newValue});
            }}
          />
        </Grid>
      </Grid>
    </React.Fragment>
  )
}
